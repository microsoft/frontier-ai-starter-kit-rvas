# Build Intelligent Apps with Microsoft Foundry

[![Deploy GitHub Pages](https://github.com/olivomarco/ai-hackathon/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/olivomarco/ai-hackathon/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/olivomarco/ai-hackathon)

*A What The Hack hackathon: from prompt to production*

---

## What is What The Hack?

**What The Hack** (WTH) is Microsoft's hackathon-in-a-box format designed to teach cloud and AI technologies through hands-on challenge-based learning. This repository brings WTH to Microsoft Foundry, a unified platform for building, evaluating, and deploying intelligent applications.

This hackathon, you and your team build **one evolving artifact** — the **Northfield University IQ Assistant** — across three tiers. First you complete a guided **Foundations** challenge (four ordered steps) to stand up a deployed, grounded agent; then you pick **Advanced** challenges in any order to make it act, prove it safe, observe it, and ship it; finally you converge on an open-ended **Capstone** that breaks the single agent into a multi-agent team. Rather than lectures, you'll learn by *doing*: deploying models, building agents, grounding them in real data with a knowledge base, wiring action tools, shipping a hosted agent, and orchestrating a multi-agent system. Coaches guide discovery and unblock issues, but the learning is yours to own.

By the end, you'll have hands-on experience with the Microsoft Foundry platform, practical skills in prompt engineering and RAG (Retrieval-Augmented Generation), and a deployment-ready AI application to show for your work.

---

## Learning Outcomes

By the end of this hackathon, you will be able to:

- Navigate Microsoft Foundry and provision an AI project with connected resources (`azd up`)
- Deploy and compare models from the Azure AI model catalog
- Build a named, versioned Foundry **agent** with a persona and guardrails
- Ground the agent in your own data with an **Index + Foundry IQ knowledge base** (with citations)
- Give the agent **action tools** via MCP that execute real operations
- Evaluate outputs for quality and safety, including **red teaming**
- Trace every answer end-to-end, then **deploy a hosted agent**

---

## Who is this for?

### Students

You're a great fit for this hackathon if you:

- Have some Python experience (variables, functions, pip) and understand REST APIs and JSON
- Are curious about how AI models work and want to build with them
- Have a GitHub account and access to Azure (via Azure Pass, Azure for Students, or a trial subscription)
- Are ready to learn by solving real challenges, not watching tutorials

No prior Azure or AI experience needed. Just bring curiosity and a willingness to debug.

### Coaches

You're ready to coach if you:

- Are familiar with Microsoft Foundry, Azure OpenAI Service, and prompt engineering
- Enjoy helping teams think through problems (instead of giving direct answers)
- Can spend 6–8 hours supporting 2–3 teams
- Have access to the [Coach Hub](docs/coach-hub.md) and solution materials in this repo

---

## Prerequisites

Before you start, make sure you have:

- **Azure subscription**: Provided via Azure Pass, Azure for Students, or a free trial
- **GitHub account**: With Codespaces access (required for the dev environment)
- **Basic Python**: Comfortable with variables, functions, pip, and virtual environments
- **Basic API knowledge**: Understand REST APIs, HTTP requests, and JSON
- **VS Code familiarity**: Helpful, but not required (the devcontainer includes everything)

---

## Getting Started

### 1. Open in GitHub Codespaces or Dev Container

Click the badge below to open a fully configured development environment:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/olivomarco/ai-hackathon)

**Alternative**: Open locally with [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) in VS Code.

### 2. Authenticate with Azure

Once your environment is ready, authenticate to Azure:

```bash
az login
```

Follow the prompts to sign in with your Azure account. This connects your workspace to your Azure subscription so you can provision Microsoft Foundry resources.

### 3. Start with Foundations (or bootstrap)

**Path A (beginner, recommended):** Read [Foundations](challenges/foundations/README.md) and work through Steps 1–4 to stand up a deployed, grounded Northfield IQ Assistant.

**Path B (advanced skip):** Materialize the Foundations end-state with one bootstrap (~10–15 min), verify the single checkpoint, then jump straight to the Advanced tier:

```bash
azd up                                   # provision Foundry + AI Search + App Insights + ACR
./scripts/setup-foundations.sh           # build the agent + index + IQ knowledge base
python scripts/validate-foundations.py   # ✅ asserts the Foundations end-state
```

---

## Challenges

The curriculum is a **tree of three tiers** — climb a guided trunk, fan out across modular branches,
then converge on an open summit. **Tier 1 Foundations** is one guided, linear challenge with four
ordered steps (everyone does it). **Tier 2 Advanced** challenges are modular and can be attempted in
**any order** — they all assume the Foundations end-state. **Tier 3 Capstone** is an open-ended
design brief that composes everything into a multi-agent system.

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

### Tier 1 — Foundations (`challenges/foundations/`)

| Step | Title | Duration | Difficulty | Builds toward end-state |
|---|-----------|----------|------------|------------|
| 1 | [Setup & Provisioning (Foundry + AI Search)](challenges/foundations/README.md#step-1--setup--provisioning-foundry--ai-search) | 30 min | ⭐ | Infra live; `.env` contract |
| 2 | [Model Selection & the Playground](challenges/foundations/README.md#step-2--model-selection--the-playground) | 45 min | ⭐ | A chosen model + system instructions |
| 3 | [Your First Agent](challenges/foundations/README.md#step-3--your-first-agent) | 45 min | ⭐⭐ | A named, versioned agent |
| 4 | [Knowledge Base — Index + Foundry IQ](challenges/foundations/README.md#step-4--knowledge-base-index--foundry-iq---foundations-end-state) | 1.5 hr | ⭐⭐⭐ | **Grounded agent w/ citations (END-STATE)** |

### Tier 2 — Advanced (modular · any order)

Each Advanced challenge offers two paths: a **Guided** path (revised, honest time) and a longer
**Build-from-scratch** path with fewer placeholders. Both are graded by the same `validate.py`.

| Challenge | Guided | Build-from-scratch | Difficulty | Key Skills |
|-----------|--------|--------------------|------------|------------|
| [Action Tools — Make the Agent Do Work](challenges/advanced-action-tools/README.md) | ~45 min | ~1.5 hr | ⭐⭐⭐ | MCP tool, tool-approval loop |
| [Evaluation & Red Teaming](challenges/advanced-evaluation-redteam/README.md) | ~1.25 hr | ~2 hr | ⭐⭐⭐⭐ | NLP metrics + adversarial safety |
| [Tracing & Observability](challenges/advanced-tracing-observability/README.md) | ~1 hr | ~1.5 hr | ⭐⭐⭐⭐ | OTel GenAI → App Insights → KQL |
| [Deploy as a Hosted Agent](challenges/advanced-deploy-hosted-agent/README.md) | ~60–90 min | ~1.5 hr | ⭐⭐⭐⭐⭐ | `azd ai agent`, hosted endpoint |

**Extras** (optional, modular) — re-slotted by their role in the tree:
- **Capstone-feeders**: Magentic Workflows, MAF + Hosted Long-Running Agents — the strongest content
  feeds straight into the Tier 3 multi-agent build.
- **Capstone companion**: Build a UI — a web front-end for your agent (or agent team).
- **Deepeners**: Fabric IQ, Give It a Voice (Voice Live), Copilot-Assisted Build — extend one concept.

See the `challenges/extra-*` folders.

### Tier 3 — Capstone (`challenges/capstone-multi-agent/`)

The open-ended summit: break the single Northfield IQ Assistant into a **multi-agent team** — a
[triage/router that fans out to specialist agents and converges](challenges/capstone-multi-agent/README.md#the-agent-org-chart-role-as-agent),
orchestrated with the **Microsoft Agent Framework (MAF)**. It's a **design brief, not a placeholder-fill** —
you decide the org-chart and wire the graph.

| Capstone | Time | Difficulty | Prereqs |
|----------|------|------------|---------|
| [Northfield IQ, the Team — Multi-Agent Orchestration](challenges/capstone-multi-agent/README.md) | 2–2.5 hr core (+1 hr Magentic stretch, +1.5 hr hosted variant) | ⭐⭐⭐⭐⭐ | Foundations end-state **+** Action Tools |

**Make it your own:** the capstone is the best place to reskin — swap Northfield for your domain
(insurance, factory ops, retail) and demo *your* agent team.

**Total guided path (Foundations + all four Advanced): ~7.25 hours** + **~2.5 hr Capstone** — a clean
multi-day story. For a **1-day event**, run Foundations + 2–3 Advanced challenges and save the Capstone
for a second day or a follow-up sprint.

---

## Repository Structure

```
ai-hackathon/
├── README.md                          # ← You are here
├── azure.yaml                         # azd project (golden-path provisioning)
├── infra/                             # Bicep — Foundry + AI Search + App Insights + ACR
├── scripts/                           # deploy.sh, setup-foundations.sh, validate-foundations.py, cleanup.sh
│   └── action-backend/                # Action Tools REST API + FastMCP server (provided)
├── challenges/                        # Challenge content and solutions
│   ├── foundations/                   # Tier 1 — guided, Steps 1–4
│   ├── advanced-action-tools/         # Tier 2 — modular, any order
│   ├── advanced-evaluation-redteam/
│   ├── advanced-tracing-observability/
│   ├── advanced-deploy-hosted-agent/
│   ├── capstone-multi-agent/          # Tier 3 — open-ended MAF capstone
│   └── extra-*/                       # Tier 2 — Extras (optional)
├── resources/sample-data/             # Northfield University FAQ corpus (knowledge base source)
├── docs/                              # Supporting documentation (Jekyll/GitHub Pages)
├── .devcontainer/                     # Dev environment config (Python, Azure CLI, azd)
├── .github/                           # Copilot enablement (skills, copilot-instructions) + workflows
├── .vscode/mcp.json                   # MCP servers: azure, foundry-mcp, microsoft-docs
└── .env.sample                        # The .env variable contract (never commit a real .env)
```

Each challenge folder contains:
- `README.md`: the challenge brief (what to build)
- `solution.md`: the solution guide (coaches only)
- Sample data or starter code (if needed)

---

## For Coaches

### Getting Started

Visit the [Coach Hub](docs/coach-hub.md) for tips on facilitating WTH events and working with your teams.

### Solution Guides

Solution guides for each challenge are included in this repo under `challenges/*/solution.md`. These are **for coaches only**; share judiciously to encourage discovery over answers.

Clone or access this repo locally and navigate to the challenge solution you need.

### Quick-Start Coaching Checklist

1. Verify all participants have Azure subscriptions and Codespaces access
2. Review the challenge brief before your team starts
3. Walk through Foundations Step 1 with them to confirm the environment works
4. For each challenge, guide them toward the solution without giving it away
5. Use the solution guide to unblock them if they're truly stuck

---

## Resources

- **[Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)**: Official docs and tutorials
- **[Azure AI Learning Path](https://learn.microsoft.com/training/paths/develop-generative-ai-solutions-azure-ai-foundry/)**: Structured training modules
- **[Microsoft AI Skills Navigator](https://microsoft.com/ai/skills)**: Browse AI and cloud certifications
- **[What The Hack Format Guide](https://microsoft.github.io/WhatTheHack/)**: Learn about WTH events

---

**Ready to build?** Start with [Foundations](challenges/foundations/README.md).
