# Module 5 — Generate the accessible avatar experience

Now you render the experience — but only from an **approved script revision**, and only with the
accessibility and disclosure guarantees a synthetic presenter legally and ethically requires. A great
avatar with no transcript, no caption, no disclosure, and no non-avatar path is a compliance
incident, not a demo.

Speech facts verified on learn.microsoft.com on **2026-07-24**.

## What you build

1. The rendered experience (a talking-avatar video, a real-time stream, a Voice Live session, or
   plain audio) produced from the approved artifact.
2. **Disclosure** that the presenter is synthetic/AI-assisted, shown/spoken to the user.
3. **Captions + a transcript** and a **non-avatar fallback** (an accessible HTML/audio path) that
   carry the same approved content.
4. **Locale handling** so the right voice/language is used per cohort.

The renderer is [`accelerator/mock_renderer.py`](../accelerator/mock_renderer.py): a deterministic,
offline stand-in that validates the approved pack and emits a traceable artifact **without calling a
paid service or embedding any real likeness**. It is how you rehearse the pipeline safely; the real
Speech call is the same shape.

## Choose your path

The capability you chose in module 1 decides how you render. All four carry the **same** disclosure +
accessibility obligations.

| Option | How you generate | Output | Latency | Best when |
| --- | --- | --- | --- | --- |
| **A. Batch avatar synthesis** *(default)* | REST job: submit SSML → poll → download mp4 | Reviewable video file | Async (seconds–minutes) | Pre-produced onboarding you approve once and replay |
| B. Real-time avatar | Speech SDK + WebRTC stream | Live avatar in the browser | Sub-second | An interactive kiosk/agent showing a face |
| C. Voice Live (avatar or audio) | Managed speech-to-speech WebSocket | Live spoken (optionally avatar) agent | Sub-second | A conversational onboarding assistant |
| D. Plain audio | TTS narration | Audio + transcript | Either | Accessibility-first / lowest risk — **and the mandatory fallback for A–C** |

**Default: Option A.** It produces a concrete artifact that flows through module 6's approval gate,
uses a standard avatar/voice (no talent gating), and is the cheapest governed path. Every option must
still ship the Option D fallback.

**Migration cost.** A → B/C is the batch→streaming rebuild from module 1 (WebRTC/TURN or Voice Live
client). Any → D is trivial. Do not skip D "for now" — it is the accessible path, not an extra.

## Implementation

### Option A — Batch avatar synthesis (default)

**Render locally first (safe, deterministic, keyless-free).** This validates approval + accessibility
and builds the exact request body — no Azure call, no likeness:

```bash
python3 scenarios/avatar-onboarding/accelerator/mock_renderer.py \
  --data-dir scenarios/avatar-onboarding/accelerator/sample-data \
  --output-dir scenarios/avatar-onboarding/accelerator/generated-artifacts
```

The renderer **rejects** the pack unless every script segment's spoken text is an exact approved
claim, all required approvals are present, and the disclosure appears in both the transcript and the
HTML fallback. That is the accessibility + grounding gate in code.

**Submit the real batch job (verified API).** The approved artifact becomes an SSML batch request:

```
PUT https://{resource}.cognitiveservices.azure.com/avatar/batchsyntheses/{SynthesisId}?api-version=2024-08-01
```

```json
{
  "inputKind": "SSML",
  "inputs": [{ "content": "<speak version='1.0' xml:lang='en-US'><voice name='en-US-AvaMultilingualNeural'>Complete your benefits selection in the employee portal during your first week.</voice></speak>" }],
  "avatarConfig": {
    "talkingAvatarCharacter": "lisa",
    "talkingAvatarStyle": "casual-sitting",
    "videoFormat": "Mp4",
    "subtitleType": "soft_embedded"
  }
}
```

Poll `GET …/batchsyntheses/{id}` until `status` is `Succeeded`, then download `outputs.result`
(the mp4). Keyless: send `Authorization: Bearer <entra-token>` (works because module 2 set the custom
subdomain). Limits: payload ≤ 500 KB, ≤ 200 concurrent jobs, ≤ 20-minute output.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/batch-synthesis-avatar>

`subtitleType: soft_embedded` gives you captions in the video; you still ship the standalone
transcript and HTML fallback for the accessible path.

### Option B — Real-time avatar

Use the Speech SDK to open a WebRTC session: fetch ICE details from the Speech REST API, create the
peer connection, then `new SpeechSDK.AvatarConfig("lisa", "casual-sitting")` and a voice such as
`en-US-Ava:DragonHDLatestNeural`. Requires **Standard S0** and outbound access to
`relay.communication.microsoft.com` (UDP 3478 / TCP 443). Show the disclosure in the UI before the
avatar speaks, render live captions, and keep the Option D fallback one click away.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/real-time-synthesis-avatar>

### Option C — Voice Live (avatar or audio)

Voice Live is the managed speech-to-speech path and can emit avatar visuals. Bind it to the module-4
agent (agent mode, Entra auth) so spoken answers stay grounded. This is exactly the
[Voice Live activity](../../../activities/extra-voice-live/README.md) — build it there. Disclose the
synthetic voice at session start (spoken and on-screen) and offer the transcript/fallback.
<https://learn.microsoft.com/azure/ai-services/speech-service/voice-live>

### Option D — Plain audio (and the mandatory fallback)

Synthesize the approved claims as narration with a standard neural voice, ship the transcript, and
serve the `accessible-fallback.html` page (semantic HTML, `lang` set, `<main>` landmark) that carries
the same content without an avatar. This is what a screen-reader user, a low-bandwidth user, or
anyone who opts out of the avatar receives. The sample fallback is
[`accessible-fallback.html`](../accelerator/sample-data/accessible-fallback.html).

### Disclosure & accessibility are non-negotiable (verified)

- **Disclose the synthetic nature** of the voice/avatar to users — required for standard *and*
  custom. Design guidance:
  <https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines>
- **Never** render a real person's face or voice in this repo or a demo. Custom likeness requires the
  limited-access + consent path from module 1.
- Ship captions, a transcript, and a non-avatar fallback for every option — the renderer enforces
  their presence.

## Verify

```bash
python3 scenarios/avatar-onboarding/accelerator/scripts/verify_experience.py
```

Expected:

```
== Module 5 checkpoint: accessible experience generation ==
PASS  approved pack accepted by the renderer
PASS  experience carries a synthetic-media disclosure
PASS  captions enabled
PASS  transcript attached
PASS  non-avatar fallback attached
...
✅ Module 5 checkpoint PASS — accessible experience rendered from an approved revision
```

Offline (default) it validates the pack, renders the artifact, asserts disclosure + captions +
transcript + fallback, and prints the exact batch-synthesis request the approved script produces.
Add `--submit` to send that request to the real Speech avatar API and poll for the mp4. A pack
missing the disclosure or the fallback **fails**.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Renderer rejects the pack | A segment's spoken text isn't an exact approved claim, or an approval/disclosure is missing | Fix the script to use exact claims; complete approvals (module 6) |
| `401` submitting the batch job | No custom subdomain / wrong role | Module 2 sets the subdomain; assign **Cognitive Services Speech User** |
| `400 unsupported voice/locale` | Voice not available for the input language | Pick a voice that supports the locale; verify in language-and-voice support |
| Custom avatar/voice rejected | Limited access not approved | File <https://aka.ms/customneural>; ship a **standard** avatar until approved |
| Real-time avatar won't stream | WebRTC/TURN egress blocked | Allow `relay.communication.microsoft.com` UDP 3478 / TCP 443 |
| Job exceeds limits | > 20 min output or > 500 KB payload | Split into segments; keep each job within limits |
| Captions present but no transcript | Relied on embedded subtitles only | Ship the standalone transcript + HTML fallback too |

## Decision record

Keep: chosen generation option and why; the avatar character/style and voice (confirm **standard**,
not custom, unless the limited-access path is approved); the disclosure wording and where it appears
(spoken + on-screen + transcript + fallback); the accessibility artifacts shipped; and the locales
covered. Note the artifact id and its trace hash so module 6 can approve *this exact* revision.

## Next module

[Module 6 — Gate publication behind human approval](06-approval-gating.md) requires named human
sign-off and a withdrawal path before anything reaches an employee.
