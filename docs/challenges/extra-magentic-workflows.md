---
title: "Extra: Magentic Workflows"
parent: Challenges
nav_order: 22
---

# Extra · Magentic Workflows (Microsoft Agent Framework)

> **Tier 2 · Extra — modular.** You can attempt this in any order with the other Extras.
> **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ Assistant).
> Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> **Specific prereq:** the **Advanced · Action Tools** challenge — your Action sub-agent reuses the MCP
> action tool (`ACTION_MCP_URL`) you wired there.

> ⚙️ **Infra prerequisite:** the **`agent-framework`** SDK (install on demand — not pre-pinned) and **DevUI** for
> visualization — both run **locally**, no extra Azure provisioning. You only need your Foundations
> `.env` + the Action Tools backend running.
>
> 🎤 **Demo wow-factor:** a **manager agent plans live** which specialist to call next — watch the plan
> light up in **DevUI** (green = done, purple = running) instead of a hard-coded if/else chain.

## Why this challenge

Your assistant is **one** agent doing everything: triage, retrieval, action, escalation. That works
until the jobs conflict — a good retriever makes a clumsy escalation-writer. The **Microsoft Agent
Framework (MAF)** lets you compose **specialized** agents and have a **Magentic manager** *plan*, at
runtime, which one to call for each part of a request. This is **dynamic** orchestration — the manager
decides the route per task, unlike a fixed sequential/fan-out pipeline.

You'll build four specialists and let the manager coordinate them:

| Sub-agent | Responsibility | Backed by |
|---|---|---|
| **Triage** | Classify the request, decide what's needed | model + instructions |
| **Knowledge** | Answer from the FAQ corpus | your Foundations AI Search knowledge base |
| **Action** | Execute a real operation (ticket/hold/booking) | the MCP action tool (`ACTION_MCP_URL`) |
| **Escalation** | Draft a human-handoff when confidence is low | model + instructions |

```text
   request
      |
      v
   +------------------------+
   | Magentic manager       |
   | plans + routes (live)  |
   +-----+-----+-----+-----+
         |     |     |     |
         v     v     v     v
   +--------+ +-----------+ +--------+ +------------+
   | Triage | | Knowledge | | Action | | Escalation |
   +--------+ +-----------+ +--------+ +------------+

```

---

## Step 1 — Define the four specialist agents (MAF)

**Goal:** Four single-responsibility agents exist as MAF `ChatAgent`s with focused instructions.

**Tasks:**

1. `pip install agent-framework` (install on demand; not pre-pinned). **Search before you implement:** query `microsoft-docs`
   and `foundry-mcp` (the **`foundry-workflows`** skill) for the *current* MAF `ChatAgent` /
   Magentic builder API — MAF is fast-moving.

2. Create **Triage**, **Knowledge**, **Action**, **Escalation** as separate agents, each with a tight
   system prompt scoped to its one job.

3. Give **Knowledge** your AI Search knowledge base and **Action** the MCP tool at `ACTION_MCP_URL`
   (reuse the Action Tools wiring). Triage and Escalation are model-only.

**Success Criteria:**

- [ ] Four distinct agents instantiate, each with single-responsibility instructions.
- [ ] Knowledge is grounded in the FAQ corpus; Action holds the MCP tool.

**Checkpoint:** *Self-check* — four distinct agents instantiate (Triage, Knowledge, Action, Escalation), each with single-responsibility instructions; Knowledge is grounded in the FAQ corpus and Action holds the MCP tool.

---

## Step 2 — Compose them under a Magentic manager

**Goal:** A Magentic workflow where the manager plans which specialist handles each part of a request.

**Tasks:**

1. Build a **Magentic** workflow (manager/planner) and register the four specialists as participants.
2. Write the manager instructions: *triage first; route knowledge questions to Knowledge; route
   do-something requests to Action; if confidence is low or the request is out of scope, hand to
   Escalation.*

3. Run a composite prompt that needs **two** specialists, e.g. *"I can't log into the portal and I need
   to drop CS101 — help."* (Knowledge for the login FAQ + Action for the course hold/drop).

**Success Criteria:**

- [ ] The manager invokes **more than one** specialist for a composite request.
- [ ] The Action path still respects the **human-approval** loop from Action Tools.

**Checkpoint:** *Self-check* — on the composite request the manager invokes **more than one** specialist, and the Action path still respects the human-approval loop.

---

## Step 3 — Visualize the plan in DevUI

**Goal:** Watch the manager's plan execute live.

**Tasks:**

1. Launch **DevUI** and point it at your workflow.
2. Submit the composite request and watch the plan graph: nodes go **purple while running**, **green
   when done**, as the manager fans out to specialists.

3. Submit a low-confidence / out-of-scope request ("Can you change my final grade?") and confirm it
   routes to **Escalation**.

**Success Criteria:**

- [ ] DevUI renders the plan with live status colors per sub-agent.
- [ ] An out-of-scope request is routed to Escalation, not actioned.

**Checkpoint:** *DevUI state* — screenshot the plan graph mid-run (a running + a completed node) and the
Escalation route.

> _No `validate.py` ships here — Steps 1–2 are observable from the run output and Step 3 is a DevUI visual. solution.md lists what a headless checker would assert if your team wants to script Steps 1–2._

---

## What you built

A **multi-agent** Northfield assistant where a Magentic manager **plans the route at runtime** across
four specialists — dynamic orchestration you can *watch* in DevUI, not a brittle hand-coded pipeline.
