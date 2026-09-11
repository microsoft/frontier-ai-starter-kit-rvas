# Fictional sample data

These files are safe workshop fixtures for **Northstar Outdoor Supply**, a fictional retailer. They
contain no customer, employee, tenant, account, or production operational data.

`source-manifest.json` supplies metadata for the model-comparison context. Each document also
repeats its source ID, owner, date, classification, and access groups in reviewable front matter.

| Source ID | File | Access group | Demonstrates |
|---|---|---|---|
| `RET-POL-2026-01` | `returns-policy.md` | coordinators, supervisors | approved standard policy |
| `RET-EXC-2026-01` | `returns-exceptions.md` | coordinators, supervisors | authorized exception handling |
| `SVC-ALPINE-2026-02-03` | `service-update.md` | coordinators, supervisors | freshness and superseded guidance |
| `RET-SUP-2026-01` | `returns-supervisor-playbook.md` | supervisors only | confidential escalation procedure |

The groups are fictional role labels, not directory groups. `compare_models.py` includes a source
only when the case has a listed access group. This scopes its prompt context; it does not configure
Azure permissions. The blob ingestion script does not translate this manifest into ACLs.

## Golden questions and access cases

`../golden-questions.json` defines each test case, expected citation IDs, role, pass condition,
and refusal reason. It covers routine policy, exceptions, freshness, confidential-source access,
prohibited data, and insufficient evidence. The comparison and retrieval scripts call Azure services.
The service notice marks an older notice as superseded, but the corpus does not include that older
document. It cannot test ranking between two competing notices.

## Required swaps before a customer pilot

- Use approved customer source content in the customer's environment, never in this repository.
- Set the storage, knowledge-base, and deployment values in the local `.env` contract.
- Map approved identities to real source permissions and verify them after ingestion.
- Rebuild the golden dataset with customer reviewers and access-denied cases.

Upload only the four source documents listed in the manifest; this README is not corpus content.
