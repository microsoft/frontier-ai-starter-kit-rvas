# Capstone · Northfield IQ, the Team — Multi-Agent Orchestration with MAF

> Tier 3 · Capstone — the summit. ⏱ Core 2–2.5 hr (sequential + fan-out + DevUI + trace) ·
> +1 hr Magentic manager stretch · +1.5 hr hosted long-running deploy variant.
> ⭐⭐⭐⭐⭐ · Open-ended design brief — not a placeholder-fill.
>
> Prerequisites: the Foundations end-state (a deployed, grounded Northfield IQ Assistant)
> and the Advanced · Action Tools challenge (you reuse its approval loop). Tracing &
> Observability strongly recommended — Step 5 leans on it. Deploy as a Hosted Agent is required
> only for the hosted variant. Bootstrap skip-path if you skipped Foundations:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

You have built one Northfield IQ Assistant: it knows things (Foundations KB), it does things
(Action Tools), you can prove it safe (Eval), watch it (Tracing), and ship it (Deploy). This capstone
asks the question every real deployment eventually hits: what happens when one agent isn't enough?

You will break the monolith into a team — a triage/router that decides who handles a request,
specialist agents that each own one job, and a synthesizer that merges their work into one
cited, governed answer. You orchestrate them with the Microsoft Agent Framework (MAF) — the Oct-2025
SDK that merges Semantic Kernel + AutoGen into a code-first graph of agents.

This challenge is deliberately less guided. There is no starter file with `< PLACEHOLDER >` gaps to
fill. You get the org-chart sketch, two illustrative `WorkflowBuilder` snippets, the acceptance
criteria, and pointers to the skills + MCP. The design *is* the learning. You decide the org-chart;
you wire the graph.

> 🔎 Search-Before-Implement. Every MAF/SDK snippet below is illustrative. MAF is fast-moving
> and much of it is preview. Confirm the current class names, builder methods, and call shapes via
> the `microsoft-docs` MCP (and `foundry-mcp` for Foundry-native ops) before you code. Do not
> assume a memorized signature is still correct — load the `foundry-workflows` skill for the proven
> pattern, then verify the surface.

---

## Learning objectives

By the end, your team can:

1. Decompose a monolithic agent into specialist roles with explicit, non-overlapping
   responsibilities (the *role-as-agent* pattern).
2. Use MAF primitives — Executors, Edges, Workflows, Events — and the `WorkflowBuilder` to wire a
   graph of agents.
3. Build a sequential workflow first, then evolve it to parallel fan-out with a fan-in join.
4. Add a triage/router that *decides* which specialist(s) to invoke — the step beyond a static
   fan-out.
5. Pass typed (Pydantic) data contracts between agents instead of regex-parsing prose.
6. Visualize first in DevUI (green = done / purple = running / black = pending), then instrument
   with the OTel tracing you already learned — and confirm a multi-agent span tree.
7. *(Deploy variant)* Host the workflow as a long-running / background agent that keeps working
   after the tab is closed.

---

## The agent org-chart (role-as-agent)

The single Northfield IQ Assistant becomes a student-services desk team. Every box is a real role on
a real help desk — that is what makes "multi-agent orchestration" click. Each specialist reuses an
artifact you already built; the triage and escalation agents are new, small, tool-less reasoners.

```text
                         ┌──────────────────────────┐
            student ────▶│   TRIAGE / ROUTER agent   │   "what kind of request is this?"
            question     │   (classifier, no tools)  │   → routes to 1..N specialists
                         └─────────────┬─────────────┘
                       ┌───────────────┼────────────────┐
                       ▼               ▼                ▼
            ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐
            │ KNOWLEDGE agent │ │  ACTION agent   │ │  ESCALATION agent  │
            │ (AI Search /    │ │ (MCP tools +    │ │ (human-handoff;    │
            │  Foundry IQ KB) │ │  approval loop) │ │  out-of-scope)     │
            │  [Foundations]  │ │ [Action Tools]  │ │                    │
            └───────┬────────┘ └───────┬────────┘ └─────────┬──────────┘
                    └──────────────────┼────────────────────┘
                                       ▼
                         ┌──────────────────────────┐
                         │   SYNTHESIZER  (fan-in)   │  merges specialist outputs into
                         │                           │  one cited, governed answer
                         └──────────────────────────┘
```

Reuse, don't rebuild:

| Agent | What it is | Where it comes from |
|---|---|---|
| Triage / Router | A tool-less reasoner that classifies the request and emits a typed routing decision | New — small prompt-only agent |
| Knowledge specialist | The grounded, citing agent from Foundations | Reuse the Foundations KB agent (AI Search / Foundry IQ) |
| Action specialist | The MCP-tool agent with the human-approval loop | Reuse the Advanced · Action Tools agent + its approval loop |
| Escalation | A tool-less reasoner that produces a clean human-handoff for out-of-scope requests | New — small prompt-only agent |
| Synthesizer | A fan-in agent that merges specialist outputs into one cited, governed answer | New — small prompt-only agent |

---

## The build, in two passes

You will build the graph twice — sequential first to warm up, then fan-out for the real topology.
Both snippets are illustrative; confirm the current MAF surface via `microsoft-docs` MCP first.

### Pass 1 — sequential (warm-up)

Chain Triage → Knowledge → Synthesizer with explicit edges. Prove one question flows end-to-end before
you add concurrency.

```python
# illustrative — confirm current MAF surface via microsoft-docs MCP before coding
WorkflowBuilder()
  .set_start_executor(triage_executor)
  .add_edge(triage_executor, knowledge_executor)
  .add_edge(knowledge_executor, synthesizer_executor)
  .build()
```

### Pass 2 — parallel fan-out + fan-in

Triage fans out to Knowledge and Action concurrently; both converge on the Synthesizer (fan-in).

```python
# illustrative — confirm current MAF surface via microsoft-docs MCP before coding
WorkflowBuilder()
  .set_start_executor(triage_executor)
  .add_edge(triage_executor, knowledge_executor)       # fan-out
  .add_edge(triage_executor, action_executor)          # fan-out
  .add_edge(knowledge_executor, synthesizer_executor)  # fan-in
  .add_edge(action_executor,    synthesizer_executor)  # fan-in
  .build()
```

Typed contracts, end-to-end. Executors pass typed Pydantic messages (e.g.
`await ctx.send_message(result)`); the terminal executor emits via `await ctx.yield_output(result)`.
No regex-parsing of prose between hops — define a Pydantic model for the routing decision, for each
specialist's output, and for the final synthesized answer. This is a graded criterion.

> Stretch — Magentic manager/planner. Replace the hand-wired Triage edges with a MAF Magentic
> manager that *plans dynamically* which specialists to call per request. This is exactly what the
> Magentic Workflows Extra scaffolds — fold it in here. Confirm the manager/planner surface via
> `microsoft-docs` MCP and the `foundry-workflows` skill.

---

## Visual-first, then traced

1. DevUI first. Launch the workflow in MAF's DevUI and *watch* the graph light up as a question
   flows through (green = done, purple = running, black = pending). Build intuition before rigor — you
   should be able to *see* the fan-out happen and the fan-in wait for both branches.
2. Then instrument. Turn on the OTel GenAI tracing from the Tracing & Observability challenge
   (set the env flags above all `azure.ai.*` imports). Re-run one question and confirm you now get a
   multi-span tree across agents — triage → fan-out → fan-in — correlated by `operation_Id`. The
   capstone is where Tracing pays off: roughly *N spans per question across the team*, not one.

---

## Make it your own (scenario swap)

The agent-graph shape here is identical for almost any help-desk-shaped domain — only the corpus,
the specialist prompts, the action tools, and the eval set change. Reskinning the capstone
for your own domain (insurance, factory ops, retail, …) is exactly what the
[Customer Build Track — Grow It Into a Team](challenge.html?id=customer-capstone-multi-agent)
chapter walks you through, decision by decision. Build the Northfield version below first; it is the
known-good reference the customer chapter links back to.

---

## Reuse the existing `.env` contract — invent nothing

This challenge uses only variables already defined in [`.env.sample`](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.env.sample). Do not
add new env vars by hand. If the hosted long-running variant needs anything new, it comes from
Livingston via Bicep outputs — never hand-edited into `.env.sample`.

| Variable | Used by |
|---|---|
| `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_FOUNDRY_AGENT_NAME` | every agent (model + project) |
| `AZURE_SEARCH_*`, `AZURE_SEARCH_INDEX_NAME=university-faq` | Knowledge specialist (grounding) |
| `ACTION_API_URL=http://localhost:8080`, `ACTION_MCP_URL=http://localhost:8765/mcp`, `ACTION_API_KEY` *(empty)*; `server_label=northfield_actions` | Action specialist (MCP + approval loop) |
| `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` | the trace step |

---

## Acceptance criteria (graded — no step-by-step)

Your submission passes if all of these are demonstrably true. You show it; a light `validate.py`
(authored by the QA harness) checks the structural ones headlessly.

- [ ] ≥ 3 agents with distinct roles, at least one router/triage that *decides* routing and at
      least two specialists.
- [ ] The workflow runs both a sequential and a parallel fan-out topology (show both graphs).
- [ ] Typed Pydantic contracts flow between agents — no free-text regex parsing between hops.
- [ ] At least one specialist reuses the Foundations KB (grounded, cited) and one reuses the
      Action Tools approval loop (governed).
- [ ] The run is visualized in DevUI and traced end-to-end (a multi-agent span tree by
      `operation_Id`).
- [ ] A 2-minute demo narrates one question's journey through the team.
- [ ] *(Stretch / deploy variant)* the workflow is hosted with a background / long-running run
      that completes after the tab is closed.

> Guidance level is intentionally LOW. We give the org-chart sketch, the two `WorkflowBuilder`
> snippets, the acceptance criteria, and pointers to the skills + MCP — not a placeholder file. The
> learning *is* the design and wiring. This is the autonomy payoff of the curriculum tree.

**Checkpoint:** `validate.py` (in-repo at `challenges/capstone-multi-agent/validate.py`) asserts the structural subset of
the criteria above — ≥ 3 agents defined, a fan-out edge present, and typed (Pydantic) contracts in use.
The non-structural criteria (DevUI visual, the 2-minute demo, the hosted background run) are confirmed
live with your coach.

```text
# structural subset of the acceptance criteria
python validate.py --all
# expected: "✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use"
```

---

## Learning Resources
- [Microsoft Agent Framework (MAF) overview](https://learn.microsoft.com/azure/foundry/agents/)
- [`foundry-workflows` skill](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/foundry-workflows/SKILL.md) — Magentic + workflow patterns
- [Advanced · Action Tools](challenge.html?id=advanced-action-tools) — the approval loop you reuse
- [Advanced · Tracing & Observability](challenge.html?id=advanced-tracing-observability) — the OTel setup for Step 5
- [Advanced · Deploy as a Hosted Agent](challenge.html?id=advanced-deploy-hosted-agent) — the hosted variant
- [Extra · Magentic Workflows](challenge.html?id=extra-magentic-workflows) — the Magentic manager stretch
- [Extra · Hosted Long-Running](challenge.html?id=extra-hosted-longrunning) — the background-run deploy variant

## Tips
- Design before you wire. Sketch the org-chart and the Pydantic contracts on paper first. The graph
  is easy once the roles and the message types are clear.
- Sequential before parallel, always. Get one question through Triage → Knowledge → Synthesizer
  before you add the Action branch and the fan-in. Concurrency hides bugs.
- Typed contracts beat regex. If you find yourself parsing the previous agent's prose with a regex,
  stop — define a Pydantic model and pass it. This is graded *and* it's the thing that makes the system
  maintainable.
- DevUI is your debugger. If a branch never lights up, your triage didn't route to it. If the
  synthesizer fires before both branches finish, your fan-in edges are wrong.
- Set the trace env flags before importing the SDK — same gotcha as the Tracing challenge. Flags set
  after the first `azure.ai.*` import are silently ignored.
- Reuse means reuse. The Knowledge and Action agents already work. Wrap them as executors — don't
  reimplement grounding or the approval loop.
