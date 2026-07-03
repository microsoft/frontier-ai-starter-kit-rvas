
# Customer Build · Chapter 0 — Define your outcome



**This is the first task in the Customer Build Track.** Fill it out once, use it as the north star from Foundations through Capstone, and update it only when the customer outcome changes.

If you arrived from [Idea Forge](challenge.html?id=idea-forge), transfer the selected idea's business outcome, users, data sources, tier guidance, and risk notes into the table below.

## Scenario pack

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

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="challenge.html?id=customer-foundations">Start Chapter 1 with your scenario</a>
</div>
