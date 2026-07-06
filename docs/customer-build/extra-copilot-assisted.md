---
title: "Copilot-Assisted Build"
parent: Customer Build Track
nav_order: 80
description: Use Copilot with MCP and skills to rebuild one scenario artifact from current Foundry guidance.
---

# Customer Build · Copilot-Assisted Build

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Copilot-Assisted Build" artifact="A before/after build artifact showing Copilot used current docs and skills for YOUR scenario instead of guessing." next="Use this as a learning accelerator after you have built at least one thing manually." %}

This deepener is mutuated from [Extra · Copilot-Assisted Build](../challenges/extra-copilot-assisted) — same MCP-and-skills workflow, but aimed at one artifact from your scenario in [Define your outcome](../customer-outcome). This is an OPTIONAL deepener. It is best after you have felt the manual path and can judge whether Copilot is improving it.

> Before you start this deepener: have live infrastructure and at least one challenge artifact you understand. If your team is still defining the outcome or debugging basics, skip this until later.

---

## Step 1 — Confirm the Copilot enablement layer is live

**Why it matters for your app:** Copilot can only build safely if it sees the repo instructions, MCP servers, and the right Foundry skill for the task.

**Does this apply to you?** → Skip it if your editor cannot use Copilot, MCP, or `npx` during the event.
- Build it if you want Copilot to generate or modify Foundry code for your scenario.
- Adapt it if only one teammate has the full setup and will drive the assisted build.

**Decisions to make:**
- Which challenge artifact from your scenario is worth rebuilding?
- Which MCP server and skill map to that artifact?
- What current API surface must Copilot verify before writing code?

**Apply it to your app:** verify the MCP servers, repo instructions, and the matching skill before prompting for code. → [Extra · Copilot-Assisted Build — Step 1](../challenges/extra-copilot-assisted#step-1--confirm-the-copilot-enablement-layer-is-live)

**Prove you applied it:**
- □ The relevant MCP servers show connected in the editor.
- □ You can name the skill that maps to your chosen artifact.
- □ Your prompt will require docs/MCP lookup before implementation.

**Stuck?** [Northfield Step 1](../challenges/extra-copilot-assisted#step-1--confirm-the-copilot-enablement-layer-is-live).

---

## Step 2 — Pick a challenge and rebuild it agent-assisted

**Why it matters for your app:** the useful lesson is not "Copilot wrote code"; it is whether Copilot used current sources to build your real artifact faster or better.

**Does this apply to you?** → Skip it if you do not yet have a manual baseline to compare against.
- Build it if you can choose one concrete artifact: agent create, tool attach, evaluator, hosted agent, or UI slice.
- Adapt it if Copilot should refactor or harden an existing scenario file instead of starting fresh.

**Decisions to make:**
- Which manual artifact will you rebuild?
- What scenario-specific inputs must the prompt include: users, corpus, action candidates, safety boundaries, env names?
- What acceptance check proves the generated artifact works?

**Apply it to your app:** prompt Copilot to search first, load the matching skill, and implement against your real `.env` contract. → [Extra · Copilot-Assisted Build — Step 2](../challenges/extra-copilot-assisted#step-2--pick-a-challenge-and-rebuild-it-agent-assisted)

**Prove you applied it:**
- □ The prompt explicitly required docs/MCP lookup before code.
- □ The generated artifact uses your scenario names and authoritative env variables.
- □ The artifact runs or demonstrates successfully against your project.

**Stuck?** [Northfield Step 2](../challenges/extra-copilot-assisted#step-2--pick-a-challenge-and-rebuild-it-agent-assisted).

---

## Step 3 — Prove grounding beats guessing

**Why it matters for your app:** this is the evidence that MCP-grounded Copilot reduces stale SDK calls and hallucinated patterns.

**Does this apply to you?** → Skip it if you cannot capture or compare the grounded and ungrounded outputs.
- Build it if your readout includes how the team used Copilot responsibly.
- Adapt it if the comparison is a code review note rather than a live demo.

**Decisions to make:**
- Which API detail is likely to drift and therefore worth checking?
- What under-specified prompt will serve as the "guessing" contrast?
- How will you summarize the difference for non-technical stakeholders?

**Apply it to your app:** compare a grounded Copilot output with a guessing-prone one and document the corrected API detail. → [Extra · Copilot-Assisted Build — Step 3](../challenges/extra-copilot-assisted#step-3--prove-grounding-beats-guessing)

**Prove you applied it:**
- □ You captured a concrete API or pattern difference.
- □ You can explain why the grounded result is safer or more current.
- □ The comparison is tied to your scenario artifact, not a generic sample.

**Stuck?** [Northfield Step 3](../challenges/extra-copilot-assisted#step-3--prove-grounding-beats-guessing).

---

## Deepener end-state

You have evidence that Copilot, MCP, and skills improved one real build artifact. Deepeners are optional; return to the [Customer Build Track](../customer-build) and use this workflow where it saves time without hiding understanding.
