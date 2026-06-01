# Coach Guide · Extra — Fabric IQ (Real-Time Data Grounding)

> **Coach-only.** This Extra has the **heaviest infra dependency** of any Extra. If Fabric capacity
> isn't provisioned, **do not start it** — redirect the team to Voice Live or Magentic. The whole point
> is *live* data, which you cannot fake with the static index.

## What this challenge is really teaching

The limit of document RAG. Students who've only done Foundations Step 4 believe "grounding = search an
index." This Extra reframes grounding as **"connect the agent to the right source of truth"** — and for
*right-now* questions that source is a live operational store (OneLake), not a re-indexed document. The
keeper insight is **source routing**: the agent must choose FAQ-knowledge-base vs Fabric-tool per
question. The demo lands when the seat count changes between two asks with **no re-index**.

## Infra to pre-provision (do this BEFORE the session)

1. **Fabric capacity** — an **F-SKU** (F2 is enough) or a **Fabric trial** capacity assigned to a
   workspace. This is the gate; without it the Extra is impossible.
2. **OneLake lakehouse** (e.g. `northfield_ops`) with a **`course_seats`** table:
   `course_code, section, capacity, enrolled, seats_open, updated_at`. Seed a handful of rows incl.
   **CS101** with a small `seats_open` (so you can drive it to 0 live for the demo).
3. A **Fabric data-agent / Fabric IQ connection** the Foundry project can reach, plus the
   connection string / endpoint to hand teams in Step 2.
4. Confirm the Foundry project's **managed identity** (keyless) or the supplied connection has read access
   to the lakehouse.

> **Cost/capacity flag for the coordinator:** Fabric F-SKU bills while running — **pause the capacity**
> when the session ends. A single shared capacity can serve all teams; they only need read access.

## Search-Before-Implement (mandatory here)

The Fabric tool class + constructor are **preview** and rename frequently. Tell teams to query
`foundry-mcp` and `microsoft-docs` (the `foundry-toolboxes` skill) for the **current** Fabric tool
signature before coding. Do **not** hand them a hard-coded class name — it will likely be stale by event
day. That's the doctrine the whole curriculum teaches; this Extra is where it bites hardest.

## Per-step facilitation

### Step 1 — see the live row
- If a team can't preview the table, it's almost always a **capacity not running** or **no read access**
  problem. Check the capacity is *on* and the project identity is granted on the lakehouse.

### Step 2 — attach the tool
- **Pitfall:** teams drop the AI Search tool when adding Fabric. They must keep **both** — the routing
  rule only works if both sources are attached.
- **Pitfall:** vague system instructions. The routing rule must name the trigger words
  ("seats / capacity / right now / wait time" → Fabric). Without it the model guesses and sometimes
  answers seat questions from stale FAQ text.

### Step 3 — the money shot
- Drive the demo yourself: open Fabric, run
  `UPDATE course_seats SET seats_open = 0 WHERE course_code='CS101'`, then have the team re-ask. The
  answer flips to "no seats" with no re-index. That contrast *is* the learning outcome.
- Verify the policy question still cites the **FAQ corpus** — if it routes to Fabric, the instructions
  need tightening.

## Why no `validate.py`

Grounding correctness here depends on **live, mutating** external data and a preview tool surface, so a
portal/transcript checkpoint is the honest check. Verify by: (1) two CS101 transcripts straddling a data
change showing the number moved, and (2) one policy answer still citing the FAQ knowledge base.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "Tool not found" at attach | stale/preview class name | re-query `foundry-mcp`/`microsoft-docs` for current signature |
| Seat answer never changes | answered from FAQ index, not Fabric | tighten routing rule; confirm Fabric tool actually attached |
| Can't preview table | capacity paused / no RBAC | start capacity; grant project MI read on lakehouse |
| Policy Q hits Fabric | over-broad routing rule | scope Fabric to availability/real-time keywords only |
