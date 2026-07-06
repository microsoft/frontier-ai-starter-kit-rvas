---
title: "Deepener — Magentic Workflows"
parent: Customer Build Track
nav_order: 70
description: Split your scenario assistant into specialist agents coordinated by a Magentic manager.
---

# Customer Build · Deepener — Magentic Workflows

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Deepener &middot; Magentic Workflows" artifact="A multi-agent workflow where a manager routes YOUR composite user request across focused specialists." next="If the workflow proves valuable, consider the Long-Running Agents deepener to host it." %}

This deepener is **mutuated from [Extra · Magentic Workflows](../challenges/extra-magentic-workflows)** — same orchestration pattern, but applied only if your scenario from [Chapter 0](../customer-outcome) needs more than one specialist brain. This is an **OPTIONAL deepener**. Keep your corpus, action candidates, safety boundaries, success measures, and demo story in view; do not add Magentic orchestration just because it is impressive.

> **Before you start this deepener:** complete Chapter 1 and Chapter 2 if your Action specialist will call a real tool. If one well-instructed agent already handles your demo cleanly, skip this.

---

## Step 1 — Define your specialist agents

**Why it matters for your app:** specialists let you separate conflicting jobs: triage, grounded answering, action execution, and escalation can each have tighter instructions than one overloaded assistant.

**Does this apply to you?** → **Skip it** if your scenario is a single straightforward Q&A or one action flow.
- **Build it** if your top user task regularly combines diagnosis, knowledge lookup, action, and escalation.
- **Adapt it** if you need different specialists than Northfield's four, such as Compliance, Pricing, Scheduler, or Case Summary.

**Decisions to make:**
- Which Chapter 0 **user tasks** need different skills or safety posture?
- Which specialist owns your **corpus** questions, your **action candidates**, and your **safety boundaries**?
- What is each specialist explicitly forbidden to do?

**Apply it to your app:** define focused agents for your scenario; keep each one single-purpose and wire only the tools it needs. Use the spine for exact MAF mechanics. → [Extra · Magentic Workflows — Step 1](../challenges/extra-magentic-workflows#step-1--define-the-four-specialist-agents-maf)

**Prove you applied it:**
- □ Each specialist has a distinct name and one responsibility.
- □ Knowledge specialists cite your corpus; action specialists use only approved tools.
- □ At least one safety boundary is assigned to an escalation or refusal path.

**Stuck?** [Northfield Step 1](../challenges/extra-magentic-workflows#step-1--define-the-four-specialist-agents-maf).

---

## Step 2 — Compose them under a Magentic manager

**Why it matters for your app:** the manager decides the route at runtime, so a composite user request can use the right specialists without a brittle if/else pipeline.

**Does this apply to you?** → **Skip it** if the route is always fixed and simple.
- **Build it** if users ask mixed requests like "explain the policy and submit the request."
- **Adapt it** if your manager should constrain order, require human approval before actions, or escalate early.

**Decisions to make:**
- What routing rules map your Chapter 0 **top tasks** to specialists?
- Which requests must always start with triage or safety screening?
- What success measure proves orchestration helped: fewer wrong tool calls, clearer handoffs, faster resolution?

**Apply it to your app:** register your specialists and write manager instructions that reflect your real routing rules. Test with a composite prompt from your demo story. → [Extra · Magentic Workflows — Step 2](../challenges/extra-magentic-workflows#step-2--compose-them-under-a-magentic-manager)

**Prove you applied it:**
- □ One realistic composite prompt invokes more than one specialist.
- □ The action path still preserves your approval or safety gate.
- □ Out-of-scope or low-confidence requests do not reach the action specialist.

**Stuck?** [Northfield Step 2](../challenges/extra-magentic-workflows#step-2--compose-them-under-a-magentic-manager).

---

## Step 3 — Visualize the plan in DevUI

**Why it matters for your app:** stakeholders trust orchestration more when they can see why the manager called each specialist and where the work went.

**Does this apply to you?** → **Skip it** if your readout does not need orchestration transparency.
- **Build it** if your demo story benefits from showing live planning and routing.
- **Adapt it** if a screenshot or trace is enough for your audience instead of a live DevUI demo.

**Decisions to make:**
- Which demo prompt shows the clearest multi-specialist path?
- Which node proves safety: escalation, refusal, or human approval?
- What visual artifact will you include in your final readout?

**Apply it to your app:** run the same composite prompt in DevUI and capture the live plan with your specialist names. → [Extra · Magentic Workflows — Step 3](../challenges/extra-magentic-workflows#step-3--visualize-the-plan-in-devui)

**Prove you applied it:**
- □ DevUI shows your manager and specialist nodes.
- □ A screenshot captures at least one running and one completed node.
- □ A low-confidence or unsafe request routes to escalation/refusal.

**Stuck?** [Northfield Step 3](../challenges/extra-magentic-workflows#step-3--visualize-the-plan-in-devui).

---

## Deepener end-state

You have a scenario-specific multi-agent workflow only if your app truly needed dynamic routing. Deepeners are optional; return to the [Customer Build Track](../customer-build) and continue with the smallest set that proves your outcome.
