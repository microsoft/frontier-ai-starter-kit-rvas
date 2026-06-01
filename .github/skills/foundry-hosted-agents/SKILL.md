---
name: foundry-hosted-agents
description: Build, deploy, and manage Microsoft Foundry hosted (containerized) agents — Responses + Invocations protocols, agent.yaml, azd ai agent, per-agent Entra identity, dedicated endpoints, ACR. Use for Advanced Deploy as a Hosted Agent.
---

# foundry-hosted-agents (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-hosted-agents
```

**Maps to:** Advanced · Deploy as a Hosted Agent.

**Before implementing:** query `foundry-mcp` and `microsoft-docs` for the current `azd ai agent`
(create → deploy → invoke) flow and `agent.yaml` schema. ACR is provisioned by `azd up`
(`AZURE_CONTAINER_REGISTRY_ENDPOINT` in `.env`). Configure per-agent managed identity and review run
history + traces against the live endpoint.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-hosted-agents/`
