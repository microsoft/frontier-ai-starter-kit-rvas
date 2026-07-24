# Module 4 — Implement typed extraction with evidence

A demo that prints fields is not a workflow. This module turns whichever capability you chose in
module 3 into **one validated result contract**: every value carries a confidence and grounding
evidence, low-confidence and missing fields route to review, and the model never invents a value.

## What you build

A normalizer that maps your capability's raw output into the typed result contract and enforces four
invariants, plus a checkpoint that rejects a result violating any of them. The reference result is
[`accelerator/sample-data/workflow/typed-result.json`](../accelerator/sample-data/workflow/typed-result.json);
the deliberately broken one is
[`typed-result-invalid.json`](../accelerator/sample-data/workflow/typed-result-invalid.json).

The four invariants:

1. Every field with a value has a `confidence` and non-empty grounding `evidence` — **a value without
   evidence is an inferred value and is rejected**.
2. Any field below the confidence threshold is flagged `low_confidence:<field>` and forces review.
3. A missing/uncertain field is surfaced for review, never guessed.
4. `requires_human_review` and `routing_decision` agree with the flags.

## Choose your path

| Option | Source of confidence + evidence | Normalizer effort | Best when |
| --- | --- | --- | --- |
| **A. Map a Content Understanding result** *(default)* | `confidence` + `source`/`spans` per field | Low — evidence is already there | You chose CU prebuilt or custom (module 3 A/B/F) |
| B. Map a Document Intelligence result | `field.confidence` + `bounding_regions` | Low | You chose a DI prebuilt or custom model (module 3 C/D) |
| C. LLM output + self-reported grounding | You require a span per field and verify it | High — you build evidence + validation | You chose LLM structured outputs (module 3 E) |

**Default: Option A.** Content Understanding already returns confidence and a grounding source per
field, so the normalizer is a thin mapping and the invariants are cheap to enforce.

**Choose B** when you standardized on Document Intelligence models — the shape differs but the evidence
is equally present. **Choose C** only if you accepted the build-your-own trade in module 3; you are now
paying for it by implementing evidence and validation yourself.

**Migration cost.** A ↔ B is a mapping change only — the contract and every downstream module are
identical. A/B → C adds a validation layer you must test as carefully as the extraction itself.

## Implementation

### Option A — Map a Content Understanding result

```python
def to_contract(document_id, cu_fields, threshold):
    fields, review_reasons = {}, []
    for name, raw in cu_fields.items():
        value = raw.get("valueString") or raw.get("valueNumber") or raw.get("valueDate")
        confidence = raw.get("confidence")
        spans = raw.get("spans") or []
        if value is None:
            review_reasons.append(f"missing_field:{name}")
            continue
        if not spans or raw.get("source") is None:          # invariant 1: no inferred values
            review_reasons.append(f"no_evidence:{name}")
        if confidence is not None and confidence < threshold:  # invariant 2
            review_reasons.append(f"low_confidence:{name}")
        fields[name] = {"value": value, "confidence": confidence,
                        "evidence": {"page": _page(raw.get("source")), "spans": spans}}
    requires_review = bool(review_reasons)                    # invariants 3 + 4
    return {"document_id": document_id, "confidence_threshold": threshold,
            "fields": fields, "review_reasons": review_reasons,
            "requires_human_review": requires_review,
            "routing_decision": "route_human_review" if requires_review else "auto_post"}
```

### Option B — Map a Document Intelligence result

Same contract, different source shape — `field.confidence` and `field.bounding_regions`:

```python
def di_to_contract(document_id, di_document, threshold):
    fields, review_reasons = {}, []
    for name, field in di_document.fields.items():
        value = field.get("content")
        confidence = field.get("confidence")
        regions = field.get("boundingRegions") or []
        if value is None:
            review_reasons.append(f"missing_field:{name}"); continue
        if not regions:
            review_reasons.append(f"no_evidence:{name}")
        if confidence is not None and confidence < threshold:
            review_reasons.append(f"low_confidence:{name}")
        page = regions[0]["pageNumber"] if regions else None
        fields[name] = {"value": value, "confidence": confidence,
                        "evidence": {"page": page, "spans": [{"polygon": r["polygon"]} for r in regions]}}
    requires_review = bool(review_reasons)
    return {"document_id": document_id, "confidence_threshold": threshold, "fields": fields,
            "review_reasons": review_reasons, "requires_human_review": requires_review,
            "routing_decision": "route_human_review" if requires_review else "auto_post"}
```

### Option C — LLM output + self-reported grounding

There is no confidence score, so you *manufacture* evidence and validate it. Require the model to
return, for each field, the exact source substring; then confirm that substring exists in the
document and reject any field it cannot locate:

```python
def validate_llm_field(name, value, quoted_span, document_text, review_reasons):
    if value is None:
        review_reasons.append(f"missing_field:{name}"); return None
    offset = document_text.find(quoted_span or "")
    if not quoted_span or offset < 0:            # invariant 1: reject unlocatable = inferred
        review_reasons.append(f"no_evidence:{name}")
        return {"value": value, "confidence": None, "evidence": {"page": 1, "spans": []}}
    return {"value": value, "confidence": None,
            "evidence": {"page": 1, "spans": [{"offset": offset, "length": len(quoted_span)}]}}
```

Any field that reaches `spans: []` fails the checkpoint — which is the point: without grounding you
cannot claim the value came from the document.

Modules 3 and 4 are the canonical
[Document Workflow activity](../../../activities/extra-document-workflow/README.md).

## Verify

```bash
# Passing result
python3 scenarios/content-understanding/accelerator/scripts/verify_typed_extraction.py --offline

# Fail path — inferred value + unflagged low confidence
python3 scenarios/content-understanding/accelerator/scripts/verify_typed_extraction.py \
  --offline --result scenarios/content-understanding/accelerator/sample-data/workflow/typed-result-invalid.json
```

Expected (passing):

```
✅ Module 4 checkpoint PASS — extraction is typed, evidence-backed, and fails safely
```

The fail path prints exactly why it is unsafe — a field with a value but empty evidence, a
low-confidence field not flagged, and a routing decision that would auto-post it.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Checkpoint fails on `no_evidence` | Mapped a value but dropped its span/region | Carry `spans`/`bounding_regions`; for LLM, require and verify a source span |
| Everything routes to review | Threshold too high for this document class | Recalibrate the threshold per class; measure it in module 6, don't guess |
| Low-confidence field auto-posts | Gate not applied, or `requires_human_review` hard-coded | Derive `requires_human_review` from `review_reasons`, never set it manually |
| CU `source` is a polygon, not a page | Grounding is a region string `D(page, …)` | Parse the leading page index; keep the polygon as the span payload |
| DI field has no `boundingRegions` | Field was inferred from key-value pairing, not located | Treat as `no_evidence` and route to review |
| Missing field silently omitted | Normalizer skipped `None` values without flagging | Emit `missing_field:<name>` so the reviewer sees the gap |

## Decision record

Short: the confidence threshold per document class and how it was set, the evidence representation
(spans vs polygons vs verified quote), and the routing rule. One paragraph, with a date.

## Next module

[Module 5 — Build review, correction, and handoff](05-human-review.md) routes the exceptions this
module raised to a named reviewer and captures the outcome.
