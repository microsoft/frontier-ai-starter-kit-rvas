---
title: Home
nav_order: 1
description: Kick off the What The Hack experience and navigate the three-tier Microsoft Foundry challenge set.
---

<div class="hero-panel">
  <span class="hero-kicker">What The Hack • Microsoft Foundry</span>
  <h1>Build Intelligent Apps with Microsoft Foundry</h1>
  <p class="hero-tagline">Bring your outcome and build a real application — a grounded, evaluated, demo-ready agent prototype your customer or team can use. New to Foundry? The Northfield University reference scenario gives you a guided path to the same end-state.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Bring your outcome</a>
    <a class="btn btn-outline" href="{{ '/setup' | relative_url }}">Get Started</a>
    <a class="btn btn-outline" href="{{ '/coach-hub' | relative_url }}">Coaches: Start here</a>
  </div>

</div>

## What is this?

What The Hack (WTH) is Microsoft’s hands-on, challenge-first format for learning by building. Instead of sitting through a lecture, teams move through a sequence of guided tasks, validate their work as they go, and lean on coaches for hints when they hit real friction.

This edition focuses on Microsoft Foundry. The **primary motion is Customer Build Mode**: bring a real customer scenario and leave with a grounded, evaluated prototype. If your team is new to Foundry and needs a guided learning path, **Upskill Mode** uses the Northfield University reference scenario as a safe fallback. Both motions use the same three-tier path. **Tier 1 · Foundations** is one guided, linear challenge — four ordered steps that take every team to a deployed, grounded assistant with citations. **Tier 2 · Advanced** is a set of modular challenges you attempt in any order: action tools, evaluation & red teaming, tracing & observability, and deploying as a hosted agent — plus optional Extras. **Tier 3 · Capstone** is an open-ended design brief that composes everything into a multi-agent system built with the Microsoft Agent Framework (MAF).

> **No idea yet?** Use the [**Customer Challenge-Forge**](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md) skill: give it a customer name and industry and it researches public documentation to generate ~10 right-sized, buildable Microsoft Foundry AI application ideas — your ready-made on-ramp to Customer Build Mode.

<div class="quick-grid">
  <div class="quick-card">
    <h3>Build something real</h3>
    <p>Start from your own customer or business outcome. Complete the Customer Outcome Canvas and map the same challenges to your domain — data, actions, evals, and a 2-minute demo story.</p>
  </div>

  <div class="quick-card">
    <h3>Outcome checkpoints</h3>
    <p>Each tier produces customer-facing evidence: cited answers, governed actions, eval scorecards, traces, deployment, and demo story.</p>
  </div>

  <div class="quick-card">
    <h3>Coach-guided discovery</h3>
    <p>Coaches help teams translate a scenario into data, tools, evals, risks, and a stakeholder-ready demo. No idea yet? Coaches can run Customer Challenge-Forge with you.</p>
  </div>

</div>

## Which path is right for you?

| Mode | Use when | Default artifact |
|------|----------|-----------------|
| **Customer Build Mode** *(primary)* | You have a customer, account, or business scenario to build against | Your own grounded, evaluated, demo-ready agent prototype |
| **Upskill Mode** *(fallback)* | Your team is learning Foundry for the first time or has no customer scenario | The Northfield University IQ Assistant (guided reference corpus) |

Start with the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}) to lock in your user, data source, workflow, safety boundary, and demo story before the first line of code. If you don't have a customer or idea yet, the [**Customer Challenge-Forge**](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md) skill generates ~10 tailored ideas from a customer name and industry — pick one and fill in the canvas.

## Three tiers

Both modes use the same three-tier path. The canvas sets the outcome; the tiers deliver it.

<div class="challenge-card" markdown="1">

**Tier 1 · [Foundations](challenges/foundations)** — one guided, linear challenge (four ordered steps):

| Step | Focus | Outcome |
|------|-------|---------|
| [1 — Setup & Provisioning](challenges/foundations#step-1--setup--provisioning-foundry--ai-search) | `azd up`, keyless auth | Infrastructure live |
| [2 — Model & Playground](challenges/foundations#step-2--model-selection--the-playground) | Deploy + compare models | Generic answers from your model |
| [3 — Your First Agent](challenges/foundations#step-3--your-first-agent) | Persona + guardrails | An agent that refuses out-of-scope asks |
| [4 — Knowledge Base (IQ)](challenges/foundations#step-4--knowledge-base-index--foundry-iq---foundations-end-state) | Index the FAQ + Foundry IQ | **Grounded answers with citations — END-STATE** |

**Tier 2 · Advanced (any order)** — each assumes the Foundations end-state:

| Advanced | Extras |
|----------|--------|
| [Action Tools](challenges/advanced-action-tools) | [Fabric IQ](challenges/extra-fabric-iq) · [Give It a Voice](challenges/extra-voice-live) |
| [Evaluation & Red Teaming](challenges/advanced-evaluation-redteam) | [Magentic Workflows](challenges/extra-magentic-workflows) · [Hosted Long-Running](challenges/extra-hosted-longrunning) |
| [Tracing & Observability](challenges/advanced-tracing-observability) | [Build a UI](challenges/extra-build-ui) · [Copilot-Assisted Build](challenges/extra-copilot-assisted) |
| [Deploy as a Hosted Agent](challenges/advanced-deploy-hosted-agent) | |

**Tier 3 · [Capstone](challenges/capstone-multi-agent)** — the open-ended summit: break the single Northfield IQ Assistant into a **multi-agent team** — a triage/router that fans out to specialist agents (knowledge, actions) and converges — orchestrated with the **Microsoft Agent Framework (MAF)**. It's a design brief, not a placeholder-fill: you decide the org-chart and wire the graph.

| Capstone | Time | Prereqs |
|----------|------|---------|
| [Northfield IQ, the Team — Multi-Agent Orchestration](challenges/capstone-multi-agent) | 2–2.5 hr core (+1 hr Magentic stretch, +1.5 hr hosted variant) | Foundations end-state **+** Action Tools |

<a class="btn btn-primary" href="challenges/capstone-multi-agent">Start the Capstone →</a>

See the [Challenges overview](challenges/) for the full run options (Guided path vs. Advanced-skip bootstrap).

</div>

## Who is this for?

### Students

You are in the right place if you know basic Python, want hands-on experience with modern AI tooling, and prefer learning by shipping instead of watching demos. No prior Microsoft Foundry experience is required.

### Coaches

This site is built to help you pace teams, spot common blockers early, and keep the day moving. Use the Coach Hub for timing, facilitation prompts, and escalation guidance while keeping solution walkthroughs inside the repo.

## Start here

<a class="btn btn-primary btn-lg" href="{{ '/customer-outcome' | relative_url }}">Bring your outcome</a>
<a class="btn btn-outline btn-lg" href="{{ '/setup' | relative_url }}">Get Started (setup)</a>
<a class="btn btn-outline btn-lg" href="{{ '/coach-hub' | relative_url }}">Coaches: Start here</a>
