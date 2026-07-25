# Synthetic local data pack

This pack contains invented names, identifiers, amounts, and dates. It contains no customer, production, credential, or service data.

The `.md`, `.txt`, and `.html` files are **local teaching fixtures** that make the document facts inspectable in a workshop. They do not claim to be upload formats or API payloads for Content Understanding. Confirm currently supported formats and integration behavior before using any service.

## Pack contents

- `fixtures/tuning/` — two examples for schema and expected-output discussion.
- `fixtures/golden/` — two holdout cases: a missing delivery date and conflicting invoice total.
- `expected/` — structured JSON expected outcomes, including a SHA-256 binding to each source fixture.
- `golden-cases.json` — holdout membership and intent.
- `corrections/` — a separate reviewer correction record for `invoice-2002`; it deliberately preserves the original expected outcome.
- `manifest.json` and `result-contract.json` — the scenario validator's input contract.

Run `python3 validate.py` from the scenario folder to check this pack. The validator uses Python's standard library only and makes no network or Azure calls.
