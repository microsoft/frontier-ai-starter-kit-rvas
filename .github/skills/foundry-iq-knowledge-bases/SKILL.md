---
name: foundry-iq-knowledge-bases
description: Build Microsoft Foundry IQ knowledge bases (preview) — multi-source, permission-aware grounding with agentic retrieval (query decomposition + parallel search + reranking); expose to agents via MCP. Use for Foundations Step 4 (Knowledge Base — Index + Foundry IQ).
---

# foundry-iq-knowledge-bases (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-iq-knowledge-bases
```

**Maps to:** Foundations · Step 4 — Knowledge Base (Index + Foundry IQ) — the Foundations **end-state**.

**Before implementing:** query `microsoft-docs` for the current (preview) knowledge-base API and the
Azure AI Search tool query types (`VECTOR_SEMANTIC_HYBRID` is the recommended default). The index over
`resources/sample-data/university-faq/` is built by `scripts/setup-foundations.sh`; use this skill to
build the IQ knowledge base over it and attach it to the agent as an MCP/tool. RBAC: *Search Index Data
Contributor* + *Search Service Contributor*, keyless via the project managed identity.

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-iq-knowledge-bases/`
