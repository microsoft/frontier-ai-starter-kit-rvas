# Implementation notes — Hosted long-running agents

Use these notes when a scenario needs work that outlives a browser request. The pattern is general:
submit a background job, keep a platform handle, retrieve the result later, and trace the run.
Magentic Workflows are one useful example, not a required prerequisite.

## What this activity is really teaching

**Async, durable** agent work. Everything so far has been request/response in a live process. This Extra
introduces `background=True`: submit → get a handle → work continues → poll later. The keeper insight is
that a long-running agent **decouples** the caller's session from the work, and observability
(App Insights) is what makes async work *trustworthy* — you can prove what happened after the fact.

## Runtime prerequisites

All already created by `azd up` (Foundations/Deploy), but **verify**:
1. **ACR** exists and the team can push (or use ACR **cloud build** — no local Docker needed).
2. **Hosted-agent endpoints** enabled on the project (`azd ai agent` works — same as Deploy activity).
   Managed hosted agents are generally available; verify regional availability and the current `azd` surface.
3. **App Insights** wired. Hosted Agent Service provides observability configuration to the running
   container; do not bake a connection string into an image or source file.
4. Any tool backend reachable from the *hosted* environment — `localhost` won't resolve from a
   container. Use an authenticated remote endpoint, not an unauthenticated public tunnel.

## Search-Before-Implement

Hosted Agent Service is generally available, but the Python Agent Framework hosting integration may be
prerelease and its APIs can move. The Responses `background=True` submission/retrieval flow also evolves.
Send teams to `microsoft-docs` / `foundry-mcp` for current signatures rather than guessing.

## Implementation notes by step

### Step 1 — containerize the worker
- This is the Deploy activity applied to a long-running worker instead of a short request/response
  agent. If the worker uses MAF, include `agent-framework` in the container `requirements.txt`.
- **Pitfall:** tool URLs still pointing at localhost → hosted worker fails remotely. Fix the URL.

### Step 2 — background run
- The teaching beat: the submit call must **return immediately**. If they're blocking on completion, they
  haven't actually used the background path — they've just deployed a slow synchronous agent.
- A good batch task loops over a small list of items so it visibly outlives a request but completes
  quickly enough to inspect.

### Step 3 — poll + trace
- The "close the tab, come back" demo: have them submit in one terminal, kill it, then **poll from a fresh
  process** with only the run id. Retrieving the result proves durability.
- App Insights closes the loop: the background run's span tree is the evidence. Reuse the Tracing
  activity's KQL muscle — list spans by duration.

## Verification

The deliverables are a **deployed endpoint**, an **async run that outlives a process**, and **App Insights
traces** — all portal/live state, not statically checkable. Verify via: hosted agent in the project with
run history; an immediate-return submit; a fresh-process poll retrieving the result; spans in App Insights.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Workflow won't start in container | `agent-framework` missing from image | add to container `requirements.txt` |
| Action specialist fails when hosted | `ACTION_MCP_URL` = localhost | use an authenticated remote MCP endpoint |
| Submit blocks until done | not using the Responses background path | use `background=True` and retrieve the response later |
| No spans for background run | observability isn't configured for the hosted agent | verify the hosted-agent/App Insights deployment configuration |
| Can't retrieve result later | relying on in-memory state | retrieve the platform response handle, not local vars |
