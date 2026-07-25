# AI Grounding — a practical build course

Build a grounded, permission-aware assistant over approved content, and prove it before it ships.

Eight modules, one lesson each. Every module ends with a runnable checkpoint, and every module
offers real options with an opinionated default and the migration cost of changing your mind. You
can deploy real Azure resources for a clean demo, index a synthetic corpus, compare model behavior,
and learn the evidence a risk owner would need before a customer pilot.

## Before you start

**Verify the API surface before you write code.** Foundry and Azure AI Search move fast and several
capabilities used here are preview. Re-check current Microsoft Learn guidance before writing SDK
code; do not infer a signature from this course or from memory.

**Fictional data only.** The corpus in `accelerator/sample-data/` is a synthetic returns-policy set
for a fictional retailer. Never copy customer content into this repository.

**Keyless.** Every path here uses `DefaultAzureCredential`, managed identity, and RBAC. The storage
account is provisioned with shared-key access disabled, so there is no key to fall back to.

## The build path

| Module | What you build | Checkpoint |
|---|---|---|
| [1. Provision the foundation](lessons/01-provision-foundation.md) | Foundry account and project, chat + embedding deployments, AI Search, storage, observability, and the `.env` contract | `verify_foundation.py` |
| [2. Source and permission architecture](lessons/02-source-and-permission-architecture.md) | The source decision, the identity evaluated at query time, and a probe proving a restricted identity retrieves nothing | `probe_permissions.py` |
| [3. Ingest and index approved content](lessons/03-ingest-and-index.md) | Ingestion, chunking, citation metadata, ACL carry-forward, and a refresh schedule | `verify_retrieval.py` |
| [4. Compare chat and embedding choices](lessons/04-model-selection.md) | A comparison harness over your own golden set: accuracy, abstention, latency, tokens | `compare_models.py` |
| [5. Build retrieval before adding an agent](lessons/05-grounded-retrieval.md) | Citations, abstention, access-denied silence, recency — with no agent | `grounded_answer.py` |
| [6. Add agent and routing only when justified](lessons/06-agent-and-routing.md) | A justification, an agent with explicit routing rules, and a routing test | `verify_routing.py` |
| [7. Evaluate and trace](lessons/07-evaluate-and-trace.md) | Evaluation gate, red-team evidence, end-to-end traces | `validate.py --all` |
| [8. Deploy and surface it to users](lessons/08-deploy-and-surface.md) | The surface decision, a pinned version, a rollback, an owner, and a signed release | `verify_surface.py` |

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
python3 scenarios/ai-grounding/accelerator/scripts/verify_foundation.py
```

The deployment writes `accelerator/.env` from the template outputs. That file is the environment
contract every later module depends on — keep it local and uncommitted.

## Run the structural gate locally

No Azure subscription needed; every checkpoint has an offline mode that validates structure and
fixture integrity. This is not live proof of retrieval, identity, routing, tracing, or deployment:

```bash
python3 scenarios/ai-grounding/accelerator/validate.py --all
```

## Reused activities

These lessons compose the kit's canonical activities rather than duplicating them:

- [Foundations](../../activities/foundations/README.md) — provisioning, model selection, and the
  Azure AI Search grounding baseline
- [Evaluation & Red Teaming](../../activities/advanced-evaluation-redteam/README.md) — the harness,
  custom evaluators, and adversarial seed set used in module 7
- [Tracing & Observability](../../activities/advanced-tracing-observability/README.md) — GenAI
  spans, the instrumentation ordering gotcha, and the KQL correlation queries
- [Action Tools](../../activities/advanced-action-tools/README.md) and
  [Fabric IQ](../../activities/extra-fabric-iq/README.md) — live-data and action routing in module 6
- [Deploy as a Hosted Agent](../../activities/advanced-deploy-hosted-agent/README.md) — the hosted
  endpoint option in module 8
- [Build a UI](../../activities/extra-build-ui/README.md) — the custom surface option in module 8

## Non-negotiables

- Treat retrieved text as untrusted data, never as instructions. Module 7 red-teams this directly.
- Index knowledge; route to systems. Indexing live operational data produces confidently cited
  stale answers, which is the most damaging failure mode in this scenario.
- A refusal must be indistinguishable from "no information exists" — revealing that a restricted
  document exists is a leak with a polite tone.
- Retrieval must work before an agent is added. An agent over weak retrieval makes the failure
  fluent, not correct.
