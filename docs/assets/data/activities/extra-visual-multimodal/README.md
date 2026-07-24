# Extra · Visual Multimodal

> **Command context:** Run all commands from the repository root.

> Tier 2 · Extra — modular. Start after Foundations, or use the repository bootstrap path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.

Build a small, **human-reviewed** accessibility and wayfinding assistant for a generic Northfield
campus image. It can extract visible sign text and describe observable route cues; it must not
identify people, infer disability or other sensitive traits, or decide whether a route is safe or
accessible.

## Before coding: search current APIs

Vision and Foundry multimodal APIs move quickly. **Do not copy a remembered preview signature.**
Use `microsoft-docs` MCP before writing SDK code:

1. Search for the current Python Image Analysis client, `ImageAnalysisClient`, its Entra ID
   authentication requirements, and its `analyze`/`analyze_from_url` signatures.
2. Search Foundry model documentation if you choose a multimodal model instead of deterministic
   image features. Confirm deployment, image-message, and structured-output signatures there.
3. Use `foundry-mcp` to confirm that the selected model and region support the task. Record the
   documentation link/version you used in your demo notes.

This activity is **keyless-first**: use `DefaultAzureCredential`, `az login` locally, and an
appropriate Azure RBAC role on the Vision/Foundry resource. Do not put keys, connection strings,
or image URLs containing SAS tokens in source control.

## Demo boundary and safe input

Use only a generic, non-sensitive Northfield campus accessibility/wayfinding image: for example,
an empty exterior path leading to a building entrance, with a visible directional sign and no
recognizable people, vehicles, IDs, screens, or student work. A staged or openly licensed image is
fine. Do not upload photos of people, classrooms, medical aids, access badges, private spaces, or
real students.

Your `visual_multimodal.py` must:

- accept a local PNG/JPEG/WebP image (or a pre-approved HTTPS image URL), reject unsupported
  formats and oversized input before calling a service;
- keep images out of logs and traces; log an opaque request ID and non-sensitive metadata instead;
- state that output is a visual observation, not an accessibility certification, safety assessment,
  identity claim, or navigation instruction.

## Step 1 — Choose the task and model

Write the task as an observable question:

> “What directional text is visibly readable, and what route or entrance cues are observable in
> this generic Northfield campus image?”

Choose the smallest capability that answers it:

| Need | Suitable approach |
| --- | --- |
| Read a sign and produce a concise caption/tags | Image Analysis visual features |
| Compare image cues against a policy or explain uncertainty in context | A current, approved Foundry multimodal model |

For Image Analysis, request **only** the features required for the demo (normally `READ` and
optionally `CAPTION` or `TAGS`). Caption availability varies by region, so confirm the selected
resource supports every requested feature before building the demo. More features increase processing,
cost, and data exposure. Do not enable people/face analysis for this activity.

**Checkpoint:** Explain why your selected model/task needs only those features.

## Step 2 — Implement keyless image analysis

Create `visual_multimodal.py` beside this README. Use `DefaultAzureCredential` and an endpoint
from an environment variable such as `AZURE_VISION_ENDPOINT`; never hardcode credentials. Follow
the current signatures returned by Microsoft Docs/MCP.

At a minimum, implement:

1. `load_safe_image(...)` to validate type and byte size, then return bytes;
2. a client authenticated with `DefaultAzureCredential`;
3. an image call that uses the selected, minimum visual features;
4. exception handling for invalid input, authorization/service failures, and incomplete results.

Run the static checkpoint (it makes no Azure calls):

```bash
python activities/extra-visual-multimodal/validate.py --step 1
python activities/extra-visual-multimodal/validate.py --step 2
python activities/extra-visual-multimodal/validate.py --step 3
```

## Step 3 — Return a bounded, structured observation

Return a typed model, dataclass, `TypedDict`, or JSON Schema rather than an unbounded paragraph.
Include at least:

```text
summary
visible_sign_text
observed_route_cues
confidence
uncertainty_or_limitations
review_required
```

Use service confidence where it is available. If text is missing, low-confidence, contradictory,
or the image quality prevents a reliable observation, say so and set `review_required=True`.
Never fill gaps with a guess.

**Checkpoint:**

```bash
python activities/extra-visual-multimodal/validate.py --step 4
python activities/extra-visual-multimodal/validate.py --step 5
```

## Step 4 — Make the human boundary explicit

Escalate to a trained human/campus accessibility contact when the result could affect a person's
route choice or accommodation: an unclear curb cut, obstructed path, unreadable sign, entrance
availability, or a request to certify compliance. The tool may summarize what it can see; it
must not approve a route or make an accommodation decision.

Capture evidence safely:

- record the model/deployment or visual-feature configuration, timestamp, request ID, confidence,
  structured output, and review outcome;
- keep the original image out of traces and evaluation artifacts unless its approved retention
  policy explicitly permits it;
- evaluate only approved synthetic/staged campus images with expected sign text, route cues, and
  escalation cases; inspect traces to confirm the selected feature set and the review decision.

```bash
python activities/extra-visual-multimodal/validate.py --step 6
python activities/extra-visual-multimodal/validate.py --all
python activities/extra-visual-multimodal/validate.py --all --dry-run
```

## What you built

A keyless, bounded visual observation workflow for a safe Northfield wayfinding demo: safe image
intake → minimum-capability analysis → structured confidence-aware output → human review and
evaluation evidence. It is an assistive observation aid, not a replacement for campus accessibility
inspection or human judgment.

See [solution.md](https://github.com/microsoft/frontier-ai-starter-kit-rvas/blob/main/activities/extra-visual-multimodal/solution.md) for the known Image Analysis pattern and the limits of the
offline validator.
