# Solution · Extra · Visual Multimodal

This is a reference pattern, not a substitute for the current API documentation. Before coding,
use `microsoft-docs` MCP to verify the installed SDK's exact signatures and use `foundry-mcp` to
verify model/region capability. Do not invent or rely on preview Foundry multimodal SDK calls.

## Known Image Analysis Python pattern

The repository's Vision skill documents this stable pattern:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

credential = DefaultAzureCredential()
client = ImageAnalysisClient(endpoint=endpoint, credential=credential)

# Local, approved image bytes:
result = client.analyze(
    image_data=image_bytes,
    visual_features=[VisualFeatures.READ, VisualFeatures.CAPTION],
)

# Or, for a pre-approved URL:
# result = client.analyze_from_url(
#     image_url=approved_image_url,
#     visual_features=[VisualFeatures.READ],
# )
```

Use the current Docs result model to extract visible text and captions. Request only the features
needed for the chosen task: `READ` for a directional sign, `CAPTION` for a concise scene
description, and `TAGS` only if tags materially help. Confirm regional availability first, especially
for caption features. Do not request people/face-related features for the sample organization demo.

For multimodal reasoning beyond those features, select a currently supported Foundry multimodal
deployment and follow the exact message/image and structured-output syntax returned by
`microsoft-docs` MCP. Keep the same input, confidence, and human-review boundaries below.

## Reference workflow

1. **Intake:** allow only a local approved PNG/JPEG/WebP (or explicitly allowlisted HTTPS URL);
   check extension/content type and a small size limit before reading or transmitting it. Reject
   images with personal or sensitive content. Do not write image bytes to logs.
2. **Authenticate:** set `AZURE_VISION_ENDPOINT` outside source control, use
   `DefaultAzureCredential`, and run `az login` during local development. Grant RBAC rather than
   supplying a key.
3. **Analyze:** use `analyze(image_data=image_bytes)` for local bytes or
   `analyze_from_url(image_url=...)` for an approved URL. Catch invalid-image, auth, and service
   errors. Preserve an “analysis unavailable” outcome instead of fabricating an observation.
4. **Normalize:** convert the service response into a deliberately small result object. Do not
   expose raw response blobs by default.
5. **Review:** flag low-confidence/missing text and every accessibility-impacting interpretation
   for human review. A model can observe a ramp-like feature; it cannot certify accessibility or
   recommend a safe route.

An example result shape:

```python
from dataclasses import dataclass

@dataclass
class WayfindingObservation:
    summary: str
    visible_sign_text: list[str]
    observed_route_cues: list[str]
    confidence: float | None
    uncertainty_or_limitations: list[str]
    review_required: bool
    request_id: str
```

Set `review_required` when confidence is below your documented threshold, input quality is poor,
text cannot be read, results conflict, or a user asks for an accessibility/safety decision. Make
the limitation visible in the returned object, not merely in a log message.

## Evidence and evaluation

Use only approved staged/synthetic campus images. Build a small evaluation table containing expected
visible text, expected observable cues, expected uncertainty, and whether human review must occur.
Trace a request ID, model/deployment or selected visual features, output confidence, review flag,
and outcome. Do not trace raw image data or personal content. Review traces for feature minimization,
correct escalation, failed calls, and any unsupported inference.

## Offline check

`validate.py` never imports Azure packages, reads credentials, invokes Azure, or verifies a model
response. It only performs conservative AST/text checks on `visual_multimodal.py`. Passing it proves
that the expected safety and implementation signals are present; it does **not** prove RBAC,
current SDK compatibility, image safety, accuracy, or accessibility compliance.
