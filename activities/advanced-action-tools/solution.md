# Implementation notes — Advanced Action Tools

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

These notes capture the reusable implementation mechanics behind the activity. Use them to adapt the
approval-loop pattern to a scenario-specific action backend.

## What this activity is really teaching

The leap from a **knowledge** agent (reads/answers) to an **action** agent (changes state) — and the
governance that leap demands. Both reference repos stop at knowledge tools or auto-firing actions;
this activity adds the **human-in-the-loop approval** that real deployments require. The pedagogical
core is the application-owned `function_call → approve/deny → FunctionCallOutput` loop: the model
requests an action, the human decides, and only then can application code execute it.

> **SDK note:** the current path is `azure-ai-projects` 2.x:
> `agents.create_version(PromptAgentDefinition(...))`, Responses `function_call` items, and
> `FunctionCallOutput` in a Foundry conversation. Do not use retired `agents.threads` /
> `agents.runs` examples for this pattern.

## Env contract (authoritative — keep in lockstep)

| Variable | Default | Notes |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | provided FastAPI backend base URL |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | MCP endpoint shipped by backend — **optional**, preview/stretch only; not required for the guided path |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key`; leave empty for the workshop |

We **ship the backend** so teams stay on the approval-loop objective instead of building a CRUD API.
It lives in `scripts/action-backend/` (FastAPI `app.py` + FastMCP `mcp_server.py`) and exposes three
REST endpoints (`/it-tickets`, `/course-holds`, `/advising-slots`) that the FunctionTool callables hit.

## Runtime setup

```bash
# provided backend (REST — required)
cd scripts/action-backend && pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080      # terminal 1
# optional: python mcp_server.py               # only for stretch goal 1 (MCP server exploration)
# agent side
az login                                        # keyless DefaultAzureCredential
# .env: AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME, ACTION_API_URL
```

## Implementation notes by step

### Step 0 / Step 1 — backend reachable
- `python activities/advanced-action-tools/validate.py --step 1` hits `GET /health` over REST. If it fails, the backend isn't running or
  `ACTION_API_URL` is wrong.

### Step 1 — knowledge vs action
- Side effects change the risk boundary. The sample actions open a ticket, place a hold, and book a
  slot; replace them with the scenario's approved actions. Any action that changes state, spends
  money, exposes data, or affects a user's access should require approval.

### Step 2 — define the action FunctionTool
Reference completion of `build_action_tools()` and the three action stubs:
```python
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from openai.types.responses.response_input_param import FunctionCallOutput
import httpx, json, os

API_URL = os.environ.get("ACTION_API_URL", "http://localhost:8080").rstrip("/")
API_KEY = os.environ.get("ACTION_API_KEY", "").strip()

def _headers():
    return {"x-api-key": API_KEY} if API_KEY else {}

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

def place_course_hold(student_id, course_code, reason):
    """Place a registration hold on a course for a student.

    :param student_id: University student identifier.
    :param course_code: Course code to hold (e.g. CS101).
    :param reason: Reason for the hold.
    """
    r = httpx.post(f"{API_URL}/course-holds",
                   json={"student_id": student_id, "course_code": course_code, "reason": reason},
                   headers=_headers(), timeout=10.0)
    r.raise_for_status()
    return r.text

def book_advising_slot(student_id, advisor, iso_datetime, topic="General advising"):
    """Book an academic advising slot.

    :param student_id: University student identifier.
    :param advisor: Advisor name (e.g. Dr. Lee).
    :param iso_datetime: ISO 8601 datetime for the slot (e.g. 2026-06-10T15:00:00Z).
    :param topic: Topic to discuss.
    """
    r = httpx.post(f"{API_URL}/advising-slots",
                   json={"student_id": student_id, "advisor": advisor,
                         "iso_datetime": iso_datetime, "topic": topic},
                   headers=_headers(), timeout=10.0)
    r.raise_for_status()
    return r.text

def build_action_tools():
    return [
        FunctionTool(
            name="create_it_ticket",
            description="Open an IT support ticket for a student.",
            parameters={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string"},
                    "summary": {"type": "string"},
                    "category": {"type": "string", "enum": ["wifi", "account", "hardware", "software", "other"]},
                    "priority": {"type": "string", "enum": ["low", "normal", "high", "urgent"]},
                },
                "required": ["student_id", "summary", "category", "priority"],
                "additionalProperties": False,
            },
            strict=True,
        ),
        FunctionTool(
            name="place_course_hold",
            description="Place a registration hold on a course for a student.",
            parameters={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string"},
                    "course_code": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["student_id", "course_code", "reason"],
                "additionalProperties": False,
            },
            strict=True,
        ),
        FunctionTool(
            name="book_advising_slot",
            description="Book an academic advising slot for a student.",
            parameters={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string"},
                    "advisor": {"type": "string"},
                    "iso_datetime": {"type": "string"},
                    "topic": {"type": "string"},
                },
                "required": ["student_id", "advisor", "iso_datetime", "topic"],
                "additionalProperties": False,
            },
            strict=True,
        ),
    ]
```
- **Pitfall:** `azure-ai-projects` 2.x requires explicit function names, descriptions, and JSON
  parameter schemas. The old `FunctionTool(functions={...})` reflection helper belongs to the
  retired threads/runs surface and is not used here.
- **`python activities/advanced-action-tools/validate.py --step 2`** checks for `FunctionTool`, the three function names, and `ACTION_API_URL`.
  It FAIL/PLACEHOLDERs out if the stubs aren't filled.

### Step 3 — the approval loop (the heart of it)
Reference completion of `run_with_approval()`:
```python
def run_with_approval(openai, agent_name, prompt):
    conversation = openai.conversations.create()
    try:
        response = openai.responses.create(
            input=prompt,
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        )
        while any(item.type == "function_call" for item in response.output):
            outputs = []
            for item in response.output:
                if item.type != "function_call":
                    continue
                args = json.loads(item.arguments)
                print(f"\nAction requested: {item.name}\n  {item.arguments}")
                approved = input("Approve this action? [y/N] ").strip().lower() == "y"
                if approved:
                    fn_map = {
                        "create_it_ticket": create_it_ticket,
                        "place_course_hold": place_course_hold,
                        "book_advising_slot": book_advising_slot,
                    }
                    fn = fn_map.get(item.name)
                    result = (
                        fn(**args)
                        if fn is not None
                        else json.dumps({"error": f"Unknown action: {item.name}"})
                    )
                else:
                    result = json.dumps({"denied": "Human operator declined."})
                outputs.append(FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result,
                ))
            response = openai.responses.create(
                input=outputs,
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            )
        return response
    finally:
        openai.conversations.delete(conversation_id=conversation.id)
```
- **Implementation points:** (1) the application receives a requested function call and executes
  nothing until the human decides; (2) showing the function name + arguments to the human is the
  governance moment; (3) returning the denial JSON
  cleanly tells the agent "you were blocked" so it can report back gracefully.
- **Pitfall:** omitting `conversation=conversation.id` on either call loses the tool-call turn context.
- **Pitfall:** `item.arguments` is a **JSON string** — parse it with `json.loads` before
  unpacking as `**args`.

### Step 4 — end-to-end
- `python activities/advanced-action-tools/validate.py --step 4` imports the learner's completed
  `run_with_approval()`, supplies a deterministic fake Responses function call, approves it, and
  verifies the real backend record. This catches broken dispatch and continuation wiring without
  consuming model quota.
- The real proof is: natural-language prompt → approve → agent reports a `ticket_id` → `curl
  /it-tickets` shows it. Then the **denial** path: deny → nothing created. Make every team run the
  denial — it's where the governance lesson lands.

## Common issues & fast unblocks
- **`Step 1 FAIL — backend not reachable`** → backend not started / wrong `ACTION_API_URL`.
- **Model never calls the tool** → function docstrings missing `:param` lines, or `FunctionTool` not passed to `tools=`.
- **Agent loses context after approval** → pass the same `conversation=conversation.id` on both calls.
- **`Unauthorized` to backend** → `ACTION_API_KEY` set on one process but not the other; either set it
  in both terminals or unset it everywhere for the workshop.
- **Auto-approve everything** → out of scope for this activity; the approval gate is the point.

## Verification

With the backend running and `agent_with_actions.py` completed, run:

```bash
python activities/advanced-action-tools/validate.py --all
```

Steps 1 and 4 require the provided backend. Step 4 executes the completed approval loop against a
deterministic fake Responses client, then verifies the backend record. Steps 2 and 3 are structural
checks that catch missing tool definitions and unfinished approval-loop wiring.
