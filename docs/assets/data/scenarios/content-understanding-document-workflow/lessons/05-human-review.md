# Module 5 — Build review, correction, and handoff

Module 4 raises exceptions; this module resolves them. A reviewer sees missing and low-confidence
fields, corrects them, and approves the result. Retain every correction as evidence. Never silently
overwrite extraction, and send corrections to module 6's evaluation.

![Human review handoff](../diagrams/05-human-review-handoff.png)

## What you build

1. A review queue that routes exceptions to a named reviewer with the document, extracted fields, and
   grounding evidence.
2. A correction record that keeps the field, original value, corrected value, and reason.
3. A governed handoff where approved results cross one seam to the downstream system as the workflow
   identity, with an auditable trace. Reference:
   [`accelerator/sample-data/workflow/approval-trace.json`](../accelerator/sample-data/workflow/approval-trace.json).

## Choose your path

| Option | Reviewer surface | Handoff mechanism | Build effort | Best when |
| --- | --- | --- | --- | --- |
| **A. Action tool handoff** *(default)* | Any queue/app that reads the result | Agent calls an approved action tool (API/MCP) to post the result | Low–medium | You are building on the Foundry agent stack |
| B. Human-in-the-loop review app | Purpose-built correction UI over the result | App writes back the approved result | Medium–high | Reviewers need a rich correction experience |
| C. Multi-agent workflow handoff | Upstream agent hands the case to a reviewer/approver agent | Workflow transition with state | Medium | You already run a multi-agent workflow |

**Default: Option A.** The correction UI can be simple. The **handoff seam** must be correct: one
approved action tool posts an approved result as the workflow identity and records a trace. Action
tools are the canonical kit pattern, so they provide auth, schema, and observability without a custom
integration.

**Choose B** when reviewers need a rich correction experience (side-by-side document and fields,
bounding-box overlays). The handoff still uses the approved seam. **Choose C** when this workflow is
already an agent in a multi-agent system and needs an explicit approver-agent handoff.

**Migration cost.** Moving from A to B adds a UI before the same seam. Moving from A or B to C changes
orchestration but retains the result contract and correction record. Keep the handoff seam stable so
the rest can change.

## Implementation

### Option A — Action tool handoff (default)

Route exceptions to a queue, let a reviewer correct them, then post the approved result through one
action tool. Record the correction **before** handoff and never mutate the original result:

```python
def apply_correction(result, field, corrected_value, reviewer_id, reason):
    original = result["fields"][field]["value"]
    correction = {"field": field, "original_value": original,
                  "corrected_value": corrected_value, "reason": reason}
    # New reviewed copy — the original extraction is retained as evidence.
    reviewed = {**result, "fields": {**result["fields"],
                field: {**result["fields"][field], "value": corrected_value, "corrected": True}}}
    trace = {"document_id": result["document_id"], "reviewer_id": reviewer_id,
             "reviewed_at": _utcnow(), "review_outcome": "approved_with_correction",
             "corrections": [correction],
             "handoff": {"target_seam": "procurement_posting_action_tool", "approved": True}}
    return reviewed, trace
```

Then hand off through the approved tool as the workflow identity, using keyless access. Build and
register the tool in the canonical [Action Tools activity](../../../activities/advanced-action-tools/README.md).
The agent calls one posting tool and cannot write elsewhere.

### Option B — Human-in-the-loop review app

Give reviewers the document with grounding overlays and editable flagged fields. On approval, the app
writes the same correction record and calls the same handoff seam. The app captures reviewer identity,
timestamp, before-and-after values, and reason, so its trace matches Option A. Only the reviewer
experience changes.

### Option C — Multi-agent workflow handoff

If this workflow is one agent among several, use an explicit handoff. The extraction agent transfers
the typed result and correction record to an approver agent, which owns correction and approval.
Approval still ends in the action-tool seam. This is the pattern the
[Deploy as a Hosted Agent activity](../../../activities/advanced-deploy-hosted-agent/README.md) builds
on when the workflow ships.

## Verify

Check the trace written by your review step, then check who may trigger the handoff. Write the
approval trace to `trace.json` and inspect it.

**1. The correction is retained, not an overwrite.**

```bash
jq 'select(.review_outcome == "approved_with_correction")
    | {reviewer: .reviewer_id, at: .reviewed_at,
       corrections: [.corrections[] | {field, original_value, corrected_value, reason}],
       seam: .handoff.target_seam, approved: .handoff.approved}' trace.json
```

Every correction needs a `reviewer_id`, `reviewed_at`, `reason`, and `original_value` that differs
from `corrected_value`. If `original_value` is absent or unchanged, the review overwrote extraction
and lost before-and-after evidence. Module 6 uses these records as test cases, so a silent overwrite
also corrupts the evaluation set.

**2. The handoff refuses a caller who is not an approver.**

Call the approved action-tool seam as an identity that lacks the approver role:

```bash
TOKEN=$(az account get-access-token --resource "$ACTION_API_URL" --query accessToken -o tsv)
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: ******" \
  -X POST "$ACTION_API_URL/post-approved-result" -d @trace.json -H "Content-Type: application/json"
```

A non-approver identity must get `401` or `403`. A `200` means anyone who reaches the seam can post
an approved result downstream. Grant the approver role only to reviewer identities. Do not widen the
seam to pass a test.

**3. The post is attributed to the workflow identity.**

In the downstream system (or Application Insights traces), confirm the approved result arrived once
with the workflow identity and `document_id`, rather than the reviewer's personal account. A shared
app identity for every case prevents you from identifying the approver.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Correction overwrote the original result | Mutated the extraction in place | Keep the original; write a separate correction record and a reviewed copy |
| Handoff posts as the app for everyone | Service identity used instead of the workflow identity with a scoped tool | Post through one approved action tool; scope its permissions |
| Approval has no reviewer identity | Trace built without the signed-in reviewer | Require reviewer id + timestamp before the handoff is allowed |
| Reviewer approves without seeing evidence | Queue shows values but not grounding | Surface the grounding span/region beside each flagged field |
| Corrections never reach evaluation | Records discarded after handoff | Persist correction records; module 6 reads them as evaluation evidence |
| Anyone can trigger the handoff | Seam not access-controlled | Restrict the action tool to approver identities |

## Decision record

Record the reviewer surface, single handoff seam and permitted callers, correction-record location and
retention, and denial and return path. Use one dated paragraph.

## Next module

[Module 6 — Evaluate and trace the workflow](06-prove-and-observe.md) turns the corrections you just
retained into an evaluation gate and reviewable traces.
