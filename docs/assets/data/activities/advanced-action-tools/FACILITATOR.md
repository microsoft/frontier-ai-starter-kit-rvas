
# Facilitator Guide · Advanced — Action Tools

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> **Facilitator-only.** The full reference implementation of the approval loop is below. Do not paste it
> into the student channel — the starter `agent_with_actions.py` deliberately leaves the FunctionTool
> and approval loop as `< PLACEHOLDER >` gaps (the ATA "single-line completion moment" pattern).

## What this activity is really teaching

The leap from a knowledge agent (reads/answers) to an action agent (changes state) — and the
governance that leap demands. Both reference repos stop at knowledge tools or auto-firing actions;
this activity adds the human-in-the-loop approval that real deployments require. The pedagogical
core is the `requires_action → ToolOutput` loop: the run pauses, the human decides, only then does
anything execute.

> **SDK note for facilitators:** MCP-native approval classes (`McpTool`, `RequiredMcpToolCall`,
> `SubmitToolApprovalAction`, `ToolApproval`) are not in the current public `azure-ai-agents`
> 1.x release. The activity uses `FunctionTool` + `RequiredFunctionToolCall` +
> `SubmitToolOutputsAction` + `ToolOutput` — same governance objective, fully supported in 1.x.

We ship the backend so teams stay on the approval-loop objective instead of building a CRUD API.
It lives in `scripts/action-backend/` (FastAPI `app.py` + FastMCP `mcp_server.py`) and exposes three
REST endpoints that the FunctionTool callables hit.

## Env contract (authoritative — keep in lockstep)

| Variable | Default | Notes |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | provided FastAPI backend base URL |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | MCP endpoint shipped by backend — optional, preview/stretch only; not required for the guided path |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key`; leave empty for the workshop |

These names are defined in `.env.sample`, `scripts/deploy.sh`, and the backend. If anyone renames one,
it must change in all four places + this activity.

## Setup the team needs

```bash
# provided backend (REST — required)
cd scripts/action-backend && pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080      # terminal 1
# optional: python mcp_server.py               # only for stretch goal 1 (MCP server exploration)
# agent side
az login                                        # keyless DefaultAzureCredential
# .env: AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME, ACTION_API_URL

```

## Per-step facilitation

### Step 0 / Step 1 checkpoint — backend reachable
- `python activities/advanced-action-tools/validate.py --step 1` hits `GET /health` over REST. If it fails, the backend isn't running or
  `ACTION_API_URL` is wrong. This is the #1 blocker — check it first for any stuck team.

### Step 1 — knowledge vs action
- Answer key: side effects — `create_it_ticket` pages IT; `place_course_hold` blocks a student's
  registration (highest-stakes — a wrongful hold is real harm); `book_advising_slot` consumes an
  advisor's calendar. All three warrant approval. The registration hold is the one to dwell on.

### Step 2 — define the action FunctionTool

Reference completion:

```python
from azure.ai.agents.models import (
    FunctionTool, RequiredFunctionToolCall, SubmitToolOutputsAction, ToolOutput
)
import httpx, json

def create_it_ticket(student_id, summary, category="other", priority="normal"):
    """Open an IT support ticket for a student.

    :param student_id: University student identifier (e.g. s1029384).
    :param summary: One-line description of the issue.
    :param category: Issue category — wifi, account, hardware, software, or other.
    :param priority: Ticket priority — low, normal, high, or urgent.
    """
    r = httpx.post(f"{API_URL}/it-tickets",
                   json={"student_id": student_id, "summary": summary,
                         "category": category, "priority": priority},
                   headers=_headers(), timeout=10.0)
    r.raise_for_status()
    return r.text

# (place_course_hold and book_advising_slot follow same pattern — see solution.md)

def build_action_tools():
    return FunctionTool(functions={create_it_ticket, place_course_hold, book_advising_slot})

```

- **Pitfall:** `FunctionTool` builds schemas from docstring `:param name: description` lines. Missing
  docstrings → model won't understand arguments → it will hallucinate or refuse to call the tool.
- `python activities/advanced-action-tools/validate.py --step 2` checks for `FunctionTool`, the three function names, and `ACTION_API_URL`.

### Step 3 — the approval loop (the heart of it)

Reference completion of `run_with_approval()`:

```python
def run_with_approval(agent_id, thread_id):
    run = agents.runs.create(thread_id=thread_id, agent_id=agent_id)
    while run.status in ("queued", "in_progress", "requires_action"):
        if run.status == "requires_action" and isinstance(
            run.required_action, SubmitToolOutputsAction
        ):
            tool_outputs = []
            for call in run.required_action.submit_tool_outputs.tool_calls:
                if isinstance(call, RequiredFunctionToolCall):
                    args = json.loads(call.function.arguments)
                    print(f"\n🔧 Action requested: {call.function.name}")
                    print(f"   {call.function.arguments}")
                    decision = input("Approve this action? [y/N] ").strip().lower() == "y"
                    if decision:
                        fn_map = {
                            "create_it_ticket": create_it_ticket,
                            "place_course_hold": place_course_hold,
                            "book_advising_slot": book_advising_slot,
                        }
                        result = fn_map[call.function.name](**args)
                    else:
                        result = json.dumps({"denied": "Human operator declined."})
                    tool_outputs.append(ToolOutput(tool_call_id=call.id, output=result))
            agents.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
            )
        run = agents.runs.get(thread_id=thread_id, run_id=run.id)
    return run

```

- Teaching points: (1) the run pauses at `requires_action` — nothing executes until
  `submit_tool_outputs` is called; (2) showing `call.function.name` + `call.function.arguments` to
  the human is the governance moment — don't let teams skip the print; (3) returning the denial JSON
  tells the agent "you were blocked" so it reports back gracefully.
- **Pitfall:** `call.function.arguments` is a JSON string — `json.loads` before unpacking as `**args`.
- **Pitfall:** forgetting to re-`get` the run inside the loop → infinite `requires_action`.

### Step 4 — end-to-end
- `python activities/advanced-action-tools/validate.py --step 4` does its own REST round-trip (create IT ticket → list → confirm) against
  the backend, independent of the agent, so you can verify the backend is wired even if a team's agent
  code is mid-flight.

- The real proof for the team is: NL prompt → approve → agent reports a `ticket_id` → `curl
  /it-tickets` shows it. Then the denial path: deny → nothing created. Make every team run the
  denial — it's where the governance lesson lands.

## Common issues & fast unblocks
- `Step 1 FAIL — backend not reachable` → backend not started / wrong `ACTION_API_URL`.
- Model never calls the tool → function docstrings missing `:param` lines, or `FunctionTool` not in `tools=`.
- Agent stalls after approval → missing the re-`get`/poll inside the while loop.

- `Unauthorized` to backend → `ACTION_API_KEY` set on one process but not the other; either set it
  in both terminals or unset it everywhere for the workshop.

- Team wants to auto-approve everything → push back; the whole activity is the approval gate.

## Timing (75 min)
- 0–10: Step 0 start backend + Step 1 conceptual
- 10–30: Step 2 define FunctionTool (fill function stubs + build_action_tools)
- 30–60: Step 3 approval loop (spend the time here)
- 60–75: Step 4 end-to-end approve + deny, debrief

## Debrief questions
- "Which of the three actions is most dangerous to auto-run, and why?"
- "Walk me through what the run looks like at the moment it pauses."
- "Show me the denial path — what did the agent do, what did the backend store?"
- "How does an action tool change your threat model vs. a knowledge tool?" (bridge to Red Teaming)

## Checkpoint answer key

With the backend running and `agent_with_actions.py` completed:

```text
python activities/advanced-action-tools/validate.py --all
# ✅ Step 1 PASS — Action Tools backend reachable at http://localhost:8080
# ✅ Step 2 PASS — action FunctionTool defined (northfield actions @ ACTION_API_URL)
# ✅ Step 3 PASS — human tool-approval loop implemented
# ✅ Step 4 PASS — action round-tripped through the backend (ticket ...)
# ✅ ALL CHECKPOINTS PASS

```
Steps 1 & 4 require the provided backend running; Steps 2 & 3 are static checks on the wiring file.
Before completion, Steps 2/3 correctly FAIL on the unfilled `< PLACEHOLDER >` markers.
