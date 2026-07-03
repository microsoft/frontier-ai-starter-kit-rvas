
# Customer Build · Chapter 6 — Grow it into a team



This chapter is **mutuated from [Capstone · Multi-Agent](challenge.html?id=capstone-multi-agent)** — same MAF design brief, same structural validator — but the org chart, specialists, contracts, and demo journey come from *your* scenario in [Chapter 0: Define your outcome](challenge.html?id=customer-outcome).

> **Before you start this chapter:** finish [Chapter 1](challenge.html?id=customer-foundations) and [Chapter 2](challenge.html?id=customer-action-tools) if your team will include an action specialist. [Chapter 4](challenge.html?id=customer-tracing-observability) makes the final demo much stronger.

---

## Section 1 — Decide whether one agent is enough

**Why it matters for your app:** multi-agent design adds power and complexity. Use it only when separate roles make the outcome clearer, safer, or easier to govern.

**Does this apply to you?**
- **Build it** if your demo journey naturally crosses multiple roles, tools, risk levels, or knowledge domains.
- **Adapt it** if you only need a router plus one specialist; keep the graph small and explain the future branches.
- **Skip it** if one grounded agent with one action already tells the best story.

**Decisions to make:**
- Which Chapter 0 user journey has real handoffs?
- What work should be routed, retrieved, acted on, escalated, and synthesized?
- Which responsibilities must not overlap?
- What will the audience learn from seeing a team instead of one agent?

**Apply it to your app:** use the capstone objectives to decide whether multi-agent is justified before writing code. → [Capstone — Learning objectives](challenge.html?id=capstone-multi-agent#learning-objectives)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --list`
- Checklist: ☐ team design is justified ☐ one-agent alternative considered ☐ final demo journey needs at least two specialist viewpoints.

**Stuck?** [Northfield learning objectives](challenge.html?id=capstone-multi-agent#learning-objectives).

---

## Section 2 — Draw your agent org chart

**Why it matters for your app:** roles are the architecture. If the org chart is fuzzy, the graph will be fuzzy.

**Does this apply to you?**
- **Build it** if Chapter 6 is in scope.
- **Adapt it** if your domain needs different specialists than knowledge/action/escalation.
- **Skip it** if you decided the monolith is the right demo artifact.

**Decisions to make:**
- What does the router classify?
- Which specialists map to real business functions or systems?
- Which specialist reuses your Chapter 1 grounded agent?
- Which specialist reuses your Chapter 2 approval loop?
- What does the synthesizer merge, cite, and refuse?

**Apply it to your app:** replace the Northfield help-desk roles with your own process roles. → [Capstone — Agent org-chart](challenge.html?id=capstone-multi-agent#the-agent-org-chart-role-as-agent)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --step 1 --path <your-capstone-dir>`
- Checklist: ☐ ≥3 roles named ☐ one router/triage role ☐ ≥2 specialists ☐ roles are non-overlapping ☐ at least one role reuses prior chapter work.

**Stuck?** [Northfield org chart](challenge.html?id=capstone-multi-agent#the-agent-org-chart-role-as-agent).

---

## Section 3 — Build sequential first

**Why it matters for your app:** sequential flow proves contracts and role boundaries before concurrency hides bugs.

**Does this apply to you?**
- **Build it** if you are implementing the graph.
- **Adapt it** if your final path is parallel — still run one sequential warm-up path first.
- **Skip it** only if Chapter 6 is a design-only sketch.

**Decisions to make:**
- What is the smallest route through router → one specialist → synthesizer?
- What typed message does each hop receive and emit?
- What single question proves the contract works?
- What failure should route to escalation instead?

**Apply it to your app:** create the warm-up graph using current MAF signatures from docs and the workflow skill. → [Capstone — Pass 1](challenge.html?id=capstone-multi-agent#pass-1--sequential-warm-up)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --step 3 --path <your-capstone-dir>`
- Checklist: ☐ typed Pydantic contracts exist ☐ agents pass typed objects, not regex-parsed prose ☐ one sequential run completes ☐ final answer cites or explains limits.

**Stuck?** [Northfield Pass 1](challenge.html?id=capstone-multi-agent#pass-1--sequential-warm-up).

---

## Section 4 — Add fan-out and fan-in

**Why it matters for your app:** fan-out lets specialists work in parallel; fan-in forces the final answer to wait for all relevant evidence and decisions.

**Does this apply to you?**
- **Build it** if one user request needs multiple specialists at once.
- **Adapt it** if only some requests fan out — route dynamically and keep simple requests single-path.
- **Skip it** if parallelism does not improve the demo.

**Decisions to make:**
- Which router decision sends work to multiple specialists?
- Which branches can safely run in parallel?
- What must the synthesizer wait for?
- How are conflicting specialist outputs resolved?

**Apply it to your app:** evolve the warm-up graph into fan-out/fan-in. Verify current MAF builder APIs before coding. → [Capstone — Pass 2](challenge.html?id=capstone-multi-agent#pass-2--parallel-fan-out--fan-in)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --step 2 --path <your-capstone-dir>`
- Checklist: ☐ router fans out to ≥2 branches ☐ synthesizer waits for relevant branches ☐ action branch still honors approval ☐ knowledge branch still cites sources.

**Stuck?** [Northfield Pass 2](challenge.html?id=capstone-multi-agent#pass-2--parallel-fan-out--fan-in).

---

## Section 5 — Visualize and trace the team

**Why it matters for your app:** multi-agent demos are hard to trust unless the audience can see the handoffs and you can trace the run after the fact.

**Does this apply to you?**
- **Build it** if Chapter 6 is part of the final demo.
- **Adapt it** if DevUI is unavailable — capture logs plus an operation-id trace.
- **Skip it** only for a paper design; mark it coach-judged/manual.

**Decisions to make:**
- Which run will you show in DevUI?
- What trace proves router, specialists, and synthesizer all participated?
- What token/latency signal is most important for this team design?
- How will you explain a branch that did not run?

**Apply it to your app:** visualize first, then reuse Chapter 4 tracing to capture the multi-agent span tree. → [Capstone — Visual-first, then traced](challenge.html?id=capstone-multi-agent#visual-first-then-traced)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --all --path <your-capstone-dir>`
- Checklist: ☐ DevUI or equivalent shows the graph ☐ trace shows multi-agent handoffs ☐ operation id is captured ☐ 2-minute demo narrates the journey.

**Stuck?** [Northfield visual/tracing guidance](challenge.html?id=capstone-multi-agent#visual-first-then-traced).

---

## Section 6 — Swap in your scenario and acceptance criteria (chapter end-state)

**Why it matters for your app:** the capstone is only valuable if the team handles your corpus, tools, risks, and success measures — not Northfield's.

**Does this apply to you?**
- **Build it** if you want a stakeholder-ready final story.
- **Adapt it** if some artifacts are still Northfield-shaped — clearly label what is real vs. placeholder.
- **Skip it** only if you are doing the upskill path, not Customer Build.

**Decisions to make:**
- Which domain examples replace Northfield in prompts, tools, data, and evals?
- Which `.env.sample` variables are reused unchanged?
- What acceptance criteria are auto-validated vs. coach/stakeholder-judged?
- What pilot backlog remains after the hackathon?

**Apply it to your app:** use the scenario-swap and acceptance-criteria sections as your final checklist. → [Capstone — Make it your own](challenge.html?id=capstone-multi-agent#make-it-your-own-scenario-swap) and [Capstone — Acceptance criteria](challenge.html?id=capstone-multi-agent#acceptance-criteria-graded--no-step-by-step)

**Prove you applied it:**
- `python challenges/capstone-multi-agent/validate.py --track customer --all --path <your-capstone-dir>`
- Checklist: ☐ Northfield defaults removed or clearly marked as placeholders ☐ existing `.env` contract reused ☐ acceptance criteria mapped to your demo ☐ risks and next-step backlog are ready.

**Stuck?** [Northfield scenario-swap](challenge.html?id=capstone-multi-agent#make-it-your-own-scenario-swap) and [acceptance criteria](challenge.html?id=capstone-multi-agent#acceptance-criteria-graded--no-step-by-step).

---

## Chapter 6 end-state

You have a **customer-specific agent team**: router, specialists, typed contracts, fan-out/fan-in, and a traceable 2-minute journey.

```bash
python challenges/capstone-multi-agent/validate.py --track customer --all --path <your-capstone-dir>
```

Finish with your **2-minute stakeholder demo**, scorecard, known risks, and pilot backlog.
