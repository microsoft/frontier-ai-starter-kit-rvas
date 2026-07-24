---
title: "Fabric IQ"
parent: Customer Build Track
nav_order: 76
description: Add live operational data beside your static knowledge base when the current number matters.
---

# Customer Build · Fabric IQ

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Fabric IQ" artifact="A dual-grounded agent that routes YOUR policy questions to documents and YOUR right-now questions to live data." next="Use this only when live operational state is essential to your scenario." %}

This deepener adapts [Extra · Fabric IQ](../activities/extra-fabric-iq): it uses the same live-data grounding pattern for the operational data in your scenario from [Define your outcome](../customer-outcome). Without Fabric capacity and a meaningful live table, skip it.

> Before you start this deepener: confirm facilitator-provisioned Fabric capacity, OneLake data, and a Foundry-reachable Fabric IQ connection. If your answers are document-grounded and not time-sensitive, skip this.

---

## Step 1 — Confirm your live data source in OneLake

**Why it matters for your app:** static RAG answers policy; live data answers "right now." You need a trustworthy operational table before adding a live tool.

**Does this apply to you?** → Skip it if your corpus has no live operational component.
- Build it if users ask about availability, capacity, status, inventory, SLA, queue position, or current metrics.
- Adapt it if your live source is another governed data platform, but keep the same source-of-truth discipline.

**Decisions to make:**
- Which knowledge source is live, not static?
- Which fields must the agent be allowed to query?
- What current value can you record and later prove the agent matched?

**Apply it to your app:** locate your lakehouse/table and record a current value that your assistant should answer from. → [Extra · Fabric IQ — Step 1](../activities/extra-fabric-iq#step-1--confirm-the-live-data-source-in-onelake)

**Prove you applied it:**
- [ ] You can read at least one live row for your scenario.
- [ ] You know the workspace, lakehouse, table, and key fields.
- [ ] You recorded a current value for the demo comparison.

**Stuck?** [Northfield Step 1](../activities/extra-fabric-iq#step-1--confirm-the-live-data-source-in-onelake).

---

## Step 2 — Wire the Fabric IQ tool to your agent

**Why it matters for your app:** the agent needs explicit source routing so it uses live data for current-state questions and documents for stable policy.

**Does this apply to you?** → Skip it if you cannot attach a Fabric tool in the event environment.
- Build it if your Foundry project can reach the Fabric IQ/data-agent connection.
- Adapt it if the live tool should be available only to a specialist agent, not the main assistant.

**Decisions to make:**
- Which agent gets the live tool?
- What routing rule separates policy/corpus questions from live/current questions?
- Which safety boundaries limit sensitive live data exposure?

**Apply it to your app:** attach the Fabric IQ tool alongside your existing knowledge base and update instructions with your routing rule. → [Extra · Fabric IQ — Step 2](../activities/extra-fabric-iq#step-2--wire-the-fabric-iq-tool-to-your-agent)

**Prove you applied it:**
- [ ] The agent lists both static knowledge and live data tools.
- [ ] Instructions state when to use each source.
- [ ] A test "right now" question invokes the live-data path.

**Stuck?** [Northfield Step 2](../activities/extra-fabric-iq#step-2--wire-the-fabric-iq-tool-to-your-agent).

---

## Step 3 — Prove live grounding

**Why it matters for your app:** the whole point is contrast: the answer changes when the operational source changes, without re-indexing documents.

**Does this apply to you?** → Skip it if you cannot safely mutate or observe changing data.
- Build it if your demo can show before/after values from the source of truth.
- Adapt it if you can only show two timestamps or two records instead of mutating data live.

**Decisions to make:**
- Which question proves live state better than static RAG?
- How will you change or observe the data safely?
- Which policy question proves source routing still uses your corpus?

**Apply it to your app:** ask a right-now question, compare with OneLake, change or observe the data, and ask again; then ask a policy question to prove routing. → [Extra · Fabric IQ — Step 3](../activities/extra-fabric-iq#step-3--prove-live-grounding-and-contrast-with-static-rag)

**Prove you applied it:**
- [ ] The agent's first live answer matches the table value.
- [ ] After the value changes, the answer changes without re-indexing.
- [ ] A policy question still cites your static corpus.

**Stuck?** [Northfield Step 3](../activities/extra-fabric-iq#step-3--prove-live-grounding-and-contrast-with-static-rag).

---

## Deepener end-state

You have dual grounding only if your outcome needs live operational truth. Deepeners are optional; return to the [Customer Build Track](../customer-build) and keep the demo focused.
