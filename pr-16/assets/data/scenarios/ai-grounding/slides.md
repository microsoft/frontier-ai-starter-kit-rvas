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

Use this deck to discuss answer sources, access, retrieval evidence, and the proof needed before a
pilot ships.

**Workshop outcome:** select a governed context pattern, access boundary, evaluation plan, and
operating evidence for a bounded AI-assisted decision.

---
<!-- slide:id=scenario-intro -->

# How to use this conversation

Choose the smallest useful scenario that can be grounded, evaluated, and operated safely. This is not
a complete enterprise-platform design session.

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

Agree the technical foundation before content enters the pilot.

Customer discussion prompts:

- Which business decision or action needs trusted context?
- Which environment will host the pilot, and who owns it?
- Which region, identity model, logging boundary, and data handling expectations apply?
- Which model and retrieval capabilities must be available in that environment?

**Principle:** protect the source of truth before optimizing developer convenience.

---
<!-- slide:id=lesson-foundation-choices -->

# Lesson 1 choices: shared foundation or existing landing zone?

| Choice | When it fits | Trade-off |
|---|---|---|
| Scenario-provisioned foundation | Fast pilot with clear defaults | Customer still needs operational ownership |
| Existing Azure landing zone | Enterprise controls are already in place | More dependency on customer platform teams |
| Portal-led setup | Early orientation or stakeholder demo | Harder to reproduce without a written contract |
| Bring-your-own resources | Customer already has Foundry, search, and monitoring | Must prove configuration matches the pilot needs |

Discuss identity, network boundaries, observability, and regional capacity before content ingestion.

---
<!-- slide:id=lesson-foundation-evidence -->

# Lesson 1 — what must be true: foundation is ready for content

Move forward when the team can show:

- A named environment owner and service owner
- Keyless-first access plan for people and workload identities
- Model and retrieval capabilities available in the chosen region
- Monitoring and trace destination identified before pilot traffic
- Environment values documented as a reusable contract, without secrets

**Decision:** it is safe to connect approved pilot content.

---
<!-- slide:id=lesson-source-selection-context -->

# Lesson 2 context: select the source and permission architecture

Start grounding with source ownership, not a search box.

Ask the customer:

- Which system remains the source of truth?
- Who owns content quality, retention, and retirement?
- Which users may see which records, and why?
- Is permission trimming needed at retrieval time, answer time, or both?
- What happens when content is missing, conflicting, or restricted?

**Non-negotiable:** every pilot source needs an owner and an access decision.

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

# Lesson 2 — what must be true: signed source and access decision

The source decision is ready when it records:

- Approved source or sources, with business owner and steward
- Source-of-truth statement and freshness expectation
- Permission model, including restricted and access-denied cases
- Citation, provenance, and audit expectations
- Boundary between governed internal knowledge, live work data, analytics, and public information

**Decision:** the pilot has a defensible source architecture before indexing starts.

---
<!-- slide:id=lesson-ingestion-context -->

# Lesson 3 context: ingest and index approved content

Ingestion does more than move files. It preserves the evidence behind an answer.

Discuss:

- Which approved content is small enough for the pilot but representative enough to test?
- What metadata must survive ingestion: source, version, owner, date, sensitivity, access group?
- How will stale, duplicate, superseded, and conflicting documents be handled?
- Which content should stay remote rather than copied?

**Goal:** retrieve the right passage and provenance for the user.

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

Do not copy content only to make the retrieval architecture look simpler.

---
<!-- slide:id=lesson-ingestion-evidence -->

# Lesson 3 — what must be true: approved documents are discoverable

Before moving on, reviewers should see:

- Representative pilot corpus indexed or connected
- Required source metadata visible in retrieval results
- Permission-sensitive examples behaving as designed
- Golden questions returning plausible source passages
- Known stale or conflicting content labeled and handled

**Decision:** the knowledge layer produces trustworthy retrieval evidence before you judge answers.

---
<!-- slide:id=lesson-model-selection-context -->

# Lesson 4 context: compare chat and embedding choices

Model choice matters. Judge it through the grounding task.

Discuss what the pilot needs from:

- The chat or query-planning model: reasoning, instruction following, latency, cost, region, and safety behavior
- The embedding model: retrieval quality for the customer’s vocabulary, abbreviations, and document style
- Capacity: expected users, peaks, and whether throughput should be reserved or consumption-based

**Principle:** pick models using golden-dataset evidence, not reputation.

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

Access control and citations are baseline obligations, not trade-offs.

---
<!-- slide:id=lesson-model-selection-evidence -->

# Lesson 4 — what must be true: model decision supports grounded answers

A model choice is ready when the team has compared:

- Retrieval hit quality on golden questions
- Answer usefulness with citations and abstention behavior
- Latency and cost under expected pilot usage
- Region and quota feasibility
- Failure behavior on ambiguous, stale, or restricted questions

**Decision:** the selected model and embedding path meet the pilot's quality and operating constraints.

---
<!-- slide:id=lesson-grounded-app-context -->

# Lesson 5 context: build retrieval before adding an agent

A grounded experience should prove retrieval before adding orchestration.

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

State the required behaviors: cite available evidence, abstain when it is missing, and separate
“not found” from “not allowed.”

---
<!-- slide:id=lesson-grounded-app-evidence -->

# Lesson 5 — what must be true: retrieval is trustworthy enough to use

The grounded app is ready for the next step when:

- Golden questions return relevant sources with provenance
- Answers quote or summarize only supported evidence
- Access-denied cases do not leak restricted content
- Stale-source cases trigger the agreed warning or refusal
- Reviewers can explain why an answer was accepted or rejected

**Decision:** add an agent only when orchestration solves a customer need that retrieval alone cannot.

---
<!-- slide:id=lesson-agent-routing-context -->

# Lesson 6 context: add agent and live-data routing only when justified

Use agents and tools when the experience needs planning, source routing, or action boundaries. They
cannot compensate for unclear knowledge architecture.

Discuss:

- Which requests should use policy knowledge, analytics, work context, public information, or live operational data?
- Which source is authoritative for each request type?
- Which live-data calls are safe, necessary, and auditable?
- What must the agent refuse or route away from?

**Boundary:** live data complements the source of truth. It must not silently replace it.

---
<!-- slide:id=lesson-agent-routing-choices -->

# Lesson 6 choices: route sources with clear rules

| Choice | Use when | Trade-off |
|---|---|---|
| Foundry agent with knowledge tool | The experience needs orchestration over approved knowledge | Requires explicit instructions and routing tests |
| Multi-source knowledge routing | Several governed knowledge sets answer different intents | Source boundaries must be visible and testable |
| Live-data tool | A real-time status, inventory, case, or transaction check is required | Tool reliability, permissions, and audit become part of the pilot |
| Multi-agent workflow | Distinct roles need separate responsibilities | More moving parts and harder evaluation |

Choose the simplest route that preserves source authority and user trust.

---
<!-- slide:id=lesson-agent-routing-evidence -->

# Lesson 6 — what must be true: routing is explainable and controlled

Routing is ready when the team can show:

- Test questions for each source boundary
- Correct route chosen for policy, analytical, work-context, web, and live-data cases
- Refusal or escalation for unsupported requests
- No live-data call without a justified real-time need
- Trace or log evidence that shows which source answered

**Decision:** evaluate the agent as a controlled router.

---
<!-- slide:id=lesson-evaluate-and-trace-context -->

# Lesson 7 context: evaluate and trace

Decide whether the assistant is good enough for real people.

Discuss:

- Which golden questions represent normal, edge, stale, restricted, and adversarial cases?
- Who reviews correctness, citations, access behavior, and business usefulness?
- What traces are needed to investigate a failure without exposing unnecessary sensitive content?
- Who signs off that the evidence is enough?

**Operating mindset:** an evaluation you read is a report. One that blocks release is a control.

---
<!-- slide:id=lesson-evaluate-and-trace-choices -->

# Lesson 7 choices: how much evidence is enough

| Decision | Customer trade-off |
|---|---|
| Strict evaluation gate | Slower release, stronger trust for high-impact decisions |
| Phased pilot gate | Faster learning, with narrower scope and clear limits |
| Trace detail | Better troubleshooting, balanced against privacy and retention |
| Continuous evaluation | Better drift detection, with ongoing reviewer commitment |
| Manual review | Higher judgment quality, but limited scale |
| Automated checks | Better repeatability, but must be calibrated against human review |

Generic quality metrics miss correct refusal, current citation, and silence about restricted content.

---
<!-- slide:id=lesson-evaluate-and-trace-evidence -->

# Lesson 7 — what must be true: the assistant is good enough

Evidence to produce:

- Golden-set results for correctness, citation, abstention, and access behavior
- Adversarial cases including prompt injection hidden in retrieved content, with the mitigation re-tested
- One request traced end to end, so a wrong answer can be explained rather than guessed at
- The permission probe re-run against the agent

**Decision:** the evidence supports release to real people, or identifies what must change first.

---
<!-- slide:id=lesson-deploy-and-surface-context -->

# Lesson 8 context: deploy and surface it to users

Decide where people meet the assistant and who runs it.

Discuss:

- Where does this audience already work — Teams, an existing app, or somewhere new?
- Who is in the pilot, and how is access granted and revoked?
- Who triages a wrong answer, and how does a user report one?
- What ends the pilot?

**Operating mindset:** the agent is already deployed. Choose a doorway; do not build another system.

---
<!-- slide:id=lesson-deploy-and-surface-choices -->

# Lesson 8 choices: pick the doorway, keep the rules

| Surface | Where users meet it | When it wins |
|---|---|---|
| Your own app or API | An existing front end | Pilots with one consumer |
| Publish to Teams and M365 Copilot | Teams, Copilot app | Users already work there; no new app to adopt |
| Copilot Studio | Teams, Copilot app | Only if the source decision was SharePoint and M365 |
| Foundry hosted agent | A dedicated endpoint | Other teams consume it, or you need runtime control |
| Custom web UI | A purpose-built app | Demo, custom auth, or a required response contract |

Five rules stay fixed: no keys; preserve the permission boundary; carry tracing into the runtime; pin
the version; rollback by repointing.

---
<!-- slide:id=lesson-deploy-and-surface-evidence -->

# Lesson 8 — what must be true: safe to hand to real users

The release contract records:

- The surface, why it was chosen, and who can use it
- A pinned agent version and a rollback measured in minutes
- The permission probe re-run against the surface itself, not just the agent
- A named triage owner, a review cadence, and how users report a bad answer
- A pilot exit criterion with a date, and a signed release decision

**Decision:** ship, ship with conditions, or stop. A written decision to stop has value.

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

**Exit outcome:** a pilot decision record the delivery team can implement through the lesson activities.
