# Extra · MAF + Hosted Long-Running Agents

> **Command context:** Run the bootstrap command from the repository root.

> Tier 2 · Extra — modular. You can attempt this in any order with the other Extras.
> Prerequisite: the Foundations end-state (a deployed, grounded sample IQ assistant).
> Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> Specific prereqs (two): the Advanced · Deploy as a Hosted Agent activity (you reuse
> `azd ai agent` + ACR) and Extra C · Magentic Workflows (you deploy *that* workflow).

> ⚙️ Infra prerequisite (facilitator must pre-provision): ACR (Azure Container Registry) +
> hosted-agent endpoints + Application Insights — all already stood up by `azd up` from
> Foundations/Deploy. Confirm the deployed agent has platform-provided observability configuration
> rather than baking a connection string into the image. See [solution.md](solution.md).
>
> 🎤 Demo wow-factor: submit a job, close the tab, come back later to a completed
> long-running agent run with full trace history — async work that survives your session.

## Why this activity

Extra C's Magentic workflow runs in your terminal — close it and the work dies. Real student-services
work isn't always interactive: *batch-process the overnight enrollment queue*, *reconcile 500 waitlist
requests*, *re-grade a backlog*. Those are long-running jobs that shouldn't block a caller.

In this Extra you deploy the MAF workflow from Extra C as a hosted agent (its own endpoint +
identity, like the Deploy activity), then submit a Responses request with `background=True`. The
platform accepts the job, returns immediately with a response handle, and continues processing it.
You retrieve that response later — and every step is traced in App Insights.

```text
  submit job ──▶ hosted MAF workflow (Responses `background=True`)
                    │  returns response handle immediately
   close tab ✷      │  …keeps working async…
                    ▼
  poll handle ──▶ completed result + full trace in App Insights
```

---

## Step 1 — Containerize the Magentic workflow as a hosted agent

**Goal:** The Extra C workflow runs as a deployed hosted agent, not a local script.

**Tasks:**
1. Reuse the Deploy as a Hosted Agent pattern: scaffold a unified `azure.yaml` + source project that
   serves your Extra C Magentic workflow (manager + 4 specialists) over Responses or Invocations.
2. Test with `azd ai agent run`, then deploy with `azd deploy`.
   Search before you implement: confirm the current `azure.yaml` hosted-agent schema via the
   `foundry-hosted-agents` skill (`foundry-mcp` / `microsoft-docs`).
3. Invoke the deployed endpoint with the composite request from Extra C and confirm it still routes
   across specialists.

**Success Criteria:**
- [ ] The Magentic workflow answers over a deployed endpoint (not localhost).
- [ ] A composite request still fans to ≥2 specialists when invoked remotely.

**Checkpoint:** *Portal state* — the hosted agent shows in the project with a run in its history;
invoking the endpoint returns a multi-specialist answer.

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

**Checkpoint:** *Console/portal state* — the submit call returns a response id immediately; the run is shown
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

**Checkpoint:** *Portal state* — the completed run + its span tree appear in App Insights; your KQL lists
the spans.

---

## What you built

The Magentic workflow, now shipped as a hosted agent with a background Responses path that does async,
long-running work and survives your session — fully traced. This is what "production multi-agent" actually
looks like.
