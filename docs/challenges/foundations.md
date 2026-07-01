---
title: "Foundations"
parent: Challenge Library
nav_order: 1
---

# Foundations — Build the Northfield University IQ Assistant

{% include journey-status.html tone="shared" path="Challenge Library &rarr; Foundations" artifact="A deployed, grounded assistant with citations. Upskill teams use Northfield; Customer Build teams swap in their own corpus and persona." next="Complete Steps 1-4 in order, then choose Advanced modules from the library." %}

> **Tier 1 · Foundations — the guided, linear challenge everyone completes.**
> One evolving artifact, four ordered steps. By the end you will have a **deployed, grounded
> Northfield University "IQ" Assistant** — an agent that answers student-services questions from
> Northfield's own FAQ corpus, **with citations**.

## How this hackathon is structured (read first)

The curriculum has **three tiers**:

- **Tier 1 · Foundations (this challenge)** — a single guided path, broken into **four ordered
  steps**. Everyone does it. Each step ends in a **Checkpoint** you can verify before moving on.
  Step N's Checkpoint is the prerequisite for Step N+1.

- **Tier 2 · Advanced** — modular, self-contained challenges you can attempt **in any order**
  (Action Tools, Evaluation & Red Teaming, Tracing & Observability, Deploy as a Hosted Agent, plus
  Extras). **Every Advanced challenge assumes the Foundations end-state** — the grounded assistant
  you build here.

- **Tier 3 · Capstone** *(optional end-of-day)* — splits the assistant into a router and specialist
  agents. Requires the Foundations end-state plus at least one Advanced challenge completed.
  You do not need to reach it to succeed today — think of it as the stretch goal if time allows.

**Completing Step 4 = the Foundations end-state.** It is the prerequisite for the entire Advanced
tier. If you only do one thing today, finish all four steps below.

### Choose the scenario mode

Use **Upskill Mode** if you want the known-good learning path: build the Northfield University IQ
Assistant exactly as written. Use **Customer Build Mode** if your event is tied to an account or
project: complete the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}), then use
Northfield as the reference while replacing the corpus, persona, action candidates, eval prompts, and
final demo story with customer-safe equivalents.

### The default scenario

You are building the **Northfield University IQ Assistant**, a student-services agent. It grows
across the four steps:

| Step | What the assistant can do afterward |
|---|---|
| [**1 · Setup**](#step-1--setup--provisioning-foundry--ai-search) | Nothing yet — your infrastructure is live and authenticated |
| [**2 · Model & Playground**](#step-2--model-selection--the-playground) | Answer generic questions with a model and system instructions you chose |
| [**3 · First Agent**](#step-3--your-first-agent) | Run as a named, versioned agent with a persona and guardrails |
| [**4 · Knowledge Base**](#step-4--knowledge-base-index--foundry-iq---foundations-end-state) | Answer from Northfield's real FAQ corpus, **with citations** ← **end-state** |

In Customer Build Mode, the Step 4 end-state should prove the same capability with customer-relevant
questions: grounded answers, citations, and clear abstention when the trusted corpus is missing the
answer.

### What you need before you start

- The repo open in **GitHub Codespaces** or a local **Dev Container** (Python + Azure CLI + `azd`).
- An Azure subscription where you can create AI resources.
- About **3–3.5 hours** for the full guided path.

> **Checkpoints are machine-checkable.** Each step ends with `python validate.py --step N`. The
> validator (provided in this folder) inspects your live Azure resources and prints
> `✅ Step N PASS` or a specific failure. The final `python validate.py --all` asserts the complete
> end-state.

---

## Step 1 — Setup & Provisioning (Foundry + AI Search)

**Goal:** Provision the full hackathon footprint with one command and confirm keyless Entra auth works end-to-end.

**Tasks:**

1. Open the repository in **GitHub Codespaces** (use the **Open in GitHub Codespaces** button in the root `README.md`) or in a local **Dev Container**. When the build finishes, confirm your toolchain in a terminal:

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

3. Provision everything with **one `azd up`**. This deploys, via Bicep, a **Foundry resource**
   (project-management enabled), a **Foundry project**, a chat **model deployment**, an **Azure AI
   Search** service, and **Log Analytics + Application Insights** — and auto-generates your `.env`:

   ```bash
   azd up

   ```
   > If `azd up` is blocked by quota or region limits, use the Bash fallback `./scripts/deploy.sh`
   > and pick a supported region when prompted.
4. Confirm the generated **`.env`** exists and holds your resource contract (do **not** commit it).

   > **What is the `.env` contract?** `azd up` writes a `.env` file containing your resource
   > endpoints, deployment names, and connection strings. Every script in this repo loads it
   > automatically via `python-dotenv` (`load_dotenv()`). It is git-ignored — never commit it.

   At minimum it contains the project endpoint, the model deployment name, and the search endpoint:

   ```bash
   grep -E "AZURE_AI_PROJECT_ENDPOINT|AZURE_AI_MODEL_DEPLOYMENT_NAME|AZURE_SEARCH_ENDPOINT" .env

   ```

5. Verify **keyless** authentication works (no API keys — `DefaultAzureCredential` reuses your
   `az login` session).

   > **Why keyless auth?** `DefaultAzureCredential` (from `azure-identity`) checks your `az login`
   > session and requests a short-lived token from Entra. Access is governed by your Azure RBAC
   > roles — no secrets to rotate or accidentally commit.

   Open the [Microsoft Foundry portal](https://ai.azure.com/), confirm your new
   project is listed, and browse **Discover → Models** to see the catalog.

**Success Criteria:**

- [ ] `azd up` completes and reports the Foundry, AI Search, and App Insights resources as provisioned.
- [ ] A generated `.env` exists with `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, and `AZURE_SEARCH_ENDPOINT` populated (no placeholder `<...>` values).
- [ ] Your project appears in the Foundry portal and the model catalog opens under **Discover → Models**.
- [ ] No API keys are pasted anywhere — auth flows through `DefaultAzureCredential`.

**Checkpoint:** Provisioning and auth are verified programmatically.

```bash
python validate.py --step 1
# expected: "✅ Step 1 PASS"

```

---

## Step 2 — Model Selection & the Playground

**Goal:** Choose a model for the assistant by comparing two contrasting models in the Playground, tune the **system instructions**, then reproduce that behavior in code.

**Tasks:**

1. `azd up` already deployed **`gpt-4o`** (deployment name `gpt-4o`) — this is the model your `.env`
   `AZURE_AI_MODEL_DEPLOYMENT_NAME` points at and the one you carry forward through Foundations. In
   the Foundry portal, go to **Discover → Models** and deploy **one contrasting model** to compare it
   against — a faster, lower-cost option such as `gpt-4.1-mini`, or a different family such as `phi-4`.
   Wait until the new deployment status reads **Succeeded** / **Ready**.

2. Open the **Chat Playground**, select your `gpt-4o` deployment, and set a starting **system
   instruction** for the assistant:

   ```text
   You are Northfield University's student services assistant. Answer in a warm, clear,
   student-friendly tone. If you are unsure or the information is missing, say so plainly
   and point the student to the right office.

   ```
   Send a few Northfield questions and note tone, structure, and accuracy:

   - "How do I apply for scholarships?"
   - "What computer science programs do you offer?"
   - "Can I register late for classes?"
3. Switch the Playground to your **second** model and run the **same** prompts. Compare on four axes:
   answer detail, latency, tone, and suitability for a student-services assistant. Change **only the
   model** between runs so the comparison is fair.

4. Iterate on the **system instruction** until the smaller model behaves well: define audience, tone,
   how to handle missing information, and what is out of scope. Save your best version to
    `challenges/foundations/assets/system-instructions.txt`.

5. Reproduce the Playground behavior **in code**. Create `challenges/foundations/app/step2_chat.py`
   and call your chosen deployment through the project's OpenAI client.

   > **Responses API** — the stateless OpenAI-compatible endpoint used throughout this hackathon.
   > `openai.responses.create(model=..., instructions=..., input=...)` sends a single prompt and
   > returns a reply. In later steps you'll pass an `agent_reference` in `extra_body` to route the
   > call through your named agent instead.

   ```python
   import os
   from azure.ai.projects import AIProjectClient
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv

   load_dotenv()

   project = AIProjectClient(
       endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )
   openai = project.get_openai_client()

   with open("assets/system-instructions.txt", encoding="utf-8") as f:
       system_instructions = f.read()

   response = openai.responses.create(
       model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
       instructions=system_instructions,
       input="How do I apply for scholarships at Northfield?",
   )
   print(response.output_text)

   ```
   Run it: `python app/step2_chat.py`. The code answer should match the tone you tuned in the Playground.

**Success Criteria:**

- [ ] Two contrasting models are deployed and visible in the **Models / Deployments** view.
- [ ] You ran the **same** prompts against both models and can state one concrete trade-off (cost, latency, tone, or detail).
- [ ] A tuned system instruction is saved to `assets/system-instructions.txt`.
- [ ] `python app/step2_chat.py` prints an on-tone answer using `responses.create()` and `DefaultAzureCredential` (no API key).

**Checkpoint:** The deployments exist and the SDK call succeeds.

```bash
python validate.py --step 2
# expected: "✅ Step 2 PASS"

```

---

## Step 3 — Your First Agent

**Goal:** Promote your system instructions into a **named, versioned Foundry agent** with a persona and guardrails — created both in the portal and via the SDK.

**Tasks:**

1. Decide the agent's identity. Build on your Step 2 system instructions, adding **guardrails** and
   **refusal behavior**. A strong agent definition covers:

   - **Persona** — "Northfield University Student Services Assistant."
   - **Scope** — answers admissions, financial aid, housing, registration, academics, student support.
   - **Uncertainty** — says what information is missing instead of inventing facts.
   - **Refusals** — declines off-topic, harmful, or academic-integrity-violating requests, and redirects to the right office.
   - **Format** — concise, student-friendly; offers a next action or contact when relevant.
2. Create the agent **in the portal**: open **Build → Agents → New agent**, name it
   `northfield-iq-assistant`, select your `gpt-4o` deployment, paste your instructions, and save.
   Test it on a few questions in the agent Playground surface.

3. Create the same agent **in code** as a versioned resource. Create
    `challenges/foundations/app/step3_agent.py`:

   ```python
   import os
   from azure.ai.projects import AIProjectClient
   from azure.ai.projects.models import PromptAgentDefinition
   from azure.identity import DefaultAzureCredential
   from dotenv import load_dotenv

   load_dotenv()

   project = AIProjectClient(
       endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
       credential=DefaultAzureCredential(),
   )

   with open("assets/system-instructions.txt", encoding="utf-8") as f:
       instructions = f.read()

   agent = project.agents.create_version(
       agent_name="northfield-iq-assistant",
       definition=PromptAgentDefinition(
           model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
           instructions=instructions,
       ),
   )
   print(f"Created {agent.name} version {agent.version}")

   ```
   Run it: `python app/step3_agent.py`. Re-running it creates a **new version** of the same named agent.

4. Drive the agent through the **Responses API** using an `agent_reference`, and confirm guardrails
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
           extra_body={"agent": {"name": "northfield-iq-assistant", "type": "agent_reference"}},
       )
       print(f"\nQ: {question}\nA: {resp.output_text}")

   ```

**Success Criteria:**

- [ ] An agent named `northfield-iq-assistant` exists in the portal **Agents** list with a persona + guardrails.
- [ ] `python app/step3_agent.py` creates (or versions) the agent via `agents.create_version(PromptAgentDefinition(...))` and prints a version number.
- [ ] The agent answers an in-scope question and **refuses** the cheating request and the out-of-scope request.
- [ ] The same instructions exist in both the portal and code (code↔portal parity).

**Checkpoint:** The named, versioned agent exists and responds through the Responses API.

```bash
python validate.py --step 3
# expected: "✅ Step 3 PASS"

```

---

## Step 4 — Knowledge Base: Index + Foundry IQ  *(← Foundations end-state)*

**Goal:** Ground the agent in Northfield's own data — index the FAQ corpus into Azure AI Search, build a Foundry IQ knowledge base, attach it to the agent, and verify answers come back **with citations**.

**Tasks:**

1. **Inspect the corpus.** The source data lives in
   [resources/sample-data/university-faq/](https://github.com/microsoft/frontier-foundry-hackathon/tree/main/resources/sample-data/university-faq) — admissions,
   financial aid, housing, registration, academics, student clubs, IT support, and more. Knowing what
   it covers tells you what the assistant should and should not be able to answer.

   > **Customer Build Mode — preparing your own corpus:** if you are swapping in customer data,
   > follow these guidelines before indexing:
   > - **Minimum useful size:** 5–20 well-structured documents (FAQs, policy pages, SOPs) is enough
   >   for a convincing demo. Sparse corpora produce "I don't know" answers even for valid questions.
   > - **Safe data only:** no PII, unredacted customer data, confidential pricing, or legal content
   >   not cleared for use. When in doubt, use public-facing or pre-approved summaries.
   > - **Supported formats:** the `step4_index.py` script ingests plain text (`.txt`) and Markdown
   >   (`.md`) directly. For PDFs, extract text first (e.g., `pypdf` or Azure Document Intelligence).
   > - **PDFs / SharePoint:** the Foundry portal's **Build → Indexes → Add data** flow can ingest
   >   PDFs and SharePoint pages directly — no code required for the portal path.
   > - **Northfield as fallback:** if customer data is not cleared or not ready, complete Foundations
   >   with the Northfield corpus and mark the corpus swap as a follow-up task. The architecture
   >   (indexing, grounding, citations) is identical regardless of the corpus.

2. **Index it into Azure AI Search.** Create a **vector/hybrid** index over the FAQ files. Use the
    helper `challenges/foundations/app/step4_index.py` (outline below) to chunk, embed, and upload:

   ```python
   import os, glob
   from azure.identity import DefaultAzureCredential
   from azure.search.documents.indexes import SearchIndexClient
   # Build a vector + keyword (hybrid) index named after AZURE_SEARCH_INDEX_NAME.
   # For each .md file under resources/sample-data/university-faq/:
   #   - chunk to ~500 tokens with ~15% overlap
   #   - embed each chunk
   #   - upload documents with a retrievable `content` field (for answers)
   #     and a `source` field = the file name (for citations)

   ```
   Aim for **moderate chunks with light overlap** so policy details (deadlines, GPA thresholds,
   office hours) are not split awkwardly. Keep a retrievable `content` field and a `source` field so
   the agent can cite where each answer came from.

3. **Confirm keyless RBAC.** For the agent's managed identity to read the index without keys, the
   **Foundry project managed identity** needs two roles on the AI Search resource:
   **Search Index Data Contributor** and **Search Service Contributor**. `azd up` assigns these; if a
   query later returns 401/403, assign them in the portal (AI Search → Access control (IAM)).

4. **Build a Foundry IQ knowledge base** over the index (agentic retrieval: query decomposition →
   parallel search → rerank). In the portal: **Build → Knowledge bases → New**, point it at your AI
   Search index, and choose the **`VECTOR_SEMANTIC_HYBRID`** query type.

   > **`VECTOR_SEMANTIC_HYBRID`** — Azure AI Search query type that combines vector similarity
   > (semantic meaning), BM25 keyword matching (exact terms), and semantic reranking in one call.
   > It typically outperforms pure vector search on factual FAQ-style content and is the recommended
   > default for grounded agents.

5. **Attach the knowledge base to the agent** and require citations. Create
    `challenges/foundations/app/step4_ground.py` — add the Azure AI Search tool to a **new
   version** of `northfield-iq-assistant` and update the instructions to demand sources:

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
   kb = project.indexes.get(
       name=os.environ["AZURE_FOUNDRY_KNOWLEDGE_BASE_NAME"], version="1",
   )

   instructions = (
       "You are Northfield University's student services assistant. Answer ONLY from the "
       "knowledge base. If the answer is not in the documents, say so. Always cite your "
       "sources as [source]."
   )

   agent = project.agents.create_version(
       agent_name="northfield-iq-assistant",
       definition=PromptAgentDefinition(
           model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
           instructions=instructions,
           tools=[AzureAISearchTool(
               azure_ai_search=AzureAISearchToolResource(indexes=[
                   AISearchIndexResource(
                       index_asset_id=kb.id,
                       query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID,
                       top_k=5,
                   ),
               ])
           )],
       ),
   )
   print(f"Grounded {agent.name} version {agent.version}")

   ```

6. **Verify grounded answers with citations.** Ask the grounded agent precise questions and confirm
   the answers reference the corpus:

   ```python
   openai = project.get_openai_client()
   resp = openai.responses.create(
       input="What is Northfield's FAFSA priority deadline and school code?",
       extra_body={"agent": {"name": "northfield-iq-assistant", "type": "agent_reference"}},
   )
   print(resp.output_text)   # expect: March 1 priority deadline, school code 041777, with a citation

   ```
   Compare a grounded answer to the **ungrounded** Step 3 answer for the same question — the grounded
   one should be specific and sourced; the ungrounded one vague or invented.

**Success Criteria:**

- [ ] An Azure AI Search index over the Northfield FAQ corpus exists and returns results for a test query.
- [ ] A Foundry IQ knowledge base is built over the index using `VECTOR_SEMANTIC_HYBRID` retrieval.
- [ ] The `northfield-iq-assistant` agent has a new version with the AI Search tool attached.
- [ ] The agent answers a precise question (e.g. FAFSA deadline + school code `041777`) **with at least one citation** to a source document.
- [ ] A grounded vs. ungrounded comparison shows the grounded answer is more specific and sourced.

**Checkpoint:** The grounded agent returns a cited answer — this is the Foundations end-state.

```bash
python validate.py --step 4
# expected: "✅ Step 4 PASS"

```

---

## End-state Checkpoint

You have reached the **Foundations end-state**: a deployed, grounded Northfield University IQ
Assistant that answers from the FAQ corpus with citations. Confirm the whole thing end-to-end:

```bash
python validate.py --all
# expected: "✅ Foundations end-state PASS — grounded Northfield IQ Assistant is live"

```

`--all` re-asserts every step: infra provisioned (Step 1), model deployment reachable (Step 2), the
named versioned agent exists (Step 3), and the agent returns a **cited** answer from the knowledge
base (Step 4). When this passes green, every Advanced challenge is unblocked.

---

## What's next — the Advanced tier

Pick **any** of these, in **any order**. Each one extends the same assistant and assumes the
Foundations end-state you just built (or the bootstrap skip-path:
`azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`).

| Advanced challenge | What it adds to your assistant |
|---|---|
| **Action Tools — Make the Agent Do Work** | Hands: create an IT ticket / place a registration hold / book advising via an MCP tool, with a human-approval loop |
| **Evaluation & Red Teaming** | Proof it's accurate **and** safe — groundedness metrics plus adversarial / jailbreak results on record |
| **Tracing & Observability** | Every answer observable end-to-end in Application Insights (model, retrieval, and tool spans) |
| **Deploy as a Hosted Agent** | Ship it as a containerized hosted agent with its own endpoint and identity |
| **Extras** (Fabric IQ · Voice Live · Magentic Workflows · Hosted Long-Running · Build a UI · Copilot-Assisted) | Live data, a voice, multi-agent workflows, a polished UI, and more |

> See the **`challenges/advanced-*`** folders for each modular challenge. Coaches: the facilitation
> guide for these four steps lives in [solution.md](foundations-coach).
