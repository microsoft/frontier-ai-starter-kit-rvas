---
title: Customer Build Track
nav_order: 2
has_children: true
description: Bring a customer outcome and build a grounded, evaluated Foundry agent prototype.
---

<div class="hero-panel track-hero track-hero--customer">
  <span class="hero-kicker">Track 1 • Customer Build</span>
  <h1>Turn a real outcome into a working agent prototype.</h1>
  <p class="hero-tagline">Use Northfield as the reference shape, but swap in your customer-safe corpus, persona, workflow, trust tests, and final demo story.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Define your outcome</a>
    <a class="btn btn-outline" href="{{ '/customer-build/foundations' | relative_url }}">Ground your app</a>
  </div>
</div>

{% include journey-status.html tone="customer" path="Customer Build Track" artifact="A customer-safe scenario pack plus one evolving Foundry agent prototype." next="Complete Define your outcome, then run Foundations with your own data and Northfield as the reference." %}

## The customer route

<ol class="journey-map">
  <li><span>0</span><strong>Define</strong><small>Outcome, users, corpus, action, safety</small></li>
  <li><span>1</span><strong>Ground</strong><small>Foundations with customer-safe data</small></li>
  <li><span>2</span><strong>Activate</strong><small>One approval-gated workflow</small></li>
  <li><span>3</span><strong>Trust</strong><small>Eval, red-team, tracing</small></li>
  <li><span>4</span><strong>Demo</strong><small>Hosted/UI artifact plus pilot backlog</small></li>
</ol>

## What to swap from Northfield

Northfield is the reference scenario — a student-services assistant for the fictional *Northfield
University*, grounded in a public university-FAQ corpus. Its [Foundations track]({{ '/activities/foundations' | relative_url }})
builds it step by step, so those steps are worked examples you copy commands from; you don't need
to build the Northfield version first. Customer Build keeps its mechanics and swaps in your content.

Use the [Scenario swap guide]({{ '/customer-outcome' | relative_url }}#scenario-swap-guide) as the canonical mapping. Do not maintain a second copy here; the canvas owns the customer-specific corpus, persona, workflow, safety boundaries, eval prompts, and demo story.

## The chapters

Each chapter adapts a Northfield reference module. It keeps the same objective and checkpoints,
but applies them to your app and asks whether the step is relevant. Make the decisions here; use
the linked reference for exact commands.

| Chapter | Reframes |
|---|---|
| [Define your outcome]({{ '/customer-outcome' | relative_url }}) | Scenario pack: user, corpus, action, safety, demo |
| [Ground your app]({{ '/customer-build/foundations' | relative_url }}) | Foundations |
| [Make it act]({{ '/customer-build/advanced-action-tools' | relative_url }}) | Action Tools |
| [Prove it's safe]({{ '/customer-build/advanced-evaluation-redteam' | relative_url }}) | Evaluation & Red Teaming |
| [See inside it]({{ '/customer-build/advanced-tracing-observability' | relative_url }}) | Tracing & Observability |
| [Ship it]({{ '/customer-build/advanced-deploy-hosted-agent' | relative_url }}) | Deploy as a Hosted Agent |
| [Grow it into a team]({{ '/customer-build/capstone-multi-agent' | relative_url }}) | Multi-Agent Capstone |

Optional deepeners (do only if your scenario needs them):
[Magentic Workflows]({{ '/customer-build/extra-magentic-workflows' | relative_url }}) ·
[Long-Running Agents]({{ '/customer-build/extra-hosted-longrunning' | relative_url }}) ·
[Build a UI]({{ '/customer-build/extra-build-ui' | relative_url }}) ·
[Fabric IQ]({{ '/customer-build/extra-fabric-iq' | relative_url }}) ·
[Give It a Voice]({{ '/customer-build/extra-voice-live' | relative_url }}) ·
[Copilot-Assisted Build]({{ '/customer-build/extra-copilot-assisted' | relative_url }})

## Build order for a one-day event

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Must do</span>
    <h3>Define your outcome + Foundations</h3>
    <p>Leave with a grounded assistant that answers customer-relevant questions with citations from trusted data.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">High value</span>
    <h3>Action + Evaluation</h3>
    <p>Add one governed workflow and a scorecard that shows accuracy, safety, and abstention behavior.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Demo polish</span>
    <h3>Deploy or UI</h3>
    <p>Give stakeholders a real endpoint, web face, citations panel, or approval card they can understand quickly.</p>
  </div>
</div>

## Your first move

Complete [Define your outcome]({{ '/customer-outcome' | relative_url }}) before starting Foundations. If you do not have an app idea yet, go through [Idea Forge]({{ '/idea-forge' | relative_url }}) first; it feeds directly into Define your outcome.

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Complete Define your outcome</a>
</div>
