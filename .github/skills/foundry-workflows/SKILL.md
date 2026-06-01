---
name: foundry-workflows
description: Multi-agent orchestration in Microsoft Foundry — declarative workflow vs A2A tool call vs Connected Agents pattern; Microsoft Agent Framework (MAF) patterns including Magentic manager/planner. Use for the Magentic Workflows and MAF Extras.
---

# foundry-workflows (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-workflows
```

**Maps to:** Extras · Magentic Workflows (MAF) and MAF + Hosted Long-Running Agents.

**Before implementing:** query `foundry-mcp` for the current workflow/Connected-Agents surface and the
`agent-framework` SDK docs via `microsoft-docs`. Compose specialized agents (Triage / Knowledge / Action /
Escalation) with the Magentic manager pattern; visualize in DevUI.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-workflows/`
