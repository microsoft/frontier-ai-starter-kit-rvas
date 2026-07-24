---
title: "Ship It"
parent: Customer Build Track
nav_order: 50
description: Package your agent as a hosted endpoint with identity, auth, and observable runs — if your demo needs shipping.
---

# Customer Build · Ship it

> **Command context:** Run commands from the repository root unless a linked reference step explicitly says otherwise.

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Ship" artifact="A hosted endpoint for YOUR agent, or an explicit decision that local/UI demo is the right scope." next="Once the artifact is shippable, move to Grow it into a team." %}

This chapter adapts [Advanced · Deploy as a Hosted Agent](../activities/advanced-deploy-hosted-agent): it uses the same hosted-agent pattern and identity checks, but the hosted artifact is *your* scenario agent from [Define your outcome](../customer-outcome).

> Before you start this chapter: finish [Ground your app](foundations). [See inside it](advanced-tracing-observability) is strongly recommended so hosted runs are observable.

---

## Decision checkpoint — launch, harden, or remain demo-only

Hosting an endpoint is not the same as being ready for broad production use. Before making the
final recommendation, record these decisions in the [scenario record](../customer-outcome):

- Which environment is this: demo, controlled pilot, or production? What data and users are
  allowed in it?
- Which callers may invoke the endpoint, and which permissions does the agent itself need?
- Who approves a deployed change, who can roll it back, and what is the safe fallback if it fails?
- Who supports the service, which signal tells them it is unhealthy, and what known hardening work
  remains?

**Decision:** choose one outcome explicitly: **launch a controlled pilot**, **harden first**, or
**remain demo-only**. A hosted endpoint with managed identity is valuable evidence, but it does not
replace the ownership, access, support, and change decisions above.

---

## Step 1 — Package the hosted agent project

**Why it matters for your app:** a hosted agent is a real artifact: manifest, container entrypoint, Dockerfile, endpoint protocol, and instructions under source control.

**Does this apply to you?**
- Build it if a stakeholder app, integration, or API client must call your agent.
- Adapt it if your demo is a UI calling the project agent directly — package only the parts you need and record the gap.
- Skip it if a local script/notebook is the intended session deliverable.

**Decisions to make:**
- What hosted agent name matches your scenario?
- Which persona/guardrails from your grounded agent move into the manifest?
- Which model deployment and tools are required at runtime?
- What data must the container never bake in: secrets, `.env`, customer documents?

**Apply it to your app:** adapt the manifest, entrypoint, and Dockerfile to your agent name and instructions. → [Deploy — Step 1](../activities/advanced-deploy-hosted-agent#step-1--author-agentyaml-and-the-container-entrypoint)

**Prove you applied it:**
- `python activities/advanced-deploy-hosted-agent/validate.py --track customer --step 1 --dry-run`
- Checklist:
  - [ ] hosted manifest uses your agent name
  - [ ] instructions are your scenario instructions
  - [ ] responses protocol is declared
  - [ ] Dockerfile exposes the expected port
  - [ ] no secrets are copied.

**Stuck?** [Northfield Step 1](../activities/advanced-deploy-hosted-agent#step-1--author-agentyaml-and-the-container-entrypoint).

---

## Step 2 — Deploy a hosted version

**Why it matters for your app:** deployment proves the artifact can leave your dev environment and run with a version, image, and managed identity.

**Does this apply to you?**
- Build it if endpoint delivery is part of your value proposition.
- Adapt it if cloud build or quota blocks you — show the manifest and local container, then mark hosted deploy as backlog.
- Skip it if the demo is intentionally local or embedded in another app.

**Decisions to make:**
- What unique image tag identifies this demo build?
- Which subscription/resource group owns the hosted artifact?
- Who has permission to deploy and roll back?
- What status proves the hosted version is active?

**Apply it to your app:** use the hosted-agent deployment flow after confirming current commands in the reference. → [Deploy — Step 2](../activities/advanced-deploy-hosted-agent#step-2--containerize-and-deploy-with-azd-ai-agent)

**Prove you applied it:**
- `python activities/advanced-deploy-hosted-agent/validate.py --track customer --step 2 --dry-run`
- Checklist:
  - [ ] image tag is unique
  - [ ] hosted version is active or deployment gap is documented
  - [ ] per-agent identity exists
  - [ ] rollback/cleanup path is known.

**Stuck?** [Northfield Step 2](../activities/advanced-deploy-hosted-agent#step-2--containerize-and-deploy-with-azd-ai-agent).

---

## Step 3 — Invoke the endpoint and verify auth

**Why it matters for your app:** a shipped endpoint must answer authenticated callers and reject anonymous ones.

**Does this apply to you?**
- Build it if you deployed a hosted agent.
- Adapt it if another app layer calls the agent — verify auth at that layer and note how it maps to the agent.
- Skip it if Step 2 was skipped.

**Decisions to make:**
- Who is the intended caller: UI backend, integration, test script, or another agent?
- What role assignment is needed for invocation?
- What prompt proves the endpoint is your scenario, not the Northfield default?
- What is the expected unauthenticated response?

**Apply it to your app:** invoke the production Responses endpoint with a token and test anonymous rejection. → [Deploy — Step 3](../activities/advanced-deploy-hosted-agent#step-3--invoke-the-live-endpoint-and-verify-identityauth)

**Prove you applied it:**
- `python activities/advanced-deploy-hosted-agent/validate.py --track customer --step 3 --dry-run`
- Checklist:
  - [ ] authenticated call returns a scenario answer
  - [ ] anonymous call is rejected
  - [ ] per-agent identity is named
  - [ ] no API key is required for local dev unless documented.

**Stuck?** [Northfield Step 3](../activities/advanced-deploy-hosted-agent#step-3--invoke-the-live-endpoint-and-verify-identityauth).

---

## Step 4 — Observe hosted runs (chapter end-state)

**Why it matters for your app:** production readiness includes run history and traces. If a stakeholder reports a bad answer, you need to find the run.

**Does this apply to you?**
- Build it if the agent is hosted.
- Adapt it if you only have local tracing — show the same operation-id pattern and mark hosted observability as backlog.
- Skip it if deployment was intentionally skipped.

**Decisions to make:**
- Which hosted run is your canonical demo evidence?
- What run-history fields matter to the stakeholder: latency, status, token usage, caller, outcome?
- Which KQL query from your tracing confirms hosted telemetry?
- What alert or dashboard would be next for pilot?

**Apply it to your app:** tie one hosted invocation back to run history and App Insights. → [Deploy — Step 4](../activities/advanced-deploy-hosted-agent#step-4--tie-monitoring-back-to-tracing--review-run-history)

**Prove you applied it:**
- `python activities/advanced-deploy-hosted-agent/validate.py --track customer --all --dry-run`
- Checklist:
  - [ ] hosted invocation appears in run history
  - [ ] trace is visible or gap recorded
  - [ ] operation id is captured
  - [ ] cleanup plan is clear.

**Stuck?** [Northfield Step 4](../activities/advanced-deploy-hosted-agent#step-4--tie-monitoring-back-to-tracing--review-run-history).

---

## Chapter end-state

You either have a hosted, authenticated, observable endpoint for your scenario agent, or a clear scope decision that the session demo remains local/UI-only.

```bash
python activities/advanced-deploy-hosted-agent/validate.py --track customer --all --dry-run
```

Next: [Grow it into a team](capstone-multi-agent).
