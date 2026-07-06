---
title: "Extra: Magentic Workflows · Facilitator"
parent: Build Modules
nav_order: 122
nav_exclude: true
---

# Facilitator Guide · Extra — Magentic Workflows (MAF)

> **Facilitator-only.** Hardest Extra conceptually (⭐⭐⭐⭐⭐), but no extra Azure infra — it all runs
> locally on `agent-framework` + DevUI. The gate is the Action Tools prereq (the Action sub-agent
> reuses that MCP wiring) and the team's comfort with the fast-moving MAF API.

## What this activity is really teaching

Dynamic orchestration. The contrast that matters: a fixed sequential/fan-out pipeline routes the
*same way every time*; a Magentic manager *plans the route per request*. Neither reference repo ships
a Magentic pattern — this is the differentiator. The keeper insight is single-responsibility agents +
a planner: small, sharp specialists beat one do-everything agent, and the manager composes them.

## Infra to pre-provision

None beyond Foundations. Confirm:

- `agent-framework` installs on demand via `pip install agent-framework` (not pre-pinned).
- DevUI launches locally.
- The Action Tools backend is running (`ACTION_MCP_URL` reachable) — the Action sub-agent needs it.

## Search-Before-Implement (critical — MAF moves weekly)

MAF's `ChatAgent` constructor and the Magentic builder API change often. Do not hand teams a fixed
snippet. Point them at `microsoft-docs` + `foundry-mcp` via the `foundry-workflows` skill for the
current surface. If a team is stuck on import/constructor errors, it's almost always a stale signature —
re-query rather than guess.

## Reference shape (for your eyes — adapt to the live API)

Four specialists, then a Magentic manager composing them:

```python
# Illustrative ONLY — confirm current names via microsoft-docs before using.
from agent_framework import ChatAgent  # name/path may differ in current SDK

triage     = ChatAgent(name="Triage",     instructions="Classify the request; decide what is needed.")
knowledge  = ChatAgent(name="Knowledge",  instructions="Answer ONLY from the Northfield FAQ.", tools=[search_tool])
action     = ChatAgent(name="Action",     instructions="Execute the requested operation.", tools=[mcp_action_tool])
escalation = ChatAgent(name="Escalation", instructions="Draft a human handoff when confidence is low.")

# Magentic manager plans which specialist to call per task.
workflow = MagenticBuilder().participants(triage, knowledge, action, escalation).build()

```
The point is the shape (4 specialists + planner), not these exact symbols.

## Per-step facilitation

### Step 1 — four specialists
- **Pitfall:** instructions too broad → agents overlap and the manager can't route cleanly. Push for
  *one job each*. Knowledge must be grounded; Action must hold the MCP tool.

- `validate.py --step 1` checks the four agents are defined with distinct roles.

### Step 2 — Magentic manager
- The composite prompt ("can't log in and drop CS101") is designed to force ≥2 specialists. If the
  manager only calls one, the manager instructions aren't decomposing the request — tighten them.

- Critical: the Action path must still honor the approval loop from Action Tools. Composing
  agents does not remove human-in-the-loop on writes.

- `validate.py --step 2` asserts ≥2 specialists fire on the composite request.

### Step 3 — DevUI
- This is the demo. Green/purple nodes make the *live planning* visible — that's the "aha." Have them
  screenshot a mid-run graph.

- The out-of-scope prompt ("change my final grade") must route to Escalation, proving the manager
  refuses+hands off rather than forcing an action. Great teaching moment on safe orchestration.

## Validate.py scope

Steps 1–2 are headless-checkable (agents defined; routing fans to ≥2 specialists) — hence
`validate.py`. Step 3 is a DevUI visual (screenshot the plan graph), so its checkpoint is portal/DevUI
state; `--all` re-runs 1–2.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Import/constructor errors | stale MAF API | re-query `microsoft-docs`/`foundry-workflows` |
| Manager calls only one agent | weak decomposition instructions | make manager triage + split composite asks |
| Action runs without asking | approval loop dropped | reuse Action Tools approval handling |
| DevUI shows nothing | not pointed at the workflow | launch DevUI against the built workflow |
| Out-of-scope gets actioned | no escalation rule | add low-confidence → Escalation routing |
