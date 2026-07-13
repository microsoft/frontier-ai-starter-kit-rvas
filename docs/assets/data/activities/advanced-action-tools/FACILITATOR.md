# Facilitator Guide · Advanced — Action Tools

> **Command context:** Run commands from the repository root unless a step changes directory.

## Teaching objective

Teams move from an agent that only answers questions to one that can change state. The critical
control is application-owned approval: the model may request a function call, but backend code must
not execute it until a human approves the displayed name and arguments.

The current SDK path is:

1. Create a versioned prompt agent with `PromptAgentDefinition` and explicit `FunctionTool` schemas.
2. Invoke it through `project.get_openai_client().responses.create(...)` with `agent_reference`.
3. Inspect `response.output` for `function_call` items.
4. Ask the human to approve or deny each requested call.
5. Execute approved calls only, encode each result as `FunctionCallOutput`, and continue with
   `previous_response_id=response.id`.

Do not use retired `agents.threads`, `agents.runs`, or run-status approval samples.

## Environment contract

| Variable | Default | Purpose |
|---|---|---|
| `AZURE_AI_PROJECT_ENDPOINT` | none | Foundry project endpoint |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | none | deployed chat model |
| `ACTION_API_URL` | `http://localhost:8080` | provided REST action backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | optional MCP stretch endpoint |
| `ACTION_API_KEY` | empty | optional `x-api-key` |

## Setup

```bash
cd scripts/action-backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

In another terminal:

```bash
az login
python activities/advanced-action-tools/validate.py --step 1
```

The guided path uses the REST backend. The MCP server is an optional comparison exercise, not a
prerequisite for the validator.

## Step guidance

### Step 1 — identify side effects

All three tools require approval. `place_course_hold` is the highest-stakes example because an
incorrect call can block registration. Draw out the distinction between the model deciding that an
action is useful and the application authorizing that action.

### Step 2 — define tools explicitly

Teams complete the three HTTP functions and their `FunctionTool` JSON schemas in
`activities/advanced-action-tools/agent_with_actions.py`. The schema name, required fields, and enum
values must match the backend contract. The current Projects SDK expects explicit schemas; the old
reflection-style `FunctionTool(functions={...})` helper is not the pattern used here.

Checkpoint:

```bash
python activities/advanced-action-tools/validate.py --step 2
```

### Step 3 — implement approval

The approval loop must:

- display `call.name` and parsed `call.arguments`
- collect an explicit approve/deny decision
- avoid calling the backend on denial
- call only a known function from a fixed registry
- return backend output or a denial message as `FunctionCallOutput`
- continue the Responses chain with `previous_response_id`

Checkpoint:

```bash
python activities/advanced-action-tools/validate.py --step 3
python activities/advanced-action-tools/agent_with_actions.py
```

Use `activities/advanced-action-tools/solution.md` as the facilitator reference implementation.

## Common failure modes

- **Backend unreachable:** verify `curl http://localhost:8080/health`.
- **No function call returned:** verify the agent version includes the explicit tool schemas and the
  request uses the versioned `agent_reference`.
- **Action executes before approval:** move dispatch below the human decision branch.
- **Unknown tool name:** reject it; never dynamically evaluate a model-provided name.
- **Second response starts a new conversation:** pass `previous_response_id=response.id`.
- **Version cleanup fails:** delete the exact agent version created by the activity.

## Success standard

The demo is complete only when the requested name and arguments are visible before execution,
approval creates a real backend record, denial creates nothing, and the final agent response
reflects the submitted function output.
