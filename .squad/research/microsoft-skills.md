# Research Notes — `microsoft/skills`

> **Author:** Livingston (DevOps & GitHub Engineer)
> **Date:** 2026-06-01
> **Repo:** https://github.com/microsoft/skills (branch `main`, last push 2026-05-24)
> **Tagline:** *"Skills, custom agents, AGENTS.md templates, and MCP configurations for AI coding agents working with Azure SDKs and Microsoft AI Foundry."*
> **Scope of this doc:** Research-only. How we could "plop GitHub Copilot on top of" the AI Starter Kit RVAS (`Build Intelligent Apps with Microsoft Foundry`) using these Foundry skills + MCP servers.

---

## 1. Overview & What the Repo Provides

`microsoft/skills` is Microsoft's official **"Context-Driven Development"** library for AI coding agents (GitHub Copilot in VS Code, Copilot CLI, Claude Code, opencode). It does **not** ship runtime libraries — it ships *activation context*: curated `SKILL.md` knowledge files, custom agent personas, an `AGENTS.md` template, reusable prompts, and pre-wired MCP server configs. The thesis (stated in the README): the SDK patterns are already in the model's pretrained weights; skills just supply the *right activation context* to surface them, paired with MCP servers that fetch *fresh* API signatures so generated code isn't stale.

Headline numbers (from `README.md`):
- **174 skills** across Core + 5 language plugins (Python `-py`, .NET `-dotnet`, TypeScript `-ts`, Java `-java`, Rust `-rust`).
- **11 language-agnostic Foundry skills** — the part most relevant to our session.
- **Skill Explorer** with 1-click install: https://microsoft.github.io/skills/
- Backing blog: *"Context-Driven Development: Agent Skills for Microsoft Foundry and Azure"* (devblogs.microsoft.com/all-things-azure).

**Core mechanics (from `.github/docs/agent-integration.md`):**
- **Progressive disclosure / 3-tier loading** — Tier 1 metadata (`name`+`description`, ~50–100 tokens, loaded at startup) → Tier 2 full `SKILL.md` body (loaded on activation) → Tier 3 `references/`, `scripts/`, `assets/` (loaded on demand).
- Discovery: agents scan `.github/skills/` for folders containing `SKILL.md`; Copilot also reads `.github/copilot-instructions.md` and `.github/agents/*.agent.md`.
- **Selective loading is mandatory** — the README and docs repeatedly warn that loading all skills causes "context rot" (diluted attention, wasted tokens, conflated SDK patterns). Only copy the skills a project actually needs.

**Repo layout (key paths):**
```
AGENTS.md                         # agent-config template (referenced; root file currently 404s on raw)
.github/skills/                   # backward-compat symlinks to plugin skills
.github/plugins/                  # the real content — language + Foundry bundles
  ├─ azure-sdk-python|dotnet|typescript|java|rust/   # per-language SDK skills
  ├─ azure-skills/                # 35 Azure ops skills + the big microsoft-foundry router
  ├─ microsoft-foundry/           # standalone Foundry plugin (10 sub-skills + .mcp.json)
  ├─ deep-wiki/                   # wiki/onboarding generator plugin
.github/agents/                   # 6 agent personas (backend, frontend, infra, planner, presenter, scaffolder)
.github/prompts/                  # reusable prompt templates
.github/docs/                     # agent-integration.md, mcp-usage.md, skills.md, workflow-patterns.md, pattern-enforcement.md
.vscode/mcp.json                  # reference MCP server configs
docs/                             # generated llms.txt / llms-full.txt (daily workflow, GitHub Pages)
tests/                            # Copilot SDK test harness (Ralph Loop, Sensei scoring)
```

> ⚠️ **Note:** The `azure-skills` plugin is *vendored* from [`microsoft/github-copilot-for-azure`](https://github.com/microsoft/github-copilot-for-azure) — upstream changes belong there. Several Foundry sub-skills exist in **two** places: the standalone `microsoft-foundry` plugin (clean, language-agnostic, with its own `.mcp.json`) and a larger router under `azure-skills/skills/microsoft-foundry/` (with `foundry-agent/` deploy/invoke/observe/trace/troubleshoot/create/agent-optimizer sub-workflows).

---

## 2. Inventory of Relevant Skills / MCP Servers / Agents

### 2a. Foundry skills (language-agnostic) — the core of a Copilot+Foundry track
Source: `.github/plugins/microsoft-foundry/skills/` and `.github/plugins/azure-skills/skills/microsoft-foundry/`

| Skill | What it does | Session activity fit |
|-------|--------------|-------------------------|
| `microsoft-foundry` (orchestrator/router) | Maps user intent → correct sub-skill + discovery surface (Docs MCP, Foundry MCP, `azd ai agent`, `az`). The `azure-skills` variant adds full agent lifecycle sub-skills: **deploy, invoke, observe, trace, troubleshoot, create, agent-optimizer, eval-datasets, finetuning, quota, rbac**. | All / Ch00 |
| `foundry-projects-resources` | Provision Foundry resources & projects; connections (key / OAuth / managed identity / agent identity); standard vs private-network infra. | Ch00 Setup |
| `foundry-models` | Discover/deploy/manage models; preset vs customized deploy; capacity discovery across regions; quota; PTU vs PAYG; RAI policy. | Ch01 First Model |
| `foundry-hosted-agents` | Build/deploy/manage **hosted (containerized) agents** — Responses + Invocations protocols, `agent.yaml`, `azd ai agent`, per-agent Entra identity, dedicated endpoints. | Ch06 Deploy |
| `foundry-toolboxes` | Curate intent-based **Toolboxes (preview)** — one MCP-compatible endpoint bundling **9 tool types: MCP, Web Search, Azure AI Search, Code Interpreter, File Search, OpenAPI, A2A, Browser Automation, Computer Use**. Build once, consume everywhere. | Action Tools / Knowledge Base / Extras |
| `foundry-workflows` | Multi-agent orchestration — declarative workflow vs A2A tool call vs **Connected Agents** pattern; Microsoft Agent Framework patterns. | Capstone / Magentic Workflows |
| `foundry-iq-knowledge-bases` | **Foundry IQ knowledge bases (preview)** — multi-source, permission-aware grounding. Connect Blob/SharePoint/OneLake/web; **agentic retrieval pipeline (query decomposition + parallel search + reranking)**; expose via MCP to agents. | **Ch04 RAG** |
| `foundry-managed-skills` | `SKILL.md` as a **Foundry-side resource (preview)** — author behavioral guidelines once, store via Skills REST API, load into hosted-agent containers as session instructions. Decouples policy from code. | Extras / governance |
| `foundry-memory` | Long-term **managed memory (preview)** — user-profile vs chat-summary memory, memory-search tool vs store APIs, scoping, prompt-injection/memory-corruption risks. | Extras |
| `foundry-observability` | Trace/monitor/evaluate hosted agents — OpenTelemetry GenAI traces in App Insights (KQL), eval↔trace correlation, `azd ai agent monitor`, dataset curation from prod traces, built-in quality + safety/RAI evaluators, batch evals, regression detection. | **Ch05 Evaluation** |
| `foundry-governance` | Govern agent fleets — Foundry Control Plane + **AI Gateway** (MCP routing/policy), RBAC, agent identity, RAI policies, transparency notes. | Extras / facilitator track |

### 2b. Companion SDK skills (called by Foundry agents)
| Capability | Skills | Plugin |
|------------|--------|--------|
| **AI Search** (vector / hybrid / agentic retrieval) | `azure-search-documents-py`, `-dotnet`, `-ts` | `azure-sdk-*` |
| **High-level Foundry SDK** (project client, versioned agents, evals, connections) | `azure-ai-projects-py` (12 test scenarios — top-tested skill), `-dotnet`, `-ts`, `-java` | `azure-sdk-*` |
| **Agent Framework** (persistent agents, hosted tools, MCP, streaming) | `agent-framework-azure-ai-py` | `azure-sdk-python` |
| **Content Safety** (RAI / harmful-content detection) | `azure-ai-contentsafety-py`, `-ts`, `-java` | `azure-sdk-*` |
| **App service layer** (RAG API host) | `fastapi-router-py`, `pydantic-models-py`, `azure-cosmos-db-py` | `azure-sdk-python` |
| **Voice** | `azure-ai-voicelive-*` | `azure-sdk-*` |

### 2c. Foundry "action-executing" tools (agent tool references)
Source: `.github/plugins/azure-skills/skills/microsoft-foundry/foundry-agent/create/references/`

| Tool reference file | What it wires up |
|--------------------|------------------|
| `tool-azure-ai-search.md` | **Azure AI Search tool** — grounds agent on a vector index. Documents RBAC (Search Index Data Contributor + Search Service Contributor on the AI Search resource, keyless via project managed identity), project connection setup, and query types: `SIMPLE`, `VECTOR`, `SEMANTIC`, `VECTOR_SIMPLE_HYBRID`, `VECTOR_SEMANTIC_HYBRID` (default/recommended). |
| `tool-file-search.md` | File Search tool (upload-and-ground). |
| `tool-fabric-iq.md` | Fabric IQ grounding tool. |
| `tool-web-search.md` | Web Search tool. |
| `tool-work-iq.md` | Work IQ (M365) tool. |
| `tool-tool-search.md` | Tool-search (dynamic tool discovery). |
| `toolbox-reference.md` / `use-toolbox-in-hosted-agent.md` | How to bundle the above into a Toolbox and consume it from a hosted agent. |

### 2d. MCP servers
**Foundry plugin MCP wiring** — `.github/plugins/microsoft-foundry/.mcp.json` (auto-activates on plugin install):
| Server | Transport | Purpose |
|--------|-----------|---------|
| **`azure`** | stdio `npx -y @azure/mcp@latest server start` | Azure resource mgmt, deployments, 40+ services. The `microsoft-foundry` skill **requires** calling the `foundry` tool on this MCP first as a discovery step. |
| **`foundry-mcp`** | http `https://mcp.ai.azure.com` | Foundry-native ops: model catalog, agents, **toolboxes, knowledge bases**, evals. |
| **`microsoft-docs`** | http `https://learn.microsoft.com/api/mcp` | Real-time Microsoft Learn search (fetch current SDK syntax). |

**Repo-wide reference MCP set** — `.vscode/mcp.json`: `microsoft-docs`, `context7`, `deepwiki`, `github`, `playwright`, `terraform`, `ESLint`, `sequentialthinking`, `memory`, `markitdown`, `huggingface`, `svelte` (+ prompt-string `inputs` for tokens). Usage rules in `.github/docs/mcp-usage.md`: **"Search Before Implement"** — always query `microsoft-docs` MCP *before* writing Azure SDK code, then load the skill, then implement (*"MCP = Fresh information. Skills = Proven patterns."*).

### 2e. Custom agents & AGENTS.md
- `.github/agents/`: `backend.agent.md`, `frontend.agent.md`, `infrastructure.agent.md`, `planner.agent.md`, `presenter.agent.md`, `scaffolder.agent.md`. Personas declare expertise + which skills to load (e.g., backend → FastAPI/Pydantic/Cosmos; infra → Bicep/Azure CLI/Container Apps).
- `AGENTS.md` (repo root) — template for configuring agent behavior in *your* project. Verify the
  current upstream filename before vendoring because this area changes with the skills repo.
- `.github/copilot-instructions.md` — the workspace-level instruction file Copilot reads to know which skills exist.

---

## 3. How GitHub Copilot Could Be Layered onto Our Session

Our workshop (`PLAN.md`) already mirrors the Foundry lifecycle, so the skill→activity mapping is almost 1:1:

| Our Activity | Topic | Drop-in Foundry skill(s) | MCP servers |
|---------------|-------|--------------------------|-------------|
| **00 Setup** | Provision Foundry resource/project | `foundry-projects-resources`, router `project/create` + `resource/create` | `azure`, `foundry-mcp` |
| **01 First Model** | Deploy from model catalog | `foundry-models` (`models/deploy-model`: preset/customize/capacity) | `foundry-mcp`, `microsoft-docs` |
| **02 Prompt Engineering** | Prompt design | `azure-ai-projects-*`, prompt templates | `microsoft-docs` |
| **Capstone / Magentic Workflows** | Agent orchestration | `foundry-workflows` (Connected Agents), `foundry-toolboxes` | `foundry-mcp` |
| **04 RAG** | Grounded retrieval | **`foundry-iq-knowledge-bases`** + `azure-search-documents-py` + `tool-azure-ai-search.md` | `foundry-mcp`, `azure` |
| **05 Evaluation** | Quality/safety/RAI | **`foundry-observability`** + `azure-ai-contentsafety-py` | `azure`, `microsoft-docs` |
| **06 Deploy** | Endpoint + app integration | **`foundry-hosted-agents`** + router `deploy`/`invoke` (`azd ai agent`) | `azure`, `foundry-mcp` |

**The "plop Copilot on top" model:** participants keep solving activities *the manual way* (which is the learning objective — facilitators "never give answers directly"), but Copilot becomes the **always-available expert pair-programmer**:
1. Add the relevant `SKILL.md` files + `.vscode/mcp.json` + `.github/copilot-instructions.md` to the student Codespace.
2. Copilot, when asked, queries `microsoft-docs`/`foundry-mcp` for *current* Foundry API surface (avoids the #1 student failure mode: hallucinated/stale SDK calls).
3. The `microsoft-foundry` router enforces a *workflow* (read sub-skill → discovery step → implement → validate), which keeps Copilot from jumping straight to unverified code and instead walks the same path the activity teaches.
4. This is **inversely useful for facilitators**: a facilitator can run the full lifecycle with these skills to validate student solutions and unblock fast.

---

## 4. Setup / Infra Implications

**Install paths (from README):**
- One-shot wizard: `npx skills add microsoft/skills` → installs selected skills to `.github/skills/` (Copilot) and symlinks for multi-agent setups (`.opencode/skills`, `.claude/skills`).
- Copilot CLI plugins: `/plugin marketplace add microsoft/skills` then `/plugin install microsoft-foundry@skills` (or `azure-skills@skills`, `deep-wiki@skills`).
- Targeted: `npx skills add microsoft/skills --skill microsoft-foundry`.
- Manual: `git clone` + `cp -r` / `ln -s` specific skill folders.

**Runtime / dependency requirements:**
- **Node/npx** for MCP servers (`@azure/mcp`, `@upstash/context7-mcp`, `@modelcontextprotocol/*`, `@playwright/mcp`).
- **`azd` (Azure Developer CLI)** + **`az` CLI** — Foundry agent lifecycle (`azd ai agent`, `azd env get-values`, `azure.yaml` with `host: azure.ai.agent`).
- **Docker** — hosted-agent containerization (build → ACR push) and the `terraform` MCP.
- **Azure subscription + Foundry project** — already a session prerequisite; hosted agents also need **ACR**, **App Insights** (observability), and **RBAC** (e.g., AI Search tool needs *Search Index Data Contributor* + *Search Service Contributor* on the AI Search resource; keyless via the project's managed identity is recommended).
- **`foundry-mcp` is a hosted HTTP endpoint** (`https://mcp.ai.azure.com`) — needs network egress + Azure auth; verify it's reachable from GitHub Codespaces.
- Optional secrets via `mcp.json` `inputs` (HF token, memory file path, Clarity token).

**Context-budget discipline (critical for a student Codespace):** do **not** ship all 174 skills. Ship only the ~7 Foundry skills + 2–3 companion SDK skills mapped to the active activity. The repo itself enforces this warning in both `README.md` and `.github/docs/agent-integration.md`.

**Currency risk:** repo is flagged **Work in Progress**; many Foundry features are **preview** (Toolboxes, Foundry IQ, managed-skills, memory). Pin to a commit if we vendor, and lean on `microsoft-docs` MCP for live syntax.

---

## 5. Specific Items Worth Integrating into an Advanced / Extras Activity

A bolt-on **"Activity 07 (Extras): Copilot + Foundry Skills — Build an Agent the Agent-Assisted Way"**:

1. **Foundry IQ knowledge base for RAG (upgrade Ch04):** instead of hand-rolling an index, use `foundry-iq-knowledge-bases` + the agentic retrieval pipeline (decomposition + parallel search + rerank) over the existing `resources/sample-data/university-faq/` corpus. Expose it via MCP to an agent. *Files:* `.github/plugins/microsoft-foundry/skills/foundry-iq-knowledge-bases/`, `tool-azure-ai-search.md`.
2. **Toolbox assembly:** have teams curate a `foundry-toolboxes` endpoint bundling AI Search + Web Search + Code Interpreter, then consume it from a hosted agent (`use-toolbox-in-hosted-agent.md`). Demonstrates "build once, consume everywhere."
3. **Hosted agent deploy with `azd ai agent` (upgrade Ch06):** `foundry-hosted-agents` + router `create → deploy → invoke`, Responses protocol, per-agent Entra identity. Real containerized endpoint vs a notebook.
4. **Eval-driven dev loop (upgrade Ch05):** `foundry-observability` — OpenTelemetry traces in App Insights, batch evals, **regression detection**, dataset curation from production traces; optionally the **agent-optimizer** / `prompt_optimize` MCP tool to auto-improve instructions.
5. **Responsible AI gate:** `azure-ai-contentsafety-py` + `foundry-governance` RAI policies as a "ship gate" — fits our Learning Outcome #5 (evaluate for safety/RAI).
6. **Connected Agents / multi-agent (stretch):** `foundry-workflows` Connected Agents pattern as a capstone.
7. **Facilitator enablement:** the `deep-wiki` plugin (`/deep-wiki:onboard`, `/deep-wiki:agents`, `/deep-wiki:generate`) to auto-generate an onboarding wiki + `AGENTS.md` for the session repo itself.

---

## 6. Reusable Assets Worth Referencing

| Asset | Path / URL | Why reuse |
|-------|-----------|-----------|
| Foundry plugin MCP config | `.github/plugins/microsoft-foundry/.mcp.json` | Exact 3-server wiring (`azure`, `foundry-mcp`, `microsoft-docs`) — copy verbatim into student Codespace. |
| Reference MCP set | `.vscode/mcp.json` | Full server catalog incl. `context7`, `playwright`, `github`, `sequentialthinking`. |
| MCP usage doctrine | `.github/docs/mcp-usage.md` | "Search Before Implement" decision tree — good facilitator handout. |
| Agent integration model | `.github/docs/agent-integration.md` | Progressive-disclosure / selective-loading rules — explains the token economics to participants. |
| Skill authoring guide | `.github/skills/skill-creator/SKILL.md` | If we want to write *session-specific* skills (e.g., a "university-faq-rag" skill). |
| MCP builder skill | `.github/skills/mcp-builder/` | Teams building a custom MCP tool (FastMCP/Node/.NET) as a stretch goal. |
| Copilot SDK skill + test harness | `.github/skills/copilot-sdk/`, `tests/` (Ralph Loop, Sensei scoring) | Pattern for *auto-grading* student output against acceptance criteria (1158 test scenarios across 128 skills). |
| Agent personas | `.github/agents/*.agent.md` | `planner`, `backend`, `infrastructure` personas as starting points for role-based team work. |
| Prompt templates | `.github/prompts/` (`code-review`, `add-endpoint`, `create-store`, `create-node`) | Reusable, drop into our prompt-engineering activity. |
| `azure-ai-projects-py` skill | `.github/plugins/azure-sdk-python/skills/azure-ai-projects-py/` | Highest-tested Foundry SDK skill (12 scenarios) — most reliable Copilot grounding for our Python audience. |
| AI Search tool reference | `…/microsoft-foundry/foundry-agent/create/references/tool-azure-ai-search.md` | Copy-paste RBAC + query-type table for Ch04. |
| Skill Explorer | https://microsoft.github.io/skills/ | 1-click install UI; share with participants. |
| Blog (rationale) | https://devblogs.microsoft.com/all-things-azure/context-driven-development-agent-skills-for-microsoft-foundry-and-azure/ | Framing/intro for a kickoff slide. |

---

### Open questions / follow-ups
- Confirm `foundry-mcp` (`https://mcp.ai.azure.com`) reachability + auth flow from a student GitHub Codespace.
- Decide vendor-vs-reference: pin a commit (repo is WIP + many previews) vs `npx skills add` live.
- Validate `azd ai agent` availability in the target Azure Pass/sandbox subscriptions before promising a hosted-agent activity.
