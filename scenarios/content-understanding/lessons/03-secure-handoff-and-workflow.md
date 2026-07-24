# 3. Secure handoff and workflow

## Goal

Produce a reviewable handoff contract and a source-to-review workflow design that preserves ownership and does not treat an analyzer as a security boundary.

## Duration

40 minutes.

## Audience

Engineering lead, business SME, workflow/source owner, security/platform representative, and facilitator.

## Preparation

- Bring Lesson 2's schema and test-observation log.
- Read `accelerator/main.bicep` and `accelerator/parameters.example.json` as planning-only artifacts.
- Open `accelerator/sample-data/result-contract.json`; it is a workshop JSON contract, not an SDK response definition.

## Timed exercise

| Time | Activity |
| --- | --- |
| 0–10 min | Identify source, source identity/version, owner, retention rule, and who may review each exception. |
| 10–20 min | Draft the handoff contract: schema version, analyzer/project reference placeholder, test-set reference, review rules, owners, and release status. |
| 20–30 min | Draw `approved source → ingestion → approved integration → policy → human review → system of record + evidence`. Mark where permission checks occur. |
| 30–35 min | Compare the four expected results and decide how their routes map to the workflow. |
| 35–40 min | Record unknown current-service details that engineering must verify before implementation. |

## Artifact

A versioned, secret-free handoff contract plus a workflow trace that identifies source identity, access checks, evidence storage, exception queue, and system-of-record update.

## Expected output

The team has an engineering-ready contract that contains references and policy, not credentials; a workflow trace that preserves document provenance; and an explicit list of unresolved platform decisions.

## Validation

The facilitator verifies that the contract has no endpoint, key, or copied source document; that it distinguishes environment references from secrets; and that each route in the expected JSON has a workflow owner. Run:

```bash
python3 scenarios/content-understanding/scripts/validate_local_pack.py
```

Review the generated evidence file before approving the handoff.

## Debrief

Ask where authorization is actually enforced, whether reviewer access exceeds source access, and what breaks if the source item changes while it is in review.

## Next decision

Choose whether the platform team can approve an implementation discovery phase, or whether access, retention, and environment isolation must be decided first.
