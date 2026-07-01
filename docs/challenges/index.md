---
title: Challenge Library
nav_order: 6
has_children: true
---

# Challenge Library

{% include journey-status.html tone="shared" path="Challenge Library" artifact="Reusable modules for both Customer Build and Upskill tracks." next="If you are starting from scratch, go through your track page first; use this library once you know the module you need." %}

This page lists the shared modules used by both the **Customer Build Track** and **Upskill Track**.

Every route uses the same three-tier architecture:

- **Tier 1 · Foundations** is one guided, linear challenge with four ordered steps.
- **Tier 2 · Advanced** is modular: Action Tools, Evaluation, Tracing, Deploy, and Extras.
- **Tier 3 · Capstone** composes the work into a multi-agent system.

## Start from a track, not from a random page

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Customer Build</span>
    <h3><a href="{{ '/customer-build' | relative_url }}">Bring your own outcome</a></h3>
    <p>Use the canvas first, then run these challenge modules with your customer-safe data and workflow.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Idea intake</span>
    <h3><a href="{{ '/idea-forge' | relative_url }}">Need an idea?</a></h3>
    <p>Generate and pick a buildable idea, then continue into Customer Build.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Upskill</span>
    <h3><a href="{{ '/upskill' | relative_url }}">Learn with Northfield</a></h3>
    <p>Follow the known-good reference scenario through Foundations and beyond.</p>
  </div>
</div>

## Tier 1 · Foundations

One guided challenge, four ordered steps. Each step ends in a Checkpoint (`python validate.py --step N`)
that is the prerequisite for the next. **Completing Step 4 is the Foundations end-state** — the gate to
the entire Advanced tier.

For customer engagements, the Foundations outcome is not just "the validator passed"; it is "the agent
answers customer-relevant questions from trusted sources and cites them."

<div class="challenge-card" markdown="1">

| Step | Focus | Outcome |
|------|-------|---------|
| [**1 — Setup & Provisioning**](foundations#step-1--setup--provisioning-foundry--ai-search) | `azd up` (Foundry + AI Search + App Insights), keyless auth | Infrastructure live and authenticated |
| [**2 — Model & Playground**](foundations#step-2--model-selection--the-playground) | Deploy + compare models, tune system instructions | Generic answers from a model you chose |
| [**3 — Your First Agent**](foundations#step-3--your-first-agent) | Named, versioned Foundry agent with persona + guardrails | An agent that refuses out-of-scope/unsafe asks |
| [**4 — Knowledge Base (IQ)**](foundations#step-4--knowledge-base-index--foundry-iq---foundations-end-state) | Index the FAQ corpus, build Foundry IQ, attach to the agent | **Grounded answers with citations — END-STATE** |

[Start Foundations →](foundations){: .btn .btn-primary }

</div>

## Tier 2 · Advanced + Extras

Pick **any** of these in **any order**. Each one extends the same assistant and assumes the Foundations
end-state (or the bootstrap skip-path below).

<div class="challenge-card" markdown="1">

| Advanced challenge | Guided / Scratch | What it adds |
|--------------------|------------------|--------------|
| [Action Tools](advanced-action-tools) | ~45 min / ~1.5 hr | The agent **does work** — opens a ticket / places a hold / books advising via an MCP tool, with a human-approval loop |
| [Evaluation & Red Teaming](advanced-evaluation-redteam) | ~1.25 hr / ~2 hr | Proof it's accurate **and** safe — groundedness metrics + adversarial/jailbreak results, with a CI score gate |
| [Tracing & Observability](advanced-tracing-observability) | ~1 hr / ~1.5 hr | Every answer observable end-to-end — OTel GenAI spans → App Insights → KQL |
| [Deploy as a Hosted Agent](advanced-deploy-hosted-agent) | ~60–90 min / ~1.5 hr | Ship it as a containerized hosted agent with its own endpoint and per-agent identity |

Each Advanced challenge offers a **Guided** path (revised, honest time) and a longer
**Build-from-scratch** path — both graded by the same `validate.py`.

**Extras**, re-slotted by their role in the tree:

| Extra (optional) | Tree role | What it adds |
|------------------|-----------|--------------|
| [Magentic Workflows](extra-magentic-workflows) | Capstone-feeder | Multi-agent orchestration with a Magentic manager (MAF) |
| [Hosted Long-Running Agents](extra-hosted-longrunning) | Capstone-feeder | MAF + hosted long-running agent patterns |
| [Build a UI](extra-build-ui) | Capstone companion | A web front-end: streaming chat, citations panel, action-approval card |
| [Fabric IQ](extra-fabric-iq) | Deepener | Live operational data grounding via OneLake / Fabric IQ |
| [Give It a Voice](extra-voice-live) | Deepener | A spoken interface with the Voice Live API |
| [Copilot-Assisted Build](extra-copilot-assisted) | Deepener | Use microsoft/skills + MCP + `copilot-instructions.md` to build faster |

</div>

## Tier 3 · Capstone

Break the single Northfield IQ Assistant into a **multi-agent team** — a triage/router that fans out
to specialist agents and converges — orchestrated with the **Microsoft Agent Framework (MAF)**.

<div class="challenge-card" markdown="1">

| Capstone | Time | Prereqs |
|----------|------|---------|
| [Northfield IQ, the Team — Multi-Agent Orchestration](capstone-multi-agent) | 2–2.5 hr core (+1 hr Magentic stretch, +1.5 hr hosted variant) | Foundations end-state **+** Action Tools |

[Start the Capstone →](capstone-multi-agent){: .btn .btn-primary }

</div>
