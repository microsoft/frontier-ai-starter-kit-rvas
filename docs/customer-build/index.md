---
title: Customer Build Track
nav_order: 2
has_children: true
description: Choose an application path, then reuse the canonical Foundry sessions needed to prove a customer outcome.
---

# Customer Build

Start with one [scenario record](../customer-outcome), then choose the shape of application that
best proves the customer outcome. Paths do not create new sessions: they link to the same
Northfield reference sessions, identifying what is required, recommended, or optional for the
application you are building.

## The shared lifecycle

Every customer application starts by defining the outcome, target users, approved inputs or data,
access assumptions, safety boundaries, owners, and a testable success measure. Every credible
prototype then needs scenario-specific evaluation, a trace/operating decision, and a pilot,
harden, or stop decision.

The middle differs by application type. Grounding is required when trusted documents are the
product; it is optional when the product is a governed action, live-data copilot, voice
experience, or durable workflow.

## Choose a path

| Application shape | Choose it when | Route |
|---|---|---|
| Knowledge and policy assistant | Users need trusted answers from policies, manuals, FAQs, or approved documents. | [Open knowledge path]({{ '/catalog.html?outcome=customer-build&path=knowledge-assistant' | relative_url }}) |
| Governed action and workflow agent | The value is creating, changing, routing, or escalating work safely. | [Open workflow path]({{ '/catalog.html?outcome=customer-build&path=governed-workflow-agent' | relative_url }}) |
| Live data and insights copilot | Users need a current operational answer from a governed data source. | [Open live-data path]({{ '/catalog.html?outcome=customer-build&path=live-data-copilot' | relative_url }}) |
| Voice or multimodal assistant | Spoken, hands-free, or accessible interaction is central to the user journey. | [Open voice path]({{ '/catalog.html?outcome=customer-build&path=voice-multimodal-assistant' | relative_url }}) |
| Visual multimodal assistant | A safe image is necessary to complete a bounded, reviewable task. | [Open visual path]({{ '/catalog.html?outcome=customer-build&path=visual-multimodal-assistant' | relative_url }}) |
| Document workflow | A document must be extracted, validated, reviewed, and routed into work. | [Open document path]({{ '/catalog.html?outcome=customer-build&path=document-workflow' | relative_url }}) |
| Governed data copilot | Insight needs explicit data access, field, query, and provenance controls. | [Open data path]({{ '/catalog.html?outcome=customer-build&path=governed-data-copilot' | relative_url }}) |
| Orchestrated or long-running workflow | The outcome requires specialist handoffs, durable jobs, or an auditable multi-step process. | [Open orchestration path]({{ '/catalog.html?outcome=customer-build&path=orchestrated-workflow' | relative_url }}) |

## How the paths work

Each path begins with **Define your outcome**, then links to canonical sessions with a route-specific
note. Follow the reference session for the hands-on mechanics; use your scenario record to decide
what to substitute, what to test, and what proof is enough for the next decision.

- **Required** sessions establish the path's core capability and trust evidence.
- **Recommended** sessions strengthen a controlled pilot or stakeholder demo.
- **Optional** sessions are only worth doing when they improve the customer outcome.

Document processing is intentionally not listed as a path yet. It needs a dedicated canonical
session before it can be offered as a repeatable build route.

## Start here

Complete [Define your outcome](../customer-outcome) before choosing a path. If the customer does
not yet have an idea, start with [Idea Forge](../idea-forge).
