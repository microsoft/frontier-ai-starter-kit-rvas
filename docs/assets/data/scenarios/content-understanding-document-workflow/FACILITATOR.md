# Facilitator guide: Content Understanding and document workflow

## Purpose and boundary

This is a 2-hour-45-minute facilitated decision workshop. It uses only the synthetic local pack under `accelerator/sample-data/`. It does not provision Azure, call an SDK, upload a document, or validate a service capability.

The outcome is a reviewed decision package: business outcome, SME schema/test record, secret-free handoff, review/evaluation policy, and a next decision. It is not production approval.

## Before participants arrive

1. Work through the seven modules yourself once, so the Verify steps are familiar before you run them in front of a room.
2. Confirm that every exercise will use only the four synthetic fixtures.
3. Invite a business SME, process owner, source/workflow owner, product owner, engineering lead, and security/platform representative.
4. Prepare a shared space for the seven module artifacts and a release-decision record.
5. Do not request endpoints, keys, tenant identifiers, screenshots of customer documents, or live service access.

## Agenda

| Module | Time | Outcome |
| --- | ---: | --- |
| [1. Provision the shared Foundry foundation](lessons/01-provision-foundation.md) | 25 min | foundation and region decision |
| [2. Connect an approved document source](lessons/02-document-source.md) | 25 min | source ownership and access contract |
| [3. Select the extraction capability](lessons/03-extraction-selection.md) | 25 min | Content Understanding / Document Intelligence decision |
| [4. Implement typed extraction with evidence](lessons/04-typed-extraction.md) | 35 min | typed output and evidence record |
| [5. Build review, correction, and handoff](lessons/05-human-review.md) | 30 min | review workflow and handoff contract |
| [6. Evaluate and trace the workflow](lessons/06-prove-and-observe.md) | 25 min | evaluation and trace evidence |
| [7. Deploy the reviewable workflow](lessons/07-deploy.md) | 25 min | controlled deployment decision |

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
5. An extraction result the team compared field by field against the source document.

## Safety and escalation

Stop the exercise if a participant introduces real documents, credentials, customer identifiers, or unapproved screenshots. Replace the item with a synthetic placeholder and record the gap.

Escalate these decisions to the named owner rather than resolving them in the room:

- service availability, supported formats, product lifecycle, and APIs;
- document-source permissions, reviewer access, retention, and residency;
- environment isolation, workload identity, logging, and promotion controls;
- acceptance thresholds, production rollout, and rollback authority.

## Closing prompt

Ask: “Given the evidence produced today, should we authorize separate implementation discovery, repeat the safe exercise with better examples, or defer?” Record the accountable owner and date for the chosen next step.
