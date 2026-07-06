---
name: content-accuracy-audit
description: 'Audit session content (activity guides, facilitator notes, READMEs, validate.py, solution.md, the rendered _site/, docs/, skills, infra, scripts) for correctness, currency, hallucinations, broken cross-references, and pacing. Cross-checks every Azure / Microsoft Foundry SDK signature, CLI command, env var, and API surface against official Microsoft Learn docs via the microsoft-docs MCP and the live web. USE WHEN: review content for errors, fact-check the docs, find hallucinations, check if the docs are up to date, verify API signatures, validate activity instructions, spot outdated SDK calls, check pacing/difficulty, audit the site, find broken links or stale references. Produces a ranked findings report and applies safe fixes.'
argument-hint: '[optional: path or area to audit, e.g. activities/foundations or docs/]'
disable-model-invocation: true
user-invocable: true
---

# Content Accuracy Audit

Systematic review of this session's learning content for **correctness, currency,
hallucinations, broken references, and pacing**. The golden rule of this repo applies:
**Search Before Implement** — never trust a memorized API signature. Every Azure / Foundry
SDK call, CLI command, env var, and preview-feature claim must be verified against the
**current** official docs before you mark it correct or rewrite it.

## When to Use

- "Review/audit all our content for errors of any kind"
- "Check the docs for hallucinations / outdated SDK calls / wrong API signatures"
- "Are the activity instructions still accurate and up to date?"
- "Verify the env vars, CLI commands, and code snippets actually work"
- "Check pacing and difficulty progression across activities"
- "Find broken cross-references / dead links / stale file paths"

## Inputs

- **Scope** (optional argument): a path or area (e.g. `activities/foundations`, `docs/`,
  `_site/`, `.github/skills/`). If omitted, audit the whole repo content surface (below).
- The audit is **read-heavy**; fixes are applied only after findings are confirmed.

## Content surface to audit

| Area | What to check |
|---|---|
| `docs/activities/*.md` (+ `*-facilitator.md`) | Instructions, code snippets, env vars, pacing, learning objectives |
| `activities/*/README.md`, `solution.md` | Steps match the validator; solution actually satisfies `validate.py` |
| `activities/*/validate.py`, `*.py` | Imports/signatures exist; checks match the stated steps |
| `_site/` and `docs/_site/` | **Generated** — flag drift vs source `docs/`, do NOT hand-edit (see Pitfalls) |
| `.github/skills/*/SKILL.md` | Stub install commands, env-var names, "gotcha" claims still valid |
| `infra/*.bicep`, `azure.yaml`, `scripts/*.sh` | Resource/API versions, command flags, output→`.env` contract |
| `.env.sample`, `requirements.txt` | Var names authoritative & consistent everywhere; pinned versions exist |
| `README.md`, `decisions.md`, `setup.md`, `resources.md` | Cross-links resolve; claims match current Azure/Foundry reality |

## Procedure

Work one area at a time. Use the detailed [audit checklist](./references/audit-checklist.md)
for the full per-category criteria. Track progress with a todo list when scope is large.

### 1. Inventory the scope
Enumerate the files in scope. For large scope, group by area (table above) and audit
area-by-area so findings stay organized.

### 2. Extract verifiable claims
From each file, pull out every **checkable assertion**:
- SDK imports, classes, methods, kwargs (e.g. `AIProjectClient`, `configure_azure_monitor`)
- CLI commands & flags (`az`, `azd`, `azd ai agent`, `func`)
- Env var names and the values they expect
- Package names + pinned versions in `requirements.txt`
- Bicep resource types + `apiVersion` values
- Preview/GA status claims and "this feature does X" statements
- Cross-file references (file paths, anchor links, "see Step N")

### 3. Verify against official sources (Search Before Implement)
For each claim, confirm against the **current** source of truth — do not rely on memory:
- **`microsoft-docs` MCP** (`microsoft_docs_search`, then `microsoft_docs_fetch` for depth;
  `microsoft_code_sample_search` for real code) — primary for SDK/CLI/env signatures.
- **`foundry-mcp`** — Foundry-native ops (model catalog, agents, toolboxes, KBs, evals)
  to confirm feature names, capabilities, and current availability.
- **`azure` MCP** — resource types, RBAC, quota, Bicep `apiVersion` reality.
- **Live web** (`fetch_webpage`) — only for official Microsoft/Azure URLs already cited in
  the content, to confirm they resolve and still say what we claim. Do not invent URLs.
- **Repo ground truth** — does `solution.md` actually pass `validate.py`? Do env-var names
  match `.env.sample` and `infra/` outputs exactly?

Record the authoritative source (doc URL or MCP result) for every confirmed or refuted claim.

### 4. Classify findings
Use these categories and severities (details in the checklist):
- **Hallucination** — API/feature/flag that does not exist → **Critical**
- **Outdated** — real but superseded/renamed/deprecated signature → **High**
- **Incorrect** — wrong value, wrong step order, solution won't pass validator → **High**
- **Inconsistent** — env var / path / version mismatch across files → **Medium**
- **Broken reference** — dead link, wrong file path, stale "Step N" → **Medium**
- **Pacing** — difficulty jump, missing prerequisite, unexplained concept → **Low/Medium**
- **Style/clarity** — ambiguous or sloppy wording → **Low**

### 5. Report
Produce a ranked findings report using the
[report template](./assets/findings-report-template.md): one row per finding with
file+line link, category, severity, the verified source, and the proposed fix.
**Present findings before mass-editing.**

### 6. Apply fixes (after confirmation)
- Fix **source** files (`docs/`, `activities/`, `.github/skills/`), never the generated
  `_site/` by hand.
- Make minimal, targeted edits — correct the inaccuracy, don't rewrite surrounding prose.
- When a fix changes an env var / path / version, update **every** occurrence repo-wide.
- After fixing code or validators, re-run the relevant `validate.py` to confirm green.
- Re-verify each fixed signature one last time against the doc source you cited.

## Quality bar (completion checks)

- [ ] Every flagged SDK/CLI/env claim has a cited authoritative source (doc URL or MCP result).
- [ ] No fix introduces a signature you did not verify this session.
- [ ] Env-var names, file paths, and pinned versions are consistent across all files.
- [ ] `solution.md` steps still satisfy the matching `validate.py` (re-run where feasible).
- [ ] Generated `_site/` drift is reported, not hand-patched.
- [ ] Findings report lists residual/unverifiable items explicitly (don't silently drop them).

## Pitfalls

- **Don't hand-edit `_site/` or `docs/_site/`.** They are generated (Jekyll). Fix the source
  in `docs/` and note that the site must be rebuilt.
- **Don't guess preview status.** Foundry features move fast and many are preview — confirm
  GA/preview wording against current docs every time.
- **Don't invent or "fix" URLs.** Only verify URLs already present; never fabricate links.
- **Prompt Flow is removed from this curriculum.** Any `promptflow` / `.flow.dag` reference is
  itself a finding to remove — do not "correct" it, flag it.
- **Keyless-first.** Flag examples that use keys where `DefaultAzureCredential` is the convention.
- **Don't mass-rewrite for style.** Stay scoped to correctness, currency, and pacing unless asked.
