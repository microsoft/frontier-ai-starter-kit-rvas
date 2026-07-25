
# Facilitator Guide · Extra — Visual Multimodal

> **Command context:** Run all commands from the repository root.

> **Facilitator-only.** This is a bounded visual-observation exercise, not a route-planning,
> accessibility-certification, identity, or surveillance exercise.

## Prerequisites

1. A provisioned Vision/Foundry resource in a region that supports the selected capability, plus
   keyless RBAC for learners. Local users need `az login`; do not distribute service keys.
2. A current documentation check through `microsoft-docs` MCP before coding. Image Analysis and
   Foundry multimodal signatures change; have teams confirm current client, image input, and
   structured-output APIs rather than copying a preview call.
3. One approved generic sample organization campus wayfinding/accessibility image per team, or a shared
   staged/openly licensed image. The room should know the approved retention and trace policy.

## Safe image rules

Allow only an empty/staged campus exterior or similarly generic image with a path, entrance, and
directional sign. Do not use people, faces, badges, screens, classrooms, medical aids, private
areas, student work, vehicles with readable plates, or images from personal devices. Do not ask a
model to identify a person, infer a disability, assess safety, or certify ADA/accessibility
compliance. The appropriate demo question is: “What sign text and route cues are visibly
observable?” not “Is this path accessible?”

## Expected artifacts

- `visual_multimodal.py` in the activity directory (learner-authored), with safe intake,
  `DefaultAzureCredential`, minimum image features or an approved current multimodal call, and
  bounded failure handling.
- A typed/schema result containing a summary, visible sign text, observed route cues, confidence,
  limitations/uncertainty, and `review_required`.
- A short evidence record or trace view showing selected model/features, an opaque request ID,
  confidence, and human-review decision—without raw image content.
- A tiny approved evaluation set including at least one unreadable/ambiguous-sign case that
  escalates to a human.

Run the local checkpoint:

```bash
python activities/extra-visual-multimodal/validate.py --all
```

## Facilitation cues

- Press teams to select the **minimum** features: normally `READ`, optionally `CAPTION` or `TAGS`.
  Confirm regional availability for every selected feature, especially captions.
  More features cost more and enlarge the data footprint; people/face features have no role here.
- If a team uses a Foundry multimodal model, ask them to show the current Docs/MCP result for the
  exact image-message and structured-output signature. Do not approve invented SDK code.
- Require an uncertainty outcome. Low-confidence OCR, poor image quality, contradictory cues, or
  a request that could influence a route/accommodation must set the review flag rather than guess.
- Trace metadata, not images. Make clear that a model observation is input to a human process, not
  a compliance decision.

## Common issues

| Symptom | Likely cause | Facilitator response |
| --- | --- | --- |
| `DefaultAzureCredential` cannot authenticate | learner has not run `az login`, or RBAC is missing | verify identity and resource role before changing code |
| SDK call does not match | copied a stale sample or preview signature | return to `microsoft-docs` MCP and verify the installed version |
| Output invents a route conclusion | prompt/schema lacks a boundary | require visible observations, limitations, and `review_required` |
| Trace contains image content | logging was too broad | remove raw image/request-body capture; retain only approved metadata |
| OCR cannot read the sign | image is low quality or sign is ambiguous | return uncertainty and human review; do not retry with a guess |

## Static validation limitation

`validate.py` is intentionally offline: it uses AST/text heuristics, imports no Azure SDK, reads no
credentials, and makes no Azure calls. Passing proves only that the learner artifact visibly
contains expected implementation and safety signals. It cannot prove current SDK compatibility,
RBAC, model availability, image-policy compliance, visual accuracy, trace configuration, or real
human review. Confirm those through a supervised safe demo and evidence review.
