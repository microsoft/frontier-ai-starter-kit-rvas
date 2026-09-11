# Module 7 — Deploy the reviewable workflow

The workflow passed the gate. Deploy it without losing the controls that made it safe. Deployment
makes keyless auth, monitoring, and rollback operational rather than aspirational.

![Controlled deployment boundary](../diagrams/07-controlled-deployment.png)

## What you build

An authenticated endpoint that runs the reviewed workflow with a managed identity, Application
Insights monitoring and GenAI tracing, plus a rollback path. Confirm that the endpoint rejects
unauthenticated calls.

## Choose your path

| Option | Runtime | Identity + auth | Rollback | Best when |
| --- | --- | --- | --- | --- |
| **A. Hosted agent (`azd ai agent`)** *(default)* | Foundry-hosted container | Managed identity, authenticated endpoint | Pin/swap revision | You built on the Foundry agent stack |
| B. Container app / managed online endpoint | Your container | Managed identity + Entra auth | Revision or blue/green | You need custom runtime or scaling control |
| C. API behind API Management | Your API | Entra-validated via APIM | Deployment slots | You are fronting an existing API estate |
| D. Hosted long-running workflow | Background job handle + later retrieval | Managed identity, authenticated submit/poll | Pin/swap revision | Document processing outlives an interactive request |

**Default: Option A.** The workflow is already a Foundry agent with an approved action-tool seam. A
hosted agent retains its managed identity, auth, and tracing wiring. It is the shortest route from a
passed gate to an authenticated service.

**Choose B** when you need a custom runtime, specific scaling, or network isolation unavailable from
hosting. **Choose C** when the workflow belongs behind an existing API Management estate and its
policies. Every option follows the same rule: **no keys**, managed identity, authenticated endpoint,
monitoring enabled, rollback ready.

**Choose D** only for naturally asynchronous work: overnight intake, a file backlog, or a review
process users submit and check later. The
[Hosted Long-Running Agents activity](../../../activities/extra-hosted-longrunning/README.md)
covers the background-run contract, response handle, later retrieval, and trace review. Do not add
this complexity when a reviewer expects one document to return while waiting.

**Migration cost.** Moving from A to B or C rehosts the same container and identity model. The
workflow, action-tool seam, and evaluation gate remain unchanged. You can make this decision late
and reverse it.

## Implementation

### Option A — Hosted agent (default)

Deploy the reviewed workflow as a hosted agent with managed identity and an authenticated endpoint.
Keep GenAI tracing enabled. Build and deploy it with the canonical
[Deploy as a Hosted Agent activity](../../../activities/advanced-deploy-hosted-agent/README.md), which
covers `agent.yaml`, `azd ai agent`, per-agent Entra identity, and the dedicated endpoint. Carry the
same tracing env into the deployment:

```bash
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

### Option B — Container app / managed online endpoint

Run the same container with a system-assigned managed identity and Entra authentication at ingress.
Point Application Insights at it (the connection is already a project connection from module 1). Keep
two revisions so rollback is a revision swap. The action-tool seam and workflow identity remain the
same; only the host changes.

### Option C — API behind API Management

Front the workflow with an API and let API Management validate Entra tokens before requests reach it.
Use deployment slots for rollback. This fits organizations that standardize AI endpoints behind one
gateway. It adds one hop and gains APIM throttling, logging, and policy.

## Verify

Check the deployed endpoint as both attacker and operator. Try it without a token, confirm it uses an
identity rather than a key, and verify that traces still arrive.

**1. The endpoint refuses an unauthenticated caller.**

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://<your-endpoint>/<route>
```

You want `401` or `403`. A `200` exposes the workflow anonymously. Anyone who finds the URL can push
documents through it and read extracted results. Then confirm that an authenticated call still works:

```bash
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
curl -sS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" https://<your-endpoint>/<route>
```

**2. The runtime runs as a managed identity, with no keys.**

```bash
grep -inE '(api[_-]?key|account[_-]?key|connection[_-]?string|sharedaccesskey)' \
  scenarios/content-understanding/accelerator/.env
```

Inspect the deployed runtime settings too. This scan flags names for review; it does not prove
that a value is a secret. An Application Insights connection string identifies a telemetry
destination and is not a model API key. Confirm that the deployment identity holds its required roles. Without them,
the endpoint authenticates callers but cannot access models or storage:

```bash
az role assignment list --assignee "<deployment-managed-identity-object-id>" \
  --query "[].roleDefinitionName" -o tsv
```

Expect **Cognitive Services User** and **Storage Blob Data Reader**. A key in configuration or a
missing role breaks the keyless design at the last step.

**3. The deployed runtime still emits traces.**

Send one authenticated request, then query the workspace behind `APPLICATIONINSIGHTS_RESOURCE_ID`:

```kusto
dependencies
| where timestamp > ago(15m)
| where customDimensions has "gen_ai"
| project timestamp, name, duration, operation_Id
| order by timestamp desc
```

Rows for your request mean tracing survived deployment. No rows mean the runtime did not receive the
GenAI environment variables, so you cannot observe the workflow in production.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Live probe returns `200` unauthenticated | Endpoint not protected | Require Entra auth on ingress; never expose the workflow anonymously |
| Deployment can't reach models or storage | Managed identity missing roles | Re-assign **Cognitive Services User** / **Storage Blob Data Reader** to the deployment identity |
| No traces after deploy | Tracing env not carried into the runtime | Set both GenAI env vars in the deployment, before the SDK loads |
| Rollback means a full redeploy | No revision/slot retained | Keep the previous revision pinned; make rollback a swap |
| Manifest still lists module 6 as not passed | Shipping before module 6 passed | Do not deploy until the gate is green; it is a release prerequisite |
| Secrets appear in the deployment config | Key-based auth crept back in | Return to managed identity; scan config for `*_KEY` / connection strings |

## Next module

You have completed the seven-module path: a reviewable, evidence-backed document workflow. Start the
next document decision at [Module 1](01-provision-foundation.md), or extend this workflow with
deployment and operations patterns that fit the next customer decision.
