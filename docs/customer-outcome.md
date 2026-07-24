---
title: "Define Your Outcome"
parent: Customer Build Track
nav_order: 1
---

# Customer Build · Define your outcome

{% include journey-status.html tone="customer" path="Customer Build Track" artifact="One evolving scenario record: outcome, owners, data, boundaries, evidence, and the next decision." next="Use this record throughout the journey. Each chapter adds evidence for the next customer decision." %}

This is the first task in the Customer Build Track. Start it here, then update the same record
from Foundations through deployment. It is not a compliance pack: it is the short shared record
that lets the customer decide what is safe to build, test, pilot, and eventually operate.

> First, what is "Northfield"? Throughout this track you'll see *Northfield* used as the
> reference scenario: a student-services assistant for the fictional *Northfield University*,
> grounded in a public [university-FAQ corpus]({{ '/activities/foundations' | relative_url }}). The
> base [Foundations track]({{ '/activities/foundations' | relative_url }}) builds it step by step, so
> its steps double as worked examples you can copy the exact commands from. Customer Build keeps
> Northfield's mechanics and swaps in your own corpus, persona, and questions — you do not need to
> build the Northfield version first. When a step says "follow the Northfield reference," that's the
> place to grab the commands, not a prerequisite you must have finished.

If you arrived from [Idea Forge]({{ '/idea-forge' | relative_url }}), transfer the selected idea's business outcome, users, data sources, tier guidance, and risk notes into the table below.

## Scenario pack

| Field | Prompt |
|---|---|
| Customer / business area | Which team, process, or account is this for? |
| Owners | Who owns the business outcome, the technical build, and the source data? Name people or roles. |
| Target users and access | Who will use the assistant, and who should not? Note employees, customers, operators, or other audiences and any access assumptions. |
| Business outcome | What should be faster, safer, cheaper, or more reliable after the prototype works? |
| Top user tasks | What are the top 3 questions or workflows users need help with? |
| Knowledge sources and access | Which approved documents, FAQs, policies, manuals, tickets, pages, APIs, or operational datasets are relevant? Who owns them, who may see them, and who keeps them current? *(Use corpus prep guidance below only when the selected path needs document grounding.)* |
| Action candidates | What may the agent do? For each meaningful action, who may request it, approve it, or must receive an escalation? |
| Safety boundaries | What must the agent refuse, escalate, redact, or never automate? What failure would be unacceptable even if other results look good? |
| Success measures | What evidence would make stakeholders trust the prototype? Separate useful quality measures from failures that must block a pilot. |
| Operating assumptions | Where will it run, who can view traces or logs, and who investigates a bad answer or failed action? Record assumptions now; refine them in later chapters. |
| Final demo and next decision | What short scenario proves the outcome, and what decision should the customer make after seeing the evidence: build, test, pilot, harden, or stop? |

## Decision checkpoints

Use these checkpoints to keep the engagement moving. A decision can be **yes**, **not yet**, or
**change the scope**. Capture the reason in the scenario record; do not create a separate document.

| Checkpoint | Decision | Evidence from the journey |
|---|---|---|
| Before building | Is the outcome bounded enough to build safely? | Owners, intended users, approved data, safety boundaries, and a narrow first outcome |
| Before intended-user testing | Is the core capability and access model ready to test? | Cited answers or live-data proof where applicable, action approval behavior where applicable, source ownership, and data/access assumptions |
| Before a controlled pilot | Is the action, behavior, and operating plan understood well enough to expose it? | Approval policy, evaluation and red-team results, trace-data decision, support owner, and known risks |
| Before broader release | Should we launch, harden first, or remain demo-only? | Hosted deployment evidence, caller/agent permissions, rollback path, service signals, and residual gaps |

### Preparing your corpus for Foundations Step 4

When filling in Knowledge sources, use these guidelines to avoid the most common corpus problems:

- Minimum useful size: 5–20 well-structured documents (FAQs, policy pages, SOPs, product guides)
  is enough for a compelling session demo. A sparse corpus produces "I don't know" answers even on
  questions the assistant should handle.
- Safe data only: no PII, unredacted customer data, confidential pricing, or legal content that
  has not been cleared for use in a demo environment. When in doubt, use public-facing or
  pre-approved summaries.
- State the access assumption: who is allowed to read each source, whether the prototype can
  enforce that boundary yet, and who approves a source change. A citation shows where an answer
  came from; it does not prove every viewer was entitled to see the source.
- Supported formats: the indexing step you'll build in Foundations Step 4 (following the
  Northfield reference, pointed at *your* files) reads Markdown (`.md`) and plain text (`.txt`)
  directly. For PDFs, extract text first — `pypdf` is fast enough for session use; Azure Document
  Intelligence gives higher quality for complex layouts.
- PDFs / SharePoint: the Foundry portal's Build → Indexes → Add data flow can ingest PDFs
  and SharePoint pages without writing code — a good option if the team is comfortable with portal
  navigation and wants to move quickly.
- Northfield as fallback: if customer data is not cleared or not ready by event day, complete
  Foundations with the Northfield University corpus and capture the corpus swap as a follow-up task.
  The indexing architecture, agent wiring, and grounding pattern are identical regardless of which
  corpus you use — Northfield is the reference, not a ceiling.

## Map the path to the customer outcome

Choose an application path after this page. It links the canonical sessions below without copying
them; do not force a RAG build onto an app whose value is action, live data, voice, or orchestration.

| Capability | Build activity | Customer proof point |
|---|---|---|
| Shared agent baseline | Provision Foundry, choose a model, create an agent, and define guardrails | The team has a bounded, owned agent contract |
| Knowledge, action, data, voice, or orchestration | Select the route-specific canonical session(s) | The primary outcome works with the right source, interface, or workflow control |
| Evaluation & Red Teaming | Create scenario-specific eval and adversarial prompts | The team can show task quality, safety, and critical-failure behavior |
| Tracing & Observability | Instrument the run and inspect spans in App Insights | The team can explain latency, retrieval, tool calls, handoffs, and failure paths |
| Deploy / UI | Host the agent and expose a stakeholder-facing experience | A non-technical stakeholder can test the relevant proof point |

## Scenario swap guide

Northfield gives you the reference shape:

| Northfield artifact | Customer Build replacement |
|---|---|
| University FAQ corpus | Customer-safe domain corpus |
| Student-services persona | Target-user assistant persona |
| Admissions, financial aid, housing topics | Customer-specific intents and support areas |
| IT ticket / course hold / advising actions | One or more real workflow actions, usually approval-gated |
| Student safety and academic-integrity refusals | Domain-specific safety, compliance, and escalation rules |
| Northfield eval prompts | Customer scenario eval and red-team prompts |

Keep the shape; swap the content. If the customer does not have safe data ready, run Northfield first
and capture the customer scenario as follow-up work.

## Engagement deliverable

By the end of the engagement, the scenario record should support one clear recommendation:

1. **Launch a controlled pilot** — the bounded use case, owners, evidence, and operating plan are sufficient.
2. **Harden first** — the prototype is valuable, but named gaps must be closed before intended users rely on it.
3. **Remain demo-only or stop** — the evidence does not yet support a pilot, or the use case should change.

The supporting evidence stays lightweight: the grounded demo, scorecard, action-policy decisions,
trace/operating notes, and a short list of residual risks and next actions.

## Facilitator prompts

- What business decision or workflow improves if this prototype works?
- Which source of truth should the agent cite before anyone trusts the answer?
- Which action is valuable enough to automate but risky enough to require approval?
- What would make the customer say, "Yes, this is worth piloting"?
- What will you show in two minutes that proves the outcome, not just the technology?

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/customer-build' | relative_url }}">Choose your application path</a>
</div>
