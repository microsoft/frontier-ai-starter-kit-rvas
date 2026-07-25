# Content Understanding — the reviewable document workflow

Build a controlled document-to-decision path for invoices, RFQs, or specifications: a typed,
evidence-backed, human-reviewed result — not an autonomous business decision and not a generic OCR
demo. This is a practical, opinionated build course. Each module names the Microsoft options, picks a
default, implements the default path or contract, and names the seam for swapping to another
approved option.

The quality bar and reference format are the [Foundations activity](../../activities/foundations/README.md)
and the AI Grounding scenario lessons. The scenario reference contract lives in
[`accelerator/solution.md`](accelerator/solution.md).

## The seven modules

| # | Module | You decide | Checkpoint |
| --- | --- | --- | --- |
| 1 | [Provision the foundation](lessons/01-provision-foundation.md) | How to stand up a keyless Foundry account with Content Understanding, Document Intelligence, models, and document storage | `verify_foundation.py` |
| 2 | [Connect an approved source](lessons/02-document-source.md) | Azure Blob, ADLS Gen2, SharePoint, or OneLake — and the intake/quarantine controls | `verify_document_source.py` |
| 3 | [Select the extraction capability](lessons/03-extraction-selection.md) | CU prebuilt/custom analyzer, DI prebuilt/custom model, LLM structured outputs, or multimodal | `verify_extraction_selection.py` |
| 4 | [Typed extraction with evidence](lessons/04-typed-extraction.md) | How to normalize output into one validated contract with confidence + grounding | `verify_typed_extraction.py` |
| 5 | [Review, correction, and handoff](lessons/05-human-review.md) | Action-tool handoff, a review app, or a workflow handoff | `verify_human_review.py` |
| 6 | [Evaluate and trace](lessons/06-prove-and-observe.md) | Foundry evaluators, an offline harness, and an adversarial pass, against a gate | `verify_prove_and_observe.py` |
| 7 | [Deploy the workflow](lessons/07-deploy.md) | Hosted agent, container app, or an API behind APIM | `verify_deploy.py` |

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

- [Foundations](../../activities/foundations/README.md) — provisioning and the `.env` contract.
- [Document Workflow](../../activities/extra-document-workflow/README.md) — extraction implementation.
- [Action Tools](../../activities/advanced-action-tools/README.md) — the governed handoff seam.
- [Evaluation & Red Teaming](../../activities/advanced-evaluation-redteam/README.md) and
  [Tracing & Observability](../../activities/advanced-tracing-observability/README.md) — the gate and traces.
- [Deploy as a Hosted Agent](../../activities/advanced-deploy-hosted-agent/README.md) — the pilot endpoint.

## Get started

```bash
# 1. Provision the optional clean-subscription foundation (no inline secrets, keyless-first)
./accelerator/scripts/deploy.sh rg-content-understanding eastus2

# 2. Work through the modules; each has an offline checkpoint you can run now
python3 accelerator/scripts/verify_foundation.py --offline
python3 accelerator/scripts/verify_document_source.py --offline
# ... through verify_deploy.py

# 3. Validate the synthetic pack end-to-end, no network
python3 scripts/validate_local_pack.py
```

Verified API facts (API versions, model ids, SDK packages) were fetched from learn.microsoft.com on
**2026-07-24** and are cited inline in each lesson and in [`accelerator/solution.md`](accelerator/solution.md).

## Non-negotiable boundaries

- **Synthetic data only.** The fixtures under [`accelerator/sample-data/README.md`](accelerator/sample-data/README.md)
  are fictional. Real deployable infrastructure is fine; real customer documents are not, until a
  source owner, security owner, and retention policy approve a separate path.
- **Keyless-first.** `DefaultAzureCredential` + managed identity + Entra RBAC. No keys in code, `.env`,
  or Bicep.
- **Evidence, never inference.** Every extracted value keeps its confidence and grounding; a value
  without evidence is rejected and a missing value is surfaced for review, never guessed.
- **Prompt Flow is banned** in this curriculum — use agents + tools + MCP instead.
