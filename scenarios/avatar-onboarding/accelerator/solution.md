# Solution — Avatar Scenario reference implementation

This reference collects the scenario's infrastructure, local pack checks, and integration snippets.
It is not an end-to-end application. You still need a rendering/channel adapter, authenticated
approvals, expiry and withdrawal controls, and an evaluation harness. Run commands from the repository root.

> Fictional data only. The accelerator ships synthetic HR content. Never place real customer
> content, or a real person's voice or likeness, in this repository.

## Reference stack (the default path)

| Concern | Reference choice | Module |
| --- | --- | --- |
| Experience capability | **Speech text-to-speech avatar — batch synthesis**, standard avatar + standard neural voice (no limited-access gate) | 1 |
| Foundation | Azure AI Foundry (AIServices, `kind: AIServices`, custom subdomain) + project, chat + embedding deployments, AI Search, Storage, Log Analytics + App Insights | 2 |
| Content pipeline | Versioned claims in `sample-data/claims.json`, approved-content blob container, owner/version/expiry metadata | 3 |
| Grounded assistant | Model + approved claim set; optional Foundry agent; refuses with `NO_APPROVED_CLAIM` | 4 |
| Experience generation | Batch avatar synthesis from an approved script revision + disclosure, captions, transcript, non-avatar fallback | 5 |
| Approval gate | Versioned approval record enforced by `content_pack.py`; withdrawal on source change | 6 |
| Prove & operate | Foundry evaluations + AI Red Teaming Agent, GenAI tracing, aggregate-only telemetry, release scorecard | 7 |

## 0. Prerequisites

```bash
az login
az account set --subscription "<subscription-id>"
python3 -m pip install -r requirements.txt
```

## 1. Select the experience capability (Module 1)

The default, **standard batch avatar**, avoids the Azure limited-access registration that
*custom* avatar / *custom* neural voice requires. It still requires synthetic-media disclosure. See
`lessons/01-experience-selection.md` for the option comparison and responsible-AI gates.

## 2. Provision the foundation (Module 2)

```bash
scenarios/avatar-onboarding/accelerator/scripts/deploy.sh rg-avatar-onboarding westus2
set -a; source scenarios/avatar-onboarding/accelerator/.env; set +a

# Confirm the Speech endpoint answers your Entra identity
TOKEN=$(az account get-access-token --scope https://cognitiveservices.azure.com/.default --query accessToken -o tsv)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
  "$AZURE_SPEECH_ENDPOINT/avatar/batchsyntheses?api-version=2024-08-01"
```

`deploy.sh` deploys `accelerator/main.bicep` and writes a **keyless** `.env` contract from the
deployment outputs (plus the two tracing switches). Key outputs:

```
AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_FOUNDRY_ENDPOINT,
AZURE_AI_MODEL_DEPLOYMENT_NAME, AZURE_AI_EMBEDDING_DEPLOYMENT_NAME,
AZURE_SPEECH_ENDPOINT, AZURE_SPEECH_REGION, AZURE_SPEECH_RESOURCE_ID,
AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_CONNECTION_NAME,
AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_CONTAINER_NAME,
AZURE_EXPERIENCE_OUTPUT_CONTAINER_NAME, APPLICATIONINSIGHTS_RESOURCE_ID
```

Services use managed identities; local commands use the signed-in user. The template assigns that
user data-plane roles that generic Owner/Contributor do **not** grant, including **Cognitive Services Speech User**
(`f2dc8367-1007-4938-bd23-fe263f013447`) for keyless Speech, plus Cognitive Services User, OpenAI
User, Search index/service, and Storage Blob roles. Keyless Entra auth requires the custom subdomain
the template sets via `customSubDomainName`.

## 3. Build the governed content pipeline (Module 3)

Upload approved content and produce the versioned claim set:

```bash
# List what is actually in the approved-content container
az storage blob list --auth-mode login \
  --account-name "$AZURE_STORAGE_ACCOUNT_NAME" \
  --container-name "$AZURE_STORAGE_CONTAINER_NAME" \
  --query "[].name" -o tsv
```

Each claim carries `claim_id`, `source_reference`, and `owner`. The pack carries `version` and
`review_by`. The publishing adapter must reject expired or invalidated content and withdraw
affected publications. The local validator does not implement those controls.

## 4. Build the grounded assistant (Module 4)

Follow [Foundations Steps 3–4](../../../activities/foundations/README.md) to build the grounded,
citing agent. The onboarding contract is simple: on-claim asks return the **exact approved wording** and the
`claim_id`; off-claim asks return `NO_APPROVED_CLAIM` plus a human-help path. The assistant provides
interactive help; it must **not** silently add claims to a published script.

## 5. Generate the accessible experience (Module 5)

Render deterministically first (no service calls), then submit the live batch job.

Watch the batch synthesis job to completion, then download and watch the result. A successful job
can still produce the wrong script, omit disclosure, or use audio that does not match approved
claims.

Batch synthesis endpoint:

```
PUT  https://{resource}.cognitiveservices.azure.com/avatar/batchsyntheses/{id}?api-version=2024-08-01
GET  https://{resource}.cognitiveservices.azure.com/avatar/batchsyntheses/{id}?api-version=2024-08-01
```

Body carries `inputKind` (`PlainText`|`SSML`), `inputs[].content`, and
`avatarConfig.talkingAvatarCharacter`/`talkingAvatarStyle`. Poll `NotStarted → Running → Succeeded`;
`outputs.result` is the mp4 SAS URL. Limits: payload ≤500 KB, ≤200 concurrent jobs, ≤20 min output,
1920×1080 @ 25 fps. Every render emits: the synthetic-media **disclosure**, **captions**, a
**transcript**, and a **non-avatar fallback** (`accessible-fallback.html`). Authenticate with
`DefaultAzureCredential` (Entra token), never a key.

## 6. Gate publication behind human approval (Module 6)

Four named approvals bind to the exact `script_id`+`script_version`: `SME`, `legal-compliance`,
`brand-communications`, `content-owner` (the renderer's `REQUIRED_APPROVER_ROLES`). Withdrawal:

```python
import json, pathlib
p = pathlib.Path("scenarios/avatar-onboarding/accelerator/sample-data/approvals.json")
r = json.loads(p.read_text()); r["approval_status"] = "withdrawn"
p.write_text(json.dumps(r, indent=2))   # renderer now rejects the pack — publication paused
```

## 7. Evaluate, red-team, trace, operate (Module 7)

```bash
export AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true   # BEFORE importing the Foundry SDK
python  activities/advanced-evaluation-redteam/validate.py
```

Evaluate grounding, refusal, disclosure, and accessibility on a golden set. Run the AI Red Teaming
Agent and the synthetic-media probes (impersonation, "skip the disclosure", unapproved claims).
Review a trace for a failed case. Ship only when every gate is green. Measure
the pilot with **aggregate, identifier-free** telemetry only.

## End-to-end verification

```bash
# Deployable, secret-free infrastructure:
bicep build scenarios/avatar-onboarding/accelerator/main.bicep --outfile scenarios/avatar-onboarding/accelerator/.build/main.json
bicep lint  scenarios/avatar-onboarding/accelerator/main.bicep
```

Then watch the published artifact as a new joiner would. The disclosure appears before the persona
speaks, every spoken claim traces to an approved source, and the non-avatar alternative is reachable.

## Responsible-AI gates before production

- **Standard** avatar + **standard** neural voice: no registration, but synthetic-media **disclosure
  to users and a feedback channel are required**.
- **Custom** avatar / **custom** or **personal** voice: **Limited Access**, registration only via
  <https://aka.ms/customneural>, Microsoft-managed customers only; custom video avatar needs ≥10 min
  actor video, **explicit written consent**, and the "Disclosure for voice and avatar talent" shared
  in advance.
- Never impersonate a real person; keep disclosure mandatory in the system prompt; keep the Module 6
  withdrawal path one action away.

Sources: `/azure/ai-services/speech-service/text-to-speech-avatar/*`,
`/azure/foundry/responsible-ai/speech-service/text-to-speech/{limited-access,concepts-disclosure-guidelines,transparency-note,disclosure-voice-talent}`.
