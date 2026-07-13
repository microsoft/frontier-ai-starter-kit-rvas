# Advanced — Action Tools

The maintained participant activity is `activities/advanced-action-tools/README.md`; the published
site is generated from that source by `docs/build.js`.

The activity uses the current `azure-ai-projects` 2.x flow: versioned prompt agents, explicit
`FunctionTool` schemas, Responses `function_call` items, human approval before dispatch, and
`FunctionCallOutput` results chained with `previous_response_id`.

Run the provided backend and checkpoints from the repository root:

```bash
cd scripts/action-backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

```bash
python activities/advanced-action-tools/validate.py --step 1
python activities/advanced-action-tools/validate.py --step 2
python activities/advanced-action-tools/validate.py --step 3
```

Do not use older threads/runs or run-status approval examples with this repository's Projects 2.x
dependency line.
