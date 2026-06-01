---
title: "Advanced: Deploy as a Hosted Agent"
parent: Challenges
nav_order: 13
---

# Advanced — Deploy as a Hosted Agent

> **Tier 2 · Advanced — modular.** You can attempt this in any order with the other Advanced
> challenges. **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

## Why this challenge

So far your Northfield IQ Assistant lives inside your project as a **prompt agent** — you invoke it
from a notebook or script through the Responses API. That's perfect for building, but it isn't a thing
you can hand to the IT helpdesk or a student-portal team. They need a **real endpoint**: a URL with its
own identity, its own scaling, and its own run history, independent of your dev environment.

In this challenge you **ship the artifact**. You containerize the assistant, deploy it as a **hosted
Foundry agent** with `azd ai agent`, give it a **per-agent Entra (managed) identity**, and invoke it
over its production **Responses** endpoint. Then you tie its live runs back to the observability you
built in the Tracing challenge.

This is a genuine containerized deployment — not a "next steps" hand-wave. The same grounded assistant,
now running as its own service.

```text
   agent.yaml + Dockerfile + app code
                |
                v  azd ai agent create/deploy
   container image --> ACR --> hosted agent (per-agent identity)
                                        |
                                        | /protocols/openai/responses
                                        v
                          invoke --> run history + traces (App Insights)

```

> ⚠️ **No Prompt Flow here.** Earlier drafts of this challenge deployed a Prompt Flow to a managed
> online endpoint. That path is **removed**. The artifact you ship is a **hosted agent**, deployed with
> `azd ai agent` against the Foundations agent definition — not a flow, and not a managed online
> endpoint.

## What you will need

- The Foundations `.env` (or bootstrap `.env`) with at least:
  - `AZURE_AI_PROJECT_ENDPOINT` — your Foundry project endpoint
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` — the chat model deployment the agent uses
  - `AZURE_FOUNDRY_AGENT_NAME` — the Northfield IQ Assistant agent name (e.g. `northfield-iq-assistant`)
- CLI tooling (in the devcontainer): `az`, **`azd`** (Azure Developer CLI), and `docker`. You can build
  the image **without local Docker** using ACR cloud build (shown in Step 2).

- Logged in: `az login` and `azd auth login`, with the subscription set to your event subscription.

> 💡 Recommended order: do **Tracing & Observability** before this challenge. Step 4 here assumes you
> know how to read a run in the portal Tracing tab / App Insights.

---

## Step 1 — Author `agent.yaml` and the container entrypoint

**Goal:** Your repo holds a self-contained hosted-agent project: an `agent.yaml` manifest, the app code
that serves the Responses protocol, and a Dockerfile.

**Tasks:**

1. Create the folder `challenges/advanced-deploy-hosted-agent/hosted/` and add an **`agent.yaml`**
   that declares the agent name, the model deployment, the system instructions (reuse your Foundations
   persona/guardrails), and the **`responses`** protocol on port `8088`.

2. Add `main.py` that hosts the agent and serves `POST /responses` on `8088`. The simplest path is the
   Microsoft Agent Framework hosted-agent server, which speaks the Responses protocol for you.

3. Add a `Dockerfile` (slim Python base, `linux/amd64`, expose `8088`) and a `requirements.txt` for the
   container (`agent-framework`, `azure-ai-projects`, `azure-identity`).

```yaml
# hosted/agent.yaml
name: northfield-iq-assistant
description: Northfield University student-services IQ Assistant (grounded, hosted).
model:
  deployment: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
instructions: |
  You are the Northfield University Student Services Assistant. Answer only from the
  Northfield knowledge base and always cite your sources. If the answer is not in the
  knowledge base, say so and point the student to the relevant office. Never invent
  deadlines, dollar amounts, or policies.
protocols:
  - type: responses
    version: 1.0.0
    port: 8088

```

```python
# hosted/main.py — serves the Responses protocol on :8088
import os
from agent_framework.azure import AzureAIAgentServerHost
from azure.identity import DefaultAzureCredential

host = AzureAIAgentServerHost(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
    agent_name=os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant"),
    model_deployment=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
)

if __name__ == "__main__":
    # Hosted agents must listen on 0.0.0.0:8088 for the Responses protocol.
    host.run(host_address="0.0.0.0", port=8088)

```

```dockerfile
# hosted/Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8088
CMD ["python", "main.py"]

```

**Success Criteria:**

- [ ] `hosted/agent.yaml` declares the `responses` protocol (v `1.0.0`) on port `8088`.
- [ ] `hosted/main.py` serves `POST /responses` on `0.0.0.0:8088`.
- [ ] `hosted/Dockerfile` targets `linux/amd64`, exposes `8088`, and runs `main.py`.
- [ ] The container runs locally and answers a Responses call:
      `curl -s -X POST http://localhost:8088/responses -d '{"input":"Where is the registrar?"}'`.

**Checkpoint:**

```bash
python validate.py --step 1
# expected: "✅ Step 1 PASS — agent.yaml + responses entrypoint + Dockerfile present and valid"

```

> _Coach note: see solution.md._

---

## Step 2 — Containerize and deploy with `azd ai agent`

**Goal:** The image is built, pushed to ACR, and the agent is deployed as a **hosted** agent with its
own version and a per-agent managed identity.

**Tasks:**

1. From `hosted/`, build the image to ACR. Prefer **cloud build** (no local Docker needed); the
   `--source-acr-auth-id "[caller]"` flag is mandatory:

   ```bash
   az acr build \
     --registry <acr-name> \
     --image northfield-iq-assistant:$(date +%Y%m%d%H%M) \
     --platform linux/amd64 \
     --source-acr-auth-id "[caller]" \
     --file Dockerfile .

   ```

2. Deploy the hosted agent. `azd ai agent` reads `agent.yaml`, wires the image, creates the agent
   version, and provisions the **per-agent identity**:

   ```bash
   azd ai agent create   # first time: registers the agent from agent.yaml
   azd ai agent deploy    # builds/pushes (if needed) and rolls out the hosted version

   ```

3. Confirm the deployed version is **`active`** before invoking — a hosted version provisions
   asynchronously:

   ```bash
   az ai agent show --name northfield-iq-assistant --query "version,status"

   ```

> ⚠️ **Use a unique image tag every build** (e.g. a timestamp). Reusing `latest` or `v1` causes ACR to
> serve a stale layer and your changes won't roll out.

**Success Criteria:**

- [ ] The image is present in ACR with a unique (timestamped) tag.
- [ ] `azd ai agent deploy` completes and the agent has a deployed hosted version.
- [ ] The version status reports `active`.

**Checkpoint:**

```bash
python validate.py --step 2
# expected: "✅ Step 2 PASS — hosted agent deployed, version active in the project"

```

> _Coach note: see solution.md._

---

## Step 3 — Invoke the live endpoint and verify identity/auth

**Goal:** You call the hosted agent over its production **Responses** endpoint and confirm it runs under
its **own Entra identity**, not your user credentials.

**Tasks:**

1. Create a session, then invoke the deployed agent against its Responses endpoint. The route is
   `{AZURE_AI_PROJECT_ENDPOINT}/agents/{agentName}/endpoint/protocols/openai/responses`:

   ```python
   # invoke_hosted.py
   import os
   from openai import OpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider

   token = get_bearer_token_provider(
       DefaultAzureCredential(), "https://ai.azure.com/.default"
   )
   agent = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant")
   base = os.environ["AZURE_AI_PROJECT_ENDPOINT"].rstrip("/")

   client = OpenAI(
       base_url=f"{base}/agents/{agent}/endpoint/protocols/openai",
       api_key="placeholder",                       # replaced by the bearer token below
       default_headers={"Authorization": f"Bearer {token()}"},
   )

   resp = client.responses.create(input="How do I place a registration hold?")
   print(resp.output_text)

   ```

2. Verify **authorization is enforced**: confirm an unauthenticated call (no bearer token) is rejected
   with `401`/`403`. The endpoint requires the `Foundry User` (formerly `Azure AI User`) role — the agent's **per-agent managed
   identity** is what it uses to reach the model and knowledge base, not your token.

3. Inspect the agent's identity in the portal (agent → **Identity**) and note its principal id. This is
   the identity you'd grant data-plane roles to in production.

**Success Criteria:**

- [ ] An authenticated Responses call returns a grounded answer from the live endpoint.
- [ ] An unauthenticated call is rejected (`401`/`403`).
- [ ] You can name the agent's per-agent managed identity (principal id) from the portal.

**Checkpoint:**

```bash
python challenges/advanced-deploy-hosted-agent/invoke_hosted.py
python validate.py --step 3
# expected: "✅ Step 3 PASS — live endpoint answers authenticated calls, rejects anonymous"

```

> _Coach note: see solution.md._

---

## Step 4 — Tie monitoring back to Tracing & review run history

**Goal:** The hosted agent's production runs are observable — you can see run history on the agent and
the same OTel traces you learned to read in the Tracing challenge.

**Tasks:**

1. Open the agent in the portal → **Runs / Run history**. Confirm your Step 3 invocation appears with
   status, latency, and token usage.

2. Open the **Tracing** tab and find the trace for the hosted run. Confirm it has the same span shape
   you saw locally (model + retrieval spans). The hosted agent inherits the project's App Insights, so
   the spans land in the **same** `dependencies`/`requests`/`traces` tables.

3. Run your `correlate.kql` from the Tracing challenge (or the starter query below) against a **hosted**
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
python validate.py --step 4
# expected: "✅ Step 4 PASS — hosted run visible in run history and App Insights traces"

```

> _Coach note: see solution.md._

---

## Done — what you shipped

- The Northfield IQ Assistant runs as a **hosted Foundry agent** with its own endpoint, version, and
  **per-agent managed identity**.

- It's invocable over the production Responses protocol, enforces auth, and every run is observable in
  run history and App Insights.

**This unlocks Extras:** MAF + Hosted Long-Running Agents (Extra D) and Build a UI (Extra E) both
target this live endpoint.

## Stretch goals

- Add a second **`invocations`** protocol to the same container for a custom request schema.
- Wire a **CI step** (GitHub Actions) that rebuilds the image with a fresh tag and runs
  `azd ai agent deploy` on push.

- Grant the per-agent identity **least-privilege** data-plane roles and remove any local-auth fallback.

## Cleanup

After the event, delete the hosted agent and its image to stop incurring cost:

```bash
azd down            # tears down azd-provisioned resources
# or, agent-only:
az ai agent delete --name northfield-iq-assistant

```

## Learning resources

- [Hosted agents in Microsoft Foundry](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents)
- [Deploy agents with `azd ai agent`](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Hosted-agent samples (foundry-samples)](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
- [Responses & Invocations protocols](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#protocols-responses-and-invocations)
- [ACR cloud build (`az acr build`)](https://learn.microsoft.com/azure/container-registry/container-registry-tutorial-quick-task)
