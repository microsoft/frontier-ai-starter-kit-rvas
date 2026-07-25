---
title: "Extra: Document Workflow · Facilitator"
parent: Build Modules
nav_order: 126
nav_exclude: true
---

# Facilitator Guide · Extra — Document Workflow

> **Command context:** Run commands from the repository root.

This is an auditable document **intake** exercise, not an automated admissions workflow. Use only
fictional sample organization applications supplied or invented for the workshop. Do not collect, upload, or
display real applicant records.

## Prerequisites

1. A Document Intelligence resource and endpoint in the event subscription, with keyless access
   configured for learner identities. Confirm the current role and regional requirements in Microsoft
   Docs before the event.
2. Learners can use `az login`; the deployment identity is managed identity where applicable.
3. A few harmless fictional PDF/image applications, including one clean case and one low-quality or
   missing-field case.
4. Network access to `microsoft-docs` MCP. Teams must search current SDK/auth/poller guidance before
   coding because the API evolves.

## Expected completion artifacts

- `document_workflow.py` using `DefaultAzureCredential` and current layout/OCR SDK syntax.
- A structured JSON intake result with field confidence, source reference, status, and review reason.
- A demonstrated human-review route and explicit reviewer approval for fictional data.
- Redacted trace/correlation evidence plus a small fictional evaluation summary (accuracy, review rate,
  reviewer overrides, and false approvals).
- Passing `python activities/extra-document-workflow/validate.py --all --path .` as a structural checkpoint.

## Common failures

| Symptom | Likely cause | Facilitation response |
|---|---|---|
| 401/403 or credential chain failure | keyless RBAC or `az login` not ready | verify identity and current Docs role guidance; do not fall back to embedding a key |
| Layout call fails or polling code is stale | copied an old SDK sample | require a fresh `microsoft-docs` MCP search and compare with the project skill reference |
| Workflow marks low-confidence fields complete | threshold is only displayed, not enforced | have the team test the blurred fictional case and route it to review |
| Review is a console message, not a decision | no approval state or queue handoff | require reviewer, reason, source reference, and explicit approve/reject transition |
| Trace contains OCR text or identifiers | overly broad logging | retain only correlation ID, timing, status, threshold version, and review reason |

## Why static validation is limited

`validate.py` intentionally performs offline AST/text heuristics. It does not install Azure packages,
authenticate, inspect a document, call a service, prove RBAC, prove a Docs search happened, verify a
real human approval, or establish that traces/evaluation values are truthful. It can catch missing
keyless/auth, confidence, review, output, and evidence signals cheaply; facilitators must verify the
live fictional demo and inspect the redacted artifacts.
