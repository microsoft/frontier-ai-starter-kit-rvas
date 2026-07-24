# AI Grounding / IQ accelerator

This is a **decision artifact**, not a tenant deployment. It has no Azure SDK code, tenant identifiers, connections, secrets, or runnable knowledge-source configuration.

`main.bicep` is deliberately minimal: it can be used as a clean-subscription deployment record or a bring-your-own (BYO) existing-environment handoff, but creates no landing zone and no resource. This prevents a workshop template from inventing service resource APIs or changing a customer tenant.

## Two workshop paths

### Clean-subscription demo

Use a disposable subscription only after the customer agrees the pilot boundary. Keep the deployment record minimal; separately provision approved services with current, verified patterns.

### BYO existing environment

Record the existing resource IDs and the approved source boundary. Do not redeploy or mutate customer resources from this package.

## Before any implementation

1. Search current Microsoft Learn documentation and the relevant Microsoft Foundry guidance for the required capability.
2. Confirm whether Copilot Studio + SharePoint is the simpler governed experience before selecting Foundry.
3. Verify current supported source, permission, region, network, and evaluation behavior for Foundry IQ, Fabric IQ, Work IQ, or Web IQ.
4. Load the matching implementation guidance, then implement against the verified signature.
5. Run the customer’s golden dataset and access tests before connecting production content.

Do not infer preview API signatures from this repository.

## Minimal Bicep handoff

```bash
az deployment sub create \
  --location <approved-region> \
  --template-file main.bicep \
  --parameters @parameters.example.json
```

The command records chosen mode and supplied existing-environment identifiers in deployment outputs. It creates no resources.

## Local-only corpus review

`LOCAL-DEMO.md` runs a standard-library-only simulation over the fictional sample corpus. It produces `evidence/local-retrieval-evidence.json`, a reviewable record of source metadata, access groups, golden-question citations, and refusal/access cases. It is a transparent workshop check, not an Azure, Foundry IQ, or authorization implementation.

## Sample-data swaps

The fictional files in `sample-data/` model a small returns-policy pilot. Before a real pilot, replace **all** of the following explicitly:

| Sample element | Replace with |
|---|---|
| `sample-data/` content | approved customer documents, records, or web scope |
| `customer-demo-grounding` container label | the approved storage/container or source location |
| `customer-demo-iq-index` index label | the approved Foundry/Fabric/other index or knowledge configuration |
| `customer-demo-embedding-model` | the approved embedding model/deployment, verified for the chosen service and region |

Never treat these labels as deployed resources or supported API names.
