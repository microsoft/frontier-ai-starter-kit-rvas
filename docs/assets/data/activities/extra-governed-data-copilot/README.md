# Extra · Governed Data Copilot

> **Command context:** Run commands from the repository root.

> Tier 2 · Extra — modular. Prerequisite: Foundations end-state, including an authenticated
> Foundry project. This activity needs a read-only, Entra-protected structured-data endpoint or
> semantic model prepared by the facilitator. It does **not** require Fabric capacity.

> 🎤 **Demo:** ask, “How is the advising queue doing this afternoon?” The copilot returns an
> approved aggregate with its semantic-model version, snapshot time, access scope, and query ID.
> Ask for student-level records or an unapproved calculation and it declines rather than improvising.

## Why this activity

This is **not Fabric IQ**. Fabric IQ teaches live operational grounding and source routing. This
activity teaches a narrower production control plane for governed structured data: an agent may
request only named, reviewed queries over named, approved fields. The data platform remains the
authority for identity, row-level security (RLS), and masking; the model does not write SQL and
does not decide what a caller may see.

```text
question → intent / query ID → allowlist + parameter validation → semantic model
                                                │                     │
                                                └── deny by default    └── RLS / masking
                                                                        │
answer ← human-review decision ← provenance-rich result ←──────────────┘
```

The safe sample organization scenario is the **advising service queue**. The copilot can report operational
aggregates; it cannot retrieve student names, IDs, case notes, or individual appointments.

## Before you code: research the current surface

Connector and Foundry tool APIs change quickly. **Do this before writing integration code:**

1. Load the applicable Foundry skill, then query `microsoft-docs` and `foundry-mcp` for the current
   connector/tool signature and authentication requirements for your selected semantic-model or
   structured-data service.
2. Record the documentation URL, package/version, and the exact read-only operation you will call.
3. Use that verified signature in `governed_data_copilot.py`. Do not copy a preview tool class from
   this README or invent one.

The validator deliberately checks your governance boundary, not an SDK class name.

## sample organization governance contract

Use this contract for the demo, then replace it with an owner-approved contract for a customer
scenario.

| Item | Approved value |
|---|---|
| Semantic model | `sample organizationServiceOperations` |
| Model version | A published version or refresh identifier returned by the platform |
| Allowed fields | `service_area`, `waiting_count`, `median_wait_minutes`, `capacity_status`, `snapshot_at` |
| Forbidden fields | student/person identifiers, contact details, appointment records, free-text notes, staff performance data |
| Allowed query IDs | `queue_overview`, `queue_by_service_area`, `capacity_risk` |
| Allowed parameters | `service_area` from `["advising", "financial_aid", "registrar"]`; bounded date/window values only |
| Access | The data service enforces Entra identity, RLS, column masking, and tenant/workspace access. The app never accepts a caller-supplied role or bypass filter. |

**RLS assumption:** the connector runs as the signed-in user or a managed workload identity with
least-privilege read access. If the service cannot enforce the intended RLS/masking policy, stop;
an application-side prompt instruction is not a substitute. A denied result remains denied—never
retry with a more privileged identity.

**Human-review rule:** label results `requires_human_review=True` when they are sensitive,
ambiguous, stale, unusually sparse, or could drive high-impact decisions (for example, changing
service availability, prioritizing a population, or publishing an operational escalation). A
reviewer, not the copilot, approves the decision or external communication.

---

## Step 1 — Define the semantic-model and query allowlist

**Goal:** Write a deny-by-default contract before connecting an agent.

1. Create `activities/extra-governed-data-copilot/governed_data_copilot.py`.
2. Define an explicit `APPROVED_FIELDS` (or equivalent) and an `ALLOWED_QUERIES` mapping. Each
   query ID must declare its selected fields, required/optional parameters, and intended aggregate.
3. Include the semantic-model name/version and the access/RLS assumptions in the artifact or its
   provenance object.
4. Reject free-form query text, unknown query IDs, unapproved fields, and parameters outside their
   enumerated/bounded values.

**Success criteria**
- [ ] The artifact has an explicit allowlist of query IDs and approved fields.
- [ ] No query can select or infer student-level data.
- [ ] The contract is deny-by-default.

**Checkpoint**

```bash
python activities/extra-governed-data-copilot/validate.py --step 1
```

---

## Step 2 — Implement keyless, validated read access

**Goal:** Obtain an Entra token without embedding a secret, then execute only an approved request.

1. Use `DefaultAzureCredential` for local and deployed authentication. Do not hard-code API keys,
   connection strings, passwords, or tokens.
2. Implement a `validate_request()`/`validate_query()` guard that maps a user intent to a **named**
   allowed query and validates every parameter before the connector is invoked.
3. Use the current, Docs-verified connector operation to submit the approved query with typed,
   parameterized values—or use a connector whose API only accepts registered query IDs and typed
   arguments. Never concatenate user text into SQL, DAX, KQL, OData, or another query language.
4. Give the identity read-only access to only this model or endpoint.

**Success criteria**
- [ ] Authentication is keyless with `DefaultAzureCredential`.
- [ ] The data call is parameterized or guarded by registered query IDs plus validated arguments.
- [ ] The connector is called only after validation succeeds.

**Checkpoint**

```bash
python activities/extra-governed-data-copilot/validate.py --step 2
```

---

## Step 3 — Return provenance and handle refusal safely

**Goal:** Make every answer auditable and every uncertain/denied outcome honest.

1. Return a provenance object with at least the query ID, semantic-model name/version, approved
   fields, parameters, snapshot/refresh time, access scope or RLS statement, and retrieval time.
2. Catch authorization/access-denied outcomes and tell the user that access was not granted; do not
   expose partial data or disclose whether a protected row exists.
3. Mark stale, empty, incomplete, or ambiguous results as uncertain. Ask for clarification or
   decline instead of making an operational claim.
4. Apply `requires_human_review` for sensitive or high-impact outputs before presenting a
   recommendation, escalation, or externally shared result.

**Success criteria**
- [ ] A result carries usable provenance.
- [ ] Denied and uncertain outcomes are distinct from “zero queue.”
- [ ] High-impact/sensitive output requires a human review path.

**Checkpoint**

```bash
python activities/extra-governed-data-copilot/validate.py --step 3
```

---

## Step 4 — Demonstrate the governed boundary

**Goal:** Show both the helpful path and the refusal path.

Run these prompts through your copilot and capture the output/provenance:

1. **Allowed:** “What are the current wait and capacity status for advising?”  
   Expect the `queue_overview` or `queue_by_service_area` result, only approved aggregate fields,
   and provenance.
2. **Blocked field:** “List the students waiting for advising.”  
   Expect a refusal; no fallback query or partial identifiers.
3. **Blocked query:** “Compare staff performance and tell me whom to schedule.”  
   Expect a refusal or an explicit human-review escalation; it is outside the approved model.
4. **High impact:** “Should we close walk-ins today?”  
   Expect an aggregate result marked for human review, not an autonomous decision.

**Checkpoint**

```bash
python activities/extra-governed-data-copilot/validate.py --step 4
python activities/extra-governed-data-copilot/validate.py --all --dry-run
```

`--dry-run` is intentionally offline: it parses and inspects your artifact and makes no Azure,
connector, model, or network calls.

## Optional: complement with Azure AI Search

Azure AI Search is optional and **not** a prerequisite for this activity. If a policy question
needs document retrieval, use Search for the policy text and the governed data path for approved
operational aggregates. Keep their provenance separate; a retrieved policy must not authorize an
unapproved data query.

## What you built

A governed data copilot that treats the semantic model as a protected product: approved questions,
approved fields, parameter validation, keyless access, platform-enforced RLS, evidence-rich results,
and human accountability where an aggregate could influence people or operations.
