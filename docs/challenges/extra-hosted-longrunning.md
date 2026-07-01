---
title: "Extra: Hosted Long-Running Agents"
parent: Challenge Library
nav_order: 23
---

# Extra · MAF + Hosted Long-Running Agents

{% include challenge-prereq.html %}
>
> **Specific prereqs (two):** the **Advanced · Deploy as a Hosted Agent** challenge (you reuse
> `azd ai agent` + ACR) **and** **Extra C · Magentic Workflows** (you deploy *that* workflow).

> ⚙️ **Infra prerequisite (coach must pre-provision):** **ACR** (Azure Container Registry) +
> **hosted-agent endpoints** + **Application Insights** — all already stood up by `azd up` from
> Foundations/Deploy. You also need `APPLICATIONINSIGHTS_CONNECTION_STRING` set so background runs are
> traceable. See [solution.md](extra-hosted-longrunning-coach).
>
> 🎤 **Demo wow-factor:** submit a job, **close the tab**, come back later to a **completed**
> long-running agent run with full trace history — async work that survives your session.

## Why this challenge

Extra C's Magentic workflow runs **in your terminal** — close it and the work dies. Real student-services
work isn't always interactive: *batch-process the overnight enrollment queue*, *reconcile 500 waitlist
requests*, *re-grade a backlog*. Those are **long-running** jobs that shouldn't block a caller.

In this Extra you **deploy** the MAF workflow from Extra C as **hosted agents** (its own endpoint +
identity, like the Deploy challenge), and add a **background agent** (`background=True`) that accepts a
job, returns immediately with a handle, and keeps working **async**. You poll the handle later for the
result — and every step is traced in App Insights.

```text
  submit job ──▶ hosted MAF workflow (background=True)
                    │  returns run handle immediately
   close tab ✷      │  …keeps working async…
                    ▼
  poll handle ──▶ completed result + full trace in App Insights

```

---

## Step 1 — Containerize the Magentic workflow as a hosted agent

**Goal:** The Extra C workflow runs as a deployed hosted agent, not a local script.

**Tasks:**

1. Reuse the **Deploy as a Hosted Agent** pattern: author an `agent.yaml` + Dockerfile that serve your
   Extra C Magentic workflow (manager + 4 specialists) over the Responses/Invocations protocol.

2. Build + push to **ACR** and deploy with `azd ai agent` (ACR cloud build works without local Docker).
   **Search before you implement:** confirm the *current* `azd ai agent` + `agent.yaml` schema via the
   **`foundry-hosted-agents`** skill (`foundry-mcp` / `microsoft-docs`).

3. Invoke the deployed endpoint with the composite request from Extra C and confirm it still routes
   across specialists.

**Success Criteria:**

- [ ] The Magentic workflow answers over a **deployed endpoint** (not localhost).
- [ ] A composite request still fans to ≥2 specialists when invoked remotely.

**Checkpoint:** *Portal state* — the hosted agent shows in the project with a run in its history;
invoking the endpoint returns a multi-specialist answer.

---

## Step 2 — Add a background (long-running) agent

**Goal:** A job submitted with `background=True` returns immediately and finishes async.

**Tasks:**

1. Add a **background agent** / background run path (`background=True`) for a batch task, e.g.
   *"process the overnight enrollment queue"* (loop the Action sub-agent over a list).

2. Submit the job and confirm the call **returns a run handle right away** (non-blocking) instead of
   waiting for completion.

3. **Search before you implement:** confirm the current background-run API (submit + poll/retrieve) via
   `microsoft-docs`.

**Success Criteria:**

- [ ] Submitting the job returns a handle **without** blocking on completion.
- [ ] The run continues after the submitting process/tab is gone.

**Checkpoint:** *Console/portal state* — the submit call returns a run id immediately; the run is shown
`in_progress` in the portal while your client is idle/closed.

---

## Step 3 — Poll for the result and read the trace

**Goal:** Retrieve a completed background result and inspect its end-to-end trace.

**Tasks:**

1. In a **fresh** process (simulate "come back later"), poll the run handle until it reports completed,
   then read the result.

2. Open **Application Insights** (the run is traced via `APPLICATIONINSIGHTS_CONNECTION_STRING`) and find
   the background run's spans — manager planning, each specialist, each action.

3. Write a one-line **KQL** to list the background run's spans by duration (reuse what you learned in the
   Tracing challenge).

**Success Criteria:**

- [ ] A fresh client retrieves the completed result using only the run handle.
- [ ] The background run's spans are visible in App Insights and your KQL returns them.

**Checkpoint:** *Portal state* — the completed run + its span tree appear in App Insights; your KQL lists
the spans.

---

## What you built

The Magentic workflow, now **shipped** as hosted agents with a **background** path that does async,
long-running work and survives your session — fully traced. This is what "production multi-agent" actually
looks like.
