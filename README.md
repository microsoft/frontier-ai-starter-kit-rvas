# AI Starter Kit — Customer Delivery with Microsoft Foundry

[![Deploy GitHub Pages](https://github.com/microsoft/frontier-ai-starter-kit-rvas/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/microsoft/frontier-ai-starter-kit-rvas/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/frontier-ai-starter-kit-rvas)

*Turn a customer conversation into a useful AI start.*

---

## Start with the customer decision

This repository is a reusable customer-delivery kit—not a fixed RAG curriculum. It helps a seller,
partner, or customer choose the next useful AI decision, then provides the relevant playbook
lessons, customer-facing slides, and a deliberately minimal accelerator.

1. Use [Customer Activity-Forge](.github/skills/customer-activity-forge/) when the customer
   opportunity is unclear.
2. Discuss outcome, data reality, existing environment, ownership, and evidence without pretending
   a file count decides architecture.
3. Choose one equal-priority scenario:
   - [AI Grounding / IQ](docs/scenario.html?id=ai-grounding)
   - [Content Understanding and Document Workflow](docs/scenario.html?id=content-understanding-document-workflow)
   - [Avatar Scenario](docs/scenario.html?id=avatar-scenario)
4. Select only the lessons required to prove the next decision. Each scenario includes
   source-controlled slides that can be printed or saved as a PDF, a safe minimal demonstrator,
   and a bring-your-own-environment path.

The kit does not prescribe a landing zone or a platform before the conversation. Foundry, Copilot
Studio, SharePoint, Fabric, and the IQ family are decision outcomes, evaluated against the
customer’s access, ownership, licensing, and operating needs.

## Scenario contribution

Scenarios live in [`scenarios/`](scenarios/). `npm run build` regenerates their static-site assets;
run `npm run validate:scenarios` to validate scenario packs. Read the [scenario contribution
contract](scenarios/README.md) before proposing a scenario or lesson.
Accelerators are resource-free decision blueprints plus local demonstrations; they never create
Azure resources or an enterprise platform baseline.

## Legacy technical reference

The remaining Northfield activities are retained as a technical reference for existing deep links,
safe samples, and implementation patterns. They are not the primary customer journey. Use the
scenario playbook first, then draw on the reference only when a selected lesson requires it.

---

## Who is this for?

### Participants

You're a great fit for this session if you:

- Have some Python experience (variables, functions, pip) and understand REST APIs and JSON
- Are curious about how AI models work and want to build with them
- Have a GitHub account and access to Azure (via Azure Pass, Azure for Students, or a trial subscription)
- Are ready to learn by solving real activities, not watching tutorials

No prior Azure or AI experience needed. Just bring curiosity and a willingness to debug.

### Facilitators

You're ready to facilitate if you:

- Are familiar with Microsoft Foundry model and agent concepts, and prompt engineering
- Enjoy helping teams think through problems (instead of giving direct answers)
- Can spend 6–8 hours supporting 2–3 teams
- Have access to the [Facilitator Hub](docs/facilitator-hub.md) and solution materials in this repo
- Can help teams translate a business scenario into data, tools, evals, and a demoable outcome

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

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/frontier-ai-starter-kit-rvas)

**Alternative**: Open locally with [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) in VS Code.

### 2. Authenticate with Azure

Once your environment is ready, authenticate to Azure:

```bash
az login
```

Follow the prompts to sign in with your Azure account. This connects your workspace to your Azure subscription so you can provision Microsoft Foundry resources.

### 3. Start the customer-delivery journey

Open the scenario playbook that matches the customer outcome. Use its lessons, printable customer
slides, and either the minimal accelerator or the bring-your-own-environment path. The remaining
activity material below is an archived implementation reference, not a prerequisite or a competing
event mode.

**Advanced skip:** Materialize the Foundations end-state with one bootstrap (~10–15 min), verify the single checkpoint, then jump straight to the Advanced tier:

Run these commands from the repository root:

```bash
azd up                                   # provision Foundry + AI Search + App Insights + ACR
./scripts/setup-foundations.sh           # build the agent + index + IQ knowledge base
python scripts/validate-foundations.py   # ✅ asserts the Foundations end-state
```

---

## Activities

The curriculum has three tiers. **Tier 1 Foundations** is one guided activity with four ordered
steps. **Tier 2 Advanced** activities are modular and can be completed in **any order** after
Foundations. **Tier 3 Capstone** is an open-ended design activity that combines the work into a
multi-agent system.

For customer engagements, treat every tier as an outcome checkpoint:

| Tier | Technical checkpoint | Customer-outcome checkpoint |
|---|---|---|
| Foundations | Grounded agent with citations | Answers real scenario questions from trusted data |
| Action Tools | Governed MCP action loop | Completes one valuable workflow with human approval |
| Evaluation | Quality + safety tests | Produces a trust scorecard the customer can review |
| Tracing / Deploy / UI | Observable, hosted app | Stakeholders can try it and inspect failures |
| Capstone | Multi-agent orchestration | Specialist agents handle a realistic business request |

```text
  TIER 1  FOUNDATIONS (guided, linear)
    Step1 --> Step2 --> Step3 --> Step4  <-- Foundations end-state
           |
           v
  TIER 2  ADVANCED (modular, pick any order)
    Action Tools | Evaluation+RedTeam | Tracing | Deploy
    deepeners: Fabric IQ | Document Workflow | Visual Multimodal | Governed Data Copilot | Voice Live | Build a UI | Copilot-Assisted
           |
           v
  TIER 3  CAPSTONE (open-ended design activity)
    Northfield IQ multi-agent: triage/router fans out to specialists
    (knowledge, actions), then converges.
```

### Tier 1 — Foundations (`activities/foundations/`)

| Step | Title | Duration | Difficulty | Builds toward end-state |
|---|-----------|----------|------------|------------|
| 1 | [Setup & Provisioning (Foundry + AI Search)](activities/foundations/README.md#step-1--setup--provisioning-foundry--ai-search) | 30 min | ⭐ | Infra live; `.env` contract |
| 2 | [Model Selection & the Playground](activities/foundations/README.md#step-2--model-selection--the-playground) | 45 min | ⭐ | A chosen model + system instructions |
| 3 | [Your First Agent](activities/foundations/README.md#step-3--your-first-agent) | 45 min | ⭐⭐ | A named, versioned agent |
| 4 | [Knowledge Base — Index + Foundry IQ](activities/foundations/README.md#step-4--knowledge-base-index--foundry-iq---foundations-end-state) | 1.5 hr | ⭐⭐⭐ | **Grounded agent w/ citations (END-STATE)** |

### Tier 2 — Advanced (modular · any order)

Each Advanced activity offers two paths: a **Guided** path (revised, honest time) and a longer
**Build-from-scratch** path with fewer placeholders. Both are graded by the same `validate.py`.

| Activity | Guided | Build-from-scratch | Difficulty | Key Skills |
|-----------|--------|--------------------|------------|------------|
| [Action Tools — Make the Agent Do Work](activities/advanced-action-tools/README.md) | ~45 min | ~1.5 hr | ⭐⭐⭐ | MCP tool, tool-approval loop |
| [Evaluation & Red Teaming](activities/advanced-evaluation-redteam/README.md) | ~1.25 hr | ~2 hr | ⭐⭐⭐⭐ | NLP metrics + adversarial safety |
| [Tracing & Observability](activities/advanced-tracing-observability/README.md) | ~1 hr | ~1.5 hr | ⭐⭐⭐⭐ | OTel GenAI → App Insights → KQL |
| [Deploy as a Hosted Agent](activities/advanced-deploy-hosted-agent/README.md) | ~60–90 min | ~1.5 hr | ⭐⭐⭐⭐⭐ | `azd ai agent`, hosted endpoint |

**Extras** (optional, modular) — re-slotted by their role in the tree:
- **Capstone-feeders**: Magentic Workflows, MAF + Hosted Long-Running Agents — the strongest content
  feeds straight into the Tier 3 multi-agent build.
- **Capstone companion**: Build a UI — a web front-end for your agent (or agent team).
- **Deepeners**: Fabric IQ, Document Workflow, Visual Multimodal, Governed Data Copilot,
  Give It a Voice (Voice Live), Copilot-Assisted Build — extend one concept.

See the `activities/extra-*` folders.

### Tier 3 — Capstone (`activities/capstone-multi-agent/`)

Break the single Northfield IQ Assistant into a **multi-agent team** — a
[triage/router that fans out to specialist agents and converges](activities/capstone-multi-agent/README.md#the-agent-org-chart-role-as-agent),
orchestrated with the **Microsoft Agent Framework (MAF)**. You decide the org chart and wire the graph
against the acceptance criteria.

| Capstone | Time | Difficulty | Prereqs |
|----------|------|------------|---------|
| [Northfield IQ, the Team — Multi-Agent Orchestration](activities/capstone-multi-agent/README.md) | 2–2.5 hr core (+1 hr Magentic stretch, +1.5 hr hosted variant) | ⭐⭐⭐⭐⭐ | Foundations end-state **+** Action Tools |

**Make it your own:** the capstone is the best place to reskin — swap Northfield for your domain
(insurance, factory ops, retail) and demo *your* agent team.

**Total guided path (Foundations + all four Advanced): ~7.25 hours** + **~2.5 hr Capstone** — a clean
multi-day story. For a **1-day event**, run Foundations + 2–3 Advanced activities and save the Capstone
for a second day or a follow-up sprint.

---

## Repository Structure

```
ai-starter-kit-rvas/
├── README.md                          # ← You are here
├── azure.yaml                         # azd project (golden-path provisioning)
├── infra/                             # Bicep — Foundry + AI Search + App Insights + ACR
├── scripts/                           # deploy.sh, setup-foundations.sh, validate-foundations.py, cleanup.sh
│   └── action-backend/                # Action Tools REST API + FastMCP server (provided)
├── activities/                        # Activity content and solutions
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

Each activity folder contains:
- `README.md`: the activity brief (what to build)
- `solution.md`: the solution guide (facilitators only)
- Sample data or starter code (if needed)

---

## For Facilitators

### Getting Started

Visit the [Facilitator Hub](docs/facilitator-hub.md) for tips on facilitating the event and working with your teams.

### Solution Guides

Solution guides for each activity are included in this repo under `activities/*/solution.md`. These are **for facilitators only**; share judiciously to encourage discovery over answers.

Clone or access this repo locally and navigate to the activity solution you need.

### Quick-Start Facilitation Checklist

1. Verify all participants have Azure subscriptions and Codespaces access
2. Review the activity brief before your team starts
3. Walk through Foundations Step 1 with them to confirm the environment works
4. For each activity, guide them toward the solution without giving it away
5. Use the solution guide to unblock them if they're truly stuck

---

## Resources

- **[Microsoft Foundry Documentation](https://learn.microsoft.com/azure/foundry/)**: Official docs and tutorials
- **[Microsoft Foundry Training](https://learn.microsoft.com/training/azure/ai-foundry)**: Structured training modules
- **[Microsoft AI Skills Navigator](https://microsoft.com/ai/skills)**: Browse AI and cloud certifications

---

**Ready to build?** Start with [Foundations](activities/foundations/README.md).
