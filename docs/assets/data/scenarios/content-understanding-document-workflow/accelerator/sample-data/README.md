# Synthetic local data pack

This pack contains invented names, identifiers, amounts, and dates. It has no customer, production,
credential, or service data.

The `.md`, `.txt`, and `.html` files are **local teaching fixtures** for inspecting document facts in
a workshop. They are not Content Understanding upload formats or API payloads. Confirm supported
formats and integration behavior before you use a service.

## Pack contents

- `fixtures/tuning/` — two examples for schema and expected-output discussion.
- `fixtures/golden/` — two holdout cases: a missing delivery date and conflicting invoice total.
- `expected/` — structured JSON expected outcomes, including a SHA-256 binding to each source fixture.
- `golden-cases.json` — holdout membership and intent.
- `corrections/` — a separate reviewer correction record for `invoice-2002`; it deliberately preserves the original expected outcome.
- `manifest.json` and `result-contract.json` — the scenario validator's input contract.

**Expected values are not normalized service results.** The local records omit field confidence
and grounding spans. Use them to check facts and routing; they cannot prove module 4's evidence
contract. The fixtures also contain routing hints, so add separate attack cases without those hints
before measuring injection resistance.

Run the workflow over this pack and compare every extracted field with its source document. That
comparison is the evidence.
