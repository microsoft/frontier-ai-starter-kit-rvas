---
title: Idea Forge
nav_order: 3
description: Generate a buildable customer AI application idea, then continue into Customer Build.
---

<div class="hero-panel track-hero track-hero--idea">
  <span class="hero-kicker">Intake • Need an idea</span>
  <h1>No app idea yet? Forge one, then build it.</h1>
  <p class="hero-tagline">This is not a separate track. It is a fast intake step that turns a customer name or industry into a ranked set of Foundry application ideas.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md">Open Challenge-Forge</a>
    <a class="btn btn-outline" href="{{ '/customer-build' | relative_url }}">See Customer Build</a>
  </div>
</div>

{% include journey-status.html tone="idea" path="Idea Forge &rarr; Customer Build Track" artifact="One selected AI application idea with outcome, users, data sources, and tier guidance." next="Paste the chosen idea into Customer Build Step 0, then continue the track." %}

## Five-minute idea funnel

<ol class="route-list">
  <li><strong>Name the context.</strong> Provide a customer name, business area, or target industry.</li>
  <li><strong>Run Customer Challenge-Forge.</strong> Generate roughly 10 ranked, right-sized ideas grounded in public context.</li>
  <li><strong>Pick one idea.</strong> Prefer the idea with clear users, safe data, one useful action, and a believable demo.</li>
  <li><strong>Complete Customer Build Step 0.</strong> Transfer the idea's outcome, users, sources, action candidates, and risk notes.</li>
  <li><strong>Continue as Customer Build.</strong> From this point on, you are no longer in an idea flow; you are building the prototype.</li>
</ol>

## Pick the idea that can actually ship today

<div class="quick-grid">
  <div class="quick-card">
    <h3>Good idea</h3>
    <p>Has a narrow user, a trusted corpus, one workflow action, and a two-minute demo story.</p>
  </div>

  <div class="quick-card">
    <h3>Risky idea</h3>
    <p>Requires confidential data, broad automation, unclear users, or production integrations you cannot safely mock.</p>
  </div>

  <div class="quick-card">
    <h3>Best hackathon shape</h3>
    <p>A grounded assistant that answers with citations, performs one approval-gated action, and produces a trust scorecard.</p>
  </div>
</div>

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Complete Step 0</a>
</div>
