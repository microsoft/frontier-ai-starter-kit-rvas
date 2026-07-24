# Lesson 1 — Establish the approved-content pack

## Goal

Define exactly what the experience may say before anyone writes a script.

## Duration

20 minutes.

## Audience

Content owner, onboarding lead, subject-matter expert (SME), legal/compliance representative, and facilitator.

## Prep

Bring one sanitized onboarding source, its owner and review date, and the fictional `../accelerator/sample-data/claims.json` structure. Do not paste customer policy into the sample fixture.

## Timed activity

| Time | Activity |
| --- | --- |
| 0–4 min | Select one employee moment, cohort, locale, and channel. Name its accountable content owner. |
| 4–12 min | Split the source into atomic, testable claims. For each, record source ID, version, owner, review date, audience, locale, reviewer, and human help route. |
| 12–16 min | Mark claims requiring SME or legal review. Remove any statement without an authoritative source. |
| 16–20 min | Agree the invalidation rule: a source change pauses linked publication until it is reviewed again. |

## Artifact

An approved-claims list using the `claims.json` fields.

## Expected output

Every proposed spoken statement has one claim ID, a versioned source reference, a named owner, a review date, and an escalation path.

## Validation

Read the list aloud. If a participant cannot name the authoritative source or owner for a statement, remove it. Run `python3 ../validate.py` after using the supplied fixture.

## Debrief

Which statements felt useful but could not be grounded? Those are questions for a human owner, not material for an avatar.

## Next decision

Confirm the claim set that may enter the script and storyboard in Lesson 2.
