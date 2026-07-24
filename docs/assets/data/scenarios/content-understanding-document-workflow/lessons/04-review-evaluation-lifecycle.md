# 4. Review, evaluation, and lifecycle

## Goal

Set a review policy, evaluate holdout behavior, and make an evidence-based release or hold decision.

## Duration

45 minutes.

## Audience

Product owner, business SME, reviewer lead, engineering lead, operations owner, and facilitator.

## Preparation

- Bring the handoff contract and workflow trace from Lesson 3.
- Read the golden cases and the correction record for `invoice-2002`.
- Set aside a place to record a release decision and rollback owner.

## Timed exercise

| Time | Activity |
| --- | --- |
| 0–10 min | Define review triggers: missing required field, contradictory value, unsupported class, source-policy violation, and sensitive access case. |
| 10–20 min | Compare the two golden expected results with the policy; verify each review reason has a reviewer and disposition. |
| 20–30 min | Inspect `corrections/invoice-2002-correction.json` and decide what correction evidence must be retained without overwriting the original result. |
| 30–40 min | Define field quality, route quality, review rate, correction rate, and failure segments for a future approved test run. |
| 40–45 min | Record approve, defer, or rollback decision criteria and the accountable owner. |

## Artifact

A review-policy table, holdout evaluation record, correction-retention rule, release decision record, and rollback reference.

## Expected output

The team can explain why the golden cases do not auto-approve, how `invoice-2002` is corrected to `220.00` by a reviewer, and why the original contradictory extraction remains part of the evidence.

## Validation

Check that the policy covers both golden review reasons; the correction changes a known field without changing the original expected JSON; and release criteria use holdout evidence rather than a successful tuning example. Run the validator and review:

```bash
python3 scenarios/content-understanding/scripts/validate_local_pack.py
```

The evidence must report four checked fixtures, two golden cases, and no errors before the facilitator marks this workshop pack complete.

## Debrief

Ask which failure segments need more authorized synthetic examples, what event triggers re-evaluation, and who can stop promotion. Do not infer production readiness from this local exercise.

## Next decision

Decide whether to authorize a separately governed discovery/implementation plan, defer for missing evidence, or repeat the workshop with revised safe fixtures.
