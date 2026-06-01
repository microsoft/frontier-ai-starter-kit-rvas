---
name: foundry-projects-resources
description: Provision Microsoft Foundry resources and projects; wire connections (key / OAuth / managed identity / agent identity); standard vs private-network infra. Use for Foundations Step 1 (Setup & Provisioning).
---

# foundry-projects-resources (stub)

> **Minimal stub.** This is a pointer, not the full skill. The authoritative content lives upstream
> in [`microsoft/skills`](https://github.com/microsoft/skills). Do **not** vendor the whole upstream
> body here — install on demand to avoid context rot.

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-projects-resources
```

**Maps to:** Foundations · Step 1 — Setup & Provisioning (Foundry + AI Search).

**Before implementing:** query the `microsoft-docs` and `foundry-mcp` MCP servers for the current
provisioning API surface (Foundry resource `kind=AIServices`, `allowProjectManagement: true`, projects,
connections). In this repo, provisioning is already done by `azd up` + Bicep (`infra/`) — use this skill
to understand the resource ↔ project ↔ connection model and to extend the infra.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-projects-resources/`
