---
marp: true
title: Avatar Scenario Customer Discussion Deck
paginate: true
---
<!-- slide:id=scenario-open -->

# Avatar Scenario
## A governed, accessible avatar-led experience

This workshop is about deciding how an avatar-led experience can help employees understand approved onboarding content while keeping human ownership, disclosure, accessibility, and operating evidence intact.

**Customer question:** What would make this trustworthy enough to pilot?

---
<!-- slide:id=lesson-experience-selection-context -->

# Module 1 — Context
## Select the experience capability

Not every onboarding moment needs the same experience. A short policy update, a multilingual welcome, a live support moment, and a replayable training segment each imply different choices.

We start by separating the **customer experience goal** from the technology option:

- What should the employee be able to understand or do afterward?
- Does the moment need video, avatar presence, live interaction, translated video, plain audio, or text?
- Which audience, locale, channel, and accessibility needs define the first pilot?
- Where would synthetic media help clarity, and where might it reduce trust?

---
<!-- slide:id=lesson-experience-selection-choices -->

# Module 1 — Choices and trade-offs
## Match capability to risk and value

Compare experience options against the actual pilot need:

- **Batch avatar video:** good for reviewed, reusable messages; slower to change.
- **Real-time avatar:** more interactive; higher latency, consent, moderation, and support expectations.
- **Voice or audio-first:** lower production weight; may meet accessibility and channel needs better.
- **Video translation:** useful when source video already exists; requires careful approval of translated meaning.
- **No avatar:** still valid when disclosure, accessibility, cost, or trust argues for a simpler format.

The decision should include consent, likeness and voice rights, supported regions, identity model, pricing shape, accessibility coverage, content-safety controls, and exit path.

---
<!-- slide:id=lesson-experience-selection-evidence -->

# Module 1 — What must be true
## A capability decision the sponsor can defend

By the end of this module, the team should have a short decision record that explains:

- selected experience capability and why it fits the pilot
- alternatives considered and why they were not selected
- consent, disclosure, accessibility, privacy, residency, and retention assumptions
- operating owner, support path, and conditions that would stop or simplify the experience

**Discussion:** If the avatar option became unavailable tomorrow, could the onboarding outcome still be delivered safely?

---
<!-- slide:id=lesson-foundation-context -->

# Module 2 — Context
## Provision the Foundry and Speech foundation

The scenario needs a foundation that lets teams build without turning every prototype into a one-off integration.

The foundation should support:

- keyless access patterns where possible
- a model and grounding path for drafting and review
- Speech or media services for the selected experience capability
- search or knowledge access for approved onboarding content
- telemetry that helps owners understand behavior without over-collecting employee data

This is the shared base for future policy, learning, and multilingual communication scenarios.

---
<!-- slide:id=lesson-foundation-choices -->

# Module 2 — Choices and trade-offs
## Reusable platform, not hard-coded demo

Key design choices shape how easily the pilot can become a repeatable pattern:

- **Identity:** managed identity and role-based access reduce secret handling, but require clear ownership.
- **Region and capacity:** availability, latency, data residency, and cost may point to different deployment choices.
- **Model path:** a general model may be enough for drafting; stricter use cases may need more evaluation and guardrails.
- **Observability:** useful traces help diagnose issues, but message content capture must be intentional and governed.
- **Seams:** keep rendering, assistant, content, and approval components replaceable.

The goal is a foundation customers can adapt, not a locked architecture.

---
<!-- slide:id=lesson-foundation-evidence -->

# Module 2 — What must be true
## A foundation ready for governed work

The bar is not “the services exist.” It is whether the foundation supports accountable operation:

- required resources are provisioned with the intended identity model
- environment settings are documented without exposing secrets
- content, assistant, rendering, approval, and telemetry components can connect
- owners know where logs, traces, and configuration evidence will live
- the platform team understands what must change for a real customer tenant

**Discussion:** Can the team explain who can access what, why, and how that access is reviewed?

---
<!-- slide:id=lesson-content-pipeline-context -->

# Module 3 — Context
## Build the governed content pipeline

The avatar must not become an unreviewed policy source. It should express approved content, not invent it.

For every claim used in the experience, the pipeline needs:

- source, version, owner, and review cycle
- audience and locale
- sensitivity and escalation route
- expiry or withdrawal conditions
- traceability from source to script segment

This turns onboarding content into a controlled input for the assistant, storyboard, approvals, and final experience.

---
<!-- slide:id=lesson-content-pipeline-choices -->

# Module 3 — Choices and trade-offs
## Govern claims without slowing every edit

Teams need enough control to protect employees without making simple updates impossible.

Discussion choices:

- What counts as an approved source: policy page, HR guide, learning page, legal FAQ, or SME note?
- Which changes need full reapproval versus owner review?
- How granular should claims be for traceability?
- How are locale-specific policy differences handled?
- Who can retire, pause, or replace content when guidance changes?

The trade-off is speed versus confidence. The practical answer is usually a small, well-owned pilot corpus.

---
<!-- slide:id=lesson-content-pipeline-evidence -->

# Module 3 — What must be true
## Versioned claims with named ownership

What you should have is a traceable claim set that downstream steps can rely on:

- each claim has an authoritative source and owner
- versions and expiry rules are visible
- sensitive topics are marked with review and escalation requirements
- unapproved or expired material is excluded from drafting
- the source-to-script relationship can be shown to reviewers

**Discussion:** If an employee challenges a statement in the avatar experience, can the owner show where it came from and whether it was current?

---
<!-- slide:id=lesson-grounded-assistant-context -->

# Module 4 — Context
## Build the grounded assistant behind the experience

The assistant helps draft scripts, answer reviewer questions, and propose employee-facing language. It must stay grounded in approved content.

Expected behavior:

- cite approved sources when making claims
- refuse or escalate when content is missing or expired
- avoid policy interpretation beyond the approved corpus
- support human review rather than replacing it
- preserve a clear path from source to script to final experience

The assistant is useful only if reviewers can see why it said what it said.

---
<!-- slide:id=lesson-grounded-assistant-choices -->

# Module 4 — Choices and trade-offs
## Helpful drafting versus unsafe authority

The assistant can speed preparation, but it should not become the decision-maker.

Design choices include:

- how strict retrieval should be before drafting
- whether the assistant answers employee questions directly or routes to human support
- how it handles missing, conflicting, or stale content
- what tone and reading level it uses for onboarding audiences
- how citations appear for reviewers versus employees

The safer pattern is to make the assistant excellent at grounded drafting, refusal, and escalation before broad interaction.

---
<!-- slide:id=lesson-grounded-assistant-evidence -->

# Module 4 — What must be true
## Cited drafts and visible refusals

The evidence should show that the assistant supports accountable content work:

- draft segments include source links or claim references
- unsupported requests are refused or routed for human help
- reviewer prompts produce evidence, not unsupported confidence
- sensitive policy questions trigger the expected escalation path
- logs or traces help diagnose grounding failures without overexposing employee data

**Discussion:** Which answer would worry us more: “I don’t know” or a confident answer without a source?

---
<!-- slide:id=lesson-experience-generation-context -->

# Module 5 — Context
## Generate the accessible avatar experience

The experience is more than a rendered avatar. It includes the script, visuals, captions, transcript, disclosure, fallback path, and channel experience.

For customers, the key question is whether employees can understand the message clearly and honestly:

- synthetic-media disclosure is visible and plain
- captions and transcript are available
- keyboard, mobile, and low-bandwidth access are considered
- languages and locale differences are handled intentionally
- a non-avatar alternative exists where needed

Accessibility and disclosure are part of the product, not post-production cleanup.

---
<!-- slide:id=lesson-experience-generation-choices -->

# Module 5 — Choices and trade-offs
## Design for trust, not novelty

Experience choices affect employee trust:

- **Avatar style:** realistic avatars can feel polished, but may raise impersonation concerns.
- **Voice:** branded voice can improve consistency, but requires consent and rights clarity.
- **Disclosure placement:** early and visible disclosure is safer than hidden footnotes.
- **Fallback:** transcript, audio, or human-led alternatives reduce exclusion.
- **Localization:** translation must preserve meaning, policy nuance, and accessibility.
- **Channel:** Teams, learning platform, intranet, or email each changes measurement and support.

The experience should never imply that a real person said something they did not approve.

---
<!-- slide:id=lesson-experience-generation-evidence -->

# Module 5 — What must be true
## Approved revision rendered accessibly

What you should have is an experience package that can be reviewed before release:

- generated only from an approved script revision
- includes disclosure, captions, transcript, and fallback
- preserves source and approval references
- supports the selected audience, locale, and channel
- identifies who can pause or withdraw the published version

**Discussion:** Could an employee understand that the media is synthetic, get the same message without the avatar, and find human help?

---
<!-- slide:id=lesson-approval-gating-context -->

# Module 6 — Context
## Gate publication behind human approval

Human approval is the control that turns generated content into accountable communication.

Before anything is published, named reviewers should confirm:

- factual accuracy and source alignment
- legal, compliance, privacy, and labor considerations
- brand, tone, and employee experience fit
- accessibility and inclusive design expectations
- publication scope, support route, and withdrawal authority

No approval record means no production release.

---
<!-- slide:id=lesson-approval-gating-choices -->

# Module 6 — Choices and trade-offs
## Keep approval strong and workable

Approval should protect the organization without making every typo a governance crisis.

Decisions to make:

- Which roles are mandatory for each content type?
- What changes reset approval: source change, translation, visual edit, voice change, or channel move?
- Who can emergency-pause an experience?
- How are reviewer disagreements resolved?
- What evidence must be retained, and for how long?

The approval gate should be simple enough to use and strong enough to stop unsafe publication.

---
<!-- slide:id=lesson-approval-gating-evidence -->

# Module 6 — What must be true
## Publication and withdrawal record

What you should have is a release record that shows:

- approved script revision and rendered experience
- reviewer roles, decisions, and conditions
- accessibility and disclosure review outcome
- publication channel, audience, and owner
- pause, withdrawal, and replacement process

**Discussion:** If a source policy changes after launch, who knows, who acts, and what happens to the published experience?

---
<!-- slide:id=lesson-prove-and-operate-context -->

# Module 7 — Context
## Evaluate, red-team, trace, and operate

The pilot should generate evidence for a business decision, not just engagement numbers.

Useful operating evidence includes:

- grounding quality and unsupported-claim defects
- disclosure and accessibility checks
- comprehension, task completion, and support handoffs
- feedback themes from employees and reviewers
- red-team findings around deception, bias, unsafe advice, and stale content
- trace review for failures and improvement opportunities

The goal is to decide whether to iterate, scale, pause, or withdraw.

---
<!-- slide:id=lesson-prove-and-operate-choices -->

# Module 7 — Choices and trade-offs
## Measure enough to learn, not enough to surveil

Operating the experience requires careful measurement design:

- cohort-level insight is usually safer than individual-level monitoring
- qualitative feedback explains confusion that metrics can hide
- red-team scenarios should include accessibility, language, disclosure, and policy edge cases
- trace capture helps debugging but must respect privacy and data minimization
- scorecards should define action thresholds before the pilot starts

Evidence should help owners improve the experience without making employees feel observed.

---
<!-- slide:id=lesson-prove-and-operate-evidence -->

# Module 7 — What must be true
## Pilot scorecard and release decision

The final artifact is a decision package:

- pilot scorecard tied to the original onboarding outcome
- known defects and remediation owners
- red-team results and accepted residual risks
- trace review themes and operating improvements
- recommendation to iterate, scale, pause, or withdraw

**Discussion:** What evidence would convince this customer to expand the pattern to another topic, locale, or audience?

---
<!-- slide:id=scenario-next-session -->

# Next working session
## Turn the discussion into a pilot plan

For the next session, bring one real onboarding moment and the people who own it.

We will align on:

- pilot topic, audience, locale, and channel
- approved source owners and review expectations
- selected experience capability and fallback
- disclosure, accessibility, and human-help requirements
- approval gate and withdrawal path
- first scorecard for operating evidence

**Working outcome:** a narrow, governed pilot that can be built, reviewed, and measured without pretending the starter kit is the full production solution.
