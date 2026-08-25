# Content Understanding: turn documents into reviewable decisions

Build a controlled path from an invoice, RFQ, or specification to a typed result that a person can
check. The workflow keeps the source evidence and stops before making a business decision on its own.
Each module compares the available Microsoft options, recommends a default, and shows where another
approved service can be swapped in.

The quality bar and reference format are the [Foundations activity](activity.html?id=foundations)
and the AI Grounding scenario lessons. The scenario reference contract lives in
[`accelerator/solution.md`](accelerator/solution.md).

## The seven modules

| Module | You decide | Outcome |
|---|---|---|
| [1. Provision the foundation](lesson.html?scenario=content-understanding-document-workflow&lesson=foundation) | How to stand up a keyless Foundry account with Content Understanding, Document Intelligence, models, and document storage | Foundations Step 1 |
| [2. Connect an approved source](lesson.html?scenario=content-understanding-document-workflow&lesson=document-source) | Azure Blob, ADLS Gen2, SharePoint, or OneLake — and the intake/quarantine controls | Approved intake and document-retention design |
| [3. Select the extraction capability](lesson.html?scenario=content-understanding-document-workflow&lesson=extraction-selection) | CU prebuilt/custom analyzer, DI prebuilt/custom model, LLM structured outputs, or multimodal | Document capability and implementation decision |
| [4. Typed extraction with evidence](lesson.html?scenario=content-understanding-document-workflow&lesson=typed-extraction) | How to normalize output into one validated contract with confidence + grounding | Structured extraction result and low-confidence failure path |
| [5. Review, correction, and handoff](lesson.html?scenario=content-understanding-document-workflow&lesson=human-review) | Action-tool handoff, a review app, or a workflow handoff | Reviewer correction and approval trace |
| [6. Evaluate and trace](lesson.html?scenario=content-understanding-document-workflow&lesson=prove-and-observe) | Foundry evaluators, an offline harness, and an adversarial pass, against a gate | Scenario evaluation gate and trace review |
| [7. Deploy the workflow](lesson.html?scenario=content-understanding-document-workflow&lesson=deploy) | Hosted agent, container app, or an API behind APIM | Controlled pilot deployment |

Each lesson tells you what to build, which path to choose, how to implement it, and what evidence to
inspect. Modules build on one another, so finish them in order.

## Decision gates to carry into the customer conversation

Answer these questions before opening the reference library:

| Gate | Decide before building |
|---|---|
| Document boundary | Which document types are approved, who owns them, and what retention/access rules apply? |
| Extraction boundary | Which fields need evidence, confidence, normalization, and missing-value behavior? |
| Review boundary | Who corrects low-confidence or conflicting values, and what evidence must they see? |
| Handoff boundary | Which downstream action is allowed, approval-gated, queued, or explicitly out of scope? |
| Trust boundary | Which extraction, prompt-injection, review-routing, and deployment-access failures block a pilot? |

## Canonical activities

This scenario covers the document-specific decisions. It links to shared implementation activities
instead of repeating them:

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
```

Then work through the modules in order. Each **Verify** section gives you a command to run and tells
you what its output means.

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
