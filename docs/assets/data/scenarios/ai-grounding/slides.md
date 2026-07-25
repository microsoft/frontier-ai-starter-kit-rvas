---
marp: true
theme: default
paginate: true
title: "AI Grounding / IQ — Customer Discussion Deck"
version: "1.0.0"
footer: "Customer Delivery · AI Grounding / IQ"
---
<!-- slide:id=scenario-open -->

# AI Grounding / IQ
## Choose trusted context for one customer decision

This deck guides a customer conversation about where answers should come from, who is allowed to see them, how retrieval is proven, and what evidence is needed before a pilot ships.

**Workshop outcome:** select a governed context pattern, access boundary, evaluation plan, and operating evidence for a bounded AI-assisted decision.

---
<!-- slide:id=scenario-intro -->

# How to use this conversation

We are not designing a complete enterprise platform today. We are choosing the smallest useful scenario that can be grounded, evaluated, and operated safely.

Discuss each lesson through three lenses:

| Lens | Customer question |
|---|---|
| Context | What decision are we improving, and what constraints matter? |
| Choices | Which path fits the source, access model, and experience? |
| Evidence | What must be true before we move on? |

Keep implementation details in the lesson and activity pages.

---
<!-- slide:id=lesson-foundation-context -->

# Lesson 1 context: provision the grounding foundation

Before content enters the pilot, agree the technical foundation that will hold it.

Customer discussion prompts:

- Which business decision or action needs trusted context?
- Which environment will host the pilot, and who owns it?
- Which region, identity model, logging boundary, and data handling expectations apply?
- Which model and retrieval capabilities must be available in that environment?

**Principle:** foundation choices should protect the source of truth before they optimize developer convenience.

---
<!-- slide:id=lesson-foundation-choices -->

# Lesson 1 choices: shared foundation or existing landing zone?

| Choice | When it fits | Trade-off |
|---|---|---|
| Scenario-provisioned foundation | Fast pilot with clear defaults | Customer still needs operational ownership |
| Existing Azure landing zone | Enterprise controls are already in place | More dependency on customer platform teams |
| Portal-led setup | Early orientation or stakeholder demo | Harder to reproduce without a written contract |
| Bring-your-own resources | Customer already has Foundry, search, and monitoring | Must prove configuration matches the pilot needs |

Discuss identity, network boundaries, observability, and regional capacity before discussing content ingestion.

---
<!-- slide:id=lesson-foundation-evidence -->

# Lesson 1 evidence/checkpoint: foundation is ready for content

Move forward when the team can show:

- A named environment owner and service owner
- Keyless-first access plan for people and workload identities
- Model and retrieval capabilities available in the chosen region
- Monitoring and trace destination identified before pilot traffic
- Environment values documented as a reusable contract, without secrets

**Checkpoint decision:** the foundation is safe enough to connect approved pilot content.

---
<!-- slide:id=lesson-source-selection-context -->

# Lesson 2 context: select the source and permission architecture

Grounding starts with source ownership, not with a search box.

Ask the customer:

- Which system remains the source of truth?
- Who owns content quality, retention, and retirement?
- Which users may see which records, and why?
- Is permission trimming needed at retrieval time, answer time, or both?
- What happens when content is missing, conflicting, or restricted?

**Non-negotiable:** no source enters the pilot without an owner and an access decision.

---
<!-- slide:id=lesson-source-selection-choices -->

# Lesson 2 choices: match IQ and source patterns to the work

| Pattern | Best fit | Watch for |
|---|---|---|
| Copilot Studio + SharePoint | M365 workflow over governed SharePoint content | Limited need for custom orchestration |
| Foundry IQ | Custom app or agent needing managed grounding over approved knowledge | Confirm source support, region, and permissions |
| Azure AI Search | Custom indexing, scoring, or retrieval control | You own more ingestion and access behavior |
| Fabric IQ | Analytical facts, measures, and business semantics | Keep metrics aligned to governed data products |
| Work IQ | Microsoft 365 collaboration and work context | Respect user-scoped permissions and privacy |
| Web IQ | Curated public information with attribution | Treat as external context, not the system of record |

---
<!-- slide:id=lesson-source-selection-evidence -->

# Lesson 2 evidence/checkpoint: signed source and access decision

The source decision is ready when it records:

- Approved source or sources, with business owner and steward
- Source-of-truth statement and freshness expectation
- Permission model, including restricted and access-denied cases
- Citation, provenance, and audit expectations
- Boundary between governed internal knowledge, live work data, analytics, and public information

**Checkpoint decision:** the pilot has a defensible source architecture before anything is indexed.

---
<!-- slide:id=lesson-ingestion-context -->

# Lesson 3 context: ingest and index approved content

Ingestion is not just moving files. It preserves the evidence needed to trust an answer.

Discuss:

- Which approved content is small enough for the pilot but representative enough to test?
- What metadata must survive ingestion: source, version, owner, date, sensitivity, access group?
- How will stale, duplicate, superseded, and conflicting documents be handled?
- Which content should stay remote rather than copied?

**Goal:** retrieve the right passage with the right provenance for the right user.

---
<!-- slide:id=lesson-ingestion-choices -->

# Lesson 3 choices: managed, custom, or remote knowledge

| Choice | Use when | Trade-off |
|---|---|---|
| Foundry IQ managed ingestion | The platform-supported source pattern fits | Less custom control, more managed behavior |
| Azure AI Search indexer | Source can be pulled on a schedule | Indexer limits shape metadata and enrichment options |
| Push indexing | Custom chunking, enrichment, or source pipeline is required | Team owns more code and operational failure modes |
| Content preprocessing | Documents need extraction, layout, or structure first | Adds another quality gate before retrieval |
| Remote knowledge source | Content should remain in place | Availability and permissions depend on the remote system |

Do not copy content just to make retrieval architecture look simpler.

---
<!-- slide:id=lesson-ingestion-evidence -->

# Lesson 3 evidence/checkpoint: approved documents are discoverable

Before moving on, reviewers should see:

- Representative pilot corpus indexed or connected
- Required source metadata visible in retrieval results
- Permission-sensitive examples behaving as designed
- Golden questions returning plausible source passages
- Known stale or conflicting content labeled and handled

**Checkpoint decision:** the knowledge layer can produce trustworthy retrieval evidence before answer generation is judged.

---
<!-- slide:id=lesson-model-selection-context -->

# Lesson 4 context: compare chat and embedding choices

Model choice matters, but it should be judged through the grounding task.

Discuss what the pilot needs from:

- The chat or query-planning model: reasoning, instruction following, latency, cost, region, and safety behavior
- The embedding model: retrieval quality for the customer’s vocabulary, abbreviations, and document style
- Capacity: expected users, peaks, and whether throughput should be reserved or consumption-based

**Principle:** pick models by evidence on the golden dataset, not by reputation alone.

---
<!-- slide:id=lesson-model-selection-choices -->

# Lesson 4 choices: quality, latency, cost, and capacity

| Decision | Customer trade-off |
|---|---|
| Larger chat model | May improve reasoning, but can increase latency and cost |
| Smaller chat model | May be faster and cheaper, but needs proof on hard cases |
| Embedding candidate | Must improve retrieval for this corpus, not just benchmark well |
| Regional deployment | Keeps data and latency aligned, but may constrain availability |
| Pay-as-you-go | Flexible for pilots, with variable throughput |
| Provisioned throughput | Predictable capacity, with stronger planning commitment |

Keep access control and citation requirements out of the trade space; they are baseline obligations.

---
<!-- slide:id=lesson-model-selection-evidence -->

# Lesson 4 evidence/checkpoint: model decision supports grounded answers

A model choice is ready when the team has compared:

- Retrieval hit quality on golden questions
- Answer usefulness with citations and abstention behavior
- Latency and cost under expected pilot usage
- Region and quota feasibility
- Failure behavior on ambiguous, stale, or restricted questions

**Checkpoint decision:** the selected model and embedding path are good enough for the pilot’s decision quality and operating constraints.

---
<!-- slide:id=lesson-grounded-app-context -->

# Lesson 5 context: build retrieval before adding an agent

A grounded experience should prove retrieval before orchestration becomes more complex.

Customer discussion prompts:

- Can the system find the right source passage for the user’s question?
- Does the answer cite the source and avoid unsupported claims?
- What should happen when evidence is weak, missing, stale, or access denied?
- Which user action is safe after the answer is shown?

**Design stance:** retrieval, citations, abstention, and recency come before agent behavior.

---
<!-- slide:id=lesson-grounded-app-choices -->

# Lesson 5 choices: answer synthesis or extractive retrieval?

| Choice | When it fits | Trade-off |
|---|---|---|
| Knowledge-base answer synthesis | Managed grounding can produce useful cited answers | Less direct control over answer construction |
| Extractive retrieval plus custom prompt | Team needs stronger control over tone and policy | More prompt and evaluation ownership |
| Direct hybrid query | App needs transparent retrieval and custom ranking | More engineering effort before user value |

Discuss three required behaviors explicitly: cite when evidence exists, abstain when it does not, and separate “not found” from “not allowed.”

---
<!-- slide:id=lesson-grounded-app-evidence -->

# Lesson 5 evidence/checkpoint: retrieval is trustworthy enough to use

The grounded app is ready for the next step when:

- Golden questions return relevant sources with provenance
- Answers quote or summarize only supported evidence
- Access-denied cases do not leak restricted content
- Stale-source cases trigger the agreed warning or refusal
- Reviewers can explain why an answer was accepted or rejected

**Checkpoint decision:** add an agent only if orchestration would solve a real customer need that retrieval alone does not.

---
<!-- slide:id=lesson-agent-routing-context -->

# Lesson 6 context: add agent and live-data routing only when justified

Agents and tools are useful when the experience needs planning, source routing, or action boundaries. They are not a shortcut around unclear knowledge architecture.

Discuss:

- Which requests should use policy knowledge, analytics, work context, public information, or live operational data?
- Which source is authoritative for each request type?
- Which live-data calls are safe, necessary, and auditable?
- What must the agent refuse or route away from?

**Boundary:** live data complements the source of truth; it does not silently replace it.

---
<!-- slide:id=lesson-agent-routing-choices -->

# Lesson 6 choices: route sources with clear rules

| Choice | Use when | Trade-off |
|---|---|---|
| Foundry agent with knowledge tool | The experience needs orchestration over approved knowledge | Requires explicit instructions and routing tests |
| Multi-source knowledge routing | Several governed knowledge sets answer different intents | Source boundaries must be visible and testable |
| Live-data tool | A real-time status, inventory, case, or transaction check is required | Tool reliability, permissions, and audit become part of the pilot |
| Multi-agent workflow | Distinct roles need separate responsibilities | More moving parts and harder evaluation |

Prefer the simplest route that preserves source authority and user trust.

---
<!-- slide:id=lesson-agent-routing-evidence -->

# Lesson 6 evidence/checkpoint: routing is explainable and controlled

Routing is ready when the team can show:

- Test questions for each source boundary
- Correct route chosen for policy, analytical, work-context, web, and live-data cases
- Refusal or escalation for unsupported requests
- No live-data call without a justified real-time need
- Trace or log evidence that shows which source answered

**Checkpoint decision:** the agent can be evaluated as a controlled router, not a black box.

---
<!-- slide:id=lesson-prove-and-ship-context -->

# Lesson 7 context: evaluate, trace, deploy, and operate

The pilot should ship only when evidence supports a responsible release decision.

Discuss:

- Which golden questions represent normal, edge, stale, restricted, and adversarial cases?
- Who reviews correctness, citations, access behavior, and business usefulness?
- What traces are needed to investigate failures without exposing unnecessary sensitive content?
- What operating rhythm keeps source, model, and permission changes under control?

**Operating mindset:** grounded AI is a service with evidence, owners, and change management.

---
<!-- slide:id=lesson-prove-and-ship-choices -->

# Lesson 7 choices: release gate and operating evidence

| Decision | Customer trade-off |
|---|---|
| Strict evaluation gate | Slower release, stronger trust for high-impact decisions |
| Phased pilot gate | Faster learning, with narrower scope and clear limits |
| Trace detail | Better troubleshooting, balanced against privacy and retention |
| Continuous evaluation | Better drift detection, with ongoing reviewer commitment |
| Manual review | Higher judgment quality, but limited scale |
| Automated checks | Better repeatability, but must be calibrated against human review |

Do not treat launch as the finish line; source changes can break grounding after release.

---
<!-- slide:id=lesson-prove-and-ship-evidence -->

# Lesson 7 evidence/checkpoint: pilot release decision

A release decision should include:

- Golden-set results for correctness, citation, abstention, and access behavior
- Adversarial and prompt-injection cases with expected safe responses
- Trace evidence for failed or borderline examples
- Named owners for source quality, service health, evaluation, and security review
- Expansion criteria and rollback triggers

**Checkpoint decision:** ship the pilot only with operating evidence the customer can review and repeat.

---
<!-- slide:id=scenario-next-session -->

# Next working session: turn decisions into the pilot plan

Bring the people who can approve sources, permissions, evaluation, and operations.

Recommended agenda:

1. Confirm the bounded customer decision and non-goals.
2. Name the source of truth, source owner, and access boundary.
3. Select the IQ/source pattern and live-data boundary.
4. Draft the golden dataset, including restricted and stale-source cases.
5. Agree the evidence gate for retrieval, routing, evaluation, tracing, and release.

**Exit outcome:** a pilot decision record that the delivery team can implement in the lesson activities.
