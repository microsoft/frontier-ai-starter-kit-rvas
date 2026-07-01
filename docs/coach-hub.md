---
title: Coach Hub
nav_order: 8
has_children: false
---

# Coach Hub

Your job is to create momentum, not to become the team's keyboard. In What The Hack, great coaching means asking better questions rather than giving faster answers.

Coaches for this event should focus on facilitation, pacing, and unblock strategy. Student-facing challenge pages stay public; full solution guides remain in the repository so you can use them selectively when a team is truly stuck.

## Event Day Checklist

### Pre-event

- Verify participants have a working GitHub path and an Azure subscription route
- Confirm you can access the repo locally, including `solution.md` files in each challenge folder
- Skim the challenge sequence so you know where setup ends and AI work begins
- Check the event’s escalation path for Azure subscription or portal issues
- Run the opening triage below so each team starts from a route, not from a random challenge page

### During the event

- **Start every team from their outcome, not from the tutorial.** Briefly review the selected route before touching Foundations Step 1
- Start every team in **Foundations** (Step 1) and confirm their environment is actually usable
- Watch for drift: teams often think they are blocked by code when they are really blocked by setup
- Keep teams time-boxed and encourage strategic skipping if the event clock gets tight
- Use questions first, direct fixes second
- Keep customer teams focused on the outcome: cited answers, one governed action, a trust scorecard, and a 2-minute demo

### Post-event

- Help teams capture what they built and what they learned
- Encourage cleanup of unused Azure resources if the event requires it
- Share next-step learning resources for teams that want to keep building
- For customer teams, capture the pilot backlog, risks, missing data, permissions, and production-readiness gaps

## Opening triage

| Team state | Coach action |
|---|---|
| Has a customer scenario or business outcome | Send them to [Customer Build Step 0]({{ '/customer-outcome' | relative_url }}) before Foundations. |
| Has a customer or industry, but no idea | Run [Customer Challenge-Forge](https://github.com/microsoft/frontier-foundry-hackathon/blob/main/.github/skills/customer-challenge-forge/SKILL.md), pick one idea, then fill the canvas. |
| Wants pure upskilling | Send them through the [Upskill Track]({{ '/upskill' | relative_url }}) with Northfield. |

## Facilitation Principles

### Ask, don’t tell

Good prompts for teams:

- “What changed right before it stopped working?”
- “Where do you think the request is failing: auth, config, or code?”
- “What does success look like for this challenge?”
- “If you had to test one assumption first, which would it be?”

### Identify struggle vs. stuck

Healthy struggle looks like experimentation, note-taking, and narrowing hypotheses. A stuck team repeats the same failing action, cannot name the blocker, or loses confidence in the next step. Intervene when they stop learning from the attempt.

### Celebrate progress, not just completion

Call out good debugging, clear prompt design, and smart teamwork. Teams gain energy when you recognize real progress between checkpoints.

### Anchor customer work in outcomes

Every team — whether they have a real customer or are following the Northfield path — should work toward a defined outcome. The default for teams with a scenario is **Customer Build Mode**; Northfield is the **safe fallback** for pure upskilling.

In Customer Build Mode, keep the team from building a generic chatbot. Useful coaching questions:

- “What business workflow or decision improves if this works?”
- “Which source of truth should the agent cite before the customer trusts it?”
- “Which action is valuable enough to automate, but risky enough to require approval?”
- “What evidence will you show in the final two-minute demo?”
- “What risk would block a pilot if you do not address it?”

## Per-step / per-challenge timing guide

**Pre-event / opening session (~30 min):**

| Activity | Expected Time | Note |
|---|---|---|
| Customer Build Step 0 review | 20–30 min | Every customer team should have its scenario pack before touching Step 1. Use this window to challenge vague "knowledge sources" and help teams without a scenario run Customer Challenge-Forge. Teams that skip Step 0 tend to drift during Advanced challenges. |

**Tier 1 · Foundations** (one guided challenge, four ordered steps):

| Step | Expected Time | Warning Sign | Intervention |
|------|---------------|--------------|--------------|
| 1 Setup & Provisioning | 30 min | >45 min | Check Azure subscription, Codespaces readiness, `azd up`, and Foundry access. |
| 2 Model & Playground | 45 min | >1 hr | Verify model deployment, endpoint, and keyless auth (`DefaultAzureCredential`). |
| 3 Your First Agent | 1 hr | Agent answers out-of-scope/unsafe asks | Review persona, system instructions, and guardrails. |
| 4 Knowledge Base (IQ) | 1.5 hr | Answers hallucinate or lack citations | Check indexing, grounding data quality, and IQ knowledge base wiring. |

**Tier 2 · Advanced** (modular, any order — each assumes the Foundations end-state):

| Advanced challenge | Expected Time | Warning Sign | Intervention |
|--------------------|---------------|--------------|--------------|
| Action Tools | 1–1.5 hr | Tool fires without approval, or never fires | Inspect the MCP `requires_action` loop and approval gate. |
| Evaluation & Red Teaming | 1–1.5 hr | Teams ignore metrics they do not like | Reframe metrics as design feedback; check the CI score gate. |
| Tracing & Observability | 1 hr | No spans land in App Insights | Confirm GenAI tracing env vars are set **before** SDK import. |
| Deploy as a Hosted Agent | 1–1.5 hr | Image builds but endpoint 401/500s | Check ACR push, `agent.yaml`, and per-agent managed identity. |
| Extras (Fabric IQ, Voice Live, Magentic Workflows, Build a UI, …) | 45–90 min each | Teams lose 30+ min on unrelated concepts | Anchor each Extra to the outcome: *"what does this add to the prototype for your customer?"* |

**Tier 3 · Capstone** *(optional — only attempt if Foundations + ≥1 Advanced are complete)*:

| Activity | Expected Time | When to recommend | When to skip |
|---|---|---|---|
| Capstone (multi-agent router + specialists) | 1.5–2 hr | Team finished Foundations + 2+ Advanced with 2+ hr remaining | Team still on Step 4 or has only one Advanced complete — don't split attention. |

**Event-level pacing heuristic:** If a team is on Step 3 or later at the 3-hour mark and has a customer scenario, encourage them to start thinking about which Advanced challenge maps most directly to their customer outcome. Not every team needs every Advanced challenge — depth on one is often more valuable than breadth on three.

**Extras choice guide:** Steer teams toward the Extra that connects to their canvas:

| Canvas signal | Suggested Extra |
|---|---|
| Customer wants live data or BI integration | Fabric IQ |
| Customer uses voice / contact center | Voice Live |
| Multi-department workflow, handoffs | Magentic Workflows |
| Customer wants a stakeholder-facing UI | Build a UI |
| Team wants to build faster with AI | Copilot-Assisted Build |

## Common blockers across all challenges

| Blocker | What it usually means | What to do |
|---------|------------------------|------------|
| “Azure is broken” | Wrong tenant, missing subscription, or quota issue | Re-check account, subscription, and region before touching code. |
| “The model is not responding” | Deployment mismatch or bad credentials | Confirm the exact deployment name, endpoint URL, and key source. |
| “The agent answers anything” | Persona/guardrails not applied | Re-check system instructions and refusal behavior for out-of-scope asks. |
| “RAG answers are off-topic” | Weak retrieval or poor chunk quality | Verify indexing, source data, and whether grounding is actually enabled. |
| “Nothing works anymore” | Several changes landed at once | Roll back to the last known-good step and recover incrementally. |

## Per-challenge coach notes

Each challenge has a coach-only reference page with the expected solution path, common blockers, and timing tips. These pages are hidden from the main navigation so students do not stumble into them.

<div class="challenge-card" markdown="1">

| Challenge | Coach view |
| --- | --- |
| Foundations | [Coach notes]({{ '/challenges/foundations-coach' | relative_url }}) |
| Advanced — Action Tools | [Coach notes]({{ '/challenges/advanced-action-tools-coach' | relative_url }}) |
| Advanced — Evaluation & Red Teaming | [Coach notes]({{ '/challenges/advanced-evaluation-redteam-coach' | relative_url }}) |
| Advanced — Tracing & Observability | [Coach notes]({{ '/challenges/advanced-tracing-observability-coach' | relative_url }}) |
| Advanced — Deploy as a Hosted Agent | [Coach notes]({{ '/challenges/advanced-deploy-hosted-agent-coach' | relative_url }}) |
| Extra — Fabric IQ | [Coach notes]({{ '/challenges/extra-fabric-iq-coach' | relative_url }}) |
| Extra — Give It a Voice | [Coach notes]({{ '/challenges/extra-voice-live-coach' | relative_url }}) |
| Extra — Magentic Workflows | [Coach notes]({{ '/challenges/extra-magentic-workflows-coach' | relative_url }}) |
| Extra — Hosted Long-Running Agents | [Coach notes]({{ '/challenges/extra-hosted-longrunning-coach' | relative_url }}) |
| Extra — Build a UI | [Coach notes]({{ '/challenges/extra-build-ui-coach' | relative_url }}) |
| Extra — Copilot-Assisted Build | [Coach notes]({{ '/challenges/extra-copilot-assisted-coach' | relative_url }}) |

</div>

## Solution guides are in the repo

Coach solution guides are published as themed pages on this site (see the table above) and are also available as raw files in the repository. Clone the repository and use `challenges/*/solution.md` as a back-pocket reference when teams need structured rescue help without opening a browser.

<p class="coach-note">Use solution guides to restore momentum, not to short-circuit discovery.</p>

## Emergency resources

- Microsoft Foundry documentation: <https://learn.microsoft.com/azure/foundry/>
- Azure status page: <https://azure.status.microsoft/en-us/status>
- Portal sign-in/account issues: confirm tenant, subscription, and event instructions first
- Event escalation: follow your organizer’s support route for Azure Pass, quota, or tenant problems
