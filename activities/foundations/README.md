# Foundations — Reusable Foundry mechanics reference

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> Reference module for the shared Foundry mechanics used by the scenario tracks: provision a
> keyless project, compare models, create a named agent, and ground that agent with Azure AI Search.
> Use the sample organization corpus only as a replaceable placeholder when your scenario does not
> already provide approved data.

## How to use this reference

This module is not a parallel scenario track. Scenario lessons own the customer decision record and
the order of work. Use the steps below only when a scenario points you to the reusable mechanics:

- **Step 1** — provision the keyless Foundry + AI Search foundation and export the `.env` contract.
- **Step 2** — compare model deployments and reproduce the selected behavior in code.
- **Step 3** — create a named, versioned prompt agent.
- **Step 4** — attach an Azure AI Search grounding source and require citations.

If your scenario already has a dedicated foundation lesson, follow that lesson first and use this
module as the mechanics reference for commands, environment names, and verification shape.

### Replaceable sample path

The examples use a fictional sample organization IQ assistant so the commands have concrete payloads.
Replace the assistant name, instructions, questions, and corpus with the approved data from your
scenario or customer build.

| Step | What the assistant can do afterward |
|---|---|
| 1 · Setup | Nothing yet — your infrastructure is live and authenticated |
| 2 · Model & Playground | Answer generic questions with a model and system instructions you chose |
| 3 · First Agent | Run as a named, versioned agent with a persona and guardrails |
| 4 · Knowledge Base | Answer from an approved corpus, with citations |

### What you need before you start

- The repo open in GitHub Codespaces or a local Dev Container (Python + Azure CLI + `azd`).
- An Azure subscription where you can create AI resources.
- Enough time to complete the specific mechanics your scenario references.

> Verification is machine-checkable when you use the provided sample assets. Each step ends with
> `python activities/foundations/validate.py --step N`; the final
> `python activities/foundations/validate.py --all` asserts the complete grounded-agent mechanics.

---

## Step 1 — Setup & Provisioning (Foundry + AI Search)

**Goal:** Provision the full session footprint with one command and confirm keyless Entra auth works end-to-end.

**Tasks:**
1. Open the repository in GitHub Codespaces (use the Open in GitHub Codespaces button in the root `README.md`) or in a local Dev Container. When the build finishes, confirm your toolchain in a terminal:
   ```bash
   python --version
   az --version
   azd version
   ```
2. Sign in to Azure from both the CLI and `azd`, then select the correct subscription for the event:
   ```bash
   az login
   azd auth login
   az account list --output table
   az account set --subscription "<your-subscription-name-or-id>"
   ```
3. Provision everything with one `azd up`. This deploys, via Bicep, a Foundry resource
   (project-management enabled), a Foundry project, a chat model deployment, an Azure AI
   Search service, and Log Analytics + Application Insights:
   ```bash
   azd up
   ```
   > If `azd up` is blocked by quota or region limits, use the Bash fallback `./scripts/deploy.sh`
   > and pick a supported region when prompted.
4. Export the `azd` environment to `.env`, then confirm it holds your resource contract (do not commit it).

   > What is the `.env` contract? `azd up` writes outputs to the selected `azd` environment.
   > Export them with `azd env get-values > .env`; that file contains your resource
   > endpoints, deployment names, and connection strings. Every script in this repo loads it
   > automatically via `python-dotenv` (`load_dotenv()`). It is git-ignored — never commit it.

   At minimum it contains the project endpoint, the model deployment name, and the search endpoint:
   ```bash
   azd env get-values > .env
   grep -E "AZURE_AI_PROJECT_ENDPOINT|AZURE_AI_MODEL_DEPLOYMENT_NAME|AZURE_SEARCH_ENDPOINT" .env
   ```
5. Verify keyless authentication works (no API keys — `DefaultAzureCredential` reuses your
   `az login` session).

   > Why keyless auth? `DefaultAzureCredential` (from `azure-identity`) checks your `az login`
   > session and requests a short-lived token from Entra. Access is governed by your Azure RBAC
   > roles — no secrets to rotate or accidentally commit.

   Open the [Microsoft Foundry portal](https://ai.azure.com/), confirm your new
   project is listed, and browse Discover → Models to see the catalog.

**Success Criteria:**
- [ ] `azd up` completes and reports the Foundry, AI Search, and App Insights resources as provisioned.
- [ ] A generated `.env` exists with `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, and `AZURE_SEARCH_ENDPOINT` populated (no placeholder `<...>` values).
- [ ] Your project appears in the Foundry portal and the model catalog opens under Discover → Models.
- [ ] No API keys are pasted anywhere — auth flows through `DefaultAzureCredential`.

**Verify:** Provisioning and auth are verified programmatically.
```bash
python activities/foundations/validate.py --step 1
```

---

## Step 2 — Model Selection & the Playground

**Goal:** Choose a model for the assistant by comparing two contrasting models in the Playground, tune the system instructions, then reproduce that behavior in code.

**Tasks:**
1. `azd up` deployed the model named by `.env`'s `AZURE_AI_MODEL_DEPLOYMENT_NAME`; this is the
   deployment you carry forward through Foundations. In
   the Foundry portal, go to Discover → Models and deploy one contrasting model to compare it
   against — a faster, lower-cost option such as `gpt-4.1-mini`, or a different family such as `phi-4`.
   Wait until the new deployment status reads Succeeded / Ready.
2. Open the Chat Playground, select that deployment, and set a starting system
   instruction for the assistant:
   ```text
   You are the approved scenario assistant. Answer in a warm, clear tone for the intended
   audience. If you are unsure or the information is missing, say so plainly and point the
   user to the right owner rather than guessing.
   ```
   Send a few scenario-specific questions and note tone, structure, and accuracy:
   - "How do I apply for scholarships?"
   - "What computer science programs do you offer?"
   - "Can I register late for classes?"
3. Switch the Playground to your second model and run the same prompts. Compare on four axes:
   answer detail, latency, tone, and suitability for the scenario assistant. Change only the
   model between runs so the comparison is fair.
4. Iterate on the system instruction until the smaller model behaves well: define audience, tone,
   how to handle missing information, and what is out of scope. Save your best version to
   `activities/foundations/assets/system-instructions.txt`.
5. Reproduce the Playground behavior in code. Create `activities/foundations/app/step2_chat.py`
   and call your chosen deployment through the project's OpenAI client.

   > Responses API — the stateless OpenAI-compatible endpoint used throughout this session.
   > `openai.responses.create(model=..., instructions=..., input=...)` sends a single prompt and
   > returns a reply. In later steps you'll pass an `agent_reference` in `extra_body` to route the
   > call through your named agent instead.

   ```python
   import os
   from pathlib import Path
   from azure.ai.projects import AIProjectClient
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv

   load_dotenv()

   project = AIProjectClient(
       endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )
   openai = project.get_openai_client()

   instructions_path = Path(__file__).resolve().parents[1] / "assets" / "system-instructions.txt"
   with instructions_path.open(encoding="utf-8") as f:
       system_instructions = f.read()

   response = openai.responses.create(
       model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
       instructions=system_instructions,
       input="How do I apply for scholarships at the sample organization?",
   )
   print(response.output_text)
   ```
   Run it: `python activities/foundations/app/step2_chat.py`. The code answer should match the tone you tuned in the Playground.

**Success Criteria:**
- [ ] Two contrasting models are deployed and visible in the Models / Deployments view.
- [ ] You ran the same prompts against both models and can state one concrete trade-off (cost, latency, tone, or detail).
- [ ] A tuned system instruction is saved to `assets/system-instructions.txt`.
- [ ] `python activities/foundations/app/step2_chat.py` prints an on-tone answer using `responses.create()` and `DefaultAzureCredential` (no API key).

**Verify:** The deployments exist and the SDK call succeeds.
```bash
python activities/foundations/validate.py --step 2
```

---

## Step 3 — Your First Agent

**Goal:** Promote your system instructions into a named, versioned Foundry agent with a persona and guardrails — created both in the portal and via the SDK.

**Tasks:**
1. Decide the agent's identity. Build on your Step 2 system instructions, adding guardrails and
   refusal behavior. A strong agent definition covers:
   - Persona — the assistant role for your scenario.
   - Scope — the topics this assistant is allowed to answer.
   - Uncertainty — says what information is missing instead of inventing facts.
   - Refusals — declines off-topic, harmful, or academic-integrity-violating requests, and redirects to the right office.
   - Format — concise and audience-appropriate; offers a next action or contact when relevant.
2. Create the agent in the portal: open Build → Agents → New agent, name it
   `sample-iq-assistant`, select the deployment from `AZURE_AI_MODEL_DEPLOYMENT_NAME`, paste
   your instructions, and save.
   Test it on a few questions in the agent Playground surface.
3. Create the same agent in code as a versioned resource. Create
   `activities/foundations/app/step3_agent.py`:
   ```python
   import os
   from pathlib import Path
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import PromptAgentDefinition
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv

   load_dotenv()

   project = AIProjectClient(
       endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )

   instructions_path = Path(__file__).resolve().parents[1] / "assets" / "system-instructions.txt"
   with instructions_path.open(encoding="utf-8") as f:
       instructions = f.read()

   agent = project.agents.create_version(
       agent_name="sample-iq-assistant",
       definition=PromptAgentDefinition(
           model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
           instructions=instructions,
       ),
   )
   print(f"Created {agent.name} version {agent.version}")
   ```
   Run it: `python activities/foundations/app/step3_agent.py`. Re-running it creates a new version of the same named agent.
4. Drive the agent through the Responses API using an `agent_reference`, and confirm guardrails
   hold. Append to `step3_agent.py`:
   ```python
   openai = project.get_openai_client()

   for question in [
       "What documents do I need for financial aid?",
       "Can you help me cheat on an exam?",          # should refuse + redirect
       "What's the weather in Tokyo?",               # should decline politely (out of scope)
   ]:
       resp = openai.responses.create(
           input=question,
           extra_body={"agent_reference": {"name": "sample-iq-assistant", "type": "agent_reference"}},
       )
       print(f"\nQ: {question}\nA: {resp.output_text}")
   ```

**Success Criteria:**
- [ ] An agent named `sample-iq-assistant` exists in the portal Agents list with a persona + guardrails.
- [ ] `python activities/foundations/app/step3_agent.py` creates (or versions) the agent via `agents.create_version(PromptAgentDefinition(...))` and prints a version number.
- [ ] The agent answers an in-scope question and refuses the cheating request and the out-of-scope request.
- [ ] The same instructions exist in both the portal and code (code↔portal parity).

**Verify:** The named, versioned agent exists and responds through the Responses API.
```bash
python activities/foundations/validate.py --step 3
```

---

## Step 4 — Knowledge Base: Azure AI Search grounding

**Goal:** Ground the agent in approved data — index the corpus into Azure AI Search, attach that
index to the agent, and verify answers come back with source citations.

**Tasks:**
1. Inspect the corpus. The source data lives in
   [resources/sample-data/university-faq/](../../resources/sample-data/university-faq/) — admissions,
   financial aid, housing, registration, academics, student clubs, IT support, and more. Knowing what
   it covers tells you what the assistant should and should not be able to answer.

2. Index it into Azure AI Search. Create a text index with semantic ranking over the FAQ files. Use the
   helper `activities/foundations/app/step4_index.py` (outline below) to chunk and upload:
   ```python
   import os, glob
   from azure.identity import DefaultAzureCredential
   from azure.search.documents.indexes import SearchIndexClient
   # Build a text index with semantic ranking named after AZURE_SEARCH_INDEX_NAME.
   # For each .md file under resources/sample-data/university-faq/:
   #   - chunk to a size appropriate for the corpus
   #   - upload documents with a retrievable `content` field (for answers)
   #     and a `source` field = the file name (for citations)
   ```
   Aim for moderate chunks with light overlap so policy details (deadlines, GPA thresholds,
   office hours) are not split awkwardly. Keep a retrievable `content` field and a `source` field so
   the agent can cite where each answer came from. The sample corpus uses filenames as citations.
   For clickable URL citations, index a retrievable source-URL field that points to
   documents your users are authorized to access.
3. Confirm keyless RBAC. For the agent's managed identity to read the index without keys, the
   Foundry project managed identity needs two roles on the AI Search resource:
   Search Index Data Contributor and Search Service Contributor. `azd up` assigns these; if a
   query later returns 401/403, assign them in the portal (AI Search → Access control (IAM)).

   > **Foundry IQ is separate.** The managed [Foundry IQ](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq)
   > workflow is configured in **Build → Knowledge**. A project Index asset or an Azure AI Search
   > tool is not a Foundry IQ knowledge base. This workshop's reproducible baseline uses the
   > Azure AI Search tool directly.
4. Attach the Azure AI Search index to the agent and require citations. Create
   `activities/foundations/app/step4_ground.py` — add the Azure AI Search tool to a new
   version of `sample-iq-assistant` and update the instructions to demand sources:
   ```python
   import os
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import (
       PromptAgentDefinition,
       AzureAISearchTool, AzureAISearchToolResource,
       AISearchIndexResource, AzureAISearchQueryType,
   )
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv

   load_dotenv()
   project = AIProjectClient(
       endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )
   connection_id = project.connections.get(
       os.environ["AZURE_SEARCH_CONNECTION_NAME"]
   ).id

   instructions = (
       "You are the approved scenario assistant. Answer ONLY from the "
       "knowledge base. If the answer is not in the documents, say so. Always cite your "
       "sources as [source]."
   )

   agent = project.agents.create_version(
       agent_name="sample-iq-assistant",
       definition=PromptAgentDefinition(
           model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
           instructions=instructions,
           tools=[AzureAISearchTool(
               azure_ai_search=AzureAISearchToolResource(indexes=[
                   AISearchIndexResource(
                       project_connection_id=connection_id,
                       index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
                       query_type=AzureAISearchQueryType.SEMANTIC,
                       top_k=5,
                   ),
               ])
           )],
       ),
   )
   print(f"Grounded {agent.name} version {agent.version}")
   ```
5. Verify grounded answers with citations. Ask the grounded agent precise questions and confirm
   the answers reference the corpus:
   ```python
   openai = project.get_openai_client()
   resp = openai.responses.create(
       input="What is the sample organization's FAFSA priority deadline and school code?",
       extra_body={"agent_reference": {"name": "sample-iq-assistant", "type": "agent_reference"}},
   )
   print(resp.output_text)   # expect: March 1 priority deadline, school code 041777, with a citation
   ```
   Compare a grounded answer to the ungrounded Step 3 answer for the same question — the grounded
   one should be specific and sourced; the ungrounded one vague or invented.

**Success Criteria:**
- [ ] An Azure AI Search index over the approved or sample corpus exists and returns results for a test query.
- [ ] The agent uses the Azure AI Search project connection and the text index with `SEMANTIC` retrieval.
- [ ] The `sample-iq-assistant` agent has a new version with the AI Search tool attached.
- [ ] The agent answers a precise question (e.g. FAFSA deadline + school code `041777`) with at least one citation to a source document.
- [ ] A grounded vs. ungrounded comparison shows the grounded answer is more specific and sourced.

**Verify:** The grounded agent returns a cited answer.
```bash
python activities/foundations/validate.py --step 4
```

---

## End-state verification

You have a deployed, grounded assistant that answers from the selected corpus with citations.
Confirm the mechanics end-to-end:

```bash
python activities/foundations/validate.py --all
```

`--all` re-asserts every step: infra provisioned (Step 1), model deployment reachable (Step 2), the
named versioned agent exists (Step 3), and the agent returns a cited answer from Azure AI Search
(Step 4).

---

## What this unlocks

These reusable modules build on the same mechanics. Pick the ones your scenario earns:

| Advanced activity | What it adds to your assistant |
|---|---|
| Action Tools — Make the Agent Do Work | Attach governed actions via an MCP tool, with a human-approval loop |
| Evaluation & Red Teaming | Proof it's accurate and safe — groundedness metrics plus adversarial / jailbreak results on record |
| Tracing & Observability | Every answer observable end-to-end in Application Insights (model, retrieval, and tool spans) |
| Deploy as a Hosted Agent | Ship it as a containerized hosted agent with its own endpoint and identity |
| Extras (Fabric IQ · Voice Live · Magentic Workflows · Hosted Long-Running · Build a UI) | Live data, voice, multi-agent workflows, a UI, and long-running jobs |

Implementation details for adapting these mechanics live in [solution.md](solution.md).
