---
name: foundry-toolboxes
description: Curate intent-based Microsoft Foundry Toolboxes (preview) — one MCP-compatible endpoint bundling MCP, Web Search, Azure AI Search, Code Interpreter, File Search, OpenAPI, A2A, Browser Automation, and Computer Use tools. Build once, consume everywhere. Use for Advanced Action Tools.
---

# foundry-toolboxes (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-toolboxes
```

**Maps to:** Advanced · Action Tools — Make the Agent Do Work.

**Before implementing:** query `foundry-mcp` for the current Toolboxes (preview) surface. In this repo
the action backend + FastMCP server live in `scripts/action-backend/` (env contract in `.env.sample`:
`ACTION_API_URL`, `ACTION_MCP_URL`, `ACTION_API_KEY`). Use this skill to bundle the action MCP tool with
AI Search and consume it from the agent, including the `RequiredMcpToolCall` → `SubmitToolApprovalAction`
human-approval loop.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-toolboxes/`
