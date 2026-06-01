# WTH AI Hackathon — Curriculum V2 (Agent-Era Rearchitecture)

> ➡️ **Superseded in part by [PLAN-V3.md](PLAN-V3.md).** V3 **extends** this doc and overrides it on
> three things only: the **two-tier** framing below becomes a **three-tier tree** (V3 §1), the Advanced
> tier is **de-guided** (V3 §2), and a new **Tier 3 MAF Capstone** is added (V3 §3). Everything else in
> PLAN-V2 — the Foundations spine, the two-paths, the STEP template, the `.env` contract, the migration
> KEEP/CUT/REWRITE — **still stands and is authoritative.** Read PLAN-V3 for the current tier model.
>
> **"Build Intelligent Agents with Microsoft Foundry"**
>
> Successor architecture to [PLAN.md](PLAN.md). This document **does not replace** v1 — it
> defines the target curriculum the squad will build. Authored by Danny (Lead & Content
> Architect), 2026-06-01.
>
> **Driving inputs:** the FrontierWeekHack agent-lifecycle lab, the azure-trust-agents
> one-artifact-five-acts MAF hack, and the microsoft/skills Copilot enablement library.
> See `.squad/research/` for full notes; citations inline below as **[FWH]**, **[ATA]**, **[SKILLS]**.

---

## 1. Vision & What Changes vs. V1

### 1.1 The one-sentence vision

> Participants build **one evolving artifact** — the **Northfield University "IQ" Assistant** — by first
> completing a guided **Foundations** challenge (a deployed, grounded agent) and then **picking, in any
> order**, a set of self-contained **Advanced** challenges that make it act, prove it safe, observe it,
> ship it, and extend it.

We adopt the **one-artifact, many-acts arc** that makes azure-trust-agents so effective **[ATA §1, §4.1]**:
no throwaway work, every challenge visibly extends the same thing. We keep the Northfield University FAQ
corpus the squad already authored (`resources/sample-data/university-faq/`) so Wave-1/Wave-2 content
investment is preserved.

### 1.1a The two-tier model (LOCKED)

> ⚠️ **Superseded by [PLAN-V3.md](PLAN-V3.md) §1 (three-tier).** The two-tier framing here is now the
> trunk-and-fan of a **three-tier tree** — Foundations (Tier 1) → Advanced (Tier 2) → **Capstone
> (Tier 3, MAF multi-agent)** — plus a cross-cutting *make-it-your-own* branch. The Tier 1/Tier 2
> content below is unchanged; V3 only adds the Capstone summit on top.

The curriculum is delivered in **two tiers**:

1. **Tier 1 — Foundations** (the "Basic" challenge): **ONE guided, linear challenge** broken into **four
   ordered STEPS**, not separate challenges. **Everyone completes it.** Its end-state is a **deployed,
   grounded Northfield IQ Assistant agent**.
   - **Step 1** — Setup & Provisioning (Foundry + AI Search)
   - **Step 2** — Model Selection & the Playground (system instructions)
   - **Step 3** — Your First Agent
   - **Step 4** — Knowledge Base — Index + Foundry IQ (grounded agent)
2. **Tier 2 — Advanced challenges**: **modular, self-contained, pickable in ANY order**, each internally
   broken into numbered STEPS with success criteria. **All advanced challenges assume the Foundations
   end-state.** They are: **Action Tools**, **Evaluation & Red Teaming**, **Tracing & Observability**,
   **Deploy as a Hosted Agent**, and the modular **Extras** (Fabric IQ, Voice Live, Magentic Workflows,
   MAF + Hosted Long-Running Agents, Build a UI, Copilot-Assisted Build).

A **bootstrap skip-path** lets advanced teams materialize the Foundations end-state with **one script**
(~10–15 min) and jump straight to Tier 2 — see §1.5. **Prompt Flow is removed everywhere** (reaffirmed).

### 1.2 The scenario (recommended, concrete)

**Northfield University IQ Assistant** — a student-services agent.

| Tier / Unit | What the assistant can do by the end |
|---|---|
| **Foundations · Step 1** Setup | (nothing yet — infra is live) |
| **Foundations · Step 2** Model & Playground | Answer generic questions; you've picked the right model + system instructions |
| **Foundations · Step 3** First Agent | A named, versioned Foundry **agent** with a persona and guardrails |
| **Foundations · Step 4** Knowledge Base (IQ) | Answers grounded in Northfield's real FAQ corpus, with **citations** — **← Foundations end-state** |
| **Advanced** Action Tools | **Does work**: creates an IT ticket / registers a course hold / books an advising slot via an MCP tool |
| **Advanced** Evaluation + Red Team | Proven safe + accurate; groundedness + adversarial results on record |
| **Advanced** Tracing | Every answer is observable end-to-end in App Insights |
| **Advanced** Deploy | Shipped as a **hosted agent** with its own endpoint + identity |
| **Extras** (any order) | Live data (Fabric IQ), a voice, multi-agent workflows, a UI, Copilot-assisted build |

The four **Advanced** challenges and all **Extras** branch off the **Foundations end-state** and can be
attempted **in any order** (subject to the light prereqs noted per challenge).

This mirrors azure-trust-agents' **role-as-agent** intuition **[ATA §4.2]** — the assistant plays a real
student-services-desk role — without the regulated-finance complexity that would intimidate students.

### 1.3 What fundamentally changes vs. v1

| Dimension | V1 (PLAN.md) | V2 (this plan) |
|---|---|---|
| **Central abstraction** | Prompt + Prompt Flow | **Agent** (named, versioned Foundry resource) **[FWH §4.3]** |
| **Orchestration** | Prompt Flow visual DAG | **Agents + Tools + MCP**; Microsoft Agent Framework (MAF) in extras **[ATA §3]** |
| **RAG** | Hand-rolled vector index + "On Your Data" in a flow | **Foundry IQ knowledge base** (agentic retrieval) exposed to the agent via **MCP** **[SKILLS §2a]** |
| **"Does work"** | Not covered | **Action tool / MCP** that executes a real operation **[ATA §3 Pattern 4]** |
| **Evaluation** | Quality metrics only | NLP metrics **+ red teaming / adversarial safety** (the conspicuous gap in both reference repos) **[FWH §5, ATA §5]** |
| **Observability** | "Monitoring" mentioned at deploy | **Dedicated tracing challenge** (OTel GenAI → App Insights → KQL) **[FWH §2 Ch2, ATA §3]** |
| **Deploy** | Managed online endpoint for a flow | **Hosted (containerized) agent** via `azd ai agent` **[SKILLS §2a foundry-hosted-agents]** |
| **Copilot** | Pre-installed but unused | **First-class enablement layer**: microsoft/skills + `.mcp.json` + `copilot-instructions.md` **[SKILLS §3]** |
| **Provisioning** | `setup-resources.sh` (ad hoc) | **`azd up` + Bicep** as the golden path (Bash fallback) **[FWH §5 gap]** |
| **Extras** | None | Fabric IQ, Voice Live, Magentic/MAF, hosted long-running agents, UI, Copilot-assisted build |

---

## 1.5 How to Run This Hackathon (Two Paths)

There are **two ways in**. Both converge on the same **Foundations end-state** (a deployed, grounded
Northfield IQ Assistant), then fan out into the modular Advanced tier.

### Path A — Beginner (default, recommended)

Complete **Foundations** as one guided, linear challenge (4 ordered steps), then **pick Advanced
challenges in any order**.

### Path B — Advanced-skip (for teams who already know Foundry basics)

Run **one bootstrap** (~10–15 min) that materializes the Foundations end-state, verify a **single
checkpoint**, then jump straight to the Advanced tier. **Recommended only if your team already knows
Foundry basics** — you skip the guided learning, not the prerequisites.

```text
                ┌──────────────────────────────────────────────┐
  PATH A        │  FOUNDATIONS  (guided · linear · everyone)    │
  Beginner ───▶ │  Step1 ─▶ Step2 ─▶ Step3 ─▶ Step4             │
                │  Setup    Model    Agent    Knowledge Base    │
                └───────────────────────┬──────────────────────┘
                                         │
  PATH B                                 │  ◀── Foundations END-STATE
  Advanced ──▶  [ bootstrap: azd up                (deployed, grounded
  skip          + setup-foundations ]  ────────────▶  Northfield IQ Assistant)
  (~15 min, 1 checkpoint)                │
                                         ▼
        ┌───────────────── ADVANCED (modular · pick ANY order) ─────────────────┐
        │  Action Tools   Evaluation+RedTeam   Tracing   Deploy as Hosted Agent  │
        │  Extras:  Fabric IQ · Voice Live · Magentic · Hosted MAF · UI · Copilot │
        └────────────────────────────────────────────────────────────────────────┘
```

**Why one bootstrap checkpoint is enough:** every Advanced challenge assumes the **same** Foundations
end-state. Materialize it once, verify it once, and all Advanced challenges are unblocked. The bootstrap
is a gate, not a shortcut around setup: `azd up` provisions infra and a `setup-foundations` script builds
the model deployment, agent, index, and IQ knowledge base to match a manual Foundations run.

### The bootstrap checkpoint (single gate for Path B)

```bash
azd up                      # provision Foundry + AI Search + App Insights (+ ACR for deploy)
./scripts/setup-foundations.sh   # deploy model, create agent, index corpus, build IQ knowledge base
python scripts/validate-foundations.py   # ✅ asserts the Foundations end-state exists
```

`validate-foundations.py` must pass **green** before a Path-B team starts any Advanced challenge.

## 1.6 Standard STEP Template (every step & advanced challenge follows this)

Every **Foundations step** and every **Advanced challenge step** uses the **same four-part shape**:

> **Goal** — one sentence: what this step makes true.
> **Tasks** — numbered, do-this-then-that actions (portal and/or code).
> **Success Criteria** — observable, checkable statements ("the agent returns a cited answer").
> **Checkpoint** — the exact command or portal state that proves the step is done (e.g.
> `python validate.py --step 3`, or "the Tracing tab shows a span for the tool call").

Authors fill this skeleton for **every** unit. The copy-paste skeleton lives in
[RESTRUCTURE-SPEC.md](RESTRUCTURE-SPEC.md) so all content is structurally identical and QA-checkable.

---

## 2. Migration Notes — Keep / Cut / Rewrite

### 2.1 CUT (hard directive — Prompt Flow is deprecated)

- **Challenge 03 (Prompt Flow Orchestration)** — removed entirely. The classification → routing →
  formatting logic Rusty built (decisions.md, Wave 2) is **re-expressed as agent instructions + tools**,
  not a flow.
- **Prompt Flow RAG nodes** in old Ch04 — replaced by Foundry IQ knowledge base + AI Search tool.
- **Prompt Flow as a deploy target** in old Ch06 — replaced by hosted-agent deployment.
- **`requirements.txt`:** remove `promptflow`, `promptflow-tools`; the `ms-toolsai.promptflow` VS Code
  extension comes out of the devcontainer. Add `azure-ai-agents`, `azure-monitor-opentelemetry`,
  `azure-core-tracing-opentelemetry`, `agent-framework` (extras). Align SDK pins to FWH's tested set
  (`azure-ai-projects>=2.0.0`, `azure-ai-agents>=1.1.0`, `azure-ai-evaluation>=1.16.7`) **[FWH §1]**.

### 2.2 KEEP (preserve squad investment)

- Northfield University FAQ corpus (`resources/sample-data/university-faq/`) — now the **knowledge-base
  source** in Ch03 and the eval ground-truth source in Ch05.
- Repo layout `challenges/challenge-NN-slug/` with paired `README.md` (student) + `solution.md` (coach).
- `docs/` Jekyll `just-the-docs` site (Linus) — extend nav, don't rebuild.
- `validate-environment.py` pattern — extend to a **per-challenge `validate.py`** (gap both repos have) **[ATA §5]**.
- Ch00–02 content **substantially reusable** (setup, model deploy, prompt/system-instruction design)
  — they re-skin cleanly into **Foundations Steps 1–3**; old Ch04 RAG content seeds **Foundations Step 4**.

### 2.3 REWRITE

| Old (v1 / interim v2 Ch#) | New (two-tier model) |
|---|---|
| Ch00 "Setup" | **Foundations · Step 1** (Setup & Provisioning) |
| Ch01 "First Model" + Ch02 "Prompt Engineering" | **Foundations · Step 2** (Model Selection & Playground / system instructions) |
| Ch02 "First Agent" (agent persona/guardrails) | **Foundations · Step 3** (Your First Agent) |
| Ch04 "RAG via Prompt Flow" | **Foundations · Step 4** (Knowledge Base — Index + Foundry IQ via MCP) |
| Ch04 "Action Tools" | **Advanced** Action Tools (standalone, modular) |
| Ch05 "Evaluation" | **Advanced** Evaluation + Red Teaming (adds adversarial/safety + `evaluate.py`) |
| Ch06 "Tracing" | **Advanced** Tracing & Observability (standalone, modular) |
| Ch06 "Deploy a flow" / Ch07 | **Advanced** Deploy a hosted agent (`azd ai agent`) |

---

## 3. Curriculum Structure — Two Tiers

> ⚠️ **Superseded by [PLAN-V3.md](PLAN-V3.md) §1 (three-tier).** Add **Tier 3 — Capstone** (the MAF
> multi-agent `challenges/capstone-multi-agent/`) on top of the two tiers described here. The two-tier
> structure below remains correct for Foundations + Advanced.

The curriculum is **two tiers**: **Tier 1 Foundations** (one guided, linear challenge, four steps,
everyone does it) and **Tier 2 Advanced** (modular, self-contained, any order, all assuming the
Foundations end-state). Every unit follows the **Standard STEP Template** (§1.6).

### 3.1 Tier 1 — Foundations (the "Basic" challenge · linear · stepped)

**ONE challenge** (`challenges/foundations/`), four ordered steps. **End-state = a deployed, grounded
Northfield IQ Assistant agent.** Everyone completes this before touching Tier 2 — or materializes it via
the bootstrap skip-path (§1.5).

| Step | Title | Time | Difficulty | Builds toward end-state | Covers E2E bullet(s) |
|---|-------|------|------------|-------------------------|----------------------|
| **1** | Setup & Provisioning (Foundry + AI Search) | 30 min | ⭐ | Infra live; `.env` contract | **Deployment: Foundry + AI Search** |
| **2** | Model Selection & the Playground | 45 min | ⭐ | A chosen model + system instructions | **Model selection/comparison**, **Playground w/ system instructions** |
| **3** | Your First Agent | 45 min | ⭐⭐ | A named, versioned agent | **Creating a basic agent** |
| **4** | Knowledge Base — Index + Foundry IQ | 1.5 hr | ⭐⭐⭐ | **Grounded agent w/ citations (END-STATE)** | **Index docs in AI Search**, **build a knowledge base (IQ)**, **add Foundry IQ MCP to the agent** |

**Foundations total: ~3.25 hr.** Linear; Step N's Checkpoint gates Step N+1.

### 3.2 Tier 2 — Advanced challenges (modular · any order · assume Foundations end-state)

Each is a **self-contained folder** with its own numbered steps + success criteria. **Prereq for all =
the Foundations end-state** (completed guided, or via bootstrap). Light extra prereqs noted per row.

| Advanced challenge | Time | Difficulty | Extra prereq | Covers E2E bullet |
|--------------------|------|------------|--------------|-------------------|
| **Action Tools — Make the Agent Do Work** | 1.25 hr | ⭐⭐⭐ | — | **Add an MCP/tool that executes actions** |
| **Evaluation & Red Teaming** | 1.25 hr | ⭐⭐⭐⭐ | — (richer with Action Tools) | **Evaluations: NLP metrics + red teaming** |
| **Tracing & Observability** | 1 hr | ⭐⭐⭐⭐ | — (richer with Action Tools) | **Tracing & Observability** |
| **Deploy as a Hosted Agent** | 1 hr | ⭐⭐⭐⭐⭐ | — | (ships the artifact) |

### 3.3 Tier 2 — Extras (modular · optional · self-contained)

| ID | Extra | Time | Difficulty | Extra prereq | Covers E2E bullet |
|----|-------|------|------------|--------------|-------------------|
| A | Fabric IQ — Real-Time Data Grounding | 1 hr | ⭐⭐⭐⭐ | Foundations end-state | **Fabric IQ integration** |
| B | Give It a Voice — Voice Live API | 1 hr | ⭐⭐⭐ | Foundations end-state | **Speech / text→voice agent** |
| C | Magentic Workflows (MAF) | 1.5 hr | ⭐⭐⭐⭐⭐ | Action Tools | **Workflows, esp. Magentic** |
| D | MAF + Hosted Long-Running Agents | 1.5 hr | ⭐⭐⭐⭐⭐ | Deploy + Extra C | **MAF + Hosted Agents** |
| E | Build a UI for Your Agent | 1 hr | ⭐⭐⭐ | Deploy (recommended) | **Build a UI** |
| F | Copilot-Assisted Build (microsoft/skills) | cross-cutting | ⭐⭐ | Foundations Step 1 | **GitHub Copilot on microsoft/skills** |

**Every user E2E bullet is mapped** across Tier 1 + Tier 2; **nothing is missed**. Total guided path
(Foundations + all four Advanced) ≈ **7.75 hr**; Extras extend to multi-day / showcase formats.

---

### 3.4 Per-unit detail blocks

> **Foundations** units below are **Steps 1–4** of the single `challenges/foundations/` challenge.
> **Advanced** units are standalone modular challenges. Each maps to the Standard STEP Template (§1.6).

#### Foundations · Step 1 — Setup & Provisioning (Foundry + AI Search)
| Field | Detail |
|---|---|
| **Description** | Provision the full hackathon footprint with **one `azd up`**: a Foundry resource (project-management enabled), a Foundry project, a deployed chat model, an **Azure AI Search** service, Log Analytics + Application Insights, and an auto-generated `.env`. Verify Entra auth end-to-end. |
| **Time** | 30 min |
| **Difficulty** | ⭐ Beginner |
| **Dependencies** | None |
| **Foundry features** | Foundry resource (`AIServices`, `allowProjectManagement: true`), project, model deployment, resource connections, AI Search connection, App Insights link |
| **Learning objectives** | Provision Foundry + AI Search via `azd`/Bicep; understand resource↔project↔connection model; verify keyless `DefaultAzureCredential` auth; read the generated `.env` contract |

> **Design note:** adopt FWH's **graceful Entra fallback** and **auto-`.env`** patterns, but deliver them
> through `azd up` + Bicep rather than raw `az rest` ARM PUT — the explicit gap FWH calls out **[FWH §5]**.
> Keep a `deploy.sh` Bash fallback for quota/region edge cases.

#### Foundations · Step 2 — Model Selection & the Playground
| Field | Detail |
|---|---|
| **Description** | Browse the model catalog, deploy two contrasting models (e.g. a flagship vs. a mini), and compare them in the **Playground** on Northfield questions. Iterate on **system instructions** and observe behavior changes. Then call the deployment from the `azure-ai-inference` / OpenAI SDK. |
| **Time** | 45 min |
| **Difficulty** | ⭐ Beginner |
| **Dependencies** | Foundations Step 1 |
| **Foundry features** | Model catalog, deployments (GlobalStandard / MaaS vs MaaP), Playground (Chat), system-instruction editing, content-filter awareness, Inference SDK |
| **Learning objectives** | Compare model families on cost/latency/quality; write effective **system instructions**; reproduce Playground behavior in code; understand deployment SKUs & capacity |
| **Maps E2E** | Model selection/comparison · Playground experimentation with system instructions |

#### Foundations · Step 3 — Your First Agent
| Field | Detail |
|---|---|
| **Description** | Promote your system-instruction prompt into a **named, versioned Foundry agent**. Define a persona ("Northfield Student Services Assistant"), guardrails, and refusal behavior. Create it both in the **portal** and via the SDK (`agents.create_version(PromptAgentDefinition(...))`); drive it through the **Responses API** and a conversation lifecycle. |
| **Time** | 45 min |
| **Difficulty** | ⭐⭐ Beginner–Intermediate |
| **Dependencies** | Foundations Step 2 |
| **Foundry features** | `AIProjectClient`, `PromptAgentDefinition`, `agents.create_version()`, Responses API, conversations API, Playground agent surface |
| **Learning objectives** | Understand agents as versioned resources; author persona + guardrails; code↔portal parity; manage conversation lifecycle |
| **Maps E2E** | Creating a basic agent |

> Borrows FWH's **agent-as-versioned-resource** idiom and the **Responses API + agent_reference** pattern **[FWH §4.3]**.

#### Foundations · Step 4 — Knowledge Base: Index + Foundry IQ  *(← Foundations end-state)*
| Field | Detail |
|---|---|
| **Description** | Ground the agent in Northfield's own data. Index `resources/sample-data/university-faq/` into **Azure AI Search**, build a **Foundry IQ knowledge base** over it (agentic retrieval: query decomposition → parallel search → rerank), and **attach it to the agent as a tool/MCP**. Compare grounded vs. ungrounded answers; verify **citations**. |
| **Time** | 1.5 hr |
| **Difficulty** | ⭐⭐⭐ Intermediate |
| **Dependencies** | Foundations Step 3 |
| **Foundry features** | AI Search vector/hybrid index, **Foundry IQ knowledge bases (preview)**, agentic retrieval, **Azure AI Search tool** (`VECTOR_SEMANTIC_HYBRID`), knowledge base exposed via **MCP**, RBAC (Search Index Data Contributor + Search Service Contributor, keyless via project MI) |
| **Learning objectives** | Build & populate a vector index; create an IQ knowledge base; attach it to an agent via MCP; reason about hybrid retrieval & citations; configure keyless RBAC |
| **Maps E2E** | Index documents in AI Search · Build a knowledge base (IQ) · Add Foundry IQ MCP to the agent |

> This is the headline upgrade: both reference repos **lack a real RAG/knowledge-base build** **[FWH §5, ATA]**.
> Uses `foundry-iq-knowledge-bases` + `tool-azure-ai-search.md` RBAC/query-type table **[SKILLS §2a, §5.1]**.

#### Advanced — Action Tools: Make the Agent Do Work
| Field | Detail |
|---|---|
| **Description** | Give the assistant hands. Attach an **MCP tool** that executes a real operation — e.g. *create an IT-support ticket*, *place a course-registration hold*, or *book an advising slot* — against a pre-built REST API (provided; teams **wire it, not build it**). Implement the **tool-approval loop** so the agent asks before acting. |
| **Time** | 1.25 hr |
| **Difficulty** | ⭐⭐⭐ Intermediate |
| **Dependencies** | **Foundations end-state** |
| **Foundry features** | `McpTool`, MCP server (APIM "Expose API as MCP" or a small FastMCP server), `RequiredMcpToolCall` + `SubmitToolApprovalAction` approval loop, function-call loop, subscription-key/header auth |
| **Learning objectives** | Distinguish **knowledge tools vs. action tools** **[ATA §3 Pattern 4]**; wire an MCP server; implement governed (human-approved) tool execution; close the function-call loop |
| **Maps E2E** | Add an MCP/tool that executes actions |

> Adopts ATA's **provide-the-API, teach-the-wiring** discipline + the `< PLACEHOLDER >` single-line
> completion moment **[ATA §4.3, §4.4]**. We ship the backend so learners stay on the MCP objective.

#### Advanced — Evaluation & Red Teaming
| Field | Detail |
|---|---|
| **Description** | Prove the assistant is accurate **and** safe. Run **NLP/quality metrics** (groundedness, relevance, coherence, fluency) over a Northfield eval dataset both in the portal and via a code-driven `evaluate.py`. Then run **red teaming / adversarial safety** (jailbreak, harmful content, prompt-injection via retrieved docs) using the AI Red Teaming Agent / safety evaluators. Add a custom domain evaluator. |
| **Time** | 1.25 hr |
| **Difficulty** | ⭐⭐⭐⭐ Advanced |
| **Dependencies** | **Foundations end-state** (richer with Action Tools) |
| **Foundry features** | `azure-ai-evaluation` (Groundedness, Relevance, Coherence, Fluency), custom evaluators, **AI Red Teaming Agent / safety evaluators**, content-safety, `.jsonl` datasets, portal Evaluations flow |
| **Learning objectives** | Run quality + safety evals; interpret per-row vs aggregate; build a custom evaluator; **red-team** an agent and read adversarial results; gate on score (CI concept) |
| **Maps E2E** | Evaluations: NLP metrics + red teaming |

> Fills the **single biggest gap** in both reference repos — neither ships eval **or** red teaming
> despite "trust" branding **[FWH §5, ATA §5]**. Expand dataset beyond the tiny 10-row samples **[FWH §5]**.

#### Advanced — Tracing & Observability
| Field | Detail |
|---|---|
| **Description** | Make every answer observable. Enable **OpenTelemetry GenAI tracing**, export to **Application Insights**, and inspect spans (model call, retrieval, tool call) in the portal **Tracing** tab and via **KQL**. Correlate a single student question end-to-end; surface token/latency/cost. |
| **Time** | 1 hr |
| **Difficulty** | ⭐⭐⭐⭐ Advanced |
| **Dependencies** | **Foundations end-state** (richer with Action Tools) |
| **Foundry features** | `AIProjectInstrumentor`, `configure_azure_monitor`, OTel GenAI semantic conventions, App Insights, Transaction Search / end-to-end Gantt, KQL, optional Workbook |
| **Learning objectives** | Instrument an agent; the **"set env before import"** gotcha **[FWH §3]**; read spans across model/retrieval/tool tiers; write a starter KQL; correlate eval↔trace |
| **Maps E2E** | Tracing & Observability |

> Teach the same data **two ways** (portal Tracing tab + App Insights/KQL) per FWH **[FWH §4.5]**;
> optionally ship ATA's 3-tier `TelemetryManager` + Workbook JSON as a stretch reference **[ATA §6]**.

#### Advanced — Deploy as a Hosted Agent
| Field | Detail |
|---|---|
| **Description** | Ship the assistant. Containerize and deploy it as a **hosted Foundry agent** with its own endpoint and per-agent **Entra identity** using `azd ai agent`. Invoke it via the Responses/Invocations protocol; review run history + traces against the live endpoint. |
| **Time** | 1 hr |
| **Difficulty** | ⭐⭐⭐⭐⭐ Advanced |
| **Dependencies** | **Foundations end-state** |
| **Foundry features** | **`foundry-hosted-agents`**, `agent.yaml`, `azd ai agent` (create → deploy → invoke), ACR, Responses/Invocations protocols, per-agent managed identity, run history |
| **Learning objectives** | Containerize & deploy a hosted agent; configure agent identity/auth; invoke a production endpoint; tie monitoring back to Ch06 |
| **Maps E2E** | (ships the artifact; foundation for Extras D & E) |

> Real containerized endpoint vs. FWH's "next steps only" deploy **[FWH §5, SKILLS §5.3]**.

---

### 3.5 Extras detail blocks

#### Extra A — Fabric IQ: Real-Time Data Grounding
| Field | Detail |
|---|---|
| **Description** | Ground the assistant on **live operational data** (e.g. real-time course-seat availability, dining-hall capacity) via the **Fabric IQ** tool, alongside the static FAQ knowledge base. |
| **Prereq** | Foundations end-state |
| **Infra needs** | **Microsoft Fabric** capacity (F-SKU / trial) + OneLake data; `tool-fabric-iq.md` wiring **[SKILLS §2c]** |
| **Time / Difficulty** | 1 hr / ⭐⭐⭐⭐ |
| **Demo wow-factor** | Assistant answers *"are there seats left in CS101 right now?"* with live numbers — static RAG can't do this. |

#### Extra B — Give It a Voice: Voice Live API
| Field | Detail |
|---|---|
| **Description** | Turn the text assistant into a **spoken** one using the **Voice Live API** — speech-in, speech-out, low-latency. |
| **Prereq** | Foundations end-state (works with Step 3 agent; better with Step 4 RAG) |
| **Infra needs** | Voice Live API access (Azure AI Speech/Foundry), mic-capable client; `azure-ai-voicelive-*` skill **[SKILLS §2b]** |
| **Time / Difficulty** | 1 hr / ⭐⭐⭐ |
| **Demo wow-factor** | A literal talking campus assistant — the strongest crowd demo of the event. |

#### Extra C — Magentic Workflows (Microsoft Agent Framework)
| Field | Detail |
|---|---|
| **Description** | Compose multiple specialized agents (e.g. *Triage*, *Knowledge*, *Action*, *Escalation*) using **MAF** with the **Magentic manager/planner** pattern — dynamic planning vs. the fixed sequential/fan-out of the core track. |
| **Prereq** | Advanced: Action Tools |
| **Infra needs** | `agent-framework` SDK; DevUI for visualization **[ATA §3, §6]** |
| **Time / Difficulty** | 1.5 hr / ⭐⭐⭐⭐⭐ |
| **Demo wow-factor** | A manager agent **plans live** which sub-agents to call — visualized in DevUI (green=done/purple=running) **[ATA §4.5]**. Both reference repos **lack** a Magentic pattern **[ATA §5]**. |

#### Extra D — MAF + Hosted Long-Running Agents
| Field | Detail |
|---|---|
| **Description** | Deploy the MAF workflow from Extra C as **hosted agents**, including a **long-running / background** agent (`background=True`) for async work (e.g. batch-processing enrollment requests overnight). |
| **Prereq** | Advanced: Deploy as a Hosted Agent + Extra C |
| **Infra needs** | ACR, hosted-agent endpoints, App Insights; `foundry-hosted-agents` + `foundry-workflows` **[SKILLS §2a]** |
| **Time / Difficulty** | 1.5 hr / ⭐⭐⭐⭐⭐ |
| **Demo wow-factor** | Submit a job, close the tab, come back to a completed long-running agent run with full trace history. |

#### Extra E — Build a UI for Your Agent
| Field | Detail |
|---|---|
| **Description** | Wrap the deployed hosted agent (Advanced: Deploy) in a clean web UI — chat window, citations panel, and an approval prompt for action tools. Recommended **capstone** for demo day. |
| **Prereq** | Advanced: Deploy as a Hosted Agent |
| **Infra needs** | Container Apps (or Static Web Apps), CORS to the agent endpoint; reuse FWH's `frontend-design` skill + `ui-designer` agent **[FWH §6]**; pattern after ATA's Container-Apps frontend **[ATA §2 Ch4]** |
| **Time / Difficulty** | 1 hr / ⭐⭐⭐ |
| **Demo wow-factor** | A polished, shareable app — the thing teams screenshot for the readout. |

#### Extra F — Copilot-Assisted Build (microsoft/skills)
| Field | Detail |
|---|---|
| **Description** | Re-build one challenge **"the agent-assisted way"**: with microsoft/skills Foundry skills + MCP servers loaded, let GitHub Copilot act as an expert pair-programmer that fetches **current** Foundry APIs before generating code. |
| **Prereq** | Foundations Step 1 (most valuable after a team has felt the manual path) |
| **Infra needs** | See §5 — skills + `.mcp.json` + `copilot-instructions.md` in the Codespace |
| **Time / Difficulty** | cross-cutting / ⭐⭐ |
| **Demo wow-factor** | Copilot one-shots a working agent tool using **live** SDK syntax — and teams see *why* grounding beats hallucinated calls **[SKILLS §3]**. |

---

## 4. The "Copilot + Foundry Skills" Enablement Layer

This is a **cross-cutting layer** (not just Extra F): Copilot is available the whole event as an
expert pair-programmer, while coaches still "never give answers directly." Source: **[SKILLS §3, §4]**.

### 4.1 What to drop into the student Codespace

```
.github/
  copilot-instructions.md          # tells Copilot which skills exist + the "Search-Before-Implement" rule
  skills/                          # ONLY the per-challenge skills (selective loading — see 4.3)
    foundry-projects-resources/    # Ch00
    foundry-models/                # Ch01
    foundry-iq-knowledge-bases/    # Ch03
    foundry-toolboxes/             # Ch03/04
    foundry-observability/         # Ch05/06
    foundry-hosted-agents/         # Ch07
    foundry-workflows/             # Extras C/D
.vscode/
  mcp.json                         # azure, foundry-mcp, microsoft-docs (copy verbatim) [SKILLS §6]
```

### 4.2 The three MCP servers (copy verbatim from `microsoft-foundry/.mcp.json`) **[SKILLS §2d]**

| Server | Transport | Role |
|--------|-----------|------|
| `azure` | stdio `npx -y @azure/mcp@latest server start` | Azure resource ops; the Foundry skill requires calling its `foundry` tool first as a discovery step |
| `foundry-mcp` | http `https://mcp.ai.azure.com` | Foundry-native: catalog, agents, **knowledge bases**, toolboxes, evals |
| `microsoft-docs` | http `https://learn.microsoft.com/api/mcp` | Fresh SDK syntax — kills the #1 student failure mode (hallucinated/stale API calls) |

### 4.3 The doctrine to teach

- **Selective loading is mandatory.** Ship ~7 Foundry skills + 2–3 companion SDK skills, **not** all 174
  — loading everything causes "context rot" **[SKILLS §1, §4]**.
- **"Search Before Implement" / "MCP = fresh info, Skills = proven patterns."** Copilot queries
  `microsoft-docs`/`foundry-mcp` *before* writing Azure SDK code **[SKILLS §2d, §6]**.
- **Coach inversion:** coaches load the **full** skill set to validate student solutions and unblock fast **[SKILLS §3]**.
- **Install path:** `npx skills add microsoft/skills --skill microsoft-foundry` (targeted) or the Skill
  Explorer 1-click UI; **pin a commit** since the repo is WIP and several features are preview **[SKILLS §4]**.

---

## 5. Infra / Setup Implications

### 5.1 Provisioning path: `azd up` + Bicep (golden path)

Replace v1's ad-hoc `setup-resources.sh` with an **`azure.yaml` + `infra/*.bicep`** module set deployed by
`azd up`, with a Bash `deploy.sh` fallback for quota/region edge cases. This is the explicit improvement
both reference repos skipped (FWH used raw `az rest`; ATA used one-click ARM) **[FWH §5, ATA §6]**.

**Bootstrap skip-path (Path B, §1.5):** in addition to `azd up` (infra), ship a
`scripts/setup-foundations.sh` that **materializes the Foundations end-state** (deploy model → create
agent → index Northfield corpus → build IQ knowledge base → attach via MCP) and a
`scripts/validate-foundations.py` that asserts it. This is the **single checkpoint** that unblocks every
Advanced challenge for teams who skip guided Foundations. Gate it in docs: *"recommended only if your
team already knows Foundry basics."*

### 5.2 Azure resources across the full curriculum

| Resource | Needed by | Notes |
|----------|-----------|-------|
| **Foundry resource** (`AIServices`, `allowProjectManagement`) | 00 → all | project-management flag required |
| **Foundry project** | 00 → all | |
| **Model deployment** (chat) | 01 → all | parameterize model + region; document fallbacks **[FWH §5]** |
| **Azure AI Search** | 03 → all | vector/hybrid index + IQ knowledge base; keyless RBAC |
| **Application Insights + Log Analytics** | 06, 07, D | OTel export target |
| **Azure Container Registry (ACR)** | 07, D | hosted-agent images |
| **Hosted agent endpoint(s)** | 07, D | per-agent Entra identity |
| **APIM** (or small FastMCP host) | 04 | "Expose API as MCP"; or vendor a FastMCP server |
| **Action backend API** | 04 | pre-built; ship in-repo (avoid ATA's external-repo risk) **[ATA §5]** |
| **Container Apps / Static Web Apps** | E | UI host + CORS |

**Extras requiring extra provisioning (flagged):**

| Extra | Extra infra |
|-------|-------------|
| A Fabric IQ | **Microsoft Fabric capacity** (F-SKU/trial) + OneLake — heaviest add |
| B Voice Live | **Voice Live API** access + mic client |
| C Magentic | none beyond core (MAF SDK only) |
| D Hosted MAF | ACR + extra hosted endpoints |
| E UI | Container Apps / SWA |
| F Copilot | none (Codespace files only) |

### 5.3 Devcontainer deltas vs v1

- **Remove:** `promptflow`, `promptflow-tools`, `ms-toolsai.promptflow`.
- **Add:** `azure-ai-agents`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`,
  `agent-framework` (extras), `azure-ai-voicelive` (Extra B); ensure **`azd`**, **`az`**, **Node/npx**
  (MCP servers), **Docker** (hosted agents) present **[SKILLS §4]**.
- Pre-load Copilot + Copilot Chat (already present) and wire `.vscode/mcp.json`.

---

## 6. Timing & Format Options

Reframed for the two-tier model: **Foundations** (Tier 1) is the shared base; **Advanced** challenges
(Tier 2) are picked à la carte. Strong teams use the **bootstrap skip-path** (§1.5) to compress Tier 1.

| Format | Audience | Track |
|--------|----------|-------|
| **1-day beginner** (~6–7 hr) | Students new to Foundry | Foundations (4 steps) → pick 2 Advanced (Action Tools + Deploy) |
| **1-day fast** (~7 hr) | Strong cohorts | Foundations → all 4 Advanced (Action Tools, Eval+RedTeam, Tracing, Deploy) |
| **1-day advanced-skip** (~6 hr) | Foundry-fluent teams | **Bootstrap (~15 min)** → all 4 Advanced + 1 Extra |
| **2-day** | Deep dive | Day 1: Foundations + Action Tools + Eval+RedTeam; Day 2: Tracing + Deploy + Extras **C Magentic** + **E UI** |
| **Demo-day / exec** | Showcase | Foundations → Action Tools + **Extra B Voice** + **Extra E UI** (maximize wow, minimize eval depth) |
| **Coach / advanced** | Practitioners | Bootstrap → all Advanced + Extras C/D + Extra F enablement |

**Recommended default:** 2-day — **Foundations + all four Advanced** + Extras C (Magentic) and E (UI).
Magentic + a live voice/UI demo are the highest-wow closers **[ATA §4.5, FWH §6]**.

---

## 7. Risks & Open Questions (validate before the event)

| Risk | Detail | Validate by |
|------|--------|-------------|
| **Preview-feature churn** | Foundry IQ, Toolboxes, hosted agents, managed skills, memory are **preview** **[SKILLS §4]** | Smoke-test each on the target subscription 2 weeks out; pin SDK versions |
| **`foundry-mcp` reachability** | `https://mcp.ai.azure.com` egress + auth from GitHub Codespaces unconfirmed **[SKILLS §6]** | Test from a clean Codespace; have fallback (docs MCP only) |
| **`azd ai agent` availability** | Hosted-agent CLI may not be in all Azure Pass/sandbox subs **[SKILLS §6]** | Confirm in sandbox; if absent, make Ch07 portal-based |
| **Model/region/quota** | FWH pins `gpt-5.4`/`swedencentral`; quota friction likely **[FWH §5, ATA §5]** | Parameterize model+region; document 2 fallbacks; pre-request quota |
| **Red-teaming tooling maturity** | AI Red Teaming Agent surface evolving | Lock the exact evaluator set + SDK version for Ch05 |
| **Fabric capacity cost** | Extra A needs a Fabric F-SKU/trial | Decide trial vs shared capacity; gate Extra A behind coach availability |
| **Voice Live access** | API availability/region for Extra B | Confirm access + a known-good client sample |
| **APIM "Expose as MCP" is preview** | Ch04 MCP path | Validate; keep a FastMCP server fallback we control |

---

## 8. Prioritized Build Backlog

Ordered; tag = primary owner. (Danny = Lead/Content, Rusty = Curriculum, Linus = Frontend/Docs,
Livingston = DevOps/Infra, Basher = DevRel/Coach.) Folder/page targets are specified in
[RESTRUCTURE-SPEC.md](RESTRUCTURE-SPEC.md).

| # | Work item | Owner | Why first |
|---|-----------|-------|-----------|
| 1 | **Restructure folders** to two-tier layout (`challenges/foundations/` + `challenges/advanced-*` + `challenges/extra-*`); execute the `git mv` map; **delete** `challenge-03-prompt-flow` | **Danny + Livingston** | Locks the new skeleton everyone authors into; per [RESTRUCTURE-SPEC.md](RESTRUCTURE-SPEC.md) |
| 2 | **`azd up` + Bicep provisioning** (Foundry + AI Search + App Insights + ACR) with auto-`.env` + Bash fallback | **Livingston** | Everything depends on reliable infra; unblocks all challenge authoring |
| 3 | **Bootstrap skip-path:** `scripts/setup-foundations.sh` + `scripts/validate-foundations.py` (materialize + verify the Foundations end-state — the single Path-B checkpoint) | **Livingston** | Unblocks every Advanced challenge for advanced-skip teams |
| 4 | **Strip Prompt Flow** everywhere (delete `challenge-03-prompt-flow`, `requirements.txt`, devcontainer ext, docs nav) + cut decision recorded | **Livingston + Danny** | Honor hard directive; prevents new content building on deprecated base |
| 5 | **Author Foundations** as ONE stepped challenge (Steps 1–4, each Goal→Tasks→Success→Checkpoint) ending in the grounded IQ Assistant; Step 4 (Knowledge Base) is the headline new content | **Rusty + Danny** | Tier 1 is the shared base every team needs; gates all Advanced |
| 6 | **Author Advanced: Action Tools** + ship the **pre-built action backend API + MCP server** (in-repo) | **Rusty + Livingston** | "Agent does work" is the core promise; backend must exist before content |
| 7 | **Author Advanced: Evaluation + Red Teaming** with code-driven `evaluate.py` + expanded Northfield eval dataset | **Basher + Rusty** | Fills the #1 gap in both reference repos; needs a real dataset |
| 8 | **Author Advanced: Tracing & Observability** + **Deploy as Hosted Agent** | Danny + Livingston | Completes the Advanced spine |
| 9 | Per-step / per-challenge **`validate.py`** implementing every Checkpoint in the STEP template | Rusty + Basher | Makes Success Criteria machine-checkable (gap both repos have) |
| 10 | Wire the **Copilot enablement layer** (skills subset + `.mcp.json` + `copilot-instructions.md`, pinned commit) | Livingston + Basher | Cross-cutting; validate `foundry-mcp` reachability |
| 11 | Build **Extra E (UI)** + reuse `frontend-design`/`ui-designer` | Linus | Demo-day capstone |
| 12 | Extras C (Magentic), D (hosted MAF), A (Fabric), B (Voice), F (Copilot) — author as bandwidth allows | Danny + Rusty | Optional tracks; sequence by demo value (C, E first) |
| 13 | Update `docs/` Jekyll nav + pages to mirror the two-tier layout 1:1 (Foundations page + per-Advanced pages + coach pages + index) | Linus | Keep Pages site in sync; per [RESTRUCTURE-SPEC.md](RESTRUCTURE-SPEC.md) |
| 14 | Author **facilitator guides** (coach `solution.md` per unit) + the Prompt-Flow removal verification pass | Basher | Coach enablement + QA the cut |

---

## 9. Bottom Line

V2 replaces a prompt-and-flow pipeline with a **single agent that grows into a deployed, grounded,
action-taking, observable product** — the Northfield IQ Assistant — and layers Copilot + microsoft/skills
on top as an always-on expert pair-programmer. It deletes deprecated Prompt Flow, fills the RAG / action /
red-teaming / hosted-deploy white space that the FrontierWeekHack and azure-trust-agents repos leave
open, and packages five optional high-wow extras for longer or showcase formats.
