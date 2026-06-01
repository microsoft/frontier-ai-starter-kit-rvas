# Action Tools Backend + MCP Server

> **Provided infrastructure for the Advanced challenge "Action Tools — Make the Agent Do Work."**
> Teams **wire** this into their agent; they do **not** build it. It gives the Northfield IQ
> Assistant *hands*: create an IT ticket, place a course hold, and book an advising slot.

Two processes:

1. **`app.py`** — a FastAPI REST API with an in-memory store (resets on restart).
2. **`mcp_server.py`** — a FastMCP server that wraps the REST API and exposes the three
   actions as **MCP tools** an agent attaches via `McpTool`.

---

## Env contract (authoritative — matches repo `.env.sample`)

| Variable | Default | Used by | Meaning |
|---|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | MCP server, challenge | Base URL of the FastAPI backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | agent, challenge | MCP endpoint students attach as `McpTool` |
| `ACTION_API_KEY` | *(empty)* | backend, MCP server | Optional `x-api-key` shared secret; empty = open/no-auth |

> If you change a name here, change it in `.env.sample` and the challenge content too.

---

## Run it

From this folder:

```bash
# 1. (recommended) isolated env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. start the REST backend  -> ACTION_API_URL (http://localhost:8080)
uvicorn app:app --host 0.0.0.0 --port 8080

# 3. in a second terminal, start the MCP server -> ACTION_MCP_URL (http://localhost:8765/mcp)
python mcp_server.py
```

Optional auth for both processes:

```bash
export ACTION_API_KEY="dev-secret"   # set in BOTH terminals before starting
```

---

## Smoke test

```bash
# health
curl http://localhost:8080/health

# create an IT ticket (add  -H "x-api-key: dev-secret"  if ACTION_API_KEY is set)
curl -X POST http://localhost:8080/it-tickets \
  -H "Content-Type: application/json" \
  -d '{"student_id":"s1029384","category":"wifi","summary":"No eduroam in dorm","priority":"high"}'

# place a course hold
curl -X POST http://localhost:8080/course-holds \
  -H "Content-Type: application/json" \
  -d '{"student_id":"s1029384","course_code":"CS101","reason":"Prereq check"}'

# book an advising slot
curl -X POST http://localhost:8080/advising-slots \
  -H "Content-Type: application/json" \
  -d '{"student_id":"s1029384","advisor":"Dr. Lee","iso_datetime":"2026-06-10T15:00:00Z","topic":"Fall planning"}'
```

Interactive API docs: <http://localhost:8080/docs>.

---

## Attaching to a Foundry agent (what teams build)

```python
import os
from azure.ai.agents.models import McpTool

actions = McpTool(
    server_label="northfield_actions",
    server_url=os.environ["ACTION_MCP_URL"],   # http://localhost:8765/mcp
)
# add `actions.definitions` to the agent's tools and implement the
# RequiredMcpToolCall -> SubmitToolApprovalAction human-approval loop.
```

The challenge teaches the **tool-approval loop** (the agent asks before acting) and the
knowledge-vs-action tool distinction. See `challenges/advanced-action-tools/`.

---

## Notes

- **In-memory only** — state is lost on restart. That is intentional for a workshop.
- For a public demo over the internet, front the MCP server with a tunnel (e.g. `azd`/Container
  Apps or a dev tunnel) and set `ACTION_MCP_URL` to the public URL.
- No secrets are committed. `ACTION_API_KEY` is read from the environment only.
