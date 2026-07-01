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
    <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Start Step 0</a>
    <a class="btn btn-outline" href="{{ '/challenges/foundations' | relative_url }}">Start Foundations</a>
  </div>
</div>

{% include journey-status.html tone="customer" path="Customer Build Track" artifact="A customer-safe scenario pack plus one evolving Foundry agent prototype." next="Complete Step 0, then run Foundations with your own data and Northfield as the reference." %}

## The customer route

<ol class="journey-map">
  <li><span>0</span><strong>Define</strong><small>Outcome, users, corpus, action, safety</small></li>
  <li><span>1</span><strong>Ground</strong><small>Foundations with customer-safe data</small></li>
  <li><span>2</span><strong>Activate</strong><small>One approval-gated workflow</small></li>
  <li><span>3</span><strong>Trust</strong><small>Eval, red-team, tracing</small></li>
  <li><span>4</span><strong>Demo</strong><small>Hosted/UI artifact plus pilot backlog</small></li>
</ol>

## What to swap from Northfield

Use the [Scenario swap guide]({{ '/customer-outcome' | relative_url }}#scenario-swap-guide) as the canonical mapping. Do not maintain a second copy here; the canvas owns the customer-specific corpus, persona, workflow, safety boundaries, eval prompts, and demo story.

## Build order for a one-day event

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Must do</span>
    <h3>Step 0 + Foundations</h3>
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

Complete [Step 0: Define your outcome]({{ '/customer-outcome' | relative_url }}) before starting Foundations. If you do not have an app idea yet, go through [Idea Forge]({{ '/idea-forge' | relative_url }}) first; it feeds directly into Step 0.

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Complete Step 0</a>
</div>
