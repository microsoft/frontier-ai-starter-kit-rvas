---
name: customer-activity-forge
description: "Research a customer and industry from public sources, then generate ranked AI-application ideas mapped to the three customer-delivery scenario playbooks."
argument-hint: "Company name and industry are required. Optional: region/segment and known pain points."
---

## Context

Use this skill when a participant has a customer or industry but no bounded AI opportunity. It
bridges “we should do something with AI” and a useful customer conversation: research public facts,
propose approximately ten achievable ideas, and map the best candidates to a scenario playbook.

This is an intake tool, not an architecture approval. The next step after choosing an idea is a
scenario playbook conversation that validates source ownership, access, environment, operating
model, and the evidence needed for the next decision.

## Input

**Required**
- `customer_name` — company or business unit.
- `industry` — sector, such as retail, healthcare, financial services, or manufacturing.

**Optional**
- `region_or_segment` — geography or sub-segment.
- `known_pain_points` — customer signals to verify during research.

If either required input is missing, ask for it before proceeding.

## Process

### 1. Research public sources only

Use `web_search` and `web_fetch` to collect:

- the company’s products, services, customer segments, recent announcements, and stated priorities;
- public evidence of operating activities from investor relations, annual reports, earnings material,
  leadership posts, or official press releases;
- current industry pressures and AI/automation trends from freely accessible industry bodies,
  analysts, or government sources.

Cite every company or industry claim with a URL and retrieval date. Mark unavailable facts with
⚠️ rather than guessing. Do not use account plans, CRM data, confidential material, or non-public
information.

### 2. Generate approximately ten ideas

Every idea must be tied to the research, safe enough for a first demonstration, and described with:

| Field | Guidance |
|---|---|
| **Title** | Outcome-first, 4–8 words |
| **Description** | What improves, how the experience works, and the first tangible output |
| **Target user** | The role benefiting from the result |
| **Business outcome** | What becomes faster, safer, cheaper, or more reliable |
| **Scenario direction** | One primary playbook plus any relevant secondary capability |
| **First decision** | The question to take into the selected scenario playbook |
| **Effort** | `Starter`, `Core`, or `Stretch` |
| **Research fit** | Why the idea fits this customer, with citation |
| **Safe representative context** | Candidate documents, data product, approved content, or sample to use in a demonstration |
| **Evidence** | The routine, edge, refusal, review, or access case that proves the first outcome |

Use these exact primary scenario labels:

| Scenario direction | Use when |
|---|---|
| **AI Grounding / IQ** | Trusted answers require the right mix of enterprise knowledge and operational context. This can include Foundry IQ, Fabric IQ, Work IQ, Web IQ, SharePoint, or a Copilot Studio discussion. |
| **Content Understanding and Document Workflow** | Business content needs SME-authored understanding, extraction, review, and handoff into a process. |
| **Avatar Scenario** | Approved learning, communications, onboarding, or support content needs an accessible, governed semi-automated avatar-led presentation. |

Visual input, structured data, actions, evaluation, tracing, and deployment are capabilities—not
competing top-level scenarios. Mention them only when they are necessary to the proposed proof.

### 3. Calibrate scope

| Effort | Meaning |
|---|---|
| `Starter` | A narrow demonstrator for one user and one customer decision: a safe sample, an explicit owner, and a small evidence set. |
| `Core` | A credible customer workshop or event-day proof: one bounded outcome, an evaluation/golden-data slice, and a clear review or operating decision. |
| `Stretch` | A follow-on proof requiring multiple systems, a richer integration, multiple interfaces, or a more mature operating model. State what is intentionally deferred. |

Apply these guardrails:

- Do not propose a generic chatbot, a broad autonomous workflow, or a production integration that
  cannot be demonstrated safely.
- Do not assume that every idea needs RAG, a new landing zone, or a Foundry-only implementation.
- Do not use file counts as an architecture decision. Start with ownership, access, freshness,
  quality, and the evidence needed.
- Every idea needs an approved or synthetic representative sample. If customer data is not ready,
  name the gap and use a safe sample only for the conversation.

### 4. Produce the result

Return the following sections, in this order:

#### Part A — Research summary

Three to five sentences with inline citations and explicit coverage gaps.

#### Part B — Ranked summary

| # | Title | Effort | Scenario direction | Why it fits |
|---|---|---|---|---|
| 1 | … | Core | AI Grounding / IQ | … |

Rank by customer fit, achievable first proof, and differentiation.

#### Part C — Idea details

Give all ten fields from step 2 for every idea.

#### Part D — Recommended top three

Name the top three and give a one-sentence reason for each.

#### Part E — Scenario handoff

For the top idea, pre-fill this handoff. Clearly mark information the customer must confirm.

| Scenario input | Pre-filled direction |
|---|---|
| Customer outcome | … |
| Target users and access boundary | … |
| Context and source owner | … |
| Existing environment | … |
| Ownership model | … |
| Recommended scenario | … |
| Golden-dataset / evidence starter | … |
| First customer decision | … |

End with the recommended scenario-playbook URL:

- `docs/scenario.html?id=ai-grounding`
- `docs/scenario.html?id=content-understanding-document-workflow`
- `docs/scenario.html?id=avatar-scenario`

## Anti-patterns

- Fabricating company facts or leaving research claims uncited.
- Treating the output as an approved architecture or a product recommendation.
- Prescribing Foundry, Copilot Studio, SharePoint, Fabric, or an IQ flavor before the customer’s
  data ownership, access, licensing, and operating constraints are discussed.
- Suggesting a landing zone, broad infrastructure baseline, or production deployment for a first
  demonstration.
- Omitting the customer owner, safe representative context, or first evidence case.
