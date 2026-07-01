---
title: Upskill Track
nav_order: 4
description: Learn Microsoft Foundry with the guided Northfield University reference scenario.
---

<div class="hero-panel track-hero track-hero--upskill">
  <span class="hero-kicker">Track 2 • Upskill</span>
  <h1>Learn the full Foundry path with Northfield.</h1>
  <p class="hero-tagline">Use the fictional Northfield University IQ Assistant as a safe, known-good scenario. You build the same architecture customer teams use, without needing real customer data.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ '/setup' | relative_url }}">Start setup</a>
    <a class="btn btn-outline" href="{{ '/challenges/foundations' | relative_url }}">Open Foundations</a>
  </div>
</div>

{% include journey-status.html tone="upskill" path="Upskill Track &rarr; Northfield reference scenario" artifact="A grounded Northfield University IQ Assistant that grows across Foundations, Advanced modules, and Capstone." next="Set up your environment, then complete Foundations Steps 1-4 in order." %}

## The upskill route

<ol class="journey-map">
  <li><span>0</span><strong>Setup</strong><small>Codespaces, Azure auth, toolchain</small></li>
  <li><span>1</span><strong>Foundations</strong><small>Provision, model, agent, IQ knowledge</small></li>
  <li><span>2</span><strong>Advanced</strong><small>Action, eval, tracing, deploy</small></li>
  <li><span>3</span><strong>Extras</strong><small>UI, voice, Fabric IQ, Copilot-assisted</small></li>
  <li><span>4</span><strong>Capstone</strong><small>Router plus specialist agents</small></li>
</ol>

## Why Northfield is the right fallback

<div class="quick-grid">
  <div class="quick-card">
    <h3>Known-good data</h3>
    <p>The corpus, prompts, tools, and evals are already shaped for the challenge validators.</p>
  </div>

  <div class="quick-card">
    <h3>Same architecture</h3>
    <p>You still learn provisioning, model choice, agents, Foundry IQ, actions, evals, tracing, deploy, and orchestration.</p>
  </div>

  <div class="quick-card">
    <h3>Reusable later</h3>
    <p>After the event, swap Northfield artifacts for a customer corpus, domain persona, workflow, and scorecard.</p>
  </div>
</div>

## Convert later to Customer Build

<div class="challenge-card" markdown="1">

| Northfield artifact | Future customer replacement |
|---|---|
| University FAQ corpus | Customer-safe documents, SOPs, manuals, FAQs, or product content |
| Student-services persona | Target-user assistant persona |
| Student workflow tools | One approval-gated customer workflow |
| Northfield eval prompts | Customer scenario eval and red-team prompts |
| Student demo story | Stakeholder outcome demo |

</div>

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/setup' | relative_url }}">Set up your environment</a>
</div>
