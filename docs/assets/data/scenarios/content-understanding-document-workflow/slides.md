---
marp: true
paginate: true
title: Content Understanding and Document Workflow
description: Customer conversation deck
version: 0.1.0
---

# Content Understanding and Document Workflow

**Customer conversation · v0.1.0**  
From SME-led understanding to a governed business decision.

---

## Start with a decision, not a document demo

- Route an RFQ to the right team
- Validate invoice information before posting
- Surface requirements from a technical specification

Success is a reliable workflow outcome, not extraction on one attractive sample.

---

## The SME self-service loop

1. Use authorized, safe samples in Content Understanding Studio.
2. Define classes, fields, and expected outcomes.
3. Test normal and difficult documents.
4. Refine the analyzer/schema with business context.
5. Record acceptance examples and unresolved cases.

The SME owns meaning; engineering owns production integration.

---

## Data readiness is a delivery gate

| Ready | Not ready |
| --- | --- |
| Representative and authorized samples | A single cleaned-up PDF |
| Expected values and failure cases | “It looks right” |
| Source/retention owner | Uncontrolled document copies |
| Review and correction owner | Automation with no exception path |

---

## Handoff: portable contract, not a promise

The SME hands off a reviewed JSON contract:

- analyzer/project reference and version
- schema and document classes
- test-set and acceptance evidence
- routing/review policy
- contacts, ownership, and change record

Engineering validates portability and access in each environment. An export is not assumed to be a cross-project or cross-tenant deployment package.

---

## Production workflow seam

`SharePoint or business source → ingestion → analyzer → policy → human review → system of record`

- Preserve source identity, version, and permissions.
- Use approved workload identity and secrets handling.
- Store the result, evidence, correction, and contract version together.

---

## Human correction is designed in

Review when values are missing, inconsistent, uncertain, unsupported, or sensitive.

Reviewers need document context, extracted evidence, a correction reason, and a way to reject a result. Corrections become the next evaluation signal.

---

## Evidence from the first iteration

- Holdout examples distinct from tuning examples
- Field quality and routing accuracy
- Review and correction rates
- Failure segments: layout, supplier, language, scan quality
- Release approval and rollback reference

No promotion on a demo alone.

---

## Honest service maturity discussion

Studio enables rapid SME experimentation, but it is not automatically the enterprise security, promotion, or workflow layer.

Confirm current service availability, analyzer/project segmentation, RBAC, export behavior, and supported APIs before committing to an operating model. Put document access controls and environment isolation where they are actually enforced.

---

## A small accelerator, then a real design

1. Review the resource-free planning blueprint.
2. Validate the safe local fixture pack and expected outcomes.
3. Capture the JSON handoff and evaluation evidence.
4. Separately verify the current supported integration path.
5. Decide what must be engineered for scale, isolation, and lifecycle.

---

## Next customer working session

Bring:

- one high-value decision;
- 15–30 safe, representative samples;
- a source/workflow owner and SME;
- expected outputs and unacceptable errors;
- security and environment constraints.

**Question:** which document decision creates value when people spend less time finding, checking, or rekeying information?
