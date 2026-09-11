# AI Grounding / IQ accelerator

This accelerator has two parts: a synthetic corpus and scripts that run against your Azure
resources, plus an optional Bicep foundation for a clean Azure demo subscription. It is neither a
landing zone nor production approval.

`main.bicep` provisions the minimal Foundry, AI Search, Storage, and observability footprint for the
scenario lessons. Use it only in a clean demo subscription. In a bring-your-own environment, use the
same lesson contracts and validators against customer-approved resources. Do not redeploy this package.

## Two workshop paths

### Clean-subscription demo

Use a disposable subscription after the customer agrees the pilot boundary. Provision the demo
foundation, then replace the fictional corpus through the agreed source and permission process.

### BYO existing environment

Record the resource IDs and approved source boundary. Do not redeploy or change customer resources
from this package.

## Before any implementation

1. Search current Microsoft Learn documentation and the relevant Microsoft Foundry guidance for the required capability.
2. Confirm whether Copilot Studio + SharePoint is the simpler governed experience before selecting Foundry.
3. Verify current supported source, permission, region, network, and evaluation behavior for Foundry IQ, Fabric IQ, Work IQ, or Web IQ.
4. Load the matching implementation guidance, then implement against the verified signature.
5. Run the customer’s golden dataset and access tests before you connect production content.

Do not infer preview API signatures from this repository.

## Optional Bicep foundation

```bash
az deployment group create \
  --resource-group <demo-resource-group> \
  --template-file main.bicep \
  --parameters @parameters.example.json
```

The command creates demo resources and emits the `.env` contract that later scripts consume.

## Scripts

Five scripts work against your resources. `build_knowledge_source.py` creates the knowledge source
and knowledge base. `probe_permissions.py` checks the permission boundary with a second,
lower-privileged identity. `compare_models.py` compares candidate deployments, and
`grounded_answer.py` runs golden questions and reports citations, abstention, and recall. All need a
subscription and the `.env` contract. Each lesson's **Verify** section says which to run and how to
read its output.

`probe_surface.py` verifies a deployed HTTP surface. It sends the same configured request as an
anonymous caller, an authorized caller, and a restricted caller. The endpoint is required on the
command line; `surface-probe.json` defines the method, headers, body, allowed statuses, and safe
response markers for that surface. Set the two caller tokens in named environment variables, then
pass only their variable names to the script. It never prints tokens, headers, request bodies, or
response bodies.

## Sample-data swaps

The fictional files in `sample-data/` model a small returns-policy pilot. Before a real pilot, replace **all** of the following explicitly:

| Sample element | Replace with |
|---|---|
| `sample-data/` content | approved customer documents, records, or web scope |
| `customer-demo-grounding` container label | the approved storage/container or source location |
| `customer-demo-iq-index` index label | the approved Foundry/Fabric/other index or knowledge configuration |
| `customer-demo-embedding-model` | the approved embedding model/deployment, verified for the chosen service and region |

Never treat these labels as deployed resources or supported API names.
