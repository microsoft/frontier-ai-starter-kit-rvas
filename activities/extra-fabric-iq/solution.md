# Implementation notes — Fabric IQ real-time grounding

Use these notes when a scenario needs live Fabric/OneLake grounding through a Fabric IQ data agent.
Fabric IQ handles live Fabric source routing. Governed Data Copilot handles allowlisted
structured-data access and provenance.

## Core idea

Document RAG has limits. For *right-now* questions, use a live operational store (OneLake), rather
than a re-indexed document. The agent must route each question to the FAQ knowledge base or Fabric
tool. Demonstrate that by changing a seat count between two questions with **no re-index**.

## Infra to pre-provision (do this BEFORE the session)

1. **Fabric capacity** — an appropriate Fabric capacity or trial capacity assigned to a
   workspace. This is the gate; without it the module is impossible.
2. **OneLake lakehouse** (e.g. `sample_ops`) with a **`course_seats`** table:
   `course_code, section, capacity, enrolled, seats_open, updated_at`. Seed a handful of rows incl.
   **CS101** with a small `seats_open` (so you can drive it to 0 live for the demo).
3. A **Fabric IQ data agent** configured for the OneLake source, plus the current Foundry
   server-side-tool and user OAuth/sign-in setup.
4. Confirm each invoking user has the required Fabric license and Fabric permissions. Fabric IQ requests
   run in the signed-in user's context and honor Fabric governance; a Foundry project managed identity
   alone does not grant table access.

Fabric F-SKU bills while running. Pause the capacity when the session ends.

## Search-Before-Implement (mandatory here)

Foundry's Fabric IQ integration is **preview** and can change frequently. Query `foundry-mcp` and
`microsoft-docs` through the `foundry-toolboxes` skill for the **current** Fabric tool signature
before coding. Do **not** use a hard-coded class name; it may be stale by event day.

## Implementation notes by step

### Step 1 — see the live row
- If a team can't preview the table, it's often a **capacity not running**, missing Fabric license, or
  missing user access problem. Check the capacity is on and the signed-in user is entitled to the item.

### Step 2 — attach the tool
- **Pitfall:** teams drop the AI Search tool when adding Fabric. They must keep **both** — the routing
  rule only works if both sources are attached.
- **Pitfall:** vague system instructions. The routing rule must name the trigger words
  ("seats / capacity / right now / wait time" → Fabric). Without it the model guesses and sometimes
  answers seat questions from stale FAQ text.

### Step 3 — the money shot
- Run the demo yourself: open Fabric, run
  `UPDATE course_seats SET seats_open = 0 WHERE course_code='CS101'`, then have the team re-ask. The
  answer changes to "no seats" with no re-index.
- Verify the policy question still cites the **FAQ corpus** — if it routes to Fabric, the instructions
  need tightening.

## Verification

Grounding correctness here depends on **live, mutating** external data and a preview tool surface, so a
portal/transcript checkpoint is the honest check. Verify by: (1) two CS101 transcripts straddling a data
change showing the number moved, and (2) one policy answer still citing the FAQ knowledge base.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "Tool not found" at attach | stale/preview class name | re-query `foundry-mcp`/`microsoft-docs` for current signature |
| Seat answer never changes | answered from FAQ index, not Fabric | tighten routing rule; confirm Fabric tool actually attached |
| Can't preview table | capacity paused, missing license, or missing user access | start capacity; confirm Fabric license and user permissions |
| Policy Q hits Fabric | over-broad routing rule | scope Fabric to availability/real-time keywords only |
