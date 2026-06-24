---
title: Customer Outcome Canvas
nav_order: 2
---

# Customer Outcome Canvas

**This canvas is the working artifact for your hackathon.** Fill it out once — and use it as your north star from Tier 1 through Capstone.

Pick your path:

### You have a customer or business idea ready
{: .text-delta }

Fill in the **Pre-work** canvas table below to lock in your outcome, users, data sources, actions, and demo story. Then start [Foundations]({{ '/challenges' | relative_url }}#tier-1--foundations) with your own data.

### You need an idea
{: .text-delta }

Use the [**Customer Challenge-Forge**](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md) skill to generate ~10 right-sized, buildable Microsoft Foundry AI ideas from a customer name and industry. Pick the one that resonates, and use its output to fill in the canvas below — business outcome, users, data sources, and tier guidance map directly. Then proceed to [Foundations]({{ '/challenges' | relative_url }}#tier-1--foundations).

### You're here to upskill with no customer scenario
{: .text-delta }

Start with [Getting Started]({{ '/setup' | relative_url }}) to configure your environment, then begin [Foundations]({{ '/challenges' | relative_url }}#tier-1--foundations) using **Northfield University** as your reference scenario. The architecture, tiers, and checkpoint structure are identical to Customer Build Mode — Northfield is the shape, not a ceiling. After this event, you can swap in a customer scenario using the [Scenario swap guide](#scenario-swap-guide) below.

## Pre-work: fill this in before the event

| Field | Prompt |
|---|---|
| Customer / business area | Which team, process, or account is this for? |
| Target users | Who will use the assistant: employees, support agents, sellers, operators, students, citizens? |
| Business outcome | What should be faster, safer, cheaper, or more reliable after the prototype works? |
| Top user tasks | What are the top 3 questions or workflows users need help with? |
| Knowledge sources | Which safe documents, FAQs, policies, manuals, tickets, or pages can ground answers? *(see corpus prep guidance below)* |
| Action candidates | What should the agent be allowed to do, and which actions require approval? |
| Safety boundaries | What should the agent refuse, escalate, redact, or avoid automating? |
| Success measures | What metrics or demo evidence would make stakeholders trust the prototype? |
| Final demo story | What 2-minute journey will show the outcome clearly? |

### Preparing your corpus for Foundations Step 4

When filling in **Knowledge sources**, use these guidelines to avoid the most common corpus problems:

- **Minimum useful size:** 5–20 well-structured documents (FAQs, policy pages, SOPs, product guides)
  is enough for a compelling hackathon demo. A sparse corpus produces "I don't know" answers even on
  questions the assistant should handle.
- **Safe data only:** no PII, unredacted customer data, confidential pricing, or legal content that
  has not been cleared for use in a demo environment. When in doubt, use public-facing or
  pre-approved summaries.
- **Supported formats:** the indexing script (`step4_index.py`) handles plain text (`.txt`) and
  Markdown (`.md`) natively. For PDFs, extract text first — `pypdf` is fast enough for hackathon
  use; Azure Document Intelligence gives higher quality for complex layouts.
- **PDFs / SharePoint:** the Foundry portal's **Build → Indexes → Add data** flow can ingest PDFs
  and SharePoint pages without writing code — a good option if the team is comfortable with portal
  navigation and wants to move quickly.
- **Northfield as fallback:** if customer data is not cleared or not ready by event day, complete
  Foundations with the Northfield University corpus and capture the corpus swap as a follow-up task.
  The indexing architecture, agent wiring, and grounding pattern are identical regardless of which
  corpus you use — Northfield is the reference, not a ceiling.

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
