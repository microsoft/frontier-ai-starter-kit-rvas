# 2. SME Studio loop

## Goal

Turn the approved decision into an SME-owned schema, test observations, and acceptance examples without claiming an implementation API or service result.

## Duration

45 minutes.

## Audience

Business SME, process owner, facilitator, and an engineering observer.

## Preparation

- Complete Lesson 1's decision statement.
- Open `rfq-1001` and `invoice-2001` as tuning examples.
- Keep `rfq-1002` and `invoice-2002` unopened until the holdout check.
- Use current product documentation if a live Studio demonstration is authorized; this module does not require one.

## Timed exercise

| Time | Activity |
| --- | --- |
| 0–10 min | Define document classes, required fields, accepted alternatives, and evidence a reviewer needs. |
| 10–20 min | Walk the tuning fixtures and write the expected JSON shape in business language. |
| 20–30 min | Identify an intentional change the SME would make after an observed error; record the reason and affected examples. |
| 30–40 min | Reveal the two golden fixtures and predict route/review outcomes before reading their expected JSON. |
| 40–45 min | Record acceptance examples and unresolved cases. |

## Artifact

A schema and test-observation log with document classes, field definitions, accepted alternatives, sample IDs, expected routes, change rationale, and unresolved cases.

## Expected output

The SME can distinguish tuning examples from holdout evidence and can explain why `rfq-1002` needs review for its missing delivery date and `invoice-2002` needs review for its conflicting total.

## Validation

Confirm the schema log includes all four fixture IDs and that no golden case drove the proposed schema change. Inspect:

- `accelerator/sample-data/expected/rfq-1002.json`
- `accelerator/sample-data/expected/invoice-2002.json`
- `accelerator/sample-data/golden-cases.json`

Run the local validator and attach `evidence/local-validation.json` to the workshop notes.

## Debrief

Ask what business context the SME supplied that a generic extraction example could not. Ask which uncertainty needs a policy decision rather than further schema tuning.

## Next decision

Decide whether the schema, acceptance examples, and unresolved cases are ready for a versioned engineering handoff.
