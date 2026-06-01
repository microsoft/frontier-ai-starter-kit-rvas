# QA Validation Matrix

Date: 2026-06-01
Requested by: Marco Olivo
Executor: Basher (QA & Coach Enablement)
Team root: /home/marco/ai-hackathon

## Execution setup
- Preferred env rule applied: no repo venv detected (`.venv`/`venv` absent), so a temporary venv was created at `/tmp/aihack-qa-venv`.
- Dependencies installed only after first pass showed missing modules (`httpx`, `azure-*`): `pip install -r requirements.txt`.
- Final matrix below is based on the second pass executed from `/tmp/aihack-qa-venv/bin/python`.

## Status matrix

| Target | Command | Exit | Status | Evidence (key output) |
|---|---|---:|---|---|
| scripts/validate-foundations.py | `/tmp/aihack-qa-venv/bin/python scripts/validate-foundations.py` | 1 | BLOCKED | Missing required `.env` vars: `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX_NAME`, `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`. Log: `/tmp/qa-validate-20260601-venv/scripts_validate_foundations.log` |
| challenges/foundations/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/foundations/validate.py --all` | 1 | BLOCKED | `.env` placeholders/missing values; project endpoint unreachable (`AZURE_AI_PROJECT_ENDPOINT`); requires `azd up` + `az login` + env export. Log: `/tmp/qa-validate-20260601-venv/foundations_validate_all.log` |
| challenges/advanced-action-tools/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/advanced-action-tools/validate.py --all` | 1 | BLOCKED | Step 1 cannot reach backend at `http://localhost:8080` (`Connection refused`); backend prerequisite not running. Log: `/tmp/qa-validate-20260601-venv/advanced_action_tools_validate_all.log` |
| challenges/advanced-evaluation-redteam/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/advanced-evaluation-redteam/validate.py --all` | 0 | PASS | All 4 steps passed: eval dataset shape, `evaluate.py` run, custom evaluator discrimination, adversarial seed coverage. Log: `/tmp/qa-validate-20260601-venv/advanced_evaluation_redteam_validate_all.log` |
| challenges/advanced-tracing-observability/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/advanced-tracing-observability/validate.py --all` | 1 | BLOCKED | Required learner artifacts absent: `trace_setup.py`, `traced_run.py`, `correlate.kql`. Log: `/tmp/qa-validate-20260601-venv/advanced_tracing_observability_validate_all.log` |
| challenges/advanced-deploy-hosted-agent/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/advanced-deploy-hosted-agent/validate.py --all` | 1 | BLOCKED | Missing `hosted/agent.yaml`; `.env` missing `AZURE_AI_PROJECT_ENDPOINT`; hosted deployment prerequisites not satisfied. Log: `/tmp/qa-validate-20260601-venv/advanced_deploy_hosted_agent_validate_all.log` |
| challenges/capstone-multi-agent/validate.py | `/tmp/aihack-qa-venv/bin/python challenges/capstone-multi-agent/validate.py --all` | 1 | BLOCKED | No learner `*.py` files found under default `--path` (`challenges/capstone-multi-agent`); structural checks cannot execute without capstone implementation files. Log: `/tmp/qa-validate-20260601-venv/capstone_multi_agent_validate_all.log` |

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
