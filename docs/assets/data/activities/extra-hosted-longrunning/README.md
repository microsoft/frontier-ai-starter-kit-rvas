# Extra · Hosted Long-Running Agents

> **Command context:** Run the bootstrap command from the repository root.

This is an **optional extension** for work that must continue after the caller disconnects. Complete
[Deploy as a Hosted Agent](activity.html?id=advanced-deploy-hosted-agent) first. That activity is the
canonical hosted deployment path and owns container setup, identity, endpoint configuration, and
run history.

Use this activity only when a proven runtime need requires durable async execution, such as a
bounded batch job or reconciliation run. A slow interactive request is not enough reason to add it.

## Prerequisites

- A deployed hosted agent from [Deploy as a Hosted Agent](activity.html?id=advanced-deploy-hosted-agent).
- An authenticated remote endpoint for any worker tool. `localhost` does not resolve inside the
  hosted container.
- Project Application Insights. For trace correlation and evidence, use
  [Tracing & Observability](activity.html?id=advanced-tracing-observability).

## Step 1 — Adapt the deployed worker

Use the existing hosted-agent project as the worker. Do not repeat scaffolding or deployment here.
Choose one bounded job that can complete in a reasonable demo window and confirm its normal remote
request works before adding background behavior.

**Verify:** the deployed worker appears in the project and completes a representative remote request.

## Step 2 — Submit async work

Add a Responses request with `background=True`. The submission must return a response handle before
the work completes. Confirm the current submission and retrieval API through Microsoft Learn before
writing code.

**Verify:** the request returns a response ID immediately and the run continues after the submitting
client exits.

## Step 3 — Retrieve the result and its evidence

From a fresh process, retrieve or poll using only the response handle. Then use the correlation
method in [Tracing & Observability](activity.html?id=advanced-tracing-observability) to inspect the
background run and its duration.

**Verify:** a fresh client retrieves the completed result, and App Insights shows the same run.

## Outcome

You have an optional durable-execution path over the hosted agent. Hosted deployment remains in
[Deploy as a Hosted Agent](activity.html?id=advanced-deploy-hosted-agent); trace evidence remains in
[Tracing & Observability](activity.html?id=advanced-tracing-observability).
