# Content Understanding — the reviewable document workflow

Build a controlled document-to-decision path for invoices, RFQs, or specifications: a typed,
evidence-backed, human-reviewed result — not an autonomous business decision and not a generic OCR
demo. This is a practical, opinionated build course. Each module names the Microsoft options, picks a
default, implements the default path or contract, and names the seam for swapping to another
approved option.

The quality bar and reference format are the [Foundations activity](activity.html?id=foundations)
and the AI Grounding scenario lessons. The scenario reference contract lives in
[`accelerator/solution.md`](accelerator/solution.md).

## The seven modules

| # | Module | You decide | Checkpoint |
| --- | --- | --- | --- |
| 1 | [Provision the foundation](lesson.html?scenario=content-understanding-document-workflow&lesson=foundation) | How to stand up a keyless Foundry account with Content Understanding, Document Intelligence, models, and document storage | `verify_foundation.py` |
| 2 | [Connect an approved source](lesson.html?scenario=content-understanding-document-workflow&lesson=document-source) | Azure Blob, ADLS Gen2, SharePoint, or OneLake — and the intake/quarantine controls | `verify_document_source.py` |
| 3 | [Select the extraction capability](lesson.html?scenario=content-understanding-document-workflow&lesson=extraction-selection) | CU prebuilt/custom analyzer, DI prebuilt/custom model, LLM structured outputs, or multimodal | `verify_extraction_selection.py` |
| 4 | [Typed extraction with evidence](lesson.html?scenario=content-understanding-document-workflow&lesson=typed-extraction) | How to normalize output into one validated contract with confidence + grounding | `verify_typed_extraction.py` |
| 5 | [Review, correction, and handoff](lesson.html?scenario=content-understanding-document-workflow&lesson=human-review) | Action-tool handoff, a review app, or a workflow handoff | `verify_human_review.py` |
| 6 | [Evaluate and trace](lesson.html?scenario=content-understanding-document-workflow&lesson=prove-and-observe) | Foundry evaluators, an offline harness, and an adversarial pass, against a gate | `verify_prove_and_observe.py` |
| 7 | [Deploy the workflow](lesson.html?scenario=content-understanding-document-workflow&lesson=deploy) | Hosted agent, container app, or an API behind APIM | `verify_deploy.py` |

Each lesson follows the same contract: **What you build · Choose your path · Implementation · Verify ·
Troubleshooting · Decision record · Next module.** Modules build on the previous one — module N's
checkpoint is module N+1's prerequisite.

## Decision gates to carry into the customer conversation

Use these gates before opening reference-library mechanics:

| Gate | Decide before building |
|---|---|
| Document boundary | Which document types are approved, who owns them, and what retention/access rules apply? |
| Extraction boundary | Which fields need evidence, confidence, normalization, and missing-value behavior? |
| Review boundary | Who corrects low-confidence or conflicting values, and what evidence must they see? |
| Handoff boundary | Which downstream action is allowed, approval-gated, queued, or explicitly out of scope? |
| Trust boundary | Which extraction, prompt-injection, review-routing, and deployment-access failures block a pilot? |

## Canonical activities

The scenario supplies document-specific decisions, contracts, and evidence gates, and **links** to the
canonical activities for shared mechanics rather than duplicating them:

- [Foundations](activity.html?id=foundations) — provisioning and the `.env` contract.
- [Document Workflow](activity.html?id=extra-document-workflow) — extraction implementation.
- [Action Tools](activity.html?id=advanced-action-tools) — the governed handoff seam.
- [Evaluation & Red Teaming](activity.html?id=advanced-evaluation-redteam) and
  [Tracing & Observability](activity.html?id=advanced-tracing-observability) — the gate and traces.
- [Deploy as a Hosted Agent](activity.html?id=advanced-deploy-hosted-agent) — the pilot endpoint.

## Get started

```bash
# 1. Provision the optional clean-subscription foundation (no inline secrets, keyless-first)
./accelerator/scripts/deploy.sh rg-content-understanding eastus2

# 2. Work through the modules; each has an offline checkpoint you can run now
python3 accelerator/scripts/verify_foundation.py --offline
python3 accelerator/scripts/verify_document_source.py --offline
# ... through verify_deploy.py

# 3. Validate the whole scenario contract and synthetic pack, no network
python3 validate.py
```

API facts (API versions, model ids, SDK packages) are cited inline in each lesson and in
[`accelerator/solution.md`](accelerator/solution.md). Re-check current Microsoft Learn guidance
before writing SDK code.

## Non-negotiable boundaries

- **Synthetic data only.** The fixtures under [`accelerator/sample-data/README.md`](accelerator/sample-data/README.md)
  are fictional. Real deployable infrastructure is fine; real customer documents are not, until a
  source owner, security owner, and retention policy approve a separate path.
- **Keyless-first.** `DefaultAzureCredential` + managed identity + Entra RBAC. No keys in code, `.env`,
  or Bicep.
- **Evidence, never inference.** Every extracted value keeps its confidence and grounding; a value
  without evidence is rejected and a missing value is surfaced for review, never guessed.
- **Prompt Flow is banned** in this curriculum — use agents + tools + MCP instead.
