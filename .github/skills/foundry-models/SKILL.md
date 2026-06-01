---
name: foundry-models
description: Discover, deploy, and manage Microsoft Foundry models; preset vs customized deployments; capacity discovery across regions; quota; PTU vs PAYG; RAI policy. Use for Foundations Step 2 (Model Selection & the Playground).
---

# foundry-models (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-models
```

**Maps to:** Foundations · Step 2 — Model Selection & the Playground.

**Before implementing:** use the `foundry-mcp` MCP server to browse the live model catalog and the
`azure` MCP server for capacity/quota in your region. Compare model families on cost/latency/quality,
write effective system instructions, then reproduce Playground behavior in code via the Inference SDK.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-models/`
