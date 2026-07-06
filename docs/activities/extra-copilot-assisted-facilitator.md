---
title: "Extra: Copilot-Assisted Build · Facilitator"
parent: Build Modules
nav_order: 125
nav_exclude: true
---

# Facilitator Guide · Extra — Copilot-Assisted Build (microsoft/skills)

> **Facilitator-only.** The lowest-infra, highest-meta Extra: no new Azure resources, and the "deliverable"
> is a *way of working*. Its value is almost entirely contrast — it lands only if the team has already
> felt the manual, search-by-hand path on a real activity. Steer teams to do it after, not first.

## What this activity is really teaching

The whole curriculum's doctrine, made visceral: "MCP = fresh information. Skills = proven patterns."
Students' #1 failure mode all event is hallucinated/stale SDK calls against preview Foundry APIs. This
Extra shows that loading the 3 MCP servers + Foundry skills makes Copilot *fetch the current signature
first*, eliminating that failure class. The keeper insight: grounded generation beats guessing, and
you can prove it side-by-side.

## Infra to pre-provision

None. But verify the enablement layer Livingston shipped is present and wired in the student
Codespace/devcontainer:

- [`.vscode/mcp.json`](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/.vscode/mcp.json) — 3 servers: `azure` (stdio `@azure/mcp`), `foundry-mcp`
  (http `https://mcp.ai.azure.com`), `microsoft-docs` (http `https://learn.microsoft.com/api/mcp`).

- [`.github/copilot-instructions.md`](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/.github/copilot-instructions.md) — the Search-Before-Implement
  rule + skills/MCP map.

- [`.github/skills/`](https://github.com/microsoft/frontier-ai-starter-kit-rvas/tree/main/.github/skills) — the 7 Foundry skill stubs (progressive disclosure;
  installed on demand via `npx skills add`, not vendored — avoids context rot).

> **Flag for the coordinator:** confirm Copilot is licensed/enabled for every participant and that the
> editor actually connects the http MCP servers (corporate proxies sometimes block `learn.microsoft.com/api/mcp`
> or `mcp.ai.azure.com`). Test connectivity at setup, not at demo time.

## Per-step facilitation

### Step 1 — enablement live
- The common blocker is MCP servers not connecting (proxy/firewall). If `microsoft-docs` won't
  connect, the whole Extra is moot — fix networking first.

- Selective loading is mandatory: they install only the skill matching their target activity, not all
  of them. Loading everything causes context rot — the exact anti-pattern the curriculum warns about.

### Step 2 — rebuild assisted
- Best targets: Foundations Step 3 (agent create) or Action Tools (attach MCP tool) — small,
  self-contained, and API-churny enough that grounding visibly helps.

- Watch for: the chat should show a `microsoft-docs`/`foundry-mcp` tool call *before* code. If Copilot
  just emits code from memory, the prompt didn't invoke the doctrine — have them explicitly say "check
  microsoft-docs for the current API first."

- Enforce the authoritative env names (`AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
  `AZURE_FOUNDRY_AGENT_NAME`, `ACTION_MCP_URL`, etc.) so the generated code runs against the real project.

### Step 3 — grounded vs guessed
- The money moment: same task, grounded vs under-specified. The grounded build uses a current
  signature; the guess often uses a renamed class, an old API version, or a removed parameter. Have them
  name the specific diff — that concrete artifact is the whole point.

- Great place to reinforce the facilitator inversion: facilitators load the *full* skill set to validate student
  solutions fast; students load selectively.

## Why no `validate.py`

There's no fixed code artifact to assert — the deliverable is a behavior (Copilot searches before it
builds) and a before/after contrast. Verify by watching the chat transcript (a doc/MCP call precedes
generation) and reviewing the grounded-vs-guessed note. The rebuilt activity's own `validate.py` (if it
has one) is the proof the generated code actually works.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `microsoft-docs` won't connect | proxy/firewall blocks http MCP | whitelist the endpoint; test at setup |
| Copilot codes from memory | prompt didn't invoke search | explicitly ask it to check docs/MCP first |
| Generated code won't run | wrong/guessed env names | use the authoritative `.env` contract names |
| "Context rot" / slow Copilot | all skills loaded at once | load only the one matching the activity |
| No visible contrast | only ran the grounded version | run the under-specified prompt too, compare |
