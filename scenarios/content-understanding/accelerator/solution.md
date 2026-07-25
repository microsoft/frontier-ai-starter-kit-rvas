# Content Understanding document workflow — reference implementation

This is the complete, keyless reference for the seven modules. API versions, model ids, and packages
are called out where they matter. The lessons under [`../lessons/`](../lessons/) walk through the
decisions; this file is the code you land on.

> Keyless-first throughout: `DefaultAzureCredential` + managed identity + Entra RBAC. No keys
> appear in code, `.env`, or Bicep. Run `az login` for local development.

## 0. Provision and load the contract

```bash
./scripts/deploy.sh rg-content-understanding eastus2
# writes accelerator/.env, then confirm the endpoint answers your Entra identity:
TOKEN=$(az account get-access-token --scope https://cognitiveservices.azure.com/.default --query accessToken -o tsv)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  "$AZURE_CONTENT_UNDERSTANDING_ENDPOINT"
```

The `.env` contract (no secrets):

```
AZURE_AI_PROJECT_ENDPOINT=https://aif-<token>.services.ai.azure.com/api/projects/proj-<token>
AZURE_CONTENT_UNDERSTANDING_ENDPOINT=https://aif-<token>.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://aif-<token>.cognitiveservices.azure.com/
AZURE_AI_MODEL_DEPLOYMENT_NAME=chat
AZURE_AI_EMBEDDING_DEPLOYMENT_NAME=embedding
AZURE_STORAGE_ACCOUNT_NAME=st<token>
AZURE_DOCUMENTS_CONTAINER_NAME=documents-inbound
AZURE_QUARANTINE_CONTAINER_NAME=documents-quarantine
```

## 1. Content Understanding — prebuilt analyzer (GA `2025-11-01`)

Set resource default model deployments once, then analyze. Content Understanding is async:
`POST …:analyze` returns `202` + `Operation-Location`; poll the result.

```python
import os, time, requests
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_CONTENT_UNDERSTANDING_ENDPOINT"].rstrip("/")
token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
api = "api-version=2025-11-01"

# prebuilt-invoice extracts typed fields with confidence + grounding.
start = requests.post(
    f"{endpoint}/contentunderstanding/analyzers/prebuilt-invoice:analyze?{api}",
    headers=headers,
    json={"inputs": [{"url": "https://<account>.blob.core.windows.net/documents-inbound/invoice-2002.pdf"}]},
)
start.raise_for_status()
op = start.headers["Operation-Location"]

while True:
    result = requests.get(op, headers={"Authorization": f"Bearer {token}"}).json()
    if result["status"] in ("Succeeded", "Failed"):
        break
    time.sleep(2)

fields = result["result"]["contents"][0]["fields"]
total = fields["InvoiceTotal"]["valueObject"]["Amount"]
print(total["valueNumber"], total["confidence"], total["source"])  # value, 0..1, grounding polygon
```

To get confidence + grounding from a **custom** analyzer, set
`"estimateFieldSourceAndConfidence": true` in the analyzer definition, then create it with
`PUT /contentunderstanding/analyzers/{analyzerId}?api-version=2025-11-01` before calling `:analyze`.

Reference: <https://learn.microsoft.com/azure/ai-services/content-understanding/quickstart/use-rest-api>

## 2. Document Intelligence — prebuilt model (v4.0 GA `2024-11-30`)

Deterministic extraction for stable templates. Keyless with `DocumentIntelligenceClient`.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

client = DocumentIntelligenceClient(
    endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
poller = client.begin_analyze_document(
    "prebuilt-invoice",
    AnalyzeDocumentRequest(url_source="https://<account>.blob.core.windows.net/documents-inbound/invoice-2002.pdf"),
)
result = poller.result()
for doc in result.documents:
    field = doc.fields["InvoiceTotal"]
    print(field.value_currency, field.confidence, field.bounding_regions)  # value, 0..1, polygons
```

Package: `pip install azure-ai-documentintelligence`. Model ids: `prebuilt-invoice`,
`prebuilt-layout`, `prebuilt-read`, `prebuilt-contract`, plus tax/mortgage/id models. For custom
structured forms, train a custom model and pass its id instead of `prebuilt-invoice`.
Reference: <https://learn.microsoft.com/azure/ai-services/document-intelligence/overview?view=doc-intel-4.0.0>

## 3. LLM structured outputs (build-your-own fallback)

Full control, but **no native confidence or grounding** — you own validation.

```python
from pydantic import BaseModel
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
client = OpenAI(base_url="https://<res>.openai.azure.com/openai/v1/", api_key=token_provider)

class Invoice(BaseModel):
    invoice_number: str
    total_due_usd: str

completion = client.beta.chat.completions.parse(
    model="chat",                       # your deployment name
    messages=[{"role": "system", "content": "Extract only fields present in the document; never infer."},
              {"role": "user", "content": document_markdown}],
    response_format=Invoice,
)
invoice = completion.choices[0].message.parsed
```

Reference: <https://learn.microsoft.com/azure/foundry/openai/how-to/structured-outputs>

## 4. Typed result contract with evidence

Normalize every capability's output into one contract, then gate on confidence and evidence.
See [`sample-data/workflow/typed-result.json`](sample-data/workflow/typed-result.json). The rule:
**a value without grounding evidence is an inferred value and is rejected**; any field below the
threshold forces human review.

Open the typed result next to the source document and check each field's span actually points at the
text it claims. A field with a high confidence score and no usable span is the one that will burn
you.

## 5. Human review, correction, and handoff

The reviewer decision is captured as an [approval trace](sample-data/workflow/approval-trace.json):
reviewer identity, timestamp, before/after values, and the approved downstream seam (an action
tool). Corrections are retained as evaluation evidence — they never overwrite the original expected
result. See [`../lessons/05-human-review.md`](../lessons/05-human-review.md) and the canonical
[Action Tools activity](../../../activities/advanced-action-tools/README.md).

Submit one document you know is ambiguous and confirm it lands in the review queue rather than
passing straight through. If nothing ever routes to a human, the threshold is wrong, not the corpus.

## 6. Evaluate and trace

Grade a real evaluation run against the gate in
[`sample-data/workflow/eval-report.json`](sample-data/workflow/eval-report.json): field accuracy,
false-approval rate, review rate, and injection resistance. Enable GenAI tracing **before**
importing the Foundry SDK:

```bash
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
```

Then confirm traces are arriving in Application Insights before you rely on them.

Canonical activity: [Evaluation & Red Teaming](../../../activities/advanced-evaluation-redteam/README.md).

## 7. Deploy the reviewable workflow

Ship behind an authenticated endpoint with managed identity, Application Insights, and a rollback
path. Confirm the endpoint refuses an unauthenticated caller:

```bash
curl -s -o /dev/null -w '%{http_code}\n' "$WORKFLOW_ENDPOINT"
```

A `401` or `403` is the answer you want.

Canonical activity: [Deploy as a Hosted Agent](../../../activities/advanced-deploy-hosted-agent/README.md).

## Offline validation pack

Run the whole workflow over the synthetic fixtures and compare every extracted field against the
source document. That comparison is the evidence — a workflow that runs without erroring is not the
same as a workflow that extracts the right values.
