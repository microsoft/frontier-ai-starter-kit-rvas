# Avatar Scenario Accelerator

This accelerator has two parts: a small, vendor-neutral **approved-content pack and integration
seam** for local workshops, plus optional Bicep for a clean Azure demo subscription. It does not
choose an avatar platform, provision a landing zone, or implement a production channel adapter.

## Contents

- `sample-data/` — complete fictional claims, approvals, script/storyboard, transcript, accessible HTML fallback, and aggregated feedback fixture.
- `main.bicep` — optional deployable foundation for Foundry, Search, Storage, Speech data-plane access, and observability. It is not a landing zone or production channel implementation.
- `parameters.example.json` — safe placeholder values.
- `content_pack.py` — standard-library-only pack contract that enforces the approval and claim gates.

## Clean demo

1. Use `content_pack.py` to load the approved-content pack. It enforces the approval and claim gates.
2. Use the fictional claims as the only source of scripted claims.
3. Display the traceable artifact, source links, approval record, disclosure, transcript, and non-avatar alternative.
4. Record feedback only as aggregated example operational evidence; do not treat it as production employee data.

## BYO environment

Provide the selected platform’s endpoints/configuration through deployment parameters or the
customer’s approved configuration mechanism. Keep secrets out of parameters and source control. The
adapter should accept an approved content record, return a platform-specific artifact/reference, and
preserve the source, script, approval, disclosure, locale, and publication identifiers.

## Integration seam

```text
approved-content pack + approvals
             │
             ▼
customer-owned adapter ──► selected avatar/voice service
             │                         │
             └──────────────► selected employee channel
```

The adapter enforces the approval gate, adds disclosure, supplies captions/transcript and fallback
links, and collects permitted operational evidence. It must be able to pause or withdraw an artifact.

## Search before implement

Before you build the adapter, search current official documentation for the chosen platform and
channel. Verify supported APIs, authentication, availability, privacy/residency,
accessibility/language behavior, content moderation, auditability, and deletion/withdrawal
controls. Implement only against verified signatures. This accelerator intentionally contains no
vendor SDK calls or speculative Bicep resource definitions.
