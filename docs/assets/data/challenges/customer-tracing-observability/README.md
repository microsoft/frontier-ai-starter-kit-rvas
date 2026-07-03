
# Customer Build · Chapter 4 — See inside it



This chapter is **mutuated from [Advanced · Tracing & Observability](challenge.html?id=advanced-tracing-observability)** — same OpenTelemetry setup, same span-reading workflow — but the run you trace is *your* demo journey from [Chapter 0: Define your outcome](challenge.html?id=customer-outcome).

> **Before you start this chapter:** finish [Chapter 1](challenge.html?id=customer-foundations). If [Chapter 2](challenge.html?id=customer-action-tools) applies, include one approved or denied action in the traced path.

---

## Step 1 — Enable tracing before imports

**Why it matters for your app:** without instrumentation, failures look like vibes. With traces, you can point to the model, retrieval, or tool span that caused the issue.

**Does this apply to you?**
- **Build it** if you will show or pilot the agent beyond a notebook.
- **Adapt it** if this is a tiny local demo — still set the flags and capture one trace, but skip dashboards.
- **Skip it** only for a static mock where no live agent call happens.

**Decisions to make:**
- Which environment runs the traced demo: local script, notebook, UI backend, or hosted agent?
- Who may view captured message content?
- Is your corpus safe to appear in trace payloads?
- What app name or run label helps you find your trace later?

**Apply it to your app:** wire the tracing setup exactly as the reference shows; the import order is not optional. → [Tracing — Step 1](challenge.html?id=advanced-tracing-observability#step-1--enable-genai-instrumentation)

**Prove you applied it:**
- `python challenges/advanced-tracing-observability/validate.py --track customer --step 1 --dry-run`
- Checklist: ☐ tracing flags are set before Azure SDK imports ☐ App Insights connection is resolved ☐ message capture is acceptable for your demo data ☐ no secrets or PII are logged.

**Stuck?** [Northfield Step 1](challenge.html?id=advanced-tracing-observability#step-1--enable-genai-instrumentation).

---

## Step 2 — Trace a real scenario run

**Why it matters for your app:** a trace is only useful if it covers the path stakeholders care about, not a generic ping.

**Does this apply to you?**
- **Build it** for any live agent demo.
- **Adapt it** if the demo is small — trace one representative question and one failure/abstention.
- **Skip it** only if you skipped live agent execution entirely.

**Decisions to make:**
- Which Chapter 0 *demo story* question becomes the traced run?
- Does it force retrieval, action, escalation, or all three?
- What output proves the run belongs to your scenario?
- What identifier will you copy into your notes: response id, operation id, timestamp?

**Apply it to your app:** run your agent through the traced wrapper and ask your real scenario question. → [Tracing — Step 2](challenge.html?id=advanced-tracing-observability#step-2--run-the-agent-and-emit-spans)

**Prove you applied it:**
- `python challenges/advanced-tracing-observability/validate.py --track customer --step 2 --dry-run`
- Checklist: ☐ traced run prints an answer ☐ run includes your scenario question ☐ operation/response id is captured ☐ wait time for span propagation is accounted for.

**Stuck?** [Northfield Step 2](challenge.html?id=advanced-tracing-observability#step-2--run-the-agent-and-emit-spans).

---

## Step 3 — Inspect the span tree

**Why it matters for your app:** the span tree tells you whether the answer came from the model alone, retrieval, a tool, or a failed branch.

**Does this apply to you?**
- **Build it** if you need to explain a success or failure to a coach or stakeholder.
- **Adapt it** if you only have model spans today — record that retrieval/tool spans are absent and why.
- **Skip it** only if you cannot access the portal during the event; keep the KQL step as backup.

**Decisions to make:**
- Which spans should exist for your app path?
- What token, latency, and retrieval signals matter for your success measures?
- What span would reveal a safety-boundary failure?

**Apply it to your app:** find the trace in Foundry and identify model, retrieval, and tool spans as applicable. → [Tracing — Step 3](challenge.html?id=advanced-tracing-observability#step-3--inspect-the-spans-portal-tracing-tab)

**Prove you applied it:**
- `python challenges/advanced-tracing-observability/validate.py --track customer --step 3 --dry-run`
- Checklist: ☐ parent span found ☐ model span identified ☐ retrieval/tool spans identified or explicitly absent ☐ token and latency notes recorded.

**Stuck?** [Northfield Step 3](challenge.html?id=advanced-tracing-observability#step-3--inspect-the-spans-portal-tracing-tab).

---

## Step 4 — Correlate the run in KQL (chapter end-state)

**Why it matters for your app:** KQL lets you turn a single demo run into evidence: ordered spans, latency, token totals, and cost signals.

**Does this apply to you?**
- **Build it** if you need repeatable troubleshooting or a production hardening story.
- **Adapt it** for a small demo by saving one useful query, not a full dashboard.
- **Skip it** only if observability is out of scope; document that your prototype is not diagnosable yet.

**Decisions to make:**
- Which operation id is your canonical demo trace?
- What summary fields matter: total latency, token count, retrieval count, tool count, failure status?
- What threshold would become an alert later?

**Apply it to your app:** save a correlation query that reconstructs one of your scenario runs end-to-end. → [Tracing — Step 4](challenge.html?id=advanced-tracing-observability#step-4--correlate-one-question-end-to-end-with-kql)

**Prove you applied it:**
- `python challenges/advanced-tracing-observability/validate.py --track customer --all --dry-run`
- Checklist: ☐ `correlate.kql` exists ☐ query filters one operation id ☐ output includes ordered spans ☐ one latency/token/cost observation is ready for the demo.

**Stuck?** [Northfield Step 4](challenge.html?id=advanced-tracing-observability#step-4--correlate-one-question-end-to-end-with-kql).

---

## Chapter 4 end-state

You have **one end-to-end trace for your scenario**, plus a KQL query that explains where time, tokens, retrieval, and tools went.

```bash
python challenges/advanced-tracing-observability/validate.py --track customer --all --dry-run
```

Next: **[Chapter 5 — Ship it](challenge.html?id=customer-deploy-hosted-agent)**.
