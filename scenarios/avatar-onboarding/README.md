# Avatar Scenario — technical build course

Build a governed, accessible, avatar-led experience on Azure and Microsoft Foundry. The sample
challenge uses employee onboarding, but the pattern applies to approved learning, communications,
and support experiences where every published statement traces to approved content, named human
approvals, a synthetic-media disclosure, and operational evidence, and where any published revision
can be withdrawn the moment its source changes.

This is a **build** course, not a survey. Each module makes one high-stakes decision, compares the
viable Microsoft options, fully implements the default path, and names the seam for swapping in a
different approved platform. The reference implementation is in [`solution.md`](accelerator/solution.md);
the deployable foundation is in [`accelerator/README.md`](accelerator/README.md).

> **Fictional data only.** The accelerator ships synthetic HR content. Never place real customer
> content, or a real person's voice or likeness, in this repository. **Keyless-first:**
> `DefaultAzureCredential` + managed identity + RBAC — never keys in code or Bicep.

## The 7 modules

| Module | You build | Default path | Canonical activity |
| --- | --- | --- | --- |
| [1 — Select the experience capability](lessons/01-experience-selection.md) | A dated, evidence-backed capability decision (batch avatar vs real-time vs Voice Live vs video translation vs audio) | Speech **batch avatar**, standard voice | Current Microsoft docs |
| [2 — Provision the foundation](lessons/02-foundation.md) | Keyless Foundry + model + Search + Speech data plane + observability | `azd`/Bicep, managed identity | [Foundations](../../activities/foundations/README.md) |
| [3 — Governed content pipeline](lessons/03-content-pipeline.md) | Versioned claims with owner/version/expiry that gate everything downstream | Blob + typed claim set | This scenario's accelerator |
| [4 — Grounded assistant](lessons/04-grounded-assistant.md) | A citing assistant that refuses on unapproved claims and hands off | Foundry agent grounded on approved content | [Foundations, Steps 3–4](../../activities/foundations/README.md) |
| [5 — Generate the accessible experience](lessons/05-experience-generation.md) | Avatar render from an approved revision with disclosure, captions, transcript, fallback | Batch synthesis + accessibility outputs | [Voice & Live](../../activities/extra-voice-live/README.md) |
| [6 — Gate publication behind human approval](lessons/06-approval-gating.md) | A versioned four-role approval gate and a withdrawal path | Signed record enforced in code | This scenario's accelerator |
| [7 — Evaluate, red-team, trace, operate](lessons/07-prove-and-operate.md) | Evaluation + red-team + tracing + release scorecard | Foundry evaluations + AI Red Teaming Agent | [Evaluation](../../activities/advanced-evaluation-redteam/README.md) |

Work the modules in order — Module 1 is the highest-stakes decision and every later module depends
on it.

## Decision gates to carry into the customer conversation

Use these gates before opening reference-library mechanics:

| Gate | Decide before building |
|---|---|
| Experience boundary | Why does avatar, voice, audio, or video improve the outcome compared with a typed experience? |
| Content boundary | Which claims are approved, versioned, owned, expirable, and traceable to source evidence? |
| Consent boundary | Which likeness, voice, disclosure, accessibility, and fallback rules apply before generation? |
| Approval boundary | Which roles approve factual accuracy, compliance, brand, and source ownership for each revision? |
| Operating boundary | What evaluation, red-team, trace, feedback, and withdrawal evidence is required before release? |

## Working contract

- **Approved content is the publishing boundary.** A grounded assistant may cite permitted sources
  for interactive help, but it may not silently add claims to a published script.
- **Human approval is a release gate.** Factual/SME, legal/compliance, brand, and content-owner
  decisions are required before anything publishes, and they bind to an exact script revision.
- **Accessibility is a first-class output.** Every experience ships a transcript, captions (where the
  capability supports them), an equivalent non-avatar fallback, a human-help path, and a clear
  AI/avatar disclosure.
- **Consent and privacy are non-negotiable.** Never clone a real voice or likeness without explicit
  recorded authorization; custom avatar/voice is an Azure limited-access feature. Minimize pilot
  telemetry to aggregate, identifier-free signals.
- **Withdrawal is part of the build.** A source change, consent withdrawal, safety issue, or defect
  must identify and pause the affected published revision.

## Quick start

```bash
# 1. Deploy the keyless foundation (writes accelerator/.env):
scenarios/avatar-onboarding/accelerator/scripts/deploy.sh rg-avatar-onboarding westus2

# 2. Run the scenario's offline contract + all module checkpoints:
python3 scenarios/avatar-onboarding/validate.py
```

The offline checkpoints validate the fictional pack and its approval gates deterministically; they
are not media generators and make no service calls. The full reference implementation, end-to-end,
is in [`solution.md`](accelerator/solution.md).

## Responsible AI

Standard avatar + standard neural voice needs **no** registration, but synthetic-media **disclosure**
to users and a feedback channel are still required. **Custom** avatar / **custom** or **personal**
voice is **Limited Access** (registration only, Microsoft-managed customers), and custom video avatar
requires actor consent and advance disclosure to the talent. Module 1 records the exact gates for
your chosen capability; Module 7 proves them before any release.
