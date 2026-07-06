---
title: "Long-Running Agents"
parent: Customer Build Track
nav_order: 72
description: Host a workflow and run scenario jobs asynchronously when work should survive the session.
---

# Customer Build · Long-Running Agents

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Long-Running Agents" artifact="A hosted background run for YOUR scenario that returns a handle, completes later, and is traceable." next="Use this only for jobs that should outlive a chat turn or browser session." %}

This deepener is mutuated from [Extra · MAF + Hosted Long-Running Agents](../challenges/extra-hosted-longrunning) — same hosted/background pattern, but applied to your scenario from [Define your outcome](../customer-outcome). This is an OPTIONAL deepener. Use it when your demo story includes durable async work, not for normal chat responses.

> Before you start this deepener: complete a hosted agent path, and complete Magentic Workflows if the thing you are hosting is a multi-agent workflow. If your action finishes inside one user turn, skip this.

---

## Step 1 — Containerize your workflow as a hosted agent

**Why it matters for your app:** hosting turns a local workflow into a deployed endpoint with identity, history, and a path toward production demos.

**Does this apply to you?** → Skip it if your build track demo stays local or only needs the existing hosted assistant.
- Build it if your scenario workflow must be invoked remotely by a UI, service, or scheduler.
- Adapt it if you are hosting a single agent or tool worker instead of a Magentic workflow.

**Decisions to make:**
- Which artifact from your build should become the hosted endpoint?
- Which environment values and managed identity permissions does it need?
- What request from your demo story proves the deployed endpoint still routes correctly?

**Apply it to your app:** package your scenario workflow with the hosted-agent pattern, then invoke it remotely with a real composite request. → [Extra · Long-Running Agents — Step 1](../challenges/extra-hosted-longrunning#step-1--containerize-the-magentic-workflow-as-a-hosted-agent)

**Prove you applied it:**
- □ Your workflow answers through a deployed endpoint, not localhost.
- □ The deployed run uses your scenario names, tools, and instructions.
- □ A remote invocation exercises the same routing or action path as local.

**Stuck?** [Northfield Step 1](../challenges/extra-hosted-longrunning#step-1--containerize-the-magentic-workflow-as-a-hosted-agent).

---

## Step 2 — Add a background run path

**Why it matters for your app:** long-running work should return a handle quickly and continue after the caller closes the tab or moves on.

**Does this apply to you?** → Skip it if every action should complete synchronously in front of the user.
- Build it if your action candidates include batch processing, reconciliation, report generation, or multi-record review.
- Adapt it if the background job is a scheduler-triggered process rather than user-submitted.

**Decisions to make:**
- What is your durable job: queue, report, audit, migration, or case review?
- What handle/status will your user need while it runs?
- Which safety boundary requires approval before the background work starts?

**Apply it to your app:** add a background submission path for one real long-running job and return a run handle immediately. → [Extra · Long-Running Agents — Step 2](../challenges/extra-hosted-longrunning#step-2--add-a-background-long-running-agent)

**Prove you applied it:**
- □ Submitting the job returns a handle without waiting for completion.
- □ The job continues after the submitting client is closed.
- □ The submitted payload is safe, scoped, and tied to your scenario.

**Stuck?** [Northfield Step 2](../challenges/extra-hosted-longrunning#step-2--add-a-background-long-running-agent).

---

## Step 3 — Poll for the result and read the trace

**Why it matters for your app:** async work is only useful if users can retrieve the result later and operators can inspect what happened.

**Does this apply to you?** → Skip it if you skipped background execution.
- Build it if your demo promises "come back later" behavior.
- Adapt it if notification or webhook delivery is a better fit than polling.

**Decisions to make:**
- What result summary will prove the job completed successfully?
- Which trace spans matter to your success measures: planning, retrieval, action, retry, or approval?
- What KQL or portal screenshot will your readout use?

**Apply it to your app:** retrieve the completed run from a fresh client and inspect the App Insights trace. → [Extra · Long-Running Agents — Step 3](../challenges/extra-hosted-longrunning#step-3--poll-for-the-result-and-read-the-trace)

**Prove you applied it:**
- □ A fresh process retrieves the result using only the run handle.
- □ App Insights shows spans for the background run.
- □ Your readout includes the duration or trace evidence for the job.

**Stuck?** [Northfield Step 3](../challenges/extra-hosted-longrunning#step-3--poll-for-the-result-and-read-the-trace).

---

## Deepener end-state

You have a hosted async path for work that should survive the session. Deepeners are optional; return to the [Customer Build Track](../customer-build) and keep only the ones that strengthen your outcome.
