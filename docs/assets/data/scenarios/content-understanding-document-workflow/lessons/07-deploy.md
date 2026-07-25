# Module 7 — Deploy the reviewable workflow

The workflow passed the gate; now ship it without losing anything that made it safe. Deployment is
where keyless auth, monitoring, and rollback stop being slideware and become the difference between a
pilot you can operate and one you cannot.

![Controlled deployment boundary](../diagrams/07-controlled-deployment.png)

## What you build

An authenticated endpoint running the reviewed workflow with a managed identity, Application Insights
monitoring with GenAI tracing on, and a rollback path — captured as
[`accelerator/sample-data/workflow/deploy-manifest.json`](../accelerator/sample-data/workflow/deploy-manifest.json)
and confirmed by observing that the endpoint rejects unauthenticated calls.

## Choose your path

| Option | Runtime | Identity + auth | Rollback | Best when |
| --- | --- | --- | --- | --- |
| **A. Hosted agent (`azd ai agent`)** *(default)* | Foundry-hosted container | Managed identity, authenticated endpoint | Pin/swap revision | You built on the Foundry agent stack |
| B. Container app / managed online endpoint | Your container | Managed identity + Entra auth | Revision or blue/green | You need custom runtime or scaling control |
| C. API behind API Management | Your API | Entra-validated via APIM | Deployment slots | You are fronting an existing API estate |
| D. Hosted long-running workflow | Background job handle + later retrieval | Managed identity, authenticated submit/poll | Pin/swap revision | Document processing outlives an interactive request |

**Default: Option A.** The workflow is already a Foundry agent with an approved action-tool seam; a
hosted agent keeps the managed identity, auth, and tracing wiring you built rather than re-creating
it. It is the shortest path from "passed the gate" to "running behind auth".

**Choose B** when you need a custom runtime, specific scaling, or network isolation the hosted option
doesn't give you. **Choose C** when this workflow must live behind an existing API Management estate
and inherit its policies. All three keep the same rule: **no keys**, managed identity, authenticated
endpoint, monitoring on, rollback ready.

**Choose D** only when the document workload is naturally asynchronous: overnight intake, a backlog of
files, or a review process the user submits and checks later. The
[Hosted Long-Running Agents activity](../../../activities/extra-hosted-longrunning/README.md)
covers the background-run contract, response handle, later retrieval, and trace review. If one
document should return while the reviewer is waiting, do not add this complexity.

**Migration cost.** A → B/C re-hosts the same container and identity model; the workflow, action-tool
seam, and evaluation gate are unchanged. The manifest you record is identical across all
three — only the runtime line differs. That is deliberate: the deployment target is a late, reversible
decision.

## Implementation

### Option A — Hosted agent (default)

Ship the reviewed workflow as a hosted agent with a managed identity and an authenticated endpoint,
keeping GenAI tracing on. Build and deploy it with the canonical
[Deploy as a Hosted Agent activity](../../../activities/advanced-deploy-hosted-agent/README.md), which
covers `agent.yaml`, `azd ai agent`, per-agent Entra identity, and the dedicated endpoint. Carry the
same tracing env into the deployment:

```bash
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

Record the deployment facts (auth mode, managed identity, monitoring, rollback strategy, and that the
module-6 gate passed) into `deploy-manifest.json`.

### Option B — Container app / managed online endpoint

Run the same container yourself with a system-assigned managed identity and Entra authentication on
the ingress. Point Application Insights at it (the connection is already a project connection from
module 1) and keep two revisions so rollback is a revision swap, not a redeploy. The action-tool seam
and the workflow identity are unchanged — you are only changing where the container runs.

### Option C — API behind API Management

Front the workflow with an API and let API Management validate Entra tokens before the request
reaches it. Use deployment slots for rollback. This suits an organization standardizing every AI
endpoint behind one gateway; you inherit APIM's throttling, logging, and policy at the cost of one
more hop.

## Verify

Check the deployed endpoint the way an attacker and an operator would: try it without a token, confirm
it runs as an identity and not a key, and confirm it is still traced.

**1. The endpoint refuses an unauthenticated caller.**

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://<your-endpoint>/<route>
```

You want `401` or `403`. A `200` means the workflow is exposed anonymously — anyone who finds the URL
can push documents through it and read extracted results. Then confirm an authenticated call still
works so you know you tested the right route:

```bash
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: ******" https://<your-endpoint>/<route>
```

**2. The runtime runs as a managed identity, with no keys.**

```bash
grep -riE '(api[_-]?key|account[_-]?key|connection[_-]?string|sharedaccesskey)' deploy-manifest.json
```

No output is what you want. Then confirm the deployment identity actually holds the roles it needs —
absent them, the endpoint authenticates callers but cannot reach its own models or storage:

```bash
az role assignment list --assignee "<deployment-managed-identity-object-id>" \
  --query "[].roleDefinitionName" -o tsv
```

Expect **Cognitive Services User** and **Storage Blob Data Reader**. A key in the config or a missing
role is how key-based auth quietly creeps back in at the last step.

**3. The deployed runtime still emits traces.**

Send one authenticated request, then query the workspace behind `APPLICATIONINSIGHTS_RESOURCE_ID`:

```kusto
dependencies
| where timestamp > ago(15m)
| where customDimensions has "gen_ai"
| project timestamp, name, duration, operation_Id
| order by timestamp desc
```

Rows for your request mean tracing survived the deployment. No rows means the GenAI env vars were not
carried into the runtime, and you shipped a workflow you cannot observe in production.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Live probe returns `200` unauthenticated | Endpoint not protected | Require Entra auth on ingress; never expose the workflow anonymously |
| Deployment can't reach models or storage | Managed identity missing roles | Re-assign **Cognitive Services User** / **Storage Blob Data Reader** to the deployment identity |
| No traces after deploy | Tracing env not carried into the runtime | Set both GenAI env vars in the deployment, before the SDK loads |
| Rollback means a full redeploy | No revision/slot retained | Keep the previous revision pinned; make rollback a swap |
| Manifest still lists module 6 as not passed | Shipping before module 6 passed | Do not deploy until the gate is green; it is a release prerequisite |
| Secrets appear in the deployment config | Key-based auth crept back in | Return to managed identity; scan config for `*_KEY` / connection strings |

## Decision record

Short: the runtime you chose and why, the endpoint auth model, the monitoring and trace destination,
the rollback mechanism, and the release approver. One paragraph, with a date — this is the pilot
release record.

## Next module

You have completed the seven-module path — a reviewable, evidence-backed document workflow. Start the
next document decision at [Module 1](01-provision-foundation.md), or extend this workflow with the
deployment and operations patterns that match the next customer decision.
