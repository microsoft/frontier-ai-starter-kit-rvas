# AI Grounding — a practical build course

Build a grounded, permission-aware assistant over approved content, and prove it before it ships.

Eight modules, one lesson each. Every module ends with something you can see working against your
own resources, and every module offers real options with an opinionated default and the migration
cost of changing your mind. You can deploy real Azure resources for a clean demo, index a synthetic
corpus, compare model behavior, and learn the evidence a risk owner would need before a customer
pilot.

## Before you start

**Verify the API surface before you write code.** Foundry and Azure AI Search move fast and several
capabilities used here are preview. Re-check current Microsoft Learn guidance before writing SDK
code; do not infer a signature from this course or from memory.

**Fictional data only.** The corpus in `accelerator/sample-data/` is a synthetic returns-policy set
for a fictional retailer. Never copy customer content into this repository.

**Keyless.** Every path here uses `DefaultAzureCredential`, managed identity, and RBAC. The storage
account is provisioned with shared-key access disabled, so there is no key to fall back to.

## The build path

| Module | What you build | Outcome |
|---|---|---|
| [1. Provision the foundation](lesson.html?scenario=ai-grounding&lesson=foundation) | Foundry account and project, chat + embedding deployments, AI Search, storage, observability, and the `.env` contract | Foundations Step 1 |
| [2. Source and permission architecture](lesson.html?scenario=ai-grounding&lesson=source-selection) | The source decision, the identity evaluated at query time, and a probe proving a restricted identity retrieves nothing | Signed source, access, freshness, and system-of-record decision |
| [3. Ingest and index approved content](lesson.html?scenario=ai-grounding&lesson=ingestion) | Ingestion, chunking, citation metadata, ACL carry-forward, and a refresh schedule | Approved documents are discoverable with source metadata |
| [4. Compare chat and embedding choices](lesson.html?scenario=ai-grounding&lesson=model-selection) | A comparison harness over your own golden set: accuracy, abstention, latency, tokens | Foundations Step 2 |
| [5. Build retrieval before adding an agent](lesson.html?scenario=ai-grounding&lesson=grounded-app) | Citations, abstention, access-denied silence, recency — with no agent | Foundations Step 4 |
| [6. Add agent and routing only when justified](lesson.html?scenario=ai-grounding&lesson=agent-routing) | A justification, an agent with explicit routing rules, and a routing test | Policy and live-data questions route to the correct source |
| [7. Evaluate and trace](lesson.html?scenario=ai-grounding&lesson=evaluate-and-trace) | Evaluation gate, red-team evidence, end-to-end traces | Evaluation gate passed with trace and red-team evidence |
| [8. Deploy and surface it to users](lesson.html?scenario=ai-grounding&lesson=deploy-and-surface) | The surface decision, a pinned version, a rollback, an owner, and a signed release | Surface release contract complete and the unauthenticated caller refused |

Modules 5, 6, and 7 contain the decisions that most often go wrong: teams add an agent before
retrieval works, index live data instead of routing to it, and ship without an evaluation gate.
Module 8 catches the fourth: shipping to a surface that quietly loses the permission boundary
everything else was built to protect.

## Decision gates to carry into the customer conversation

Use these gates before opening reference-library mechanics:

| Gate | Decide before building |
|---|---|
| Knowledge boundary | Which approved sources may be cited, who owns them, and what version/freshness is acceptable? |
| Permission boundary | Which identity is evaluated at query time, and what should access-denied retrieval return? |
| Live-data boundary | Which questions require a live system/tool instead of an indexed document snapshot? |
| Trust boundary | Which cited-answer, abstention, stale-data, and restricted-source failures block a pilot? |
| Operating boundary | Who can see traces, who investigates a bad answer, and what rollback or pause action exists? |

## Deploy the foundation

```bash
az login
./scenarios/ai-grounding/accelerator/scripts/deploy.sh rg-ai-grounding eastus2
```

The deployment writes `accelerator/.env` from the template outputs. That file is the environment
contract every later module depends on — keep it local and uncommitted.

## Run the scripts

The accelerator ships four scripts that do real work against your own Azure resources. They need a
subscription and the `.env` contract; there is no offline mode, because a script that passes without
touching Azure tells you nothing about whether your grounding works.

```bash
# Create the knowledge source and knowledge base
python3 scenarios/ai-grounding/accelerator/scripts/build_knowledge_source.py

# Check the permission boundary with a second, lower-privileged identity
python3 scenarios/ai-grounding/accelerator/scripts/probe_permissions.py --knowledge-base grounding-kb

# Compare candidate models on your own golden questions
python3 scenarios/ai-grounding/accelerator/scripts/compare_models.py --deployments chat chat-candidate

# Run the golden questions and read citations, abstention, and recall@5
python3 scenarios/ai-grounding/accelerator/scripts/grounded_answer.py --knowledge-base grounding-kb
```

Each lesson's **Verify** section lists the specific commands and signals for that module.

## Reused activities

These lessons compose the kit's canonical activities rather than duplicating them:

- [Foundations](activity.html?id=foundations) — provisioning, model selection, and the
  Azure AI Search grounding baseline
- [Evaluation & Red Teaming](activity.html?id=advanced-evaluation-redteam) — the harness,
  custom evaluators, and adversarial seed set used in module 7
- [Tracing & Observability](activity.html?id=advanced-tracing-observability) — GenAI
  spans, the instrumentation ordering gotcha, and the KQL correlation queries
- [Action Tools](activity.html?id=advanced-action-tools) and
  [Fabric IQ](activity.html?id=extra-fabric-iq) — live-data and action routing in module 6
- [Deploy as a Hosted Agent](activity.html?id=advanced-deploy-hosted-agent) — the hosted
  endpoint option in module 8
- [Build a UI](activity.html?id=extra-build-ui) — the custom surface option in module 8

## Non-negotiables

- Treat retrieved text as untrusted data, never as instructions. Module 7 red-teams this directly.
- Index knowledge; route to systems. Indexing live operational data produces confidently cited
  stale answers, which is the most damaging failure mode in this scenario.
- A refusal must be indistinguishable from "no information exists" — revealing that a restricted
  document exists is a leak with a polite tone.
- Retrieval must work before an agent is added. An agent over weak retrieval makes the failure
  fluent, not correct.
