---
title: Facilitator Hub
nav_order: 8
has_children: false
---

# Facilitator Hub

Your job is to create momentum, not to become the team's keyboard. In session facilitation means asking better questions rather than giving faster answers.

Facilitators for this event should focus on facilitation, pacing, and unblock strategy. Student-facing activity pages stay public; full solution guides remain in the repository so you can use them selectively when a team is truly stuck.

For Customer Build, think beyond a single event. The build may span several weeks, and each chapter
should help the customer make one useful decision: continue, narrow the scope, harden a gap, or
start a controlled pilot. Keep the [scenario record]({{ '/customer-outcome' | relative_url }}) as
the one shared record; do not ask teams to create separate governance paperwork.

## Event Day Checklist

### Pre-event

- Verify participants have a working GitHub path and an Azure subscription route
- Confirm you can access the repo locally, including `solution.md` files in each activity folder
- Skim the activity sequence so you know where setup ends and AI work begins
- Check the event’s escalation path for Azure subscription or portal issues
- Run the opening triage below so each team starts from a route, not from a random activity page
- For Customer Build, identify the business, technical, and data owners before the first build session

### During the event

- **Start every team from their outcome, not from the tutorial.** Briefly review the selected route before touching Foundations Step 1
- Start every team in **Foundations** (Step 1) and confirm their environment is actually usable
- Watch for drift: teams often think they are blocked by code when they are really blocked by setup
- Keep teams time-boxed and encourage strategic skipping if the event clock gets tight
- Use questions first, direct fixes second
- Keep customer teams focused on the outcome: cited answers, one governed action, a trust scorecard, and a 2-minute demo
- At each Customer Build checkpoint, ask for a decision and its reason, not a polished document

### Post-event

- Help teams capture what they built and what they learned
- Encourage cleanup of unused Azure resources if the event requires it
- Share next-step learning resources for teams that want to keep building
- For customer teams, confirm whether the outcome is launch a controlled pilot, harden first, or remain demo-only; capture only the gaps that support that decision

## Opening triage

| Team state | Facilitator action |
|---|---|
| Has a customer scenario or business outcome | Send them to [Customer Build Step 0]({{ '/customer-outcome' | relative_url }}) before Foundations. |
| Has a customer or industry, but no idea | Run [Customer Activity-Forge](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/.github/skills/customer-activity-forge/SKILL.md), pick one idea, then fill the canvas. |
| Wants pure upskilling | Send them through the [Upskill Track]({{ '/upskill' | relative_url }}) with Northfield. |

## Facilitation Principles

### Ask, don’t tell

Good prompts for teams:

- “What changed right before it stopped working?”
- “Where do you think the request is failing: auth, config, or code?”
- “What does success look like for this activity?”
- “If you had to test one assumption first, which would it be?”

### Identify struggle vs. stuck

Healthy struggle looks like experimentation, note-taking, and narrowing hypotheses. A stuck team repeats the same failing action, cannot name the blocker, or loses confidence in the next step. Intervene when they stop learning from the attempt.

### Celebrate progress, not just completion

Call out good debugging, clear prompt design, and smart teamwork. Teams gain energy when you recognize real progress between checkpoints.

### Anchor customer work in outcomes

Every team — whether they have a real customer or are following the Northfield path — should work toward a defined outcome. The default for teams with a scenario is **Customer Build Mode**; Northfield is the **safe fallback** for pure upskilling.

In Customer Build Mode, keep the team from building a generic chatbot. Useful facilitation questions:

- “What business workflow or decision improves if this works?”
- “Which source of truth should the agent cite before the customer trusts it?”
- “Which action is valuable enough to automate, but risky enough to require approval?”
- “What evidence will you show in the final two-minute demo?”
- “What risk would block a pilot if you do not address it?”

## Customer Build decision checkpoints

Use these checkpoints across the engagement. They are conversation guides, not additional
deliverables.

| Point in the journey | Ask the customer | Useful outcome |
|---|---|---|
| Define | “Is this use case owned, bounded, and safe enough to build?” | Named owners, intended users, approved data, and a narrow first outcome |
| Ground | “Can intended users safely test answers from these sources?” | Cited answers, abstention behavior, source ownership, and stated access assumptions |
| Act | “Who can request, approve, deny, and investigate this side effect?” | A compact action policy and an appropriate draft/escalation path where needed |
| Prove | “What failure would make a pilot unacceptable?” | Scenario-specific evaluation, red-team evidence, and explicit residual risks |
| Operate | “Can we find and handle a bad run without exposing sensitive trace data?” | Trace-data choices, service signal, and a named investigation owner |
| Ship | “Do we launch a controlled pilot, harden first, or remain demo-only?” | A clear recommendation, owner, and next action |

## Per-step / per-activity timing guide

**Customer Build kickoff:**

| Activity | Expected Time | Note |
|---|---|---|
| Customer Build Step 0 review | 20–30 min | Every customer team should have its scenario record before touching Step 1. Clarify vague "knowledge sources," name owners, and agree the first decision. Teams that skip Step 0 tend to drift during Advanced activities. |

**Tier 1 · Foundations** (one guided activity, four ordered steps):

| Step | Expected Time | Warning Sign | Intervention |
|------|---------------|--------------|--------------|
| 1 Setup & Provisioning | 30 min | >45 min | Check Azure subscription, Codespaces readiness, `azd up`, and Foundry access. |
| 2 Model & Playground | 45 min | >1 hr | Verify model deployment, endpoint, and keyless auth (`DefaultAzureCredential`). |
| 3 Your First Agent | 1 hr | Agent answers out-of-scope/unsafe asks | Review persona, system instructions, and guardrails. |
| 4 Knowledge Base (IQ) | 1.5 hr | Answers hallucinate or lack citations | Check indexing, grounding data quality, and IQ knowledge base wiring. |

**Tier 2 · Advanced** (modular, any order — each assumes the Foundations end-state):

| Advanced activity | Expected Time | Warning Sign | Intervention |
|--------------------|---------------|--------------|--------------|
| Action Tools | 1–1.5 hr | Tool fires without approval, or never fires | Inspect the Responses function-call loop and approval gate. |
| Evaluation & Red Teaming | 1–1.5 hr | Teams ignore metrics they do not like | Reframe metrics as design feedback; check the CI score gate. |
| Tracing & Observability | 1 hr | No spans land in App Insights | Confirm GenAI tracing env vars are set **before** SDK import. |
| Deploy as a Hosted Agent | 1–1.5 hr | Deployment completes but endpoint 401/500s | Check `azure.yaml`, hosted logs, and per-agent managed identity. |
| Extras (Fabric IQ, Voice Live, Magentic Workflows, Build a UI, …) | 45–90 min each | Teams lose 30+ min on unrelated concepts | Anchor each Extra to the outcome: *"what does this add to the prototype for your customer?"* |

**Tier 3 · Capstone** *(optional — only attempt if Foundations + ≥1 Advanced are complete)*:

| Activity | Expected Time | When to recommend | When to skip |
|---|---|---|---|
| Capstone (multi-agent router + specialists) | 1.5–2 hr | Team finished Foundations + 2+ Advanced with 2+ hr remaining | Team still on Step 4 or has only one Advanced complete — don't split attention. |

**Event-level pacing heuristic:** If a team is on Step 3 or later at the 3-hour mark and has a customer scenario, encourage them to start thinking about which Advanced activity maps most directly to their customer outcome. Not every team needs every Advanced activity — depth on one is often more valuable than breadth on three.

**Extras choice guide:** Steer teams toward the Extra that connects to their canvas:

| Canvas signal | Suggested Extra |
|---|---|
| Customer wants live data or BI integration | Fabric IQ |
| Customer uses voice / contact center | Voice Live |
| Multi-department workflow, handoffs | Magentic Workflows |
| Customer wants a stakeholder-facing UI | Build a UI |
| Team wants to build faster with AI | Copilot-Assisted Build |

## Common blockers across all activities

| Blocker | What it usually means | What to do |
|---------|------------------------|------------|
| “Azure is broken” | Wrong tenant, missing subscription, or quota issue | Re-check account, subscription, and region before touching code. |
| “The model is not responding” | Deployment mismatch or bad credentials | Confirm the exact deployment name, endpoint URL, and key source. |
| “The agent answers anything” | Persona/guardrails not applied | Re-check system instructions and refusal behavior for out-of-scope asks. |
| “RAG answers are off-topic” | Weak retrieval or poor chunk quality | Verify indexing, source data, and whether grounding is actually enabled. |
| “Nothing works anymore” | Several changes landed at once | Roll back to the last known-good step and recover incrementally. |

## Per-activity facilitator notes

Each activity has a facilitator-only reference page with the expected solution path, common blockers, and timing tips. These pages are hidden from the main navigation so students do not stumble into them.

<div class="activity-card" markdown="1">

| Activity | Facilitator view |
| --- | --- |
| Foundations | [Facilitator notes]({{ '/activities/foundations-facilitator' | relative_url }}) |
| Advanced — Action Tools | [Facilitator notes]({{ '/activities/advanced-action-tools-facilitator' | relative_url }}) |
| Advanced — Evaluation & Red Teaming | [Facilitator notes]({{ '/activities/advanced-evaluation-redteam-facilitator' | relative_url }}) |
| Advanced — Tracing & Observability | [Facilitator notes]({{ '/activities/advanced-tracing-observability-facilitator' | relative_url }}) |
| Advanced — Deploy as a Hosted Agent | [Facilitator notes]({{ '/activities/advanced-deploy-hosted-agent-facilitator' | relative_url }}) |
| Extra — Fabric IQ | [Facilitator notes]({{ '/activities/extra-fabric-iq-facilitator' | relative_url }}) |
| Extra — Give It a Voice | [Facilitator notes]({{ '/activities/extra-voice-live-facilitator' | relative_url }}) |
| Extra — Magentic Workflows | [Facilitator notes]({{ '/activities/extra-magentic-workflows-facilitator' | relative_url }}) |
| Extra — Hosted Long-Running Agents | [Facilitator notes]({{ '/activities/extra-hosted-longrunning-facilitator' | relative_url }}) |
| Extra — Build a UI | [Facilitator notes]({{ '/activities/extra-build-ui-facilitator' | relative_url }}) |
| Extra — Copilot-Assisted Build | [Facilitator notes]({{ '/activities/extra-copilot-assisted-facilitator' | relative_url }}) |

</div>

## Solution guides are in the repo

Facilitator solution guides are published as themed pages on this site (see the table above) and are also available as raw files in the repository. Clone the repository and use `activities/*/solution.md` as a back-pocket reference when teams need structured rescue help without opening a browser.

<p class="facilitator-note">Use solution guides to restore momentum, not to short-circuit discovery.</p>

## Emergency resources

- Microsoft Foundry documentation: <https://learn.microsoft.com/azure/foundry/>
- Azure status page: <https://azure.status.microsoft/en-us/status>
- Portal sign-in/account issues: confirm tenant, subscription, and event instructions first
- Event escalation: follow your organizer’s support route for Azure Pass, quota, or tenant problems
