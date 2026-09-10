# AI Starter Kit — Co-build customer AI scenarios

[![Deploy GitHub Pages](https://github.com/microsoft/frontier-ai-starter-kit-rvas/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/microsoft/frontier-ai-starter-kit-rvas/actions/workflows/deploy-pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/frontier-ai-starter-kit-rvas)

*Build with the customer, using reusable implementation patterns.*

---

## Start with the customer's scenario

The AI Starter Kit helps customer teams and their technical advisers **co-build the customer's own
AI scenario**. Each playbook breaks down the architectural decisions and guides implementation with
reusable building blocks. Teams adapt the code and work through the relevant lessons in their
approved environment. Customer-facing slides support the design discussions.

**The initial tracks cover three reusable patterns:**

| Track | What you build |
|---|---|
| [AI Grounding / IQ](docs/scenario.html?id=ai-grounding) | An assistant that answers from approved content and respects access boundaries. |
| [Content Understanding and Document Workflow](docs/scenario.html?id=content-understanding-document-workflow) | A document workflow with evidence-backed extraction and human review. |
| [Avatar Scenario](docs/scenario.html?id=avatar-scenario) | An avatar-led experience with approved content and publication controls. |

These are starting points, not a complete catalog of AI use cases. **A customer's scenario may
combine parts from several tracks.** New tracks can follow the same contribution contract.

Begin with the customer's outcome and data constraints. If the opportunity is unclear, use
[Customer Activity-Forge](.github/skills/customer-activity-forge/) to find a direction.

## Break the use case into parts

Before selecting sessions, decompose the customer's end-to-end use case into the parts it needs.
Map each part to the relevant lessons or reference activities. Record what the material covers,
what needs adapting, and what requires additional engineering. Keep uncovered work visible even
when it falls outside the engagement.

For example, a supplier-request process could draw on several parts of the kit:

| Part of the customer use case | Reusable guidance | Customer-specific work |
|---|---|---|
| Extract fields from a submitted document | Content Understanding extraction lessons | Define the fields and evaluate representative documents. |
| Answer a related policy question | AI Grounding lessons | Connect approved policy content and prove access boundaries. |
| Create a record in the customer's business system | Action Tools reference for an approval-gated handoff | Build the system-specific integration; the generic action pattern does not supply it. |

**Plan sessions around this mapping.** Combine the relevant lessons across tracks, keeping their
prerequisites. Agree which parts the engagement will build and assign owners to the remaining work.

The implementation reference focuses on Microsoft Foundry. The playbooks also discuss choices such
as Copilot Studio, SharePoint, and Fabric. Choose the platform with the customer; naming an option
does not mean the kit contains a complete implementation for it.

## Agree the delivery scope

The kit can support a scoped pilot or a longer co-build engagement. **Agree the customer-specific
work and acceptance criteria before committing to delivery.** Production readiness depends on
the customer's integrations, security requirements, and operational acceptance. Completing the
lessons or deploying an accelerator does not establish it.

Published durations estimate guided lesson time. They are not estimates for a full customer
implementation.

## What the accelerators provide

Accelerators supply sample assets and reusable code for the lessons. Some include optional Bicep
foundations for clean demo subscriptions; others include local exercises. Follow each guide's
requirements: the grounding scripts, for example, call real Azure resources.

For an existing customer environment, use the bring-your-own-environment path and approved
resources. The demo foundations do not provision an enterprise landing zone or replace
customer-specific engineering.

## Scenario contribution

Scenarios live in [`scenarios/`](scenarios/). `npm run build` regenerates their static-site assets;
run `npm run validate:scenarios` to validate scenario packs. Read the [scenario contribution
contract](scenarios/README.md) before proposing a scenario or lesson.

## Reusable technical reference

The Northfield activities provide a fictional reference implementation and guided practice.
Use the scenario playbook to choose the relevant implementation activities, then adapt them to
the customer's requirements. You do not need to complete the whole reference curriculum.

---

## Who is this for?

### Customer technical teams

Bring a scenario to build, or use Idea Forge to help choose one. The code-based lessons assume
basic Python and familiarity with REST APIs and JSON. Use synthetic data for initial exercises;
agree a separate, approved path before working with customer data.

### Delivery teams and facilitators

Use the playbooks to work through design choices with the customer and adapt the implementation
material. Review the relevant solution guides before delivery. Plan engineering capacity around
the agreed scope, including integration work and handoff to the customer's operating team.

---

## Prerequisites

Before you start, make sure you have:

- **Approved environment**: An Azure subscription and required permissions for live Azure lessons;
  local exercises list their own requirements
- **Development environment**: GitHub Codespaces or a local Dev Container for the code-based lessons
- **Basic Python**: Comfortable with variables, functions, pip, and virtual environments
- **Basic API knowledge**: Understand REST APIs, HTTP requests, and JSON
- **VS Code familiarity**: Helpful, but not required (the devcontainer includes everything)

---

## Getting Started

### 1. Choose a scenario and scope

Break the customer's use case into parts and map them to the relevant lessons. Agree what the
engagement will build and how to judge the result. Check prerequisites before provisioning resources.

### 2. Open in GitHub Codespaces or Dev Container

Click the badge below to open a fully configured development environment:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/frontier-ai-starter-kit-rvas)

**Alternative**: Open locally with [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) in VS Code.

### 3. Follow the selected environment path

For live Azure lessons, authenticate to the approved subscription:

```bash
az login
```

Follow the selected scenario's accelerator guide for a clean demo subscription or an existing
customer environment. Deploy demo resources only where approved.

### Optional: bootstrap the reference implementation

When you need the Northfield reference for an Advanced activity, the bootstrap creates the
Foundations sample end-state. This deploys sample infrastructure; it does not implement the
customer's scenario.

Run these commands from the repository root:

```bash
azd up                                   # provision Foundry + AI Search + App Insights + ACR
./scripts/setup-foundations.sh           # build the agent + index + IQ knowledge base
python scripts/validate-foundations.py   # ✅ asserts the Foundations end-state
```

---

## Activities

The reference curriculum has two activity layers. **Foundations** is one guided activity with four
ordered steps. **Advanced** activities are modular and can be completed in **any order** after
Foundations. Use the parts required by your selected scenario.

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
    deepeners: Fabric IQ | Document Workflow | Visual Multimodal | Governed Data Copilot | Voice Live | Build a UI
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

**Extras** (optional, modular) — pick only the ones that support the scenario you are building:
Fabric IQ, Document Workflow, Visual Multimodal, Governed Data Copilot, Give It a Voice (Voice Live),
Build a UI, Magentic Workflows, and Hosted Long-Running Agents.

See the `activities/extra-*` folders.

**Reference workshop time (Foundations + all four Advanced): ~7.25 hours.** For a one-day workshop,
choose Foundations and two or three Advanced activities. Customer-specific implementation work
needs a separate estimate.

---

## Publishing the documentation site

Before the first deployment, a repository administrator must open **Settings > Pages** and select **Deploy from a branch**, the `gh-pages` branch, and the `/(root)` folder. If the site currently uses **GitHub Actions** as its Pages source, change it to this branch setup. The workflow publishes the site and pull request previews to `gh-pages`; it cannot change the repository Pages settings because the `GITHUB_TOKEN` does not have that administrative permission.

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
- `solution.md`: the reference solution guide for delivery teams and facilitators
- Sample data or starter code (if needed)

---

## Solution Guides

Solution guides under `activities/*/solution.md` support delivery preparation. Use them to understand
and adapt the reference implementation. In a learning workshop, facilitators can use them to help
participants work through a problem.

Clone or access this repo locally and navigate to the activity solution you need.

### Quick-Start Facilitation Checklist

1. Agree the customer outcome, delivery scope, and acceptance criteria.
2. Map the use-case parts to sessions, identify uncovered work, and confirm lesson prerequisites.
3. Confirm the approved environment and source-access boundary.
4. Build with the customer, using the solution guides where helpful.
5. Review the evidence and record remaining work with a named owner.

---

## Resources

- **[Microsoft Foundry Documentation](https://learn.microsoft.com/azure/foundry/)**: Official docs and tutorials
- **[Microsoft Foundry Training](https://learn.microsoft.com/training/azure/ai-foundry)**: Structured training modules
- **[Microsoft AI skills resources](https://www.microsoft.com/en-us/corporate-responsibility/ai-skills-resources)**: Browse AI skilling and training resources

---

**Ready to build?** Choose a [scenario playbook](docs/index.html#outcomes).
