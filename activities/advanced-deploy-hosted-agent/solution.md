# Implementation notes — Advanced Deploy as a Hosted Agent

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

Use these notes for the canonical hosted-agent deployment path: project shape, container build,
authenticated invocation, managed identity, and run history. For async work after deployment, use
[Hosted Long-Running Agents](../extra-hosted-longrunning/README.md).

> ⚠️ **This activity was rewritten away from Prompt Flow.** The old version deployed a Prompt Flow to
> a managed online endpoint and bolted on a Flask app. **All of that is gone.** If a team is following
> an old printout that mentions "package the Prompt Flow", "managed online endpoint", or a Flask UI,
> stop them — that content is deprecated. The artifact here is a **hosted Foundry agent** deployed with
> `azd ai agent`. (A Flask/Streamlit UI is now its own Extra — *Build a UI* — that targets this
> endpoint.)

## What this activity proves

A team finishes when the sample IQ assistant runs as a **hosted, containerized agent** with its own
endpoint, version, and **per-agent managed identity**. They must invoke it over the production
Responses protocol with authentication enforced and inspect runs in App Insights.

Assumes the Foundations end-state (or bootstrap). If the agent isn't grounded locally, that's a
Foundations problem first.

## The deployment pipeline at a glance

Unified `azure.yaml` + `src/<agent>/` → `azd ai agent run` → `azd deploy` → hosted version
provisions + per-agent identity → invoke Responses endpoint → run history + traces. The most common
mistake is treating a successful `azd deploy`
exit code as "done" — the version provisions **asynchronously**, so Step 2's checkpoint waits for
`status == active`.

## Implementation notes by step

### Step 1 — unified azure.yaml + entrypoint

- **Protocol and port are required.** Hosted agents must listen on `0.0.0.0:8088` and declare the
  `responses` protocol (v `2.0.0`) in the `azure.ai.agent` service in `azure.yaml`. A container that binds `127.0.0.1` or a different
  port will deploy but never become healthy.
- **Reuse the Foundations persona.** The `instructions:` block should be the same grounded,
  cite-your-sources persona from Foundations Step 3 — don't let teams rewrite it here.
- **The MAF server host** (`AzureAIAgentServerHost` or the equivalent in the current `agent-framework`
  release) implements the Responses contract. Use the framework host instead of hand-writing a Flask
  `/responses` route. Reference:
  `foundry-samples/samples/python/hosted-agents/agent-framework/responses/`.
- **Local smoke test** before deployment: run `azd ai agent run` from `hosted/` and use the opened
  agent inspector. If the generated project fails locally, fix it before `azd deploy`.

### Step 2 — Containerize + deploy

- **Use the generated project flow.** `azd provision` connects/provisions the services declared in
  `azure.yaml`; `azd deploy` builds and deploys the hosted agent. The old
  `azd ai agent create/deploy` commands and standalone `agent.yaml` are deprecated.
- **ACR pull permission:** the Foundry project managed identity needs repository-scoped pull on the ACR
  (Foundry hosted agents use ABAC mode — `Container Registry Repository Reader`, **not** registry-level
  `AcrPull`). `azd ai agent` usually wires this; if the version fails to pull, this is why.
- **`active` is the gate.** `az ai agent show --query "version,status"`; provisioning can take a couple
  of minutes. Don't let teams move to Step 3 on a `provisioning` version — invokes will return
  `424 FailedDependency` / `session_not_ready`.

### Step 3 — Invoke + identity

- **Two identities, keep them straight:** (1) the **caller** (the student's `DefaultAzureCredential`
  bearer token) authenticates *into* the endpoint; (2) the **per-agent managed identity** is what the
  *agent* uses to reach the model and knowledge base. The teaching point is that the agent no longer
  rides on the student's credentials.
- **Required role:** the caller needs `Foundry User` (formerly `Azure AI User`) on the project to invoke. A `403` on an
  authenticated call is almost always a missing role assignment, not bad code.
- **Auth-enforced check:** an anonymous call (no `Authorization` header) must return `401`/`403`. If it
  returns `200`, something is misconfigured — escalate, don't ship.
- **Responses route:** `{endpoint}/agents/{agentName}/endpoint/protocols/openai/responses`. Teams often
  fat-finger this path; have them print `base_url` before debugging deeper.

### Step 4 — Monitoring back to Tracing

- Hosted agents inherit the **project's** App Insights. Use the canonical
  [Tracing & Observability](../advanced-tracing-observability/README.md) correlation record rather
  than creating a second evidence method here.
- Scope that activity's KQL to `cloud_RoleName`, which contains the agent/container name. Portal run
  history remains the fast way to find the hosted invocation.

## Cleanup discipline

Remove the hosted version from the portal after the event. Do not run `azd down` against a project
connected to the shared Foundations resource group, because it can delete the whole workshop footprint.

## Verification

`python activities/advanced-deploy-hosted-agent/validate.py --step 4` passes; the agent has an `active` hosted version; an authenticated Responses call
returns a grounded answer; an anonymous call is rejected; and the team can point to the run in both run
history and App Insights. No Prompt Flow, no managed online endpoint anywhere in their solution.
