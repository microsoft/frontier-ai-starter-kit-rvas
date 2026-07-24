# Facilitator guide: Content Understanding and document workflow

## Purpose and boundary

This is a 2-hour-45-minute facilitated decision workshop. It uses only the synthetic local pack under `accelerator/sample-data/`. It does not provision Azure, call an SDK, upload a document, or validate a service capability.

The outcome is a reviewed decision package: business outcome, SME schema/test record, secret-free handoff, review/evaluation policy, and a next decision. It is not production approval.

## Before participants arrive

1. Read [LOCAL_DEMO.md](LOCAL_DEMO.md) and run the validator from the repository root.
2. Confirm that every exercise will use only the four synthetic fixtures.
3. Invite a business SME, process owner, source/workflow owner, product owner, engineering lead, and security/platform representative.
4. Prepare a shared space for the four lesson artifacts and a release-decision record.
5. Do not request endpoints, keys, tenant identifiers, screenshots of customer documents, or live service access.

## Agenda

| Module | Time | Outcome |
| --- | ---: | --- |
| [1. Outcome and data readiness](lessons/01-outcome-and-readiness.md) | 35 min | decision/readiness statement |
| [2. SME Studio loop](lessons/02-sme-studio-loop.md) | 45 min | schema/test-observation log |
| [3. Secure handoff and workflow](lessons/03-secure-handoff-and-workflow.md) | 40 min | handoff contract and workflow trace |
| [4. Review, evaluation, and lifecycle](lessons/04-review-evaluation-lifecycle.md) | 45 min | review policy and release decision |

Allow 5-minute breaks between modules if the session runs longer than two hours.

## Facilitation method

- Start each module by reading its goal, expected output, and next decision aloud.
- Use `rfq-1001` and `invoice-2001` only as tuning discussion examples. Keep the golden fixtures hidden until Lesson 2's holdout exercise.
- Have the SME explain field meaning and the product owner explain the business action. Do not turn a confidence value into an approval rule without a business policy.
- Record unknowns as decisions or risks. Do not resolve them by inventing a service API, capability, or security boundary.
- Run the local validator after Lessons 1, 2, and 4. Save its deterministic JSON evidence with the workshop artifacts.

## Required workshop outputs

1. Decision/readiness statement with owners and unacceptable errors.
2. Versioned SME schema and test-observation log.
3. Secret-free handoff contract and source-to-review workflow trace.
4. Review-policy table, golden-case evaluation record, correction-retention rule, and approve/defer/rollback decision.
5. `evidence/local-validation.json` showing a passing fixture-pack validation.

## Safety and escalation

Stop the exercise if a participant introduces real documents, credentials, customer identifiers, or unapproved screenshots. Replace the item with a synthetic placeholder and record the gap.

Escalate these decisions to the named owner rather than resolving them in the room:

- service availability, supported formats, product lifecycle, and APIs;
- document-source permissions, reviewer access, retention, and residency;
- environment isolation, workload identity, logging, and promotion controls;
- acceptance thresholds, production rollout, and rollback authority.

## Closing prompt

Ask: “Given the evidence produced today, should we authorize separate implementation discovery, repeat the safe exercise with better examples, or defer?” Record the accountable owner and date for the chosen next step.
