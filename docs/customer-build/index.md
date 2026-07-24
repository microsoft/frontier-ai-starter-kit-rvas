---
title: Customer Build Track
nav_order: 2
has_children: true
description: Bring a customer outcome and build a grounded, evaluated Foundry agent prototype.
---

<div class="hero-panel track-hero track-hero--customer">
  <span class="hero-kicker">Track 1 • Customer Build</span>
  <h1>Turn a real outcome into an agent the customer can decide to pilot.</h1>
  <p class="hero-tagline">Use Northfield as the reference shape, but make clear decisions about your customer data, actions, evidence, and operating plan as you build.</p>
  <div class="cta-row">
    <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Define your outcome</a>
    <a class="btn btn-outline" href="{{ '/customer-build/foundations' | relative_url }}">Ground your app</a>
  </div>
</div>

{% include journey-status.html tone="customer" path="Customer Build Track" artifact="One evolving scenario record plus the evidence needed for the next customer decision." next="Complete Define your outcome, then ground the app with approved data and Northfield as the reference." %}

## The customer route

<ol class="journey-map">
  <li><span>0</span><strong>Define</strong><small>Outcome, owners, data, boundaries</small></li>
  <li><span>1</span><strong>Ground</strong><small>Approved data and access assumptions</small></li>
  <li><span>2</span><strong>Act</strong><small>One deliberately governed workflow</small></li>
  <li><span>3</span><strong>Prove</strong><small>Quality, safety, and critical failures</small></li>
  <li><span>4</span><strong>Operate</strong><small>Trace data, service signals, and ownership</small></li>
  <li><span>5</span><strong>Decide</strong><small>Launch a pilot, harden first, or stop</small></li>
</ol>

This is a multi-week customer engagement, not a linear one-day checklist. Each chapter produces
evidence for a decision in the same [scenario record]({{ '/customer-outcome' | relative_url }}).
If a decision is “not yet,” narrow the outcome or close the named gap before moving on.

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

| Chapter | Reframes | Customer decision |
|---|---|---|
| [Define your outcome]({{ '/customer-outcome' | relative_url }}) | Scenario record: user, data, action, safety, demo | Is this bounded and owned well enough to build? |
| [Ground your app]({{ '/customer-build/foundations' | relative_url }}) | Foundations | Is it safe to test with intended users? |
| [Make it act]({{ '/customer-build/advanced-action-tools' | relative_url }}) | Action Tools | Is the side effect governed well enough to expose? |
| [Prove it's safe]({{ '/customer-build/advanced-evaluation-redteam' | relative_url }}) | Evaluation & Red Teaming | Is it safe for a controlled pilot? |
| [See inside it]({{ '/customer-build/advanced-tracing-observability' | relative_url }}) | Tracing & Observability | Can the team investigate and operate it safely? |
| [Ship it]({{ '/customer-build/advanced-deploy-hosted-agent' | relative_url }}) | Deploy as a Hosted Agent | Launch a pilot, harden first, or remain demo-only? |
| [Grow it into a team]({{ '/customer-build/capstone-multi-agent' | relative_url }}) | Multi-Agent Capstone | Only add roles when they make the outcome clearer or safer. |

Optional deepeners (do only if your scenario needs them):
[Magentic Workflows]({{ '/customer-build/extra-magentic-workflows' | relative_url }}) ·
[Long-Running Agents]({{ '/customer-build/extra-hosted-longrunning' | relative_url }}) ·
[Build a UI]({{ '/customer-build/extra-build-ui' | relative_url }}) ·
[Fabric IQ]({{ '/customer-build/extra-fabric-iq' | relative_url }}) ·
[Give It a Voice]({{ '/customer-build/extra-voice-live' | relative_url }}) ·
[Copilot-Assisted Build]({{ '/customer-build/extra-copilot-assisted' | relative_url }})

## Build order for a customer engagement

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Start here</span>
    <h3>Define, then ground</h3>
    <p>Agree the bounded outcome, owners, data, and access assumptions; then prove the agent can answer from trusted sources.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Build confidence</span>
    <h3>Action + evaluation</h3>
    <p>Only add a useful action when its request, approval, escalation, and evidence are clear; then prove quality, refusal, and safety behavior.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Make a decision</span>
    <h3>Operate + ship</h3>
    <p>Decide how traces are handled, who investigates problems, and whether the evidence supports a controlled pilot, more hardening, or a demo-only result.</p>
  </div>
</div>

## Your first move

Complete [Define your outcome]({{ '/customer-outcome' | relative_url }}) before starting Foundations. If you do not have an app idea yet, go through [Idea Forge]({{ '/idea-forge' | relative_url }}) first; it feeds directly into Define your outcome.

<div class="next-panel">
  <strong>Next:</strong>
  <a class="btn btn-primary" href="{{ '/customer-outcome' | relative_url }}">Complete Define your outcome</a>
</div>
