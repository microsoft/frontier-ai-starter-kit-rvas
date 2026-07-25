# AI Grounding / IQ facilitator guide

## Purpose and outcome

Facilitate a 3-hour decision workshop that produces a bounded AI-grounding pilot decision, not a service deployment. Participants leave with an outcome and access boundary, decision map, context-pattern record, golden dataset, and operating-evidence plan.

Use only the fictional Northstar Outdoor Supply fixtures. Do not request, paste, or collect customer records, tenant identifiers, secrets, or production configuration.

## Before the workshop

- Invite a business decision owner, frontline representative, source owner, platform architect, security/privacy reviewer, evaluator, and operations lead.
- Share `README.md`, the seven lesson files, and `accelerator/sample-data/README.md`.
- Run the local simulation and validator in `accelerator/LOCAL-DEMO.md`; use the resulting evidence artifact to show how citations and refusal tests are reviewed.
- Arrange a shared canvas with seven sections matching the scenario modules.

## Agenda

| Time | Module | Facilitator result |
|---|---|---|
| 0–10 min | Opening | Confirm the workshop is about a decision and evidence, not “building RAG.” |
| 10–45 min | Lesson 1 | One outcome and access boundary. |
| 45–80 min | Lesson 2 | One decision map and explicit stop cases. |
| 80–90 min | Break | Preserve unresolved assumptions in the decision record. |
| 90–130 min | Lesson 3 | Selected context pattern and rejected alternative. |
| 130–175 min | Lesson 4 | Reviewable golden dataset and scoring rules. |
| 175–210 min | Lesson 5 and close | Operating-evidence plan and limited-pilot decision. |

## Facilitation moves

Start every discussion with “What action changes if this answer is good?” Ask source owners—not the implementation team—to state authority, update cadence, and prohibited use. When a participant says “the assistant should know,” ask which source proves it, which role may see it, and what citation a reviewer needs.

Keep access-denied and unsupported-evidence cases separate. An access denial means relevant content exists but the role may not use it; an unsupported request means no approved evidence supports a response. Both must avoid invented answers and must have a safe handoff.

Do not select an IQ product from this package. Assign an owner to verify current Microsoft documentation, source support, permission behavior, region, network, and evaluation capabilities before implementation.

## Pilot gate

Approve only a limited pilot when all conditions are true:

1. A named business owner accepts the bounded outcome and non-goals.
2. Every source has an owner, authority statement, and permission decision.
3. The selected pattern and alternatives are recorded, pending current capability verification.
4. Business and security reviewers accept golden cases for ordinary, freshness, access-denied, prohibited, and unsupported requests.
5. Operating owners can retain evidence and act on source, permission, context, or incident changes.

Otherwise choose **iterate**, **pause**, or **return to source governance**. Do not treat a successful local simulation as a production authorization decision.
