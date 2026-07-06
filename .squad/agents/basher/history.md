# Basher — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** AI Starter Kit RVAS — Microsoft Foundry format · **Repo:** ai-starter-kit-rvas · **Requested by:** Marco Olivo.
- Role: QA & Facilitator Enablement. Owns `validate.py` validators (activities author *to* the contract; I implement it).

## Durable learnings / gotchas
- **Validator house style:** `--step N` / `--all` (mutually exclusive group) / `--dry-run`; every Azure call guarded (ImportError + Exception → clear FAIL, never a stack trace) so checkpoints pass offline without burning quota.
- **Foundry rebrand:** "Azure AI Foundry" → "Microsoft Foundry" in prose/links only; literal SDK names + `learn.microsoft.com/azure/ai-foundry/` URLs preserved.
- **Authoritative env contract** (matches `.env.sample` + backend): `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_FOUNDRY_AGENT_NAME`, `AZURE_SEARCH_*`, `ACTION_API_URL=http://localhost:8080`, `ACTION_MCP_URL=http://localhost:8765/mcp`, `ACTION_API_KEY`, `APPLICATIONINSIGHTS_CONNECTION_STRING`. `scripts/setup-foundations.sh` locals are derived shell vars — do NOT "fix" them.
- **Env-rename safety:** ordered perl substitution + negative lookbehind for names that are substrings of each other (`MODEL_DEPLOYMENT_NAME` ⊂ `FOUNDRY_…` ⊂ `AZURE_AI_…`); filter new names back out when verifying.
- **SDK currency verified:** `azure-ai-evaluation>=1.16.9` evaluator class names unchanged; `azure-ai-projects` 2.x (no `from_connection_string`).
- **Overwrite trick:** `create_file` refuses to overwrite — truncate (`: > file`, backup to /tmp) then author; or `rm` + recreate. Not hand-editing via terminal.
- **Capstone validator heuristics:** scan every `*.py` under `--path` (open-ended brief, no fixed filenames); AST + text fallbacks; use **distinct destination sets** for fan-out degree (learners duplicate `add_edge`); aggregate evidence across all files (roles split across modules); `ast.unparse` to render edge-arg node names.

## What I built (cumulative, staged — not committed)
- Authored Advanced **Eval & Red Teaming** (README+solution+validate.py; `assets/northfield-eval.jsonl` 36 rows/13 topics; `adversarial-seed.jsonl` 10 attacks; `evaluate.py` with `--gate` CI exit + custom `NorthfieldDomainEvaluator`) and **Action Tools** validator.
- ENV reconcile across `activities/` (0 legacy tokens remain); authored 4 graceful validators (foundations, tracing, deploy, action-tools); Prompt Flow grep sign-off (activities clean; flagged docs/ hits to Linus, QA-REPORT.md stale ref to coordinator).
- Authored **Capstone `validate.py`** — stdlib-only AST structural validator, 3 gating checks (≥3 roles incl. ≥1 router + ≥2 specialists; fan-out edge; typed Pydantic + send/yield), KB/Action-reuse as non-gating advisory; PASS banner verbatim per Danny; py_compile PASS, self-tested green/red.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: `activities/capstone-multi-agent/validate.py` (stdlib-only, 3 gating checks; advisory non-gating; compiles clean, self-tested green/red). Alongside: Capstone README+solution (Danny), 4 Advanced READMEs de-guided (Rusty), `scripts/cleanup.sh` + lab-generator (Livingston), three-tier README/docs (Linus). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

### 2026-06-01 — Cross-agent note (Scribe merge batch)
- Completed markdown QA audit for Linus's docs UI refresh and markdown normalization pass. No blocking regressions identified in scope; completion was silent, recorded through orchestration + session logs.

### 2026-06-01 — ASCII diagram QA audit (docs markdown)
- Scope: read-only audit of ASCII diagrams in `docs/**/*.md` text fences for GitHub Pages + Just-the-Docs readability/render safety.
- Findings: one structural defect remains in the Magentic manager diagram (`docs/activities/extra-magentic-workflows.md`) where branch connectors are malformed (`▼──────┐ ▼───────▼───────┐`) and can mislead fan-out interpretation.
- Findings: one high line-width portability risk remains in the BFF flow diagram (`docs/activities/extra-build-ui.md`) with a 101-character line that is hard to scan on narrow mobile screens.
- Rusty verification: no Rusty-authored or Rusty-attributed diagram fixes detected in git history/worktree; latest edits touching those files added spacing/readability text but did not correct the malformed branch row.
- Practice update: keep diagram rows under ~90 chars and prefer explicit per-branch down connectors over compressed mixed-arrow rows.

### 2026-06-01 — Cross-agent note (diagram-fix closure)
- Linus addressed both QA findings with targeted doc-only edits and preserved semantics.
- Reviewer gate for this follow-up pass is closed; outcomes recorded via orchestration + session logs.

### 2026-06-01 — URL + claims QA sweep (docs/activities)
- Confirmed two stale Learn paths now return 404 in Foundry docs context: `/agents/how-to/tools/mcp` and `/agents/concepts/agent-protocols`; canonical replacements are `/agents/how-to/tools/model-context-protocol` and hosted-agents key-concepts protocol section.
- Verified activity/docs mirrors can contain hard GitHub blob links to learner-created files (for example `activities/foundations/app/step*.py`) that 404 by design at repo HEAD; treat as QA finding unless curriculum owners want those links removed or reframed.
- Identified content drift: Capstone README/facilitator/docs still say `validate.py` is forthcoming even though `activities/capstone-multi-agent/validate.py` exists and supports `--step`/`--all`.

### 2026-06-01 — Executable validator sweep (pass/fail/blocked matrix)
- Full sweep executed across all `validate*.py` in-scope targets with reproducible logs saved under `/tmp/qa-validate-20260601-venv/*.log`.
- No repo venv was present; temp venv at `/tmp/aihack-qa-venv` + `pip install -r requirements.txt` removed dependency noise and exposed true blockers.
- Result: 1 PASS (`advanced-evaluation-redteam`), 6 BLOCKED, 0 FAIL, 0 N/A.
- Recurrent blocker pattern is prerequisite absence, not harness defects: missing `.env`/Azure provisioning, localhost action backend offline, and learner-authored files not yet created for tracing/deploy/capstone.

### 2026-06-23 — Customer Activity-Forge skill + Outcome-First messaging QA

**Scope:** Two new deliverables: `.github/skills/customer-activity-forge/SKILL.md` and outcome-first messaging reframe across `README.md`, `docs/index.md`, `docs/customer-outcome.md`, `docs/facilitator-hub.md`.

**QA results:**

1. **BUILD:** Jekyll build succeeded (`bundle install` + `bundle exec jekyll build` from `docs/`). Ruby 3.3.8 / Bundler 4.0.12 available; gems installed to `docs/vendor/bundle` (local path needed due to `/var/lib/gems` permission). No build errors. Sass `@import` deprecation warnings present (pre-existing; not introduced by this change). Site output: `docs/_site/`.

2. **LINKS/NAV — FIXED:** All 5 occurrences of `.github/skills/customer-activity-forge/` in docs pages were **broken relative links** on the GitHub Pages build — `.github/` is not served by Pages. Fixed all 5 to the absolute GitHub URL `https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/.github/skills/customer-activity-forge/SKILL.md`, matching the established pattern in `docs/activities/capstone-multi-agent.md` (which uses absolute github.com URLs for all `.github/` skill refs). All anchor slugs for Foundations steps in docs/index.md were verified correct against the built `_site/activities/foundations.html` `id=""` values. README.md's relative `.github/skills/customer-activity-forge/` links are fine (repo-root context on GitHub UI). Minor: docs/index.md line 86 says "the full Two-Paths run guide" — this refers to the Beginner/Advanced-skip execution paths in `activities/index.md` (unchanged), not the two event modes. Slightly confusing post-reframe but not a broken link; flagged for Rusty.

3. **MESSAGING CONSISTENCY:** Customer Build Mode is clearly marked *(primary)* in both mode tables (docs/index.md, docs/customer-outcome.md, facilitator-hub.md pre-event checklist); Northfield is clearly marked *(fallback)*. No residual "co-equal modes" language found. Hero tagline, "What is this?" prose, and Getting Started step 3 all lead with Customer Build. Activity-Forge skill is referenced as the on-ramp for no-idea teams in all three required docs. Path labels "(primary)" and "(fallback)" are consistent across all pages. README's "two ways to run it" section mirrors the same primary/fallback framing.

4. **SKILL REVIEW — PASS:** SKILL.md (a) asks for `customer_name` (required) + `industry` (required) + two optional inputs ✓; (b) instructs public-source-only research, cites every claim with URL, flags unverifiable facts with ⚠️, anti-patterns table explicitly forbids fabrication ✓; (c) all 8 idea fields present (title/description/target user/business outcome/tier-tech/effort tag/industry fit/knowledge sources) ✓; (d) Step 4 states the "sweet spot" guardrails with a table of 5 guardrails including Not-too-trivial/Not-over-common/Not-over-complex/event-window-fit/data-ready-check ✓; (e) Part E in Step 5 maps the top idea onto all 9 Customer Outcome Canvas pre-work fields ✓. Tier/activity label cross-check: all 10 labels in SKILL.md match `activities/` folder names exactly. Two extras (`extra-copilot-assisted`, `extra-hosted-longrunning`) are absent from the label table — by design, they're omitted from idea-generation scope; not a defect. One observation for Danny: the SKILL.md `view` tool is listed to read `docs/customer-outcome.md` before generating — this works in repo context but will silently fail outside the repo without error (graceful; not a blocking issue).

**Fix applied:** 5 broken relative skill links → absolute GitHub URLs (docs/index.md ×2, docs/customer-outcome.md ×1, docs/facilitator-hub.md ×2).

**Verdict: PASS with one trivial fix applied and two minor flags for Rusty.**

### 2026-06-23 — Action Tools SDK remediation (approved branch)

**SDK finding (authoritative):** `azure-ai-agents==1.1.0` (current public release) does NOT contain
`McpTool`, `RequiredMcpToolCall`, `SubmitToolApprovalAction`, or `ToolApproval`. Confirmed via
`python3 -c "import azure.ai.agents.models as m; hasattr(m, 'McpTool')"` → `False`.

**Pattern adopted:** Standard `FunctionTool` + `RequiredFunctionToolCall` + `SubmitToolOutputsAction`
+ `ToolOutput` — all confirmed present in 1.1.0. Same governance objective: run pauses at
`requires_action`, human approves/denies, `submit_tool_outputs` resumes. MCP-native classes named in
honest SDK-note blocks only (not as golden-path requirements).

**Files changed:**
- `activities/advanced-action-tools/agent_with_actions.py` — full rewrite: 3 function stubs + `build_action_tools()` using `FunctionTool`; approval loop uses `RequiredFunctionToolCall`/`SubmitToolOutputsAction`/`ToolOutput`; SDK note in module docstring
- `activities/advanced-action-tools/validate.py` — Step 2: checks `FunctionTool`+fn-names+`ACTION_API_URL`; Step 3: checks `RequiredFunctionToolCall`+`submit_tool_outputs`+`ToolOutput`
- `activities/advanced-action-tools/README.md` — SDK note added; Step 2/3 rewritten; Rung (b) contract updated
- `activities/advanced-action-tools/solution.md` — reference code rewritten; pitfalls updated; timing adjusted
- `docs/activities/advanced-action-tools.md` — mirrors README changes
- `docs/activities/advanced-action-tools-facilitator.md` — mirrors solution.md changes
- `activities/extra-build-ui/README.md` — `RequiredMcpToolCall`→`RequiredFunctionToolCall`, `ToolApproval`→`ToolOutput`
- `activities/extra-build-ui/solution.md` — same two replacements
- `docs/activities/extra-build-ui.md` — same two replacements
- `docs/activities/extra-build-ui-facilitator.md` — same two replacements
- `activities/capstone-multi-agent/validate.py` — APPROVAL_RE broadened to include both old+new class names; advisory message updated

**Checks run (no live Azure required):**
- `py_compile` on agent_with_actions.py, validate.py, capstone validate.py → all OK
- `validate.py --all --dry-run` on starter → Step 1 PASS (dry-run), Step 2 FAIL (placeholder intact ✓)
- `validate.py --step 3` on starter → FAIL (placeholder intact ✓)
- Simulated completed-file check → all 4 signal checks pass ✓
- Capstone `validate.py --list` → runs cleanly ✓

**Remaining live-Azure blocker:** Step 4 (and the actual agent run) requires `AZURE_AI_PROJECT_ENDPOINT` + running backend. No change to that gating — Step 4 was always a live-service check.

### 2026-06-23 — Action Tools golden-path disambiguation (follow-up)

**Scope:** Follow-up review found remaining contradictions where prose still implied the guided path attaches/uses the MCP server. Addressed all required items.

**Changes made:**
- `activities/advanced-action-tools/validate.py` — (1) docstring line 5: "attaches the MCP action tool" → "wires the provided REST backend as a FunctionTool"; (2) startup instruction: removed `python mcp_server.py &`; (3) `check_step2()`: replaced `any(fn in src ...)` with **require all three** function names (strict); (4) `check_step4()` dry-run: checks `app.py` not `mcp_server.py`, updated pass message.
- `activities/advanced-action-tools/agent_with_actions.py` — `ACTION_MCP_URL` env entry labelled "optional — future/preview path only"; prereqs section no longer mentions `mcp_server.py`.
- `activities/advanced-action-tools/README.md` — intro rewritten: "REST API + MCP server … expose three MCP tools" → "REST API … exposes three action endpoints"; table header "MCP tool" → "Action function"; `ACTION_MCP_URL` row marked optional/preview; Step 0 rewritten to require only REST backend (mcp_server.py marked optional stretch); last tip fixed.
- `activities/advanced-action-tools/solution.md` (facilitator) — env table `ACTION_MCP_URL` marked optional; setup block: `python mcp_server.py` → optional comment; `.env` comment updated from `ACTION_MCP_URL` → `ACTION_API_URL`.
- `docs/activities/advanced-action-tools.md` — mirrors README changes above.
- `docs/activities/advanced-action-tools-facilitator.md` — mirrors solution.md changes above.
- `activities/extra-build-ui/README.md` + `solution.md`, `docs/activities/extra-build-ui.md` + `extra-build-ui-facilitator.md` — all `ACTION_MCP_URL` prereq references updated to `ACTION_API_URL`.

**Checks run:**
- `py_compile` on validate.py, agent_with_actions.py, capstone validate.py → all OK
- `validate.py --all --dry-run` on starter → Step 1 ✅ (dry-run), Step 2 ❌ (placeholder intact ✓), Step 4 ✅ (dry-run)
- `grep -rn "attach.*MCP|McpTool|ACTION_MCP_URL"` on all Action Tools files → all remaining hits are SDK notes or "optional/preview" labels ✓
