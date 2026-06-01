# WTH AI Hackathon: Content Architecture Plan

> **"Build Intelligent Apps with Microsoft Foundry"**
>
> A What The Hack hackathon-in-a-box that takes participants from zero to deploying an AI-powered application using Microsoft Foundry.

---

## 1. Hackathon Overview

| Field | Detail |
|-------|--------|
| **Title** | Build Intelligent Apps with Microsoft Foundry |
| **Tagline** | From prompt to production: build, evaluate, and deploy AI solutions |
| **Duration** | 1-day event (6–8 hours of challenge time) or 2-day event (relaxed pace with deeper exploration) |
| **Team size** | 3–5 participants per team |
| **Coach ratio** | 1 coach per 2–3 teams |

### Target Audience

**Participants (Students)**
- University students (CS, Data Science, or adjacent) or early-career professionals
- Comfortable with Python basics and REST APIs
- No prior Azure or Microsoft Foundry experience required

**Coaches**
- Experienced Azure practitioners (AI Engineers, Cloud Solution Architects)
- Familiar with Microsoft Foundry, Azure OpenAI Service, and prompt engineering
- Role: facilitate discovery, unblock teams, never give answers directly

### Prerequisites for Participants
- GitHub account (with Codespaces access)
- Azure subscription (provided via Azure Pass or sandbox)
- Basic Python (variables, functions, pip, virtual envs)
- Basic understanding of REST APIs and JSON
- Familiarity with VS Code (recommended, not required)

### High-Level Learning Outcomes

By the end of this hackathon, participants will be able to:

1. Navigate Microsoft Foundry and create an AI project with connected resources
2. Deploy and interact with models from the Azure AI model catalog
3. Engineer effective prompts and implement prompt flow orchestration
4. Build a grounded RAG (Retrieval-Augmented Generation) application
5. Evaluate AI model outputs for quality, safety, and responsible AI compliance
6. Deploy an AI endpoint and integrate it into an application

---

## 2. Challenge List

### Challenge 00: Setup & Orientation
| Field | Detail |
|-------|--------|
| **Description** | Provision your Microsoft Foundry resource and project. Explore the portal interface, connect your Azure OpenAI resource, and verify your development environment works end-to-end. |
| **Time** | 30 minutes |
| **Difficulty** | Beginner |
| **Dependencies** | None |
| **Microsoft Foundry features** | Foundry resource, Project creation, Resource connections, Model catalog browsing |

**Learning Objectives:**
- Create a Microsoft Foundry resource and project
- Connect an Azure OpenAI Service resource
- Navigate the Microsoft Foundry portal (deployments, playground, catalog)
- Verify the devcontainer environment connects to Azure
- Understand the relationship between Foundry resources, projects, and connections

---

### Challenge 01: Your First Model Deployment
| Field | Detail |
|-------|--------|
| **Description** | Deploy a GPT model from the model catalog, interact with it via the playground, then call it programmatically using the Azure AI Inference SDK. Compare different model capabilities. |
| **Time** | 45 minutes |
| **Difficulty** | Beginner |
| **Dependencies** | Challenge 00 |
| **Microsoft Foundry features** | Model catalog, Model deployments (MaaS/MaaP), AI Inference SDK, Playground |

**Learning Objectives:**
- Deploy a model from the Azure AI model catalog
- Understand deployment types (Models-as-a-Service vs Models-as-a-Platform)
- Use the Playground to test completions with system/user messages
- Call a deployed model using `azure-ai-inference` Python SDK
- Compare output from different model families (GPT-4o vs GPT-4o-mini)

---

### Challenge 02: Prompt Engineering & System Design
| Field | Detail |
|-------|--------|
| **Description** | Master prompt engineering techniques: persona setting, few-shot examples, chain-of-thought reasoning, and output formatting. Design a system prompt for a specific use case (e.g., a university Q&A assistant). |
| **Time** | 1 hour |
| **Difficulty** | Beginner–Intermediate |
| **Dependencies** | Challenge 01 |
| **Microsoft Foundry features** | Playground (Chat), Prompt management, Content filtering configuration |

**Learning Objectives:**
- Apply prompt engineering patterns (persona, few-shot, CoT, output schemas)
- Design a system prompt that controls model behavior reliably
- Configure content safety filters and understand their impact
- Test prompt variations systematically in the Playground
- Document prompt design decisions for reproducibility

---

### Challenge 03: Prompt Flow Orchestration
| Field | Detail |
|-------|--------|
| **Description** | Build a multi-step prompt flow that chains LLM calls with Python code nodes. Implement input validation, conditional logic, and structured output parsing. Test and iterate on the flow within Microsoft Foundry. |
| **Time** | 1.5 hours |
| **Difficulty** | Intermediate |
| **Dependencies** | Challenge 02 |
| **Microsoft Foundry features** | Prompt flow (visual editor + code), Flow variants, Connections, Batch testing |

**Learning Objectives:**
- Create a prompt flow with multiple LLM and Python nodes
- Use flow inputs/outputs and variable passing between nodes
- Implement conditional branching and error handling
- Test flows with batch inputs for reliability
- Understand connections and runtime environments in prompt flow

---

### Challenge 04: RAG — Grounding with Your Data
| Field | Detail |
|-------|--------|
| **Description** | Build a Retrieval-Augmented Generation pipeline. Index a document collection into Azure AI Search, connect it to your AI project, and create a grounded chat experience that answers questions from your own data. |
| **Time** | 1.5 hours |
| **Difficulty** | Intermediate–Advanced |
| **Dependencies** | Challenge 03 |
| **Microsoft Foundry features** | Azure AI Search integration, Vector indexes, Data connections, On Your Data, Prompt flow RAG nodes |

**Learning Objectives:**
- Create and populate a vector index in Azure AI Search
- Connect the index to a Microsoft Foundry project
- Implement RAG using "On Your Data" in the Playground
- Build a prompt flow with retrieval + generation nodes
- Handle citation attribution and source grounding

---

### Challenge 05: Evaluation & Responsible AI
| Field | Detail |
|-------|--------|
| **Description** | Evaluate your RAG application using Microsoft Foundry's built-in evaluation framework. Measure groundedness, relevance, coherence, and safety. Identify failure modes and iterate on your solution. |
| **Time** | 1 hour |
| **Difficulty** | Intermediate–Advanced |
| **Dependencies** | Challenge 04 |
| **Microsoft Foundry features** | Evaluation framework, Built-in metrics (groundedness, relevance, coherence, fluency), Custom evaluators, Safety evaluations |

**Learning Objectives:**
- Run evaluations using Microsoft Foundry's evaluation framework
- Interpret built-in quality metrics (groundedness, relevance, coherence)
- Configure and run safety evaluations (harmful content, jailbreak)
- Create a custom evaluator for domain-specific quality criteria
- Use evaluation results to improve prompt and RAG pipeline

---

### Challenge 06: Deploy & Integrate
| Field | Detail |
|-------|--------|
| **Description** | Deploy your evaluated prompt flow as a managed online endpoint. Build a minimal frontend that calls the endpoint, demonstrating a production-ready integration pattern. |
| **Time** | 1 hour |
| **Difficulty** | Advanced |
| **Dependencies** | Challenge 05 |
| **Microsoft Foundry features** | Managed online endpoints, Deployment configuration, API keys/auth, Monitoring |

**Learning Objectives:**
- Deploy a prompt flow to a managed online endpoint
- Configure deployment settings (instance type, scaling, auth)
- Call the deployed endpoint from an external application
- Implement basic error handling and retry logic
- Understand monitoring and logging for production AI services

---

### Challenge Progression Summary

```
Challenge 00 (Setup)          ─── Beginner ──────── 30 min
    │
Challenge 01 (Deploy Model)   ─── Beginner ──────── 45 min
    │
Challenge 02 (Prompts)        ─── Beg/Inter ─────── 1 hr
    │
Challenge 03 (Prompt Flow)    ─── Intermediate ──── 1.5 hr
    │
Challenge 04 (RAG)            ─── Inter/Adv ─────── 1.5 hr
    │
Challenge 05 (Evaluation)     ─── Inter/Adv ─────── 1 hr
    │
Challenge 06 (Deploy)         ─── Advanced ──────── 1 hr
                                              TOTAL: ~7.25 hr
```

---

## 3. Repository Structure

```
/
├── PLAN.md                         ← This file (content architecture)
├── README.md                       ← Entry point: overview, setup, challenge links
├── LICENSE
│
├── .devcontainer/
│   ├── devcontainer.json           ← Container config
│   └── post-create.sh             ← Post-creation setup script
│
├── .github/
│   └── workflows/
│       └── deploy-pages.yml        ← GitHub Pages deployment
│
├── docs/                           ← GitHub Pages source (Jekyll)
│   ├── _config.yml
│   ├── index.md                    ← Home page
│   ├── setup.md                    ← Setup & prerequisites guide
│   ├── coach-hub.md                ← Coach guidance & facilitation tips
│   ├── faq.md                      ← Frequently asked questions
│   └── challenges/
│       ├── challenge-00.md
│       ├── challenge-01.md
│       ├── ...
│       └── challenge-06.md
│
├── challenges/
│   ├── challenge-00-setup/
│   │   ├── README.md               ← Student-facing challenge guide
│   │   └── solution.md            ← Coach-facing solution guide
│   ├── challenge-01-first-model/
│   │   ├── README.md
│   │   └── solution.md
│   ├── challenge-02-prompt-engineering/
│   │   ├── README.md
│   │   └── solution.md
│   ├── challenge-03-prompt-flow/
│   │   ├── README.md
│   │   └── solution.md
│   ├── challenge-04-rag/
│   │   ├── README.md
│   │   └── solution.md
│   ├── challenge-05-evaluation/
│   │   ├── README.md
│   │   └── solution.md
│   └── challenge-06-deploy/
│       ├── README.md
│       └── solution.md
│
└── resources/
    ├── sample-data/                ← Documents for RAG challenge (Challenge 04)
    │   └── university-faq/        ← Example: fictional university FAQ corpus
    ├── scripts/
    │   ├── validate-environment.py ← Checks Azure connection & tools
    │   └── setup-resources.sh     ← Optional: Azure resource provisioning via azd
    └── images/                     ← Diagrams, screenshots for guides
```

### Structure Rationale

| Decision | Reasoning |
|----------|-----------|
| `challenges/` at root | Fast access for participants; each folder is self-contained |
| `docs/` separate from `challenges/` | Pages site has its own layout/nav; challenges are the source of truth, docs pages can reference them |
| `resources/sample-data/` | Shared data used across challenges (especially RAG); avoids duplication |
| Challenge folders named `challenge-NN-slug/` | Sortable, descriptive, URL-friendly |
| Coach solutions in same folder as student guide | Coaches need context; keeps student/coach content paired |
| `.devcontainer/` | Ensures consistent environment; critical for hackathon reliability |

---

## 4. Devcontainer Specification

### Base Image
`mcr.microsoft.com/devcontainers/python:3.11` (or 3.12 when stable with all SDKs)

### Tools & CLIs
| Tool | Purpose |
|------|---------|
| Azure CLI (`az`) | Azure resource management |
| Azure Developer CLI (`azd`) | Template-based provisioning |
| Python 3.11+ | Primary development language |
| Node.js 20 LTS | For any JS tooling / frontend in Challenge 06 |
| Git | Version control |
| jq | JSON parsing in shell scripts |

### Python Packages (requirements.txt)
```
azure-ai-projects>=1.0.0b1
azure-ai-inference>=1.0.0b1
azure-ai-evaluation>=1.0.0b1
azure-search-documents>=11.4.0
azure-identity>=1.15.0
openai>=1.12.0
python-dotenv>=1.0.0
requests>=2.31.0
promptflow>=1.10.0
promptflow-tools>=1.4.0
jupyter>=1.0.0
ipykernel>=6.29.0
```

### VS Code Extensions
```json
{
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "ms-azuretools.vscode-azurefunctions",
    "ms-vscode.azure-account",
    "ms-azuretools.azure-ai-foundry",
    "ms-azuretools.vscode-bicep",
    "github.copilot",
    "github.copilot-chat",
    "redhat.vscode-yaml",
    "ms-toolsai.promptflow"
  ]
}
```

### Environment Settings
```json
{
  "settings": {
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.terminal.activateEnvironment": true,
    "editor.formatOnSave": true,
    "files.autoSave": "afterDelay"
  }
}
```

### Post-Create Script (`post-create.sh`)
1. Install Python requirements
2. Login prompt for Azure CLI (`az login`)
3. Run `validate-environment.py` to verify connectivity
4. Print welcome message with challenge links

---

## 5. README.md Outline

```markdown
# 🤖 Build Intelligent Apps with Microsoft Foundry
> A What The Hack hackathon — from prompt to production

## What is this?
[2-3 sentence overview of the hackathon and WTH format]

## 🎯 Learning Outcomes
[Bullet list of what participants will achieve]

## 👥 Who is this for?
[Audience: students, coaches]

## 📋 Prerequisites
- Azure subscription
- GitHub account with Codespaces
- Python basics
- [Link to detailed setup guide]

## 🚀 Getting Started
1. Open in Codespaces / Dev Container
2. Authenticate with Azure
3. Start Challenge 00

## 🏆 Challenges
| # | Challenge | Duration | Difficulty |
|---|-----------|----------|------------|
| 00 | Setup & Orientation | 30 min | ⭐ |
| 01 | Your First Model Deployment | 45 min | ⭐ |
| 02 | Prompt Engineering & System Design | 1 hr | ⭐⭐ |
| 03 | Prompt Flow Orchestration | 1.5 hr | ⭐⭐⭐ |
| 04 | RAG — Grounding with Your Data | 1.5 hr | ⭐⭐⭐⭐ |
| 05 | Evaluation & Responsible AI | 1 hr | ⭐⭐⭐⭐ |
| 06 | Deploy & Integrate | 1 hr | ⭐⭐⭐⭐⭐ |

## 🧑‍🏫 For Coaches
[Link to coach hub with facilitation tips, common pitfalls, timing advice]

## 🏗️ Repository Structure
[Brief overview of folder layout]

## 📚 Resources
[Links to Microsoft Foundry docs, learning paths, community]

## 🤝 Contributing
[How to contribute improvements]

## License
[MIT or appropriate license]
```

---

## 6. GitHub Pages Site Map

### Navigation Structure

```
Home (/)
├── Getting Started (/setup)
│   ├── Prerequisites
│   ├── Environment Setup
│   └── Azure Subscription Setup
├── Challenges (/challenges)
│   ├── 00 — Setup & Orientation
│   ├── 01 — Your First Model Deployment
│   ├── 02 — Prompt Engineering
│   ├── 03 — Prompt Flow
│   ├── 04 — RAG
│   ├── 05 — Evaluation
│   └── 06 — Deploy & Integrate
├── Coach Hub (/coach-hub)
│   ├── Facilitation Guide
│   ├── Timing & Pacing
│   ├── Common Pitfalls per Challenge
│   └── Solution Guides (gated/separate)
└── FAQ (/faq)
```

### Theme & Style Recommendation

| Aspect | Recommendation |
|--------|---------------|
| **Jekyll theme** | `just-the-docs` — clean, searchable, sidebar navigation |
| **Color scheme** | Azure-aligned blues with high contrast |
| **Typography** | System font stack for speed; monospace for code blocks |
| **Navigation** | Left sidebar with challenge progression + status indicators |
| **Mobile** | Responsive (participants may use tablets during event) |
| **Search** | Enabled via just-the-docs built-in search |

### Page Content Strategy
- **Challenge pages on the site** render the student-facing README.md from `challenges/` (single source of truth)
- **Coach solutions** are NOT published to the public Pages site — they live in `challenges/*/solution.md` only (coaches clone the repo)
- **Home page** provides event overview and clear "Start Here" call-to-action

---

## 7. Work Breakdown

### 🔴 Rusty — Challenge Content Writer

| Task ID | Task | Dependencies | Priority |
|---------|------|--------------|----------|
| R-01 | Write `challenges/challenge-00-setup/README.md` (student guide) | Devcontainer ready | P0 |
| R-02 | Write `challenges/challenge-00-setup/solution.md` (coach guide) | R-01 | P0 |
| R-03 | Write `challenges/challenge-01-first-model/README.md` | R-01 | P0 |
| R-04 | Write `challenges/challenge-01-first-model/solution.md` | R-03 | P0 |
| R-05 | Write `challenges/challenge-02-prompt-engineering/README.md` | R-03 | P1 |
| R-06 | Write `challenges/challenge-02-prompt-engineering/solution.md` | R-05 | P1 |
| R-07 | Write `challenges/challenge-03-prompt-flow/README.md` | R-05 | P1 |
| R-08 | Write `challenges/challenge-03-prompt-flow/solution.md` | R-07 | P1 |
| R-09 | Write `challenges/challenge-04-rag/README.md` | R-07 | P2 |
| R-10 | Write `challenges/challenge-04-rag/solution.md` | R-09 | P2 |
| R-11 | Write `challenges/challenge-05-evaluation/README.md` | R-09 | P2 |
| R-12 | Write `challenges/challenge-05-evaluation/solution.md` | R-11 | P2 |
| R-13 | Write `challenges/challenge-06-deploy/README.md` | R-11 | P3 |
| R-14 | Write `challenges/challenge-06-deploy/solution.md` | R-13 | P3 |
| R-15 | Create `resources/sample-data/university-faq/` corpus (10-15 docs) | None | P1 |

**Content template for each challenge README.md:**
```markdown
# Challenge NN: [Title]

## Introduction
[Context and motivation — why this matters]

## Description
[What participants will build/accomplish]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] ...

## Learning Resources
- [Link 1 — official docs]
- [Link 2 — tutorial]

## Tips
- Hint 1 (vague — points in right direction)
- Hint 2 (slightly more specific)

## Advanced Challenges (Optional)
[Stretch goals for fast teams]
```

**Content template for each solution.md:**
```markdown
# Challenge NN: [Title] — Coach's Guide

## Overview
[What participants should accomplish and common approaches]

## Step-by-Step Solution
[Detailed walkthrough with code/screenshots]

## Common Pitfalls
[What teams typically get stuck on and how to unblock]

## Coaching Tips
[How to guide without giving answers; what questions to ask]

## Timing
[Expected pace; when to intervene if a team is stuck]
```

---

### 🟢 Linus — Frontend / GitHub Pages

| Task ID | Task | Dependencies | Priority |
|---------|------|--------------|----------|
| L-01 | Set up Jekyll with `just-the-docs` theme in `docs/` | None | P0 |
| L-02 | Create `docs/_config.yml` with navigation structure | L-01 | P0 |
| L-03 | Write `docs/index.md` (home page) | L-02 | P0 |
| L-04 | Write `docs/setup.md` (getting started guide) | L-02 | P1 |
| L-05 | Create challenge page template | L-02 | P1 |
| L-06 | Write `docs/challenges/challenge-00.md` through `challenge-06.md` | R-01+ | P1 |
| L-07 | Write `docs/coach-hub.md` | L-02 | P2 |
| L-08 | Write `docs/faq.md` | L-02 | P3 |
| L-09 | Style customization (colors, logo, branding) | L-01 | P2 |
| L-10 | Test responsive layout and navigation | L-06 | P2 |

---

### 🔵 Livingston — Infrastructure / DevOps

| Task ID | Task | Dependencies | Priority |
|---------|------|--------------|----------|
| V-01 | Create `.devcontainer/devcontainer.json` | None | P0 |
| V-02 | Create `.devcontainer/post-create.sh` | V-01 | P0 |
| V-03 | Create `resources/scripts/validate-environment.py` | V-01 | P0 |
| V-04 | Set up GitHub Actions workflow for Pages deploy | L-01 | P1 |
| V-05 | Create `resources/scripts/setup-resources.sh` (Azure provisioning) | None | P1 |
| V-06 | Configure branch protection / PR requirements | None | P3 |
| V-07 | Test devcontainer builds and connects to Azure | V-01, V-02 | P1 |

---

### 🟡 Basher — Validation & Testing

| Task ID | Task | Dependencies | Priority |
|---------|------|--------------|----------|
| B-01 | Walk through Challenge 00 end-to-end in devcontainer | V-01, R-01 | P1 |
| B-02 | Walk through Challenge 01 end-to-end | R-03, B-01 | P1 |
| B-03 | Walk through Challenge 02 end-to-end | R-05, B-02 | P2 |
| B-04 | Walk through Challenge 03 end-to-end | R-07, B-03 | P2 |
| B-05 | Walk through Challenge 04 end-to-end | R-09, B-04 | P2 |
| B-06 | Walk through Challenge 05 end-to-end | R-11, B-05 | P3 |
| B-07 | Walk through Challenge 06 end-to-end | R-13, B-06 | P3 |
| B-08 | Validate all links, code snippets compile/run | All content | P2 |
| B-09 | Time each challenge (verify estimates) | B-01 through B-07 | P2 |
| B-10 | Review coach guides for completeness | R-02+ | P2 |

---

### 🟣 Danny — Lead / Review

| Task ID | Task | Dependencies | Priority |
|---------|------|--------------|----------|
| D-01 | Write PLAN.md (this document) | None | P0 ✅ |
| D-02 | Write root README.md | PLAN.md | P0 |
| D-03 | Review all challenge content (Rusty's output) | R-* complete | P1 |
| D-04 | Review site pages (Linus's output) | L-* complete | P2 |
| D-05 | Final walkthrough and sign-off | All tasks | P3 |

---

## 8. Key Architectural Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| AD-01 | 7 challenges (00–06), linear dependency | Simpler logistics for 1-day events; no parallel tracks to manage |
| AD-02 | Challenge 00 is setup-only (no AI content) | Eliminates environment issues blocking learning |
| AD-03 | Coach solutions live in repo, not on Pages site | Coaches need full access; public site stays student-focused |
| AD-04 | `just-the-docs` Jekyll theme | Minimal config, great search, responsive, sidebar nav |
| AD-05 | Devcontainer as primary environment | Eliminates "works on my machine"; critical for hackathon reliability |
| AD-06 | RAG challenge uses provided sample data | Removes data-sourcing as a blocker; all teams work with same corpus |
| AD-07 | Evaluation before Deployment (Ch 05 before 06) | Teaches responsible AI practices before shipping to production |

---

## 9. Timeline & Execution Order

**Phase 1 — Foundation (immediate)**
- Danny: PLAN.md ✅, README.md
- Livingston: devcontainer, validation scripts
- Linus: Jekyll site scaffold

**Phase 2 — Core Content (days 1–3)**
- Rusty: Challenges 00–03 (student + coach guides)
- Linus: Site pages for challenges 00–03
- Livingston: Pages deploy workflow
- Basher: Validate challenges 00–01

**Phase 3 — Advanced Content (days 3–5)**
- Rusty: Challenges 04–06
- Linus: Remaining site pages, styling
- Basher: Validate challenges 02–06

**Phase 4 — Polish (days 5–7)**
- Danny: Full review pass
- Basher: Timing validation, link checking
- Linus: Final style/branding
- All: Bug fixes and polish

---

*Plan authored by Danny (Lead & Content Architect) — 2026-05-28*
