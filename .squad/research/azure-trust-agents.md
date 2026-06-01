# Research Notes: `microsoft/azure-trust-agents`

> **Repo:** https://github.com/microsoft/azure-trust-agents
> **Tagline:** "Automated Regulatory Compliance & Audit Hack" — build intelligent multi-agent
> financial-compliance workflows using the **Microsoft Agent Framework (MAF)**.
> **Researched:** 2026-06-01 by Rusty (Curriculum Designer). Research-only; no upstream changes.
> **Default deploy region:** Sweden Central. **Compute target:** GitHub Codespaces + Azure.

---

## 1. Overview & Scenario Framing

**Narrative:** You are a financial-services compliance team automating *regulatory compliance and
audit* with AI agents. The throughline is a **fraud-detection pipeline** that ingests transactions,
scores fraud risk against regulations (AML / KYC / CIP / EDD), produces audit-ready compliance
reports, raises real-time fraud alerts, and surfaces everything in an ops dashboard. The framing is
strong because every challenge maps to a *real role on a compliance team* (data analyst → risk
analyst → auditor → alerting/SOC → ops manager), so the agent roster reads like an org chart.

**Why the scenario drives engagement (per `README.md`):**
- Concrete, regulated, high-stakes domain (fraud + audit) — decisions are explainable and auditable,
  which is a natural fit for "show your reasoning" agent demos.
- A **single artifact evolves** across all 5 challenges: a 3-agent sequential pipeline → 4-agent
  parallel pipeline → observable pipeline → pipeline + frontend. No throwaway work.
- **"Right tool for the right job"** is the repeated design mantra (`README.md`,
  `challenge-2/readme.md`): Azure AI Foundry agents for conversational/stateful work, MCP for
  external system connectivity, rules for deterministic/auditable thresholds.

**Architecture (from root `README.md` + `images/architecture.png`):** four specialized agents —
Customer Data, Risk Analyzer, Compliance Report, Fraud Alert — orchestrated as a MAF Workflow that
fans out after risk analysis (compliance reporting + fraud alerting run in parallel).

**Data substrate (Challenge 0):** Azure Cosmos DB (`FinancialComplianceDB`) containers for
Transactions, Rules/Obligations, Alerts/Scores, Audit Reports; Azure AI Search index
`regulations-policies` holding unstructured regulation text. Seed data ships in
`challenge-0/data/` (`customers.json`, `transactions.json`, `regulations.jsonl`,
`ml_predictions.json`) and is loaded via `challenge-0/seed_data.sh`.

---

## 2. Challenge Inventory

| # | Name (path) | Learning objectives | MAF / Foundry features | Difficulty | Est. time |
|---|-------------|---------------------|------------------------|------------|-----------|
| 0 | **Setup & Data Ingestion** (`challenge-0/readme.md`) | Fork → Codespaces → deploy Azure infra (one-click ARM), retrieve keys, seed Cosmos + AI Search | ARM `azuredeploy.json`, APIM Basic v2, Cosmos DB, AI Search; `get-keys.sh` auto-writes `.env` | ★ Easy | 30 min |
| 1 | **Microsoft Agent Framework** (`challenge-1/README.md`) | Create 3 specialized agents; learn Executors/Edges/Workflows/Events; build a **sequential** workflow; visualize in DevUI | `ChatAgent`, `AzureAIAgentClient`, `create_agent`, `@executor`, `WorkflowBuilder().set_start_executor().add_edge().build()`, `HostedFileSearchTool`/`azure_ai_search` tool, Pydantic data contracts, DevUI | ★★★ Core | 60 min |
| 2 | **Connect to Alert MCP Server** (`challenge-2/readme.md`) | Expose a pre-built REST API as an **MCP server** via APIM (no code); build a 4th MCP-backed agent; evolve to **parallel fan-out** 4-agent workflow | APIM "Expose API as MCP Server (Preview)", `McpTool`, `RequiredMcpToolCall` + `SubmitToolApprovalAction` approval loop, subscription-key header auth, fan-out edges | ★★★ Core | 60 min |
| 3 | **Observability / Tracing** (`challenge-3/readme.md`) | Add OpenTelemetry tracing; export to App Insights; write KQL; build a Monitor Workbook; trace individual transactions end-to-end | OTel GenAI semantic conventions, `TelemetryManager` (`telemetry.py`), 3-tier spans (app/workflow/executor), business metrics, KQL, Azure Workbook template, batch runner | ★★★★ Advanced | 60 min |
| 4 | **Fraud Alert Frontend** (`challenge-4/README.md`) | Deploy an Angular dashboard on Container Apps; wire it to APIM; configure CORS; lock CORS to the frontend origin | Container Apps deploy (prebuilt image `ghcr.io/dsanchor/fraud-alert-management-front`), APIM CORS policy, secretref env vars | ★★ Easy-Med | 30 min |

**Total:** ~4 hours of hands-on. Progression is **scaffold → core build → core extend → harden →
ship**: env first, then the agentic core (1–2), then production hardening (3), then UX (4).

---

## 3. Multi-Agent / Workflow Patterns Used

**Framework:** Microsoft Agent Framework (MAF), the Oct-2025 SDK that merges Semantic Kernel +
AutoGen. Python is the hack's language.

**Core MAF primitives taught (Challenge 1 README):** Executors (processing units),
Edges (message routing/branching/fan-in/fan-out), Workflows (the executor+edge graph),
Events (real-time observability signals).

**Pattern 1 — Sequential orchestration (Challenge 1).** Graph-based, *not* a "Magentic"/manager
pattern. Three `@executor`-decorated async functions chained with explicit edges:
```python
# challenge-1/workflow/sequential_workflow.py (L535-539)
WorkflowBuilder()
  .set_start_executor(customer_data_executor)
  .add_edge(customer_data_executor, risk_analyzer_executor)
  .add_edge(risk_analyzer_executor, compliance_report_executor)
  .build()
```
Executors pass typed Pydantic messages via `await ctx.send_message(result)`; the terminal executor
emits results via `await ctx.yield_output(result)`. Data contracts are explicit Pydantic models
(`AnalysisRequest`, `CustomerDataResponse`, `RiskAnalysisResponse`, `ComplianceAuditResponse`).

**Pattern 2 — Parallel fan-out (Challenge 2).** Same builder, but the risk node fans out to *two*
downstream executors that run concurrently:
```python
# challenge-2/agents/sequential_workflow_chal2.py (L815-822)
WorkflowBuilder()
  .set_start_executor(customer_data_executor)
  .add_edge(customer_data_executor, risk_analyzer_executor)
  .add_edge(risk_analyzer_executor, compliance_report_executor)
  .add_edge(risk_analyzer_executor, fraud_alert_executor)   # fan-out
  .build()
```

**Pattern 3 — Hybrid agent clients ("right tool for the right job").** Mixes **Azure AI Foundry
persistent agents** (`AzureAIAgentClient` + `ChatAgent`, conversational/stateful, registered in
Foundry with reusable `asst_…` IDs) with a **responses/MCP-backed agent** for the stateless
alerting call. Agents are created once (`project_client.agents.create_agent(...)`) and rebound by ID
from `.env` during orchestration — decoupling agent authoring from workflow wiring.

**Pattern 4 — Tool typing.**
- *Knowledge tool:* Risk Analyzer attaches Azure AI Search as a native tool
  (`tools=[{"type": "azure_ai_search"}]` + `tool_resources` pointing at index `regulations-policies`),
  giving explainable, citation-bearing risk reasoning (`challenge-1/agents/risk_analyser_agent.py`).
- *Action tool:* Fraud Alert agent attaches an MCP server as a tool with an explicit
  human/tool-approval loop (`McpTool`, `RequiredMcpToolCall`, `SubmitToolApprovalAction`,
  `ToolApproval`) — a clean teaching example of governed tool execution
  (`challenge-2/agents/fraud_alert_foundry_agent.py`).

**Pattern 5 — Hybrid rule + AI decisioning.** Deterministic, auditable thresholds (amount >$10k,
high-risk countries NG/IR/RU/KP, account age <30d, device trust <0.5; score bands 0–49/50–74/75–100)
are baked into prompts *and* post-processed in code (`generate_audit_report_from_risk_analysis`),
while AI handles NL regulation interpretation and narrative. This directly teaches "explainable AI
for regulated domains."

**Observability as a first-class pattern (Challenge 3).** `TelemetryManager` wraps OTel with
three span tiers (application → workflow → executor) plus custom business metrics
(`fraud_detection.transactions.processed`, `…risk_score.distribution`, `…compliance.decisions`).
~42 traces per transaction; exported to App Insights and explored via KQL + a JSON Workbook
(`challenge-3/workbooks/azure-workbook-template.json`).

> **Note on red teaming / evals:** There is **no** dedicated evaluation harness or red-teaming
> challenge in this repo. "Trust" here means *observability + auditability + explainability*, not
> safety evals. This is a gap worth noting (see §5).

---

## 4. Coaching & Curriculum-Design Techniques Worth Borrowing

1. **One evolving artifact, five acts.** The deal is a single fraud pipeline that grows each
   challenge (3→4 agents, +tracing, +UI). Each `Conclusion` ends with a "What's Next" teaser that
   literally previews the next challenge's first paragraph — strong narrative momentum.
2. **Role-as-agent mapping.** Each agent embodies a real compliance-team role, making abstract
   "multi-agent orchestration" instantly intuitive. Borrow this: map agents to org roles in our
   scenario.
3. **Provide-the-API, teach-the-wiring.** Challenge 2 explicitly says "we will *not* implement the
   alerting logic — just configure and connect." Pre-built backends (Container App API, Angular
   frontend) keep learners on the *learning objective* (MCP, orchestration) not boilerplate.
4. **Placeholder-driven code completion.** Challenge 2's `mcp_tool = < PLACEHOLDER FOR MCP TOOL >`
   gives a single, high-signal "you write this one line" moment with the exact answer shown right
   below — low-friction but still hands-on. Good difficulty calibration.
5. **DevUI before tracing.** Challenge 1 uses the visual DevUI (node graph: green=done,
   purple=running, black=pending) to build intuition *before* Challenge 3 introduces rigorous OTel
   tracing. Visual-first, instrument-later sequencing.
6. **Explicit data contracts taught early.** Pydantic models as "workflow data contracts" are
   introduced in Challenge 1 §4 — teaches type-safe agent I/O as a named concept, not an
   afterthought.
7. **"Why this option" decision tables.** Challenge 3 has a comparison matrix (App Insights vs OTLP
   vs VS Code AI Toolkit) with a clear recommendation + rationale. Teaches *judgment*, not just
   steps.
8. **Copy-paste-runnable everything.** Every step is a shell/KQL/Python block with expected screenshots
   and "your plot should look like this" verification anchors. Heavy use of inline `![image]`
   checkpoints reduces "am I on track?" anxiety.
9. **Per-challenge duration + difficulty banner** at the top of every readme sets expectations.
10. **One-click ARM + auto-`.env`.** `azuredeploy.json` Deploy-to-Azure button + `get-keys.sh`
    populating `.env` removes the classic "setup eats the morning" failure mode.
11. **Run-individually then run-orchestrated.** Each agent has a `python <agent>.py` smoke-test
    before it's wired into the workflow — isolates failures and builds confidence incrementally.

---

## 5. Gaps / Things We'd Do Differently

- **No evaluation or red-teaming challenge.** Despite the "trust" branding, there's no eval harness
  (groundedness, accuracy of risk scores), no adversarial/jailbreak testing, no AI Foundry
  Evaluations or red-team agent. *We should add a dedicated evals + safety challenge* — it's the most
  conspicuous omission for a "trust" hack.
- **Brittle string parsing between agents.** Risk→Compliance handoff uses regex on free-text
  (`parse_risk_analysis_result`, e.g. `r'risk\s*score[:\s]*(\d+)'`). Fragile; we'd use structured
  outputs / typed tool responses end-to-end instead of re-parsing prose.
- **Security shortcuts called out but not taught.** Challenge 0 explicitly uses key-based auth +
  public network access "for convenience." A short "harden it" appendix (Managed Identity, private
  endpoints) would round out the enterprise story.
- **No Magentic / manager-planner pattern.** Only sequential + fan-out are taught. A stretch
  challenge using a manager/orchestrator agent (dynamic planning) would showcase the more advanced
  MAF orchestration the framework is known for.
- **No automated grading / completion checks.** Validation is "compare your screenshot to ours."
  Our hack could ship a `validate.py` per challenge (we already do this pattern in
  `resources/scripts/validate-environment.py`).
- **Single-region dependency (Sweden Central).** Model availability assumptions can bite learners;
  we'd document fallbacks more prominently.
- **Frontend lives in a separate repo** (`dsanchor/fraud-alert-management-front`) — external
  dependency risk. We'd vendor or pin it.
- **Heavy hardcoded business logic in prompts** (country lists, thresholds) duplicated across
  challenges — a config/source-of-truth file would reduce drift.

---

## 6. Reusable Assets Worth Referencing

| Asset | Path / URL | Why it's useful |
|-------|-----------|-----------------|
| One-click infra | `challenge-0/infra/azuredeploy.json` | ARM template: Cosmos + AI Search + APIM Basic v2 + Container Apps + App Insights in one deploy |
| Key bootstrap script | `challenge-0/get-keys.sh` (23KB) | Pattern for auto-generating `.env` from a deployed RG |
| Seed script + data | `challenge-0/seed_data.sh`, `challenge-0/data/*` | Reusable synthetic fraud dataset (customers/transactions/regulations/ml_predictions) |
| Sequential workflow reference | `challenge-1/workflow/sequential_workflow.py` (+ `.ipynb`) | Canonical MAF `WorkflowBuilder` + `@executor` + Pydantic-contract example |
| Parallel fan-out workflow | `challenge-2/agents/sequential_workflow_chal2.py` (L815-822) | Fan-out edge pattern from one node to two concurrent executors |
| MCP-tool agent w/ approval loop | `challenge-2/agents/fraud_alert_foundry_agent.py` | `McpTool` + `RequiredMcpToolCall`/`SubmitToolApprovalAction` governed tool execution |
| AI-Search-as-tool agent | `challenge-1/agents/risk_analyser_agent.py` | `create_agent(... tools=[{"type":"azure_ai_search"}], tool_resources=...)` |
| Telemetry manager | `challenge-3/telemetry.py` (456 lines) | Reusable 3-tier OTel + App Insights wrapper with business metrics |
| KQL + Workbook | `challenge-3/readme.md` (KQL blocks), `challenge-3/workbooks/azure-workbook-template.json` | Ready-made fraud-KPI dashboard JSON + timechart/piechart KQL |
| Batch simulator | `challenge-3/batch_run/batch_runner.py`, `multi_transaction_simulator.py` | Generate load for dashboard/observability demos |
| DevUI harness | `challenge-1/devui/` (`devui_launcher.py`) | Directory-based agent/workflow discovery + web UI for demos |
| APIM→MCP how-to | `challenge-2/readme.md` + https://learn.microsoft.com/azure/api-management/export-rest-mcp-server | Expose any REST/OpenAPI API as an MCP server with zero code |
| MAF docs anchors | https://learn.microsoft.com/agent-framework/overview/agent-framework-overview ; workflows/sequential | Canonical concept links the repo leans on |

---

### Plain-text summary (strongest ideas to adopt)

The single most powerful design move is the **one-artifact-five-acts arc**: a single fraud-compliance
pipeline that visibly grows each challenge (3→4 agents, then tracing, then a UI), with each
conclusion teasing the next challenge so momentum never resets. Equally worth stealing is the
**role-as-agent mapping** — every agent is a recognizable compliance-team job, which makes
"multi-agent orchestration" click instantly. Their **provide-the-backend, teach-the-wiring** discipline
(pre-built APIs/frontends, a single `< PLACEHOLDER >` line to complete) keeps learners on the actual
learning objective and calibrates difficulty well, while **one-click ARM + auto-`.env`** kills the
setup-eats-the-morning failure mode. The biggest thing we'd do *differently* is add what they're
missing despite the "trust" branding: a **dedicated evaluations + red-teaming challenge** and
**structured (non-regex) inter-agent contracts**, plus per-challenge automated validation scripts.
