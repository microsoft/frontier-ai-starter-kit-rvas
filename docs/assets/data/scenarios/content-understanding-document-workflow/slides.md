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

Move from trusted document understanding to a governed business workflow.

Use this deck to align on the decision, the evidence needed to trust automation, and the controls required before deployment.

---
<!-- slide:id=scenario-intro -->

## How to use this conversation

This is not an implementation walkthrough. It is a working-session deck for sponsors, SMEs, security, data owners, and engineering.

For each lesson, discuss three questions:

- **Context:** Why this step matters to the business outcome.
- **Choices and trade-offs:** Which path fits the customer environment.
- **Evidence and checkpoint:** What must be true before moving forward.

The practical steps live in the lesson and activity pages.

---
<!-- slide:id=lesson-foundation-context -->

## Lesson 1: Provision the shared Foundry foundation

A document workflow needs a stable foundation before customer content or extraction logic enters the picture.

Discuss:

- Which business decision this workflow will improve.
- Which teams own identity, networking, storage, monitoring, and model access.
- Which environments are needed for experimentation, pilot, and production.
- How keyless access, least privilege, and traceability should be handled from the start.

The goal is a reusable base that later scenario tracks can share, not a one-off demo environment.

---
<!-- slide:id=lesson-foundation-choices -->

## Foundation choices and trade-offs

Key decisions:

- **Shared vs. dedicated resources:** Shared foundations reduce setup friction; dedicated resources can simplify isolation and chargeback.
- **Region and model availability:** Model choice, data residency, latency, and quota must be considered together.
- **Identity model:** Prefer managed identity and role-based access over keys where possible.
- **Observability baseline:** Start tracing and monitoring early so later workflow issues are diagnosable.

Trade-off to name explicitly: speed of setup should not hide production controls that will be required later.

---
<!-- slide:id=lesson-foundation-evidence -->

## Foundation evidence and checkpoint

Before the team proceeds, confirm:

- The Foundry foundation, storage, model deployments, and monitoring plan have clear owners.
- The access model is documented and keyless-first.
- Environment boundaries are understood.
- Required outputs can be handed to later lessons without copying secrets into notes or code.
- The team knows what still needs security, networking, or operations review.

Checkpoint question: **Can engineering safely build on this foundation without re-deciding basic platform controls each lesson?**

---
<!-- slide:id=lesson-document-source-context -->

## Lesson 2: Connect an approved document source

Content Understanding starts with the right documents, not just available documents.

Discuss:

- Which source is authoritative for the workflow: Azure Blob, ADLS Gen2, SharePoint, OneLake, or another governed store.
- Who is allowed to approve sample use.
- How source identity, document version, permissions, and retention are preserved.
- How unsafe, unsupported, or out-of-scope files are quarantined.

A clean folder of copied files is useful for a lab, but it is not the same as an approved business source.

---
<!-- slide:id=lesson-document-source-choices -->

## Document source choices and trade-offs

Key decisions:

- **Business source vs. staging area:** Direct source integration preserves context; staging can simplify processing but increases governance burden.
- **Representative samples:** Include normal, edge, low-quality, multilingual, and failure cases rather than only ideal examples.
- **Permissions:** Decide whether the workflow inherits source permissions or uses a separate processing identity.
- **Retention:** Define how originals, extracted results, evidence, and corrections are retained.

Trade-off to name explicitly: faster intake is not worth losing provenance or authorization.

---
<!-- slide:id=lesson-document-source-evidence -->

## Document source evidence and checkpoint

Before moving forward, confirm:

- The document source is approved for this scenario.
- Sample documents are representative and authorized for testing.
- Each document can be tied back to source, version, owner, and retention policy.
- The team has a clear path for quarantine, deletion, and exception handling.
- Access boundaries are enforceable, not just assumed.

Checkpoint question: **Can every document used by the workflow be explained, traced, and governed?**

---
<!-- slide:id=lesson-extraction-selection-context -->

## Lesson 3: Select the extraction capability

The right extraction method depends on document variability, schema needs, confidence requirements, and operating constraints.

Discuss:

- Whether Content Understanding analyzers fit the document classes and fields.
- Where Document Intelligence, LLM structured outputs, or multimodal approaches may be better suited.
- Which fields require exact evidence versus broad summarization.
- Which errors are tolerable, reviewable, or unacceptable.

The customer should leave with a reasoned capability decision, not a default product choice.

---
<!-- slide:id=lesson-extraction-selection-choices -->

## Extraction choices and trade-offs

Key decisions:

- **Content Understanding:** Strong when SMEs need to shape classes and schemas against varied content.
- **Document Intelligence:** Useful for established document extraction patterns and form-like structure.
- **LLM structured outputs:** Flexible for reasoning over text, but require strict validation and evidence controls.
- **Multimodal processing:** Helpful when layout, images, or visual cues matter.

Trade-off to name explicitly: more flexible extraction can increase validation, review, cost, and monitoring responsibilities.

---
<!-- slide:id=lesson-extraction-selection-evidence -->

## Extraction selection evidence and checkpoint

Before implementation, confirm:

- The selected capability matches document quality, field complexity, region, cost, and review needs.
- The target schema is specific enough to test.
- Known failure cases are included in the decision.
- The team has agreed when a field must be empty rather than inferred.
- Human review rules are part of the extraction decision, not added later.

Checkpoint question: **Can the team explain why this capability is the right fit for the first controlled workflow?**

---
<!-- slide:id=lesson-typed-extraction-context -->

## Lesson 4: Implement typed extraction with evidence

A useful extraction result is typed, validated, and backed by evidence.

Discuss:

- Which fields are required, optional, derived, or prohibited.
- What evidence is needed for each important value: page, span, citation, confidence, or source reference.
- How missing, ambiguous, conflicting, or low-confidence values should be represented.
- Where the workflow must avoid inferred values.

The goal is not just a JSON shape. The goal is a decision record a reviewer and auditor can trust.

---
<!-- slide:id=lesson-typed-extraction-choices -->

## Typed extraction choices and trade-offs

Key decisions:

- **Strict schema vs. flexible notes:** Strict schemas help automation; flexible notes may help SMEs explain unusual cases.
- **Confidence thresholds:** High thresholds reduce false approvals but increase review volume.
- **Evidence granularity:** More detailed evidence improves trust but can increase storage and UI complexity.
- **Failure behavior:** Empty-with-reason is safer than filling a field without support.

Trade-off to name explicitly: automation value depends on trustworthy uncertainty handling, not only high field coverage.

---
<!-- slide:id=lesson-typed-extraction-evidence -->

## Typed extraction evidence and checkpoint

Before the workflow can use extracted results, confirm:

- The output validates against the agreed schema.
- Important fields include evidence and confidence where appropriate.
- Missing and low-confidence fields follow a consistent policy.
- Unsupported values are not invented to satisfy the schema.
- Reviewers can see enough source context to challenge or confirm a value.

Checkpoint question: **Would a business reviewer understand what was extracted, why it was trusted, and what still needs attention?**

---
<!-- slide:id=lesson-human-review-context -->

## Lesson 5: Build review, correction, and handoff

Human review is part of the product design, not a fallback after automation fails.

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
- **Correction model:** Corrections should update the case record and feed evaluation, not silently overwrite history.
- **Approval boundary:** Decide which results can flow automatically and which require a named approver.
- **Handoff seam:** Treat downstream integration as a governed contract, not a direct write from unreviewed extraction.

Trade-off to name explicitly: reducing reviewer effort must not erase accountability.

---
<!-- slide:id=lesson-human-review-evidence -->

## Review evidence and checkpoint

Before handoff is trusted, confirm:

- Review rules are explicit and testable.
- A reviewer can correct, approve, reject, and explain the decision.
- Corrections are retained with document, evidence, reviewer, timestamp, and contract version.
- Approved results are handed off through a controlled interface.
- Exceptions have an owner and a resolution path.

Checkpoint question: **Can the customer prove who approved a result, what changed, and why it was sent downstream?**

---
<!-- slide:id=lesson-prove-and-observe-context -->

## Lesson 6: Evaluate and trace the workflow

A document workflow is ready only when it performs consistently across representative cases and can be diagnosed when it fails.

Discuss:

- Which quality measures matter: field accuracy, routing accuracy, false approvals, review rate, latency, and cost.
- Which adversarial or messy cases should be tested.
- What traces must show across intake, extraction, review, and handoff.
- How corrections become future evaluation evidence.

Evaluation should reflect real workflow risk, not only model output quality.

---
<!-- slide:id=lesson-prove-and-observe-choices -->

## Evaluation and tracing choices and trade-offs

Key decisions:

- **Holdout data:** Keep evaluation examples separate from tuning examples.
- **Quality gates:** Define thresholds for automation, review, and rejection.
- **Trace detail:** Capture enough context to debug without overexposing sensitive content.
- **Regression testing:** Re-run important cases when schemas, analyzers, prompts, or review rules change.

Trade-off to name explicitly: more automation without measurement increases hidden business risk.

---
<!-- slide:id=lesson-prove-and-observe-evidence -->

## Evaluation evidence and checkpoint

Before promotion, confirm:

- Representative test cases cover normal, edge, and failure segments.
- Field accuracy, review volume, false approval risk, and latency are measured.
- Traces connect document intake, extraction, policy, review, correction, and handoff.
- Failures have named causes and owners.
- The release decision includes rollback and monitoring expectations.

Checkpoint question: **Can the team defend the workflow with evidence rather than a successful demo?**

---
<!-- slide:id=lesson-deploy-context -->

## Lesson 7: Deploy the reviewable workflow

Deployment is the point where experimentation becomes an accountable business service.

Discuss:

- Who can invoke the workflow and under what identity.
- Which environment receives the pilot and what production controls are required.
- How analyzer or schema versions are promoted.
- How monitoring, support, rollback, and change management work.

The first deployment should be controlled, observable, and reversible.

---
<!-- slide:id=lesson-deploy-choices -->

## Deployment choices and trade-offs

Key decisions:

- **Pilot scope:** Start with a bounded document set, user group, and decision path.
- **Endpoint and identity:** Use authenticated access and managed identity where possible.
- **Versioning:** Track analyzer, schema, policy, review rules, and downstream contract together.
- **Operations:** Decide alert ownership, support process, rollback criteria, and release cadence.

Trade-off to name explicitly: broad rollout before operational readiness can create more manual work than it removes.

---
<!-- slide:id=lesson-deploy-evidence -->

## Deployment evidence and checkpoint

Before controlled rollout, confirm:

- The workflow runs behind approved access controls.
- Monitoring and tracing are enabled for the end-to-end path.
- Version and rollback information is documented.
- Review and correction data remain available after deployment.
- The pilot owner can decide whether to expand, pause, or revise the workflow.

Checkpoint question: **Is the workflow ready to serve a bounded real use case with accountable controls?**

---
<!-- slide:id=scenario-next-session -->

## Next working session

Bring the people and evidence needed to make the scenario real:

- One high-value document decision and its business owner.
- An approved source and 15–30 safe, representative samples.
- Expected fields, unacceptable errors, and review rules.
- SME, engineering, security, and workflow handoff owners.
- Current constraints for identity, retention, monitoring, and deployment.

Outcome: agree the first pilot slice and the evidence required before expansion.
