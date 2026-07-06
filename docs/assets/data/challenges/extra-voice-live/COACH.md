
# Coach Guide · Extra — Give It a Voice (Voice Live API)

> **Coach-only.** Highest *wow-per-effort* Extra and the best demo-day closer, but it has two hard
> dependencies that fail silently: regional API access and a working mic/speaker on the client.
> Verify both before anyone starts.

## What this challenge is really teaching

That the agent and the interface are separable. Students have only ever typed; Voice Live shows the
*same grounded agent* behind a real-time speech channel. The conceptual win is full-duplex streaming
(incremental audio in *and* out) versus the naive STT → agent → TTS pipeline — that's where the
sub-second latency and barge-in come from. Don't let teams build three separate calls; Voice Live is one
session.

## Infra to pre-provision (do this BEFORE the session)

1. Voice Live API access on an Azure AI Speech / Foundry resource in a supported region —
   confirm availability for your event subscription/region *weeks ahead*; it's newer and not everywhere.

2. Keyless RBAC for the project identity (or a key as workshop fallback) on the Speech/Voice resource.
3. Client hardware: each team needs a laptop with a working mic + speakers (headset is better —
   avoids feedback/echo in a noisy room). This is the #1 silent failure.

4. Confirm `azure-ai-voicelive` installs cleanly via `pip install azure-ai-voicelive` (install on demand; not pre-pinned).

> **Flag for the coordinator:** if the venue is loud, headsets or a quiet breakout corner make or break
> the demo. Echo cancellation only goes so far.

## Search-Before-Implement

`azure-ai-voicelive` connect/session signatures are new and changing. Send teams to `microsoft-docs`
for the current connect call and event names before coding. The event names in Step 2
(`session.created`, response audio deltas, response-done) are illustrative — confirm the live ones.

## Per-step facilitation

### Step 1 — connect
- **Pitfall:** binding to a bare model instead of the agent → spoken answers lose persona/grounding.
  They must pass `AZURE_FOUNDRY_AGENT_NAME` so turns run through the Northfield agent.

- Auth errors here are usually region/access, not code. Check the resource supports Voice Live.

### Step 2 — duplex loop
- **Pitfall:** buffering the entire response before playback → kills the latency demo. Play audio deltas
  as they stream. If it sounds laggy, this is why.

- Mic permissions on macOS/Linux trip people up — confirm the OS granted the terminal/IDE mic access.

### Step 3 — natural conversation
- VAD/turn-detection and barge-in are the "feels real" features. If a team is short on time, VAD is the
  priority; barge-in is the flourish.

- On the Step 4 grounded agent, confirm the spoken answer is actually grounded (cite-worthy content),
  proving the voice path didn't bypass the knowledge base.

## Why no `validate.py`

The deliverable is audio — inherently a live/portal demo. Verify by watching/hearing a spoken
multi-turn conversation with one barge-in. A short screen+audio recording is the artifact for the readout.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| No audio out | playback waits for full response | play streamed audio deltas incrementally |
| Auth/region error on connect | Voice Live not available in region | use a supported region / resource |
| Echo / feedback loop | open speakers + mic | use a headset; enable echo cancellation |
| Answers ignore the corpus | bound to model not agent | bind session to `AZURE_FOUNDRY_AGENT_NAME` |
| Push-to-talk feels clunky | VAD not enabled | enable server-side turn detection |
