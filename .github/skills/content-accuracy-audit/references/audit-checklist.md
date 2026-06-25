# Audit Checklist (per category)

Detailed criteria for [content-accuracy-audit](../SKILL.md). Work top-to-bottom for each
area in scope. Cite an authoritative source (Microsoft Learn URL or MCP result) for every
claim you confirm or refute.

## 1. SDK code snippets (`*.py`, fenced blocks in `*.md`)

- [ ] Every imported module/class/function exists in the **current** package version
      (verify via `microsoft_docs_search` / `microsoft_code_sample_search`).
- [ ] Method names, argument names, and required kwargs match current signatures
      (e.g. `AIProjectClient`, `configure_azure_monitor`, `AIProjectInstrumentor`,
      `azure-ai-evaluation` evaluators).
- [ ] Deprecated/renamed symbols are flagged as **Outdated** with the replacement.
- [ ] Auth uses `DefaultAzureCredential` (keyless-first); key-based examples are flagged.
- [ ] Tracing snippets set `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` and
      `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` **before importing** the SDK.
- [ ] Imports referenced in `solution.md` are actually used/checked by the matching `validate.py`.

## 2. CLI commands (`az`, `azd`, `azd ai agent`, `func`, `npx skills`)

- [ ] Command, subcommand, and flags exist and are spelled correctly.
- [ ] `azd up` / `azd env get-values` / provisioning flow matches `azure.yaml` + `infra/`.
- [ ] Skill stub install commands (`npx skills add microsoft/skills --skill <name>`) name a
      real skill and the `<name>` matches the folder.

## 3. Environment variables

- [ ] Var names are **identical** across `.env.sample`, `docs/`, `challenges/`, `infra/` outputs,
      and `scripts/`. Any drift is **Inconsistent / Medium**.
- [ ] Authoritative Action Tools names match `.env.sample`: `ACTION_API_URL`, `ACTION_MCP_URL`,
      `ACTION_API_KEY`.
- [ ] Foundations vars referenced by validators exist (`AZURE_SEARCH_ENDPOINT`,
      `AZURE_SEARCH_INDEX_NAME`, `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
      `APPLICATIONINSIGHTS_CONNECTION_STRING`, etc.).
- [ ] No real secrets are committed anywhere (`.env` must not be in the repo).

## 4. Infra (`infra/*.bicep`, `azure.yaml`, `scripts/*.sh`)

- [ ] Bicep resource types and `apiVersion` values are valid/current (verify via `azure` MCP /
      `bicepschema`).
- [ ] Bash fallback (`scripts/deploy.sh`) produces the same `.env` contract as `azd up`.
- [ ] Region / SKU / model deployment names referenced in docs exist and are available.

## 5. Dependencies (`requirements.txt`, backend `requirements.txt`)

- [ ] Every package referenced in code is pinned and present.
- [ ] Pinned versions are real and not yanked; flag suspiciously old/preview pins.

## 6. Feature & preview claims

- [ ] "Foundry does X / supports Y" statements confirmed against current docs or `foundry-mcp`.
- [ ] GA vs **preview** status is correct (re-confirm every time — these change fast).
- [ ] No references to removed curriculum pieces (**Prompt Flow** / `promptflow` / `.flow.dag`).

## 7. Cross-references & structure

- [ ] Internal links resolve (file paths, `#anchors`, "see Step N" still points to that step).
- [ ] File paths named in prose exist at that path.
- [ ] `solution.md` step order matches `README.md` and the `validate.py` checks.
- [ ] `_site/` / `docs/_site/` content matches source `docs/` (report drift; don't hand-edit).

## 8. Pacing & pedagogy

- [ ] Each challenge states prerequisites and learning objectives.
- [ ] Difficulty progresses without unexplained jumps; new concepts are introduced before use.
- [ ] Coach (`*-coach.md`) notes align with the learner-facing version (no contradictions).
- [ ] Time/effort estimates (if present) are plausible for the stated steps.

## Severity reference

| Category | Severity |
|---|---|
| Hallucination (nonexistent API/flag/feature) | Critical |
| Outdated (renamed/deprecated/superseded) | High |
| Incorrect (wrong value/order; solution fails validator) | High |
| Inconsistent (env var/path/version mismatch) | Medium |
| Broken reference (dead link / wrong path / stale step) | Medium |
| Pacing (jump / missing prereq / unexplained concept) | Low–Medium |
| Style / clarity | Low |
