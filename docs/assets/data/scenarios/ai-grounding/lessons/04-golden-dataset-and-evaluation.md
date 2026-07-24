# Lesson 4 — Golden dataset and evaluation from the beginning

## Goal

Create a reviewable golden set that tests answer quality, citations, freshness, refusals, and access before a source connection is scaled.

## Duration

45 minutes.

## Audience

Business reviewer, source owner, security reviewer, evaluator, frontline practitioner, and facilitator.

## Preparation

Bring the selected decision record and representative examples. Review the fictional `../accelerator/golden-questions.json` and its evidence artifact; replace neither with real data during this workshop.

## Timed activity

| Time | Facilitation step |
|---|---|
| 0–10 min | Define the fields for role, request, allowed sources, expected action, citations, reviewer, and pass rule. |
| 10–25 min | Write two routine, one ambiguous, one stale/conflicting, one access-denied, and one unsupported-evidence case. |
| 25–35 min | Specify exact citation/provenance expectations and the safe refusal or escalation for each negative case. |
| 35–45 min | Independently score two cases with business and security reviewers; reconcile disagreements. |

## Artifact

A versioned golden dataset with acceptance criteria and named reviewers. The fictional local example is `../accelerator/golden-questions.json`.

## Expected output

The fixture includes policy, transit-damage, current-service-notice, supervisor-only, private-data refusal, and unsupported-refund cases with expected source IDs.

## Validation

Every case has an expected behavior and citation list; every refusal has a reason and must cite nothing; reviewers can score it without implementation code.

## Debrief

Ask: “Would we detect a plausible but unauthorized answer?” If not, add a case rather than lowering the acceptance threshold.

## Next decision

Choose the evidence events, owners, and review triggers needed to operate this golden set after pilot launch.
