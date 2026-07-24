# Avatar-enabled Onboarding Accelerator

This accelerator is a small, vendor-neutral **approved-content pack and integration seam**. It supports a clean workshop demo and a BYO environment without provisioning a landing zone, choosing an avatar platform, or assuming service APIs.

## Contents

- `sample-data/` — complete fictional claims, approvals, script/storyboard, transcript, accessible HTML fallback, and aggregated feedback fixture.
- `main.bicep` — resource-less deployment contract that exposes the integration settings; it deliberately creates no resources.
- `parameters.example.json` — safe placeholder values.
- `mock_renderer.py` — standard-library-only local renderer that enforces the approval and claim gates.

## Clean demo

1. Run `../validate.py`, then run `mock_renderer.py` as described in `../local-demo.md`.
2. Use the fictional claims as the only source of scripted claims.
3. Display the traceable artifact, source links, approval record, disclosure, transcript, and non-avatar alternative.
4. Record feedback only as aggregated example operational evidence; do not treat it as production employee data.

## BYO environment

Provide the selected platform’s endpoints/configuration through the deployment parameters or the customer’s approved configuration mechanism. Keep secrets out of parameters and source control. The consuming adapter should accept an approved content record, return a platform-specific artifact/reference, and preserve the source, script, approval, disclosure, locale, and publication identifiers.

## Integration seam

```text
approved-content pack + approvals
             │
             ▼
customer-owned adapter ──► selected avatar/voice service
             │                         │
             └──────────────► selected employee channel
```

The adapter is responsible for enforcing the approval gate, adding disclosure, supplying captions/transcript and fallback links, and collecting permitted operational evidence. It should be able to pause or withdraw an artifact.

## Search before implement

Before building the adapter, search current official documentation for the chosen platform and channel. Verify supported APIs, authentication, service availability, privacy/residency, accessibility/language behavior, content moderation, auditability, and deletion/withdrawal controls. Implement only against verified signatures; this accelerator intentionally contains no vendor SDK calls or speculative Bicep resource definitions.
