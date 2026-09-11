# Avatar Scenario accelerator

Build an accessible avatar-led experience from approved content. The accelerator includes a
vendor-neutral approved-content pack and integration seam, plus an optional Bicep foundation for a
clean Azure demo subscription. The reference path uses Azure Speech batch avatar synthesis. It
supports a pilot. It does not select a production channel or implement a production channel adapter.

## What this accelerator proves

- Published claims trace to an approved source and an exact script revision.
- Named reviewers approve a revision before it publishes.
- The experience includes disclosure, captions or transcript, and a non-avatar fallback.
- A source or consent change can pause or withdraw a published revision.
- Pilot telemetry stays aggregate and free of personal identifiers.

## Before you start

**Check the current API surface before writing SDK code.** The selected avatar service and channel
determine the API, identity model, availability, privacy controls, accessibility behavior, and
withdrawal controls. Search current official documentation and the relevant Foundry guidance. Do
not infer a signature from this accelerator or from memory.

**Use fictional data only.** `sample-data/` contains synthetic HR content. Do not add customer
content, a real person's voice, or a real person's likeness to this repository.

**Use keyless access.** The reference path uses `DefaultAzureCredential`, managed identity, and
RBAC. Keep secrets out of parameters and source control.

## Choose an environment

### Clean-subscription demo

Use a disposable subscription after the customer agrees the pilot boundary. Deploy the optional
foundation, then use the approved-content pack and the fictional claims for the workshop.

### Existing customer environment

Record the chosen platform, channel, source boundary, and access model. Do not redeploy this
package into customer resources. Build the customer-owned adapter against the approved platform and
configuration instead.

## The build path

| Module | What you build | Evidence |
|---|---|---|
| 1. Experience selection | Capability choice, consent rules, accessibility needs, and release gates | Approved capability decision |
| 2. Foundation | Keyless Foundry, Speech, Search, storage, and observability | Generated `.env` contract and live resources |
| 3. Content pipeline | Versioned claims with owners, source links, and expiry | Approved claim set |
| 4. Grounded assistant | Citing help that refuses unsupported claims | Cited response or clear handoff |
| 5. Experience generation | Render from an approved script revision | Disclosure, transcript, and fallback artifact |
| 6. Approval gate | Exact-revision approvals and withdrawal path | Publish or withdrawal record |
| 7. Prove and operate | Evaluation, red-team cases, trace review, and release scorecard | Pilot release decision |

Complete the modules in order. The experience capability chosen in module 1 shapes the rest of the
path.

## Decisions to make with the customer

| Gate | Decide before building |
|---|---|
| Experience boundary | Why is an avatar, voice, audio, or video better than a typed experience here? |
| Content boundary | Which claims are approved, owned, versioned, and traceable to source evidence? |
| Consent boundary | Which likeness, voice, disclosure, accessibility, and fallback rules apply? |
| Approval boundary | Which roles approve factual accuracy, compliance, brand, and source ownership? |
| Operating boundary | Which evaluation, feedback, and withdrawal evidence is required before release? |

## Get started

Run these commands from the repository root:

```bash
az login
./scenarios/avatar-onboarding/accelerator/scripts/deploy.sh rg-avatar-onboarding westus2
```

The deployment writes `accelerator/.env`. Later modules use that local file. Do not commit it.
Each lesson's **Verify** section gives the command and signal for that module.

## Scope and boundaries

- The customer-owned adapter takes approved content and returns a platform-specific artifact while
  preserving source, script, approval, disclosure, locale, and publication identifiers.
- Never clone a real voice or likeness without recorded authorization.
- Treat human approval as a release gate for the exact script revision.
- Keep a withdrawal path one action away when a source changes, consent is withdrawn, or a defect
  appears.

## Related implementation activities

- [Foundations](../../../activities/foundations/README.md) for the Foundry and grounding baseline.
- [Voice & Live](../../../activities/extra-voice-live/README.md) for speech and voice patterns.
- [Evaluation & Red Teaming](../../../activities/advanced-evaluation-redteam/README.md) and
  [Tracing & Observability](../../../activities/advanced-tracing-observability/README.md) for
  release evidence and traces.

See [solution.md](solution.md) for the complete facilitator reference.
