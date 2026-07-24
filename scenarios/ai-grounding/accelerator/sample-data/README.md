# Fictional sample data

These files are safe workshop fixtures for **Northstar Outdoor Supply**, a fictional retailer. They contain no customer, employee, tenant, account, or production operational data.

`source-manifest.json` is the source-of-truth metadata used by the local simulation. Each document also repeats its source ID, owner, date, classification, and access groups in reviewable front matter.

| Source ID | File | Access group | Demonstrates |
|---|---|---|---|
| `RET-POL-2026-01` | `returns-policy.md` | coordinators, supervisors | approved standard policy |
| `RET-EXC-2026-01` | `returns-exceptions.md` | coordinators, supervisors | authorized exception handling |
| `SVC-ALPINE-2026-02-03` | `service-update.md` | coordinators, supervisors | freshness and superseded guidance |
| `RET-SUP-2026-01` | `returns-supervisor-playbook.md` | supervisors only | confidential escalation procedure |

The groups are fictional role labels, not identities or directory groups. A source is included only when the simulated role has a listed access group. This demonstrates an access boundary; it does not implement a permission system.

## Golden questions and access cases

`../golden-questions.json` specifies every local test case, expected citation IDs, role, pass condition, and refusal reason. It includes routine policy, exception, freshness, confidential-source access, prohibited-data, and insufficient-evidence cases. The simulation produces evidence rather than calling an AI service.

## Required swaps before a customer pilot

## Required swaps before a customer pilot

- Replace these documents with approved customer source content.
- Replace the `customer-demo-grounding` container/source label.
- Replace the `customer-demo-iq-index` index/knowledge configuration label.
- Replace the `customer-demo-embedding-model` model/deployment label with the approved, supported choice.
- Rebuild the golden dataset with customer reviewers and access-denied cases.

The labels are illustrative only; they are not Azure resources or API values.
