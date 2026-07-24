---
title: "Extra: Governed Data Copilot · Facilitator"
parent: Build Modules
nav_order: 126
nav_exclude: true
---

# Facilitator Guide · Extra — Governed Data Copilot

> **Command context:** Run all commands from the repository root.

> **Facilitator-only.** This session is about a governed semantic-model boundary, not a general
> database chatbot. Do not permit a connection that lets learners issue arbitrary SQL/DAX/KQL or
> access row-level student data.

## What this activity is really teaching

Fabric IQ answers “what is happening live?” from Fabric/OneLake. This Extra answers a different
question: “what may this copilot ask, for whom, and how can a person audit the answer?” Learners
practice named query allowlists, approved fields, typed inputs, platform-enforced RLS/masking,
provenance, and human review. The key learning is **deny by default**: natural language is not a
data-access policy.

The Northfield demo uses aggregate advising service-queue status. It deliberately excludes student
identity, free-text notes, appointment details, and staff-performance information.

## Prerequisites and pre-session setup

1. A Foundry project and an Entra-authenticated learner/workload identity. Learners need local
   `az login`; deployed demos should use a managed identity.
2. A read-only semantic model or structured-data endpoint containing an aggregate-only
   `NorthfieldServiceOperations` view. Seed fields: `service_area`, `waiting_count`,
   `median_wait_minutes`, `capacity_status`, and `snapshot_at`.
3. Platform configuration that enforces tenant/workspace access, RLS, and column masking. Test the
   learner identity: it must not be able to retrieve student-level fields even if it changes a client
   request.
4. An approved set of registered operations or a connector that supports typed, parameterized
   requests. If the platform cannot offer one, pre-create a minimal read-only query facade; do not
   expose a raw query endpoint for the workshop.
5. A current connector choice. Before the session, search `microsoft-docs` and `foundry-mcp`, then
   load the matching Foundry skill to verify the connector/tool signature. Give learners the research
   task and current docs link—not a pasted preview class name.

Azure AI Search is optional. It can retrieve the policy that describes queue handling, but is neither
required nor an authorization mechanism for the structured-data path.

## Expected learner artifacts

- `activities/extra-governed-data-copilot/governed_data_copilot.py`
  - `DefaultAzureCredential` keyless authentication
  - explicit query allowlist and approved field allowlist
  - parameterized or registered-query validation before execution
  - provenance carrying query/model/version/snapshot/access context
  - explicit access-denied and uncertainty handling
  - `requires_human_review` path for sensitive/high-impact output
- A short capture of the four Step 4 prompts: one approved aggregate, blocked field request, blocked
  query, and high-impact question routed to review.
- Learner notes containing the current Docs/MCP source and verified connector operation.

Run the offline checkpoint with:

```bash
python activities/extra-governed-data-copilot/validate.py --all --dry-run
```

## Facilitation flow

### Step 1 — make the contract visible

Ask learners to read their allowlist aloud. Challenge it with “show me the student names” and “add a
staff-performance calculation.” They should identify the unknown query/field as a denial before any
connector call. Point out that prompt wording does not enforce RLS.

### Step 2 — verify the identity boundary

Have learners show `DefaultAzureCredential`, the current Docs/MCP result, and the named-query guard.
Ask which identity is used locally versus deployed. Confirm that the connector is read-only and
platform RLS/masking is active. A failure must remain an access denial; “try the admin key” is a
failed design.

### Step 3 — inspect evidence, not prose

Require provenance in the output: registered query ID, semantic model and version, validated
arguments, snapshot time, access/RLS statement, and retrieval time. Make an incomplete or stale
response visibly uncertain rather than equivalent to an empty queue.

### Step 4 — run the boundary demo

The positive demo is “How is advising doing this afternoon?” The answer should contain only the
approved aggregate. Then drive the three negative/high-impact prompts from the activity README.
For “Should we close walk-ins?” insist the response presents evidence only and is marked for human
review; the agent must not make the operational decision.

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Learner asks arbitrary SQL/DAX | raw endpoint or over-broad tool | replace with registered query IDs and typed parameters; deny unknown requests |
| App prompt says “respect RLS” but records appear | RLS/masking not configured at platform | stop the demo; enforce data-plane identity, RLS, and masking before continuing |
| 403 becomes a retry with a stronger credential | confused operational convenience with authorization | return neutral access-denied outcome; use least privilege and correct role assignment |
| “No data” is reported as zero queue | stale/partial/error response collapsed into a value | add uncertainty handling and snapshot freshness checks |
| Output has a number but no evidence | provenance discarded during response shaping | preserve query ID, model/version, fields, parameters, snapshot, access scope, retrieval time |
| Agent recommends closing a service | high-impact decision not gated | mark `requires_human_review`; a designated operator decides |
| Connector code fails on event day | copied a stale preview signature | repeat Docs/MCP search and update only the adapter |

## Validator limitations

`validate.py` is intentionally static and offline. It parses and searches
`governed_data_copilot.py`; it makes no Azure, semantic-model, Foundry, or network calls and does not
require SDK packages. It can confirm the presence of governance-shaped code, but cannot prove that:

- the current connector signature works;
- the deployed identity truly has least privilege;
- RLS, masking, or registered operations are enforced by the data platform;
- provenance values are truthful or complete at runtime; or
- a human actually reviewed a high-impact result.

Treat a passing validator result as a checkpoint, then verify the identity, access policy, approved
operations, and four-prompt demo in the real environment.
