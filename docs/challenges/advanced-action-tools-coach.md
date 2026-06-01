---
title: "Advanced: Action Tools · Coach"
parent: Challenges
nav_order: 110
nav_exclude: true
---

# Coach Guide · Advanced — Action Tools

> **Coach-only.** The full reference implementation of the approval loop is below. Do **not** paste it
> into the student channel — the starter `agent_with_actions.py` deliberately leaves the McpTool and
> approval loop as `< PLACEHOLDER >` gaps (the ATA "single-line completion moment" pattern).

## What this challenge is really teaching

The leap from a **knowledge** agent (reads/answers) to an **action** agent (changes state) — and the
governance that leap demands. Both reference repos stop at knowledge tools or auto-firing actions;
this challenge adds the **human-in-the-loop approval** that real deployments require. The pedagogical
core is the `RequiredMcpToolCall → ToolApproval → SubmitToolApprovalAction` loop.

We **ship the backend** so teams stay on the MCP/approval objective instead of building a CRUD API.
It lives in `scripts/action-backend/` (FastAPI `app.py` + FastMCP `mcp_server.py`) and exposes three
tools: `create_it_ticket`, `place_course_hold`, `book_advising_slot`, under `server_label`
**`northfield_actions`**.

## Env contract (authoritative — keep in lockstep)

| Variable | Default | Notes |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | provided FastAPI backend base URL |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | **the MCP endpoint students attach** |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key`; leave empty for the workshop |

These names are defined in `.env.sample`, `scripts/deploy.sh`, and the backend. If anyone renames one,
it must change in all four places + this challenge.

## Setup the team needs

```bash
# provided backend (two terminals)
cd scripts/action-backend && pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080      # terminal 1
python mcp_server.py                            # terminal 2
# agent side
az login                                        # keyless DefaultAzureCredential
# .env: AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME, ACTION_MCP_URL
```

## Per-step facilitation

### Step 0 / Step 1 checkpoint — backend reachable
- `validate.py --step 1` hits `GET /health` over REST. If it fails, the backend isn't running or
  `ACTION_API_URL` is wrong. This is the #1 blocker — check it first for any stuck team.

### Step 1 — knowledge vs action
- Answer key: side effects — `create_it_ticket` pages IT; `place_course_hold` **blocks a student's
  registration** (highest-stakes — a wrongful hold is real harm); `book_advising_slot` consumes an
  advisor's calendar. All three warrant approval. The registration hold is the one to dwell on.

### Step 2 — attach the McpTool
Reference completion of `build_action_tool()`:
```python
from azure.ai.agents.models import McpTool, RequiredMcpToolCall, SubmitToolApprovalAction, ToolApproval

def build_action_tool():
    return McpTool(
        server_label="northfield_actions",
        server_url=os.environ["ACTION_MCP_URL"],
        # require_approval defaults to "always" — leave it on for action tools
    )
```
- **Pitfall:** `server_label` must be `northfield_actions` or `validate.py --step 2` fails and the model
  may not find the tools. **Pitfall:** Agent Service only accepts **remote** MCP endpoints — `localhost`
  works from the SDK in-loop here, but for a hosted/public demo they must tunnel it (Container Apps /
  dev tunnel) and reset `ACTION_MCP_URL`.

### Step 3 — the approval loop (the heart of it)
Reference completion of `run_with_approval()`:
```python
def run_with_approval(agent_id, thread_id):
    run = agents.runs.create(thread_id=thread_id, agent_id=agent_id)
    while run.status in ("queued", "in_progress", "requires_action"):
        if run.status == "requires_action" and isinstance(
            run.required_action, SubmitToolApprovalAction
        ):
            tool_calls = run.required_action.submit_tool_approval.tool_calls
            approvals = []
            for call in tool_calls:
                if isinstance(call, RequiredMcpToolCall):
                    print(f"\nAgent wants to call: {call.name}\n  args: {call.arguments}")
                    decision = input("Approve this action? [y/N] ").strip().lower() == "y"
                    approvals.append(ToolApproval(tool_call_id=call.id, approve=decision))
            agents.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=run.id, tool_approvals=approvals
            )
        run = agents.runs.get(thread_id=thread_id, run_id=run.id)
    return run
```
- **Teaching points:** (1) the run **pauses** at `requires_action` — nothing executes until approval is
  submitted; (2) showing `call.name` + `call.arguments` to the human is the governance moment — don't
  let teams skip the print; (3) `approve=False` cleanly ends the run with no side effect.
- **Pitfall:** SDK shape drift. Depending on `azure-ai-agents` version the approvals kwarg may be
  `tool_approvals=` (shown) or folded into `submit_tool_outputs`. If their installed version differs,
  send them to `references/sdk/foundry-sdk-py.md` and the MCP tool how-to. `validate.py --step 3` only
  checks the symbols are present and placeholders are gone — it does not pin the exact call shape.
- **Pitfall:** forgetting to re-`get` the run inside the loop → infinite `requires_action`.

### Step 4 — end-to-end
- `validate.py --step 4` does its **own** REST round-trip (create IT ticket → list → confirm) against
  the backend, independent of the agent, so you can verify the backend is wired even if a team's agent
  code is mid-flight.
- The real proof for the team is: NL prompt → approve → agent reports a `ticket_id` → `curl
  /it-tickets` shows it. Then the **denial** path: deny → nothing created. Make every team run the
  denial — it's where the governance lesson lands.

## Common issues & fast unblocks
- **`Step 1 FAIL — backend not reachable`** → backend not started / wrong `ACTION_API_URL`.
- **Model never calls the tool** → wrong `server_label`/`server_url`, or MCP server down.
- **Agent stalls after approval** → missing the re-`get`/poll, or (Responses API) missing
  `previous_response_id`.
- **`Unauthorized` to backend** → `ACTION_API_KEY` set on one process but not the other; either set it
  in both terminals or unset it everywhere for the workshop.
- **Team wants to auto-approve everything** → push back; the whole challenge is the approval gate.

## Timing (75 min)
- 0–10: Step 0 start backend + Step 1 conceptual
- 10–25: Step 2 attach McpTool
- 25–55: Step 3 approval loop (spend the time here)
- 55–75: Step 4 end-to-end approve + deny, debrief

## Debrief questions
- "Which of the three actions is most dangerous to auto-run, and why?"
- "Walk me through what the run looks like at the moment it pauses."
- "Show me the denial path — what did the agent do, what did the backend store?"
- "How does an action tool change your threat model vs. a knowledge tool?" (bridge to Red Teaming)

## Checkpoint answer key
With the backend running and `agent_with_actions.py` completed:
```text
python validate.py --all
# ✅ Step 1 PASS — Action Tools backend reachable at http://localhost:8080
# ✅ Step 2 PASS — MCP action tool attached (northfield_actions @ ACTION_MCP_URL)
# ✅ Step 3 PASS — human tool-approval loop implemented
# ✅ Step 4 PASS — action round-tripped through the backend (ticket ...)
# ✅ ALL CHECKPOINTS PASS
```
Steps 1 & 4 require the provided backend running; Steps 2 & 3 are static checks on the wiring file.
Before completion, Steps 2/3 correctly FAIL on the unfilled `< PLACEHOLDER >` markers.
