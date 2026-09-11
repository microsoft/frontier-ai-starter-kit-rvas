# AI Grounding: build answers people can trust

Build toward a grounded, permission-aware assistant over approved content. Prove it before it ships.

The eight modules guide a pilot build. Each asks for evidence
from your resources. You deploy Azure resources, index a synthetic
corpus, compare models, and test the failures that matter before anyone uses the assistant.

## Before you start

**Verify the API surface before you write code.** Foundry and Azure AI Search move fast and several
capabilities used here are preview. Re-check current Microsoft Learn guidance before writing SDK
code; do not infer a signature from this course or from memory.

**Fictional data only.** The corpus in `accelerator/sample-data/` is a synthetic returns-policy set
for a fictional retailer. Never copy customer content into this repository.

**Setup.** Use Bash, Azure CLI, Bicep, and Python 3 in a virtual environment. Your Azure account
needs permission to create the resources and role assignments. Install the Python packages listed
in [the facilitator reference](accelerator/solution.md#prerequisites).

**Access.** The main data paths use `DefaultAzureCredential`, managed identity, and RBAC.
The permission probe uses a separate client secret, and the template configures an Application
Insights connection string. The storage account disables shared-key access.

**Known implementation gaps:** the shipped path does not yet prove per-document permissions,
retrieval recall, or agent-level evaluation. Read the
[accelerator limits](accelerator/README.md#known-implementation-gaps) before treating results as a release gate.

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
| [8. Deploy and surface it to users](lesson.html?scenario=ai-grounding&lesson=deploy-and-surface) | A pinned agent version and permission-aware surface | Deployed surface passes anonymous, authorized, and restricted HTTP checks |

Most teams run into trouble in modules 5 through 7. They add an agent before retrieval works, copy
live data into an index, or ship without a release gate. Module 8 checks another common failure:
the final app must preserve the retrieval layer's permission boundary.

## Decision gates to carry into the customer conversation

Answer these questions before opening the reference library:

| Gate | Decide before building |
|---|---|
| Knowledge boundary | Which approved sources may be cited, who owns them, and what version/freshness is acceptable? |
| Permission boundary | Which identity is evaluated at query time, and what should access-denied retrieval return? |
| Live-data boundary | Which questions require a live system/tool instead of an indexed document snapshot? |
| Trust boundary | Which cited-answer, abstention, stale-data, and restricted-source failures block a pilot? |
| Operating boundary | Who can see traces, who investigates a bad answer, and what rollback or pause action exists? |

## Deploy the foundation

Run commands from the repository root.

```bash
az login
./scenarios/ai-grounding/accelerator/scripts/deploy.sh rg-ai-grounding eastus2
```

The deployment writes `accelerator/.env` from the template outputs. Later modules read that file,
so keep it local and do not commit it.

For shell commands in the lessons, load the generated values into your current shell:

```bash
set -a
source scenarios/ai-grounding/accelerator/.env
set +a
export AZURE_KNOWLEDGE_BASE_NAME=grounding-kb
```

## Run the scripts

These scripts call your Azure resources directly. They need a subscription and the `.env` file.
There is no offline mode. An offline pass cannot tell you whether retrieval works.

```bash
# Create the knowledge source and knowledge base
# First upload the approved corpus using module 3, then wait for ingestion to finish.
python3 scenarios/ai-grounding/accelerator/scripts/build_knowledge_source.py

# Check the permission boundary with a second, lower-privileged identity
python3 scenarios/ai-grounding/accelerator/scripts/probe_permissions.py --knowledge-base grounding-kb

# Compare candidate models on your own golden questions
python3 scenarios/ai-grounding/accelerator/scripts/compare_models.py --deployments chat chat-candidate

# Run the golden questions and read citations, abstention, and recall@5
python3 scenarios/ai-grounding/accelerator/scripts/grounded_answer.py --knowledge-base grounding-kb

# Verify the deployed surface with tokens held only in environment variables
python3 scenarios/ai-grounding/accelerator/scripts/probe_surface.py \
  --endpoint "https://<your-surface>/<route>" \
  --authorized-token-env SURFACE_AUTHORIZED_TOKEN \
  --restricted-token-env SURFACE_RESTRICTED_TOKEN
```

Each lesson's **Verify** section lists the specific commands and signals for that module.

## Reused activities

These lessons reuse the kit's implementation activities:

- [Foundations](activity.html?id=foundations) — provisioning, model selection, and
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

- Treat retrieved text as untrusted data, never as instructions. Module 7 tests this directly.
- Index knowledge and route to systems. Indexing live operational data produces confidently cited,
  stale answers. That is the worst failure mode in this scenario.
- A refusal must be indistinguishable from "no information exists." Revealing that a restricted
  document exists is still a leak.
- Make retrieval work before adding an agent. An agent over weak retrieval makes failures fluent,
  not correct.
