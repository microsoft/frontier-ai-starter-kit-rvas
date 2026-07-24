# Extra · Fabric IQ — Real-Time Data Grounding

> **Command context:** Run the bootstrap command from the repository root.

> Tier 2 · Extra — modular. You can attempt this in any order with the other Extras.
> Prerequisite: the Foundations end-state (a deployed, grounded Northfield IQ Assistant).
> Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> Specific prereq: Foundations Step 4 (the AI Search knowledge base) — this Extra adds a
> *second*, live source alongside it.

> ⚙️ Infra prerequisite (facilitator must pre-provision): a Microsoft Fabric capacity
> (F-SKU or Fabric trial) with a OneLake lakehouse holding a live operational table, plus a
> Fabric IQ data agent that users can access. See
> [solution.md](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/activities/extra-fabric-iq/solution.md) → *Infra to pre-provision* for the exact setup. Gate this Extra behind
> facilitator availability — without Fabric capacity it cannot be completed.
>
> 🎤 Demo wow-factor: the assistant answers *"are there seats left in CS101 right now?"* with live
> numbers pulled from Fabric — something a static RAG index physically cannot do.

> ⚠️ **Preview:** Foundry's Fabric IQ integration is currently preview, has no SLA, and is not
> recommended for production workloads. Confirm current regional support, licensing, identity,
> data-boundary, and governance requirements with your Fabric administrator before the event.

## Why this activity

Your Foundations assistant is grounded in documents — the Northfield FAQ corpus indexed in Azure AI
Search. Documents are perfect for policy, deadlines, and how-to answers, but they go stale: an
indexed PDF can't tell a student that CS101 just dropped from 3 open seats to 0 five minutes ago.

Fabric IQ closes that gap. It exposes live operational data sitting in OneLake (course-seat
availability, dining-hall capacity, shuttle ETAs) to your agent as a tool, right next to the static
knowledge base. The agent learns to pick the right source: *policy question → FAQ knowledge base;
right-now question → Fabric IQ*.

```text
   student question
        │
        ▼
   Northfield IQ Assistant ──┬──▶ AI Search knowledge base   (static: policy, deadlines)
                             └──▶ Fabric IQ tool  ──▶ OneLake (LIVE: seats, capacity, ETAs)
```

---

## Step 1 — Confirm the live data source in OneLake

**Goal:** You can see a live operational table in OneLake that the agent will query.

**Tasks:**
1. Open the Fabric workspace your facilitator provisioned and find the lakehouse (e.g. `northfield_ops`).
2. Locate the live table — for this Extra, `course_seats` with columns
   `course_code, section, capacity, enrolled, seats_open, updated_at`.
3. Run a quick SQL/Spark preview in Fabric: `SELECT course_code, seats_open FROM course_seats WHERE course_code = 'CS101'`.
   Note the value — you'll prove the agent returns the same number.

**Success Criteria:**
- [ ] You can read at least one row of live data and record its current `seats_open` value.
- [ ] You know the lakehouse + table name your agent will be pointed at.

**Checkpoint:** *Portal state* — the Fabric SQL/Spark preview returns a `seats_open` value for CS101.

> _The number changing between runs is the point — that's the live-ness you'll demo._

---

## Step 2 — Wire the Fabric IQ tool to your agent

**Goal:** Attach Fabric IQ to the Northfield IQ Assistant as a second grounding tool.

**Tasks:**
1. In your Foundry project, register the Fabric IQ server-side tool using the current Foundry setup
   flow. Your facilitator supplies the Fabric workspace/data-agent details and handles the required
   user sign-in/OAuth flow; this is not a connection-string or project-managed-identity shortcut.
2. Using the `foundry-toolboxes` skill pattern, attach the Fabric IQ tool to your existing agent
   (`AZURE_FOUNDRY_AGENT_NAME`) alongside the AI Search knowledge-base tool from Foundations Step 4.
   Search before you implement: query `foundry-mcp` and `microsoft-docs` for the current Fabric tool
   class + constructor — this surface is preview and moves.
3. Update the agent's system instructions with a routing rule: *"For real-time availability
   (seats, capacity, wait times) use the Fabric tool; for policies and procedures use the knowledge base."*

**Success Criteria:**
- [ ] The agent lists two grounding tools: the AI Search knowledge base and the Fabric IQ tool.
- [ ] The system instructions contain an explicit source-routing rule.

**Checkpoint:** *Portal state* — the agent's Tools panel shows both the knowledge base and the Fabric
tool attached; a Playground test run invokes the Fabric tool for a "right now" question.

---

## Step 3 — Prove live grounding (and contrast with static RAG)

**Goal:** Show the agent answering a real-time question with a number that matches OneLake.

**Tasks:**
1. In the Playground (or via the Responses API), ask: "Are there any seats left in CS101 right now?"
2. Confirm the answer's number matches the `seats_open` you read in Step 1.
3. Mutate the data (have your facilitator update `course_seats`, or run an UPDATE in Fabric), then ask
   again — the agent's answer should change without re-indexing anything.
4. Ask a policy question ("What's the add/drop deadline?") and confirm it still routes to the FAQ
   knowledge base, not Fabric.

**Success Criteria:**
- [ ] The seat answer matches live OneLake data on the first ask.
- [ ] After mutating the table, a re-ask returns the new number with no re-index step.
- [ ] A policy question still cites the FAQ knowledge base (correct source routing).

**Checkpoint:** *Portal/transcript state* — capture two transcripts of the CS101 question across a data
change showing the number moved; capture one policy answer still citing the FAQ corpus.

> _Facilitator verifies the contrast verbally: static RAG would have returned the stale indexed number both
> times; Fabric IQ tracks the source of truth._

---

## What you built

A preview dual-grounded assistant: durable knowledge from AI Search plus live operational information
from Fabric IQ, with the agent routing each question to the right source. Fabric IQ processes requests
in the signed-in user's Fabric context and honors Fabric permissions and governance; it is not an
unrestricted database connector.
