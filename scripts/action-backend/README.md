# Action Tools Backend + MCP Server

> **Provided infrastructure for the Advanced activity "Action Tools — Make the Agent Do Work."**
> Teams **wire** this into their agent; they do **not** build it. It gives the Northfield IQ
> Assistant *hands*: create an IT ticket, place a course hold, and book an advising slot.

Two processes:

1. **`app.py`** — a FastAPI REST API with an in-memory store (resets on restart).
2. **`mcp_server.py`** — an optional FastMCP server that wraps the REST API for stretch work.
   The guided Action Tools activity uses supported `FunctionTool` wrappers against the REST API.

---

## Env contract (authoritative — matches repo `.env.sample`)

| Variable | Default | Used by | Meaning |
|---|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | MCP server, activity | Base URL of the FastAPI backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | MCP server, stretch | Optional FastMCP endpoint for Rung (c) / preview explorations |
| `ACTION_API_KEY` | *(empty)* | backend, MCP server | Optional `x-api-key` for REST mutations; the MCP server forwards it to the backend |

> If you change a name here, change it in `.env.sample` and the activity content too.

---

## Run it

From this folder:

```bash
# 1. (recommended) isolated env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. start the REST backend  -> ACTION_API_URL (http://localhost:8080)
uvicorn app:app --host 127.0.0.1 --port 8080

# 3. optional stretch: in a second terminal, start the MCP server -> ACTION_MCP_URL
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

## Wiring this backend into a Foundry agent

The supported guided path is:

1. Start `app.py`.
2. Implement Python functions that call `ACTION_API_URL` (`/it-tickets`, `/course-holds`,
   `/advising-slots`).
3. Wrap those functions in `FunctionTool`.
4. Govern each Responses `function_call` with explicit human approval, then return a
   `FunctionCallOutput` and continue with `previous_response_id`.

The FastMCP server is a stretch asset for teams that want to explore the server side of MCP. Before
attaching it directly to an agent, verify the current MCP tool and approval APIs in Microsoft Learn;
the guided activity intentionally avoids preview-only client-side approval classes.

See `activities/advanced-action-tools/` for the supported workshop implementation.

---

## Security and deployment notes

- **In-memory only** — state is lost on restart. That is intentional for a workshop.
- Both provided processes bind to loopback by default for local development. `ACTION_MCP_URL` controls
  the path exposed by the MCP server. For a loopback URL, a specified port is used by the local listener;
  for an externally advertised tunnel/proxy URL, the server still listens on `127.0.0.1:8765`.
- The provided FastMCP endpoint has **no incoming MCP authentication**. `ACTION_API_KEY` protects
  mutating REST calls between the MCP server and `app.py`; it does not authenticate an MCP client.
  Do not expose this workshop endpoint through a public tunnel. For remote use, deploy it behind an
  MCP-compatible OAuth/token-validation layer (or configure FastMCP's documented HTTP auth provider)
  and test client discovery and authorization before allowing write tools.
- No secrets are committed. `ACTION_API_KEY` is read from the environment only.
