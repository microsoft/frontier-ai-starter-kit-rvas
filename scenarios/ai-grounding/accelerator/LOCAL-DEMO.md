# Local corpus-preparation and retrieval simulation

This demo is deliberately local and deterministic. It prepares the fictional Northstar corpus, ranks document terms for each golden question, applies the fictional access-group boundary, and writes a reviewable JSON evidence artifact. It does **not** call Azure, an SDK, a model, a network endpoint, an identity provider, or a secret store.

## Run

From the repository root:

```bash
python3 scenarios/ai-grounding/accelerator/scripts/prepare_local_corpus.py
python3 scenarios/ai-grounding/accelerator/validate.py
```

The first command updates `accelerator/evidence/local-retrieval-evidence.json`. Review:

- `prepared_sources`: source IDs, owners, allowed groups, and content hashes;
- each `case`: role, question, expected and retrieved citations, withheld sources, refusal boundary, and checks;
- `summary`: the case count and any failures.

Run the first command twice and compare its output with `git diff -- scenarios/ai-grounding/accelerator/evidence/`; an unchanged corpus produces byte-identical evidence.

## What the simulation proves

It demonstrates a workshop review loop: source metadata is explicit, role groups limit eligible documents, expected citations are checked, and restricted, inaccessible, and unsupported requests refuse without citations. The lexical ranker is only a transparent training fixture; it is not a quality, authorization, or product implementation.

## Before a real pilot

Replace every fictional source and role group with approved customer governance decisions. Verify current product, source, permission, and evaluation capabilities in Microsoft documentation before implementing any Foundry IQ or other service integration.
