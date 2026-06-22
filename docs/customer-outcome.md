---
title: Customer Outcome Canvas
nav_order: 3
---

# Customer Outcome Canvas

Use this page when the event goal is more than upskilling: a team wants to start a real customer
application and leave with a concrete agent prototype. Northfield University remains the safe default
scenario; this canvas helps you swap in a customer domain without losing the structure, checkpoints, or
coachability of the hackathon.

## Choose your mode

| Mode | Use when | Default artifact |
|---|---|---|
| **Upskill Mode** | Participants need a guided Foundry learning path | Northfield University IQ Assistant |
| **Customer Build Mode** | A customer or account team wants to explore a real business outcome | Customer-specific grounded agent prototype |

Customer Build Mode should still follow the same tiers. The difference is that every checkpoint answers
a business question, not only a technical one.

## Pre-work: fill this in before the event

| Field | Prompt |
|---|---|
| Customer / business area | Which team, process, or account is this for? |
| Target users | Who will use the assistant: employees, support agents, sellers, operators, students, citizens? |
| Business outcome | What should be faster, safer, cheaper, or more reliable after the prototype works? |
| Top user tasks | What are the top 3 questions or workflows users need help with? |
| Knowledge sources | Which safe documents, FAQs, policies, manuals, tickets, or pages can ground answers? |
| Action candidates | What should the agent be allowed to do, and which actions require approval? |
| Safety boundaries | What should the agent refuse, escalate, redact, or avoid automating? |
| Success measures | What metrics or demo evidence would make stakeholders trust the prototype? |
| Final demo story | What 2-minute journey will show the outcome clearly? |

## Map the hackathon tiers to the customer outcome

| Tier | Build activity | Customer proof point |
|---|---|---|
| **Foundations** | Provision Foundry, choose a model, create an agent, attach a knowledge base | The agent answers real scenario questions with citations from trusted data |
| **Action Tools** | Attach an MCP tool and implement approval | The agent safely completes one valuable workflow without acting silently |
| **Evaluation & Red Teaming** | Create scenario-specific eval and adversarial prompts | The team can show quality, groundedness, refusal, and safety results |
| **Tracing & Observability** | Instrument the run and inspect spans in App Insights | The team can explain latency, retrieval, tool calls, and failure paths |
| **Deploy / UI** | Host the agent and expose a simple stakeholder-facing experience | A non-technical stakeholder can try the prototype and see citations or approval cards |
| **Capstone** | Split the assistant into router and specialists | A realistic customer journey is handled by the right specialist agents |

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

## End-of-event deliverable

Each Customer Build team should leave with:

1. A working grounded agent or hosted prototype.
2. A 2-minute stakeholder demo using the final demo story.
3. A short scorecard: what passed, what failed, and what still needs validation.
4. A risk list covering data quality, permissions, safety, actions, and production readiness.
5. A next-step backlog for pilot or production hardening.

## Coach prompts

- What business decision or workflow improves if this prototype works?
- Which source of truth should the agent cite before anyone trusts the answer?
- Which action is valuable enough to automate but risky enough to require approval?
- What would make the customer say, "Yes, this is worth piloting"?
- What will you show in two minutes that proves the outcome, not just the technology?
