---
name: customer-challenge-forge
description: "Given a customer name and industry, research public sources and generate ~10 ranked AI-application ideas grounded in that company's real challenges — each mapped to hackathon tiers, tagged for effort, and wired to the Customer Outcome Canvas Pre-work fields so a participant can pick an idea and build immediately."
argument-hint: "Company name and industry are required. Optional: region/segment and known pain points."
---

## Context

Use this skill when a hackathon participant has been asked to build with a customer scenario but
**has no idea where to start**. They know the customer name and the industry; they do not yet know
which AI problem is worth solving or how to scope it to a one-day build.

This skill bridges the gap between "I have a customer" and "I know what to build." It researches
the company and its industry from public sources only, synthesises ~10 AI-application ideas
calibrated to the event window, maps each idea to the hackathon's technology tiers, and then
pre-fills the Customer Outcome Canvas Pre-work fields for the top pick.

Use it **before** the hackathon starts, ideally during the pre-work session or the first
30 minutes of day one. Once the team has chosen an idea, they carry the Canvas straight into
the Foundations challenge.

---

## Input

**Required**
- `customer_name` — the company or business unit the team is working with.
- `industry` — the sector (e.g. retail, healthcare, financial services, manufacturing).

**Optional**
- `region_or_segment` — geography or sub-segment that narrows the context (e.g. "UK mid-market retail", "US federal healthcare").
- `known_pain_points` — any pain points the team already heard from the customer (freeform text). These become confirmatory signals during research, not replacements for it.

---

## Process

### Step 1 — Gather inputs

Confirm `customer_name` and `industry` are provided. If either is missing, ask before proceeding.
If `region_or_segment` or `known_pain_points` are not provided, note their absence and proceed
with what is available.

---

### Step 2 — Research phase (public sources only)

Run a structured research sweep using `web_search` and `web_fetch`. Collect findings under four
headings. Cite every source (URL + date retrieved). Flag anything you cannot verify publicly with
a ⚠️ marker rather than filling the gap with an assumption.

**2a. Company profile**
- Official website: products, services, stated mission, customer segments.
- Recent press releases or news: acquisitions, partnerships, product launches (last 18 months).
- Leadership blog posts or interviews that name operational priorities.

**2b. Public statements of business challenges**
- Investor relations page, annual report, quarterly earnings transcripts, or 10-K/10-Q equivalents.
- Themes from the most recent earnings call: cost pressure, growth bets, competitive threats.
- Sustainability, compliance, or transformation programs the company has publicly named.

**2c. Industry landscape**
- Top 5 challenges the sector faces right now (regulatory shifts, margin pressure, talent gaps,
  supply-chain fragility, customer-experience gaps, etc.).
- Analyst commentary or industry-body reports that are freely available (Gartner summary articles,
  McKinsey public briefs, IDC press releases, government statistics).
- Active AI/automation trends for this sector.

**2d. Research summary**
Write a 3–5 sentence plain-English paragraph summarising what you found. Call out the 2–3 themes
most likely to drive AI application value. Note any coverage gaps (e.g. "No public earnings
transcripts found for this company; industry benchmarks used as proxy").

---

### Step 3 — Generate ~10 AI application ideas

Each idea must be grounded in the research, buildable with Microsoft Foundry, and calibrated to
the hackathon's event window (see Difficulty Calibration below).

**Idea structure — include ALL of these fields for every idea:**

| Field | Guidance |
|---|---|
| **Title** | 4–8 words, outcome-first (e.g. "Field-Tech Knowledge Assistant with Approval Gate") |
| **Description** | 2–3 sentences: what the agent does, how it works, what it produces |
| **Target user** | The human who benefits most (e.g. "field engineer", "store manager", "compliance analyst") |
| **Business outcome** | One sentence: what is faster, safer, cheaper, or more reliable |
| **Tier / tech mapping** | Which hackathon tiers and challenges this idea exercises (use exact names below) |
| **Effort tag** | `Starter`, `Core`, or `Stretch` (see definitions below) |
| **Industry/company fit** | 1–2 sentences explaining why this idea is grounded in the research, with a citation |
| **Required knowledge sources** | What safe, realistic data would ground the agent (documents, FAQs, policies, manuals, APIs) |

**Tier and challenge names to use (use these exact labels):**

| Label | What it covers |
|---|---|
| Foundations | Provision Foundry, deploy a model, create an agent, attach a Foundry IQ knowledge base |
| Action Tools | Attach an MCP tool, implement an approval gate |
| Evaluation & Red Teaming | Eval dataset, adversarial prompts, groundedness and safety scoring |
| Tracing & Observability | OpenTelemetry spans, App Insights, latency and retrieval analysis |
| Deploy as Hosted Agent | `azd ai agent deploy`, containerised `responses`-protocol endpoint |
| Capstone | MAF multi-agent orchestration: router + specialist agents + fan-out graph |
| Extra — Fabric IQ | Grounding against Microsoft Fabric lakehouses |
| Extra — Voice Live | Real-time speech interface |
| Extra — Magentic Workflows | Magentic-style planner/manager pattern within MAF |
| Extra — Build a UI | React/HTML front-end over the agent endpoint |

**Effort tag definitions:**

| Tag | What it means |
|---|---|
| `Starter` | Single-tier build (Foundations only). Grounded FAQ assistant, no actions. Completable in ~2 hours by a first-timer. Good first challenge for a new team. |
| `Core` | Two-tier build: Foundations + one Advanced challenge (typically Action Tools or Evaluation & Red Teaming). The sweet spot for most hackathon teams. Grounded agent + one governed action or a scored eval suite. Completable in a full event day. |
| `Stretch` | Three or more tiers, or Capstone MAF orchestration. Needs strong Foundations before attempting. Best for an advanced team or a second event day. |

---

### Step 4 — Difficulty calibration and sweet-spot guardrails

Before finalising the list, apply these guardrails. State them explicitly in your output so the
participant understands the calibration:

**The sweet spot is: grounded agent + one governed action.**

| Guardrail | Description |
|---|---|
| Not too trivial | A generic FAQ bot with no domain grounding is not a hackathon deliverable. Every idea must use a real knowledge source specific to the customer's domain. |
| Not over-common | "Customer service chatbot" with no differentiation, or a basic QnA assistant that any template produces in 10 minutes, is not sufficient. Ideas should exercise at least one Foundry capability beyond a plain agent. |
| Not over-complex | A multi-source, real-time integration across five enterprise systems that requires data-engineering pre-work is out of scope for one day. Cap complexity at "one action + one knowledge source" for Core ideas. |
| Event-window fit | A Core idea should be demonstrable within a 6–8 hour event day. A Starter idea should reach a working demo in 2 hours. A Stretch idea should reach a meaningful partial demo. |
| Data-ready check | Every idea must name a realistic knowledge source the team could plausibly prepare or use from the Northfield placeholder corpus. If real customer data is not available on event day, the Northfield corpus plus a domain-specific overlay is an acceptable fallback. |

---

### Step 5 — Output format

Produce output in this exact order:

#### Part A — Research summary
One paragraph, 3–5 sentences. Cite sources inline. Flag gaps with ⚠️.

#### Part B — Ranked summary table

| # | Title | Effort | Tiers | Why it fits |
|---|---|---|---|---|
| 1 | … | Core | Foundations, Action Tools | … |
| … | | | | |

Rank by: best fit for the company's stated challenges, achievability in one event day, and
differentiation (avoids generic demos).

#### Part C — Per-idea detail blocks

For each of the ~10 ideas, output a full detail block with all eight fields from Step 3.

#### Part D — Recommended top 3

Name the top 3 ideas and give a one-sentence rationale for each. This is the section the team
takes into their coach conversation.

#### Part E — Customer Outcome Canvas pre-fill

For **Idea #1 (the top recommendation)**, pre-fill the Canvas Pre-work table from
`docs/customer-outcome.md`. Map each canvas field to the idea's specifics so the participant can
carry it straight into the Foundations challenge. Include placeholder text where the team must
supply information (e.g. actual document names, specific action API).

| Canvas field | Pre-filled value |
|---|---|
| Customer / business area | … |
| Target users | … |
| Business outcome | … |
| Top user tasks | … |
| Knowledge sources | … |
| Action candidates | … |
| Safety boundaries | … |
| Success measures | … |
| Final demo story | … |

---

## Anti-Patterns

Do not do any of the following. If you find yourself about to do one, stop and correct.

| Anti-pattern | Why it matters |
|---|---|
| **Fabricating company facts** | Every factual claim about the company must be citable to a public source. If you cannot find it, say so with ⚠️. Do not invent product lines, financial figures, or executive priorities. |
| **Using non-public or confidential data** | Do not reference internal Microsoft account data, confidential customer presentations, or any information not freely accessible on the public web. |
| **Skipping citations** | Every research claim in Parts A–C must include a URL or source reference. Uncited claims are treated as fabricated. |
| **Generic industry-blind ideas** | An idea that could apply to any company in any sector (e.g. "build a chatbot for employees") is not grounded. Every idea must reference a specific challenge or opportunity from the research. |
| **Over-complex builds** | Do not propose ideas that require real-time system integrations, production data pipelines, or custom ML models. Cap scope at "Foundry agent + knowledge base + one MCP action." |
| **Trivial demos** | A plain FAQ bot with no domain knowledge, no actions, and no evaluation is a tutorial output, not a hackathon deliverable. Minimum bar: Foundations end-state (grounded answers with citations). |
| **Ignoring the Canvas** | Part E must be filled. The skill is not complete until the top idea maps onto every Pre-work field, even if some fields carry placeholder text. |
| **Mislabelling effort** | Do not tag a multi-tier Capstone build as Starter, or a simple grounded agent as Stretch. Match the tag definitions in Step 3 exactly. |

---

## Examples

**Good title:** "Warranty Claims Triage Assistant with Escalation Approval Gate" — specific domain,
named action, named user workflow.

**Bad title:** "AI Chatbot for Customer Service" — no domain, no action, generic.

**Good industry/company fit rationale:** "In its FY25 earnings call (Q4 2025), [Company] cited
warranty-cost reduction as a top operational priority, with $120M annual spend on manual triage.
This idea addresses that gap directly. [source: investor-relations page, date]"

**Bad industry/company fit rationale:** "Retail companies often have customer service challenges."
— generic, no citation, no company-specific grounding.

---

## Notes

- This skill uses **public sources only**. It does not access internal Microsoft systems, CRM data,
  account plans, or confidential presentations.
- The Northfield University corpus (the hackathon's default scenario) remains the safe fallback if
  real customer data is not available on event day. The Canvas pre-fill in Part E should explicitly
  note this option under "Knowledge sources."
- After the team picks an idea, the next step is the [Customer Outcome Canvas](docs/customer-outcome.md)
  full discussion with their coach, then straight into the Foundations challenge.
