# Module 5 — Generate the accessible avatar experience

Render the experience only from an **approved script revision**. It must include the accessibility
and disclosure guarantees a synthetic presenter legally and ethically requires. An avatar without a
transcript, captions, disclosure, or non-avatar path is a compliance incident.

Current Speech guidance is cited inline where the implementation depends on service behavior.

![Accessible experience generation](../diagrams/05-accessible-generation.png)

## What you build

1. The rendered experience, a talking-avatar video, real-time stream, Voice Live session, or plain
   audio, produced from the approved artifact.
2. **Disclosure** that the presenter is synthetic/AI-assisted, shown/spoken to the user.
3. **Captions + a transcript** and a **non-avatar fallback** (an accessible HTML/audio path) that
   carry the same approved content.
4. **Locale handling** so the right voice/language is used per cohort.

The pack contract, [`accelerator/content_pack.py`](../accelerator/content_pack.py), is a
deterministic, offline module. It validates the approved pack and builds a traceable artifact record
**without calling a paid service or embedding a real likeness**. Use it to rehearse the pipeline
safely. Its artifact record is **not** a Speech request body; a rendering adapter must map it
to the service request.

## Choose your path

The module-1 capability determines how you render. All four have the **same** disclosure and
accessibility obligations.

| Option | How you generate | Output | Latency | Best when |
| --- | --- | --- | --- | --- |
| **A. Batch avatar synthesis** *(default)* | REST job: submit SSML → poll → download mp4 | Reviewable video file | Async (seconds–minutes) | Pre-produced onboarding you approve once and replay |
| B. Real-time avatar | Speech SDK + WebRTC stream | Live avatar in the browser | Sub-second | An interactive kiosk/agent showing a face |
| C. Voice Live (avatar or audio) | Managed speech-to-speech WebSocket | Live spoken (optionally avatar) agent | Sub-second | A conversational onboarding assistant |
| D. Plain audio | TTS narration | Audio + transcript | Either | An audio-first experience, alongside the required text fallback |

**Default: Option A.** It produces an artifact that passes through module 6's approval gate, uses a
standard avatar/voice (no talent gate), and can be reviewed before release. Every option must ship
an equivalent accessible text fallback; audio narration is optional.

**Migration cost.** A → B/C is the module-1 batch-to-streaming rebuild (WebRTC/TURN or Voice Live
client). Keep the text fallback available regardless of the media option.

## Implementation

### Option A — Batch avatar synthesis (default)

**Build the request from an approved pack, never free text.** The pack contract in
[`content_pack.py`](../accelerator/content_pack.py) rejects the pack unless every script segment's
spoken text is an exact approved claim, all required approvals are present, and the disclosure
appears in both the transcript and the HTML fallback. Use it to turn the approved artifact into the
artifact record, with no Azure call and no likeness. The sample approvals are fictional; complete
module 6's review before generating media for a real pilot:

```bash
python3 -c "import sys; from pathlib import Path; \
sys.path.insert(0, 'scenarios/avatar-onboarding/accelerator'); \
from content_pack import validate_pack, build_artifact; \
pack = validate_pack(Path('scenarios/avatar-onboarding/accelerator/sample-data')); \
print(build_artifact(pack))"
```

A pack whose spoken text is not an exact approved claim raises `PackRejectedError`. This is the
accessibility and grounding gate in code, before any Azure call.

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
(the mp4). For keyless access, send an Entra bearer token in the `Authorization` header and redact
it in logs and docs. This works only when module 2 set the custom subdomain. Limits are payload ≤
500 KB, ≤ 200 concurrent jobs, and ≤ 20-minute output.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/batch-synthesis-avatar>

`subtitleType: soft_embedded` adds captions to the video. Still ship the standalone transcript and
HTML fallback.

### Option B — Real-time avatar

Use the Speech SDK to open a WebRTC session: fetch ICE details from the Speech REST API, create the
peer connection, then `new SpeechSDK.AvatarConfig("lisa", "casual-sitting")` and a voice such as
`en-US-Ava:DragonHDLatestNeural`. Requires **Standard S0** and outbound access to
`relay.communication.microsoft.com` (UDP 3478 / TCP 443). Show the disclosure in the UI before the
avatar speaks, render live captions, and keep the Option D fallback one click away.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/real-time-synthesis-avatar>

### Option C — Voice Live (avatar or audio)

Voice Live is the managed speech-to-speech path and can emit avatar visuals. Bind it to the module-4
agent (agent mode, Entra auth) so spoken answers stay grounded. Build it in the
[Voice Live activity](../../../activities/extra-voice-live/README.md). Disclose the synthetic voice
at session start, both spoken and on-screen, and offer the transcript/fallback.
<https://learn.microsoft.com/azure/ai-services/speech-service/voice-live>

### Option D — Plain audio and the text fallback

Synthesize the approved claims as narration with a standard neural voice, ship the transcript, and
serve `accessible-fallback.html` (semantic HTML, `lang` set, `<main>` landmark) with the same
content and no avatar. Screen-reader users, low-bandwidth users, and anyone who opts out of the
avatar receive this path. The sample fallback is
[`accessible-fallback.html`](../accelerator/sample-data/accessible-fallback.html).

### Disclosure & accessibility are non-negotiable (verified)

- **Disclose the synthetic nature** of the voice/avatar to users — required for standard *and*
  custom. Design guidance:
  <https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines>
- **Never** render a real person's face or voice in this repo or a demo. Custom likeness requires the
  limited-access + consent path from module 1.
- Ship captions where applicable, a transcript, and a non-avatar fallback. The local validator
  checks text files and a captions flag; it does not inspect generated captions or media.

## Verify

Render one approved segment, then confirm the experience includes the disclosure and accessibility
artifacts a synthetic presenter requires.

**1. Submit a batch synthesis job with your Entra token and watch the result.** This proves keyless
Speech and gives you an artifact to inspect. Submit one approved claim as SSML:

```bash
set -a; source scenarios/avatar-onboarding/accelerator/.env; set +a
TOKEN=$(az account get-access-token --scope https://cognitiveservices.azure.com/.default --query accessToken -o tsv)
JOB=onb-verify-001

curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$AZURE_SPEECH_ENDPOINT/avatar/batchsyntheses/$JOB?api-version=2024-08-01" \
  -d '{
    "inputKind": "SSML",
    "inputs": [{"content": "<speak version=\"1.0\" xml:lang=\"en-US\"><voice name=\"en-US-AvaMultilingualNeural\">Complete your benefits selection in the employee portal during your first week.</voice></speak>"}],
    "avatarConfig": {"talkingAvatarCharacter": "lisa", "talkingAvatarStyle": "casual-sitting", "videoFormat": "Mp4", "subtitleType": "soft_embedded"}
  }' | jq '{id, status}'

# Poll until Succeeded, then read the output URL:
curl -s -H "Authorization: Bearer $TOKEN" \
  "$AZURE_SPEECH_ENDPOINT/avatar/batchsyntheses/$JOB?api-version=2024-08-01" | jq -r '.status, .outputs.result'
```

`status` moves `NotStarted → Running → Succeeded`. Download `outputs.result` (a time-limited SAS
URL) and play the mp4. Expect the standard `lisa` avatar to speak the exact approved wording with
soft-embedded captions. For `401`, check the token and custom-subdomain endpoint (module 2).
For `403`, check **Cognitive Services Speech User** and RBAC propagation. Use only the selected
standard avatar; a realistic-looking avatar alone does not mean you selected a custom likeness.
Custom likenesses need module 1's approval and consent checks.
<https://learn.microsoft.com/azure/ai-services/speech-service/text-to-speech-avatar/batch-synthesis-avatar>

**2. The experience carries a disclosure, and the non-avatar fallback carries the same content.** A
video with no disclosure and no accessible path is a compliance incident, not a demo:

```bash
jq -e '.disclosure | length > 0' \
  scenarios/avatar-onboarding/accelerator/sample-data/storyboard-script.json

grep -qi 'avatar-generated or AI-assisted' scenarios/avatar-onboarding/accelerator/sample-data/transcript.txt \
  && grep -qi 'benefits selection' scenarios/avatar-onboarding/accelerator/sample-data/accessible-fallback.html \
  && grep -qi 'lang=' scenarios/avatar-onboarding/accelerator/sample-data/accessible-fallback.html \
  && echo "disclosure + fallback carry the approved content"
```

Both must succeed. A missing disclosure lets an undisclosed synthetic presenter reach users. A
fallback without the approved wording or a `lang` attribute excludes screen-reader and low-bandwidth
users. Ship captions, a transcript, and the non-avatar page for every option.
<https://learn.microsoft.com/azure/foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines>

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

## Next module

[Module 6 — Gate publication behind human approval](06-approval-gating.md) requires named human
sign-off and a withdrawal path before anything reaches an employee.
