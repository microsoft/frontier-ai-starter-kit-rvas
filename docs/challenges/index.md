---
title: Challenges
nav_order: 4
has_children: true
---

# Challenges

This hackathon is a **tree of three tiers**. **Tier 1 · Foundations** is one guided, linear challenge
— four ordered steps everyone completes. **Tier 2 · Advanced** is a set of modular, self-contained
challenges (plus Extras) you can attempt **in any order**. **Tier 3 · Capstone** is an open-ended
design brief that composes everything into a multi-agent system. Every Advanced challenge and the
Capstone assume the **Foundations end-state**: a deployed, grounded Northfield University IQ Assistant
that answers from the FAQ corpus **with citations**.

Run the tree in one of three modes:

| Mode | Use it for | Starting point |
|---|---|---|
| **Customer Build Mode** | Driving a customer workshop or project kickoff toward a prototype | Complete the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}) first, then swap in customer-safe data and workflows |
| **Customer Challenge-Forge** | You have a customer scenario but no specific idea yet | Use the [Customer Challenge-Forge skill](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md) to generate ~10 right-sized AI app ideas, pick one, fill the canvas, then start building |
| **Upskill Mode** | Learning Microsoft Foundry with a known-good fictional scenario | Start Foundations with Northfield |

In **Customer Build Mode**, Northfield is the reference implementation. Keep the same architecture and
validators where possible, but replace the corpus, persona, action tools, eval prompts, and final demo
with the customer's scenario. All validators remain at `python validate.py --step N`; only your data and
context change.

```text
  TIER 1  FOUNDATIONS (guided, linear, everyone)
    Step1 --> Step2 --> Step3 --> Step4  <-- Foundations end-state
           |
           v
  TIER 2  ADVANCED (modular, pick any order)
    Action Tools | Evaluation+RedTeam | Tracing | Deploy
    deepeners: Fabric IQ | Voice Live | Build a UI | Copilot-Assisted
           |
           v
  TIER 3  CAPSTONE (open-ended design brief)
    Northfield IQ multi-agent: triage/router fans out to specialists
    (knowledge, actions), then converges.

```

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

For Customer Build Mode, prioritize **Action Tools**, **Evaluation & Red Teaming**, and **Build a UI**
when time is short. Those three turn a grounded assistant into a stakeholder-visible prototype with a
governed workflow and a trust scorecard.

## Tier 3 · Capstone

The open-ended summit: break the single Northfield IQ Assistant into a **multi-agent team** — a
triage/router that fans out to specialist agents (knowledge, actions) and converges — orchestrated
with the **Microsoft Agent Framework (MAF)**. It's a **design brief, not a placeholder-fill**: you
decide the org-chart and wire the graph.

<div class="challenge-card" markdown="1">

| Capstone | Time | Prereqs |
|----------|------|---------|
| [Northfield IQ, the Team — Multi-Agent Orchestration](capstone-multi-agent) | 2–2.5 hr core (+1 hr Magentic stretch, +1.5 hr hosted variant) | Foundations end-state **+** Action Tools |

[Start the Capstone →](capstone-multi-agent){: .btn .btn-primary }

**Make it your own:** the capstone is the best place to reskin — swap Northfield for your domain
(insurance, factory ops, retail) and demo *your* agent team.

</div>

## How to run this hackathon (two technical paths)

There are **two ways in**. Both converge on the same **Foundations end-state**, then fan out into the
modular Advanced tier.

- **Path A — Beginner (default, recommended).** Complete **Foundations** as one guided, linear challenge
  (4 ordered steps), then **pick Advanced challenges in any order**.

- **Path B — Advanced-skip (for teams who already know Foundry basics).** Run **one bootstrap**
  (~10–15 min) that materializes the Foundations end-state, verify a **single checkpoint**, then jump
  straight to the Advanced tier. You skip the guided *learning*, not the prerequisites.

```text
  PATH A (Beginner)
  +---------------------------------------------------+
  | FOUNDATIONS (guided, linear, everyone)            |
  | Step1 --> Step2 --> Step3 --> Step4               |
  | Setup    Model    Agent    Knowledge Base         |
  +---------------------------+-----------------------+
                              |
                              v  Foundations end-state:
                                 deployed, grounded Northfield IQ Assistant

  PATH B (Advanced skip)
  [bootstrap: azd up + setup-foundations] --> same end-state
  (~15 min, 1 checkpoint)
                              |
                              v
  ADVANCED (modular, pick any order)
  Action Tools | Evaluation+RedTeam | Tracing | Deploy
  Extras: Fabric IQ | Voice Live | Magentic | Hosted MAF | UI | Copilot

```

**The bootstrap checkpoint (single gate for Path B):**

```bash
azd up                                    # provision Foundry + AI Search + App Insights (+ ACR for deploy)
./scripts/setup-foundations.sh            # deploy model, create agent, index corpus, build IQ knowledge base
python scripts/validate-foundations.py    # ✅ asserts the Foundations end-state exists

```

`validate-foundations.py` must pass **green** before a Path-B team starts any Advanced challenge. Every
Advanced challenge assumes the **same** end-state, so you materialize it once, verify it once, and the
whole Advanced tier is unblocked.

Need to set up your environment first? Start at [Getting Started]({{ '/setup' | relative_url }}) and
return here once your toolchain is ready.
