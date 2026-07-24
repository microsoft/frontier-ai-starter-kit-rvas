# Solution notes · Extra — Document Workflow

This is the canonical implementation shape, not a substitute for the required live `microsoft-docs`
MCP search. The TypeScript pattern below was verified against this project's
`azure-ai-document-intelligence-ts` skill reference; confirm it again before implementation.

## Keyless layout/OCR call

Install the current packages shown by Docs:

```bash
npm install @azure-rest/ai-document-intelligence @azure/identity
```

Set only the endpoint (for example, `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`) and authenticate with `az login`
locally or managed identity in Azure. Do not configure or store a Document Intelligence key.

```ts
import { readFile } from "node:fs/promises";
import DocumentIntelligence, {
  getLongRunningPoller,
  isUnexpected,
} from "@azure-rest/ai-document-intelligence";
import { DefaultAzureCredential } from "@azure/identity";

const endpoint = process.env.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT;
if (!endpoint) throw new Error("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT is required");

const client = DocumentIntelligence(endpoint, new DefaultAzureCredential());
const base64Source = (await readFile("./fictional-northfield-application.pdf")).toString("base64");

const initialResponse = await client
  .path("/documentModels/{modelId}:analyze", "prebuilt-layout")
  .post({
    contentType: "application/json",
    body: { base64Source },
  });

if (isUnexpected(initialResponse)) {
  throw initialResponse.body.error;
}

const poller = getLongRunningPoller(client, initialResponse);
const completed = await poller.pollUntilDone();
const layout = completed.body.analyzeResult;
```

The important details are deliberate: `DocumentIntelligence(endpoint, new DefaultAzureCredential())`,
`POST /documentModels/{modelId}:analyze` with `prebuilt-layout`, `isUnexpected`, a long-running
poller followed by `pollUntilDone`, and `base64Source` for a local file. Do not replace this with a
binary stream or an old key credential sample. Current Docs remains authoritative if it differs.

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

Run the supplied static check after writing the Python workflow:

```bash
python validate.py --all --path .
```

It confirms structural signals only. Use a live fictional document and a facilitator review to prove
the actual service call, RBAC, review route, and evaluation claim.
