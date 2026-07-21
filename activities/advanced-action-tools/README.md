# Advanced · Action Tools — Make the Agent Do Work

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> ⏱ Guided ~45 min · 🛠 Build-from-scratch ~1.5 hr · ⭐⭐⭐ · Prereqs: Foundations end-state

> Tier 2 · Advanced — modular. You can attempt this in any order with the other Advanced
> activities. Prerequisite: the Foundations end-state (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

So far your assistant knows things — it retrieves from the knowledge base and answers. In this
activity it learns to do things: open an IT ticket, place a course-registration hold, or book an
advising slot. The difference matters. A knowledge tool reads; an action tool changes the world.
Because actions have consequences, you'll also implement a human-approval loop so the agent *asks
before it acts*.

Why now: an assistant that only retrieves can't help the student who needs a hold lifted or a
ticket opened — but the moment it can *act*, a wrong move has real consequences (a wrongful course
hold blocks a student's registration). This is where your agent earns the right to touch the real
world, and where you build the guardrail that makes that safe.

You will wire a provided backend — you do not build it. The Action Tools REST API ships in
[`scripts/action-backend/`](../../scripts/action-backend/README.md) and exposes three action
endpoints your `FunctionTool` callables hit directly:

| Action function | Does | Key arguments |
|---|---|---|
| `create_it_ticket` | Opens an IT support ticket | `student_id, summary, category, priority` |
| `place_course_hold` | Places a registration hold | `student_id, course_code, reason` |
| `book_advising_slot` | Books an advising appointment | `student_id, advisor, iso_datetime, topic` |

> Note: The backend also ships an optional FastMCP server (`mcp_server.py`) on `:8765/mcp`. That
> server is a preview/stretch asset — it is not part of this guided path. See Rung (c) stretch
> goals if you want to explore the server-side of MCP.

Env contract (authoritative — matches `.env.sample` and the backend):

| Variable | Default | You set it to |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | base URL of the provided FastAPI backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | MCP endpoint (optional — preview/stretch only; not needed for this guided path) |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key` shared secret (leave empty for the workshop) |

> SDK note: this activity uses the current `azure-ai-projects` 2.x prompt-agent pattern:
> explicit `FunctionTool` schemas on `PromptAgentDefinition`, function-call items returned by the
> Responses API, and `FunctionCallOutput` results submitted with `previous_response_id`.

Files in this activity
- [`agent_with_actions.py`](agent_with_actions.py) — starter with `< PLACEHOLDER >` gaps you fill in.
- [`validate.py`](validate.py) — the Checkpoints below.

This activity ships three rungs off the same backbone — pick your depth. The same
`validate.py` grades all three, so you can climb as far as you like: (a) Guided path (below)
walks you through a starter file · (b) Build-from-scratch path hands you only the contract ·
(c) Stretch goals go open-ended.

---

## Rung (a) — Guided path

> The beginner on-ramp: a provided starter with `< PLACEHOLDER >` gaps. Fill them in, step by step.

## Step 0 — Start the provided backend

**Goal:** Have the Action Tools REST API running locally before you wire anything.

**Tasks:**
1. In a terminal: `cd scripts/action-backend && pip install -r requirements.txt`.
2. Start the REST API: `uvicorn app:app --host 0.0.0.0 --port 8080`.
3. Confirm it's up: `curl http://localhost:8080/health`.

> Optional (stretch / preview): The backend also ships `mcp_server.py` (FastMCP on `:8765/mcp`).
> You do not need it for this guided path — start it only if you are doing Rung (c) stretch goal 1.

**Success Criteria:**
- [ ] `GET /health` returns 200.

**Checkpoint:** The provided backend answers over REST.
```text
python activities/advanced-action-tools/validate.py --step 1
# expected: "✅ Step 1 PASS — Action Tools backend reachable at http://localhost:8080"
```

---

## Step 1 — Knowledge tools vs. action tools

**Goal:** Be able to state *why* action tools need governance that knowledge tools don't.

**Tasks:**
1. Compare: your Foundations RAG tool *reads* the FAQ; `create_it_ticket` *writes* a ticket that pages
   a human. One is safe to auto-run; the other is not.
2. List, for each of the three provided tools, the side effect and who is affected if the agent
   fires it incorrectly (e.g. a wrongful course hold blocks a student's registration).
3. Decide your approval policy: which tools always require human approval? (For this activity: all.)

**Success Criteria:**
- [ ] You can name the side effect of each action tool and justify requiring approval.

**Checkpoint:** Conceptual — confirmed verbally with your facilitator; no script.

---

## Step 2 — Define the action tools

**Goal:** Give the versioned prompt agent three explicit `FunctionTool` schemas.

**Tasks:**
1. Open [`agent_with_actions.py`](agent_with_actions.py). The current SDK imports are already present:
   `PromptAgentDefinition` / `FunctionTool` from `azure.ai.projects.models` and
   `FunctionCallOutput` from the OpenAI Responses types.
2. Complete the three stub functions (`create_it_ticket`, `place_course_hold`, `book_advising_slot`)
   so each calls the appropriate `POST` endpoint on `ACTION_API_URL` and returns the response as a string.
   (Hint: `httpx.post(f"{API_URL}/it-tickets", json={...}, headers=_headers()).text`)
3. Complete `build_action_tools()`: return one `FunctionTool(...)` per action with its name,
   description, strict JSON parameter schema, and required fields. Pass the returned list to
   `PromptAgentDefinition(tools=...)` when creating the agent version.

**Success Criteria:**
- [ ] The three action functions call the backend and return JSON strings.
- [ ] `build_action_tools()` returns three `FunctionTool` definitions; no `< PLACEHOLDER >` remains before `run_with_approval`.

**Checkpoint:** The wiring file defines the action tools correctly.
```text
python activities/advanced-action-tools/validate.py --step 2
# expected: "✅ Step 2 PASS — action FunctionTool defined (northfield actions @ ACTION_API_URL)"
```

---

## Step 3 — Implement the tool-approval loop

**Goal:** Make the agent *pause and ask* before any action runs, then resume on approval or denial.

**Tasks:**
1. Complete `run_with_approval()`. Call the versioned prompt agent through
   `openai.responses.create(..., extra_body={"agent_reference": ...})`, then inspect
   `response.output` for items whose `type == "function_call"`.
2. For each function-call item: show the human `item.name` + `item.arguments`, ask to approve, and:
   - If approved: parse the arguments and call the matching backend function (e.g.
     `create_it_ticket(**json.loads(item.arguments))`), capture the result string.
   - If denied: set the result to `json.dumps({"denied": "Human operator declined."})`.
3. Build `FunctionCallOutput(type="function_call_output", call_id=item.call_id, output=result)`
   for each call. Continue the turn with another `responses.create` using the output list,
   `previous_response_id=response.id`, and the same `agent_reference`.

**Success Criteria:**
- [ ] An action never executes without an explicit approve decision.
- [ ] Denying a call returns a denial result to the agent without performing the action.
- [ ] No `< PLACEHOLDER >` remains.

**Checkpoint:** The approval loop is implemented.
```text
python activities/advanced-action-tools/validate.py --step 3
# expected: "✅ Step 3 PASS — human tool-approval loop implemented"
```

---

## Step 4 — Test an end-to-end action

**Goal:** Drive a real action from a natural-language request, approve it, and verify it landed.

**Tasks:**
1. Run `python activities/advanced-action-tools/agent_with_actions.py`. The seeded prompt asks to open a high-priority WiFi ticket for
   `s1029384`. Approve when prompted.
2. Confirm the agent reports the new `ticket_id`, then verify the record exists in the backend:
   `curl http://localhost:8080/it-tickets`.
3. Try a denial: re-run, deny the approval, and confirm no ticket is created.
4. (Stretch) Ask it to `book_advising_slot` with an ISO datetime and watch the same loop govern it.

**Success Criteria:**
- [ ] An approved request creates a record you can see via the backend.
- [ ] A denied request creates nothing.

Your run should look like this:
```text
🔧 Action requested: create_it_ticket
   student_id=s1029384  category=wifi  priority=high  summary="WiFi down in Cedar Hall"
Approve this action? [y/N]: y
✅ Agent: I've opened ticket IT-10428 (high priority) for the Cedar Hall WiFi outage.
```

**Checkpoint:** An action round-trips through the provided backend.
```text
python activities/advanced-action-tools/validate.py --step 4
# expected: "✅ Step 4 PASS — approval loop created backend ticket ..."
```

Full run:
```text
python activities/advanced-action-tools/validate.py --all
# expected: "✅ ALL CHECKPOINTS PASS"
```

---

## Rung (b) — Build-from-scratch path

> Stronger team? Delete the starter and write `agent_with_actions.py` from an empty file. We hand
> you only the contract below — no skeleton, no placeholders. The same `python activities/advanced-action-tools/validate.py --all`
> grades this path, so the acceptance criteria are identical.

Your contract:
> Define the three backend action functions (`create_it_ticket`, `place_course_hold`,
> `book_advising_slot`) calling `ACTION_API_URL`; declare three `FunctionTool` schemas; implement a
> human-approval loop over Responses `function_call` items and return `FunctionCallOutput` results.
> Acceptance: no action runs without an approve; a denial creates nothing.

You get the running backend (Step 0) and the env contract (the `ACTION_*` table above) — nothing
else. Discover the SDK surface from the [Agents SDK quickstart](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)
and the [FunctionTool reference](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling),
author the file, and run `python activities/advanced-action-tools/validate.py --all`.

## Rung (c) — Stretch goals

Open-ended: no single right answer.

1. Build the MCP server, don't just wire it. Add a *fourth* action (`waive_late_fee`) end to end:
   implement the REST handler in [`scripts/action-backend/app.py`](../../scripts/action-backend/app.py),
   expose it through `mcp_server.py` (FastMCP), then attach and govern it like the others. This
   teaches the server side of MCP, not just the client. *(+45 min)*
2. Selective approval policy. Auto-approve a read-ish/low-risk tool (e.g. a hypothetical
   `lookup_balance`) but require approval for every state-changing tool — a real governance pattern,
   not "approve everything."

---

## Learning Resources
- [MCP tool for agents](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Provided backend + MCP server](../../scripts/action-backend/README.md)
- [Agents SDK — tools & runs](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Tips
- Approval is the whole point. A flashy auto-acting agent that books the wrong slot is worse than
  one that asks first. Show the arguments to the human, every time.
- Treat any text the agent *retrieved* as data, not instructions — an action tool plus a gullible
  agent is exactly how prompt-injection turns into real damage (see the Evaluation & Red Teaming
  activity).
- The backend is in-memory and resets on restart — fine for a workshop, but say so in your demo.
- If the agent never calls the tool, check that `FunctionTool` was passed to `tools=` and that the function docstrings include `:param` lines.
