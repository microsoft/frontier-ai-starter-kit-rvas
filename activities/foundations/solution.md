# Implementation notes — Foundations mechanics

Use these notes to adapt the Foundations mechanics to a scenario or customer build. They are not a
second curriculum path; the scenario lesson remains the decision record.

## Step 1 — Provisioning

The reusable contract is:

- `azd up` provisions the Foundry resource/project, chat deployment, Azure AI Search, Log Analytics,
  and Application Insights.
- `azd env get-values > .env` exports the local runtime contract.
- Local code uses `DefaultAzureCredential`; do not introduce API-key paths.

When adapting the mechanics, keep `.env.sample` as the source of truth for environment variable names.
If provisioning differs by scenario, the scenario lesson should explain the decision and this module
should keep the reusable command shape.

## Step 2 — Model comparison

Keep comparisons fair:

- Change one variable at a time: model deployment, not prompt and model together.
- Use the same prompts and the same system instruction for every candidate.
- Record the observed trade-off: quality, latency, cost, or availability.

The scenario owns which model classes are acceptable. This module only shows how to compare deployed
models and reproduce the selected behavior through the Responses API.

## Step 3 — First agent

The reusable mechanics are:

- Store the instructions in source-controlled text, not only in the portal.
- Create a named, versioned prompt agent.
- Drive the agent through the Responses API with an `agent_reference`.
- Re-run guardrail probes whenever instructions change.

Use a scenario-specific name, persona, scope, refusal policy, and test prompts. The sample
`sample-iq-assistant` name is only a placeholder for the shipped sample assets.

## Step 4 — Azure AI Search grounding

The reusable mechanics are:

- Chunk approved content into an Azure AI Search index.
- Keep retrievable `content` and `source` fields so the agent can cite evidence.
- Attach the search connection as an agent tool.
- Require the assistant to answer only from retrieved context and cite sources.
- Verify retrieval separately from answer quality.

Do not call this Foundry IQ unless you are using the managed Foundry IQ knowledge workflow. This
reference uses Azure AI Search grounding directly.

## Verification contract

The sample validation commands are useful only when the sample assets are present:

Run these commands from the repository root.

| Command | Asserts |
|---|---|
| `python activities/foundations/validate.py --step 1` | Foundry + AI Search + App Insights exist; `.env` is populated; keyless auth works |
| `python activities/foundations/validate.py --step 2` | The model deployment is reachable and a Responses API call succeeds |
| `python activities/foundations/validate.py --step 3` | The named versioned agent exists and responds through the Responses API |
| `python activities/foundations/validate.py --step 4` | The Azure AI Search index exists and the agent returns a cited grounded answer |
| `python activities/foundations/validate.py --all` | All four mechanics are present end-to-end |

For customer scenarios, replace the sample prompts and corpus with the scenario's approved data and
write equivalent observable checks in that scenario's `Verify` section.
