# Implementation notes — Advanced Deploy as a Hosted Agent

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

These notes capture the reusable hosted-agent deployment mechanics: project shape, container build,
authenticated invocation, managed identity, and run history.

> ⚠️ **This activity was rewritten away from Prompt Flow.** The old version deployed a Prompt Flow to
> a managed online endpoint and bolted on a Flask app. **All of that is gone.** If a team is following
> an old printout that mentions "package the Prompt Flow", "managed online endpoint", or a Flask UI,
> stop them — that content is deprecated. The artifact here is a **hosted Foundry agent** deployed with
> `azd ai agent`. (A Flask/Streamlit UI is now its own Extra — *Build a UI* — that targets this
> endpoint.)

## What this activity proves

A team finishes when the sample IQ assistant runs as a **hosted, containerized agent** with its own
endpoint, its own version, and a **per-agent managed identity**, and they can invoke it over the
production Responses protocol with auth enforced and runs visible in App Insights. This is the "ship
it" activity — real container deployment, not the "next steps only" hand-wave the reference labs stop at.

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
  release) implements the Responses contract for them. Teams that try to hand-roll a Flask `/responses`
  route can do it, but it's a time sink — steer them to the framework host. Reference:
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

- Hosted agents inherit the **project's** App Insights, so the spans land in the **same** tables the
  team queried in the Tracing activity. The only new dimension is `cloud_RoleName`, which carries the
  agent/container name — that's how they scope KQL to hosted runs.
- If a team skipped the Tracing activity, they can still pass Step 4 via the portal **Run history** +
  **Tracing** tab; the `correlate.kql` reuse is the richer path but not required.

## Cleanup discipline

Remove the hosted version from the portal after the event. Do not run `azd down` against a project
connected to the shared Foundations resource group, because it can delete the whole workshop footprint.

## Verification

`python activities/advanced-deploy-hosted-agent/validate.py --step 4` passes; the agent has an `active` hosted version; an authenticated Responses call
returns a grounded answer; an anonymous call is rejected; and the team can point to the run in both run
history and App Insights. No Prompt Flow, no managed online endpoint anywhere in their solution.
