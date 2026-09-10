# Advanced · Action Tools — Make the Agent Do Work

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> ⏱ Guided ~45 min · 🛠 Build-from-scratch ~1.5 hr · ⭐⭐⭐ · Prereqs: Foundations end-state

> **Canonical approval, refusal, and action-provenance module.** Use it when a scenario needs a governed action seam. Prerequisite: a
> deployed Foundry agent from your scenario or the Foundations mechanics reference. Complete the
> required foundation, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

Your assistant can retrieve information and answer questions. This activity lets it open a ticket,
place a hold, book a slot, start a workflow, or call another approved system. Knowledge tools read.
Action tools change state.

Actions have consequences. Build a human-approval loop so the agent *asks before it acts*. Record
the requested function, arguments, human decision, result, and request correlation with each action.
Other activities reuse this pattern; they do not define a competing action policy.

You will wire a provided backend — you do not build it. The Action Tools REST API ships in
[`scripts/action-backend/`](../../scripts/action-backend/README.md) and exposes three action
endpoints your `FunctionTool` callables hit directly:

| Action function | Does | Key arguments |
|---|---|---|
| `create_it_ticket` | Opens a support ticket | `student_id, summary, category, priority` |
| `place_course_hold` | Places a sample hold | `student_id, course_code, reason` |
| `book_advising_slot` | Books an appointment | `student_id, advisor, iso_datetime, topic` |

> Note: The backend also ships an optional FastMCP server (`mcp_server.py`) on `:8765/mcp`. That
> server is an optional preview asset. It is outside the guided path; use the optional extension if
> you want to explore the server-side of MCP.

Env contract (authoritative — matches `.env.sample` and the backend):

| Variable | Default | You set it to |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | base URL of the provided FastAPI backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | MCP endpoint (optional — preview/stretch only; not needed for this guided path) |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key` shared secret (leave empty for the workshop) |

> SDK note: this activity uses the current `azure-ai-projects` 2.x prompt-agent pattern:
> explicit `FunctionTool` schemas on `PromptAgentDefinition`, function-call items returned by the
> Responses API, and `FunctionCallOutput` results submitted in the same Foundry conversation.

Files in this activity
- [`agent_with_actions.py`](agent_with_actions.py) — starter with `< PLACEHOLDER >` gaps you fill in.
- [`validate.py`](validate.py) — the Verify checks below.

Use the guided steps with the starter file. The validator checks the same contract if a team chooses
to build the file from scratch.

## Step 0 — Start the provided backend

**Goal:** Have the Action Tools REST API running locally before you wire anything.

**Tasks:**
1. In a terminal: `cd scripts/action-backend && pip install -r requirements.txt`.
2. Start the REST API: `uvicorn app:app --host 0.0.0.0 --port 8080`.
3. Confirm it's up: `curl http://localhost:8080/health`.

> Optional preview: The backend also ships `mcp_server.py` (FastMCP on `:8765/mcp`). Start it only
> for the MCP extension.

**Success Criteria:**
- [ ] `GET /health` returns 200.

**Verify:** The provided backend answers over REST.
```text
python activities/advanced-action-tools/validate.py --step 1
```

---

## Step 1 — Knowledge tools vs. action tools

**Goal:** Be able to state *why* action tools need governance that knowledge tools don't.

**Tasks:**
1. Compare: your Foundations RAG tool *reads* the FAQ; `create_it_ticket` *writes* a ticket that pages
   a human. One is safe to auto-run; the other is not.
2. List, for each of the three provided tools, the side effect and who is affected if the agent
   fires it incorrectly.
3. Decide your approval policy: which tools always require human approval? (For this activity: all.)

**Success Criteria:**
- [ ] You can name the side effect of each action tool and justify requiring approval.

**Verify:** You can explain the side effect and approval boundary for each action. No script is
needed for this conceptual check.

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

**Verify:** The wiring file defines the action tools correctly.
```text
python activities/advanced-action-tools/validate.py --step 2
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
3. Create a conversation before the initial call with `openai.conversations.create()`. Build
   `FunctionCallOutput(type="function_call_output", call_id=item.call_id, output=result)` for each
   call. Continue the turn with another `responses.create` using the output list, the same
   `conversation=conversation.id`, and the same `agent_reference`. Delete the conversation when done.

**Success Criteria:**
- [ ] An action never executes without an explicit approve decision.
- [ ] Denying a call returns a denial result to the agent without performing the action.
- [ ] No `< PLACEHOLDER >` remains.

**Verify:** The approval loop is implemented.
```text
python activities/advanced-action-tools/validate.py --step 3
```

---

## Step 4 — Test an end-to-end action

**Goal:** Drive a real action from a natural-language request, approve it, and verify it landed.

**Tasks:**
1. Run `python activities/advanced-action-tools/agent_with_actions.py`. The seeded prompt asks to open a high-priority WiFi ticket for
   sample user. Approve when prompted.
2. Confirm the agent reports the new `ticket_id`, then verify the record exists in the backend:
   `curl http://localhost:8080/it-tickets`.
3. Try a denial: re-run, deny the approval, and confirm no ticket is created.
4. Optionally, ask it to `book_advising_slot` with an ISO datetime and watch the same loop govern it.

**Success Criteria:**
- [ ] An approved request creates a record you can see via the backend.
- [ ] A denied request creates nothing.

Your run should look like this:
```text
🔧 Action requested: create_it_ticket
   student_id=s1029384  category=wifi  priority=high  summary="WiFi down in the sample site"
Approve this action? [y/N]: y
✅ Agent: I've opened ticket IT-10428 (high priority) for the Cedar Hall WiFi outage.
```

**Verify:** An action round-trips through the provided backend.
```text
python activities/advanced-action-tools/validate.py --step 4
```

Full run:
```text
python activities/advanced-action-tools/validate.py --all
```

---

## Build from scratch

> Write `agent_with_actions.py` from an empty file. This path provides only the contract below.
> `python activities/advanced-action-tools/validate.py --all` uses the same acceptance criteria.

Your contract:
> Define the three backend action functions (`create_it_ticket`, `place_course_hold`,
> `book_advising_slot`) calling `ACTION_API_URL`; declare three `FunctionTool` schemas; implement a
> human-approval loop over Responses `function_call` items and return `FunctionCallOutput` results.
> Acceptance: no action runs without an approve; a denial creates nothing.

You get the running backend (Step 0) and the env contract (the `ACTION_*` table above) — nothing
else. Discover the SDK surface from the [Agents SDK quickstart](https://learn.microsoft.com/azure/foundry/quickstarts/get-started-code)
and the [FunctionTool reference](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling),
author the file, and run `python activities/advanced-action-tools/validate.py --all`.

## Optional extensions

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
- Approval is the point. An auto-acting agent that books the wrong slot is worse than one that asks
  first. Show the arguments to the human every time.
- Treat any text the agent *retrieved* as data, not instructions — an action tool plus a gullible
  agent is exactly how prompt-injection turns into real damage (see the Evaluation & Red Teaming
  activity).
- The backend is in-memory and resets on restart — fine for a workshop, but say so in your demo.
- If the agent never calls the tool, check that `FunctionTool` was passed to `tools=` and that the function docstrings include `:param` lines.
