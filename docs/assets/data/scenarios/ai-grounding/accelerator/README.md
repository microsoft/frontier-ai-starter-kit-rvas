# AI Grounding / IQ accelerator

This accelerator has two parts: a synthetic corpus with scripts that run against your own Azure
resources, and an optional Bicep foundation for a clean Azure demo subscription. It is not a landing
zone and it is not production approval.

`main.bicep` provisions the minimal Foundry, AI Search, Storage, and observability footprint used by
the scenario lessons. Use it only for a clean demo subscription. For a bring-your-own environment,
use the same lesson contracts and validators against the customer-approved resources instead of
redeploying from this package.

## Two workshop paths

### Clean-subscription demo

Use a disposable subscription only after the customer agrees the pilot boundary. Provision the demo
foundation, then replace the fictional corpus with approved customer data only through the agreed
source and permission process.

### BYO existing environment

Record the existing resource IDs and the approved source boundary. Do not redeploy or mutate customer resources from this package.

## Before any implementation

1. Search current Microsoft Learn documentation and the relevant Microsoft Foundry guidance for the required capability.
2. Confirm whether Copilot Studio + SharePoint is the simpler governed experience before selecting Foundry.
3. Verify current supported source, permission, region, network, and evaluation behavior for Foundry IQ, Fabric IQ, Work IQ, or Web IQ.
4. Load the matching implementation guidance, then implement against the verified signature.
5. Run the customer’s golden dataset and access tests before connecting production content.

Do not infer preview API signatures from this repository.

## Optional Bicep foundation

```bash
az deployment group create \
  --resource-group <demo-resource-group> \
  --template-file main.bicep \
  --parameters @parameters.example.json
```

The command creates demo resources and emits the `.env` contract consumed by later scripts.

## Scripts

Four scripts do real work against your own resources: `build_knowledge_source.py` creates the
knowledge source and knowledge base, `probe_permissions.py` checks the permission boundary with a
second lower-privileged identity, `compare_models.py` prints a comparison table across candidate
deployments, and `grounded_answer.py` runs the golden questions and reports citations, abstention,
and recall. All four need a subscription and the `.env` contract. Each lesson's **Verify** section
says which to run and what its output should tell you.

## Sample-data swaps

The fictional files in `sample-data/` model a small returns-policy pilot. Before a real pilot, replace **all** of the following explicitly:

| Sample element | Replace with |
|---|---|
| `sample-data/` content | approved customer documents, records, or web scope |
| `customer-demo-grounding` container label | the approved storage/container or source location |
| `customer-demo-iq-index` index label | the approved Foundry/Fabric/other index or knowledge configuration |
| `customer-demo-embedding-model` | the approved embedding model/deployment, verified for the chosen service and region |

Never treat these labels as deployed resources or supported API names.
