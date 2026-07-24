# Facilitator Guide · Capstone — Northfield IQ, the Team

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> **Facilitator-only.** This is the **lowest-guidance** activity in the curriculum **by design** — there is
> no starter file and no PLACEHOLDER moments. Your job is **not** to hand out a reference graph; it is
> to keep teams unblocked while they design it themselves. Resist the urge to paste the solution. The
> design *is* the learning.

## What this activity is really teaching

Tiers 1–2 prove a team can build **one** agent and make it act, prove it safe, observe it, and ship it.
The capstone proves they can **compose** — the actual shape of production agentic systems. The leap is
from "an agent" to "an org-chart of agents": role decomposition, a **router that decides**, **typed
contracts** between hops, **fan-out/fan-in** concurrency, and **visual-first then traced** debugging.
Neither reference repo (FrontierWeekHack, azure-trust-agents) hands the org-chart to the learner — ATA
ships a *fixed* fan-out, FWH a *fixed* portal DAG. The open-endedness is the point.

> ⚠️ **Search-Before-Implement is a facilitator-enforced rule here.** The `WorkflowBuilder` method
> names, executor/context API, and Magentic manager class
> **drift between versions.** All code in this guide is **illustrative**. Send teams to `microsoft-docs`
> MCP and the `foundry-workflows` skill to confirm the current surface — do **not** let them (or you)
> treat these snippets as pinned fact.

## The reference org-chart (for your eyes — don't hand it out)

```text
            student ─▶ TRIAGE/ROUTER (tool-less classifier, emits typed RouteDecision)
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        KNOWLEDGE     ACTION      ESCALATION
        (Foundations  (Action     (tool-less
         KB agent)     Tools +     handoff)
                       approval)
              └───────────┼───────────┘
                          ▼
                     SYNTHESIZER (fan-in → one cited, governed answer)
```

- **Triage / Router** — new, tool-less. Classifies the request and emits a **typed** routing decision
  (which specialists, why). This is the "decides routing" criterion — a hard-coded `if` is *not* a
  router; the classification must come from the model.
- **Knowledge specialist** — **reuse the Foundations KB agent** verbatim, wrapped as an executor. It
  already grounds + cites. Do not let teams reimplement RAG.
- **Action specialist** — **reuse the Action Tools agent + approval loop** verbatim, wrapped as an
  executor. The human-approval gate must survive the wrap.
- **Escalation** — new, tool-less. Produces a clean human-handoff for out-of-scope requests.
- **Synthesizer** — new, fan-in. Merges specialist outputs into one cited, governed answer.

## The sequential → fan-out evolution (the heart of the build)

Insist teams build it **twice**. Sequential first is not busywork — it isolates the agent-wrapping and
the typed contracts from the concurrency, so when fan-out breaks they know it's the edges, not the
agents.

**Pass 1 — sequential** (illustrative; confirm surface via MCP):

```python
WorkflowBuilder(start_executor=triage_executor) \
  .add_edge(triage_executor, knowledge_executor) \
  .add_edge(knowledge_executor, synthesizer_executor) \
  .build()
```

**Pass 2 — fan-out + fan-in** (illustrative):

```python
WorkflowBuilder(start_executor=triage_executor) \
  .add_edge(triage_executor, knowledge_executor) \
  .add_edge(triage_executor, action_executor) \
  .add_fan_in_edges([knowledge_executor, action_executor], synthesizer_executor) \
  .build()
```

## Typed Pydantic contracts (the criterion teams most often skip)

The graded line is **"no free-text regex parsing between hops."** Push teams to define a model for each
message type *before* they wire anything:

```python
# illustrative — types/shape will differ; confirm executor/context API via MCP
from pydantic import BaseModel

class RouteDecision(BaseModel):
    needs_knowledge: bool
    needs_action: bool
    escalate: bool
    rationale: str

class SpecialistResult(BaseModel):
    source: str            # "knowledge" | "action" | "escalation"
    content: str
    citations: list[str] = []

class FinalAnswer(BaseModel):
    answer: str
    citations: list[str]
    actions_taken: list[str] = []
```

Executors `await ctx.send_message(typed_obj)` to pass these along; the terminal Synthesizer
`await ctx.yield_output(final)`. If you see a team running `re.search(...)` on the previous agent's
prose, that's the intervention moment — it's both the graded criterion and the maintainability lesson.

## DevUI launch (visual-first)

Have them launch the workflow in MAF's **DevUI** *before* tracing. Create a local
`devui_launcher.py` using the directory-based pattern from the Magentic Extra. The win is watching
workflow state and events change. UI colors and labels can change between DevUI releases. Facilitation
cue: ask *"why is the synthesizer still waiting?"* — the answer (it is waiting on both fan-in branches)
is the concurrency lesson made visible.

```bash
# illustrative — confirm current launcher entrypoint via the foundry-workflows skill / MCP
python devui_launcher.py        # serves the workflow graph in the browser
```

## The trace check (where Tracing pays off)

After DevUI, turn on the OTel GenAI tracing from the Tracing activity and re-run one question.

- **Env flags must be set above all `azure.ai.*` imports** — same gotcha as the Tracing activity.
  Flags set after the first import are silently ignored and they'll see *zero* spans.
- Success = a **multi-span tree across agents**: triage → fan-out (knowledge + action in parallel) →
  fan-in (synthesizer), all sharing one `operation_Id`. Contrast with the single-agent run from the
  Tracing activity — the capstone is ~N spans per question, not one.
- Good debrief question: *"In the trace, can you see the two fan-out branches running concurrently?
  How do you know?"*

## Stretch variants

### Magentic manager/planner

Replace the hand-wired Triage edges with a MAF **Magentic manager** that plans dynamically which
specialists to call. This is exactly what `extra-magentic-workflows` scaffolds — point teams there.
**Confirm the manager/planner class via `microsoft-docs` MCP** (it has drifted across MAF previews).
Common failure: teams expect the manager to "just work" — it still needs the specialists registered and
typed contracts; the manager replaces the *routing edges*, not the agents.

### Hosted long-running deploy variant

Host the workflow as a **background / long-running** agent (the `extra-hosted-longrunning` content,
which is the Deploy activity's async variant). The criterion is a run that **completes after the tab is
closed**. Prereqs stack here: Deploy **and** the workflow itself — flag this as a two-prereq, capstone-
only path. Reuse the `.env` contract; any new hosted var comes from Livingston's Bicep outputs, never a
hand-edit.

## Common failure modes (the async / DevUI / import-order gotchas)

| Symptom | Cause | Fix |
|---|---|---|
| **Zero spans in App Insights** | Trace env flags set *after* an `azure.ai.*` import | Move `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING` etc. to the very top, before any SDK import |
| **`RuntimeError: event loop is already running`** | Mixing `asyncio.run()` inside an already-async DevUI / notebook context | Use `await` on the workflow run; don't nest event loops. In notebooks, `await` directly |
| **A fan-out branch never lights up in DevUI** | Triage didn't route to it (or the edge is missing) | Inspect the typed `RouteDecision`; check the `add_edge` for that branch |
| **Synthesizer fires before both branches finish** | Fan-in modeled as two separate sinks, not a join | Both specialist edges must target the *same* synthesizer executor |
| **Regex-parsing prose between agents** | Skipped the typed-contract step | Define Pydantic models per hop; `send_message` the object, not a string |
| **Approval loop lost after wrapping the Action agent** | Re-implemented the agent instead of reusing it | Wrap the existing Action Tools agent as an executor; keep its Responses approval loop intact |
| **`AttributeError` on a `WorkflowBuilder` method** | Memorized a stale MAF signature | Confirm the current builder surface via `microsoft-docs` MCP — it drifts between previews |
| **Model "router" is actually a hard-coded `if`** | Misread "router" as branching logic | The routing decision must come from the model and be a typed output |

## Facilitation notes — reconvene points

This is a long, open activity. Don't let teams disappear for 2.5 hr. Set explicit reconvene checkpoints:

1. **~20 min in — design review (whole room).** Each team shows their org-chart sketch + Pydantic
   contracts on paper *before* coding. Catch over-engineering (5+ agents) and under-specified contracts
   here — it's cheap to fix on paper.
2. **~60 min — sequential working.** Every team should have Triage → Knowledge → Synthesizer passing one
   question end-to-end. If a team is still fighting agent-wrapping, pair them with one that's through.
3. **~90 min — fan-out + DevUI.** Teams show the graph lighting up with the parallel branches. This is
   the "aha" moment — make it visible to the room.
4. **~120 min — trace + 2-min demo dry-run.** Confirm the multi-span tree, then each team rehearses the
   2-minute narration of one question's journey.
5. **Stretch reconvene (optional).** Magentic and/or hosted variant — only for teams who cleared the
   core with time to spare.

## Timing

| Segment | Time |
|---|---|
| Design review (org-chart + contracts on paper) | 0–20 min |
| Sequential workflow working | 20–60 min |
| Fan-out + fan-in + DevUI | 60–90 min |
| Trace + 2-minute demo prep | 90–120 min |
| **Core total** | **2–2.5 hr** |
| Magentic manager stretch | +1 hr |
| Hosted long-running deploy variant | +1.5 hr |

## Debrief questions

- "Walk me through one question's journey — which agents fired, in what order, and why?"
- "Show me a typed contract between two agents. What breaks if you pass a string instead?"
- "In DevUI, point to the moment the fan-out happens. In the trace, show me the same moment."
- "Which agent is the router, and how does it *decide* — not branch — where to route?"
- "If you reskinned this to insurance claims, what changes and what stays identical?" (the
  graph-shape-is-portable insight)
- "Where would a hosted long-running run help a real student-services desk?" (bridge to deploy variant)

## Checkpoint / validate.py contract

A light `validate.py` (authored by the QA harness, not in this folder yet) asserts the **structural
subset** of the §3.7 acceptance criteria — the headless-checkable ones:

- **≥ 3 agents** defined with distinct roles, including at least one router/triage and ≥ 2 specialists.
- A **parallel fan-out edge** is present in the workflow definition (triage → two specialists).
- **Typed (Pydantic) contracts** are in use between executors (no free-text-only message passing).

```text
python activities/capstone-multi-agent/validate.py --all
# expected: "✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use"
```

The **non-structural** criteria are confirmed **live with you**: the DevUI visual, the end-to-end
multi-agent trace, the 2-minute demo narration, and (for the variant) the hosted background run that
survives a closed tab. Sign those off by observation — they are not statically assertable.
