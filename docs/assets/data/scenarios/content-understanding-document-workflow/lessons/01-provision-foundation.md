# Module 1 — Provision the shared Foundry foundation

Every later module uses the foundation you create here. Content Understanding and Document Intelligence
are **Foundry Tools on a Microsoft Foundry (AIServices) resource**, the account that also hosts model
deployments. Choose the identity model and region now. A wrong choice means redeploying later.

![Shared document workflow foundation](../diagrams/01-shared-foundation.png)

## What you build

A resource group containing:

| Resource | Why the document workflow needs it |
| --- | --- |
| Foundry account (`AIServices`) + project | Hosts Content Understanding, Document Intelligence, and the model deployments they call |
| Chat/generative deployment | Content Understanding generative & classify fields, and LLM structured-output extraction |
| Embedding deployment | Content Understanding custom analyzers and knowledge sources |
| Storage account + `documents-inbound` container | The approved document source that modules 2–4 read |
| Storage `documents-quarantine` container | Isolates documents that fail intake controls |
| Log Analytics + Application Insights | Workflow tracing and the evaluation gate in modules 6–7 |
| Role assignments | Keyless access between the account identity, storage, and the engineer |

This produces a `.env` contract with **no secrets**, used by every later module.

## Choose your path

| Option | Reproducible | Creates storage + embedding | Best when | Cost while idle |
| --- | --- | --- | --- | --- |
| **A. Scenario Bicep** *(default)* | Yes, reviewable IaC | Yes | You are building this workflow for a customer | Idle model deployments + Log Analytics; storage is pennies |
| B. `azd up` (kit root infra) | Yes | No — chat + Search only, no doc storage/embedding | You are running the whole starter kit end to end | Same, plus AI Search + ACR |
| C. Foundry portal / Content Understanding Studio | No | Manual | A throwaway demo of an analyzer | Lowest |
| D. Bring your own landing zone | Customer's IaC | Depends on what exists | The customer already has a governed Foundry resource | Already owned |

**Default: Option A.** It provisions the embedding deployment and inbound and quarantine containers
that modules 2–4 need. It also produces a diff the platform team can review.

**Migration cost.** Moving from A to D is cheap: modules 2+ only read the `.env` contract, so you
change variables. Moving from C to A costs more because portal/Studio resources have generated names
and no template. Do not demo with C and promise A.

### Region and model availability come first

Content Understanding and Document Intelligence are unavailable in some regions, and your models must
deploy in the selected region. Check both **before** you deploy:

```bash
az cognitiveservices account list-skus --location eastus2 --kind AIServices -o table
```

- Content Understanding region support:
  <https://learn.microsoft.com/azure/ai-services/content-understanding/language-region-support>
- Document Intelligence region availability:
  <https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/>

> **API versions to pin.** Content Understanding GA is **`2025-11-01`** (the
> `2024-12-01-preview` / `2025-05-01-preview` previews retire 2026-07-15). Document Intelligence GA
> is **v4.0 `2024-11-30`**. Content Understanding needs default model deployments — `gpt-4.1-mini`
> works today, but the GPT-4.1 family retires October 2026, so plan to migrate to `gpt-5.2`.
> Sources: <https://learn.microsoft.com/azure/ai-services/content-understanding/choosing-right-ai-tool>,
> <https://learn.microsoft.com/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0>

## Implementation

### Option A — Scenario Bicep (default)

The template is [`accelerator/main.bicep`](../accelerator/main.bicep); defaults live in
[`accelerator/parameters.example.json`](../accelerator/parameters.example.json).

```bash
az login
az account set --subscription "<subscription-id>"

# Compile before you deploy — catches schema errors without touching Azure.
bicep build scenarios/content-understanding/accelerator/main.bicep --stdout > /dev/null

./scenarios/content-understanding/accelerator/scripts/deploy.sh rg-content-understanding eastus2
```

`deploy.sh` creates the resource group, validates and deploys the template, then writes
`accelerator/.env` from the outputs. It passes your signed-in object ID as `principalId` to grant
keyless data-plane access.

What the template does that matters, and why:

```bicep
// Keyless-first: shared key access is OFF, so intake must use Entra ID.
allowSharedKeyAccess: false

// The account's managed identity reads inbound documents when analyzing by URL.
resource foundryToStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storage
  properties: {
    principalId: foundry.identity.principalId
    roleDefinitionId: roleStorageBlobDataReader
    principalType: 'ServicePrincipal'
  }
}
```

To deploy into an existing resource group without creating one:

```bash
az deployment group create \
  --resource-group <existing-rg> \
  --template-file scenarios/content-understanding/accelerator/main.bicep \
  --parameters @scenarios/content-understanding/accelerator/parameters.example.json \
  --parameters principalId="$(az ad signed-in-user show --query id -o tsv)"
```

### Option B — `azd up` (kit root infra)

Use when you want the shared footprint every activity in the kit uses. It provisions Foundry +
project + a **chat** deployment + AI Search + observability, but **not** the document storage or the
embedding deployment. Add them before module 2:

```bash
azd up
azd env get-values > scenarios/content-understanding/accelerator/.env

RG=$(azd env get-value AZURE_RESOURCE_GROUP)
ACCOUNT=$(azd env get-value AZURE_AI_FOUNDRY_NAME)

az cognitiveservices account deployment create \
  --resource-group "$RG" --name "$ACCOUNT" \
  --deployment-name embedding \
  --model-name text-embedding-3-large --model-version 1 --model-format OpenAI \
  --sku-name Standard --sku-capacity 30

az storage account create --resource-group "$RG" --name "st${RANDOM}cudoc" \
  --sku Standard_LRS --allow-shared-key-access false
az storage container create --account-name "st${RANDOM}cudoc" --name documents-inbound --auth-mode login
az storage container create --account-name "st${RANDOM}cudoc" --name documents-quarantine --auth-mode login
```

Then append `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME`, `AZURE_STORAGE_ACCOUNT_NAME`,
`AZURE_DOCUMENTS_CONTAINER_NAME`, `AZURE_QUARANTINE_CONTAINER_NAME`,
`AZURE_CONTENT_UNDERSTANDING_ENDPOINT`, and `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` to the `.env`.

This module maps to **Foundations Step 1** — see [the canonical activity](../../../activities/foundations/README.md).

### Option C — Foundry portal / Content Understanding Studio

Use this for a same-day analyzer demo. Create a Foundry resource in the portal, then open Content
Understanding Studio (<https://contentunderstanding.ai.azure.com>) and let it auto-deploy the
required `gpt-4.1`, `gpt-4.1-mini`, and `text-embedding-3-large` models. Record the endpoint and
deployment names into `accelerator/.env` by hand.

This option has no template, uses generated names, and leaves no reviewable platform diff. Treat work
here as disposable. Do not build the pilot on it.

### Option D — Bring your own landing zone

This option creates no resources. Verify what exists, then fill the same contract.

```bash
az cognitiveservices account list \
  --query "[?kind=='AIServices'].{name:name,rg:resourceGroup,loc:location}" -o table
```

Then confirm the three things this scenario depends on:

1. The account has `allowProjectManagement: true` (it is a Foundry account).
2. It exposes Content Understanding and Document Intelligence in its region.
3. The account identity holds **Storage Blob Data Reader** on the document storage, and your identity
   holds **Cognitive Services User** + **Cognitive Services OpenAI User** on the account.

```bash
ACCOUNT_ID=$(az cognitiveservices account show -g <rg> -n <account> --query id -o tsv)
az role assignment create --assignee "$(az ad signed-in-user show --query id -o tsv)" \
  --role "Cognitive Services User" --scope "$ACCOUNT_ID"
```

Write discovered values into `accelerator/.env` using the same variable names the template outputs,
so modules 2–7 are identical across all four options.

## Verify

Check these four items against your own resources before you build on this foundation.

**1. Both model deployments exist.**

```bash
ACCOUNT=$(echo "$AZURE_AI_FOUNDRY_ENDPOINT" | sed -E 's#https?://([^.]+)\..*#\1#')
RG=$(az cognitiveservices account list --query "[?name=='$ACCOUNT'].resourceGroup | [0]" -o tsv)
az cognitiveservices account deployment list --name "$ACCOUNT" --resource-group "$RG" \
  --query "[].name" -o tsv
```

You should see the names in `AZURE_AI_MODEL_DEPLOYMENT_NAME` and `AZURE_AI_EMBEDDING_DEPLOYMENT_NAME`.
Content Understanding calls both during analysis. If either is missing, later modules fail with a
deployment-not-found error.

**2. Content Understanding answers your Entra identity, with no key.**

```bash
CU=$(echo "$AZURE_CONTENT_UNDERSTANDING_ENDPOINT" | sed 's:/*$::')
TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: ******" \
  "$CU/contentunderstanding/analyzers?api-version=2025-11-01"
```

A `200` means keyless data-plane access works. A `403` means your identity lacks **Cognitive Services
User** on the account. Grant that role instead of using a key. A `404` means the region does not
expose Content Understanding; redeploy elsewhere.

**3. The document containers are private and reachable without a key.**

```bash
az storage container show --account-name "$AZURE_STORAGE_ACCOUNT_NAME" \
  --name "$AZURE_DOCUMENTS_CONTAINER_NAME" --auth-mode login \
  --query "properties.publicAccess" -o tsv
```

If the command succeeds, Entra data-plane access works. Empty `publicAccess` means no anonymous
access. A value of `blob` or `container` exposes the inbound corpus publicly. Fix it before uploading
documents.

**4. The environment contract holds no secrets.**

```bash
grep -iE 'api_key|account_key|connection_string|sas_token' scenarios/content-understanding/accelerator/.env
```

You want no output. Any match means an upstream step provided a key and broke the keyless chain.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `401` / `403` from the account | Missing data-plane roles; RBAC takes minutes to propagate | Assign **Cognitive Services User** + **Cognitive Services OpenAI User**, wait ~5 min, re-run |
| Deployment fails on the model | Model or capacity unavailable in the region | `az cognitiveservices account list-skus --location <region> --kind AIServices -o table`, then change region or lower `chatModelCapacity` |
| Both deployments fail together | Deployments on one account serialize | The template sets `dependsOn` on the embedding deployment; do not remove it |
| `StorageAccountAlreadyTaken` | `resourceToken` collides globally | Pass a different `resourceToken` (5–12 lowercase chars) |
| Content Understanding calls 404 | Wrong endpoint host or unsupported region | Use `AZURE_CONTENT_UNDERSTANDING_ENDPOINT` from the outputs; confirm the region supports the service |
| `.env` written but empty | Deployment succeeded with no outputs | Check `accelerator/.deployment-outputs.json`; re-run the deployment |

## Decision record

Record the selected option and why, region and its availability evidence, chat and embedding model and
version, pinned Content Understanding and Document Intelligence API versions, local-auth status, and
resource-group owner. Use one short paragraph plus `.env` variable names, never their values.

## Next module

[Module 2 — Connect an approved document source](02-document-source.md) decides where trusted
documents come from and how intake controls keep unapproved content out.
