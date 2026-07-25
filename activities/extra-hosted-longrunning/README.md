# Extra · MAF + Hosted Long-Running Agents

> **Command context:** Run the bootstrap command from the repository root.

> Reusable long-running module. Use it when a scenario needs work that outlives an interactive
> request. Prerequisite: a deployed scenario agent or hosted worker.
> Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> Specific prereq: the Advanced · Deploy as a Hosted Agent activity or equivalent hosted-agent
> deployment path. Magentic Workflows are one possible worker shape, not a requirement.

> Infra prerequisite: ACR (Azure Container Registry) +
> hosted-agent endpoints + Application Insights — all already stood up by `azd up` from
> Foundations/Deploy. Confirm the deployed agent has platform-provided observability configuration
> rather than baking a connection string into the image. See [solution.md](solution.md).
>
> 🎤 Demo wow-factor: submit a job, close the tab, come back later to a completed
> long-running agent run with full trace history — async work that survives your session.

## Why this activity

Interactive workflows often run in your terminal — close it and the work dies. Real customer work
is not always interactive: *batch-process a queue*, *reconcile many requests*, or *review a backlog*.
Those are long-running jobs that should not block a caller.

In this Extra you deploy a worker as a hosted agent (its own endpoint + identity, like the Deploy
activity), then submit a Responses request with `background=True`. The
platform accepts the job, returns immediately with a response handle, and continues processing it.
You retrieve that response later — and every step is traced in App Insights.

```text
  submit job ──▶ hosted worker (Responses `background=True`)
                    │  returns response handle immediately
   close tab ✷      │  …keeps working async…
                    ▼
  poll handle ──▶ completed result + full trace in App Insights
```

---

## Step 1 — Containerize the worker as a hosted agent

**Goal:** The long-running worker runs as a deployed hosted agent, not a local script.

**Tasks:**
1. Reuse the Deploy as a Hosted Agent pattern: scaffold a unified `azure.yaml` + source project that
   serves your worker over Responses or Invocations.
2. Test with `azd ai agent run`, then deploy with `azd deploy`.
   Search before you implement: confirm the current `azure.yaml` hosted-agent schema via the
   `foundry-hosted-agents` skill (`foundry-mcp` / `microsoft-docs`).
3. Invoke the deployed endpoint with a representative batch request and confirm it still does the
   intended work.

**Success Criteria:**
- [ ] The worker answers over a deployed endpoint (not localhost).
- [ ] A representative request still runs correctly when invoked remotely.

**Verify:** *Portal state* — the hosted agent shows in the project with a run in its history; invoking
the endpoint returns the expected worker result.

---

## Step 2 — Add a background (long-running) agent

**Goal:** A Responses request submitted with `background=True` returns immediately and finishes async.

**Tasks:**
1. Add a background Responses path (`background=True`) for a batch task, e.g.
   *"process the overnight enrollment queue"* (loop the Action sub-agent over a list).
2. Submit the job and confirm the call returns a response handle right away (non-blocking) instead of
   waiting for completion.
3. Search before you implement: confirm the current background-run API (submit + poll/retrieve) via
   `microsoft-docs`.

**Success Criteria:**
- [ ] Submitting the job returns a response handle without blocking on completion.
- [ ] The run continues after the submitting process/tab is gone.

**Verify:** *Console/portal state* — the submit call returns a response id immediately; the run is shown
`in_progress` in the portal while your client is idle/closed.

---

## Step 3 — Poll for the result and read the trace

**Goal:** Retrieve a completed background result and inspect its end-to-end trace.

**Tasks:**
1. In a fresh process (simulate "come back later"), retrieve/poll the response handle until it reports completed,
   then read the result.
2. Open Application Insights (configured by the hosted-agent deployment) and find
   the background run's spans — manager planning, each specialist, each action.
3. Write a one-line KQL to list the background run's spans by duration (reuse what you learned in the
   Tracing activity).

**Success Criteria:**
- [ ] A fresh client retrieves the completed result using only the response handle.
- [ ] The background run's spans are visible in App Insights and your KQL returns them.

**Verify:** *Portal state* — the completed run + its span tree appear in App Insights; your KQL lists
the spans.

---

## What you built

A hosted worker with a background Responses path that does async, long-running work and survives your
session — fully traced. If the worker is multi-agent, the same pattern makes the orchestration
observable after the caller disconnects.
