# Historical QA Validation Snapshot

This page records one local QA pass from 2026-06-01. It is **not** a live status page and should not
be used as current release evidence. For current validation, run the relevant `validate.py` command
from a freshly provisioned environment.

## Execution setup
- The pass used a temporary local virtual environment.
- Dependencies were installed after the first pass showed missing modules (`httpx`, `azure-*`):
  `pip install -r requirements.txt`.
- Results below reflect that single local run only.

## Status matrix

| Target | Command | Exit | Status | Evidence (key output) |
|---|---|---:|---|---|
| scripts/validate-foundations.py | `python scripts/validate-foundations.py` | 1 | BLOCKED | Missing required `.env` vars: `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX_NAME`, `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`. |
| challenges/foundations/validate.py | `python challenges/foundations/validate.py --all` | 1 | BLOCKED | `.env` placeholders/missing values; project endpoint unreachable (`AZURE_AI_PROJECT_ENDPOINT`); requires `azd up` + `az login` + env export. |
| challenges/advanced-action-tools/validate.py | `python challenges/advanced-action-tools/validate.py --all` | 1 | BLOCKED | Step 1 cannot reach backend at `http://localhost:8080` (`Connection refused`); backend prerequisite not running. |
| challenges/advanced-evaluation-redteam/validate.py | `python challenges/advanced-evaluation-redteam/validate.py --all` | 0 | PASS | All 4 steps passed: eval dataset shape, `evaluate.py` run, custom evaluator discrimination, adversarial seed coverage. |
| challenges/advanced-tracing-observability/validate.py | `python challenges/advanced-tracing-observability/validate.py --all` | 1 | BLOCKED | Required learner artifacts absent: `trace_setup.py`, `traced_run.py`, `correlate.kql`. |
| challenges/advanced-deploy-hosted-agent/validate.py | `python challenges/advanced-deploy-hosted-agent/validate.py --all` | 1 | BLOCKED | Missing `hosted/agent.yaml`; `.env` missing `AZURE_AI_PROJECT_ENDPOINT`; hosted deployment prerequisites not satisfied. |
| challenges/capstone-multi-agent/validate.py | `python challenges/capstone-multi-agent/validate.py --all` | 1 | BLOCKED | No learner `*.py` files found under default `--path` (`challenges/capstone-multi-agent`); structural checks cannot execute without capstone implementation files. |

## Summary counts
- PASS: 1
- FAIL: 0
- BLOCKED: 6
- NOT-APPLICABLE: 0

## Prioritized remediation plan (fail/blocked only)
1. Provision and export Foundations environment: run `azd up`, authenticate with `az login`, then `azd env get-values > .env` so foundation/deploy validators can reach project and search resources.
2. Start Action Tools backend before validation: run backend from `scripts/action-backend` so `http://localhost:8080` is reachable.
3. Create expected learner artifacts for tracing challenge: add `trace_setup.py`, `traced_run.py`, and `correlate.kql` per challenge steps.
4. Create hosted-agent artifacts for deploy challenge: add `hosted/agent.yaml` (and related hosted project files) before re-running `--all`.
5. Run capstone validator with implemented capstone source path: either place capstone Python files in default path or pass `--path <learner-capstone-dir>`.

## Notes
- No challenge code was modified.
- Classification rule used: missing cloud/local prerequisites are marked BLOCKED, not FAIL.
