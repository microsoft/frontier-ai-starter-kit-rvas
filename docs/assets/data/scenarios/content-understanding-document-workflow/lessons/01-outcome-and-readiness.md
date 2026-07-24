# 1. Outcome and data readiness

## Goal

Frame one document decision as a measurable workflow outcome and establish whether the synthetic pack is sufficient for a safe learning exercise.

## Duration

35 minutes.

## Audience

Business SME, process owner, data/workflow owner, product owner, and facilitator. Engineering and security may observe.

## Preparation

- Read `accelerator/sample-data/README.md` and open the two tuning fixtures.
- Bring one candidate business decision, its decision user, and the consequence of a wrong decision.
- Print or copy the sample register below. Do not substitute real documents during the session.

| Fixture | Intended decision | Expected route | Challenge |
| --- | --- | --- | --- |
| `rfq-1001` | RFQ intake | procurement | routine RFQ |
| `invoice-2001` | invoice validation | accounts payable | arithmetic agrees |

## Timed exercise

| Time | Activity |
| --- | --- |
| 0–5 min | Name the decision, user, process owner, and current manual action. |
| 5–15 min | Inspect the tuning fixtures and identify the fields that change the decision. |
| 15–25 min | Define acceptable outcomes, unacceptable errors, and when a person must intervene. |
| 25–35 min | Complete the readiness statement and approve or block the next lesson. |

## Artifact

A one-page decision and data-readiness statement containing:

- decision, owner, user, and business action;
- error consequence and measurable success signal;
- authorized sample source/classification statement;
- expected fields, routes, and exception conditions;
- retention, source-access, and reviewer owners.

## Expected output

The team can state: “For this document class, when these fields are present and consistent, route to this workflow; otherwise send it to this named reviewer.” The statement explicitly says the supplied pack is synthetic.

## Validation

The facilitator checks that every named field maps to an action, every exception has an owner, and no real document or secret was introduced. Compare the two expected JSON files with their fixtures; then run the local validator:

```bash
python3 scenarios/content-understanding/scripts/validate_local_pack.py
```

## Debrief

Ask which error would cause the greatest business harm, which sample variation is missing, and whether confidence alone could decide the action. Record gaps rather than solving them with a threshold guess.

## Next decision

Choose whether the outcome is sufficiently defined to let the SME create a schema and test plan in Lesson 2.
