---
title: Home
nav_order: 1
description: Kick off the What The Hack experience and navigate the two-tier Microsoft Foundry challenge set.
---

<div class="hero-panel">
  <span class="hero-kicker">What The Hack • Microsoft Foundry</span>
  <h1>Build Intelligent Apps with Microsoft Foundry</h1>
  <p class="hero-tagline">From prompt to production: a guided Foundations challenge plus a modular Advanced tier covering grounding, action tools, evaluation, tracing, and deployment.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ '/setup' | relative_url }}">Get Started</a>
    <a class="btn btn-outline" href="{{ '/coach-hub' | relative_url }}">Coaches: Start here</a>
  </div>
</div>

## What is this?

What The Hack (WTH) is Microsoft’s hands-on, challenge-first format for learning by building. Instead of sitting through a lecture, teams move through a sequence of guided tasks, validate their work as they go, and lean on coaches for hints when they hit real friction.

This edition focuses on Microsoft Foundry. It runs in **two tiers**. **Foundations** is one guided, linear challenge — four ordered steps that take every team to a deployed, grounded Northfield University IQ Assistant that answers from a real FAQ corpus with citations. **Advanced** is a set of modular challenges you attempt in any order: action tools, evaluation & red teaming, tracing & observability, and deploying as a hosted agent — plus optional Extras.

<div class="quick-grid">
  <div class="quick-card">
    <h3>Two tiers, two paths</h3>
    <p>Start with the guided Foundations challenge, then branch into modular Advanced challenges in any order — or bootstrap straight to the Advanced tier.</p>
  </div>
  <div class="quick-card">
    <h3>Built for event day</h3>
    <p>Time-boxed modules, mobile-friendly docs, and strong navigation for students and coaches moving fast.</p>
  </div>
  <div class="quick-card">
    <h3>Coach-guided discovery</h3>
    <p>Coaches help unblock, question, and steer without taking the keyboard away from participants.</p>
  </div>
</div>

## Two tiers

<div class="challenge-card" markdown="1">

**Tier 1 · [Foundations](challenges/foundations)** — one guided, linear challenge (four ordered steps):

| Step | Focus | Outcome |
|------|-------|---------|
| 1 — Setup & Provisioning | `azd up`, keyless auth | Infrastructure live |
| 2 — Model & Playground | Deploy + compare models | Generic answers from your model |
| 3 — Your First Agent | Persona + guardrails | An agent that refuses out-of-scope asks |
| 4 — Knowledge Base (IQ) | Index the FAQ + Foundry IQ | **Grounded answers with citations — END-STATE** |

**Tier 2 · Advanced (any order)** — each assumes the Foundations end-state:

| Advanced | Extras |
|----------|--------|
| [Action Tools](challenges/advanced-action-tools) | [Fabric IQ](challenges/extra-fabric-iq) · [Give It a Voice](challenges/extra-voice-live) |
| [Evaluation & Red Teaming](challenges/advanced-evaluation-redteam) | [Magentic Workflows](challenges/extra-magentic-workflows) · [Hosted Long-Running](challenges/extra-hosted-longrunning) |
| [Tracing & Observability](challenges/advanced-tracing-observability) | [Build a UI](challenges/extra-build-ui) · [Copilot-Assisted Build](challenges/extra-copilot-assisted) |
| [Deploy as a Hosted Agent](challenges/advanced-deploy-hosted-agent) | |

See the [Challenges overview](challenges/) for the full Two-Paths run guide (Beginner vs. Advanced-skip bootstrap).

</div>

## Who is this for?

### Students

You are in the right place if you know basic Python, want hands-on experience with modern AI tooling, and prefer learning by shipping instead of watching demos. No prior Microsoft Foundry experience is required.

### Coaches

This site is built to help you pace teams, spot common blockers early, and keep the day moving. Use the Coach Hub for timing, facilitation prompts, and escalation guidance while keeping solution walkthroughs inside the repo.

## Start with the right path

<a class="btn btn-primary btn-lg" href="{{ '/setup' | relative_url }}">Get Started</a>
<a class="btn btn-outline btn-lg" href="{{ '/coach-hub' | relative_url }}">Coaches: Start here</a>
