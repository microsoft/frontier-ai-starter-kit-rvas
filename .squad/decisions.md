# Squad Decisions

**Last Updated:** 2026-06-01 (merged inbox: +1 entry — Linus docs UI refresh + markdown normalization policy)

---

## Content Architecture & Direction

### User Directive — Prompt Flow is Deprecated (CUT)
**Author:** Marco Olivo (via Copilot / Coordinator)  
**Date:** 2026-06-01  
**Status:** Directive (binding)

**Decision:** Drop Prompt Flow from the curriculum entirely. It is deprecated and no longer the recommended path.

**Implications:**
- Challenge 03 (Prompt Flow Orchestration) is replaced/removed.
- Any RAG/evaluation steps that depended on Prompt Flow are re-architected onto current Foundry primitives (Agents, AI Search, Foundry IQ, MCP, Agent Framework / MAF).
- `promptflow*` dependencies and the Prompt Flow VS Code extension come out of the devcontainer.

---

### Curriculum V2 — Agent-Era Rearchitecture
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Superseded — reorganized into the **Two-Tier** model (see "Curriculum V2 — Two-Tier Implementation (BUILT)" below). The linear 00–07 core spine became Tier 1 Foundations (4 ordered steps) + Tier 2 modular Advanced/Extras; everything else here still holds.  
**Artifact:** `PLAN-V2.md` (revised in place), `RESTRUCTURE-SPEC.md` (new)

**Context:** Re-architect the 7-challenge v1 curriculum around current Foundry primitives, honoring the directive to remove Prompt Flow. Informed by research on microsoft/FrontierWeekHack, microsoft/azure-trust-agents, and microsoft/skills.

**Key decisions:**
1. **One-artifact-many-acts narrative** (from azure-trust-agents): a single evolving artifact — the Northfield University "IQ" Assistant — grows from a Playground prompt into a deployed, grounded, action-taking, observable agent. Preserves the existing Northfield FAQ corpus.
2. **Prompt Flow is CUT** (honors directive). Old Ch03 removed; dependent RAG/eval steps re-expressed as Agents + AI Search + Foundry IQ + MCP + MAF.
3. **New core spine (00–07):** 00 Setup & Provisioning (Foundry + AI Search) · 01 Model Selection & Playground · 02 Your First Agent · 03 Knowledge Base (Index + Foundry IQ via MCP) · 04 Action Tools (MCP that does work) · 05 Evaluation & Red Teaming · 06 Tracing & Observability · 07 Deploy as Hosted Agent.
4. **Every user E2E bullet is mapped** to a specific challenge; nothing dropped.
5. **Headline new content** = a real knowledge-base build (Ch03) and a real evaluation + red-teaming challenge (Ch05), both absent from the reference repos.
6. **Extras (optional, self-contained):** A Fabric IQ · B Voice Live · C Magentic Workflows (MAF) · D MAF + Hosted Long-Running Agents · E Build a UI · F Copilot-Assisted Build (microsoft/skills).
7. **Copilot enablement is a cross-cutting layer:** ship a selective subset of microsoft/skills Foundry skills + the 3-server `.mcp.json` (azure, foundry-mcp, microsoft-docs) + `copilot-instructions.md` into the student Codespace (pinned commit). Coaches load the full set to validate solutions.
8. **Provisioning golden path = `azd up` + Bicep** (Bash `deploy.sh` fallback), replacing v1's ad-hoc script.
9. **Format:** default 2-day (core 00–07 + Extras C and E); 1-day core (00–06) and demo-day (00–04 + Voice + UI) variants documented.

**Open items to validate before event:** preview-feature churn (Foundry IQ/Toolboxes/hosted agents), `foundry-mcp` reachability from Codespaces, `azd ai agent` availability in sandbox subs, model/region/quota, red-team tooling maturity, Fabric capacity cost, Voice Live access, APIM "Expose as MCP" preview.

**Top backlog (full list in PLAN-V2 §8):** (1) azd+Bicep infra — Livingston; (2) strip Prompt Flow — Livingston/Danny; (3) author Ch03 Knowledge Base — Rusty/Danny; (4) author Ch04 Action Tools + backend — Rusty/Livingston; (5) author Ch05 Eval + Red Team — Basher/Rusty.

---

## Curriculum V2 — Two-Tier Implementation (BUILT)

The V2 curriculum was implemented to disk this batch (staged, NOT committed). The 10 author decision records below are merged and deduplicated from the decision inbox.

### Directive — Two-Tier Structure + Bootstrap Skip-Path
**Author:** Marco Olivo (via Copilot / Coordinator)  
**Date:** 2026-06-01  
**Status:** Directive (binding)

**Decision:** Restructure the curriculum into TWO tiers:
1. **Tier 1 — Foundations** (the "Basic" challenge): ONE guided, linear challenge broken into ordered STEPS (Setup → Model/Playground → First Agent → Knowledge Base/IQ). Everyone completes it. End-state = a deployed, grounded agent.
2. **Tier 2 — Advanced challenges:** modular, self-contained, pickable in any order, each with numbered steps + success criteria, all assuming the Foundations end-state.

**Also:** single **bootstrap skip-path** (`azd up` + setup-foundations, ~10–15 min) materializes the Foundations end-state for advanced teams (gated "recommended only if your team already knows Foundry basics"); ONE shared checkpoint suffices; every unit uses a standard STEP template (Goal → Tasks → Success Criteria → Checkpoint); the `docs/` site mirrors this exactly; **Prompt Flow removed** everywhere (reaffirmed).

---

### Two-Tier Spec LOCKED — PLAN-V2 + RESTRUCTURE-SPEC
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Locked (implements Marco's binding directive)  
**Artifacts:** `PLAN-V2.md` (revised in place), `RESTRUCTURE-SPEC.md` (new)

**Decision:** Formalized the two-tier model. **Tier 1 Foundations** = 4 ordered steps (1 Setup & Provisioning · 2 Model Selection & the Playground · 3 Your First Agent · 4 Knowledge Base — Index + Foundry IQ); end-state = a deployed, grounded Northfield IQ Assistant. **Tier 2** = modular Advanced (Action Tools, Evaluation & Red Teaming, Tracing & Observability, Deploy as a Hosted Agent) + Extras (Fabric IQ, Voice Live, Magentic/MAF, Hosted Long-Running, Build a UI, Copilot-Assisted). Bootstrap skip-path = `azd up` + `scripts/setup-foundations.sh`, verified by the single `validate-foundations.py` checkpoint. Standard STEP template skeleton lives in `RESTRUCTURE-SPEC.md` §3.

**Old → New folder map:** `challenge-00-setup`→`foundations/` (Step 1); `challenge-01/02/04` harvested→`foundations/` Steps 2–4 then `git rm`; `challenge-03-prompt-flow` **DELETED** (no migration); `challenge-05-evaluation`→`advanced-evaluation-redteam/`; `challenge-06-deploy`→`advanced-deploy-hosted-agent/`; new `advanced-action-tools/`, `advanced-tracing-observability/`, and 6 `extra-*` folders. `docs/challenges/` mirrors 1:1 with coach siblings.

---

### Folder Restructure Executed + Prompt Flow Removed (non-content)
**Author:** Livingston (DevOps & GitHub Engineer)  
**Date:** 2026-06-01  
**Status:** Complete (staged on disk; NOT committed)

**Decision:** Mechanical restructure only. `git mv` for the three renames (history preserved); `git rm` for `challenge-03-prompt-flow/` + its two docs pages; harvest-before-remove for Ch01/02/04 (left in place for Rusty, removed in the content move). Created 8 placeholder challenge folders. Prompt Flow pulled from non-content files: `requirements.txt` (removed `promptflow*`, added `azure-ai-agents`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`); `.devcontainer/devcontainer.json` (removed `ms-toolsai.promptflow`); broken `challenge-03` nav rows in docs. Remaining PF prose flagged for content authors (Rusty/Linus/Basher).

---

### Foundations Challenge Authored (Tier 1, Steps 1–4)
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-06-01  
**Status:** Complete  
**Artifacts:** `challenges/foundations/README.md` + `solution.md`

**Decision:** Authored the Tier 1 Foundations challenge as ONE guided linear challenge, four steps to the §3 STEP template. Step 1 `azd up` provisioning + keyless auth; Step 2 deploy/compare two models + tune system instructions + reproduce via `openai.responses.create()`; Step 3 promote to a named, versioned agent (`agents.create_version(PromptAgentDefinition(...))`); Step 4 (END-STATE) index `university-faq` → Foundry IQ knowledge base (`VECTOR_SEMANTIC_HYBRID`) → grounded answers **with citations**. Harvested-then-removed v1 `challenge-01/02/04`. Authored to the `validate.py --step 1|2|3|4|--all` checkpoint contract (Basher implements). No answer leakage in README.

---

### Advanced — Tracing & Observability + Deploy as a Hosted Agent
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Complete (content; QA validators by Basher)

**Decision:** Authored two Advanced challenges, each self-contained, assuming the Foundations end-state, opening with the §3.2 Tier-2 banner + bootstrap skip-path. **Tracing & Observability (4 steps):** OTel GenAI instrumentation (set-env-before-import gotcha) → emit spans → inspect span tree in portal Tracing tab → correlate end-to-end with KQL by `operation_Id` (`correlate.kql`). **Deploy as a Hosted Agent (4 steps):** re-targeted off Prompt-Flow/managed-online-endpoint to a hosted Foundry agent via `azd ai agent` — author `agent.yaml` (responses protocol, port 8088) + MAF entrypoint + Dockerfile → `az acr build` + `azd ai agent create/deploy` → invoke live Responses endpoint with per-agent managed identity (401/403 anon) → tie monitoring back to Tracing. Remaining PF mentions are deliberate "this was removed" guardrails.

---

### Advanced — Evaluation & Red Teaming + Action Tools
**Author:** Basher (QA / Coach Enablement / DevRel)  
**Date:** 2026-06-01  
**Status:** Complete

**Decision:** Authored two Tier-2 Advanced challenges. **Evaluation & Red Teaming (5 steps):** portal quality metrics → code-driven `evaluate.py` (built-in Groundedness/Relevance/Coherence/Fluency + custom `NorthfieldDomainEvaluator`, `--gate FLOAT` CI gate) → custom domain evaluator → red teaming (jailbreak / harmful-content / indirect-prompt-injection) → CI score gate. Assets: `northfield-eval.jsonl` (36 grounded rows, 13 topics) + `adversarial-seed.jsonl` (10 labeled attacks, 4 categories, 3 prompt-injection-via-document rows). **Action Tools:** wiring challenge against Livingston's provided backend (`scripts/action-backend/`) — start backend → knowledge-vs-action → attach `McpTool` → `RequiredMcpToolCall → ToolApproval → SubmitToolApprovalAction` approval loop → e2e action + denial path. Reference impls live only in `solution.md`.

---

### Five Extra Challenges Authored
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Complete (staged on disk; NOT committed)

**Decision:** Filled all 10 placeholder files (5 README + 5 solution) for Extras A/B/C/D/F to the §3.2 Tier-2 banner + STEP template. `extra-build-ui/` intentionally left to Linus. Per-Extra prereq + infra/wow-factor callout. **Only Magentic gets a programmatic `validate.py`** (steps headless-checkable); the other four use portal/live-state checkpoints by design (live data / audio / async runs / Copilot behavior) with a "Why no validate.py" section each. Env contract used verbatim from Livingston's infra. Search-Before-Implement enforced — preview surfaces (Fabric tool class, `azure-ai-voicelive`, MAF Magentic builder, `azd ai agent` background-run) never hard-coded. **Coach infra gates flagged:** Fabric F-SKU + OneLake lakehouse (pause capacity after session); Voice Live regional access + mic/headset; Hosted-LR `ACTION_MCP_URL=localhost` won't resolve from a container; Copilot-Assisted needs Copilot licenses + http MCP reachability.

---

### Infra + Automation Scaffolding (azd/Bicep, bootstrap, action backend, Copilot layer)
**Author:** Livingston (DevOps & GitHub Engineer)  
**Date:** 2026-06-01  
**Status:** Complete (staged on disk; NOT committed)

**Decision:** Built the V2 infra and automation. **azd + Bicep golden path:** `azure.yaml`, `infra/main.bicep` (subscription scope, outputs the `.env` contract), `infra/resources.bicep` (Foundry `AIServices` + project + model deployment + AI Search + Log Analytics/App Insights + ACR + keyless RBAC), `infra/main.parameters.json`; `scripts/deploy.sh` Bash fallback for quota/region edge cases. **Bootstrap skip-path (Path B):** `scripts/setup-foundations.sh` (real index build + graceful-degrade KB/agent) + `scripts/validate-foundations.py` (single checkpoint: `.env` + index populated + agent exists + grounded answer with citation). **Action backend (provided, teams wire it):** `scripts/action-backend/app.py` (FastAPI, 3 actions) + `mcp_server.py` (FastMCP over streamable-http). **Copilot enablement layer:** `.vscode/mcp.json` (azure / foundry-mcp / microsoft-docs), `.github/copilot-instructions.md` (Search-Before-Implement), 7 `.github/skills/*/SKILL.md` stubs. Keyless-first throughout; `az bicep build` + `bash -n` + `py_compile` all pass.

**Action Tools env contract (AUTHORITATIVE):** `ACTION_API_URL`=`http://localhost:8080`, `ACTION_MCP_URL`=`http://localhost:8765/mcp`, `ACTION_API_KEY`=*(empty)*; `server_label`=`northfield_actions`; MCP tools `create_it_ticket`, `place_course_hold`, `book_advising_slot`. Aligned across `.env.sample`, `scripts/deploy.sh`, `scripts/action-backend/`, and the Action Tools challenge. Basher's eval/action records confirm the same names — **no conflict**.

**Full `.env` contract** emitted by Bicep outputs → `.env.sample`: Azure context, Foundry (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_FOUNDRY_AGENT_NAME`, …), Search (`AZURE_SEARCH_*`, `AZURE_SEARCH_INDEX_NAME=university-faq`), Observability (`APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`), ACR, Action Tools.

---

### ENV Var Reconcile + validate.py Checkpoints + Prompt Flow Grep Sign-off
**Author:** Basher (QA / Coach Enablement / DevRel)  
**Date:** 2026-06-01  
**Status:** Complete

**Decision:** Reconciled all of `challenges/` to the authoritative `.env.sample` contract — renamed 6 legacy env families (`FOUNDRY_PROJECT_ENDPOINT`→`AZURE_AI_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`/bare `MODEL_DEPLOYMENT_NAME`/`AZURE_OPENAI_DEPLOYMENT`→`AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FOUNDRY_AGENT_NAME`/`NORTHFIELD_AGENT_ID`→`AZURE_FOUNDRY_AGENT_NAME`), 46 tokens total; `scripts/` deliberately untouched (internal shell locals). Implemented 3 new + 1 patched `validate.py` (foundations, tracing-observability, deploy-hosted-agent; action-tools `--dry-run`) — all support `--step N`/`--all`/`--dry-run`, every Azure call guarded, `py_compile` PASS on all 7 Python files. **Prompt Flow grep sweep:** `challenges/` CLEAN (only deliberate guardrails remain); `requirements.txt:18` guardrail comment KEEP; `resources/QA-REPORT.md:39` left as-is (point-in-time QA record); docs/ hits handed to Linus.

---

### docs/ Restructured to Mirror Challenges 1:1 (Two-Tier + Two-Paths)
**Author:** Linus (Frontend Dev / Docs)  
**Date:** 2026-06-01  
**Status:** Complete (staged on disk; NOT committed)

**Decision:** The Jekyll site now mirrors final `challenges/` content 1:1. Created 24 mirror pages (`foundations` + 4 Advanced + 6 Extras, each + `-coach`); deleted 12 stale `challenge-00/01/02/04/05/06` pages; rewrote `docs/challenges/index.md` to Two-Tier + Two-Paths (Path A beginner linear; Path B advanced-skip bootstrap, PLAN-V2 §1.5 ASCII diagram), `docs/index.md` away from "seven challenges", and `docs/coach-hub.md` (PF removed, 11 coach links). A one-shot `scripts/_mirror_docs.py` (deleted after run) generated mirrors for true fidelity; link rewrites bake into the generator (`solution.md`→`-coach`, repo links→absolute GitHub blob/tree on `olivomarco/ai-hackathon@main`). nav_order: foundations 1, Advanced 10–13, Extras 20–25, coach = student+100 + `nav_exclude`. Verified: docs/ PF-clean (only deliberate notes), no stale `challenge-0N` links, 0 frontmatter problems. Caveat: full `jekyll build` runs in Pages CI (no local gems).
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-05-28T16:15:34.722+01:00  
**Status:** Proposed

**Context:** Framework for the WTH AI Hackathon built on Azure AI Foundry, targeting university students/early professionals.

**Decisions:**
- **Challenge Structure:** 7 challenges (00–06), linear dependency chain. Challenge 00 is setup-only (no AI content).
- **Progression:** Setup → Model Deployment → Prompt Engineering → Prompt Flow → RAG → Evaluation → Deploy
- **Evaluation before Deployment:** Embeds responsible AI practices
- **Repo Layout:** `challenges/challenge-NN-slug/` at root with paired `README.md` (student) + `solution.md` (coach)
- **Docs:** `docs/` for GitHub Pages (Jekyll, `just-the-docs` theme)

---

### Challenge Content Decisions — Rusty (Wave 1: Ch 00–02)
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Proposed

**Achievements:**
- Created student-facing challenge guides for Challenges 00–02 + coach solution guides
- Fictional university FAQ corpus (Northfield University) for RAG challenges
- All content aligned to WTH template: Introduction, Description, Success Criteria, Learning Resources, Tips, Advanced
- Coach guides optimized for facilitation (timing, pitfalls, coaching questions), not answer leakage
- Consistent Azure AI Foundry concepts across first three challenges

**Consequences:** Early scaffold reduces coach load; Northfield theme creates continuity into later challenges; corpus favors consistency over creativity.

---

### Challenge Content Decisions — Rusty (Wave 2: Ch 03–06)
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Complete

**Achievements:**
- Completed student-facing `README.md` and coach-facing `solution.md` for Challenges 03–06
- Maintained University Q&A Assistant narrative across prompt flow, RAG, evaluation, deployment
- Aligned guides to WTH pattern; coach guides follow 00–02 facilitation template
- **Ch 03:** Framed Prompt Flow around classification → routing → formatting (orchestration without complexity)
- **Ch 04:** Centered on Northfield FAQ; emphasized RAG vs non-RAG comparison
- **Ch 05:** Emphasized measurable improvement loops; paired quality evaluation with content safety testing
- **Ch 06:** Success = endpoint + simple Flask integration (demo-ready, approachable)

---

### README.md Writing Decisions — Danny
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Complete

**Decisions:**
1. **Structure & Tone:** Welcoming, action-oriented throughout (signals "achievable")
2. **Badge Selection:** GitHub Pages build status, MIT License, GitHub Codespaces
   - Pages badge signals deployment pipeline readiness
   - License badge builds trust
   - Codespaces badge is direct CTA for engagement

---

### Participant-Facing Challenge Guide Pattern — Linus (Wave 2)
**Author:** Linus (Frontend Dev)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Proposed

**Context:** Transform seven `docs/challenges/` placeholder pages into participant discovery layer.

**Content Pattern (all seven pages):**
- Short plain-language overview
- Time and difficulty badges
- "What participants will build" cards
- Key concepts callout
- Official learning links
- Direct repo README link
- Previous/next pager

**Rationale:** Fast scanning during event; discovery layer (not full instructions).

---

## Frontend & Pages Rendering

### GitHub Pages Information Architecture — Linus
**Author:** Linus (Frontend Dev)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Proposed

**Context:** Student-friendly GitHub Pages experience in `docs/` using Jekyll and `just-the-docs`.

**Site Structure:**
- Use `docs/` as full Jekyll site root
- Five top-level pages: Home, Getting Started, Challenges, Coach Hub, FAQ
- Seven challenge placeholder pages for sidebar navigation

**Theme & UX:**
- Use `just-the-docs` for search, responsive sidebar, low-friction deployment
- Azure-aligned visual treatment: custom hero, bright links, difficulty badges, lightweight callouts
- Plain-language, event-day friendly for laptops/tablets

---

### GitHub Pages Theme Rendering Fix — Linus
**Author:** Linus (Frontend Developer)  
**Date:** 2026-05-28  
**Status:** Completed & Deployed

**Root Cause:** Two compounding issues broke live site rendering:

1. **Missing master stylesheet:** `docs/assets/css/just-the-docs-default.scss` did not exist. Without this file (empty front-matter), Jekyll has no entry point to compile JTD theme CSS. Theme's `_layouts/default.html` references compiled file; without it, no stylesheet injected.

2. **Missing `jekyll-include-cache` plugin:** JTD uses `{% include_cached %}` in layout partials. Without plugin, includes silently fail, breaking layout entirely.

**Secondary Issues (after CSS fixed):**
- Wrong `url` in `_config.yml`
- Wrong repo links

**Files Changed:**
- Created: `docs/assets/css/just-the-docs-default.scss` (with empty front-matter)
- Updated: `_config.yml` (added plugin, fixed URLs)
- Fixed URLs: `microsoft/ai-hackathon` → `olivomarco/ai-hackathon`

**Impact:** CSS rendering restored; Pages site now displays with full theme. Marco must `git push` for deployment.

---

## Infrastructure & DevOps

### WTH Hackathon Repo Infrastructure Bootstrap — Livingston
**Author:** Livingston (DevOps & GitHub Engineer)  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Proposed

**Context:** Baseline delivery infrastructure for organizers to run event consistently in Codespaces/devcontainers and publish docs.

**Decisions:**
- Create canonical challenge, docs, resources directory structure upfront
- Standardize on Python 3.11 devcontainer with Azure CLI, Node.js 20, GitHub CLI
- Repo-root `requirements.txt` + post-create bootstrap script for deterministic Codespaces setup
- Organizer automation: explicit idempotency checks before creating resource group, AI Foundry hub/project, Azure OpenAI deployment, Azure AI Search service
- Publish docs through dedicated GitHub Pages workflow (Jekyll 4.x, `just-the-docs`)
- Add contributor hygiene: `.gitignore`, issue templates, PR template, MIT license

**Consequences:**
- Organizers can fork and bootstrap infrastructure with fewer manual steps
- Provisioning script may need updates if Azure CLI preview commands change

---

### Version Audit — Livingston
**Author:** Livingston (DevOps & GitHub Engineer)  
**Date:** 2026-05-28  
**Status:** Completed

**Microsoft Foundry Rebrand Applied:**
- `requirements.txt`: All Python deps bumped to current stable
- `.devcontainer/devcontainer.json`: Node.js `20` → `22` (current active LTS)
- `.github/workflows/deploy-pages.yml`: 4 Action versions bumped
- `docs/Gemfile`: `jekyll ~> 4.3` → `~> 4.4`; `just-the-docs ~> 0.8` → `~> 0.10`
- `docs/Gemfile.lock`: Not regenerated (requires `bundle install` in Ruby environment)

**Action Items for Maintainers:**
- After pulling these changes, run: `cd docs && bundle install` to regenerate Gemfile.lock

---

## QA, Audits & Humanization

### Content Audit — Challenges 00–03 — Rusty
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-05-28  
**Verified Against:** Microsoft Foundry docs + Livingston's version audit

**Ch 00 Fixes:**
- `solution.md` timing: "creating the hub/project" → "creating the Foundry project"
- `docs/challenge-00.md` hero: "Azure AI Foundry, Hub and Project" → "Microsoft Foundry, Foundry resource and project"
- Portal URLs confirmed valid (`ai.azure.com`)
- Project endpoint format confirmed (`https://<resource>.services.ai.azure.com/api/projects/<project>`)

**Ch 01–03:** All claims against SDK 2.x, Microsoft Foundry terminology, and gpt-4.1-mini verified; no breaking changes detected.

---

### Content Audit — Challenges 04–06 — Basher
**Author:** Basher (DevRel / Coach Materials)  
**Date:** 2026-05-28  
**Verified Against:** Azure AI Search 12.x SDK docs, azure-ai-evaluation 1.16.9, Microsoft Foundry deploy-models docs

**Ch 04 (RAG: Grounding with Data):**
- "Azure AI Foundry" → "Microsoft Foundry" (rebrand)
- Learning resources link text updated
- URLs `learn.microsoft.com/azure/ai-foundry/` confirmed valid
- No SDK code in challenge README; no direct SDK snippets needed

**Ch 05–06:** All URLs, SDK references, and terminology verified against current docs. Deployment patterns confirmed compatible with Microsoft Foundry.

**Additional Sweep:** Repo-wide URL fix (`pages.yml` → `deploy-pages.yml` in README badge).

---

### QA Review — Basher
**Author:** Basher  
**Date:** 2026-05-28T16:23:27.374+01:00  
**Status:** Completed

**Scope:** Full QA sweep across student guides, coach guides, docs pages, infra files.

**Findings:**
- 14 issue groups identified
- 11 issue groups fixed directly
- 3 issue groups left as follow-up (for Rusty/Linus judgment)

**Fixes Applied:**
- Added missing "Step-by-step" sections to Challenges 00–02
- Removed broken screenshot links from Challenge 00 setup guidance
- Aligned `requirements.txt`, `.env.example`, `validate-environment.py` with code snippets and Ch 06 endpoint variables
- Standardized coach guide headings across `solution.md` files
- Updated outdated Azure AI Foundry / setup / coach hub / resources links
- Reinforced University Q&A Assistant narrative across docs challenge pages 03–06

---

### Cross-Page Link Fix — Basher
**Author:** Basher  
**Date:** 2026-05-28  
**Status:** Completed & Committed (8d321da)

**Problem:** Seven `docs/challenges/challenge-XX.md` pages ended with Markdown links:
```
../../challenges/challenge-XX-name/README.md
```
Jekyll Pages site rooted at `docs/`; `../../` traversal exits published tree → **404** on live site.

**Solution:** Updated all seven links to GitHub repo URLs:
```
https://github.com/olivomarco/ai-hackathon/tree/main/challenges/challenge-XX-name/README.md
```
Pages now render correctly; no 404s on challenge discovery layer.

---

### Hero Panel Secondary Button Contrast Fix — Linus
**Author:** Linus (Site/Chrome)  
**Date:** 2026-05-28  
**Status:** Completed

**Root Cause:** `.hero-panel` sets `color: #fff`, which cascades to plain `.btn` children; JTD's `.btn` defaults to a near-white background → invisible white-on-white secondary CTAs (`docs/index.md` lines 13, 67).

**Solution (two-layer):**
- **CSS:** `docs/_sass/custom/custom.scss` — scoped `.hero-panel .btn:not(.btn-primary):not(.btn-purple)` rule with `color: #1f2937`, `background: rgba(255,255,255,0.92)`, plus hover enhancement.
- **Markup:** `docs/index.md` — added `btn-outline` class to both secondary buttons.

**Forward Guidance (new rule):** ALL secondary/plain `.btn` elements inside a `.hero-panel` MUST use the `btn-outline` class for readability and consistent secondary-CTA UX.

---

### Kramdown `markdown="1"` Attribute on HTML Block Elements — Linus
**Author:** Linus (Site/Chrome)  
**Date:** 2026-05-28  
**Status:** Completed

**Bug:** Jekyll Kramdown does not process markdown (tables, lists, links, emphasis) inside HTML block-level elements unless the wrapper carries `markdown="1"`. The Coach Hub coach-notes table rendered as raw pipe characters.

**Fix:** Added `markdown="1"` to 4 divs — `docs/coach-hub.md:80` (challenge-card wrapping a table) and `docs/setup.md` lines 31, 57, 98 (callout-tip / callout-warning / callout-info).

**Style Rule (new, mandatory):** Every `<div class="callout-*">` or `<div class="challenge-card">` that wraps markdown body content MUST include `markdown="1"`. Exceptions (raw HTML/CSS only, no attribute): `hero-panel`, `quick-grid`, `quick-card`, `meta-strip`, `cta-row`, `table-wrapper`, `page-nav`.

---

### Humanizer Editorial Pass — Rusty
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-05-28  
**Status:** Completed & Committed (80b1f98)  
**Scope:** 28 content files

**Pattern Fixes:**
- **Decorative emojis:** Removed 12 emojis from H1/H2/H3 headers (🤖, 🎯, 👥, 👨‍🎓, etc.)
- **Em dash overuse:** Fixed 9 em dashes → appropriate punctuation (commas, colons, periods)
- **Promotional vocabulary:** Stripped branded adjectives from headings
- **Rule-of-three patterns:** Reduced repetitive list structures
- **Passive voice:** Converted some passages to active voice

**Outcome:** Content sounds more editorial, less AI-generated; retained substance without sacrificing clarity.

---

## Curriculum V3 — Three-Tier Assessment & Plan (PROPOSED)

### PLAN-V3 — 3-Tier Tree, De-Guided Advanced, MAF Capstone — Danny
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Proposed (planning artifact — `PLAN-V3.md` at repo root; no challenge content edited)  
**Artifact:** `PLAN-V3.md`  
**Supersedes:** PLAN-V2 "two-tier" framing only (§1.1a, §3). Foundations spine, two-paths (§1.5), STEP template (§1.6), and the `.env` contract remain authoritative.

**Decision 1 — Adopt the 3-tier tree.** Curriculum becomes a tree, not a two-tier list:
- **Tier 1 Foundations** — guided, linear trunk (4 steps; everyone). High guidance.
- **Tier 2 Advanced** — modular fan, pick any order (Action Tools, Eval+RedTeam, Tracing, Deploy). Medium guidance.
- **Tier 3 Capstone** — open-ended summit: compose everything into a multi-agent MAF system. Low guidance.
- **Cross-cutting "make it your own"** branch — reskin the tree to any domain (Copilot lab-generator), applies at every tier.
Progression logic = guided → modular → autonomous. The open-ended capstone is V3's signature (absent from FrontierWeekHack and azure-trust-agents).

**Decision 2 — De-guide the Advanced tier (depth, not clock-padding).** Advanced is over-guided, not too short:
- **Action Tools** — mislabeled: 1.25 hr → ~45 min guided. Remove loop skeleton + breadcrumb PLACEHOLDERs; offer no-starter build; stretch = build the MCP server.
- **Evaluation & Red Teaming** — the meaty one; keep 1.25 hr. Make automated `RedTeam` run mandatory; require 2 custom rules. Stretch = real GitHub Actions CI gate.
- **Tracing & Observability** — stop pasting full `trace_setup.py`/`traced_run.py`; learner authors from a checklist + set-env-before-import gotcha. 1 hr holds once de-guided.
- **Deploy as a Hosted Agent** — stop pasting full `agent.yaml`/`Dockerfile`; difficulty is operational (async `status==active`, `--source-acr-auth-id`, two-identity auth), legitimately ⭐⭐⭐⭐⭐.
- **Dual path per challenge:** guided (keep scaffold) and build-from-scratch (remove it), graded by the same `validate.py` behavioral contract.
- Revised totals: ~4 hr guided / ~6.5 hr build-from-scratch for the four Advanced challenges.

**Decision 3 — New Tier 3 Capstone via MAF (the headline).** `challenges/capstone-multi-agent/` — single Northfield IQ agent → a team: Triage/Router → Knowledge + Action specialists (parallel fan-out) → Synthesizer (fan-in), with typed Pydantic contracts (no regex prose-parsing), built visual-first in DevUI then traced. MAF primitives (Executors / Edges / Workflows / Events; `WorkflowBuilder` sequential then parallel). Reuses Foundations KB agent + Action Tools approval loop. Taught as a design brief + acceptance criteria, NOT step-by-step placeholders. Magentic manager/planner = stretch; Hosted Long-Running = deploy variant; Build a UI = companion. Time ~2–2.5 hr core, +1 hr Magentic, +1.5 hr hosted variant. Prereqs: Foundations + Action Tools.

**Migration implied (not executed this batch):** README two-tier → three-tier + dual time columns + Capstone row; docs/ add Tier 3 nav + `-coach` mirror; PLAN-V2 §1.1a/§3 marked superseded; `.env.sample` untouched (reuse existing vars; new vars via Livingston Bicep outputs); new files implied (capstone README/solution/validate.py, `lab-generator.agent.md`, `scripts/cleanup.sh`, build-from-scratch sidebars).

**Backlog (11 ideas):** build-the-MCP-server · RAG/AI-Search deepening · UI re-slot · lab-generator meta-agent [FWH] · APIM-as-MCP · hybrid rule+AI [ATA] · cleanup/cost-hygiene [FWH] · Connected Agents · toolbox assembly · structured-output lab · facilitator guides. Priority: UI re-slot → lab-generator + cleanup → RAG-deepening + toolbox.

---

### Advanced-Tier Curriculum Reassessment — Rusty
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-06-01  
**Status:** Complete — analysis memo feeding Danny's `PLAN-V3.md`  
**Artifact:** `CURRICULUM-REASSESSMENT.md` (repo root) · No challenge content edited.

**Key findings:**
1. **Timing verdict — user is right.** Advanced tier labelled ~4.5 hr; genuine build effort ~1.5–2 hr. Wall-clock is padded by waiting (App Insights 1–3 min ingestion lag, async hosted-agent provisioning) and copy-paste (Tracing + Deploy hand over every line inline; Action Tools fills 2 placeholders; Eval adds 1 rule). Separate "wall-clock" from "hands-on-keyboard effort."
2. **Per-challenge audit:** Action Tools (~50–65 min, clock roughly honest); Eval & Red Teaming (~65–75 min, richest concept/thinnest authoring, clock honest); Tracing (~25 min effort, hour mostly ingestion lag, inflated as a "build"); Deploy (clock optimistic — real ACR build + preview `azd ai agent` + async provisioning = highest failure surface; budget 90 min).
3. **Core proposal — 3-rung difficulty ladder** per Advanced challenge: (a) guided [current], (b) build-from-scratch [strip starter, give API contract + acceptance criteria], (c) stretch [open]. Same `validate.py` grades all three → zero new validators.
4. **Pick-your-scenario [FWH].** Northfield spine is domain-generic; keep the 3-verb tool invariant byte-stable, swap only corpus + tool labels + persona + eval rows. Ship Northfield canonical + realize ONE alt (retail) wired to Extra F as the lab-generator analog.
5. **Top pedagogy borrows missing:** consistent per-challenge time+difficulty banner (2 of 4 Advanced READMEs show no estimate); cleanup/cost-hygiene script + wrapup. Plus DevUI visual-first before tracing, "why this order" narrative, run-individually-then-orchestrated, "why this option" decision tables.

**Recommendations to PLAN-V3:** adopt 3-rung ladder (no new validators); add honest per-challenge banner split "guided ~X / from-scratch ~Y"; document reskin contract + realize one alt domain via Extra F; re-label, don't re-clock; budget Deploy at 90 min.

---

### Deep-link Foundations Step Titles to Heading Anchors — Linus
**Author:** Linus (Frontend Dev / Docs)  
**Date:** 2026-06-01  
**Status:** Implemented (staged)  
**Scope:** `README.md`, `docs/challenges/index.md`, `docs/challenges/foundations.md`

**Context:** Tier 1 Foundations listed Steps 1–4 as plain text while Tier 2 Advanced linked every title. Foundations is a single file (`challenges/foundations/README.md`) whose four steps are `## Step N` headings — correct fix is to deep-link each step title to its heading anchor, not to four separate files.

**Decision:** (1) Wrap each Tier 1 step title in the root README in a relative link to `challenges/foundations/README.md#<anchor>`. (2) Add an `[Open the full Foundations brief →]` one-liner so the folder is reachable. (3) Mirror linking in docs: cross-page anchors in `docs/challenges/index.md` (`foundations#step-...`) and in-page anchors in `docs/challenges/foundations.md`. Frontmatter / `nav_order` untouched.

**Anchor convention (verified, not guessed):** GitHub anchors = lowercase → strip every char outside `[\w \-]` → spaces become hyphens, no hyphen collapsing. Stripped punctuation between spaces yields double/triple hyphens — these are correct:

| Step | Anchor |
|---|---|
| 1 | `step-1--setup--provisioning-foundry--ai-search` |
| 2 | `step-2--model-selection--the-playground` |
| 3 | `step-3--your-first-agent` |
| 4 | `step-4--knowledge-base-index--foundry-iq---foundations-end-state` |

Step 4's heading has two spaces before `*(` and a stripped `*(←`, producing the triple hyphen (`iq---foundations`). Verified via a Python repro of the GitHub slug algorithm against live headings.

**Rule going forward:** in-repo navigation uses relative links only (no `https://github.com/.../blob` URLs); when a multi-step challenge lives in one file, link step titles to heading anchors; always read the real heading text before deriving an anchor — never guess slugs.

---

## Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)

> Two-wave build executing PLAN-V3. All work staged to disk, **not committed**. Supersedes the
> "PROPOSED" section above — PLAN-V3 is now IMPLEMENTED.

### Tier 3 Capstone Built + PLAN-V2 Reconciled — Danny
**Author:** Danny (Lead & Content Architect)  
**Date:** 2026-06-01  
**Status:** Implemented (staged, not committed)

**Created:** `challenges/capstone-multi-agent/README.md` (student-facing **design brief** — intentionally LOW guidance: no starter file, no PLACEHOLDERs; banner + objectives + org-chart ASCII + two-pass build + visual-first/traced + make-it-your-own + acceptance checklist) and `challenges/capstone-multi-agent/solution.md` (coaches-only: reference org-chart, sequential→fan-out evolution, typed Pydantic contracts, DevUI launch, trace check, Magentic + hosted-LR stretch, reconvene points, failure-mode table, timing, debrief, validate.py contract).

**Edited:** `PLAN-V2.md` — top-of-file `➡️ Superseded in part by PLAN-V3.md` pointer; §1.1a two-tier model + §3 marked **superseded by PLAN-V3 §1 (three-tier)**. Foundations spine / two-paths / STEP template / migration KEEP-CUT-REWRITE left intact.

**Validator contract (for Basher):** assert the structural subset of §3.7 only — (1) ≥3 agents with distinct roles (≥1 router/triage + ≥2 specialists), (2) parallel fan-out edge present, (3) typed Pydantic contracts in use. PASS string (verbatim): `✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use`. The KB/Action-Tools-reuse, DevUI, trace, 2-min-demo, hosted-run criteria are coach-confirmed/live — NOT statically asserted. All MAF code marked illustrative (Search-Before-Implement via microsoft-docs MCP). Capstone reuses existing `.env.sample` vars only.

---

### Advanced READMEs De-Guided to 3-Rung Ladder — Rusty
**Author:** Rusty (Curriculum Designer)  
**Date:** 2026-06-01  
**Status:** Implemented (staged, not committed)

**Edited (READMEs only):** all four Advanced challenge READMEs (action-tools, evaluation-redteam, tracing-observability, deploy-hosted-agent) now carry the **3-rung difficulty ladder** + the **same top banner** (`⏱ Guided ~X · 🛠 Build-from-scratch ~Y · ⭐… · Prereqs: Foundations end-state`). No beginner content deleted — existing guided walkthroughs preserved verbatim as **rung (a)**; rung (b) build-from-scratch hands only the API/SDK contract + acceptance criteria; rung (c) stretch expanded. One surgical non-README edit: removed the `tool_approvals = []  # < PLACEHOLDER >` breadcrumb from `advanced-action-tools/agent_with_actions.py`. Same `validate.py` grades all rungs — no validator/`.env`/solution/root-README/docs changes.

**Final dual-time labels (mirror in root README table):** Action Tools ~45 min / ~1.5 hr ⭐⭐⭐ · Evaluation & Red Teaming ~1.25 hr / ~2 hr ⭐⭐⭐⭐ · Tracing & Observability ~1 hr / ~1.5 hr ⭐⭐⭐⭐ · Deploy as a Hosted Agent ~60–90 min / ~1.5 hr ⭐⭐⭐⭐⭐ (Deploy clock reconciles PLAN-V3 §2.5 with REASSESSMENT §5.5 — optimistic, not padded).

---

### Cleanup Script + Lab-Generator Meta-Agent — Livingston
**Author:** Livingston (DevOps / GitHub)  
**Date:** 2026-06-01  
**Status:** Implemented (staged, not committed)

**Created:** `scripts/cleanup.sh` (PLAN-V3 §4 #7 — `.env`-driven, confirmation-gated teardown/cost-hygiene: bare run is a DRY-RUN that changes nothing; destructive cloud teardown requires explicit `--yes` and shows the resource group first; `--local-only` stops local Action Tools processes; `--purge` escalates to `azd down --force --purge`; `set -Eeuo pipefail`, `timeout -k` + `</dev/null` wrap all azd calls). `.github/agents/lab-generator.agent.md` (#4 — Copilot meta-agent that scaffolds a fresh vertical from the reskin contract) + `.github/agents/scenario-template.md` (4-swap-surface skeleton with **NorthPeak Outfitters** retail worked example: `open_support_case` / `place_order_hold` / `schedule_callback`).

**Guarantees:** reuses existing env var NAMES only (never writes `.env`, no new vars); reskin contract bakes in the tool-shape invariant (create-a-ticket / place-a-hold / book-a-slot, 1:1) keeping every `validate.py` byte-reusable; Search-Before-Implement mandated. `.env.sample`, `infra/*.bicep`, root README, docs/, challenge READMEs untouched. `bash -n` clean, `chmod +x` applied, dry-run + `--local-only` exit 0. Hosted-LR variant env var (if needed) goes via Bicep output later — not hand-edited.

---

### Capstone validate.py Authored (Structural Validator) — Basher
**Author:** Basher (QA & Coach Enablement)  
**Date:** 2026-06-01  
**Status:** Implemented (staged, not committed). Compiles cleanly.

**Created:** `challenges/capstone-multi-agent/validate.py` — LIGHT, headless, **stdlib-only** (argparse, ast, pathlib, re) validator for the structural subset of §3.7. Because the Capstone is an open-ended design brief (no starter/PLACEHOLDERs/fixed filenames), it scans every `*.py` under `--path` (default = challenge dir, recursive, self-excluded) and grades by AST + text heuristics. **3 REQUIRED gating checks:** (1) ≥3 agent/executor roles — ≥1 router/triage + ≥2 specialists, (2) parallel fan-out — a node with ≥2 distinct outgoing edges (fan-in reported as hint), (3) typed Pydantic contracts — `BaseModel` subclass AND `send_message`/`yield_output`. PASS banner verbatim per Danny's contract; exit 0 only if all 3 pass.

**CLI:** `--all` / `--step {1|2|3}` / `--list` / `--path` (new). Matches the house `--step`/`--all` mutually-exclusive convention from the Advanced validators; stdlib only (no httpx/azure/pyyaml). **Reconciliation:** the KB-reuse + Action-Tools-reuse criterion (§3.7 #4) is detected by import/reference but printed under an `— advisory (coach-confirmed live, not gating) —` block that never affects exit code — README stays authoritative while the task's detection is still delivered. Verified: `py_compile` PASS; positive fixture → all 3 PASS + advisory ✅✅ + exit 0; empty-dir → Step 1 FAIL + exit 1. No new env vars, no deps.

---

### Root README + docs/ Migrated to Three-Tier Tree — Linus
**Author:** Linus (Frontend Dev / Docs)  
**Date:** 2026-06-01  
**Status:** Implemented (staged, not committed)

**README.md:** two tiers → **three tiers** in intro + `## Challenges` lead-in (verified `two tiers`=0, `three tiers`=2; Northfield "one evolving artifact" narrative preserved); inlined a trimmed PLAN-V3 §1 ASCII tree (trunk → fan → summit); Advanced table → **dual time columns** mirroring Rusty's labels; new **### Tier 3 — Capstone** section after the Advanced table (time 2–2.5 hr core, +1 hr Magentic stretch, +1.5 hr hosted variant; prereqs Foundations + Action Tools) + "make it your own" line, deep-linked to a verified anchor; repo-tree updated; Extras re-slotted.

**docs/:** created `docs/challenges/capstone-multi-agent.md` (+ `-coach` mirror), updated `docs/challenges/index.md` to three-tier, added `docs/challenges/cleanup.md` wrap-up. Depends on Rusty's dual-time labels, Danny's Capstone README, Livingston's `scripts/cleanup.sh`. `nav_order` collisions checked (none).

---

### Internal Planning Docs Archived to `.squad/planning/` — Livingston
**Author:** Livingston (DevOps / GitHub)  
**Date:** 2026-06-01  
**Requested by:** Marco Olivo  
**Status:** Implemented (staged, not committed)

**Decision:** The 7 internal build/planning docs were **archived (moved, not deleted)** out of the participant-facing tree into a new non-shipping internal folder `.squad/planning/`. Git history preserves prior locations.

**Files archived → `.squad/planning/`:** `PLAN.md` (git mv), `PLAN-V2.md` (mv — untracked), `PLAN-V3.md` (mv — untracked), `RESTRUCTURE-SPEC.md` (mv — untracked), `CURRICULUM-REASSESSMENT.md` (mv — untracked), root `decisions.md` — legacy pre-Squad log (git mv; **`.squad/decisions.md` untouched**), `resources/QA-REPORT.md` → `.squad/planning/QA-REPORT.md` (git mv, flattened).

**References fixed:** `README.md` — removed `└── PLAN-V2.md` line from the Repository Structure tree; `.env.sample` re-pointed to the closing `└──` branch (no other README changes). `docs/` and `challenges/` — no stale root-relative links (grep clean). Inter-doc relative links among the 7 still resolve (moved together).

**Added:** `.squad/planning/README.md` index (V1→V2→V3 lineage + status of all 7).

**Constraints honored:** No file deleted (move only). No `git commit` run (staging only). Untouched: `.squad/decisions.md`, challenge content, `.env.sample`, `infra/`, `scripts/`.

---

### Home Page (docs/index.md) Reframed to Three-Tier + Foundations Steps Linked — Linus
**Author:** Linus (Frontend Dev / Docs)  
**Date:** 2026-06-01  
**Requested by:** Marco Olivo  
**Status:** Implemented (staged, not committed)

**Problem:** The published GitHub Pages Home (`docs/index.md`) was stale — it framed the hackathon as **two tiers** (Foundations + Advanced), omitted **Tier 3 · Capstone**, and rendered the Foundations Step rows as plain text with no links. The rest of the site (canonical source `docs/challenges/index.md`) was already three-tier.

**Change (ONLY `docs/index.md`):** (1) frontmatter `description:` "two-tier" → "three-tier"; (2) "What is this?" prose reframed two → three tiers (Foundations / Advanced / Capstone-MAF); (3) quick-card "Two tiers, two paths" → "Three tiers, two paths" and `## Two tiers` heading → `## Three tiers`; (4) Foundations Step rows now LINK to verified anchors — `challenges/foundations#step-1--setup--provisioning-foundry--ai-search`, `#step-2--model-selection--the-playground`, `#step-3--your-first-agent`, `#step-4--knowledge-base-index--foundry-iq---foundations-end-state`; (5) added **Tier 3 · Capstone** section (blurb + time/prereqs table + "Start the Capstone →" btn) linking `challenges/capstone-multi-agent`; (6) Advanced + Extras retained, framed as Tier 2 within the three-tier whole.

**Validation:** grep for "two tier"/"two-tier"/"two tiers" in `docs/index.md` → **0 matches**; Capstone present + links to `challenges/capstone-multi-agent` (3 occurrences); all 4 Foundations steps are links with the exact anchor slugs; `challenges/...` link prefix matches existing working home-page links (no Pages 404).

**Constraints honored:** Edited ONLY `docs/index.md` — did NOT touch `challenges/index.md`, README, or challenge pages. Preserved all HTML/Liquid (hero-panel, quick-grid, btn classes, `{{ '/setup' | relative_url }}`). No git commit. **Note:** canonical source of truth for tier framing = `docs/challenges/index.md`; keep Home as a summary mirror — do not let it drift again.

---

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
- Decision merges occur at end of agent batch cycles

---

## Inbox Merge — 2026-06-01 Batch

### Docs UI Refresh + Markdown Normalization Policy — Linus
**Author:** Linus (Frontend Dev)  
**Date:** 2026-06-01  
**Status:** Implemented (merged from inbox)

**Decision:** Adopt a token-based Just-the-Docs visual system in `docs/_sass/custom/custom.scss` and `docs/_sass/color_schemes/default.scss`, while preserving existing content architecture and Jekyll pipeline constraints. Standardize markdown spacing separation around headings, lists, and checkpoint fences across `docs/` to prevent run-on rendering defects.

**Why:** Requested UI modernization and markdown rendering stability improvements without changing challenge structure or breaking GitHub Pages compatibility.

---

## Inbox Merge - 2026-06-01 ASCII Diagram Batch

### ASCII Diagram Formatting Convention for Docs Challenges - Rusty
**Author:** Rusty (Curriculum Designer)
**Date:** 2026-06-01
**Status:** Implemented (merged from inbox)

**Decision:** For challenge and curriculum flow diagrams in markdown code fences, prefer compact ASCII-only structures and consistent `-->` arrow semantics. Keep line width conservative so diagrams do not wrap or misalign in GitHub Pages/Just-the-Docs.

**Why:** A repo-wide scan found malformed and over-wide diagram blocks that were hard to read or visually broken in current layout. Standardizing lightweight ASCII improves render stability across pages and viewports.

### Docs ASCII Diagram Safety Baseline - Basher
**Author:** Marco Olivo (via Basher)
**Date:** 2026-06-01
**Status:** Implemented (merged from inbox)

**Decision:** For `docs/**/*.md` ASCII diagrams in fenced `text` blocks, enforce a readability baseline: keep line width <= 90 chars when possible, use explicit branch connectors (one clear down-path per branch), and avoid mixed compressed arrow rows that hide routing semantics.

**Why:** QA audit found a malformed branch row in `docs/challenges/extra-magentic-workflows.md` and a high-width flow line in `docs/challenges/extra-build-ui.md`; both reduce clarity on GitHub Pages/Just-the-Docs, especially on narrow viewports.

### ASCII Follow-up Fixes (Targeted) - Linus
**Author:** Linus
**Date:** 2026-06-01
**Status:** Implemented (merged from inbox)

**Decision:** Applied two scoped documentation-only diagram fixes per QA follow-up: (1) explicit four-branch fan-out mapping in `docs/challenges/extra-magentic-workflows.md`; (2) wrap-safe line splitting in the architecture diagram in `docs/challenges/extra-build-ui.md` with unchanged semantics.

**Why:** Reviewer gate requested elimination of remaining ASCII ambiguity and line-wrap fragility without broad content edits.

