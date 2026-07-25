# Extra · Document Workflow

> Reusable implementation mechanics. Prerequisite: a deployed Foundry/Azure project and an identity
> that can use its Document Intelligence or Content Understanding resource. Use only fictional,
> synthetic, or approved documents; do not upload real applicant/customer records.

Build a reviewable intake workflow, not an automatic admissions decision:

```text
local document → layout/OCR → field confidence + rules → human review → structured JSON
                                      └──────────── trace + evaluation evidence ────────────┘
```

## Before you write SDK code

Document Intelligence SDK and REST signatures change. **First search `microsoft-docs` MCP** for the
current Python Document Intelligence layout-analysis example, authentication/RBAC guidance, and
poller signature. Record the URLs or search titles you consulted in your build notes. Then load the
project `azure-ai` skill reference and implement the current signature you found. Do not copy an
old key-based sample.

Use keyless auth: `DefaultAzureCredential`, with `az login` locally and a managed identity when
deployed. Microsoft Entra authentication requires a Document Intelligence **custom subdomain** endpoint,
not a regional endpoint. Keep `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` in environment configuration; never
put a key, connection string, or applicant data in source or trace logs.

## Build `document_workflow.py`

Create this learner-owned file in this activity directory (or pass its directory with `--path`).
Use a harmless fictional PDF/image, such as a sample application containing invented
name, program, and consent fields.

### Step 1 — Intake and layout/OCR

1. Accept a local document and generate a non-sensitive correlation ID.
2. Call the current Document Intelligence layout/OCR API signature discovered above.
3. Preserve page, line/table, and bounding-region references needed for a reviewer; do not log raw
   document content.

**Verify:** a fictional application produces extracted layout text/tables with source references.

### Step 2 — Confidence and validation

1. Define a named confidence threshold (for example, `0.85`) and compare extracted field confidence
   with it.
2. Validate required demo fields: applicant ID, intended program, and consent acknowledgement.
3. Treat a missing field, invalid format, or low confidence as **needs review**. Never infer missing
   data or make an admissions decision.

**Verify:** deliberately blur or omit a fictional field and show that it is held for review.

### Step 3 — Human review and approval

Route held items to a named human-review/approval queue with the reason and source reference. A
reviewer must be able to correct a field and explicitly approve or reject the intake record. The
workflow may prepare a record; it must not approve an applicant automatically.

**Verify:** demonstrate one low-confidence document routed to review and one reviewer-approved
fictional record.

### Step 4 — Structured result and proof

Write a JSON result with a stable shape such as:

```json
{
  "intake_id": "opaque-correlation-id",
  "status": "needs_review",
  "fields": [{"name": "intended_program", "value": "Demo Program", "confidence": 0.82, "source": {"page": 1}}],
  "review": {"required": true, "reason": "confidence_below_threshold"}
}
```

Also produce evidence from a **fictional** evaluation set: a trace/correlation ID, latency and
outcome (without document text), plus an evaluation summary with field accuracy, low-confidence
review rate, and false-approval count. Explain failures and threshold trade-offs.

## Offline checkpoint

The validator never imports Azure packages or contacts Azure:

```bash
python validate.py --step intake
python validate.py --all --path .
python validate.py --all --path ./my-submission --dry-run
```

It only inspects `document_workflow.py`; passing it is not proof of a live extraction, correct RBAC,
human approval, or safe handling of real records.

## What you built

A keyless, auditable document-intake path for a safe document workflow: OCR/layout informs a structured
record, uncertainty reaches a person, and traces/evaluations show whether the workflow deserves trust.
