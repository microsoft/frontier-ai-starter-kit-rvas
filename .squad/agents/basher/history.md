# Basher — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** WTH AI Hackathon — Microsoft Foundry format · **Repo:** ai-hackathon · **Requested by:** Marco Olivo.
- Role: QA & Coach Enablement. Owns `validate.py` validators (challenges author *to* the contract; I implement it).

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
- ENV reconcile across `challenges/` (0 legacy tokens remain); authored 4 graceful validators (foundations, tracing, deploy, action-tools); Prompt Flow grep sign-off (challenges clean; flagged docs/ hits to Linus, QA-REPORT.md stale ref to coordinator).
- Authored **Capstone `validate.py`** — stdlib-only AST structural validator, 3 gating checks (≥3 roles incl. ≥1 router + ≥2 specialists; fan-out edge; typed Pydantic + send/yield), KB/Action-reuse as non-gating advisory; PASS banner verbatim per Danny; py_compile PASS, self-tested green/red.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: `challenges/capstone-multi-agent/validate.py` (stdlib-only, 3 gating checks; advisory non-gating; compiles clean, self-tested green/red). Alongside: Capstone README+solution (Danny), 4 Advanced READMEs de-guided (Rusty), `scripts/cleanup.sh` + lab-generator (Livingston), three-tier README/docs (Linus). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

### 2026-06-01 — Cross-agent note (Scribe merge batch)
- Completed markdown QA audit for Linus's docs UI refresh and markdown normalization pass. No blocking regressions identified in scope; completion was silent, recorded through orchestration + session logs.
