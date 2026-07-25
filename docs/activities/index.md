---
title: Build Modules
nav_order: 6
has_children: true
---

# Build Modules

{% include journey-status.html tone="shared" path="Build Modules" artifact="Reusable hands-on implementation guides." next="Choose the capability your prototype needs next, then open the hands-on guide." %}

These are reusable implementation modules. Start from a scenario playbook, then open only the
building blocks needed for the current customer decision.

## Primary build spine

<div class="activity-card" markdown="1">

| Capability | What you build | Hands-on guide |
|---|---|---|
| Ground | Build a grounded assistant with citations. | [Ground: Foundations](foundations) |
| Act | Use ticket, hold, and advising actions. | [Act: Action Tools](advanced-action-tools) |
| Prove | Run evaluation and red-team sets. | [Prove: Evaluation & Red Teaming](advanced-evaluation-redteam) |
| Debug | Inspect runs in Foundry and App Insights. | [Debug: Tracing & Observability](advanced-tracing-observability) |
| Deploy | Host the agent. | [Deploy: Hosted Agent](advanced-deploy-hosted-agent) |
| Demo UI | Build a stakeholder-facing chat demo. | [Demo UI: Build a UI](extra-build-ui) |
| Orchestrate | Turn the agent into a specialist team. | [Orchestrate: Multi-Agent Capstone](capstone-multi-agent) |

</div>

## Optional deepeners

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Live data</span>
    <h3><a href="extra-fabric-iq">Deepen: Fabric IQ</a></h3>
    <p>Ground answers in operational data when static documents are not enough.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Documents</span>
    <h3><a href="extra-document-workflow">Build: Document Workflow</a></h3>
    <p>Extract, validate, review, and route document data without silently trusting low-confidence fields.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Vision</span>
    <h3><a href="extra-visual-multimodal">Build: Visual Multimodal</a></h3>
    <p>Turn approved images into structured, uncertainty-aware results with a human-review boundary.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Data governance</span>
    <h3><a href="extra-governed-data-copilot">Build: Governed Data Copilot</a></h3>
    <p>Query operational data through explicit field, access, and provenance controls.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Interface</span>
    <h3><a href="extra-voice-live">Interface: Voice Live</a></h3>
    <p>Add a spoken interaction path for contact-center, accessibility, or demo scenarios.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Orchestrate</span>
    <h3><a href="extra-magentic-workflows">Orchestrate: Magentic Workflows</a></h3>
    <p>Explore manager/planner orchestration before or after the capstone.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Deploy</span>
    <h3><a href="extra-hosted-longrunning">Deploy: Long-Running Agents</a></h3>
    <p>Use background run patterns for workflows that outlive a browser session.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Accelerate</span>
    <h3><a href="extra-copilot-assisted">Accelerate: Copilot-Assisted Build</a></h3>
    <p>Use skills and MCP deliberately instead of guessing fast-moving Foundry APIs.</p>
  </div>
</div>

## Choosing modules

<div class="quick-grid">
  <div class="quick-card">
    <span class="track-badge">Scenario first</span>
    <h3><a href="{{ '/#outcomes' | relative_url }}">Choose a scenario playbook</a></h3>
    <p>The playbook decides which capabilities matter and when to open a reference module.</p>
  </div>

  <div class="quick-card">
    <span class="track-badge">Reference Library</span>
    <h3><a href="{{ '/reference.html' | relative_url }}">Browse building blocks</a></h3>
    <p>Use capability filters when you already know which implementation mechanic you need.</p>
  </div>
</div>
