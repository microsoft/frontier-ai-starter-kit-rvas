# QA Report — Full Hackathon Content Review

**Reviewer:** Basher  
**Requested by:** Marco Olivo  
**Review date:** 2026-05-28T16:23:27.374+01:00

## Executive summary

**Outcome:** 14 issue groups found — **11 fixed directly**, **3 require follow-up**.

## Overall assessment

| Area | Status | Notes |
|---|---|---|
| Structural completeness | PASS | All student guides now include Introduction, Step-by-step, Success Criteria, Learning Resources, and Tips. All coach guides now include Overview, Common Issues, Coaching Tips, and Timing. |
| Consistency | PASS | Challenge numbering, coach-guide headings, setup links, and Azure AI Foundry naming are aligned across reviewed files. |
| Technical accuracy | WARN | Package/env mismatches and outdated doc links were fixed. The environment validator now runs cleanly except for the expected local `.env` requirement in a fresh repo. |
| Narrative thread | PASS | The University Q&A Assistant thread now carries cleanly from Challenges 02→06, including docs challenge pages. |
| Cross-references | PASS | Broken relative screenshot links were removed; reviewed internal challenge/doc links are now consistent. |
| Docs ↔ challenges alignment | WARN | Site pages now match the student guides more closely, but a few advanced challenges still rely on students creating artifacts from scratch without starter templates. |
| Jekyll front matter | PASS | All reviewed `docs/*.md` files have valid front matter with required keys. |

## Specific issues found

| File / context | Issue | Action |
|---|---|---|
| `challenges/challenge-00-setup/README.md` — Step 3/4/5/6 portal guidance | Broken relative screenshot links pointed to missing files in `resources/images/`. | **Fixed:** removed broken image embeds and replaced them with text guidance that portal screens may vary. |
| `challenges/challenge-00-setup/README.md`, `challenge-01-first-model/README.md`, `challenge-02-prompt-engineering/README.md` — section structure | Missing explicit `## Step-by-step` section required by the content standard. | **Fixed:** added `## Step-by-step` headings. |
| `challenges/challenge-01-first-model/README.md`, `challenges/challenge-06-deploy/README.md` — Python starter code | Snippets read env vars but did not load `.env`, despite the repo shipping `.env.example`. | **Fixed:** added `load_dotenv()` to the starter snippets. |
| `requirements.txt` | Directly referenced snippet dependencies were incomplete (`azure-core`, `flask`). | **Fixed:** added missing packages. |
| `.env.example` | Challenge 06 endpoint variables were missing. | **Fixed:** added `UNIVERSITY_QA_ENDPOINT` and `UNIVERSITY_QA_KEY`. |
| `resources/scripts/validate-environment.py` | Validator did not check the newly required direct imports / optional endpoint vars. | **Fixed:** added `azure-core`, `flask`, `UNIVERSITY_QA_ENDPOINT`, and `UNIVERSITY_QA_KEY` checks. |
| `README.md` — coach references | Coach Hub links pointed to an outdated external docs path instead of the repo’s actual coach hub page. | **Fixed:** updated both links to `docs/coach-hub.md`. |
| `docs/setup.md` — setup path guidance | Codespaces link was generic, manual setup text was outdated, and the validation note no longer matched the repo state. | **Fixed:** updated the Codespaces URL, clarified `requirements.txt` installation, and replaced the stale validation note. |
| `docs/coach-hub.md` — emergency resources | Azure AI Foundry doc link used the old `ai-studio` path. | **Fixed:** updated to the current Azure AI Foundry docs URL. |
| `challenges/*/solution.md` — coach guide headings | Inconsistent section naming (`Common Pitfalls`, `Common issues`, `Coaching tips`, `Coach Guide`) reduced coach-guide consistency. | **Fixed:** standardized headings and coach-guide titles across all reviewed solution files. |
| `docs/challenges/challenge-01.md` through `challenge-06.md`, `docs/resources.md` | Several learning-resource links and labels used older or inconsistent Azure doc paths/naming. | **Fixed:** aligned them to current Azure AI Foundry / Azure AI Search / Flask / Requests references. |
| `docs/challenges/challenge-03.md` through `challenge-06.md` — overview copy | The site summaries underplayed the University Q&A Assistant progression described in the student guides. | **Fixed:** added explicit narrative-thread references so docs better match the challenge sequence. |
| `challenges/challenge-03-prompt-flow/README.md`, `challenge-04-rag/README.md`, `challenge-05-evaluation/README.md`, `challenge-06-deploy/README.md` | Students are asked to create core artifacts (`flow.dag.yaml`, `rag-flow.dag.yaml`, `test-dataset.jsonl`, `app.py`) from scratch. | **Recommended follow-up:** Rusty/Linus should decide whether to provide starter files or keep this as discovery work. |
| `challenges/challenge-05-evaluation/README.md` — evaluation implementation depth | The evaluation SDK guidance is still a skeleton, which may create uneven coach support across teams. | **Recommended follow-up:** decide whether to add a fuller starter script or keep the challenge intentionally open-ended. |
| `challenges/challenge-00-setup/README.md` — screenshots | Broken links are resolved, but the repo still ships no curated screenshots for setup walkthroughs. | **Recommended follow-up:** decide whether to add maintained screenshots for coach/event branches. |

## Validation performed

- Ran a targeted QA script across all requested student guides, coach guides, docs pages, `.env.example`, `requirements.txt`, and `resources/scripts/validate-environment.py`.
- Verified structural requirements, front matter, environment-variable coverage, and package/import alignment.
- Parsed all reviewed Python code snippets successfully.
- Ran `python -m compileall resources/scripts/validate-environment.py` successfully.
- Created a project virtual environment and installed `requirements.txt` successfully.
- Ran `resources/scripts/validate-environment.py`; it executed successfully and reported the expected fresh-repo failure for missing local `.env` values.

## Summary of fixes applied directly

1. Fixed student-guide structure gaps.
2. Removed broken Challenge 00 screenshot links.
3. Corrected package and environment-variable mismatches.
4. Updated the environment validator to reflect current dependencies.
5. Repaired outdated coach/setup/resource documentation links.
6. Standardized coach-guide headings and naming.
7. Improved docs challenge pages so they match the University Q&A Assistant narrative.

## Items requiring follow-up

1. Decide whether to provide starter artifacts for Challenges 03–06.
2. Decide whether Challenge 05 needs a fuller runnable evaluation starter.
3. Decide whether maintained setup screenshots should exist for coach/event branches.
