# History Archive — Basher

> Archived 2026-06-01 by Scribe (history.md exceeded 15360 B). Verbatim prior history below; active history.md now carries a tight summary.

---

## Learnings

### Project Context
- **Project:** AI Starter Kit — Microsoft Foundry format
- **Repo:** ai-starter-kit-rvas
- **Stack:** Microsoft Foundry AI, GitHub Pages (Jekyll/static), Markdown, GitHub Actions
- **Participants:** Students (new to AI) + Facilitators (facilitators)
- **Goal:** Create a complete, deliverable session format with a polished GitHub Pages site
- **Requested by:** Marco Olivo
- **Date:** 2026-05-28

### 2026-05-28T16:23:27.374+01:00 — Full QA review learnings
- The most common content-quality gaps were structural consistency issues, not major technical defects.
- Activity docs and site summaries drift fastest around naming, doc URLs, and narrative continuity; these need explicit QA checks together.
- Infra validation should track direct snippet dependencies (`azure-core`, `flask`) and activity-specific endpoint variables, not just platform packages.
- Broken media links are better removed than left as placeholders when the repo does not actually ship the assets.
- For event-day readiness, Activities 03–06 are the main candidates for optional starter artifacts if the team wants less ambiguity for students and facilitators.

### 2026-05-28T20:30:00.000+01:00 — Activities 04–06 audit + repo-wide URL sweep

**Rebrand pattern applied (Rusty-established):**
- "Azure AI Foundry" product name → "Microsoft Foundry" everywhere in narrative, link text, and planning docs.
- Exception: literal SDK names ("Azure AI Search", "azure-ai-evaluation", "Azure AI Inference SDK") are preserved unchanged.
- Exception: `learn.microsoft.com/azure/ai-foundry/` URL paths are preserved — they are valid, not stale.

**SDK verification outcomes:**
- `azure-search-documents` 12.x — Activity 04 uses the portal "Add your data" / Playground integration workflow with no direct SDK vector-query code; no code changes required. If future code samples are added, use `VectorizableTextQuery` or `VectorizedQuery` from `azure.search.documents.models`.
- `azure-ai-evaluation` 1.16.9 — `GroundednessEvaluator`, `RelevanceEvaluator`, `CoherenceEvaluator`, `FluencyEvaluator` class names are unchanged; Activity 05 skeleton is valid.
- `azure-ai-projects` 2.x constructor — `from_connection_string` not found in ch 04–06 files; clean.
- Flask 3.1.x — Activity 06 scaffold pattern is valid; no breaking API changes.

**Badge fix (Task C):**
- README.md line 3: `pages.yml` → `deploy-pages.yml`; badge link target updated from repo root to workflow runs page.

**URL sweep findings:**
- `github.com/microsoft/ai-starter-kit-rvas/discussions` → `github.com/microsoft/frontier-ai-starter-kit-rvas/discussions` (found in `docs/resources.md` Community section).
- No `docs.microsoft.com/` or `ai-studio/` path refs found in ch 04–06 or any other in-scope file.
- `learn.microsoft.com/en-us/` paths with redundant `/en-us/` were already correct (those URLs are valid).

**Files with no changes needed:**
- Activity solution/facilitator guides for 04–06 contained only facilitation language — no stale product names or SDK references.
- `.github/ISSUE_TEMPLATE/` files were clean.

---

## 2026-05-28 — Cross-page link fix (broken Pages links)

**Task:** Fix 7 `../../activities/.../README.md` relative links in `docs/activities/activity-XX.md` that resolved outside the Jekyll Pages tree and produced 404s on the live site.

**Files changed:**
- `docs/activities/activity-00.md`
- `docs/activities/activity-01.md`
- `docs/activities/activity-02.md`
- `docs/activities/activity-03.md`
- `docs/activities/activity-04.md`
- `docs/activities/activity-05.md`
- `docs/activities/activity-06.md`

**URL pattern applied:** `https://github.com/microsoft/frontier-ai-starter-kit-rvas/tree/main/activities/activity-XX-name` (folder view, not blob/README, so participants see the full folder + solution.md).

**Audit result:** Full grep of `docs/**/*.md` for `../../` patterns — no other escaping links found.

**Decision doc:** `.squad/decisions/inbox/basher-cross-page-link-fix.md`

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

### 2026-06-01 — Authored two Advanced activities (Eval & Red Teaming + Action Tools)

**Scope:** Wrote student `README.md` + facilitator `solution.md` + `validate.py` for both, using RESTRUCTURE-SPEC §3.2 banner and §3 STEP template (Goal → Tasks → Success Criteria → Checkpoint).

**Evaluation & Red Teaming** (`activities/advanced-evaluation-redteam/`):
- 5 steps: portal quality metrics → code `evaluate.py` → custom domain evaluator → red teaming (jailbreak/harmful/indirect-injection) → CI score gate.
- **Dataset:** `assets/northfield-eval.jsonl` = **36 grounded rows** across **13 topics** (financial-aid, course-registration, it-support, housing, admissions, academic-integrity, library, international, campus-health, careers, academic-programs, student-clubs, out-of-scope). Includes `factual`, `edge`, and `abstain` categories. Each row: `query`, `context`, `ground_truth`, `topic`, `category`. Far beyond the FWH/ATA 10-row samples.
- **Adversarial seed:** `assets/adversarial-seed.jsonl` = 10 labeled attacks across 4 categories incl. 3 prompt-injection-via-retrieved-doc rows (`injected_context`) + `expected_behavior` answer key.
- **`evaluate.py` interface:** `--dataset PATH`, `--gate FLOAT` (exit 1 if any metric mean < threshold = CI gate), `--custom-only`, `--dry-run` (response=ground_truth, zero Azure calls). Built-ins: Groundedness/Relevance/Coherence/Fluency via `azure-ai-evaluation`; custom `NorthfieldDomainEvaluator` (1–5, rewards grounded contact + correct abstention, penalizes foreign emails). Agent invocation via `agents.threads/messages/runs.create_and_process`.
- `validate.py --step {1..4}` / `--all` — all offline (dry-run/custom-only) so facilitators don't burn quota. **All checkpoints PASS.**

**Action Tools** (`activities/advanced-action-tools/`):
- 5 steps (0–4): start provided backend → knowledge-vs-action concept → attach `McpTool` → implement approval loop → end-to-end action + denial path.
- **Backend already shipped by Livingston** at `scripts/action-backend/` (FastAPI `app.py` + FastMCP `mcp_server.py`). Tools: `create_it_ticket`, `place_course_hold`, `book_advising_slot`; `server_label="northfield_actions"`.
- **Env contract (authoritative, matches `.env.sample` + backend):** `ACTION_API_URL=http://localhost:8080`, **`ACTION_MCP_URL=http://localhost:8765/mcp`** (the McpTool endpoint), `ACTION_API_KEY` (optional `x-api-key`, empty for workshop).
- Shipped starter `agent_with_actions.py` with `< PLACEHOLDER >` gaps (ATA single-line-completion pattern); full approval-loop reference (`RequiredMcpToolCall → ToolApproval → SubmitToolApprovalAction` via `submit_tool_outputs`) lives ONLY in `solution.md`.
- `validate.py`: Step 1 + 4 do REST round-trips against the backend (offline from Azure); Steps 2/3 are static wiring/placeholder checks. Pre-completion, Steps 2/3 correctly FAIL on unfilled placeholders.

**QA notes / patterns:**
- `create_file` refuses to overwrite; to replace harvested v1 content (old activity-05 README/solution), truncate with `: > file` (backups to /tmp) then author. This is full-file rewrite, not hand-editing via terminal.
- Leakage check: grep student READMEs for `facilitator|answer key|reference completion|def run_with_approval` — only benign "ask your facilitator" phrasing remained; no reference impls leaked.
- Verified `azure-ai-evaluation>=1.16.9` evaluator class names unchanged; pinned in requirements.txt.

### 2026-06-01 — ENV reconcile + validate.py checkpoints + Prompt Flow grep sign-off

**Requested by Marco (coordinator). Three linear QA tasks. No git commit; docs/ prose untouched (Linus owns mirror); facilitator answers stay only in solution.md.**

**Task 1 — ENV VAR RECONCILE (activities/ only).** Grepped all of `activities/` for env names NOT in the `.env.sample` contract and reconciled to the authoritative names. Renames applied (perl ordered-substitution for .md to avoid `MODEL_DEPLOYMENT_NAME` substring collisions; edit-tool for .py):
- `FOUNDRY_PROJECT_ENDPOINT` → `AZURE_AI_PROJECT_ENDPOINT` (16)
- `FOUNDRY_MODEL_DEPLOYMENT_NAME` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` (9)
- `FOUNDRY_AGENT_NAME` → `AZURE_FOUNDRY_AGENT_NAME` (6)
- bare `MODEL_DEPLOYMENT_NAME` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` (7, negative lookbehind `(?<!AZURE_AI_)`)
- `AZURE_OPENAI_DEPLOYMENT` → `AZURE_AI_MODEL_DEPLOYMENT_NAME` (4, eval only)
- `NORTHFIELD_AGENT_ID` → `AZURE_FOUNDRY_AGENT_NAME` (4; 2 markdown hits fixed manually — omitted from the perl batch)
- Files touched: foundations README+solution; advanced-evaluation-redteam README+solution+evaluate.py; advanced-tracing-observability README; advanced-deploy-hosted-agent README; advanced-action-tools solution.md+agent_with_actions.py.
- **scripts/ NOT touched** — `setup-foundations.sh` locals (`SEARCH_INDEX_NAME`, `KB_NAME`, `AGENT_NAME`, `CORPUS_DIR`) are internal shell vars correctly *derived from* the contract, not contract names. Do not "fix" them.
- Verified: 0 legacy tokens remain ("NONE — all reconciled"); 0 corruption (no `AZURE_AI_AZURE`/double-names).

**Task 2 — validate.py checkpoints.** Authored/updated 4 validators, all `--step N` / `--all` / `--dry-run`, all Azure calls guarded (ImportError + Exception → clear FAIL, never a stack trace):
- `activities/foundations/validate.py` (NEW) — Step1 .env contract + keyless `get_token`; Step2 `AIProjectClient.get_openai_client().responses.create`; Step3 named agent via `list_agents()`; Step4 grounded answer **with citation** (`_has_citation`), fallback to a citable `SearchClient` hit. `--all` → "✅ Foundations end-state PASS — grounded Northfield IQ Assistant is live".
- `activities/advanced-tracing-observability/validate.py` (NEW) — structural-first: Step1 trace_setup.py sets BOTH OTEL flags **above** first `azure.*` import (line-order check) + `configure_azure_monitor`; Step2 traced_run.py calls `enable_tracing()` then drives the agent, optional guarded App-Insights span count via `LogsQueryClient`; Step3 capture-content flag; Step4 correlate.kql has `operation_Id` + span tables.
- `activities/advanced-deploy-hosted-agent/validate.py` (NEW) — Step1 parses hosted/agent.yaml (PyYAML, regex fallback) for `responses` protocol on port 8088 + name, main.py serves 8088, Dockerfile `EXPOSE 8088`; Step2 guarded deployed-agent lookup; Step3 guarded live endpoint (anonymous → 401/403, authed → 200); Step4 guarded run-history span query.
- `activities/advanced-action-tools/validate.py` (PATCHED) — added `--dry-run`: Step1 checks provided `app.py` present (REST health skipped), Step4 checks `mcp_server.py` present (round-trip skipped); Steps 2/3 already static.
- **py_compile: PASS on all 7** (4 validators above + evaluation validate.py + evaluate.py + agent_with_actions.py).
- **Offline `--all --dry-run` smoke: all 4 non-crash**, clear FAIL/PASS. With no `.env` + unauthored student artifacts present they correctly report missing-var / missing-file FAILs (graceful, no creds needed) — exactly the intended "fails gracefully without live Azure" behavior.

**Task 3 — Prompt Flow grep sweep.** `.devcontainer/` exists and is in scope. Sweep of `activities/ resources/ requirements.txt .devcontainer/`:
- **activities/ — CLEAN of accidental refs.** All 4 hits are *deliberate guardrails*: deploy-hosted README:36 "No Prompt Flow here" box + solution.md:6/8/115 "rewritten away from Prompt Flow" facilitator context. KEEP.
- **requirements.txt:18** — guardrail comment "replaces deprecated Prompt Flow". KEEP.
- **.devcontainer/** — no hits.
- **resources/QA-REPORT.md:39** — 1 *stale historical* reference to the old `activity-03-prompt-flow/` structure + `flow.dag.yaml` artifacts. Left AS-IS: it is a point-in-time QA record, not curriculum; rewriting would falsify the report. **Flagged to coordinator.**
- **docs/ (NOTE for Linus, NOT fixed):** 8 hits — `docs/facilitator-hub.md:61,72`; `docs/activities/activity-04-facilitator.md:52,59`; `docs/activities/activity-04.md:133,135,167`; `docs/activities/activity-06.md:64,66,227`. These are the old Prompt Flow curriculum in the docs mirror; Linus owns reconciliation.

**Patterns / lessons:**
- Ordered perl substitution + negative lookbehind is the safe way to rename env vars whose names are substrings of each other (`MODEL_DEPLOYMENT_NAME` ⊂ `FOUNDRY_MODEL_DEPLOYMENT_NAME` ⊂ `AZURE_AI_MODEL_DEPLOYMENT_NAME`).
- When verifying renames, filter the new names back out (`grep -vE "AZURE_FOUNDRY_AGENT_NAME|AZURE_AI_MODEL_DEPLOYMENT_NAME"`) or false positives from the substring overlap mask a truly-clean result.
- Don't batch-rename the whole token list blindly — `NORTHFIELD_AGENT_ID` had no overlap risk but was easy to forget; cross-check the directive list against the perl script.

### 2026-06-01 — Curriculum V2 implemented (cross-agent note)
Curriculum V2 is now built to disk (staged, not committed). Final shape: **two-tier** — Tier 1 Foundations (4 ordered steps) + Tier 2 (4 Advanced activities + 6 Extras). **Prompt Flow fully removed** (deps, devcontainer, activities, docs). `docs/` mirrors `activities/` 1:1 with facilitator siblings. Decision inbox merged into `.squad/decisions.md` (28 entries); session log: `.squad/log/2026-06-01T100000Z-curriculum-v2-build.md`.

### 2026-06-01 — Authored Capstone `validate.py` (AST structural validator)

**Task (Marco):** author `activities/capstone-multi-agent/validate.py` — a LIGHT, headless validator for the STRUCTURAL subset of the Tier-3 Capstone acceptance criteria (PLAN-V3 §3.7). Aligned to Danny's contract drop (`danny-capstone-built.md`) and the authoritative README. Did NOT touch Danny's README/solution, Advanced READMEs, root README, or docs. No git commit.

**Why this validator is different from the Advanced ones:** the Capstone is an **open-ended design brief — no starter file, no PLACEHOLDERs, no fixed filenames.** So the validator can't grep one known wiring file — it scans **every `*.py` under `--path`** (default = activity dir, recursive `rglob`, self-excluded) and grades by **AST + text heuristics**, tolerant of how learners name files/agents.

**CLI shape (matches house style + Danny's contract):**
- `--all` (required group) / `--step {1,2,3}` / `--list` — mutually exclusive group.
- `--path DIR` (NEW vs other validators) — point at the learner's capstone source; defaults to the activity dir.
- **Exit 0 only if all 3 required structural checks pass.** PASS banner is **verbatim per Danny's contract**: `✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use`. Fail banner: `❌ ONE OR MORE STRUCTURAL CHECKS FAILED`.
- **Stdlib only** (argparse, ast, pathlib, re) — no httpx/azure/pyyaml — so it runs anywhere with zero deps.

**The 3 REQUIRED structural checks (auto-graded, gate exit 0):**
1. **≥3 agent/executor roles** — collects candidate identifiers from: classes subclassing `*Executor`/`*Agent`; `@executor`/`@agent`-decorated funcs; assignments `x = Something(Executor|Agent)(...)` / `ChatAgent`/`AzureAIAgent`/`create_agent`; and every node named in `add_edge`/`set_start_executor`. Requires ≥3 distinct **and** ≥1 named like a router (`triage|router|route|classif|dispatch`) **and** ≥2 specialists.
2. **Parallel fan-out** — parses `add_edge(src,dst)` (also `add_fan_out_edges(a,[b,c])` list/tuple form) into a graph; computes **distinct** out-degree/in-degree. PASS needs a node with **≥2 distinct outgoing edges** (the fan-out). Fan-in (a node with ≥2 incoming = synthesizer join) is reported as a hint, not gated — matches README wording "fan-out edge present".
3. **Typed Pydantic contracts** — needs a `BaseModel` subclass (AST base-name check + `class \w+\(...BaseModel` text fallback) **AND** a `send_message`/`yield_output` call. If `re.search/match/findall/split` appears in source, prints a ⚠ hint (possible prose-parsing) but does not fail.

**Advisory (printed, NOT gating) — the deliberate reconciliation:** Marco's task asked to also detect KB-reuse + Action-Tools-approval-loop. But Danny's contract AND the README mark criterion 4 (reuse) as **facilitator-confirmed/live, NOT in validate.py**. Constraint: "align to the README (authoritative)." **Resolution:** I detect both by import/reference (`KB_RE`: AZURE_SEARCH/AzureAISearch/university-faq/foundry_iq/…; `APPROVAL_RE`: RequiredMcpToolCall/ToolApproval/SubmitToolApprovalAction/ACTION_MCP_URL/northfield_actions/McpTool) and print them under an `— advisory (facilitator-confirmed live, not gating) —` block with ✅/➖ marks — so they inform but never change exit code. Noted in the decision drop.

**`--list`** echoes the three buckets: AUTO-GRADED (steps 1–3), ADVISORY (reuse hints), and FACILITATOR-JUDGED/MANUAL (both topologies shown, DevUI visual, OTel multi-agent span tree, 2-min demo, hosted background run) — so facilitators know exactly what's machine-checked vs eyeballed.

**Heuristics/lessons:**
- `ast.unparse` (3.9+) is the clean way to turn an edge-arg node back into a readable executor name (`Name`→id, `Attribute`→dotted, `Call`→text); wrapped in try/except with manual fallback for safety.
- Use **distinct destination sets** for degree, not raw edge counts — learners sometimes duplicate an `add_edge`, which would inflate a naive counter and false-pass fan-out.
- Aggregate evidence **across all files** (one Scan object), not per-file — learners legitimately split triage/specialists/synthesizer/contracts across modules; a per-file check would false-fail.
- Text-level fallbacks complement the AST walk (BaseModel via regex, send/yield via regex) so a contract defined in a way the AST pass misses still registers.
- **py_compile: PASS.** Self-tested with a synthetic 4-executor fan-out fixture → all 3 PASS, advisory ✅✅, exit 0, exact banner. Empty-dir negative → Step 1 FAIL, exit 1. Both correct.

### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: `activities/capstone-multi-agent/validate.py`
— stdlib-only structural validator (3 gating checks: ≥3 roles, fan-out edge, typed Pydantic
contracts; KB/Action-Tools-reuse advisory non-gating), compiles clean, self-tested green/red.
Alongside: Capstone README + solution (Danny), 4 Advanced READMEs de-guided (Rusty),
`scripts/cleanup.sh` + lab-generator (Livingston), three-tier README/docs (Linus). Inbox merged into
`.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log:
`.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
