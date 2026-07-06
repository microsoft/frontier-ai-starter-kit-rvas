# AI Starter Kit RVAS — Curriculum V3 (Tier Tree + De-Guided Advanced + MAF Capstone)

> **"Build Intelligent Agents with Microsoft Foundry"**
>
> Successor planning doc to [PLAN-V2.md](PLAN-V2.md). This document **does not replace** PLAN-V2 —
> it **extends** it. Where the two disagree, V3 wins on three things only: (1) the **3-tier tree**
> replaces the V2 "two-tier" framing, (2) the **Advanced tier is de-guided** (less placeholder-fill,
> more real authoring), and (3) a **new Tier 3 Capstone** turns the single Northfield IQ agent into a
> **multi-agent MAF system**. Everything else in PLAN-V2 (the Foundations spine, the Northfield
> narrative, the `.env` contract, the Extras) stands. Authored by Danny (Lead & Content Architect),
> 2026-06-01.
>
> **Driving inputs:** the FrontierWeekHack agent-lifecycle lab **[FWH]**, the azure-trust-agents
> one-artifact / role-as-agent / MAF hack **[ATA]**, and the microsoft/skills Copilot enablement
> library **[SKILLS]**. Full notes in `.squad/research/`; citations inline below.

---

## 0. What V3 Supersedes (read this first)

| PLAN-V2 says… | V3 changes it to… | Why |
|---|---|---|
| **"Two tiers"** (Foundations → Advanced+Extras) | **Three tiers** (Foundations → Advanced → **Capstone**), plus a cross-cutting *make-it-your-own* branch | The Advanced tier currently terminates the journey at "ship one agent." A capstone gives the curriculum a *headline finale* and a reason to learn MAF. **[ATA §1]** |
| Advanced activities sized **1–1.25 hr each**, "guided" | Each Advanced activity gets a **guided path** (revised, honest time) **and** a **build-from-scratch path** (longer, fewer placeholders) | The guided paths are over-scaffolded — see §2. Real authoring is where the learning is. **[ATA §4.4 critique]** |
| Extras are a flat list under Tier 2 | Extras are **re-slotted** into the tree by role (deepeners vs. capstone-feeders vs. cross-cutting) | Makes the optional content legible — learners can see *why* each Extra exists and when to do it. |
| Magentic (Extra C) + Hosted Long-Running (Extra D) are **Extras** | They are **promoted to feed the Tier 3 Capstone** (the capstone *is* the multi-agent build; D is its deploy variant) | The strongest content shouldn't be buried as "optional extra #3." |

**Unchanged and authoritative:** the Foundations 4-step spine, the bootstrap skip-path + single
`validate-foundations.py` checkpoint, the **`.env.sample` contract** (do not touch — see §5.4), the
Standard STEP Template, and "Prompt Flow is removed everywhere."

---

## 1. Vision — The 3-Tier Tree

The curriculum is a **tree**, not a line. You **climb a guided trunk** (Foundations), then **fan out
across modular branches** (Advanced) you pick in any order, then **converge on an open-ended summit**
(Capstone) where you compose everything into a multi-agent system. An optional **"make it your own"**
branch lets a team reskin the whole tree to a domain they care about.

```text
                       ┌───────────────────────────────────────────────┐
   TIER 1              │  FOUNDATIONS   (guided · linear · everyone)     │
   Foundations  ──────▶│  Step1 ─▶ Step2 ─▶ Step3 ─▶ Step4              │
   "follow the path"   │  Setup    Model    Agent    Knowledge Base     │
                       └───────────────────────┬───────────────────────┘
                                               │  ◀── Foundations END-STATE
                            (bootstrap skip ───┤      deployed, grounded
                             azd up + setup,   │      Northfield IQ Assistant)
                             1 checkpoint)     │
                                               ▼
   TIER 2        ┌──────────────── ADVANCED (modular · pick ANY order) ───────────────┐
   Advanced      │   Action Tools     Evaluation+RedTeam     Tracing     Deploy         │
   "choose your  │   ⭐⭐⭐            ⭐⭐⭐⭐               ⭐⭐⭐⭐     ⭐⭐⭐⭐⭐       │
    branches"    │     │                  │                    │           │            │
                 │  deepeners:  Fabric IQ · Voice Live · Build a UI · Copilot-Assisted   │
                 └─────┴──────────────────┴────────────────────┴───────────┴────────────┘
                                               │
                                               ▼
   TIER 3        ┌────────────── CAPSTONE (open-ended · design brief) ─────────────────┐
   Capstone      │   "Northfield IQ — Multi-Agent" : a MAF triage/router that fans out  │
   "lead the     │    to specialist agents (knowledge, actions) and converges.          │
    way"         │    Build visual-first in DevUI, then trace it. [ATA §3][FWH §2 Ch4]   │
                 │       ↳ deploy variant: Hosted Long-Running MAF (background runs)     │
                 └─────────────────────────────────────────────────────────────────────┘
                                               ▲
   CROSS-CUTTING ┌─────────────────────────────┴───────────────────────────────────────┐
   "make it      │  MAKE IT YOUR OWN  —  swap Northfield for YOUR domain (claims, ops,   │
    your own"    │  retail, healthcare). A Copilot "lab-generator" meta-agent scaffolds  │
                 │  the corpus + agents + eval set. Applies at ANY tier.   [FWH §4.9]    │
                 └─────────────────────────────────────────────────────────────────────┘
```

### 1.1 Progression logic — guided → modular → autonomous

The three tiers are deliberately **decreasing in guidance** and **increasing in learner agency**:

| Tier | Guidance level | Shape | What the learner supplies | Pedagogical job |
|---|---|---|---|---|
| **1 — Foundations** | **High** (step-by-step, copy-runnable) | Linear trunk | Follows instructions; fills tiny gaps | Build *vocabulary & muscle memory*: model, agent, knowledge base, citations. **[FWH §4.2 "explain the sequence"]** |
| **2 — Advanced** | **Medium** (goal + tasks + success criteria, some real authoring) | Modular fan | Authors real code in a starter scaffold; makes design choices | Build *competence per concept*: actions, safety, observability, deploy — independently, in any order. |
| **3 — Capstone** | **Low** (design brief + acceptance criteria only) | Open summit | Designs the agent org-chart and wires it themselves | Demonstrate *synthesis & judgment*: compose the pieces into a system that works. **[ATA §4.1 one-artifact arc]** |

This mirrors how both reference repos *should* have been sequenced: FWH and ATA are excellent at Tier
1–2 guidance but **neither offers an open-ended capstone** — ATA stops at a fixed fan-out workflow,
FWH stops at a portal DAG. The autonomy gradient is V3's signature.

### 1.2 The "make it your own" branch (cross-cutting)

A team that finishes Foundations can, instead of (or alongside) the Northfield branches, **reskin the
entire tree** to a domain they care about — insurance claims, factory maintenance, retail support,
clinic intake. This is lifted directly from FWH's **pick-your-scenario, shared-spine** design
**[FWH §4.1]** and powered by its **`lab-generator` meta-agent** **[FWH §4.9, §6]**: a Copilot custom
agent that generates a fresh corpus, two-to-three agents, an eval dataset, and a facilitator guide for
*any* vertical, following the same structure. We ship this as **Extra: Copilot-Assisted Build** today
(see §4) and elevate it here to a **first-class branch** because it is the single most reusable asset
in either repo. It applies at any tier — most powerfully at the Capstone, where "your domain, your
agent org-chart" is the most memorable demo a team can give.

---

## 2. De-Guiding the Advanced Tier

**Verdict (building on the Coordinator's assessment):** the Advanced tier is **real, but
over-scaffolded**, and its clock labels are **optimistic for what they actually ask**. The problem is
**not** that the activities are short — it's that the *guided paths spoon-feed the hard parts*. Three
of the four lean on the ATA-style **"provide the API, fill one PLACEHOLDER"** pattern **[ATA §4.3,
§4.4]**, which caps difficulty by design. The fix is **DEPTH, not clock-padding**: remove the
placeholders that matter, offer a **build-from-scratch path**, and add genuine stretch goals.

Below, each activity gets: *(a)* the specific thin step, *(b)* PLACEHOLDERs to remove, *(c)* a
build-from-scratch variant, *(d)* 1–2 stretch goals, and *(e)* an honest revised time split.

### 2.1 Action Tools — *the thinnest one*

**Current thin spots.** The backend is fully provided (`scripts/action-backend/`), the agent file
[activities/advanced-action-tools/agent_with_actions.py](activities/advanced-action-tools/agent_with_actions.py)
hands the learner three `# TODO`s, and **Step 1 ("knowledge vs. action tools") is a verbal,
no-script conceptual step** — pure reading. The only real authoring is `build_action_tool()` (≈3
lines) and the approval loop in `run_with_approval()` (≈10 lines). That is **~30–45 min of real work**
against a **1.25 hr** label. **[matches Coordinator assessment]**

**PLACEHOLDERs to remove (so learners author real code):**
- `build_action_tool()` — keep as authoring, but **stop sketching `tools=tool.definitions` in
  `main()`**. Make the learner discover that an `McpTool` exposes `.definitions` and wire it themselves.
- `run_with_approval()` — currently the loop skeleton (`while run.status in (...)`) is provided and
  only the *body* is a placeholder. **Remove the skeleton.** Give them the state machine in prose
  ("a run can be `requires_action`; you must inspect, decide, submit, re-poll") and have them author
  the whole loop. This is the actual learning objective.
- Delete the `tool_approvals = []  # < PLACEHOLDER >` breadcrumb — it telegraphs the answer.

**Build-from-scratch variant ("no starter file"):** ship **only** the backend + a one-paragraph spec
("attach `northfield_actions` as an MCP tool; require human approval on every call; deny cleanly").
The learner writes `agent_with_actions.py` from an empty file. The validator (`validate.py --all`) is
the contract — it already asserts the observable behavior, so it grades either path.

**Stretch goals (genuine):**
1. **Build the MCP server, don't just wire it.** Add a *fourth* action (`waive_late_fee`) end-to-end:
   implement the REST handler in `app.py`, expose it through `mcp_server.py` (FastMCP), and attach it.
   This crosses the "provide-the-API" line ATA never crosses **[ATA §5 critique]** and teaches the
   *server* side of MCP, not just the client.
2. **Selective approval policy.** Auto-approve read-ish/low-risk tools (e.g. a hypothetical
   `lookup_balance`) but require approval for state-changing ones — a real governance pattern, not
   "approve everything."

**Honest time:** **Guided path 45 min** (relabel from 1.25 hr — it was never that). **Build-from-
scratch path 1.5 hr.** With Stretch #1 (build the server): **+45 min**.

### 2.2 Evaluation & Red Teaming — *the genuinely meaty one*

**Current state.** This is the deepest Advanced activity as written: 5 steps, real `evaluate.py`, a
custom `NorthfieldDomainEvaluator`, a 36-row dataset, a labeled adversarial seed set, and a CI gate.
The Coordinator's "eval is genuinely meatier" call is correct. **It is the closest to right-sized.**
Light touch only.

**Thin spot.** Step 3 ("extend the custom evaluator with **one** rule") and Step 4's red-teaming are
where it can get shallow — a learner can satisfy Step 4 by *manually pasting prompts* and never wiring
the `RedTeam` / `IndirectAttackEvaluator` automation the step *offers but doesn't require*.

**PLACEHOLDERs / soft-spots to harden:**
- Make the **automated red-team run mandatory**, not "or run manually." Require an actual
  `RedTeam(...).scan(...)` (or `IndirectAttackEvaluator`) invocation with results on record — manual
  prompting becomes the *warm-up*, not the deliverable.
- Step 3: require **two** custom rules (one groundedness-proxy, one domain-correctness), and require
  the learner to show a row where the rules *disagree* with a built-in metric — that's where judgment
  lives.

**Build-from-scratch variant:** provide the datasets only (`northfield-eval.jsonl`,
`adversarial-seed.jsonl`) and the CI-gate spec; have the learner author `evaluate.py` (loader +
built-in evaluators + custom evaluator + `--gate`) from scratch. The current file becomes
`solution.md` reference.

**Stretch goals:**
1. **Trace-to-eval correlation.** After the Tracing activity, curate a *new* eval dataset **from
   production traces** (the App Insights rows) and re-run — closes the eval↔trace loop **[SKILLS §2a
   foundry-observability; FWH §5 "dataset curation from traces"]**.
2. **Regression CI in GitHub Actions.** Wire `evaluate.py --gate` into a real workflow that fails a PR
   — both reference repos describe this but ship no Action **[FWH §5, ATA §5]**.

**Honest time:** **Guided path 1.25 hr is accurate** (keep). **Build-from-scratch path 2 hr.**
Stretch #2 (real CI): **+30 min.**

### 2.3 Tracing & Observability

**Current thin spots.** Step 1 and Step 2 **paste the full `trace_setup.py` and `traced_run.py`**
verbatim in the README — the learner copies, runs, and reads. The genuine learning (the *set-env-
before-import* gotcha, the span tiers, the KQL) is all there, but as **reading, not authoring**. Real
authoring is effectively zero until the Step 4 KQL.

**PLACEHOLDERs to remove (convert copy-paste → author):**
- **Stop pasting the full `trace_setup.py`.** Give the **ordering rule** ("env flags above all
  `azure.ai.*` imports") and the **three function calls they need** (`configure_azure_monitor`,
  `AIProjectInstrumentor().instrument()`, resolve the connection string) as a checklist — let them
  assemble the file. Keep the gotcha box (it's the lesson).
- Step 4: ship the **starter** KQL only (already done) and require the learner to **author the
  end-to-end correlation query** (join model+retrieval+tool spans by `operation_Id`, compute total
  tokens + latency) themselves, rather than reading the finished `correlate.kql`.

**Build-from-scratch variant:** "instrument the Foundations agent and answer five questions about one
run" (tokens, latency-per-span, which span retrieved, cost estimate, the slowest hop) — no code given,
only the package list and the gotcha. The validator checks for ≥1 emitted GenAI span.

**Stretch goals:**
1. **Ship ATA's 3-tier `TelemetryManager` + Workbook JSON** as an optional reference and have the
   learner add **one custom business metric** (e.g. `northfield.answers.uncited`) and chart it
   **[ATA §3, §6]**.
2. **Batch-run + dashboard.** Adapt ATA's `batch_runner.py` to fire 20 questions and build a KQL
   timechart of token cost over the run **[ATA §6]**.

**Honest time:** **Guided path 1 hr is roughly right** but currently feels like 35 min of real work
because of the paste-and-run; de-guiding restores it to a genuine **1 hr**. **Build-from-scratch path
1.5 hr.**

### 2.4 Deploy as a Hosted Agent

**Current thin spots.** Step 1 **pastes the complete `agent.yaml`, `main.py`, and `Dockerfile`**;
Step 2 and Step 3 paste the exact `az acr build` / `azd ai agent` / `invoke_hosted.py` commands. The
hard, real-world parts (the `--source-acr-auth-id "[caller]"` flag, the async `status==active` gate,
the two-identity auth model) are **explained**, which is good — but the learner *types nothing they
designed*. The difficulty here is **operational** (things fail async), not authoring, so this one is
**legitimately ⭐⭐⭐⭐⭐ in friction** even though the keystrokes are few.

**PLACEHOLDERs to remove:**
- **Don't paste the full `agent.yaml`.** Give the required keys (`name`, `model.deployment`,
  `instructions`, `protocols: responses/1.0.0/port 8088`) and have them author it. Same for the
  Dockerfile (give constraints: slim base, `linux/amd64`, expose 8088).
- Keep `main.py` mostly given (the MAF server host is genuine API surface to look up via
  `microsoft-docs` MCP), but require them to **find the current class name** rather than copy it —
  enforces Search-Before-Implement **[SKILLS §3]**.

**Build-from-scratch variant:** "containerize and deploy the Foundations agent; prove it answers
authenticated and rejects anonymous; show its per-agent identity principal id." No YAML/Dockerfile
given — only the success criteria and the gotcha list (unique tag, `--source-acr-auth-id`, async
gate).

**Stretch goals:**
1. **Blue/green a new version.** Deploy a v2 (tweaked instructions), confirm both versions exist, and
   roll the active pointer — teaches versioned hosted agents.
2. **Harden auth.** Grant the per-agent MI the *minimum* data-plane roles to reach the KB and prove a
   missing role yields `403` — the security story ATA explicitly skips **[ATA §5 "harden it"]**.

**Honest time:** **Guided path 1 hr is accurate** (the async waits eat real wall-clock). **Build-
from-scratch path 1.5 hr.** Stretch #1 (blue/green): **+30 min.**

### 2.5 Summary — revised Advanced time table

| Advanced activity | V2 label | **V3 guided** | **V3 build-from-scratch** | Top stretch (+time) |
|---|---|---|---|---|
| Action Tools | 1.25 hr | **45 min** | **1.5 hr** | Build the MCP server (+45 min) |
| Evaluation & Red Teaming | 1.25 hr | **1.25 hr** (keep) | **2 hr** | Real CI gate (+30 min) |
| Tracing & Observability | 1 hr | **1 hr** | **1.5 hr** | TelemetryManager + custom metric (+30 min) |
| Deploy as a Hosted Agent | 1 hr | **1 hr** | **1.5 hr** | Blue/green version (+30 min) |
| **Totals** | **4.5 hr** | **~4 hr guided** | **~6.5 hr scratch** | — |

**Reading of the verdict:** the Advanced tier doesn't take *longer* than labeled in aggregate — Action
Tools was simply *mislabeled* (1.25 hr → 45 min), and the others are roughly honest. What it lacks is
**depth and agency**, which the dual-path (guided vs. scratch) + stretch goals + the new Capstone
supply. **We do not pad the clock; we deepen the work.**

---

## 3. Tier 3 — The Capstone (NEW — the headline addition)

> **`activities/capstone-multi-agent/`** — *"Northfield IQ, the Team."* Take the single grounded,
> action-taking assistant you built and **break it into a coordinated team of agents** orchestrated
> with the **Microsoft Agent Framework (MAF)**. Deliberately **less guided**: this is a **design brief
> + acceptance criteria**, not a placeholder-fill. You decide the org-chart; you wire the graph.

### 3.1 Why a capstone, and why MAF

Tiers 1–2 prove a learner can build *one* agent and make it act, prove it safe, observe it, and ship
it. The capstone proves they can **compose** — the actual shape of production agentic systems. Neither
reference repo offers this open-endedly: ATA ships a *fixed* sequential→fan-out workflow **[ATA §3
Patterns 1–2]** and FWH ships a *fixed* portal DAG **[FWH §4.7]**; **neither hands the org-chart to the
learner.** MAF is the right tool because it's the Oct-2025 SDK that merges Semantic Kernel + AutoGen
and is exactly what ATA teaches **[ATA §3]** — and our Extras already seed it (Magentic, Hosted
Long-Running).

### 3.2 Learning objectives

By the end, a team can:
1. **Decompose** a monolithic agent into specialist roles with explicit responsibilities (role-as-
   agent) **[ATA §4.2]**.
2. Use MAF **primitives** — Executors, Edges, Workflows, Events — and the `WorkflowBuilder` to wire a
   graph **[ATA §3]**.
3. Build a **sequential** workflow first, then evolve it to **parallel fan-out** **[ATA §3 Patterns
   1–2]**.
4. Add a **triage/router** that *decides* which specialist(s) to invoke (the step beyond ATA's static
   fan-out).
5. Pass **typed (Pydantic) data contracts** between agents instead of regex-parsing prose **[ATA §5
   critique]**.
6. **Visualize first in DevUI** (green=done / purple=running / black=pending), **then instrument** with
   the tracing they already learned **[ATA §4.5 visual-first]**.
7. (Deploy variant) Host the workflow with a **long-running/background** agent for async work
   **[SKILLS §2a foundry-hosted-agents]**.

### 3.3 The agent org-chart (role-as-agent)

The single Northfield IQ Assistant becomes a **student-services desk team**:

```text
                         ┌──────────────────────────┐
            student ────▶│   TRIAGE / ROUTER agent   │   "what kind of request is this?"
            question     │   (classifier, no tools)  │   → routes to 1..N specialists
                         └─────────────┬─────────────┘
                       ┌───────────────┼────────────────┐
                       ▼               ▼                ▼
            ┌────────────────┐ ┌────────────────┐ ┌────────────────────┐
            │ KNOWLEDGE agent │ │  ACTION agent   │ │  ESCALATION agent  │
            │ (AI Search /    │ │ (MCP tools +    │ │ (human-handoff;    │
            │  Foundry IQ KB) │ │  approval loop) │ │  out-of-scope)     │
            │  [Foundations]  │ │ [Action Tools]  │ │                    │
            └───────┬────────┘ └───────┬────────┘ └─────────┬──────────┘
                    └──────────────────┼────────────────────┘
                                       ▼
                         ┌──────────────────────────┐
                         │   SYNTHESIZER  (fan-in)   │  merges specialist outputs into
                         │                           │  one cited, governed answer
                         └──────────────────────────┘
```

Every box is a **real role on a student-services desk** — that's the ATA insight that makes "multi-
agent orchestration" click instantly **[ATA §4.2]**. Each specialist **reuses an artifact the team
already built**: Knowledge = the Foundations KB agent; Action = the Action Tools agent + its approval
loop; Triage/Escalation are new, small, tool-less reasoners (the FWH "reasoner-without-tools"
archetype **[FWH §4.4]**).

### 3.4 MAF primitives — the build, in two passes

**Pass 1 — sequential (warm-up).** Triage → Knowledge → Synthesizer, chained with explicit edges
**[ATA §3 Pattern 1]**:

```python
# illustrative — confirm current MAF surface via microsoft-docs MCP before coding
WorkflowBuilder()
  .set_start_executor(triage_executor)
  .add_edge(triage_executor, knowledge_executor)
  .add_edge(knowledge_executor, synthesizer_executor)
  .build()
```

**Pass 2 — parallel fan-out.** Triage fans out to Knowledge **and** Action concurrently; both
converge on the Synthesizer (fan-in) **[ATA §3 Pattern 2]**:

```python
WorkflowBuilder()
  .set_start_executor(triage_executor)
  .add_edge(triage_executor, knowledge_executor)   # fan-out
  .add_edge(triage_executor, action_executor)      # fan-out
  .add_edge(knowledge_executor, synthesizer_executor)  # fan-in
  .add_edge(action_executor,    synthesizer_executor)  # fan-in
  .build()
```

Executors pass **typed Pydantic messages** via `await ctx.send_message(result)`; the terminal executor
emits via `await ctx.yield_output(result)` — typed contracts end-to-end, **no regex prose-parsing**
**[ATA §3, §5 critique]**.

**Stretch — Magentic manager/planner.** Replace the hand-wired Triage edges with a **MAF Magentic
manager** that *plans dynamically* which specialists to call — the advanced orchestration neither
reference repo ships **[ATA §5 "no Magentic"]**. This is exactly what Extra C already scaffolds (§4).

### 3.5 Visual-first, then traced

1. **DevUI first.** Launch the workflow in MAF's DevUI and *watch* the graph light up as a question
   flows through — build intuition before rigor **[ATA §4.5]**. Reuse ATA's directory-based
   `devui_launcher.py` pattern **[ATA §6]**.
2. **Then instrument.** Turn on the OTel tracing from the Tracing activity and confirm you now get a
   **multi-span tree across agents** (triage → fan-out → fan-in), correlated by `operation_Id`. The
   capstone is where Tracing pays off: ~N spans per question across the team.

### 3.6 "Make it your own" scenario-swap

The capstone is the **best place** to reskin: swap the Northfield student-services desk for **any**
org-chart domain — insurance *claims triage → decision* **[ATA scenario]**, factory *anomaly →
diagnosis* **[FWH factory]**, retail *intent → resolution* **[FWH callcenter]**. The agent graph shape
is identical; only the corpus, the specialist prompts, and the eval set change. Teams can hand-author
the swap **or** use the Copilot **lab-generator** meta-agent to scaffold it **[FWH §4.9, §6]**. This is
the single most demo-able moment of the whole event: *"here's our agent team for **our** domain."*

### 3.7 Acceptance criteria (graded — no step-by-step)

A capstone submission passes if **all** of these are demonstrably true (the team shows it; a light
`validate.py` checks the structural ones):

- [ ] **≥ 3 agents** with distinct roles, at least one **router/triage** that *decides* routing and at
      least two **specialists**.
- [ ] The workflow runs **both** a sequential and a **parallel fan-out** topology (show both graphs).
- [ ] **Typed Pydantic contracts** flow between agents — no free-text regex parsing between hops.
- [ ] At least one specialist reuses the **Foundations KB** (grounded, cited) and one reuses the
      **Action Tools approval loop** (governed).
- [ ] The run is **visualized in DevUI** and **traced** end-to-end (a multi-agent span tree by
      `operation_Id`).
- [ ] A **2-minute demo** narrates one question's journey through the team.
- [ ] *(Stretch / deploy variant)* the workflow is **hosted** with a **background/long-running** run
      that completes after the tab is closed **[Extra D]**.

> **Guidance level is intentionally LOW.** We give the org-chart sketch, the two `WorkflowBuilder`
> snippets, the acceptance criteria, and pointers to the skills/MCP — **not** a placeholder file. The
> learning *is* the design and wiring. This is the autonomy payoff of the tree. **[§1.1]**

### 3.8 Capstone time & placement

- **Guided-ish core (sequential + fan-out + DevUI + trace):** **2–2.5 hr.**
- **+ Magentic manager stretch:** **+1 hr.**
- **+ Hosted long-running deploy variant (Extra D absorbed):** **+1.5 hr.**
- **Prereqs:** Foundations end-state **+** Action Tools (for the Action specialist). Tracing strongly
  recommended (Step 5 leans on it). Deploy required only for the hosted variant.
- **Placement:** Day-2 / showcase finale. It is the natural home for the **Build a UI** Extra (put a
  face on the team) and the **"make it your own"** branch.

---

## 4. New Activity Ideas Backlog (mined from both repos)

Each idea lists **source**, **what it teaches**, **tier placement**, and **author effort** (S ≤ ½ day,
M ≈ 1 day, L > 1 day of authoring).

| # | Idea | Source | What it teaches | Tier placement | Author effort |
|---|------|--------|-----------------|----------------|---------------|
| 1 | **Build the MCP server (not just wire it)** | [ATA §4.3] gap | Server side of MCP: FastMCP handlers, exposing a REST API as MCP, APIM "Expose as MCP" | Advanced — *stretch on Action Tools*, or standalone ⭐⭐⭐⭐ | **S** (extend existing backend) |
| 2 | **RAG / AI-Search deepening** | [FWH §5], [ATA] both lack real RAG | Hand-build a vector+hybrid index, tune `VECTOR_SEMANTIC_HYBRID`, chunking, rerank, citation quality — *below* the Foundry IQ abstraction | Foundations Step 4 **stretch**, or Advanced deepener ⭐⭐⭐⭐ | **M** |
| 3 | **UI / frontend dashboard** | [ATA §2 Ch4] Angular dashboard; [FWH §6] `frontend-design` skill | BFF pattern (no secrets in browser), streaming, citations panel, approval UI, CORS lockdown | **Already exists** as `extra-build-ui` → re-slot as **Capstone companion** (put a face on the multi-agent team) | **0** (built; just re-slot) |
| 4 | **Lab-generator Copilot meta-agent** | [FWH §4.9, §6] | Scaffold a whole new vertical (corpus + agents + eval set + facilitator guide) from a Copilot custom agent | **Cross-cutting "make it your own"** branch; powers scenario-swap at every tier | **M** (author the `.agent.md` + template) |
| 5 | **APIM-as-MCP variant** | [ATA §2 Ch2], [SKILLS §2a] | Expose a REST/OpenAPI API as an MCP server via **APIM "Expose as MCP" (preview)** with **zero code** — contrast with FastMCP | Advanced — *alternate path* for Action Tools | **S** (doc + APIM walkthrough) |
| 6 | **Hybrid rule + AI decisioning** | [ATA §3 Pattern 5] | Deterministic, auditable thresholds in code **+** AI for NL interpretation/narrative — "explainable AI for regulated domains" | Capstone **specialist variant** (a "policy" agent), or Advanced deepener ⭐⭐⭐⭐ | **M** |
| 7 | **Cleanup / cost-hygiene** | [FWH §4.10 `cleanup.sh`], [ATA] | `.env`-driven teardown, pause-capacity-after, cost-of-a-run awareness from traces | **Cross-cutting** wrap-up (every path ends here); ship `cleanup.sh` + a wrap-up page | **S** |
| 8 | **Connected Agents (declarative)** | [SKILLS §2a foundry-workflows] | The *declarative* multi-agent pattern (Connected Agents) as a **contrast** to MAF's code-first graph | Capstone **alternate orchestration** path | **M** |
| 9 | **Toolbox assembly** | [SKILLS §5.2 foundry-toolboxes] | Bundle AI Search + Web Search + Code Interpreter into one MCP-compatible **Toolbox**, consume from a hosted agent — "build once, consume everywhere" | Advanced deepener (feeds Capstone Action/Knowledge agents) ⭐⭐⭐⭐ | **M** |
| 10 | **Structured-output contracts lab** | [ATA §5 "brittle regex" critique] | Replace prose-parsing between agents with typed tool outputs / Pydantic — a focused 30-min drill | Folded into **Capstone** acceptance criteria (§3.7); optional standalone micro-lab | **S** |
| 11 | **Facilitator guides** | [FWH §5 "missing facilitator guides"] | Per-activity timing, reconvene points, common errors — the thing FWH *promises but never ships* | **Facilitator-track**, all tiers (our `solution.md` siblings already partly cover this) | **S–M** (formalize a template) |

**Backlog priorities (Danny's call):** ship **#3 re-slot** (free), **#4 lab-generator** and **#7
cleanup** next (cross-cutting, high leverage, low risk), then **#2 RAG-deepening** and **#9 toolbox**
as Advanced deepeners. **#5 APIM-as-MCP**, **#6 hybrid rules**, **#8 Connected Agents** are
preview-dependent — gate on facilitator availability and `foundry-mcp`/APIM-preview reachability (same
caveat PLAN-V2 §1 flagged).

---

## 5. Migration Notes

> **Scope discipline:** this is a PLAN. No activity content is edited in this batch. The notes below
> are the *implied* downstream changes for the team to execute next, owner-tagged.

### 5.1 README.md tier tables (owner: Danny + Linus)

- The root [README.md](README.md) currently says **"two tiers"** (lines ~107–109) and lists the
  Advanced table with the **old time labels** (Action Tools 1.25 hr). Update to:
  - **"three tiers"** framing + a one-line Capstone mention with a link to
    `activities/capstone-multi-agent/`.
  - Advanced table: **dual time columns** (guided / build-from-scratch) per §2.5, and **relabel Action
    Tools 1.25 hr → 45 min guided**.
  - Add a **Tier 3 — Capstone** row/section after the Advanced table.
  - Re-slot the **Extras** line: mark Magentic + Hosted Long-Running as **capstone-feeders**, Build a
    UI as **capstone companion**, Fabric/Voice/Copilot as **deepeners**.
- The "Total guided path" figure (currently **~7.75 hr**) becomes **~7.25 hr Foundations+Advanced
  guided** (Action Tools drop) **+ ~2.5 hr Capstone** = a clean **multi-day** story; keep the 1-day
  variant as Foundations + 2–3 Advanced.

### 5.2 docs/ navigation (owner: Linus)

- Add a **Tier 3 / Capstone** nav section mirroring `activities/capstone-multi-agent/` (+ a `-facilitator`
  sibling), following the existing 1:1 mirror rule and `nav_order` scheme (Capstone = a new band,
  e.g. `30`, facilitator = +100 + `nav_exclude`).
- Update `docs/activities/index.md` from **Two-Tier + Two-Paths** to **Three-Tier + Two-Paths**; reuse
  the §1 ASCII tree here.
- Re-slot the Extras pages under their tree roles (deepeners vs capstone-feeders) in the sidebar
  grouping; no page deletions required.
- Add the **cleanup / cost-hygiene** wrap-up page (backlog #7) to nav.

### 5.3 PLAN-V2 reconciliation (owner: Danny)

- Mark PLAN-V2 §1.1a ("two-tier model (LOCKED)") and §3 ("Curriculum Structure — Two Tiers") as
  **superseded by PLAN-V3 §1** (three-tier). Leave the Foundations spine, §1.5 two-paths, §1.6 STEP
  template, and §2 migration KEEP/CUT/REWRITE **intact** — V3 builds on them.
- Add a one-line pointer at the top of PLAN-V2 to PLAN-V3 (as PLAN-V2 already points back to PLAN.md).
- Log the supersession in `.squad/decisions.md` (see decision inbox entry written this batch).

### 5.4 Environment contract — DO NOT TOUCH (owner: everyone)

The authoritative `.env.sample` contract from Livingston's infra batch stays **byte-for-byte intact**.
The Capstone and all backlog items **reuse existing variables only**:

- `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `AZURE_FOUNDRY_AGENT_NAME`
- `AZURE_SEARCH_*`, `AZURE_SEARCH_INDEX_NAME=university-faq`
- `ACTION_API_URL=http://localhost:8080`, `ACTION_MCP_URL=http://localhost:8765/mcp`, `ACTION_API_KEY`
  *(empty)*; `server_label=northfield_actions`
- `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`,
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`

If the Capstone's hosted long-running variant needs anything new, it must be **added by Livingston via
Bicep outputs**, never hand-edited into `.env.sample` — same rule PLAN-V2 established.

### 5.5 New files implied (NOT created this batch)

| Path | Owner | Note |
|---|---|---|
| `activities/capstone-multi-agent/README.md` + `solution.md` | Danny + Rusty | Design-brief style (§3); light `validate.py` (Basher) for the structural acceptance criteria |
| `activities/capstone-multi-agent/validate.py` | Basher | Asserts ≥3 agents, fan-out edge present, typed contracts — headless-checkable subset of §3.7 |
| `.github/agents/lab-generator.agent.md` + a scenario template | Danny + Livingston | Backlog #4; port FWH's pattern **[FWH §6]** |
| `scripts/cleanup.sh` + a wrap-up page | Livingston + Linus | Backlog #7 cost-hygiene **[FWH §4.10]** |
| build-from-scratch variant notes per Advanced `solution.md` | Rusty + Basher | §2 dual-path; mostly additive "no-starter" sidebars |

---

## 6. One-Paragraph Bottom Line

V3 reshapes the curriculum from a two-tier list into a **3-tier tree**: a **guided Foundations trunk**,
a **modular Advanced fan** you pick in any order, and an **open-ended MAF Capstone summit** — with a
cross-cutting **"make it your own"** branch that reskins the whole thing to any domain. The Advanced
tier isn't *too long* — it's **over-guided**: Action Tools is honestly ~45 min not 1.25 hr, and the fix
across all four is **depth, not clock-padding** (remove the load-bearing PLACEHOLDERs, offer a
build-from-scratch path, add real stretch goals). The headline addition is **Tier 3**, where the single
Northfield IQ agent becomes a **team** — a triage/router that fans out to knowledge + action
specialists and converges on a synthesizer, built **visual-first in DevUI then traced**, taught as a
**design brief with acceptance criteria** rather than placeholders. This is the autonomy payoff —
**guided → modular → autonomous** — that neither FrontierWeekHack nor azure-trust-agents delivers.
