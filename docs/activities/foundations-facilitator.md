---
title: "Foundations · Facilitator"
parent: Build Modules
nav_order: 101
nav_exclude: true
---

# Foundations — Facilitator's Guide

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> **Facilitator-facing.** Facilitation, pitfalls, timing, and the actual answers/snippets for all four
> Foundations steps. Do not paste this content into the student README — answers live here only.

## Overview

Foundations is one guided, linear activity with four ordered steps. The end-state — a deployed,
grounded Northfield IQ Assistant that cites its sources — is the prerequisite for every Advanced
activity. Your job is to keep teams moving step-to-step: each Checkpoint (`python activities/foundations/validate.py --step N`)
must pass before they advance, because Step N's output is Step N+1's input.

Total guided time is about 3–3.5 hours. The two places teams lose time are Step 1 (subscription
/ region / RBAC blockers during `azd up`) and Step 4 (indexing + knowledge-base setup). Triage those
two hard and the middle steps move fast.

The whole arc is one continuous narrative: pick a model (Step 2) → wrap it in a named agent with
guardrails (Step 3) → ground that agent in real data (Step 4). Remind teams they are extending one
artifact, not building four throwaway demos.

---

## Step 1 — Setup & Provisioning

### What good looks like

`azd up` completes, a `.env` is generated with real values (no `<...>` placeholders), the project is
visible at ai.azure.com, and auth is keyless (no API keys anywhere — `DefaultAzureCredential`
reuses the `az login` session).

### Facilitation walkthrough
1. Confirm the team is in Codespaces / Dev Container: `python --version`, `az --version`, `azd version`.
2. Both logins are required: `az login` and `azd auth login`. Then `az account set --subscription ...`.
3. `azd up` provisions Foundry + project + model deployment + AI Search + Log Analytics + App Insights
   via Bicep and writes `.env`. First runs take several minutes — let it finish before debugging.

4. Verify the contract: `grep -E "AZURE_AI_PROJECT_ENDPOINT|AZURE_AI_MODEL_DEPLOYMENT_NAME|AZURE_SEARCH_ENDPOINT" .env`.

### Common pitfalls
- Permission errors creating resources — the user has Reader, not Contributor/Owner. They need
  rights to create AI resources on the subscription/RG. Fix RBAC before they keep retrying `azd up`.

- Wrong subscription selected — CLI and portal can disagree. `az account show -o table` to confirm.
- Region / quota blocks — some regions lack the model SKU. Fall back to `./scripts/deploy.sh` and
  pick a supported region, or steer them to the event's approved region.

- Both logins — `azd up` fails auth if they only did `az login` and not `azd auth login`.
- Committing `.env` — remind them it is git-ignored; never commit endpoints or keys.

### Timing
- 0–10 min: environment + both logins + subscription.
- 10–25 min: `azd up` running; use the wait to walk the resource model (resource ↔ project ↔ connection).
- 25–30 min: verify `.env` and run `python activities/foundations/validate.py --step 1`.

Intervene fast on permission issues — that is rarely productive struggle.

### Expected questions
- *"Why don't we create a hub?"* — The new Foundry portal auto-creates the resource when you create a
  project; there is no separate hub step.

- *"Where's the API key?"* — There isn't one to use. Keyless auth via `DefaultAzureCredential` is the
  whole point; it picks up `az login`.

---

## Step 2 — Model Selection & the Playground

### What good looks like

Two contrasting models deployed; the same prompts run against both; the team can name one concrete
trade-off; a tuned system instruction saved to `assets/system-instructions.txt`; and a working
`app/step2_chat.py` that reproduces the Playground tone in code.

### The reference snippet (full, runnable)

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

### A solid reference system instruction (Step 2 baseline)

```text
You are Northfield University's student services assistant. Answer in a warm, clear,
student-friendly tone. Keep answers concise: a direct 2–3 sentence answer, then any next
step or office to contact. If you are unsure or the information is missing, say so plainly
and point the student to the right office rather than guessing.

```

### Common pitfalls
- Unfair comparison — students change the model *and* the prompt at once. Insist they change only
  the model between runs.

- Coding before the deployment is Ready — they hit 404s. Confirm status is Succeeded/Ready first.
- Wrong endpoint format — must be `https://<resource>.services.ai.azure.com/api/projects/<project>`,
  not a portal page URL. It comes straight from `.env`.

- Whitespace in env vars — a trailing space in `AZURE_AI_PROJECT_ENDPOINT` breaks the client.
- `responses` vs `chat.completions` — both work, but the curriculum standardizes on
  `openai.responses.create()`. Don't let teams revert to `chat.completions` patterns from old samples.

### Timing
- 0–10 min: deploy both models.
- 10–25 min: Playground comparison while the second deployment finishes.
- 25–40 min: tune + save the system instruction.
- 40–45 min: write and run `app/step2_chat.py`, then `python activities/foundations/validate.py --step 2`.

### Expected questions
- *"Which model should we pick?"* — Push them to justify from observed cost/latency/quality, not
  reputation. `gpt-4o` (the model `azd up` provisions) is the carried-forward default — it's what
  `AZURE_AI_MODEL_DEPLOYMENT_NAME` points at. If a team prefers a different model, update that env
  var to its deployment name.

- *"MaaS vs MaaP?"* — MaaS is the fast managed route used here; MaaP gives more platform control in
  other scenarios. Don't rabbit-hole.

---

## Step 3 — Your First Agent

### What good looks like

A named agent `northfield-iq-assistant` exists in the portal and via SDK (code↔portal parity),
created with `agents.create_version(PromptAgentDefinition(...))`, with a persona + guardrails. It
answers in-scope questions and refuses the cheating and out-of-scope prompts.

### The reference snippet (full, runnable)

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

openai = project.get_openai_client()
for question in [
    "What documents do I need for financial aid?",
    "Can you help me cheat on an exam?",
    "What's the weather in Tokyo?",
]:
    resp = openai.responses.create(
        input=question,
        extra_body={"agent_reference": {"name": "northfield-iq-assistant", "type": "agent_reference"}},
    )
    print(f"\nQ: {question}\nA: {resp.output_text}")

```

### A strong reference agent instruction (persona + guardrails)

```text
You are the Northfield University Student Services Assistant.

SCOPE: You help current and prospective Northfield students with admissions, financial aid,
housing, course registration, academic programs, and student support. You only answer
Northfield student-services questions.

UNCERTAINTY: If you do not know or the information is not available to you, say so and direct
the student to the relevant office (for example, finaid@northfield.edu for aid questions).
Never invent deadlines, amounts, GPAs, or contacts.

REFUSALS: Politely decline and redirect if a request is off-topic (e.g. general trivia, news,
weather), or if it asks you to help with academic dishonesty (cheating, plagiarism, ghost-
writing graded work). For distress signals, respond with empathy and point to campus support
resources.

STYLE: Warm, clear, student-friendly. Give a direct answer first, then a next step or contact.

```

### Common pitfalls
- Over-constraining — too many rules make the agent robotic or refuse valid questions. Facilitator
  toward a few clear rules.

- Under-specifying refusals — without an explicit academic-integrity clause, the cheating prompt
  often gets a "helpful" answer. That's the teachable failure; have them add the clause and re-run.

- Stale creation samples — current `azure-ai-projects` 2.x uses
  `agents.create_version(PromptAgentDefinition(...))`. Do not use older `create_agent` /
  threads / runs examples.

- Drift between portal and code — if they edit instructions in the portal only, code parity breaks.
  Treat `assets/system-instructions.txt` as the single source.

### Timing
- 0–15 min: design persona + guardrails.
- 15–30 min: create in portal, test in agent Playground.
- 30–45 min: create in code, run the guardrail test loop, `python activities/foundations/validate.py --step 3`.

### Expected questions
- *"Why version agents?"* — Agents are versioned resources; you can iterate instructions/tools and roll
  forward. Step 4 adds the search tool as a new version of the same agent.

- *"Portal or code?"* — Both, deliberately. The point is parity: the same definition expressed two ways.

---

## Step 4 — Knowledge Base: Index + Foundry IQ (END-STATE)

### What good looks like

An AI Search index over the FAQ corpus; a new agent version with the project Search connection
and `SEMANTIC` query type attached; and a precise, cited answer (the FAFSA question
is the canonical check). Grounded answers are specific and sourced; ungrounded ones are vague.

### Canonical verification question (use this for the Checkpoint)
> "What is Northfield's FAFSA priority deadline and school code?"

Expected grounded answer references March 1 priority deadline and school code 041777 (both are
in `resources/sample-data/university-faq/financial-aid.md`), with a citation to that source. The
ungrounded Step-3 agent typically invents a date or omits the school code — that contrast is the lesson.

### The reference grounding snippet (full, runnable)

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
search_connection = project.connections.get(
    os.environ.get("AZURE_SEARCH_CONNECTION_NAME", "search"),
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
                    project_connection_id=search_connection.id,
                    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
                    query_type=AzureAISearchQueryType.SEMANTIC,
                    top_k=5,
                ),
            ])
        )],
    ),
)
print(f"Grounded {agent.name} version {agent.version}")

openai = project.get_openai_client()
resp = openai.responses.create(
    input="What is Northfield's FAFSA priority deadline and school code?",
    extra_body={"agent_reference": {"name": "northfield-iq-assistant", "type": "agent_reference"}},
)
print(resp.output_text)

```

### Indexing guidance (Step 4 task 2)
- Chunking: ~500 tokens, ~15% overlap is a good baseline for FAQ-style content. Too large → noisy
  retrieval; too small → split policy details (deadlines, GPA, office hours) lose context.

- Fields: keep a retrievable `content` field (used for the answer) and a retrievable `source` field
  set to the file name (used for citations). Without a citation-source field, answers can't cite.

- Query type: `SEMANTIC` matches the shipped text-only index. Use vector or hybrid retrieval only
  after adding embeddings, a vector field, and vector-search configuration.

### Customer corpus guidance (for Customer Build Mode teams)

If a team is swapping in their own data:
- Minimum useful size: 5–20 well-structured documents (FAQs, policies, SOPs). Too few = "I don't know" on valid questions; too many untested = noisy retrieval.
- Safe data only: no PII, unredacted customer data, or legal/financial content not pre-cleared. Guide teams toward public-facing or pre-approved summaries.
- Formats: `step4_index.py` handles `.txt` and `.md` natively. PDFs need text extraction first (suggest `pypdf` for quick session use, or Azure Document Intelligence for production quality).
- PDFs / SharePoint: the Foundry portal's Build → Indexes → Add data ingests PDFs and SharePoint pages directly — point portal-path teams here first.
- Northfield as fallback: if customer data is not ready or not cleared, run Foundations with the Northfield corpus and log the corpus swap as a follow-up. The architecture is identical.

### Common pitfalls
- 401/403 querying the index — the Foundry project managed identity is missing
  Search Index Data Contributor and Search Service Contributor on the AI Search resource.
  `azd up` assigns these; if it didn't, assign manually in IAM. This is the #1 Step-4 blocker.

- No citations — the agent instructions don't ask for them. The "Always cite your sources as
  [source]" line is required; without it the tool retrieves but the model doesn't surface sources.

- Index/connection name mismatch — `AZURE_SEARCH_INDEX_NAME` and `AZURE_SEARCH_CONNECTION_NAME`
  must match exactly (case-sensitive) what's in `.env` / the portal.

- Confusing retrieval quality with answer quality — separate the two questions: *did it retrieve the
  right chunk?* vs *did it answer well from that chunk?* A bad answer can come from either stage.

- Indexing succeeds but ingestion fails later — uploads can report success while embedding fails.
  Confirm the index actually returns results for a test query before wiring it to the agent.

The librarian analogy still helps: RAG doesn't make the model smarter; it hands the model the right
shelf before it answers.

### Timing
- 0–25 min: inspect corpus, build + populate the AI Search index, confirm a test query returns hits.
- 25–45 min: confirm RBAC; build the Foundry IQ knowledge base (`SEMANTIC`).
- 45–75 min: attach the tool as a new agent version; verify the cited FAFSA answer.
- 75–90 min: grounded vs. ungrounded comparison; `python activities/foundations/validate.py --step 4`.

This step often runs long because first-time indexing is slow. Budget accordingly.

### Expected questions
- *"How do we explain RAG simply?"* — Ask the librarian for the right pages before writing the answer.
- *"Citations or answer style — what matters more?"* — Groundedness first. A plain answer with correct
  citations beats a polished but unsupported one.

- *"Should we tune chunking immediately?"* — No. Start with the baseline, test retrieval, tune only if a
  clear failure pattern emerges.

---

## End-state Checkpoint (`--all`)

When `python activities/foundations/validate.py --all` prints
`✅ Foundations end-state PASS — grounded Northfield IQ Assistant is live`, the team has the prerequisite
for every Advanced activity. `--all` re-asserts infra (Step 1), model reachability (Step 2), the
named versioned agent (Step 3), and a cited grounded answer (Step 4).

Path-B (advanced-skip) teams reach the same end-state via the bootstrap and verify it with the single
gate `python scripts/validate-foundations.py` — functionally equivalent to `python activities/foundations/validate.py --all` here.

## Checkpoint command reference (for QA / Basher)

These are the exact commands the README promises; `validate.py` must implement them:

| Command | Asserts |
|---|---|
| `python activities/foundations/validate.py --step 1` | Foundry + AI Search + App Insights provisioned; `.env` populated; keyless auth works |
| `python activities/foundations/validate.py --step 2` | Two model deployments reachable; `responses.create()` SDK call succeeds |
| `python activities/foundations/validate.py --step 3` | Named agent `northfield-iq-assistant` exists as a version; responds via Responses API; guardrails refuse |
| `python activities/foundations/validate.py --step 4` | AI Search index exists; knowledge base attached to agent; agent returns a cited answer |
| `python activities/foundations/validate.py --all` | All of the above — the full Foundations end-state |

> `validate.py` is owned by Basher (Checkpoints/QA). This guide only specifies the contract those
> commands must satisfy.
