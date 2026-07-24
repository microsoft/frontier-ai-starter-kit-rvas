# Local demo runbook

## What this demonstrates

The local demo verifies the integrity of a synthetic teaching pack and compares structured JSON result records to its expected results. It does not call Azure, Content Understanding, Studio, an SDK, or a network endpoint. The `.md`, `.txt`, and `.html` fixtures are human-readable exercise material, not a claim about service upload formats.

## Prerequisite

Python 3 only. The validator uses the standard library and needs no package installation, environment variable, key, or account.

## Validate the pack

From the repository root:

```bash
python3 scenarios/content-understanding/scripts/validate_local_pack.py
```

The command verifies:

- each fixture is local text/HTML and carries the synthetic-data marker;
- each expected JSON record has the documented shape;
- each expected record's SHA-256 matches its source fixture;
- the golden-case list exactly covers the holdout fixtures;
- the correction record changes a known field without replacing the original expected result.

It writes deterministic, reviewable evidence to:

```text
scenarios/content-understanding/evidence/local-validation.json
```

The evidence contains no timestamp, source content, secret, or network-derived data, so unchanged inputs produce unchanged evidence.

## Compare participant result records

For an exact contract comparison, place one JSON result record per expected-result filename in a local directory:

```text
review-results/
  rfq-1001.json
  invoice-2001.json
  rfq-1002.json
  invoice-2002.json
```

Each file must follow [`accelerator/sample-data/result-contract.json`](accelerator/sample-data/result-contract.json), including the source hash. Then run:

```bash
python3 scenarios/content-understanding/scripts/validate_local_pack.py \
  --actual-dir review-results \
  --evidence-file scenarios/content-understanding/evidence/result-comparison.json
```

The comparison is exact and deterministic. A mismatch is a workshop discussion signal, not a score for a model or a substitute for human review.

## Review the evidence

Open the generated JSON and verify:

- `valid` is `true`;
- `fixture_count` is `4`;
- `golden_case_count` is `2`;
- `errors` is empty;
- when comparison is used, every `actual_comparisons[].status` is `match`.

Use the evidence in Lessons 2 and 4 and retain it with the session's decision record. Do not add customer documents or credentials to this scenario folder.
