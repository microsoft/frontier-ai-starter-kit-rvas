---
title: "Give It a Voice"
parent: Customer Build Track
nav_order: 78
description: Turn your scenario assistant into a low-latency spoken experience when voice is the right interface.
---

# Customer Build · Give It a Voice

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Voice" artifact="A spoken version of YOUR agent that listens, answers, and preserves grounding or safety behavior." next="Use voice only when it improves access, speed, or demo impact for your users." %}

This deepener is mutuated from [Extra · Give It a Voice](../activities/extra-voice-live) — same Voice Live pattern, but bound to your scenario agent from [Define your outcome](../customer-outcome). This is an OPTIONAL deepener. Voice is memorable, but it is not required for most build-track apps.

> Before you start this deepener: confirm Voice Live access in a supported region and a microphone/speaker client. If typed interaction is better for your users, skip this.

---

## Step 1 — Connect a Voice Live session to your agent

**Why it matters for your app:** binding voice to your existing agent preserves the persona, grounding, and guardrails you already built.

**Does this apply to you?** → Skip it if your target users are better served by text, forms, or an existing channel.
- Build it if hands-free or low-friction access is central to the scenario.
- Adapt it if voice should be a demo-only interface over the same backend.

**Decisions to make:**
- Which target user benefits from speaking instead of typing?
- Which agent should voice bind to: basic, grounded, or tool-enabled?
- What voice, language, and audio environment fit the demo?

**Apply it to your app:** open a Voice Live session against your Foundry endpoint and bind it to your scenario agent. → [Extra · Give It a Voice — Step 1](../activities/extra-voice-live#step-1--connect-a-voice-live-session-to-your-agent)

**Prove you applied it:**
- □ The client creates a Voice Live session without auth errors.
- □ Spoken turns run through your named agent, not a generic model.
- □ The configured voice and language fit the target user.

**Stuck?** [Northfield Step 1](../activities/extra-voice-live#step-1--connect-a-voice-live-session-to-your-agent).

---

## Step 2 — Speak in, hear out

**Why it matters for your app:** full-duplex audio is the capability users feel; the assistant should respond naturally without waiting for a full text round trip.

**Does this apply to you?** → Skip it if your environment cannot support a live audio demo reliably.
- Build it if your demo story is stronger with a spoken question and audible answer.
- Adapt it if you use recorded audio to avoid venue noise.

**Decisions to make:**
- Which scenario question is short, safe, and easy to understand aloud?
- What should the assistant say when it cannot hear or lacks grounding?
- How will you capture proof: live demo, recording, or facilitator sign-off?

**Apply it to your app:** stream microphone audio into the session and play response audio as it arrives. → [Extra · Give It a Voice — Step 2](../activities/extra-voice-live#step-2--speak-in-hear-out-the-full-duplex-loop)

**Prove you applied it:**
- □ Speaking a scenario question produces an audible answer.
- □ Audio starts before the full response is complete.
- □ The answer still follows your persona and safety boundaries.

**Stuck?** [Northfield Step 2](../activities/extra-voice-live#step-2--speak-in-hear-out-the-full-duplex-loop).

---

## Step 3 — Tune for natural conversation

**Why it matters for your app:** natural turn-taking and interruption make voice usable instead of a novelty.

**Does this apply to you?** → Skip it if a single recorded question is enough for your readout.
- Build it if users will have multi-turn spoken conversations.
- Adapt it if you only need VAD or only need barge-in.

**Decisions to make:**
- Should the assistant auto-detect end of speech or use push-to-talk?
- What interruption behavior is safe for your domain?
- Which grounded question proves voice still uses your corpus?

**Apply it to your app:** tune turn detection, barge-in, and a grounded spoken prompt for your scenario. → [Extra · Give It a Voice — Step 3](../activities/extra-voice-live#step-3--tune-for-natural-conversation)

**Prove you applied it:**
- □ Turn-taking works without awkward manual control.
- □ Barge-in interrupts the assistant and returns to listening.
- □ A grounded spoken answer reflects your approved corpus or safely abstains.

**Stuck?** [Northfield Step 3](../activities/extra-voice-live#step-3--tune-for-natural-conversation).

---

## Deepener end-state

You have a spoken interface only if voice helps your users or demo story. Deepeners are optional; return to the [Customer Build Track](../customer-build) and prioritize the outcome over novelty.
