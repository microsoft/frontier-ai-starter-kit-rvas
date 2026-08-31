---
marp: true
paginate: true
title: Content Understanding and Document Workflow
description: Facilitator and customer discussion deck
version: 0.2.0
---
<!-- slide:id=scenario-open -->

# Content Understanding and Document Workflow

**Customer discussion deck**

Turn document understanding into a governed business workflow.

Use this deck to agree on the decision, evidence for automation, and controls required before deployment.

---
<!-- slide:id=scenario-intro -->

## How to use this conversation

This is a working-session deck for sponsors, SMEs, security, data owners, and engineering. It is not an implementation walkthrough.

For each lesson, discuss:

- **Context:** Why the step matters to the business outcome.
- **Choices and trade-offs:** Which path fits the environment.
- **Evidence:** What must be true before moving forward.

The practical steps live in the lesson and activity pages.

---
<!-- slide:id=lesson-foundation-context -->

## Lesson 1: Provision the shared Foundry foundation

Build a stable foundation before adding customer content or extraction logic.

Discuss:

- Which business decision this workflow will improve.
- Which teams own identity, networking, storage, monitoring, and model access.
- Which environments are needed for experimentation, pilots, and production.
- How to apply keyless access, least privilege, and traceability from the start.

Build a reusable base that later scenario tracks can share. Avoid a one-off demo environment.

---
<!-- slide:id=lesson-foundation-choices -->

## Foundation choices and trade-offs

Key decisions:

- **Shared vs. dedicated resources:** Shared foundations reduce setup work; dedicated resources can simplify isolation and chargeback.
- **Region and model availability:** Consider model choice, data residency, latency, and quota together.
- **Identity model:** Prefer managed identity and role-based access over keys where possible.
- **Observability baseline:** Start tracing and monitoring early so later workflow issues are diagnosable.

State the trade-off plainly: quick setup must not hide production controls needed later.

---
<!-- slide:id=lesson-foundation-evidence -->

## Foundation evidence

Before the team proceeds, confirm:

- The Foundry foundation, storage, model deployments, and monitoring plan have owners.
- The access model is documented and keyless-first.
- Environment boundaries are understood.
- Later lessons can use required outputs without copying secrets into notes or code.
- The team knows what still needs security, networking, or operations review.

Decision question: **Can engineering safely build on this foundation without re-deciding basic platform controls each lesson?**

---
<!-- slide:id=lesson-document-source-context -->

## Lesson 2: Connect an approved document source

Content Understanding starts with approved documents, not merely available ones.

Discuss:

- Which workflow source is authoritative: Azure Blob, ADLS Gen2, SharePoint, OneLake, or another governed store.
- Who is allowed to approve sample use.
- How source identity, document version, permissions, and retention are preserved.
- How unsafe, unsupported, or out-of-scope files are quarantined.

A clean folder of copied files works for a lab. It is not an approved business source.

---
<!-- slide:id=lesson-document-source-choices -->

## Document source choices and trade-offs

Key decisions:

- **Business source vs. staging area:** Direct integration preserves context; staging can simplify processing but adds governance work.
- **Representative samples:** Include normal, edge, low-quality, multilingual, and failure cases, not only ideal examples.
- **Permissions:** Decide whether the workflow inherits source permissions or uses a separate processing identity.
- **Retention:** Define how originals, extracted results, evidence, and corrections are retained.

State the trade-off: faster intake does not justify losing provenance or authorization.

---
<!-- slide:id=lesson-document-source-evidence -->

## Document source evidence

Before moving forward, confirm:

- The document source is approved for this scenario.
- Sample documents are representative and authorized for testing.
- Each document traces to its source, version, owner, and retention policy.
- The team has a clear path for quarantine, deletion, and exception handling.
- Access boundaries are enforceable, not just assumed.

Decision question: **Can every document used by the workflow be explained, traced, and governed?**

---
<!-- slide:id=lesson-extraction-selection-context -->

## Lesson 3: Select the extraction capability

Choose extraction based on document variability, schema needs, confidence requirements, and operating constraints.

Discuss:

- Whether Content Understanding analyzers fit the document classes and fields.
- Where Document Intelligence, LLM structured outputs, or multimodal approaches may be better suited.
- Which fields require exact evidence versus broad summarization.
- Which errors are tolerable, reviewable, or unacceptable.

The customer should leave with a documented capability decision, not a default product choice.

---
<!-- slide:id=lesson-extraction-selection-choices -->

## Extraction choices and trade-offs

Key decisions:

- **Content Understanding:** Fits SMEs who need to shape classes and schemas for varied content.
- **Document Intelligence:** Useful for established document extraction patterns and form-like structure.
- **LLM structured outputs:** Flexible for reasoning over text but require strict validation and evidence controls.
- **Multimodal processing:** Helpful when layout, images, or visual cues matter.

State the trade-off: more flexible extraction increases validation, review, cost, and monitoring work.

---
<!-- slide:id=lesson-extraction-selection-evidence -->

## Extraction selection evidence

Before implementation, confirm:

- The selected capability matches document quality, field complexity, region, cost, and review needs.
- The target schema is specific enough to test.
- Known failure cases are included in the decision.
- The team has agreed when a field must be empty rather than inferred.
- Human-review rules are part of the extraction decision.

Decision question: **Can the team explain why this capability is the right fit for the first controlled workflow?**

---
<!-- slide:id=lesson-typed-extraction-context -->

## Lesson 4: Implement typed extraction with evidence

A useful extraction result is typed, validated, and supported by evidence.

Discuss:

- Which fields are required, optional, derived, or prohibited.
- What evidence is needed for each important value: page, span, citation, confidence, or source reference.
- How missing, ambiguous, conflicting, or low-confidence values should be represented.
- Where the workflow must avoid inferred values.

Build more than a JSON shape. Build a decision record a reviewer and auditor can trust.

---
<!-- slide:id=lesson-typed-extraction-choices -->

## Typed extraction choices and trade-offs

Key decisions:

- **Strict schema vs. flexible notes:** Strict schemas help automation; flexible notes may help SMEs explain unusual cases.
- **Confidence thresholds:** High thresholds reduce false approvals and increase review volume.
- **Evidence granularity:** More detailed evidence improves trust but can increase storage and UI complexity.
- **Failure behavior:** Empty-with-reason is safer than filling a field without support.

State the trade-off: automation depends on handling uncertainty well, not only on high field coverage.

---
<!-- slide:id=lesson-typed-extraction-evidence -->

## Typed extraction evidence

Before the workflow can use extracted results, confirm:

- The output validates against the agreed schema.
- Important fields include evidence and confidence where appropriate.
- Missing and low-confidence fields follow a consistent policy.
- Unsupported values are not invented to satisfy the schema.
- Reviewers can see enough source context to confirm or challenge a value.

Decision question: **Would a business reviewer understand what was extracted, why it was trusted, and what still needs attention?**

---
<!-- slide:id=lesson-human-review-context -->

## Lesson 5: Build review, correction, and handoff

Human review belongs in the product design. It is not a fallback after automation fails.

Discuss:

- Which cases require review: missing fields, low confidence, conflicting values, sensitive decisions, or policy exceptions.
- Who can approve, correct, reject, or escalate.
- What correction reason and evidence must be retained.
- Which downstream system receives approved results.

The review experience should make the right action easier than bypassing the process.
---
<!-- slide:id=lesson-human-review-choices -->

## Review and handoff choices and trade-offs

Key decisions:

- **Reviewer queue vs. embedded workflow:** Queues centralize review; embedded workflows meet users where they already work.
- **Correction model:** Corrections should update the case record and feed evaluation. Do not silently overwrite history.
- **Approval boundary:** Decide which results can flow automatically and which require a named approver.
- **Handoff seam:** Use a governed downstream contract. Do not write directly from unreviewed extraction.

State the trade-off: reducing reviewer effort must not erase accountability.

---
<!-- slide:id=lesson-human-review-evidence -->

## Review evidence

Before handoff is trusted, confirm:

- Review rules are explicit and testable.
- A reviewer can correct, approve, reject, and explain the decision.
- Corrections retain the document, evidence, reviewer, timestamp, and contract version.
- Approved results are handed off through a controlled interface.
- Exceptions have an owner and a resolution path.

Decision question: **Can the customer prove who approved a result, what changed, and why it was sent downstream?**

---
<!-- slide:id=lesson-prove-and-observe-context -->

## Lesson 6: Evaluate and trace the workflow

A document workflow is ready when it performs consistently on representative cases and you can diagnose failures.

Discuss:

- Which quality measures matter: field accuracy, routing accuracy, false approvals, review rate, latency, and cost.
- Which adversarial or messy cases should be tested.
- What traces must show across intake, extraction, review, and handoff.
- How corrections become future evaluation evidence.

Evaluate real workflow risk, not only model output quality.

---
<!-- slide:id=lesson-prove-and-observe-choices -->

## Evaluation and tracing choices and trade-offs

Key decisions:

- **Holdout data:** Keep evaluation examples separate from tuning examples.
- **Quality gates:** Define thresholds for automation, review, and rejection.
- **Trace detail:** Capture enough context to debug without exposing unnecessary sensitive content.
- **Regression testing:** Re-run important cases when schemas, analyzers, prompts, or review rules change.

State the trade-off: more automation without measurement increases hidden business risk.

---
<!-- slide:id=lesson-prove-and-observe-evidence -->

## Evaluation evidence

Before promotion, confirm:

- Representative test cases cover normal, edge, and failure segments.
- Field accuracy, review volume, false approval risk, and latency are measured.
- Traces connect document intake, extraction, policy, review, correction, and handoff.
- Failures have named causes and owners.
- The release decision covers rollback and monitoring.

Decision question: **Can the team defend the workflow with evidence rather than a successful demo?**

---
<!-- slide:id=lesson-deploy-context -->

## Lesson 7: Deploy the reviewable workflow

Deployment turns an experiment into an accountable business service.

Discuss:

- Who can invoke the workflow and under what identity.
- Which environment receives the pilot and what production controls are required.
- How analyzer or schema versions are promoted.
- How monitoring, support, rollback, and change management work.

Make the first deployment controlled, observable, and reversible.

---
<!-- slide:id=lesson-deploy-choices -->

## Deployment choices and trade-offs

Key decisions:

- **Pilot scope:** Start with a bounded document set, user group, and decision path.
- **Endpoint and identity:** Use authenticated access and managed identity where possible.
- **Versioning:** Track analyzer, schema, policy, review rules, and downstream contract together.
- **Operations:** Decide alert ownership, support process, rollback criteria, and release cadence.

State the trade-off: a broad rollout before operational readiness can create more manual work than it removes.

---
<!-- slide:id=lesson-deploy-evidence -->

## Deployment evidence

Before controlled rollout, confirm:

- The workflow runs behind approved access controls.
- Monitoring and tracing are enabled for the end-to-end path.
- Version and rollback information is documented.
- Review and correction data stay available after deployment.
- The pilot owner can decide whether to expand, pause, or revise the workflow.

Decision question: **Is the workflow ready to serve a bounded real use case with accountable controls?**

---
<!-- slide:id=scenario-next-session -->

## Next working session

Bring the people and evidence needed to start the scenario:

- One high-value document decision and its business owner.
- An approved source and 15–30 safe, representative samples.
- Expected fields, unacceptable errors, and review rules.
- SME, engineering, security, and workflow handoff owners.
- Current constraints for identity, retention, monitoring, and deployment.

Agree on the first pilot slice and the evidence required before expansion.
