# Solution notes · Extra — Document Workflow

This is the canonical Python implementation shape, not a substitute for the required live
`microsoft-docs` MCP search. It aligns with the required learner artifact, `document_workflow.py`, and
its validator. Confirm the installed SDK signature again before implementation.

## Keyless layout/OCR call

Install the current packages shown by Docs:

```bash
python -m pip install azure-ai-documentintelligence azure-identity
```

Set only the endpoint (for example, `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`) and authenticate with
`az login` locally or managed identity in Azure. The endpoint must be a custom subdomain because regional
Document Intelligence endpoints do not support Microsoft Entra authentication. Do not configure or store
a Document Intelligence key.

```python
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
client = DocumentIntelligenceClient(endpoint, DefaultAzureCredential())

with open("./fictional-sample-application.pdf", "rb") as document:
    poller = client.begin_analyze_document("prebuilt-layout", body=document)
layout = poller.result()
```

The important details are deliberate: `DocumentIntelligenceClient` with `DefaultAzureCredential`,
the `prebuilt-layout` model, and waiting for the long-running operation with `poller.result()`.
Use the current Docs signature if it differs; do not substitute an old key-credential sample.

## Workflow logic

Map layout lines/tables into only the fictional demo fields. Store per-field `confidence` and source
page/region. Use a named threshold (such as `CONFIDENCE_THRESHOLD = 0.85`) plus deterministic
required-field and format rules:

- Confidence below threshold, missing consent, or invalid applicant ID → `needs_review`.
- Send the record, reason, and source reference to a human review queue.
- Only an explicit reviewer approval may mark the intake record `approved`; this is never an
  admission decision.
- Emit a versioned JSON record containing `intake_id`, `status`, fields, confidence, source, and
  review decision. Avoid raw application text in operational logs.

## Trace and evaluation evidence

For every fictional run, emit a correlation/trace ID, model name, threshold version, timing, status,
and review reason. Keep raw OCR/layout output out of traces. Evaluate a small labeled fictional set
with known fields and report field accuracy, low-confidence review rate, reviewer overrides, and
false approvals. A successful run with low accuracy or a false approval is a failure signal, not a
reason to lower the threshold.

Run the supplied static check after writing `document_workflow.py`:

```bash
python validate.py --all --path .
```

It confirms structural signals only. Use a live fictional document and a facilitator review to prove
the actual service call, RBAC, review route, and evaluation claim.
