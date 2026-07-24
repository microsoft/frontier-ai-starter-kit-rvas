# Content Understanding and Document Workflow

## Customer outcome

A procurement or operations SME uses **Content Understanding Studio** to shape and test an analyzer for safe sample invoices, RFQs, or technical specifications. The SME is not asked to build an integration. Instead, they hand engineering a reviewable, portable JSON configuration contract and evidence from testing. Engineering connects the approved analyzer to a SharePoint/document-ingestion path or another business workflow, with human correction and lifecycle controls in place.

This is a document-workflow scenario—not a generic OCR or Document Intelligence demonstration.

## Delivery flow

1. **Choose one decision:** for example, route an RFQ, validate invoice fields, or flag a specification requirement.
2. **Prepare safe samples:** include representative layouts, suppliers, languages, poor scans, and known difficult cases. Record source, sensitivity, expected result, and whether each document may be used in Studio.
3. **SME builds in Studio:** define the document class and fields, test extraction/classification, inspect failures, and refine the analyzer/schema.
4. **Capture the handoff:** engineering receives a versioned JSON contract containing the analyzer identity/version or export reference, field definitions, document classes, test-set reference, acceptance thresholds, review rules, and owning contacts. Treat this contract as an application artifact; do not assume that a Studio export is portable across projects, tenants, or service versions.
5. **Integrate and review:** an ingestion service obtains documents from the approved SharePoint or business source, invokes the approved analyzer using a currently documented interface, stores results and confidence/evidence, and routes exceptions to people.
6. **Operate with evidence:** compare results with corrected outcomes, monitor drift and failures, retain audit records, and approve changes before promotion.

## Roles and boundaries

| Role | Accountable for |
| --- | --- |
| Business SME | Schema intent, representative samples, acceptance examples, review decisions |
| Data/workflow owner | Source authorization, retention, SharePoint/workflow ownership |
| Engineering | Current API integration, identity, error handling, records, release pipeline |
| Security/platform | Resource access, network/data controls, logging policy, separation decisions |
| Product owner | Thresholds, exception policy, lifecycle approval |

## Data readiness checklist

- A purpose, decision, and failure impact are stated for each document type.
- Samples are authorized, minimized, and safe for the selected environment; sensitive production files are not casually copied into Studio.
- Expected values and acceptable alternatives are recorded before testing.
- The sample set includes normal, edge, low-quality, and negative documents.
- Source access, retention, residency, and redaction requirements have owners.
- A reviewer can see the original document, extracted value, evidence/location where available, confidence, reason for exception, and correction history.

## Secure handoff and integration

Use a repository or approved configuration store for the portable contract. Protect it with change review, semantic versioning, and environment-specific references—not secrets. Keep secrets and service credentials in the platform's approved identity/secret mechanism. Engineering should map the contract to the target environment only after confirming that the Studio project/analyzer is accessible to the intended workload identity.

The workflow seam is intentionally simple:

`approved source → ingestion/normalization → current Content Understanding integration → confidence/policy decision → human review when needed → business system + evidence store`

For SharePoint, preserve source item/version identifiers and permissions rather than flattening documents into an ungoverned copy. A correction may update the business record, but it must also be retained as evaluation evidence.

## Human review policy

Do not treat confidence as an automatic approval. Define field- and decision-specific rules such as: missing required value, conflicting totals, unsupported document class, source policy violation, or confidence below a business-approved threshold. Human reviewers correct values, select a reason, and can reject the whole result. Escalate access-sensitive documents to the source owner rather than exposing them to a broad review queue.

## Lifecycle and evaluation from day one

Maintain a small, labeled holdout set that does not drive tuning. For each analyzer/configuration release, retain:

- contract version and analyzer/project reference;
- test documents or approved immutable references;
- expected and observed fields/classes;
- field-level quality, routing accuracy, review rate, and correction rate;
- failures segmented by supplier, layout, quality, language, and document type where permitted;
- approval decision, owner, date, and rollback reference.

Promotion should require agreed business measures, not an impressive single-document demonstration. Re-test after schema edits, source-template changes, workflow changes, or service updates.

## Maturity and design gaps

Content Understanding Studio can accelerate SME-led schema exploration, but it is not automatically a complete enterprise workflow platform. Service capabilities, project/analyzer boundaries, export behavior, RBAC, regional availability, and preview terms can change. Confirm the current product documentation and tenant behavior before design commitments.

In particular, do **not** assume that a Studio project or analyzer is a strong security boundary, that sharing an analyzer safely shares only the intended data, or that an export can be imported unchanged into every environment. Use separate environments/resources where isolation is required, enforce document-source permissions outside the analyzer, and design an explicit promotion and access model with security stakeholders.

## Search before implement

Before engineering writes Azure SDK, REST, SharePoint, or workflow code:

1. Search current Microsoft documentation/MCP for the supported Content Understanding resource, project/analyzer lifecycle, authentication, and invocation surface.
2. Confirm the Studio-created analyzer can be reached by the intended workload identity in the target environment.
3. Load the relevant Foundry/Azure skill and follow the verified pattern.
4. Implement only against the verified signature, then validate with safe documents and the recorded evaluation set.

This scenario deliberately does not publish guessed SDK or REST signatures.

## Materials

- [Customer conversation slides](slides.md)
- [Facilitator guide](FACILITATOR.md)
- [Local demo runbook](LOCAL_DEMO.md)
- [Lesson 1: outcome and readiness](lessons/01-outcome-and-readiness.md)
- [Lesson 2: SME Studio loop](lessons/02-sme-studio-loop.md)
- [Lesson 3: secure handoff and workflow](lessons/03-secure-handoff-and-workflow.md)
- [Lesson 4: review, evaluation, and lifecycle](lessons/04-review-evaluation-lifecycle.md)
- [Accelerator](accelerator/README.md)
