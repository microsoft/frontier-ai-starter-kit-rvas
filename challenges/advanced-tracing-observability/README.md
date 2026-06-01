# Advanced — Tracing & Observability

> ⏱ **Guided ~1 hr** · 🛠 **Build-from-scratch ~1.5 hr** · ⭐⭐⭐⭐ · **Prereqs:** Foundations end-state

> **Tier 2 · Advanced — modular.** You can attempt this in any order with the other Advanced
> challenges. **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

## Why this challenge

Your Northfield IQ Assistant answers grounded questions today — but when a student gets a slow,
wrong, or uncited answer, can you explain **why**? Right now the agent is a black box: a model call,
a knowledge-base retrieval, and (if you did Action Tools) a tool call all happen inside one request,
and you can see none of it.

In this challenge you make every answer **observable end to end**. You enable OpenTelemetry (OTel)
GenAI tracing, export the spans to **Application Insights**, and then read the same data **two ways** —
the Foundry portal **Tracing** tab and a **KQL** query in App Insights. By the end you can take a single
student question and reconstruct its entire journey: model → retrieval → tool, with token counts,
latency per span, and the inputs/outputs at each hop.

This is the observability layer that the Evaluation and Deploy challenges both build on: evals become
trustworthy when you can trace the row that failed, and a hosted agent is only production-ready when
you can watch it run.

```text
  student question
        │
        ▼
  ┌───────────── one request (operation_Id) ─────────────┐
  │  agent span                                          │
  │   ├─ model span        gen_ai.usage.*  (tokens)      │
  │   ├─ retrieval span    knowledge-base query          │
  │   └─ tool span         (if Action Tools attached)    │
  └──────────────────────────────────────────────────────┘
        │                                   │
        ▼                                   ▼
  Foundry portal  ◀──── App Insights ────▶  KQL (dependencies / traces / requests)
   Tracing tab           (OTel exporter)
```

## What you will need

- The Foundations `.env` (or bootstrap `.env`) with at least:
  - `AZURE_AI_PROJECT_ENDPOINT` — your Foundry project endpoint
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` — the chat model deployment
  - `AZURE_FOUNDRY_AGENT_NAME` — the Northfield IQ Assistant agent name (e.g. `northfield-iq-assistant`)
- An **Application Insights** resource linked to your Foundry project. Foundations provisions one;
  its connection string lands in `.env` as `APPLICATIONINSIGHTS_CONNECTION_STRING`. If that variable
  is missing, see Step 1 — you will fetch it from the project.
- Packages from `requirements.txt` (already installed in the devcontainer):
  `azure-ai-projects`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`.

> 💡 Tracing data takes **1–3 minutes** to land in App Insights after a run. Budget for that lag
> before you decide something is broken.

---

This challenge ships **three rungs** off the same backbone — the **same `validate.py` grades all
three**. **(a) Guided path** (below) gives you the code to assemble · **(b) Build-from-scratch path**
gives you only the gotcha + the package list · **(c) Stretch goals** go open-ended.

## Rung (a) — Guided path

> The beginner on-ramp: the code is here to assemble and run. The lesson is the *ordering gotcha*.

## Step 1 — Enable GenAI instrumentation

**Goal:** Your agent process emits OpenTelemetry GenAI spans and ships them to Application Insights.

**Tasks:**

1. Confirm your project has an App Insights connection. If `APPLICATIONINSIGHTS_CONNECTION_STRING` is
   not already in `.env`, fetch it from the project and add it (the portal shows it under
   **Monitoring → Application analytics**, or read it via the SDK as shown below).
2. Create `challenges/advanced-tracing-observability/trace_setup.py` that wires tracing **in the exact
   order below**. The two `os.environ[...]` lines MUST run **before** any `azure.ai.*` import — this is
   the single most common mistake in this challenge (see the gotcha box).
3. Run the file. It should print that instrumentation is enabled and the App Insights connection was
   resolved, without emitting spans yet.

```python
# trace_setup.py
import os

# ── 1. Tracing flags MUST be set BEFORE importing the Azure AI SDK. ──────────────
#    The instrumentation reads these at import time. Set them first or message
#    content (prompts/answers) will silently never appear on your spans.
os.environ["AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"] = "true"
os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"

# ── 2. NOW import the SDK. ───────────────────────────────────────────────────────
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor


def enable_tracing() -> AIProjectClient:
    project = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    # Resolve the App Insights connection string (env first, then ask the project).
    conn = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not conn:
        conn = project.telemetry.get_application_insights_connection_string()
        os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"] = conn

    # Route all OpenTelemetry spans to Application Insights.
    configure_azure_monitor(connection_string=conn)

    # Turn on GenAI semantic-convention spans for model / retrieval / tool calls.
    from azure.ai.projects.telemetry import AIProjectInstrumentor
    AIProjectInstrumentor().instrument()

    print("✅ GenAI tracing enabled; spans will export to Application Insights.")
    return project


if __name__ == "__main__":
    enable_tracing()
```

> ⚠️ **The "set env before import" gotcha.** If you put the two `os.environ[...]` assignments *after*
> `from azure.ai... import ...`, the instrumentation has already initialized and will **ignore them**.
> Symptom: spans appear but every prompt/response field is empty, or no GenAI spans show up at all.
> Keep the env lines at the very top of the file, above all Azure imports.

**Success Criteria:**

- [ ] `APPLICATIONINSIGHTS_CONNECTION_STRING` is present in `.env` (or resolved at runtime).
- [ ] Running `trace_setup.py` prints `✅ GenAI tracing enabled` with no import error.
- [ ] The two tracing env flags are set **above** every `azure.ai.*` import in the file.

**Checkpoint:**

```bash
python validate.py --step 1
# expected: "✅ Step 1 PASS — instrumentation wired, App Insights connection resolved"
```

> _Coach note: see solution.md._

---

## Step 2 — Run the agent and emit spans

**Goal:** A real student question flows through the agent and produces a trace (model + retrieval,
plus a tool span if Action Tools is attached).

**Tasks:**

1. Create `challenges/advanced-tracing-observability/traced_run.py`. Import and call
   `enable_tracing()` from Step 1 **first**, then ask the Northfield IQ Assistant a grounded question
   that forces a knowledge-base lookup — e.g. *"What documents do I need for financial aid?"*
2. Drive the agent through the Responses API against your `AZURE_FOUNDRY_AGENT_NAME`. Print the answer and
   the trace/operation id so you can find the run later.
3. Run it. Then **wait 1–3 minutes** for the spans to land in App Insights.

```python
# traced_run.py
import os
from trace_setup import enable_tracing   # importing this runs the env-first setup

project = enable_tracing()
client = project.get_openai_client()

QUESTION = "What documents do I need to apply for financial aid at Northfield?"

response = client.responses.create(
    input=QUESTION,
    extra_body={
        "agent_reference": {
            "name": os.environ["AZURE_FOUNDRY_AGENT_NAME"],
            "type": "agent_reference",
        }
    },
)

print("Q:", QUESTION)
print("A:", response.output_text)
print("response id:", response.id)   # use this to locate the trace
```

**Success Criteria:**

- [ ] The script prints a grounded answer (the financial-aid answer cites the FAQ corpus).
- [ ] The run completes without a tracing/auth error.
- [ ] Within ~3 minutes, at least one new GenAI span is visible in App Insights (you confirm this in
      Step 3).

**Your run should look like this:**
```text
Q: What documents do I need to apply for financial aid at Northfield?
A: You'll need your FAFSA (school code 041777), prior-year tax returns, W-2s, and ...
response id: resp_01J8X...   ← use this to find the trace
✅ GenAI tracing enabled; spans will export to Application Insights.
```

**Checkpoint:**

```bash
python challenges/advanced-tracing-observability/traced_run.py
python validate.py --step 2
# expected: "✅ Step 2 PASS — agent run emitted >=1 GenAI span to App Insights"
```

> _Coach note: see solution.md._

---

## Step 3 — Inspect the spans (portal Tracing tab)

**Goal:** You can read a single run as a span tree in the Foundry **Tracing** tab and identify the
model, retrieval, and (if present) tool spans.

**Tasks:**

1. In the Foundry portal, open your project → **Tracing** (under Observability / Monitoring). Find the
   trace for the run you just made (sort by most recent; match the timestamp).
2. Expand the trace into its **span tree**. Identify and note:
   - the **model** span — look for the `gen_ai.usage.*` token attributes,
   - the **retrieval** span — the knowledge-base / AI Search query and the documents returned,
   - the **tool** span — only present if you completed the Action Tools challenge.
3. Open the model span and record: input tokens, output tokens, total tokens, and span duration
   (latency). Note where the prompt and the generated answer appear as attributes (this only works
   because you set `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` in Step 1).

**Success Criteria:**

- [ ] The Tracing tab shows your run as a parent span with at least one child span.
- [ ] You can name which child is the model call and which is the retrieval call.
- [ ] You can read token counts and duration off the model span.

**Checkpoint:** Portal state — the **Tracing** tab shows the run's span tree with an expandable
model span exposing `gen_ai.usage.total_tokens`. Capture the trace's **operation id** for Step 4.

```bash
python validate.py --step 3
# expected: "✅ Step 3 PASS — span tree present with model + retrieval spans"
```

> _Coach note: see solution.md._

---

## Step 4 — Correlate one question end-to-end with KQL

**Goal:** Read the **same** run as data — write a KQL query that pulls every span for one student
question and surfaces token, latency, and cost signals.

**Tasks:**

1. In App Insights → **Logs**, start from this **starter query** to list recent GenAI spans. Run it,
   then copy the `operation_Id` of your financial-aid run:

   ```kusto
   // Starter: recent GenAI spans across model / retrieval / tool tiers
   dependencies
   | where timestamp > ago(1h)
   | where customDimensions has "gen_ai" or name has_any ("chat", "responses", "retrieval", "tool", "agent")
   | project timestamp, operation_Id, name, duration_ms = duration,
             total_tokens = toint(customDimensions["gen_ai.usage.total_tokens"])
   | order by timestamp desc
   ```

2. Pivot to a **single end-to-end correlation** — replace the placeholder with your `operation_Id`
   to reconstruct the whole request as an ordered timeline (model + retrieval + tool):

   ```kusto
   // End-to-end: one student question, every span, in order
   let opId = "<paste-your-operation_Id>";
   union dependencies, requests, traces
   | where operation_Id == opId
   | project timestamp, itemType, span = name, duration_ms = duration,
             input_tokens  = toint(customDimensions["gen_ai.usage.input_tokens"]),
             output_tokens = toint(customDimensions["gen_ai.usage.output_tokens"]),
             total_tokens  = toint(customDimensions["gen_ai.usage.total_tokens"])
   | order by timestamp asc
   ```

3. Extend the correlation query to **surface token, latency, and cost** in one summary row. Compute
   cost from total tokens using your model's per-1K-token rate (pick the rate for your deployed model;
   the exact number is not what's graded — the calculation is):

   ```kusto
   let opId = "<paste-your-operation_Id>";
   let price_per_1k = 0.005;   // <-- your model's $ / 1K tokens
   dependencies
   | where operation_Id == opId
   | summarize total_tokens   = sum(toint(customDimensions["gen_ai.usage.total_tokens"])),
               total_latency_ms = sum(duration),
               span_count       = count()
   | extend est_cost_usd = round(total_tokens / 1000.0 * price_per_1k, 6)
   ```

**Success Criteria:**

- [ ] The starter query returns ≥1 row for your run.
- [ ] The correlation query returns **all** spans for one `operation_Id` in timestamp order (you can
      see model and retrieval, plus tool if attached).
- [ ] The summary query outputs `total_tokens`, `total_latency_ms`, and an `est_cost_usd` for the run.
- [ ] You save your final correlation query to
      `challenges/advanced-tracing-observability/correlate.kql`.

**Checkpoint:**

```bash
python validate.py --step 4
# expected: "✅ Step 4 PASS — correlate.kql present and returns end-to-end spans for one run"
```

> _Coach note: see solution.md._

---

## Rung (b) — Build-from-scratch path

> Stronger team? **Skip the pasted code.** We hand you only the contract and the one gotcha that
> actually bites. The **same `validate.py`** (it checks for ≥1 emitted GenAI span) grades this path.

**Your contract:**
> Emit GenAI spans to App Insights and reconstruct one question end to end. **Acceptance:** model +
> retrieval spans for one `operation_Id`, with token + latency, surfaced in the portal Tracing tab
> **and** a KQL query you wrote.

**The only help you get:**
- **The gotcha:** set the two tracing env flags **before any `azure.ai.*` import** (see the gotcha
  box in Step 1) or message content silently never appears on your spans.
- **The packages:** `azure-ai-projects`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`.
- **The three calls you'll need:** `configure_azure_monitor(...)`, `AIProjectInstrumentor().instrument()`,
  and resolving the App Insights connection string.

Assemble `trace_setup.py` + `traced_run.py` yourself, then answer five questions about one run:
tokens, latency-per-span, which span retrieved, an estimated cost, and the slowest hop.

---

## Done — what you can now do

- Every Northfield IQ answer is observable end to end, two ways: portal **Tracing** tab and **KQL**.
- You can take one student question and account for its model, retrieval, and tool spans, with tokens,
  latency, and an estimated cost.

**This unlocks:** Evaluation & Red Teaming (trace the exact row that failed an eval) and Deploy as a
Hosted Agent (the same tracing follows the agent to its live endpoint).

## Rung (c) — Stretch goals

Genuinely open-ended — no single right answer:

1. **3-tier `TelemetryManager` + a custom business metric.** Ship a small `TelemetryManager` and emit
   **one custom metric** (e.g. `northfield.answers.uncited`) on every run, then chart it in a Workbook.
2. **Batch-run + dashboard.** Fire 20 questions through the agent and build a KQL **timechart** of
   token cost across the run.

- Pin your three queries into an **Azure Workbook** so the team has a live observability dashboard.
- Add a `gen_ai.response.model` breakdown to compare token/latency profiles across models.
- Wire an App Insights **alert** that fires when p95 latency or total tokens per run crosses a threshold.

## Learning resources

- [Trace AI agents with OpenTelemetry (Foundry)](https://learn.microsoft.com/azure/ai-foundry/how-to/develop/trace-agents-sdk)
- [Azure Monitor OpenTelemetry for Python](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable?tabs=python)
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Kusto Query Language (KQL) reference](https://learn.microsoft.com/azure/data-explorer/kusto/query/)
