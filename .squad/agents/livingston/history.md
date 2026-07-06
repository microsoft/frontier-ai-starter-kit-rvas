## Learnings

### GitHub Pages baseurl / private-site root-serving gotcha — 2026-06-01

- **Symptom:** Pages site 404s on every CSS/JS asset (e.g. `/ai-starter-kit-rvas/assets/css/...`).
- **Root cause:** When a Pages site's visibility is **Private**, GitHub serves it from a randomized subdomain at the ROOT (e.g. `random-name-xxxx.pages.github.io/`) with NO project-name path segment. But `docs/_config.yml` hardcodes `baseurl: "/ai-starter-kit-rvas"`, and just-the-docs prepends that baseurl to every `relative_url` asset link — so assets resolve to `/ai-starter-kit-rvas/assets/...`, which doesn't exist on a root-served site → 404.
- **Fix pattern (do NOT touch `_config.yml`):** In `.github/workflows/deploy-pages.yml`, give the `actions/configure-pages@v6` step an `id: pages`, then pass its live output to the build: `jekyll build ... --baseurl "${{ steps.pages.outputs.base_path }}"`. `base_path` is `""` for a private root-served site and `/ai-starter-kit-rvas` if flipped to Public — so the workflow self-corrects for BOTH visibilities. Keeping `_config.yml` untouched preserves local dev (`bundle exec jekyll serve`) and the public URL.
- A sibling repo (`frontier-ghaw-session`) hit and proved this exact fix.

### Cleanup + Lab-Generator batch — 2026-06-01

- **`scripts/cleanup.sh` (backlog #7, [FWH §4.10]) — safety design:** safe-by-default. A
  bare run is a DRY-RUN that only prints teardown targets + a "what keeps costing money" list
  and changes nothing. Destructive cloud teardown is gated behind an explicit `--yes`; the
  resource group is shown first and NEVER deleted blindly. Flags: `--yes` (teardown via
  `azd down --force`, RG-delete fallback), `--local-only` (explicit, safe — only stops the
  Action Tools procs/containers), `--purge` (escalates to `azd down --force --purge` + purges
  soft-deleted Cognitive Services/Foundry accounts). `set -Eeuo pipefail`; every destructive
  command guarded.
- **azd-hang gotcha:** `azd env get-values` (and `azd down`) can spawn a daemon that keeps the
  pipe open, so plain command-substitution HANGS even with login present. Fix: a `guarded()`
  helper wrapping `timeout -k 5 <secs> …` (escalates TERM→KILL) **plus** `</dev/null` on every
  azd call to detach stdin and avoid the daemon-fd hang. Verified empirically — without `-k`
  and stdin detach the dry-run never returned.
- **docker branch gotcha:** when the daemon is unreachable (WSL2) `docker ps` prints a setup
  hint to stdout, polluting the `RUNNING` capture and triggering a phantom "stopped" path.
  Gate the whole block behind `docker info >/dev/null 2>&1` first.
- **Env contract respected:** cleanup reads ONLY existing `.env.sample` variable names
  (`AZURE_RESOURCE_GROUP`, `AZURE_SUBSCRIPTION_ID`, `AZURE_LOCATION`, `AZURE_ENV_NAME`,
  `AZURE_*_ENDPOINT`, `AZURE_CONTAINER_REGISTRY_NAME`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
  `ACTION_API_URL`, `ACTION_MCP_URL`). Local ports are *derived* from the ACTION_*_URL values
  (no new names introduced). `.env` is read-only — never written.
- **`.github/agents/lab-generator.agent.md` (backlog #4, [FWH §4.9/§6]) — frontmatter format:**
  matched the house `squad.agent.md` style: YAML frontmatter with `name`, `description`, plus
  `tools:` array and a `handoff:` list (to the scenario template). Body encodes the reskin
  contract as hard invariants: tool-shape invariant (create-a-ticket / place-a-hold /
  book-a-slot, mapped 1:1, never a 4th tool), the 4 swap surfaces, `.env` NAMES read-only
  (new var ⇒ `TODO: Bicep-output (Livingston)`), do-not-touch backbone/`validate.py`, and
  Search-Before-Implement via the microsoft-docs / foundry-mcp MCP servers.
- **`.github/agents/scenario-template.md`** is the companion the lab-generator consumes — a
  fill-in skeleton for the 4 swap surfaces with **NorthPeak Outfitters** (retail) as the worked
  example: persona `northpeak-support-assistant`, corpus topics (returns/shipping/warranty/
  sizing), the 3 tools mapped 1:1 (`open_support_case` / `place_order_hold` / `schedule_callback`),
  and eval+adversarial category notes (jailbreak/harmful/injection — injection-via-review-text
  is the richest red-team material).

### Project Context
- **Project:** AI Starter Kit RVAS — Microsoft Foundry format
- **Repo:** ai-starter-kit-rvas
- **Stack:** Microsoft Foundry AI, GitHub Pages (Jekyll/static), Markdown, GitHub Actions
- **Participants:** Students (new to AI) + Facilitators (facilitators)
- **Goal:** Create a complete, deliverable session format with a polished GitHub Pages site
- **Requested by:** Marco Olivo
- **Date:** 2026-05-28

### Version Audit — 2026-05-28

- Verified all Python deps, devcontainer features, GitHub Actions, and Gemfile against current stable releases.
- `azure-ai-projects` has gone GA at 2.x — import path unchanged but constructor requires `endpoint=` kwarg. Flag raised in decision doc for Rusty/Basher to audit activity samples.
- `azure-search-documents` bumped to 12.x (major) — flag raised for RAG activity review.
- `openai` bumped to 2.x — `chat.completions` still works; `responses.create()` is new preferred API.
- `azure-ai-inference` remains beta (1.0.0b9 unchanged); `promptflow` is sustained but not growing.
- GitHub Actions: `checkout` → v6, `configure-pages` → v6, `upload-pages-artifact` → v5, `deploy-pages` → v5.
- Node.js in devcontainer bumped from 20 (maintenance LTS) to 22 (active LTS).
- `just-the-docs` `~> 0.8` → `~> 0.10` (current stable 0.12.0); `jekyll` `~> 4.3` → `~> 4.4` (current stable 4.4.1).
- Gemfile.lock NOT regenerated — must be done with `cd docs && bundle install` by a maintainer.
- Decision doc written to `.squad/decisions/inbox/livingston-version-audit.md`.

### Repo Infrastructure Setup
- Added the baseline directory scaffold for activities, docs, resources, and repo automation assets so content can land in stable locations.
- Standardized the devcontainer on Python 3.11 with Azure CLI, Node.js 20, GitHub CLI, and a post-create bootstrap flow.
- Captured a reusable GitHub Pages + Jekyll pattern with `docs/Gemfile`, a Pages deployment workflow, and contributor templates.
- Provisioning scripts for AI Foundry should be written defensively because Azure CLI support for hub/project resources can vary between extension versions.


---

## Team Update — 2026-05-28 Session Complete

**Session:** Fact-check & CSS fix (multi-batch agent work)

**Major Outcomes:**
- **Microsoft Foundry rebrand applied** — All activities verified & updated (Azure AI Foundry → Microsoft Foundry)
- **CSS rendering restored** — GitHub Pages now displays with full just-the-docs theme
- **Content verified against current docs** — All SDK versions, deployment patterns, and terminology current (no breaking changes)
- **Humanizer pass complete** — 28 files cleaned of AI-generated patterns (emojis, em dashes, promotional vocab)
- **Cross-page links fixed** — Activity discovery pages now render without 404s
- **Platform resilience discovered** — Serial agent dispatch works around 401 outages (parallel spawn causes race conditions)

**Next:** Marco needs to `git push` to deploy CSS fix to live site; maintainers must run `cd docs && bundle install` to regenerate Gemfile.lock.

---

### 2026-06-01 — Curriculum V2 direction (Scribe note)
- `PLAN-V2.md` is the new curriculum direction (Proposed): agent-era rearchitecture, core spine 00–07, one-artifact-many-acts Northfield "IQ" Assistant narrative.
- **Prompt Flow is CUT** per Marco's directive — old Activity 03 removed; dependent RAG/eval steps re-expressed on Agents + AI Search + Foundry IQ + MCP + MAF; `promptflow*` deps leave the devcontainer.
- See `.squad/decisions.md` and `.squad/log/2026-06-01-curriculum-v2-planning.md`.

### 2026-06-01 — Two-tier restructure + Prompt Flow removal (executed)
- Executed RESTRUCTURE-SPEC §2.1 `git mv`/`git rm` sequence (staged, not committed — Scribe commits later).
- **Renames (history preserved):** `activity-00-setup` → `foundations`; `activity-05-evaluation` → `advanced-evaluation-redteam`; `activity-06-deploy` → `advanced-deploy-hosted-agent`.
- **Deleted:** `activity-03-prompt-flow/` (entire folder, `git rm -r`); `docs/activities/activity-03.md` + `activity-03-facilitator.md` (spec §5).
- **Pending harvest (left in place per task + spec harvest-before-remove):** `activity-01-first-model`, `activity-02-prompt-engineering`, `activity-04-rag` — Rusty must harvest into `foundations/` Steps 2–4 before these get `git rm`'d.
- **Created placeholders** (`<!-- PLACEHOLDER: content authored in Wave 2 -->` README + solution): `advanced-action-tools`, `advanced-tracing-observability`, `extra-fabric-iq`, `extra-voice-live`, `extra-magentic-workflows`, `extra-hosted-longrunning`, `extra-build-ui`, `extra-copilot-assisted`.
- **requirements.txt:** removed `promptflow`, `promptflow-tools`; added `azure-ai-agents`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`.
- **devcontainer.json:** removed `ms-toolsai.promptflow` extension.
- **Docs nav:** removed broken `activity-03` rows from `docs/index.md`, `docs/activities/index.md`, `docs/facilitator-hub.md`.
- **GOTCHA:** git rename-detection cross-paired identical `.gitkeep` files between unrelated folders in `git status` output — cosmetic only; the real `README.md`/`solution.md` renames tracked correctly with history.
- **Left for content authors (NOT edited — prose):** prompt-flow references remain in `README.md` (root), `activities/activity-04-rag/`, `activities/advanced-deploy-hosted-agent/` (ex-06), `docs/activities/activity-04.md`, `activity-06.md`, `activity-02.md` pager, `docs/facilitator-hub.md` troubleshooting rows, `resources/QA-REPORT.md`. Full list in restructure decision doc.

### 2026-06-01 — Infra + automation scaffolding (azd/Bicep, bootstrap, action tools, Copilot layer)
- **azd golden path:** authored `azure.yaml` (no `services:` — infra-only `azd up`), `infra/main.bicep` (subscription scope, creates RG + module), `infra/resources.bicep` (Foundry AIServices `allowProjectManagement:true`, project, model deployment, AI Search basic, Log Analytics + App Insights, ACR, project connections to Search+AppInsights, keyless RBAC), `infra/main.parameters.json` (azd `${VAR=default}` substitution). `az bicep build` passes clean.
- **Bash fallback** `scripts/deploy.sh`: mirrors Bicep via `az` + ARM REST (Foundry needs `allowProjectManagement`, not in `az cognitiveservices`); writes the full `.env` contract; graceful guards (login/az/quota) fail with clear messages, model-deploy failure is non-fatal.
- **Bootstrap skip-path (Path B):** `scripts/setup-foundations.sh` (loads `.env` or `azd env get-values`; STEP 1 real AI Search index build + chunked corpus upload via `azure-search-documents`; STEP 2/3 Foundry IQ KB + agent + AI Search tool via `azure-ai-projects`, **guarded/degrades gracefully** since preview surface is volatile). `scripts/validate-foundations.py` = the single Path-B checkpoint (4 checks; agent-answer-with-citation, falls back to a grounded Search query if the preview agent surface is absent).
- **Action Tools backend (provided; teams wire it):** `scripts/action-backend/app.py` (FastAPI, in-memory, 3 actions: IT ticket / course hold / advising slot, optional `x-api-key`), `mcp_server.py` (FastMCP wraps the REST API as MCP tools), `requirements.txt`, `README.md`.
- **DECISION — action-tools env contract (AUTHORITATIVE):** no `basher-eval-action.md` existed in the inbox, so I DEFINED the names: `ACTION_API_URL=http://localhost:8080`, `ACTION_MCP_URL=http://localhost:8765/mcp`, `ACTION_API_KEY` (optional `x-api-key`). Basher/Rusty action-tools + eval content MUST match these. Documented in `.env.sample` + decision doc.
- **Copilot enablement layer:** `.vscode/mcp.json` (3 servers: `azure` stdio `@azure/mcp`, `foundry-mcp` http `https://mcp.ai.azure.com`, `microsoft-docs` http `https://learn.microsoft.com/api/mcp`), `.github/copilot-instructions.md` (Search-Before-Implement), and 7 `.github/skills/*/SKILL.md` stubs (progressive-disclosure frontmatter + `npx skills add` pointer; NOT vendored).
- **`.env.sample`** documents the whole `.env` variable contract (Foundry/Search/Obs/ACR/Azure/Action). Real `.env` never committed.
- **Prompt Flow cleanup in files I own:** rewrote root `README.md` (intro, learning outcomes, getting-started, activity table → two-tier, repo tree, footer) and `.devcontainer/post-create.sh` (activity quick-links + `.env.example`→`.env.sample`). Root README now grep-clean of prompt-flow/activity-0N.
- **Validation:** `bash -n` (both shells), `py_compile` (3 py files), JSON parse (params + mcp.json), `az bicep build` — all pass.
- **GOTCHA:** azd `.env` contract flows Bicep `output` → azd env → `azd env get-values > .env`. Output names in `main.bicep` are intentionally identical to `.env.sample` keys so the two stay in sync.
- Nothing committed (Scribe owns commits).

### 2026-06-01 — Curriculum V2 implemented (cross-agent note)
Curriculum V2 is now built to disk (staged, not committed). Final shape: **two-tier** — Tier 1 Foundations (4 ordered steps) + Tier 2 (4 Advanced activities + 6 Extras). **Prompt Flow fully removed** (deps, devcontainer, activities, docs). `docs/` mirrors `activities/` 1:1 with facilitator siblings. Decision inbox merged into `.squad/decisions.md` (28 entries); session log: `.squad/log/2026-06-01T100000Z-curriculum-v2-build.md`.

### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: `scripts/cleanup.sh`
(confirmation-gated, DRY-RUN by default, `--yes`/`--local-only`/`--purge`), `.github/agents/lab-generator.agent.md`
(reskin meta-agent), and `.github/agents/scenario-template.md` (NorthPeak retail worked example) —
existing env var NAMES only, `.env.sample`/Bicep untouched. Alongside: Tier 3 Capstone live
(Danny + Basher), 4 Advanced READMEs de-guided (Rusty), three-tier README/docs (Linus). Inbox merged
into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log:
`.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

## Learnings

- 2026-06-01 — Archived 7 internal build/planning docs out of the participant-facing tree into a new non-shipping folder `.squad/planning/` (moved, not deleted; git history preserved). Files: PLAN.md, PLAN-V2.md, PLAN-V3.md, RESTRUCTURE-SPEC.md, CURRICULUM-REASSESSMENT.md, decisions.md (root legacy log — NOT `.squad/decisions.md`), and resources/QA-REPORT.md (flattened to `.squad/planning/QA-REPORT.md`). Used `git mv` for tracked (PLAN.md, decisions.md, QA-REPORT.md), plain `mv` for untracked V2/V3/SPEC/REASSESSMENT.
- Added `.squad/planning/README.md` index documenting V1→V2→V3 lineage, RESTRUCTURE-SPEC executed, CURRICULUM-REASSESSMENT consumed by V3, decisions.md superseded by `.squad/decisions.md`, QA-REPORT = QA pass record.
- README repo-tree fix: removed the `└── PLAN-V2.md` line from the "Repository Structure" tree and re-pointed `.env.sample` to the closing `└──` branch. No other README content altered. docs/ and activities/ had no stale root-relative links to the moved files (validate.py's "PLAN-V3 §3.7" is a section citation, not a link — left untouched).
- 2026-06-01 — Dependency audit found one install blocker: `azure-ai-agents>=2.0.0` in root `requirements.txt` was unsatisfiable (latest GA is 1.1.0). Updated floor to `>=1.1.0` after confirming Foundry docs still recommend `azure-ai-projects>=2.x` + `DefaultAzureCredential` endpoint auth, and after checking release streams on PyPI. Left other lower bounds unchanged to avoid forcing avoidable beta/major jumps.

### 2026-06-23 — setup-resources.sh key-based logic removal (follow-up)

`resources/scripts/setup-resources.sh` still contained key-based legacy logic after the env-contract pass:
`get_project_key()` called `az ml workspace show-keys` / `list-keys`; collected `OPENAI_KEY` via
`az cognitiveservices account keys list`; collected `SEARCH_KEY` via `az search admin-key show`;
and wrote `AZURE_OPENAI_API_KEY` and referenced `AZURE_AI_KEY` in a warn message.

**Fix:** Replaced the entire 227-line script with a ~50-line compatibility wrapper that:
- Emits a clear `DEPRECATED` banner naming both golden paths (`azd up`, `scripts/deploy.sh`)
- Resolves `scripts/deploy.sh` relative to the script's own directory (`../../scripts/deploy.sh`)
- `exec`s into `scripts/deploy.sh "$@"` when found and executable
- Exits 1 with instructions when the delegate is missing

**Validation:**
- `bash -n resources/scripts/setup-resources.sh` → OK
- `grep -En 'AZURE_AI_KEY|AZURE_OPENAI_API_KEY|show-keys|admin-key|SEARCH_KEY'` → no matches
- Executable bit preserved (`-rwxr-xr-x`)

### 2026-06-23 — Env/dependency/repo-contract remediation

Executed the approved remediation plan across 9 files (10 changed; 2 files pre-changed by others before my pass):

**Changes made:**
- `.env.example` — replaced stale variable block with a single pointer comment directing users to `.env.sample`; eliminates conflicting legacy names (`FOUNDRY_PROJECT_ENDPOINT`, `AZURE_AI_KEY`, `UNIVERSITY_QA_ENDPOINT`, etc.)
- `.devcontainer/devcontainer.json` — replaced legacy `remoteEnv` keys (`AZURE_AI_ENDPOINT`, `AZURE_AI_KEY`) with authoritative names (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`); added port 8765 to `forwardPorts` for Action Tools MCP server
- `resources/scripts/validate-environment.py` — aligned `REQUIRED_VARS` and `OPTIONAL_VARS` to `.env.sample` contract; removed `promptflow` / `promptflow-tools` from `PACKAGE_CHECKS`; removed key-based auth logic from endpoint check (keyless-first)
- `resources/scripts/setup-resources.sh` — updated the `.env` write block to emit `.env.sample`-canonical names (replaced `AZURE_AI_ENDPOINT` + `AZURE_AI_KEY` with `AZURE_AI_PROJECT_ENDPOINT` + `AZURE_AI_MODEL_DEPLOYMENT_NAME`; removed `AZURE_SEARCH_KEY`)
- `requirements.txt` — added `httpx>=0.27.0` and `PyYAML>=6.0` (not already present; `azure-monitor-query` skipped — no imports found in validators)
- `.github/PULL_REQUEST_TEMPLATE.md` — replaced Activity 00–06 checklist with Foundations / Advanced / Extras / Capstone / Cross-cutting structure
- `.github/workflows/deploy-pages.yml` — bumped `actions/checkout@v6` → `@v7` (latest stable; configure-pages@v6, upload-pages-artifact@v5, deploy-pages@v5 were already correct)
- `docs/_config.yml` — updated nav external link from `azure/ai-foundry/` → `azure/foundry/` (canonical Microsoft Foundry docs URL); updated title from "Azure AI Foundry Docs" → "Microsoft Foundry Docs"
- `docs/setup.md` — replaced `.env.example` → `.env.sample`; replaced 4× "Activity 00" references with "Foundations"/"the Foundations activity"

**Validation:**
- `python3 -m json.tool .devcontainer/devcontainer.json` → OK
- `python3 -m py_compile resources/scripts/validate-environment.py` → OK
- `bash -n resources/scripts/setup-resources.sh` → OK
- requirements.txt parsed 18 deps cleanly
- `grep -c promptflow resources/scripts/validate-environment.py` → 0

**Constraints honored:** Did not touch Action Tools activity files (Basher's ownership). Did not edit broad curriculum prose beyond the specific stale env/activity-number references. No commit made (Scribe owns commits).

**GOTCHA:** `git diff --stat HEAD` showed `activities/foundations/README.md` and `docs/activities/foundations.md` as already modified before my pass — those are not in my ownership and I did not touch them; they appeared in the diff because an earlier agent staged changes before this session started.

---

## Pass 3 — 2026-06-23 · Missing `azure-monitor-query` root dependency

**Trigger:** Follow-up scan by Squad found two validators importing `azure.monitor.query` while `requirements.txt` lacked the package.

**Files changed:**
- `requirements.txt` — added `azure-monitor-query>=1.4.0` immediately after `azure-monitor-opentelemetry>=1.6.0` in the tracing/observability block.

**Checks run:**
- `grep azure-monitor-query requirements.txt` → confirmed present
- `python3 -m py_compile activities/advanced-tracing-observability/validate.py` → OK
- `python3 -m py_compile activities/advanced-deploy-hosted-agent/validate.py` → OK
