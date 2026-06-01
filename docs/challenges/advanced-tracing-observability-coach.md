---
title: "Advanced: Tracing & Observability · Coach"
parent: Challenges
nav_order: 112
nav_exclude: true
---

# Coach Guide — Advanced: Tracing & Observability

> **Coach-only.** Do not share with students. This guide holds the verified answers, the pitfalls
> teams hit, and the facilitation arc. The student `README.md` deliberately stops at the gotcha box.

## What this challenge proves

By the end a team can take **one** student question and account for its full execution: model span,
retrieval span, optional tool span, with tokens, latency, and an estimated cost — read **two ways**
(portal Tracing tab + KQL). The pedagogy is deliberately FrontierWeekHack's "same data, two lenses"
pattern: the portal teaches the *shape* of a trace, KQL teaches *querying* it.

The challenge assumes the Foundations end-state (a deployed, grounded Northfield IQ Assistant) **or**
the bootstrap skip-path. If a team can't get a grounded answer at all, that's a Foundations problem —
send them to `validate-foundations.py` before debugging tracing.

## The one thing that makes or breaks this challenge

**Set env before import.** 80% of failures are here. The two flags —
`AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`
— are read at SDK import time. If a student imports `azure.ai.projects` (directly or transitively via
another module) *before* setting them, instrumentation initializes without message capture and the
spans show up with empty prompt/response fields, or GenAI spans don't appear at all.

Tell-tale signs and the fix:

| Symptom | Cause | Fix |
|---|---|---|
| Spans exist, prompt/answer fields blank | flags set after import | move `os.environ[...]` to the very top, above all `azure.ai.*` imports |
| No GenAI spans at all | `configure_azure_monitor` never called, or wrong conn string | confirm App Insights conn string resolves; check `enable_tracing()` actually ran |
| `traced_run.py` blank fields but `trace_setup.py` fine | another import at top of `traced_run.py` pulled the SDK in first | ensure `from trace_setup import enable_tracing` is the **first** project import |

## Step-by-step coaching

### Step 1 — Enable instrumentation

- **App Insights connection string:** Foundations writes `APPLICATIONINSIGHTS_CONNECTION_STRING` to
  `.env`. If a team is on the bootstrap path and it's missing, the SDK call
  `project.telemetry.get_application_insights_connection_string()` resolves it (shown in the README).
  Portal path: project → **Monitoring → Application analytics** → copy connection string.

- **SDK import note:** the verified instrumentor import in the current stack is
  `from azure.ai.projects.telemetry import AIProjectInstrumentor` then `.instrument()`. Some teams may
  see tutorials using `project.telemetry.enable()` — that's the convenience wrapper around the same
  instrumentor and is equally acceptable. Either passes the checkpoint as long as message-content
  capture is on.

- If a team hits an `ImportError` on `azure.ai.projects.telemetry`, they're on an old pinned version —
  have them reinstall `requirements.txt` (`azure-ai-projects>=2.1.0`).

### Step 2 — Emit spans

- The grounded question is intentional: it forces a **retrieval** span so the trace has more than a
  bare model call. If a team's question doesn't trigger the knowledge base, the span tree is thin —
  steer them to a question that's clearly answerable only from the FAQ corpus (financial aid docs,
  housing deadlines, registration holds).

- **Latency expectation:** spans take 1–3 min to land. Teams will re-run thinking it failed and create
  duplicate traces. Tell them to wait, then refresh. The `response.id` is the anchor for finding it.

- Auth errors here are almost always `DefaultAzureCredential` (not logged in / wrong subscription),
  not tracing. Have them run `az account show` first.

### Step 3 — Portal Tracing tab

- The span hierarchy: a parent **agent/response** span, with child **model** (`gen_ai` attributes) and
  **retrieval** spans; a **tool** span appears only if they attached the Action Tools MCP tool.

- Token attributes to point at: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`,
  `gen_ai.usage.total_tokens`. Latency = the span `duration`.

- This step's checkpoint is portal-state; `validate.py --step 3` confirms via App Insights that a
  multi-span trace exists for a recent run (it can't read the portal UI directly).

### Step 4 — KQL correlation (the answers)

The README ships three queries as scaffolding. The graded artifact is `correlate.kql` — a working
end-to-end correlation for one `operation_Id`. A complete, correct answer looks like:

```kusto
// correlate.kql — end-to-end trace for one student question, with token/latency/cost rollup
let opId = "abc123def456...";            // the run's operation_Id
let price_per_1k = 0.005;                // model $ / 1K tokens
let spans =
    union dependencies, requests, traces
    | where operation_Id == opId;
spans
| project timestamp, itemType, span = name, duration_ms = duration,
          input_tokens  = toint(customDimensions["gen_ai.usage.input_tokens"]),
          output_tokens = toint(customDimensions["gen_ai.usage.output_tokens"]),
          total_tokens  = toint(customDimensions["gen_ai.usage.total_tokens"])
| order by timestamp asc;
// rollup
spans
| summarize total_tokens = sum(toint(customDimensions["gen_ai.usage.total_tokens"])),
            total_latency_ms = sum(duration),
            span_count = count()
| extend est_cost_usd = round(total_tokens / 1000.0 * price_per_1k, 6)

```

Coaching notes:

- **`dependencies` vs `traces` vs `requests`:** OTel spans map to `dependencies` (outbound calls like
  model/retrieval) and `requests` (the inbound agent invocation); `traces` holds log events. The
  `union` is what gives the full picture — teams that query only `dependencies` miss the parent request.

- **`customDimensions` keys vary slightly** by SDK version. If `gen_ai.usage.total_tokens` is null,
  have them run `dependencies | where operation_Id == opId | project customDimensions` and read the
  actual key names — don't let them assume.

- **Cost is a calculation, not a lookup.** Any sane per-1K rate passes; the learning objective is
  deriving cost from token telemetry, not knowing the exact price.

## Timing (60 min)

- 0–15 min: Step 1 instrumentation (most of the budget goes to the env-before-import gotcha).
- 15–30 min: Step 2 run + the 1–3 min export wait.
- 30–45 min: Step 3 portal span tree.
- 45–60 min: Step 4 KQL correlation + save `correlate.kql`.

If time is tight, prioritize Steps 1–2 (instrumentation working) and the **starter** KQL query over
the full cost rollup.

## Expected questions

- **"Why are my prompt/answer fields empty?"** → set-env-before-import. Walk the file top-down.
- **"Nothing shows in App Insights."** → wait 1–3 min; verify the conn string; verify
  `configure_azure_monitor` ran. Check they didn't point at a different App Insights resource.

- **"Which table has the tokens?"** → `dependencies`, in `customDimensions["gen_ai.usage.*"]`.
- **"Do I need the tool span?"** → no; it only exists if they did Action Tools. The challenge is
  complete with model + retrieval spans.

## Success definition

A team is done when `validate.py --step 4` passes, `correlate.kql` returns all spans for one run, and
they can verbally walk the trace from question → model → retrieval → answer with tokens and latency.
