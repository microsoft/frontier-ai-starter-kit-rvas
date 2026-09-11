# Module 1 — Select the avatar/experience capability

Make this decision first. The capability you choose sets the API surface, regions, cost model,
latency, accessibility obligations, and the **responsible-AI gating** that can add weeks of
registration. A poor choice creates rework in modules 2–7.

Speech features change quickly, and several are preview or limited-access. Check current Microsoft
Learn guidance before you commit.

![Experience capability decision](../diagrams/01-experience-capability-choice.png)

## What you build

An avatar experience that uses a supported API, meets the responsible-AI gates, and has an
accessible fallback.

## Choose your path

Five Microsoft capabilities can deliver an avatar-led or spoken onboarding moment. They serve
different needs.

| Option | What it is | Best when | Real-time? | Custom likeness/voice gating | Status |
| --- | --- | --- | --- | --- | --- |
| **A. Speech TTS avatar — batch synthesis** *(default)* | Async REST job renders a talking-avatar **video file** from text/SSML | Pre-produced, reviewable onboarding videos you approve once and replay | No (async job) | Standard avatar+voice = none; custom = limited access | GA (`api-version=2024-08-01`) |
| B. Speech TTS avatar — real-time synthesis | Speech SDK streams avatar video over **WebRTC** live | A live, interactive kiosk/agent that shows a face | Yes | Same as A | GA |
| C. Voice Live API | Fully-managed **speech-to-speech** voice agent; can also emit **avatar visuals** | A conversational onboarding assistant you speak to | Yes | Same as A when avatar is on | See docs (maps to `extra-voice-live`) |
| D. Video translation | Localises an **existing** onboarding video into other languages, preserving the speaker's voice | You already have approved video and need many locales | No (batch) | Voice replication of a real speaker — treat as consent-bearing | GA-ish; verify |
| E. Plain audio (TTS / Voice Live audio-only) | Natural-voice narration, **no face** | Accessibility-first, lowest cost/risk, no likeness | Either | Standard voice = none | GA |

**Default: Option A (batch avatar synthesis).** Onboarding content is authored, reviewed, and
replayed. It is not a live conversation. Batch synthesis produces a reviewable video that fits the
module-6 human-approval gate. It uses a **standard** avatar and voice, so there is *no* talent
likeness to license or limited-access form to file. It is the lowest-cost path to a governed pilot.
Verified overview:
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar>

**Migration cost.**
- **A → B** (batch → real-time) is moderate. Keep the avatars/voices, swap the REST poll for a
  Speech-SDK WebRTC client, and add TURN/firewall and per-session-latency work.
- **A → C** (batch → Voice Live) is a larger rebuild. You move from rendering a video to running a
  live speech-to-speech agent. See the `extra-voice-live` activity.
- **A → E** (drop the avatar) is trivial and always available as your accessibility fallback.
- **Anything → custom avatar or custom/personal voice** is the expensive jump. It triggers
  **limited-access registration** and talent consent (see Implementation → RAI). Budget weeks.
  Do not promise a customer's CEO's face in a demo.

## Implementation

Each option below lists the required configuration and verified facts.

### Option A — Speech TTS avatar, batch synthesis (default)

**API (verified).** Batch synthesis is a REST job on the Speech/AIServices resource host:

```
PUT  https://{resource}.cognitiveservices.azure.com/avatar/batchsyntheses/{SynthesisId}?api-version=2024-08-01
GET  https://{resource}.cognitiveservices.azure.com/avatar/batchsyntheses/{SynthesisId}?api-version=2024-08-01
```

Submit text or SSML, poll `status` (`NotStarted → Running → Succeeded/Failed`), then download
`outputs.result` (an `.mp4`). Limits are payload ≤ 500 KB, up to 200 concurrent jobs per resource,
and output ≤ 20 minutes. Standard resolution defaults to 1920×1080 at 25 FPS.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/batch-synthesis-avatar>

**Identity (verified).** The Speech data plane accepts a Microsoft Entra token **only if the
resource has a custom subdomain**. Module 2's Bicep sets `customSubDomainName`, so avatar synthesis
is keyless. Assign **Cognitive Services Speech User**
(`f2dc8367-1007-4938-bd23-fe263f013447`); the generic *Cognitive Services Contributor* / *Owner*
roles grant **no** Speech data access.
<https://learn.microsoft.com/azure/ai-services/speech-service/role-based-access-control>

### Option B — Speech TTS avatar, real-time synthesis

Real-time streams the avatar video to the browser over **WebRTC** via the Speech SDK. It needs the
**Standard S0** tier and outbound access to the TURN relay
`relay.communication.microsoft.com` (UDP 3478 / TCP 443, `20.202.0.0/16`); fetch ICE server details
from the Speech REST API. You set `AvatarConfig("lisa", "casual-sitting")` and a voice such as
`en-US-Ava:DragonHDLatestNeural`.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/real-time-synthesis-avatar>

Choose it only for genuinely interactive onboarding. Otherwise, Option A is cheaper and reviewable.

### Option C — Voice Live API

Voice Live is a **fully-managed speech-to-speech** interface: one WebSocket streams mic audio in and
returns audio, **avatar visuals**, and action triggers — no manual STT→LLM→TTS stitching. It covers
140+ STT locales and 600+ voices across 150+ locales, and **agent mode authenticates with Microsoft
Entra ID** (not a Speech key).
<https://learn.microsoft.com/azure/ai-services/speech-service/voice-live>

Build this in the [Voice Live activity](../../../activities/extra-voice-live/README.md). Record
`"selected_capability": "voice-live-realtime-avatar"` (or
`voice-live-audio`) and note that a live agent needs module 4's grounded agent first.

### Option D — Video translation

Video translation localises an **existing** approved video into more languages while replicating the
original speaker's voice. Use it only when you already have signed-off video and a multilingual
cohort. Because it replicates a real person's voice, treat the source as consent-bearing.
<https://learn.microsoft.com/azure/ai-services/speech-service/video-translation-overview>

Treat the original speaker's consent as a gate even though no *custom* model is trained.

### Option E — Plain audio (accessibility-first)

Standard-voice narration with no face. Lowest cost and lowest risk, and it is **also your mandatory
non-avatar fallback** for every other option (module 5). Choose it when a face adds risk without
value.

### The responsible-AI gate (applies to A–D, verified)

Missing this can turn a two-day build into a two-month program.

- **Standard avatar + standard voice: no registration.** Disclosure to users is still required.
- **Custom avatar (video/photo) or custom/personal voice: Limited Access.** Available only by
  registration to customers managed by Microsoft, through the intake form
  <https://aka.ms/customneural>. A **custom video avatar needs ≥ 10 minutes of the actor's video**
  and their **explicit written consent**; you must share the *Disclosure for voice and avatar talent*
  with them in advance, may only use approved use cases, must **disclose the synthetic nature** to
  end users, and must offer a feedback channel.
  <https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access>
- **Disclosure design** (how and when to tell users it's synthetic):
  <https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines>

In Verify, enforce this consistency rule: if the record says you use a custom avatar or
custom/personal voice, it must also record `limited_access_registration_required`,
`talent_consent_required`, and the form URL. Otherwise, legal review discovers the missing gate
after the build.

## Verify

You have not provisioned anything. Verify the external facts before you choose a capability.

**1. The region you named actually offers the capability you chose.** Avatar and Voice Live are
region-gated. Open the Speech regions table and find your region in the column for your capability
(batch avatar, real-time avatar, or Voice Live):

<https://learn.microsoft.com/azure/ai-services/speech-service/regions?tabs=ttsavatar>

Your region must have a check in that column. Otherwise, avatar pricing will not display there and
module 2 cannot provision the feature. Change `region` in the record now.
At the time of writing, batch and real-time avatar are offered in `westus2`, `eastus`, `eastus2`,
`southcentralus`, `southeastasia`, `centralindia`, `westeurope`, `swedencentral`, `northeurope`,
`italynorth`, and `francecentral` (limited capacity). Re-read the table; the list changes.

**2. The responsible-AI gate is complete.** If you use a custom avatar or custom/personal voice,
complete the limited-access registration and obtain talent consent through
`https://aka.ms/customneural`. A custom avatar or custom/personal voice without the
limited-access path fails legal review after the build. Standard prebuilt avatar and voice need no
registration.
<https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/limited-access>

**3. A disclosure statement is present even for a standard avatar.** Users must be told the presenter
is synthetic whether or not a custom likeness is used:

An empty or missing disclosure lets an undisclosed synthetic persona reach employees, which the
disclosure guidance forbids:
<https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines>

## Next module

[Module 2 — Provision the Foundry + Speech foundation](02-foundation.md) deploys the keyless
resources this decision implies.
