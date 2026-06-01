---
name: foundry-observability
description: Trace, monitor, and evaluate Microsoft Foundry agents — OpenTelemetry GenAI traces in Application Insights (KQL), eval↔trace correlation, azd ai agent monitor, dataset curation from prod traces, built-in quality + safety/RAI evaluators, batch evals, regression detection. Use for Advanced Tracing & Observability and Evaluation & Red Teaming.
---

# foundry-observability (stub)

> **Minimal stub** — pointer to the upstream [`microsoft/skills`](https://github.com/microsoft/skills)
> skill. Install on demand; do not vendor the full body (avoids context rot).

**Install the full skill:**

```bash
npx skills add microsoft/skills --skill foundry-observability
```

**Maps to:** Advanced · Tracing & Observability **and** Advanced · Evaluation & Red Teaming.

**Before implementing:** query `microsoft-docs` for current `AIProjectInstrumentor` /
`configure_azure_monitor` and `azure-ai-evaluation` signatures. **Gotcha:** set
`AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`
**before importing** the SDK. App Insights is provisioned by `azd up`
(`APPLICATIONINSIGHTS_CONNECTION_STRING` in `.env`).

**Upstream source:** `.github/plugins/microsoft-foundry/skills/foundry-observability/`
