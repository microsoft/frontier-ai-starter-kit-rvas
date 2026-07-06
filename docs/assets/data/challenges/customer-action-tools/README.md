
# Customer Build · Make it act



This chapter is mutuated from [Advanced · Action Tools](challenge.html?id=advanced-action-tools) — same approval-loop pattern, same checkpoints — but the action belongs to *your* scenario from [Define your outcome](challenge.html?id=customer-outcome). Use this page to decide what your agent may change; use the linked Northfield steps for exact mechanics.

> Before you start this chapter: you need a grounded agent from [Ground your app](challenge.html?id=customer-foundations) and at least one action candidate from your scenario pack.

---

## Step 0 — Stand up the action surface

**Why it matters for your app:** an action tool needs a real surface to call. Even a demo action should create, update, schedule, submit, or notify somewhere visible.

**Does this apply to you?**
- Build it if your demo promise includes a workflow change, ticket, booking, status update, or handoff.
- Adapt it if your real system is unavailable — use a safe mock API that preserves the same request/response shape.
- Skip it only if your app is knowledge-only; then move straight to [Prove it's safe](challenge.html?id=customer-evaluation-redteam).

**Decisions to make:**
- Which *action candidate* is valuable enough to demo?
- What is the safe backend for the hackathon: real dev API, mock service, provided Action Tools backend, or manual queue?
- What non-secret auth/header contract will the agent use?

**Apply it to your app:** start from the provided REST backend pattern, then substitute your endpoint only if you own the side effect and can reset it. → [Action Tools — Step 0](challenge.html?id=advanced-action-tools#step-0--start-the-provided-backend)

**Prove you applied it:**
- `python challenges/advanced-action-tools/validate.py --track customer --step 1 --dry-run`
- Checklist: □ action endpoint or mock is reachable □ no production data is mutated □ every required env var uses `.env.sample` names (`ACTION_API_URL`, `ACTION_MCP_URL`, `ACTION_API_KEY`).

**Stuck?** [Northfield Step 0](challenge.html?id=advanced-action-tools#step-0--start-the-provided-backend).

---

## Step 1 — Decide what must be governed

**Why it matters for your app:** knowledge tools read; action tools change the world. Your safety boundary starts by naming the side effect and who pays for a mistake.

**Does this apply to you?**
- Build it for any action that writes data, sends messages, changes access, spends money, books time, opens cases, or triggers people.
- Adapt it for read-only API calls that expose sensitive data — approval may become consent or audit logging instead.
- Skip it only for fully public, read-only lookups with no sensitive data.

**Decisions to make:**
- What is the side effect?
- Who is affected if it fires incorrectly?
- Is the approval policy always-approve-by-human, conditional, or deny-by-default for some inputs?
- What must be shown to the human before approval: user, record id, amount, date, rationale, source citation?

**Apply it to your app:** write your approval policy before coding the tool. Use the Northfield comparison to separate knowledge from action. → [Action Tools — Step 1](challenge.html?id=advanced-action-tools#step-1--knowledge-tools-vs-action-tools)

**Prove you applied it:**
- `python challenges/advanced-action-tools/validate.py --track customer --step 2 --dry-run`
- Checklist: □ each action has a named side effect □ approval criteria are written □ denial behavior is defined □ unsafe/out-of-scope requests route to refusal or escalation.

**Stuck?** [Northfield Step 1](challenge.html?id=advanced-action-tools#step-1--knowledge-tools-vs-action-tools).

---

## Step 2 — Define your action tools

**Why it matters for your app:** the tool schema is the contract between natural language and your system. Ambiguous parameters create bad actions.

**Does this apply to you?**
- Build it if you have one or more approved side effects.
- Adapt it if your action is currently manual — define a tool that creates a review record or draft request instead of executing directly.
- Skip it if actions are out of scope for your demo.

**Decisions to make:**
- What is the smallest useful action for the demo story?
- Which parameters are required, typed, and human-readable?
- Which values must come from grounded context vs. user input vs. human approver?
- What does success return so the agent can cite a ticket id, booking id, or handoff id?

**Apply it to your app:** wrap your backend call as a `FunctionTool` and keep the tool docstring specific to your domain. → [Action Tools — Step 2](challenge.html?id=advanced-action-tools#step-2--define-the-action-tools)

**Prove you applied it:**
- `python challenges/advanced-action-tools/validate.py --track customer --step 2 --dry-run`
- Checklist: □ tool names match your business action □ parameters are not Northfield-specific unless your scenario is Northfield □ tool uses `ACTION_API_URL` or a documented equivalent □ no placeholders remain.

**Stuck?** [Northfield Step 2](challenge.html?id=advanced-action-tools#step-2--define-the-action-tools).

---

## Step 3 — Implement the approval loop

**Why it matters for your app:** a governed agent pauses, shows the proposed action, and records approve/deny before anything mutates.

**Does this apply to you?**
- Build it for any real or realistic side effect.
- Adapt it if your demo uses a mock backend — still require approval so the production pattern is visible.
- Skip it only when all tools are read-only and non-sensitive.

**Decisions to make:**
- Who approves in the demo: user, operator, coach, or simulated approver?
- What arguments are shown exactly as the human sees them?
- What audit artifact proves approval happened?
- What message does the agent return when approval is denied?

**Apply it to your app:** reuse the `RequiredFunctionToolCall` → approve/deny → `ToolOutput` loop, substituting your action functions. → [Action Tools — Step 3](challenge.html?id=advanced-action-tools#step-3--implement-the-tool-approval-loop)

**Prove you applied it:**
- `python challenges/advanced-action-tools/validate.py --track customer --step 3 --dry-run`
- Checklist: □ action cannot execute before approval □ denial performs no side effect □ approval arguments are visible □ logs or records show the decision.

**Stuck?** [Northfield Step 3](challenge.html?id=advanced-action-tools#step-3--implement-the-tool-approval-loop).

---

## Step 4 — Prove the action end-to-end (chapter end-state)

**Why it matters for your app:** stakeholders need to see the full loop: user asks, agent proposes, human approves, system changes, agent reports the result.

**Does this apply to you?**
- Build it if action is part of your value proposition.
- Adapt it if only a draft or queue item is safe during the hackathon.
- Skip it if the demo remains knowledge-only; document this as a deliberate scope decision.

**Decisions to make:**
- What one scenario request proves the action is useful?
- What visible system record proves it happened?
- What negative test proves denial or invalid input is safe?
- How will you reset demo state between runs?

**Apply it to your app:** run the same end-to-end pattern, but verify your own side effect and denial path. → [Action Tools — Step 4](challenge.html?id=advanced-action-tools#step-4--test-an-end-to-end-action)

**Prove you applied it:**
- `python challenges/advanced-action-tools/validate.py --track customer --all --dry-run`
- Checklist: □ approved request creates/updates the expected record □ denied request creates nothing □ result id is shown to the user □ action is included in your demo story.

**Stuck?** [Northfield Step 4](challenge.html?id=advanced-action-tools#step-4--test-an-end-to-end-action).

---

## Chapter end-state

You have one governed workflow action attached to your grounded agent, with approval and denial both proven.

```bash
python challenges/advanced-action-tools/validate.py --track customer --all --dry-run
```

Next: [Prove it's safe](challenge.html?id=customer-evaluation-redteam).
