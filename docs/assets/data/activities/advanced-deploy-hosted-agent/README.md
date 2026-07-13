# Advanced — Deploy as a Hosted Agent

> **Command context:** Unless a step explicitly changes directory, run commands from the repository root.

> ⏱ Guided ~60–90 min · 🛠 Build-from-scratch ~1.5 hr · ⭐⭐⭐⭐⭐ · Prereqs: Foundations end-state

> Tier 2 · Advanced — modular. You can attempt this in any order with the other Advanced
> activities. Prerequisite: the Foundations end-state (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

## Why this activity

So far your Northfield IQ Assistant lives inside your project as a prompt agent — you invoke it
from a notebook or script through the Responses API. That's perfect for building, but it isn't a thing
you can hand to the IT helpdesk or a student-portal team. They need a real endpoint: a URL with its
own identity, its own scaling, and its own run history, independent of your dev environment.

In this activity you ship the artifact. You containerize the assistant, deploy it as a hosted
Foundry agent with `azd ai agent`, give it a per-agent Entra (managed) identity, and invoke it
over its production Responses endpoint. Then you tie its live runs back to the observability you
built in the Tracing activity.

This is a genuine containerized deployment — not a "next steps" hand-wave. The same grounded assistant,
now running as its own service.

```text
   azure.yaml + src/<agent>/ + Dockerfile
                │
                ▼  azd deploy
   ┌──────────────────────────────────────────────┐
   │  container image ──▶ ACR ──▶ hosted agent     │
   │                        (per-agent identity)   │
   └───────────────────────┬──────────────────────┘
                           │  /protocols/openai/responses
                           ▼
                 invoke ──▶ run history + traces (App Insights)
```

> ⚠️ No Prompt Flow here. Earlier drafts of this activity deployed a Prompt Flow to a managed
> online endpoint. That path is removed. The artifact you ship is a hosted agent, deployed with
> `azd ai agent` against the Foundations agent definition — not a flow, and not a managed online
> endpoint.

## What you will need

- The Foundations `.env` (or bootstrap `.env`) with at least:
  - `AZURE_AI_PROJECT_ENDPOINT` — your Foundry project endpoint
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` — the chat model deployment the agent uses
  - `AZURE_FOUNDRY_AGENT_NAME` — the Northfield IQ Assistant agent name (e.g. `northfield-iq-assistant`)
- CLI tooling (in the devcontainer): `az`, `azd` (Azure Developer CLI), and `docker`. You can build
  the image without local Docker using ACR cloud build (shown in Step 2).
- Logged in: `az login` and `azd auth login`, with the subscription set to your event subscription.

> 💡 Recommended order: do Tracing & Observability before this activity. Step 4 here assumes you
> know how to read a run in the portal Tracing tab / App Insights.

---

This activity ships three rungs off the same backbone — the same `validate.py` grades all
three. (a) Guided path (below) prints the manifests to adapt · (b) Build-from-scratch path
gives you only the deploy contract + the gotcha list · (c) Stretch goals go open-ended.

## Rung (a) — Guided path

> The beginner on-ramp starts from the current official Agent Framework Responses sample, then
> adapts the generated `azure.yaml` and source. The real difficulty is the hosted runtime contract
> and asynchronous deployment, not reconstructing a deprecated manifest.

## Step 1 — Scaffold the unified hosted-agent project

**Goal:** Your repo holds a current hosted-agent project: one unified `azure.yaml`, agent source under
`src/<agent-name>/`, and a Dockerfile.

**Tasks:**

1. Install the current Foundry extension, create an empty activity-local project directory, and
   initialize the official basic Responses sample. In the wizard, select the **existing** Foundry
   project created in Foundations and its existing model deployment:

   ```bash
   azd ext install microsoft.foundry
   mkdir -p activities/advanced-deploy-hosted-agent/hosted
   cd activities/advanced-deploy-hosted-agent/hosted
   azd ai agent init \
     -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/azure.yaml \
     --deploy-mode code \
     --agent-name northfield-iq-assistant
   ```

2. Inspect the generated `azure.yaml`. The `azure.ai.agent` service is the deploy contract and must
   use `kind: hosted`, point `project:` at the generated source directory, and declare:

   ```yaml
   protocols:
     - protocol: responses
       version: 2.0.0
   ```

3. Adapt the generated source under `src/<agent-name>/` to use the Foundations persona and model
   deployment. Keep the generated Agent Framework Responses host, `requirements.txt`, and Dockerfile.
   The hosted runtime contract is: listen on port `8088`, expose `GET /readiness`, and serve the
   Responses protocol.
4. From the `hosted/` directory, run the generated project locally:

   ```bash
   azd ai agent run
   ```

**Success Criteria:**

- [ ] `hosted/azure.yaml` contains an `azure.ai.agent` service with `kind: hosted`.
- [ ] The service declares the `responses` protocol at version `2.0.0`.
- [ ] Its `project:` directory and configured entry point exist under `hosted/src/`.
- [ ] `azd ai agent run` starts the local agent and the inspector receives an answer.

**Checkpoint:**

```bash
python activities/advanced-deploy-hosted-agent/validate.py --step 1
# expected: "✅ Step 1 PASS — azure.yaml + hosted Responses service + source project present and valid"
```

> _Facilitator note: see solution.md._

---

## Step 2 — Provision and deploy with `azd`

**Goal:** The generated project is connected to Azure and deployed as a hosted agent with its own
version and per-agent managed identity.

**Tasks:**

1. From `activities/advanced-deploy-hosted-agent/hosted/`, provision or connect the resources
   declared by the generated `azure.yaml`:

   ```bash
   azd provision
   ```

2. Deploy the hosted agent. `azd deploy` builds the generated project and rolls out a hosted version:

   ```bash
   azd deploy
   ```

3. Invoke the deployed version through the CLI:

   ```bash
   azd ai agent invoke "Where is the registrar?"
   ```

> Hosted versions provision asynchronously. If invocation reports that the session is not ready,
> wait for deployment to become active and retry; `azd ai agent monitor --follow` shows live logs.

**Success Criteria:**

- [ ] `azd provision` completes against the intended Foundry project.
- [ ] `azd deploy` completes and reports the agent endpoint/playground.
- [ ] `azd ai agent invoke` returns an answer from the deployed agent.

**Checkpoint:**

```bash
python activities/advanced-deploy-hosted-agent/validate.py --step 2
# expected: "✅ Step 2 PASS — hosted agent deployed, version active in the project"
```

> _Facilitator note: see solution.md._

---

## Step 3 — Invoke the live endpoint and verify identity/auth

**Goal:** You call the hosted agent over its production Responses endpoint and confirm it runs under
its own Entra identity, not your user credentials.

**Tasks:**

1. Create a session, then invoke the deployed agent against its Responses endpoint. The route is
   `{AZURE_AI_PROJECT_ENDPOINT}/agents/{agentName}/endpoint/protocols/openai/responses`:

   ```python
   # invoke_hosted.py
   import os
   from openai import OpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider

   token_provider = get_bearer_token_provider(
       DefaultAzureCredential(), "https://ai.azure.com/.default"
   )
   agent = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant")
   base = os.environ["AZURE_AI_PROJECT_ENDPOINT"].rstrip("/")

   client = OpenAI(
       base_url=f"{base}/agents/{agent}/endpoint/protocols/openai",
       api_key=token_provider(),
   )

   resp = client.responses.create(input="How do I place a registration hold?")
   print(resp.output_text)
   ```

2. Verify authorization is enforced: confirm an unauthenticated call (no bearer token) is rejected
   with `401`/`403`. The endpoint requires the `Foundry User` (formerly `Azure AI User`) role — the agent's per-agent managed
   identity is what it uses to reach the model and knowledge base, not your token.
3. Inspect the agent's identity in the portal (agent → Identity) and note its principal id. This is
   the identity you'd grant data-plane roles to in production.

**Success Criteria:**

- [ ] An authenticated Responses call returns a grounded answer from the live endpoint.
- [ ] An unauthenticated call is rejected (`401`/`403`).
- [ ] You can name the agent's per-agent managed identity (principal id) from the portal.

Your run should look like this:
```text
$ python invoke_hosted.py
To place a registration hold, contact the Registrar's Office (registrar@northfield.edu) ...

$ curl -s -o /dev/null -w "%{http_code}" <endpoint>/responses   # no token
403
```

**Checkpoint:**

```bash
python activities/advanced-deploy-hosted-agent/invoke_hosted.py
python activities/advanced-deploy-hosted-agent/validate.py --step 3
# expected: "✅ Step 3 PASS — live endpoint answers authenticated calls, rejects anonymous"
```

> _Facilitator note: see solution.md._

---

## Step 4 — Tie monitoring back to Tracing & review run history

**Goal:** The hosted agent's production runs are observable — you can see run history on the agent and
the same OTel traces you learned to read in the Tracing activity.

**Tasks:**

1. Open the agent in the portal → Runs / Run history. Confirm your Step 3 invocation appears with
   status, latency, and token usage.
2. Open the Tracing tab and find the trace for the hosted run. Confirm it has the same span shape
   you saw locally (model + retrieval spans). The hosted agent inherits the project's App Insights, so
   the spans land in the same `dependencies`/`requests`/`traces` tables.
3. Run your `correlate.kql` from the Tracing activity (or the starter query below) against a hosted
   run's `operation_Id` to prove the production endpoint is fully traced:

   ```kusto
   dependencies
   | where timestamp > ago(30m)
   | where cloud_RoleName has "northfield-iq-assistant"
   | project timestamp, operation_Id, name, duration,
             total_tokens = toint(customDimensions["gen_ai.usage.total_tokens"])
   | order by timestamp desc
   ```

**Success Criteria:**

- [ ] The agent's run history shows your hosted invocation(s).
- [ ] A hosted run appears as a trace in App Insights / the Tracing tab.
- [ ] A KQL query scoped to the hosted agent returns its runs with token + latency.

**Checkpoint:**

```bash
python activities/advanced-deploy-hosted-agent/validate.py --step 4
# expected: "✅ Step 4 PASS — hosted run visible in run history and App Insights traces"
```

> _Facilitator note: see solution.md._

---

## Rung (b) — Build-from-scratch path

> Stronger team? Skip the sample implementation details. Start from `azd ai agent init` around your
> own code, then author the unified `azure.yaml`, Dockerfile, and entrypoint. The same `validate.py`
> grades this path.

Your contract:
> Containerize the Foundations agent, serve the `responses` protocol on 8088, deploy with
> `azd ai agent`, invoke over the production endpoint, and prove anonymous calls get 401/403.
> Acceptance: a live grounded answer and a rejected anonymous call.

The gotchas you get (everything else you design):
- Standalone `agent.yaml` / `agent.manifest.yaml` files are deprecated; use unified `azure.yaml`.
- The Responses declaration is `protocol: responses`, version `2.0.0`.
- A hosted version provisions asynchronously — gate on `status == active` before invoking.
- Look up the current MAF server-host class name via the `microsoft-docs` MCP — don't assume it.

---

## Done — what you shipped

- The Northfield IQ Assistant runs as a hosted Foundry agent with its own endpoint, version, and
  per-agent managed identity.
- It's invocable over the production Responses protocol, enforces auth, and every run is observable in
  run history and App Insights.

This unlocks Extras: MAF + Hosted Long-Running Agents (Extra D) and Build a UI (Extra E) both
target this live endpoint.

## Rung (c) — Stretch goals

Genuinely open-ended — no single right answer:

1. Blue/green a new version. Deploy a v2 with tweaked instructions, confirm both versions exist,
   then roll the active pointer — versioned hosted agents in practice. *(+30 min)*
2. Harden auth. Grant the per-agent managed identity the *minimum* data-plane roles to reach the
   KB, then prove a missing role yields a `403` — the security story most demos skip.

- Add a second `invocations` protocol to the same container for a custom request schema.
- Wire a CI step (GitHub Actions) that runs `azd deploy` and a remote smoke invocation on push.
- Grant the per-agent identity least-privilege data-plane roles and remove any local-auth fallback.

## Cleanup

After the event, remove the hosted version from the Foundry portal. Do **not** run `azd down` when
the hosted project is connected to the shared Foundations resource group: that command can delete
the Foundry project, model deployments, Search, ACR, and App Insights together.

## Learning resources

- [Hosted agents in Microsoft Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Deploy agents with `azd ai agent`](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Hosted-agent samples (foundry-samples)](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
- [Responses & Invocations protocols](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#protocols-responses-and-invocations)
- [ACR cloud build (`az acr build`)](https://learn.microsoft.com/azure/container-registry/container-registry-tutorial-quick-task)
