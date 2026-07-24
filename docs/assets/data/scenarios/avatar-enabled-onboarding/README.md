# Avatar-enabled Onboarding

**Version 0.1.0 · Customer-delivery scenario**

Create an employee onboarding experience from approved policy and program content. The outcome is not an avatar demo: it is a controlled, inclusive learning journey whose published messages can be traced, approved, measured, and improved.

## Customer outcome

A new employee receives a short, clear onboarding experience in a suitable channel, can use captions, transcript, language, and non-video alternatives, and can give feedback or ask for help. Content owners can answer: *what was said, which approved source supported it, who approved it, where was it delivered, and what happened afterward?*

## Delivery flow

| Stage | Customer decision and output | Required control |
| --- | --- | --- |
| 1. Approved content | Identify authoritative policy, benefits, safety, and welcome content; assign content owner and expiry/review date. | Source ID, version, owner, and approved claim list. |
| 2. Script and storyboard | Produce a concise script, scene plan, accessibility plan, and claim-to-source links. | Do not introduce claims absent from the approved pack. |
| 3. SME, legal, and brand approval | Review factual accuracy, employment/legal implications, privacy, disclosure, visual identity, and localization. | Named human approvers; changes return to the script stage. |
| 4. Avatar, voice, and channel choice | Select avatar presentation, voice, languages, and channels after a vendor/platform assessment. | Consent and likeness policy; accessible alternative; channel owner. |
| 5. Employee experience | Publish the approved version with an avatar disclosure, captions, transcript, help path, and feedback prompt. | No production publish without the approval record. |
| 6. Feedback and operational evidence | Review completion, accessibility use, questions, sentiment, defects, and support handoffs. | Evidence is aggregated and minimized; content changes restart approval. |

## Grounding and traceability

Each script segment carries a source reference such as `ONB-001@2026-07-01#benefits-enrolment`. The production record keeps:

- approved source ID and version;
- script and storyboard revision;
- SME, legal, and brand decisions with timestamps;
- selected avatar/voice/channel configuration identifier;
- publication date, audience, locale, and withdrawal/review date; and
- feedback and operational metrics associated with the published revision.

A knowledge source can assist drafting or answer employee questions only when access, permissions, and citations are appropriate. It must not silently replace the approved-content pack for a published script.

## Platform and vendor decision

This scenario is intentionally vendor-neutral. Evaluate candidates against the customer’s requirements rather than assuming an avatar or voice service is available:

1. **Trust and rights** — disclosure controls, avatar likeness/voice consent, data residency, retention, training-data terms, and incident support.
2. **Experience** — caption quality, transcripts, keyboard/mobile access, language and regional voice coverage, WCAG conformance evidence, and a non-avatar fallback.
3. **Operations** — approval workflow integration, audit export, content/version management, identity and channel integration, observability, cost, and exit path.
4. **Safety and brand** — prohibited use, moderation, restricted content, brand controls, and escalation to a human owner.

Do not use a real person’s likeness or clone a voice without explicit, recorded authorization. Clearly label the experience as avatar-generated or AI-assisted where an employee could reasonably mistake it for a human presenter. Never position the avatar as a human employee or authority beyond its approved role.

## Workshop use

1. Follow `FACILITATOR.md`, review `slides.md`, and complete Lessons 1–4 using one real onboarding topic.
2. Use the complete fictional pack in `accelerator/sample-data/` to demonstrate claims, approvals, the script, transcript, accessible fallback, and aggregated feedback.
3. Run `local-demo.md` to render a traceable mock artifact from only the approved claims.
4. Replace the sample only with a small, sanitized customer-approved pack; do not fabricate policy answers.
5. Decide the pilot cohort, measures, review cadence, and the human owners who can approve, pause, or withdraw content.

## Demo boundaries

The accelerator supplies an approved-content contract and deployment seam, not an avatar runtime or a landing zone. A clean demo can use the sample pack and a mock rendering/channel adapter. A bring-your-own (BYO) environment connects the customer’s selected platform after security, privacy, accessibility, and procurement reviews. No vendor SDK signatures are assumed here.

## Scenario assets

- `FACILITATOR.md` — 90-minute facilitated-workshop runbook.
- `local-demo.md` — dependency-free local demonstration instructions.
- `validate.py` — static validation for the blueprint, fixture, lesson structure, and manifest.
- `accelerator/mock_renderer.py` — deterministic local mock that rejects unapproved content and writes a traceable JSON artifact.

## Search before implement

Before connecting any avatar, voice, channel, workflow, or knowledge service:

1. Search the selected vendor’s current official documentation and the customer’s approved architecture standards.
2. Verify current APIs, service availability, data handling, accessibility support, and identity model.
3. Map the approved-content fields and approval record to the selected platform’s verified integration points.
4. Test disclosure, captions/transcript, language fallback, audit evidence, and withdrawal before pilot publication.
