# Research: microsoft/FrontierWeekHack

> Repo: <https://github.com/microsoft/FrontierWeekHack> · Docs site: <https://microsoft.github.io/FrontierWeekHack/>
> Description: *"Hands-on Microsoft Foundry session labs to build, monitor, evaluate, and deploy agentic AI workflows."*
> Researched: 2026-06-01 (repo last pushed 2026-05-24, default branch `main`) · by Danny (Lead & Content Architect)

---

## 1. Overview & Goals

FrontierWeekHack is the official **Microsoft Cloud & AI Frontier Week** hands-on lab. It is a **code-first** (Python SDK) session that walks a participant through the **full lifecycle of a production agentic system**: build → monitor → evaluate → orchestrate/deploy. It deliberately mixes IDE work with the **Microsoft Foundry portal** (`ai.azure.com/nextgen`) so learners experience both the SDK and the no-code surfaces.

Core learning objectives (from [`README.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/README.md)):

- **Agent design** — purpose-built agents with system prompts, tools, and domain data.
- **Observability** — OpenTelemetry GenAI tracing via Application Insights.
- **Quality evaluation** — LLM-as-judge evaluation to measure output quality.
- **Multi-agent orchestration** — wiring agents into workflows via the Python SDK *and* the portal designer.

Key design decision: **one structure, three interchangeable scenarios.** All three teach identical Foundry concepts; the learner picks the domain that resonates. This makes the lab reusable as a *template generator* (see the `lab-generator` agent in §4).

**Tech baseline** ([`requirements.txt`](https://github.com/microsoft/FrontierWeekHack/blob/main/requirements.txt)):
`azure-ai-projects>=2.0.0`, `azure-ai-agents>=1.1.0`, `azure-ai-evaluation>=1.16.7`, `azure-identity`, `python-dotenv`, `aiohttp`, `opentelemetry-sdk`, `azure-monitor-opentelemetry==1.8.7`, `azure-core-tracing-opentelemetry`.
Model used throughout: **`gpt-5.4`** (version `2026-03-05`), deployed `GlobalStandard`, capacity 10. Region **`swedencentral`**.

---

## 2. Lab / Activity Inventory

The repo ships **3 parallel scenario tracks**, each with the **same 5-activity spine**. Pick one track; all teach the same Foundry features.

### Scenario tracks

| Track | Company (fictional) | Domain | Agent 1 | Agent 2 | Tool | Data file |
|-------|---------------------|--------|---------|---------|------|-----------|
| 🏭 [`factory/`](https://github.com/microsoft/FrontierWeekHack/tree/main/factory) | TireForge Industries | Predictive maintenance | Anomaly Detection | Fault Diagnosis | `check_thresholds` | `sensor_data.json` (5 machines) |
| 📋 [`claims/`](https://github.com/microsoft/FrontierWeekHack/tree/main/claims) | ClaimSight Insurance | Claims processing | Claims Triage | Claims Decision | `check_thresholds`-equiv | `claims_data.json` (5 claims) |
| 📞 [`callcenter/`](https://github.com/microsoft/FrontierWeekHack/tree/main/callcenter) | NovaTel Communications | Customer support triage | Intent Classification | Resolution Advisor | `lookup_customer` | `call_data.json` (7 calls) |

### Per-track activity spine (identical across all 3)

| # | Activity | Topics taught | Foundry features used | Est. time |
|---|-----------|---------------|----------------------|-----------|
| 0 | **Setup** | Provision infra, deploy a model, verify Entra auth, write `.env` | Foundry resource (AIServices), Foundry project, model deployment, Log Analytics, App Insights | 20 min |
| 1 | **Build Agents** | Two agents w/ system prompts + a function tool; function-call loop; conversations API | `AIProjectClient`, `PromptAgentDefinition`, `FunctionTool`, `agents.create_version()`, Responses API, Playground | 30–35 min |
| 2 | **Monitor** | GenAI distributed tracing; spans for model + tool calls; token/latency; Kusto | `AIProjectInstrumentor`, `configure_azure_monitor`, App Insights, portal **Tracing** tab | 20 min |
| 3 | **Evaluate** | LLM-as-judge; per-row vs aggregate; CI/CD gating concept | `azure-ai-evaluation` (Coherence, Relevance evaluators), portal **Evaluations** flow, `.jsonl` dataset | 25–30 min |
| 4 | **Workflow / Deploy** | Multi-agent orchestration (SDK loop + portal DAG); hosted agents; streaming invoke; run history | `WorkflowAgentDefinition` (YAML), portal Workflow designer, Responses API `background=True`, run history + traces | 20 min |

Total: ~**2 hours** per track. Each track also has a [`wrapup.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/wrapup.md) (recap + next steps + cleanup) and a [`cleanup.sh`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/cleanup.sh).

---

## 3. Infra / Setup Approach

**Provisioning is a single Bash script per track**, not azd/bicep/Terraform. See [`factory/activity-0-setup/deploy.sh`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-0-setup/deploy.sh).

What `deploy.sh` does:
1. `SUFFIX=$(openssl rand -hex 4)` → unique resource names; RG `foundry-session-rg-<suffix>`, region `swedencentral`.
2. Creates the **Foundry resource** via raw ARM REST (`az rest PUT` to `Microsoft.CognitiveServices/accounts`, `kind: AIServices`, `allowProjectManagement: true`) — *not* `az cognitiveservices account create`, because it needs the project-management flag.
3. Polls `provisioningState` up to 36×10s until `Succeeded`.
4. Force-enables local auth (`disableLocalAuth=false`) but **gracefully degrades** to `DefaultAzureCredential` (Entra) if tenant policy blocks key auth — a nice resilience pattern.
5. `az cognitiveservices account project create` → the Foundry project.
6. Deploys model `gpt-5.4` (`GlobalStandard`, capacity 10).
7. Creates **Log Analytics workspace** → **App Insights** (linked to LA).
8. `az rest PATCH` to connect App Insights to the Foundry project's `applicationInsights` property.
9. Writes a fully-populated **`.env` to the repo root** (endpoint, project connection string, model name, App Insights conn string, tracing flags).

**Dev environment**: GitHub Codespaces is the recommended path (one-click badge), backed by a [`.devcontainer`](https://github.com/microsoft/FrontierWeekHack/tree/main/.devcontainer):
- Base image `mcr.microsoft.com/devcontainers/python:3.13-bullseye` (custom Dockerfile just removes the expired Yarn apt repo).
- Features: `azure-cli` (bicep off), `node` LTS.
- `postCreateCommand` upgrades pip + installs `requirements.txt`.
- Pre-loads VS Code extensions: **GitHub Copilot + Copilot Chat**, Python/Pylance, Jupyter, REST Client, Bicep, markdown-alert; theme GitHub Dark.

**Tracing config is env-driven** (set in `.env` by `deploy.sh`):
```
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```
`monitor.py` enforces these are set **before** importing the SDK.

**Docs site**: MkDocs Material ([`mkdocs.yml`](https://github.com/microsoft/FrontierWeekHack/blob/main/mkdocs.yml)) published to GitHub Pages via [`.github/workflows/deploy-pages.yml`](https://github.com/microsoft/FrontierWeekHack/blob/main/.github/workflows/deploy-pages.yml). Custom gradient theme in `overrides/stylesheets/extra.css`. The nav simply mirrors the 3×5 activity structure.

---

## 4. Notable Patterns We Should Borrow

1. **Pick-your-scenario, shared spine.** Three domains, identical 5-activity arc and identical code skeleton. Lowers cognitive load and lets us reuse one teaching backbone across verticals.

2. **"Why the activities are in this order" narrative.** Each track README has a *Build → Monitor → Evaluate → Deploy* rationale tied to real business stakes (e.g., a missed curing-press anomaly scraps a tire batch). This is excellent pedagogy — borrow the "explain the sequence" pattern. See [`factory/README.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/README.md).

3. **Concrete SDK idioms worth standardizing** (from [`agents.py`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-1-build/agents.py) / [`deploy.py`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-4-deploy/deploy.py)):
   - `AIProjectClient(endpoint=..., credential=DefaultAzureCredential())` → `.get_openai_client()` → drive everything through the **OpenAI Responses API** with `extra_body={"agent_reference": {"name": ..., "type": "agent_reference"}}`.
   - Agents are **named, versioned resources**: `client.agents.create_version(agent_name=..., definition=PromptAgentDefinition(model=..., instructions=..., tools=[...]))`.
   - **Explicit function-call loop**: inspect `response.output` for `type == "function_call"`, run the Python fn, feed back `FunctionCallOutput(call_id=..., output=...)`, repeat until no tool calls. The lab-generator agent flags this as "a key learning moment — don't skip it."
   - Conversation lifecycle: `conversations.create()` → `responses.create(conversation=...)` → `conversations.delete()`.

4. **Two agent archetypes**: Agent 1 = **detector/classifier WITH a tool** (grounded in data); Agent 2 = **reasoner WITHOUT tools** (pure diagnosis with domain heuristics baked into the system prompt, e.g. "high temp + high pressure → blockage"). Clean, repeatable teaching pattern.

5. **Tracing UX taught from both sides**: portal **Tracing** tab *and* App Insights Transaction Search / Performance / end-to-end Gantt / a starter **Kusto** query. Teaching the same data through two lenses is great. See [`activity-2-monitor/README.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-2-monitor/README.md).

6. **Eval done in the portal with a ready `.jsonl`** — `eval_portal.jsonl` has `query` + `ground_truth` columns; learner uploads, maps the `query` column, picks Coherence + Relevance, uses `gpt-5.4` as judge. Low-friction first taste of LLM-as-judge.

7. **Workflow taught three ways**: (a) hand-rolled Python orchestration loop, (b) **portal visual DAG designer**, (c) **SDK `WorkflowAgentDefinition`** authored as **portal-format YAML** (`InvokeAzureAgent` steps + `EndConversation`). Shows code↔portal parity.

8. **Honest limitation call-outs.** The lab explicitly explains that **portal workflow playground can't run local Python tools**, so it instructs embedding sensor data in the prompt instead (`do NOT call check_thresholds`). Teaching the constraint instead of hiding it builds trust.

9. **A `lab-generator` meta-agent.** [`.github/agents/lab-generator.agent.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/.github/agents/lab-generator.agent.md) is a Copilot custom agent that **generates a brand-new lab for any industry** following this exact structure (entities, metrics, thresholds, 2 agents, eval dataset, facilitator guide). Plus a `ui-designer` agent for the MkDocs theme and a bundled `frontend-design` skill. **This is the single most reusable asset** — it encodes the whole curriculum as a repeatable template. (Note: it references a `FACILITATOR_GUIDE.md` per lab, which is *not* actually present in the shipped tracks — a gap, see §5.)

10. **Self-cleanup discipline.** Every track has `cleanup.sh` (reads `.env`, confirms, `az group delete --no-wait`) and a wrap-up that lists 3 deletion options. Good cost hygiene to copy.

---

## 5. Gaps / Things We'd Do Differently

- **No IaC beyond Bash.** No `azd`, no Bicep/ARM templates (despite the Bicep VS Code extension being pre-installed). Raw `az rest` ARM PUT/PATCH calls are brittle and hard to parameterize. **We'd add an `azd up` + Bicep path** for repeatability and teardown, keeping the Bash script as a fallback.
- **No AI Search / RAG activity.** File Search + knowledge bases + vector stores are *described* conceptually in [`activity-1-build/README.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-1-build/README.md) but **never built**. There is no AI Search index, no document upload, no grounding lab. **Big opportunity** for our expanded curriculum — a real RAG/knowledge-base activity.
- **Evaluation is shallow.** Only generic **Coherence + Relevance**; no groundedness, no task-specific/custom evaluators, **no red-teaming / adversarial / safety eval**, no automated eval *script* in the shipped tracks (the lab-generator references `evaluate.py` but the tracks evaluate via the portal only). Datasets are tiny (10 rows). **We'd add: custom evaluators, groundedness, content-safety/red-team, and a code-driven `evaluate.py` wired into CI.**
- **No MCP tools.** No Model Context Protocol servers/tools anywhere — only local `FunctionTool`s. A clear modernization gap.
- **No advanced topics at all**: no Voice Live / Speech, no Fabric IQ, no Magentic / Microsoft Agent Framework (MAF) multi-agent patterns, no genuine *hosted-agent endpoint* deployment (it's described as "next steps" only), no UI/front-end app on top of the agents (the `frontend-design` skill ships but is unused in the labs). All called out as "Beyond the Lab."
- **Missing facilitator guides.** The lab-generator promises `FACILITATOR_GUIDE.md` with timing/reconvene points/common errors, but none exist in the actual tracks. We should actually ship these.
- **CI/CD is conceptual.** "Run eval on every PR, gate on score" is described but there's no GitHub Action doing it. Easy, high-value add.
- **Function-call loop duplicated** across `agents.py` and `deploy.py` with slight variations — no shared module. Minor, but we'd factor a small SDK helper to reduce copy-paste drift.
- **Hard-pinned preview model `gpt-5.4` + `swedencentral`** can cause quota/region friction; we'd parameterize and document fallbacks.

---

## 6. Reusable Assets Worth Referencing

| Asset | Path / URL | Why it's useful |
|-------|-----------|-----------------|
| **Lab generator agent** | [`.github/agents/lab-generator.agent.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/.github/agents/lab-generator.agent.md) | Encodes the entire 5-activity curriculum + agent design patterns as a reusable Copilot agent. Our curriculum template should start here. |
| **UI designer agent + frontend skill** | [`.github/agents/ui-designer.agent.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/.github/agents/ui-designer.agent.md), [`.github/skills/SKILL.md`](https://github.com/microsoft/FrontierWeekHack/blob/main/.github/skills/SKILL.md) | MkDocs theming + production-grade frontend skill we can reuse for our docs/site and any UI activity. |
| **Provisioning script** | [`factory/activity-0-setup/deploy.sh`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-0-setup/deploy.sh) | Reference for Foundry resource + project + model + App Insights wiring via CLI/REST; note the graceful Entra-fallback + `.env` autogen patterns. |
| **`.env` template** | [`factory/activity-0-setup/.env.template`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-0-setup/.env.template) | Canonical env-var contract (endpoint, project conn string, App Insights, tracing flags, workflow name). |
| **Agent SDK reference impl** | [`factory/activity-1-build/agents.py`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-1-build/agents.py) | Clean `PromptAgentDefinition` + `FunctionTool` + function-call-loop reference. |
| **Tracing setup** | [`factory/activity-2-monitor/monitor.py`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-2-monitor/monitor.py) | Minimal `AIProjectInstrumentor` + `configure_azure_monitor` pattern + the "set env before import" gotcha. |
| **Workflow-as-YAML** | [`factory/activity-4-deploy/deploy.py`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-4-deploy/deploy.py) `create_workflow_agent()` | Portal-format workflow YAML (`InvokeAzureAgent`/`EndConversation`) authored from the SDK — the code↔portal bridge. |
| **Eval datasets** | [`*/activity-3-evaluate/eval_portal.jsonl`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-3-evaluate/eval_portal.jsonl), [`*/activity-4-deploy/evaluation_dataset.json`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/activity-4-deploy/evaluation_dataset.json) | Ready `query`+`ground_truth` shape for LLM-as-judge; copy the schema, expand the row counts. |
| **Domain data files** | `*/activity-1-build/{sensor_data,claims_data,call_data}.json` | Three worked examples of the "5 entities × 4 metrics × thresholds × status" data model (2 warning + 1 critical seeded for interesting results). |
| **Devcontainer** | [`.devcontainer/devcontainer.json`](https://github.com/microsoft/FrontierWeekHack/blob/main/.devcontainer/devcontainer.json) | Codespaces config w/ Copilot + Azure CLI + Python pre-wired. |
| **Cleanup script** | [`factory/cleanup.sh`](https://github.com/microsoft/FrontierWeekHack/blob/main/factory/cleanup.sh) | `.env`-driven RG teardown with confirmation prompt. |
| **MkDocs site config** | [`mkdocs.yml`](https://github.com/microsoft/FrontierWeekHack/blob/main/mkdocs.yml) + `deploy-pages.yml` | Drop-in docs-site scaffolding mirroring the activity structure. |

---

### One-line bottom line
A polished, narrowly-scoped **2-hour "agent lifecycle" lab** (build → trace → evaluate → orchestrate) on the Foundry SDK + portal, with a brilliant **lab-generator meta-agent** — but it deliberately stops short of RAG/AI Search, MCP, red-teaming, hosted endpoints, voice, Fabric, and MAF/Magentic, which is exactly the white space our expanded curriculum should fill.
