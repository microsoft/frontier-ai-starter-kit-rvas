# Advanced · Action Tools — Make the Agent Do Work

> ⏱ **Guided ~45 min** · 🛠 **Build-from-scratch ~1.5 hr** · ⭐⭐⭐ · **Prereqs:** Foundations end-state

> **Tier 2 · Advanced — modular.** You can attempt this in any order with the other Advanced
> challenges. **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

So far your assistant **knows** things — it retrieves from the knowledge base and answers. In this
challenge it learns to **do** things: open an IT ticket, place a course-registration hold, or book an
advising slot. The difference matters. A **knowledge tool** reads; an **action tool** changes the world.
Because actions have consequences, you'll also implement a **human-approval loop** so the agent *asks
before it acts*.

**Why now:** an assistant that only retrieves can't help the student who needs a hold lifted or a
ticket opened — but the moment it can *act*, a wrong move has real consequences (a wrongful course
hold blocks a student's registration). This is where your agent earns the right to touch the real
world, and where you build the guardrail that makes that safe.

You will **wire** a provided backend — you do **not** build it. The Action Tools REST API + MCP server
ship in [`scripts/action-backend/`](../../scripts/action-backend/README.md) and already expose three
MCP tools:

| MCP tool | Does | Key arguments |
|---|---|---|
| `create_it_ticket` | Opens an IT support ticket | `student_id, summary, category, priority` |
| `place_course_hold` | Places a registration hold | `student_id, course_code, reason` |
| `book_advising_slot` | Books an advising appointment | `student_id, advisor, iso_datetime, topic` |

**Env contract (authoritative — matches `.env.sample` and the backend):**

| Variable | Default | You set it to |
|---|---|---|
| `ACTION_API_URL` | `http://localhost:8080` | base URL of the provided FastAPI backend |
| `ACTION_MCP_URL` | `http://localhost:8765/mcp` | **the MCP endpoint you attach as `McpTool`** |
| `ACTION_API_KEY` | *(empty)* | optional `x-api-key` shared secret (leave empty for the workshop) |

**Files in this challenge**
- [`agent_with_actions.py`](agent_with_actions.py) — **starter** with `< PLACEHOLDER >` gaps you fill in.
- [`validate.py`](validate.py) — the Checkpoints below.

This challenge ships **three rungs** off the same backbone — pick your depth. The **same
`validate.py` grades all three**, so you can climb as far as you like: **(a) Guided path** (below)
walks you through a starter file · **(b) Build-from-scratch path** hands you only the contract ·
**(c) Stretch goals** go open-ended.

---

## Rung (a) — Guided path

> The beginner on-ramp: a provided starter with `< PLACEHOLDER >` gaps. Fill them in, step by step.

## Step 0 — Start the provided backend

**Goal:** Have the Action Tools REST API + MCP server running locally before you wire anything.

**Tasks:**
1. In a terminal: `cd scripts/action-backend && pip install -r requirements.txt`.
2. Start the REST API: `uvicorn app:app --host 0.0.0.0 --port 8080`.
3. In a second terminal: `python mcp_server.py` (serves `ACTION_MCP_URL` at `:8765/mcp`).
4. Confirm both are up — `curl http://localhost:8080/health` and the MCP server's startup banner.

**Success Criteria:**
- [ ] `GET /health` returns 200.
- [ ] The MCP server prints `Action Tools MCP server -> http://...:8765/mcp`.

**Checkpoint:** The provided backend answers over REST.
```text
python validate.py --step 1
# expected: "✅ Step 1 PASS — Action Tools backend reachable at http://localhost:8080"
```

---

## Step 1 — Knowledge tools vs. action tools

**Goal:** Be able to state *why* action tools need governance that knowledge tools don't.

**Tasks:**
1. Compare: your Foundations RAG tool *reads* the FAQ; `create_it_ticket` *writes* a ticket that pages
   a human. One is safe to auto-run; the other is not.
2. List, for each of the three provided tools, the **side effect** and **who is affected** if the agent
   fires it incorrectly (e.g. a wrongful course hold blocks a student's registration).
3. Decide your approval policy: which tools always require human approval? (For this challenge: **all**.)

**Success Criteria:**
- [ ] You can name the side effect of each action tool and justify requiring approval.

**Checkpoint:** Conceptual — confirmed verbally with your coach; no script.

---

## Step 2 — Attach the MCP action tool

**Goal:** Give the agent the three actions by attaching the provided MCP server as an `McpTool`.

**Tasks:**
1. Open [`agent_with_actions.py`](agent_with_actions.py). Add the import:
   `from azure.ai.agents.models import McpTool, RequiredMcpToolCall, SubmitToolApprovalAction, ToolApproval`.
2. Complete `build_action_tool()`: construct an `McpTool` with `server_label="northfield_actions"` and
   `server_url=os.environ["ACTION_MCP_URL"]`. Keep approval **on**.
3. Add the tool to the agent's `tools` when you create it. (Hint: an `McpTool` exposes its wire
   format on an attribute — discover which one rather than guessing.)

**Success Criteria:**
- [ ] The agent is created with the `northfield_actions` MCP tool attached.
- [ ] No `< PLACEHOLDER >` remains in the tool-attach section.

**Checkpoint:** The wiring file attaches the action tool correctly.
```text
python validate.py --step 2
# expected: "✅ Step 2 PASS — MCP action tool attached (northfield_actions @ ACTION_MCP_URL)"
```

---

## Step 3 — Implement the tool-approval loop

**Goal:** Make the agent *pause and ask* before any action runs, then resume on approval.

**Tasks:**
1. Complete `run_with_approval()`. When `run.status == "requires_action"`, the run is paused on one or
   more `RequiredMcpToolCall` items in `run.required_action.submit_tool_approval.tool_calls`.
2. For each tool call: **show the human the tool name + arguments**, ask to approve, and build a
   `ToolApproval(tool_call_id=<id>, approve=<True/False>)`.
3. Submit the decisions with `SubmitToolApprovalAction` via `agents.runs.submit_tool_outputs(...)`, then
   keep polling until the run leaves `requires_action`. This **closes the function-call loop**.

**Success Criteria:**
- [ ] An action never executes without an explicit approve decision.
- [ ] Denying a call cleanly ends the run without performing the action.
- [ ] No `< PLACEHOLDER >` remains.

**Checkpoint:** The approval loop is implemented.
```text
python validate.py --step 3
# expected: "✅ Step 3 PASS — human tool-approval loop implemented"
```

---

## Step 4 — Test an end-to-end action

**Goal:** Drive a real action from a natural-language request, approve it, and verify it landed.

**Tasks:**
1. Run `python agent_with_actions.py`. The seeded prompt asks to open a high-priority WiFi ticket for
   `s1029384`. Approve when prompted.
2. Confirm the agent reports the new `ticket_id`, then verify the record exists in the backend:
   `curl http://localhost:8080/it-tickets`.
3. Try a **denial**: re-run, deny the approval, and confirm no ticket is created.
4. (Stretch) Ask it to `book_advising_slot` with an ISO datetime and watch the same loop govern it.

**Success Criteria:**
- [ ] An approved request creates a record you can see via the backend.
- [ ] A denied request creates nothing.

**Your run should look like this:**
```text
🔧 Action requested: create_it_ticket
   student_id=s1029384  category=wifi  priority=high  summary="WiFi down in Cedar Hall"
Approve this action? [y/N]: y
✅ Agent: I've opened ticket IT-10428 (high priority) for the Cedar Hall WiFi outage.
```

**Checkpoint:** An action round-trips through the provided backend.
```text
python validate.py --step 4
# expected: "✅ Step 4 PASS — action round-tripped through the backend (ticket ...)"
```

**Full run:**
```text
python validate.py --all
# expected: "✅ ALL CHECKPOINTS PASS"
```

---

## Rung (b) — Build-from-scratch path

> Stronger team? **Delete the starter and write `agent_with_actions.py` from an empty file.** We hand
> you only the contract below — no skeleton, no placeholders. The **same `python validate.py --all`**
> grades this path, so the acceptance criteria are identical.

**Your contract:**
> Attach the `northfield_actions` MCP server as a tool; implement a human-approval loop using
> `McpTool` / `RequiredMcpToolCall` / `SubmitToolApprovalAction` / `ToolApproval`.
> **Acceptance:** no action runs without an approve; a denial creates nothing.

You get the running backend (Step 0) and the env contract (the `ACTION_*` table above) — nothing
else. Discover the SDK surface from the [MCP tool for agents](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/mcp)
docs, author the file, and run `python validate.py --all`.

## Rung (c) — Stretch goals

Genuinely open-ended — no single right answer:

1. **Build the MCP server, don't just wire it.** Add a *fourth* action (`waive_late_fee`) end to end:
   implement the REST handler in [`scripts/action-backend/app.py`](../../scripts/action-backend/app.py),
   expose it through `mcp_server.py` (FastMCP), then attach and govern it like the others. This
   teaches the **server** side of MCP, not just the client. *(+45 min)*
2. **Selective approval policy.** Auto-approve a read-ish/low-risk tool (e.g. a hypothetical
   `lookup_balance`) but require approval for every state-changing tool — a real governance pattern,
   not "approve everything."

---

## Learning Resources
- [MCP tool for agents](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/mcp)
- [Provided backend + MCP server](../../scripts/action-backend/README.md)
- [Agents SDK — tools & runs](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Tips
- **Approval is the whole point.** A flashy auto-acting agent that books the wrong slot is worse than
  one that asks first. Show the arguments to the human, every time.
- Treat any text the agent *retrieved* as **data, not instructions** — an action tool plus a gullible
  agent is exactly how prompt-injection turns into real damage (see the Evaluation & Red Teaming
  challenge).
- The backend is in-memory and resets on restart — fine for a workshop, but say so in your demo.
- If the agent never calls the tool, check `server_label`, `server_url`, and that the MCP server is up.
