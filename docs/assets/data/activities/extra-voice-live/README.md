# Extra · Give It a Voice — Voice Live API

> **Command context:** Run the bootstrap command from the repository root.

> Reusable interface module for realtime spoken interaction. Use it only when a scenario chooses a
> live voice branch. Prerequisite: a deployed scenario agent or the Foundations mechanics reference.
> Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> Specific prereq: Foundations Step 3 (a working agent). It works on the Step 3 agent; it's
> *better* on the Step 4 grounded agent (spoken answers gain citations).

> Infra prerequisite: Voice Live API access (Azure AI
> Speech / Foundry voice) in a supported region, and a microphone-capable client machine (laptop
> mic + speakers, or headset). See [solution.md](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/activities/extra-voice-live/solution.md) → *Infra to pre-provision*. Confirm
> regional availability before the session.
>
> Sample demo: speak a question, hear it answer in a
> natural voice with sub-second latency. The single strongest crowd demo of the event.

## Why this activity

Most activities so far have been typed. When the scenario earns a spoken interface, the user may
want to *ask*. The Voice Live API turns your text assistant into a spoken one: it streams
mic audio in, runs your agent, and streams synthesized speech back out, all over a single low-latency
WebSocket. No stitching together separate speech-to-text, agent, and text-to-speech calls — Voice Live
orchestrates the full duplex loop for you.

```text
   mic ──▶ Voice Live (STT) ──▶ scenario assistant ──▶ Voice Live (TTS) ──▶ speaker
              └────────────────── one low-latency streaming session ──────────────────┘
```

---

## Step 1 — Connect a Voice Live session to your agent

**Goal:** Open a Voice Live session bound to your scenario agent and confirm the handshake.

**Tasks:**
1. Install the current client SDK release (`pip install azure-ai-voicelive`) and confirm mic + speaker
   access on your machine. The current Python quickstart requires Python 3.10 or later.
2. Using the `azure-ai` speech skill pattern, open a Voice Live session against your Foundry
   endpoint. Search before you implement: query `microsoft-docs` for the *current* `azure-ai-voicelive`
   connect signature. The Python SDK is async-only, so run the session under an async event loop.
3. Bind the session to your existing agent (`AZURE_FOUNDRY_AGENT_NAME`) so spoken turns run *through your
   grounded agent*, not a generic model. Configure a voice (e.g. a neural voice) and the audio formats.

The existing project contract provides `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_FOUNDRY_AGENT_NAME`, and
`AZURE_AI_MODEL_DEPLOYMENT_NAME`. Voice Live **agent mode** also requires Voice Live resource/project
settings such as the Voice Live endpoint and project name, and may require an agent version. Keep these
in your local, untracked configuration; do not add a Voice Live endpoint or credentials to the tracked
root `.env.sample`. Agent mode uses Microsoft Entra ID authentication, not a Speech/API key.

**Success Criteria:**
- [ ] The client establishes a Voice Live session without auth errors.
- [ ] The session is bound to your scenario agent (not a bare model).

**Verify:** *Console state* — the client prints `session.created` (or equivalent) and a chosen voice id.

---

## Step 2 — Speak in, hear out (the full duplex loop)

**Goal:** Ask a question out loud and hear the assistant answer.

**Tasks:**
1. Stream microphone audio into the session and handle the streamed audio response, playing it back on
   your speakers.
2. Handle the core session events: input audio started/stopped, response audio deltas, and
   response-done. Play audio deltas as they arrive (don't wait for the full response — that's the latency win).
3. Ask: "When does fall registration open?" and listen to the spoken answer.

**Success Criteria:**
- [ ] Speaking a question produces an audible spoken answer.
- [ ] Audio plays back incrementally (you hear it start before the full answer is computed).

**Verify:** *Live demo* — speak a scenario question and the assistant answers out loud. Capture a
short screen+audio recording for the readout.

---

## Step 3 — Tune for natural conversation

**Goal:** Make it feel like a conversation, not a walkie-talkie.

**Tasks:**
1. Enable server-side voice activity detection (VAD) / turn detection so you don't push-to-talk —
   the assistant detects when you've stopped speaking.
2. Enable barge-in (interrupt): if you start talking while it's answering, it stops and listens.
3. (If on the Step 4 grounded agent) Ask a corpus question ("What's the tuition refund policy?") and
   confirm the spoken answer reflects grounded content — the voice path still uses your knowledge base.

**Success Criteria:**
- [ ] Turn-taking works without manual push-to-talk.
- [ ] You can interrupt (barge-in) mid-answer and it yields.
- [ ] (Grounded agent) a spoken answer reflects FAQ-corpus content.

**Verify:** *Live demo* — a multi-turn spoken conversation with at least one barge-in.

---

## What you built

A hands-free, spoken scenario assistant. Same grounded brain, new interface — the agent now
listens and talks back in real time, which is the demo people remember.
