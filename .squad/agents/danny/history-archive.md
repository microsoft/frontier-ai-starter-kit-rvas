# History Archive — Danny

> Archived 2026-06-01 by Scribe (history.md exceeded 15360 B). Verbatim prior history below; active history.md now carries a tight summary.

---

## Learnings

### Project Context
- **Project:** AI Starter Kit RVAS — Microsoft Foundry format
- **Repo:** ai-starter-kit-rvas
- **Stack:** Microsoft Foundry AI, GitHub Pages (Jekyll/static), Markdown, GitHub Actions
- **Participants:** Students (new to AI) + Facilitators (facilitators)
- **Goal:** Create a complete, deliverable session format with a polished GitHub Pages site
- **Requested by:** Marco Olivo
- **Date:** 2026-05-28

### Content Architecture Decisions (2026-05-28)
- Chose 7 activities (00–06) with strict linear progression — simplifies logistics for 1-day events
- Activity 00 is setup-only: isolates environment issues from learning content
- Evaluation (Ch 05) precedes Deployment (Ch 06) — teaches responsible AI before shipping
- Facilitator solutions stay in-repo only, never on public Pages — keeps student experience clean
- RAG activity uses pre-provided sample data to remove data-sourcing as a blocker
- `just-the-docs` Jekyll theme selected for search, sidebar nav, and minimal config
- Devcontainer is the primary environment — eliminates "works on my machine" issues at scale
- Activity time estimates total ~7.25 hours — fits a full 1-day event with breaks

### README.md Implementation (2026-05-28)
- Wrote root README.md following full specification from task brief
- Includes all sections: header with 3 badges, What is (3 paragraphs), Learning Outcomes (6 points from PLAN.md), Who is this for (Students/Facilitators subsections), Prerequisites (5 items), Getting Started (3 steps with Codespaces badge), Activities table (all 7 with links and timings), Repository Structure (15-line annotated tree), For Facilitators section with Facilitator Hub link and solution guide notes, Resources (4 key links), Contributing section, and MIT License
- Chose accessible, welcoming tone appropriate for both students and facilitators
- Codespaces badge uses placeholder org path (microsoft/ai-starter-kit-rvas) — adjust repo URL in actual GitHub org
- All activity links follow standard path pattern: `activities/activity-NN-slug/README.md`

---

### 2026-06-01 — Curriculum V2 direction (Scribe note)
- `PLAN-V2.md` is the new curriculum direction (Proposed): agent-era rearchitecture, core spine 00–07, one-artifact-many-acts Northfield "IQ" Assistant narrative.
- **Prompt Flow is CUT** per Marco's directive — old Activity 03 removed; dependent RAG/eval steps re-expressed on Agents + AI Search + Foundry IQ + MCP + MAF; `promptflow*` deps leave the devcontainer.
- See `.squad/decisions.md` and `.squad/log/2026-06-01-curriculum-v2-planning.md`.

### 2026-06-01 — Authored two Advanced activities (Tracing + Deploy hosted agent)
- Built `advanced-tracing-observability/` (README + solution) from scratch and **rewrote**
  `advanced-deploy-hosted-agent/` (ex `activity-06-deploy`, git mv'd) — both on the §3 STEP template
  (Goal → Tasks → Success Criteria → Checkpoint) under the §3.2 Tier-2 banner + bootstrap skip-path line.
- **Tracing (4 steps):** enable GenAI instrumentation (`AIProjectInstrumentor`, `configure_azure_monitor`,
  the *set-env-before-import* gotcha) → run agent to emit spans → portal Tracing-tab span tree
  (model/retrieval/tool) → KQL end-to-end correlation by `operation_Id` surfacing token/latency/cost
  (`dependencies`/`requests`/`traces` union; `customDimensions["gen_ai.usage.*"]`). Artifact: `correlate.kql`.
- **Deploy (4 steps):** author `agent.yaml` (responses protocol, port 8088) + MAF server entrypoint +
  Dockerfile → `az acr build` (mandatory `--source-acr-auth-id "[caller]"`, timestamp tag) +
  `azd ai agent create/deploy` (wait for version `active`) → invoke Responses endpoint + verify
  per-agent managed identity & auth enforcement (401/403 anon) → run history + App Insights traces back
  to the Tracing activity (`cloud_RoleName` scopes hosted runs).
- **Prompt Flow fully removed from ex-Ch06:** no managed-online-endpoint or Flask-deploy framing; the
  only remaining PF mentions are explicit "this was removed / steer teams off old printouts" callouts.
  Flask/Streamlit UI reframed as the separate *Build a UI* extra.
- **Lessons / gotchas captured for the team:**
  - `azd ai agent deploy` exit 0 ≠ done — hosted version provisions async; gate on `status==active` or
    invokes return `424 FailedDependency`/`session_not_ready`.
  - `az acr build` fails without `--source-acr-auth-id "[caller]"`; reused image tags serve stale layers.
  - Two-identity model: caller bearer token authenticates *into* endpoint; per-agent MI is what the
    agent uses to reach model/KB. `403` on authed call ⇒ caller missing `Azure AI User` role.
  - Hosted agents must bind `0.0.0.0:8088` + declare `responses` v1.0.0 or never go healthy.
  - Tracing: flags must be set above all `azure.ai.*` imports or message content is silently dropped.
- Left `validate.py` to Basher per brief — activities reference `python validate.py --step N` checkpoints
  with explicit expected PASS strings so the QA harness has a contract to implement against.
- Decision logged: `.squad/decisions/inbox/danny-tracing-deploy.md`.

### 2026-06-01 — Authored FIVE Extra activities (Fabric IQ, Voice Live, Magentic, Hosted Long-Running, Copilot-Assisted)
- Filled all 10 placeholder files (5 README + 5 solution) on the §3 STEP template under the §3.2 Tier-2
  banner; each opens with a per-Extra **specific prereq** line + an **infra-prerequisite** + **demo
  wow-factor** callout block. **extra-build-ui left untouched (Linus owns it).**
- Used the authoritative env contract verbatim in snippets: `AZURE_AI_PROJECT_ENDPOINT`,
  `AZURE_FOUNDRY_AGENT_NAME`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_SEARCH_*`,
  `APPLICATIONINSIGHTS_CONNECTION_STRING`, `ACTION_MCP_URL` (matches livingston-infra.md).
- **Checkpoint policy by Extra:** Magentic gets a real `python validate.py --step {1,2}` contract
  (headless-checkable: 4 agents defined; ≥2 specialists fan out) + DevUI visual for step 3. The other
  four are **portal/live-state** checkpoints — their deliverables are live data, audio, deployed async
  runs, or a Copilot *behavior*, none statically assertable. Documented *why* in each solution.md.
- **Prereq chain encoded:** Fabric→Step 4; Voice→Step 3; Magentic→Action Tools; Hosted-LR→Deploy + Magentic
  (two prereqs — flagged as capstone-only); Copilot→Step 1 (best AFTER a manual activity, contrast = lesson).
- **Search-Before-Implement enforced** in every code-bearing Extra: preview surfaces (Fabric tool class,
  `azure-ai-voicelive`, MAF `ChatAgent`/Magentic, `azd ai agent`/background-run) are NEVER hard-coded;
  students sent to `microsoft-docs`/`foundry-mcp` via the matching skill. Reference snippets in solution.md
  are marked "illustrative — confirm current names."
- **Infra flags for facilitators (gating):** Fabric IQ needs F-SKU/trial capacity + OneLake live table
  (`course_seats`) — gate behind facilitator availability, **pause capacity after** (bills while on). Voice Live
  needs regional API access + mic/headset client (silent failure if absent). Hosted-LR: localhost→container
  gap on `ACTION_MCP_URL` is the #1 deploy surprise (tunnel/deploy the backend). Copilot: corporate proxy can
  block the http MCP endpoints — test connectivity at setup.
- Referenced the real Livingston-shipped files in Extra F: `.github/copilot-instructions.md`,
  `.vscode/mcp.json` (azure/foundry-mcp/microsoft-docs), `.github/skills/*/SKILL.md` (7 stubs, selective load).
- Decision logged: `.squad/decisions/inbox/danny-extras.md`.

### 2026-06-01 — Curriculum V2 implemented (cross-agent note)
Curriculum V2 is now built to disk (staged, not committed). Final shape: **two-tier** — Tier 1 Foundations (4 ordered steps) + Tier 2 (4 Advanced activities + 6 Extras). **Prompt Flow fully removed** (deps, devcontainer, activities, docs). `docs/` mirrors `activities/` 1:1 with facilitator siblings. Decision inbox merged into `.squad/decisions.md` (28 entries); session log: `.squad/log/2026-06-01T100000Z-curriculum-v2-build.md`.

### 2026-06-01 — Authored PLAN-V3.md (3-tier tree + de-guided Advanced + MAF Capstone)
- New planning doc `PLAN-V3.md` at repo root — **extends** PLAN-V2, does not overwrite it. Supersedes only
  PLAN-V2's "two-tier" framing (§1.1a, §3); Foundations spine + two-paths + STEP template + `.env` contract stay.
- **Tier tree (V3 signature):** Foundations (guided trunk) → Advanced (modular fan, any order) → **Capstone**
  (open-ended summit) + a cross-cutting **"make it your own"** scenario-swap branch. Progression logic =
  **guided → modular → autonomous** (guidance decreases, learner agency increases per tier).
- **De-guiding verdict:** Advanced isn't *too short* — it's **over-guided**, and Action Tools is **mislabeled**
  (1.25 hr → really ~45 min). Fix = **DEPTH not clock-padding**. For each of the 4 advanced activities I specified:
  the thin step (cited), the load-bearing PLACEHOLDERs to remove, a **build-from-scratch path**, 1–2 real stretch
  goals, and **dual honest times** (guided vs scratch). Eval is the meaty one (keep 1.25 hr); the other three paste
  full code in the README (Tracing `trace_setup.py`, Deploy `agent.yaml`/`Dockerfile`) → convert copy-paste to author.
- **Capstone (headline):** single Northfield IQ agent → **multi-agent MAF team**: Triage/Router → Knowledge +
  Action specialists (fan-out) → Synthesizer (fan-in), typed Pydantic contracts (no regex), **DevUI visual-first
  then traced**. Taught as **design brief + acceptance criteria**, NOT placeholders. Magentic manager = stretch;
  Hosted Long-Running (ex-Extra D) = deploy variant. Reuses Foundations KB agent + Action Tools approval loop.
- **Backlog (11 ideas mined from both repos):** build-the-MCP-server, RAG/AI-Search deepening, UI re-slot (free),
  **lab-generator meta-agent** [FWH], APIM-as-MCP, hybrid rule+AI [ATA], cleanup/cost-hygiene [FWH], Connected
  Agents, toolbox assembly, structured-output lab, facilitator guides. Each tagged source/teaches/tier/effort.
- **Lessons / gotchas captured:**
  - The ATA **"provide-API + single-PLACEHOLDER"** pattern is great for calibration but **caps difficulty** — it's
    exactly what makes our Advanced tier feel thin. The cure is a **dual-path** (guided keeps the scaffold; scratch
    removes it) graded by the SAME `validate.py` behavioral contract, so we don't double-author the grader.
  - "Feels short" ≠ "is short": measure **real authoring minutes**, not page count. Pasted-code steps inflate the
    label. Action Tools Step 1 is a *verbal* step (no script) — pure reading, counts as ~0 work.
  - Capstone must stay **low-guidance on purpose** — the design IS the learning. Resisted the urge to ship a
    placeholder file; gave the org-chart sketch + two `WorkflowBuilder` snippets + acceptance criteria only.
  - Keep the `.env.sample` contract **byte-for-byte**; capstone/backlog reuse existing vars only — any new var goes
    through Livingston's Bicep outputs, never hand-edited (PLAN-V2 rule).
- Decision logged: `.squad/decisions/inbox/danny-plan-v3.md`.

### 2026-06-01 — Curriculum V3 proposed (cross-agent note)
V3 planning is **proposed, not implemented**. `PLAN-V3.md` (Danny) defines the 3-tier tree (Foundations → Advanced → MAF Capstone) and de-guides the Advanced tier (dual guided / build-from-scratch path, same `validate.py`); `CURRICULUM-REASSESSMENT.md` (Rusty) backs the timing verdict + 3-rung ladder. Linus's Foundations step deep-links are staged. No activity folders or `.env.sample` changed; no commit. Decision inbox merged into `.squad/decisions.md` (new "Curriculum V3" section); session log: `.squad/log/2026-06-01T120000Z-curriculum-v3-assessment.md`.

### 2026-06-01 — Authored the Tier 3 Capstone activity (PLAN-V3 §3 IMPLEMENTED)
- **Files shipped (staged, not committed):**
  - `activities/capstone-multi-agent/README.md` — design-brief style, intentionally LOW guidance (no starter
    file, no PLACEHOLDERs). Mirrors the Advanced README house style (banner → objectives → org-chart ASCII →
    two-pass build → visual-first/traced → make-it-your-own → acceptance checklist → Learning Resources → Tips).
  - `activities/capstone-multi-agent/solution.md` — facilitators-only guide (reference org-chart, sequential→fan-out
    evolution, typed Pydantic contracts, DevUI launch, trace check, Magentic + hosted-LR stretch variants,
    reconvene points, failure-mode table, timing, debrief, validate.py contract).
- **Banner format I shipped (for consistency with Rusty's Advanced READMEs):**
  `> **Tier 3 · Capstone — the summit.** ⏱ **Core 2–2.5 hr** · **+1 hr** Magentic · **+1.5 hr** hosted variant.`
  `> ⭐⭐⭐⭐⭐ · **Open-ended design brief — not a placeholder-fill.**` then a Prerequisites blockquote
  (Foundations end-state + Action Tools; Tracing strongly recommended; Deploy only for hosted variant) + the
  bootstrap skip-path line. Matches the §3.8 time/placement and §3.7 guidance-level note.
- **MAF surface notes:** all `WorkflowBuilder`/executor/Magentic snippets are marked **illustrative — confirm
  current MAF surface via microsoft-docs MCP** (Search-Before-Implement). Did NOT hardcode class names as fact.
  Pointed to the `foundry-workflows` skill stub. The two `WorkflowBuilder` snippets are verbatim from §3.4
  (sequential: triage→knowledge→synthesizer; fan-out: triage→{knowledge,action}→synthesizer fan-in).
- **Reuse-not-rebuild framing encoded:** Knowledge = Foundations KB agent; Action = Action Tools agent + approval
  loop; Triage/Escalation/Synthesizer = new small tool-less reasoners.
- **Env discipline:** README "invent nothing" table lists ONLY existing `.env.sample` vars
  (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_FOUNDRY_AGENT_NAME`, `AZURE_SEARCH_*`,
  `AZURE_SEARCH_INDEX_NAME=university-faq`, `ACTION_API_URL/MCP_URL/API_KEY`, `server_label=northfield_actions`,
  `APPLICATIONINSIGHTS_CONNECTION_STRING`, the two trace flags). Hosted-variant additions → Livingston via Bicep,
  never hand-edited into `.env.sample`.
- **validate.py is Basher's** (not authored here). README + solution both point at a *forthcoming* `validate.py`
  for the **structural subset only**. Expected PASS string I documented for Basher to match:
  `✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use`.
- **EXACT acceptance-criteria checklist I shipped (verbatim from §3.7 — Basher align validate.py to the first
  three / structural ones):**
  1. ≥ 3 agents with distinct roles, ≥1 router/triage that *decides* routing + ≥2 specialists. *(structural)*
  2. Workflow runs BOTH a sequential AND a parallel fan-out topology (show both graphs). *(structural: fan-out edge)*
  3. Typed Pydantic contracts flow between agents — no free-text regex parsing between hops. *(structural)*
  4. ≥1 specialist reuses the Foundations KB (grounded, cited) and one reuses the Action Tools approval loop (governed). *(live)*
  5. Run is visualized in DevUI AND traced end-to-end (multi-agent span tree by `operation_Id`). *(live)*
  6. A 2-minute demo narrates one question's journey through the team. *(live)*
  7. (Stretch/deploy variant) workflow is hosted with a background/long-running run that completes after the tab is closed. *(live)*
- **PLAN-V2 reconciliation (§5.3) done:** added a top-of-file `➡️ Superseded in part by PLAN-V3.md` pointer, and
  marked §1.1a ("two-tier model (LOCKED)") + §3 ("Curriculum Structure — Two Tiers") as **superseded by PLAN-V3
  §1 (three-tier)** with brief notes. Did NOT touch the Foundations spine, §1.5 two-paths, §1.6 STEP template, or
  §2 migration KEEP/CUT/REWRITE.
- Did NOT edit root `README.md` or `docs/` (Linus) or the Advanced READMEs (Rusty). No git commit.
- Decision logged: `.squad/decisions/inbox/danny-capstone-built.md`.

### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** to disk (staged, not committed): Tier 3 MAF Capstone **live**
(README + solution + Basher `validate.py`); 4 Advanced READMEs **de-guided** to the 3-rung ladder
(Rusty); `scripts/cleanup.sh` + lab-generator shipped (Livingston); root `README.md` + `docs/`
migrated to **three-tier** (Linus). Inbox merged into `.squad/decisions.md` ("Curriculum V3 —
Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
