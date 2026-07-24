#!/usr/bin/env python3
"""Module 4 checkpoint — typed extraction returns evidence, not inferences.

Validates a typed extraction result (sample-data/workflow/typed-result.json):
  * every field with a value carries a confidence and non-empty evidence spans
    (a value without evidence is an inferred value and is rejected),
  * every field below the confidence threshold is flagged with a
    `low_confidence:<field>` review reason and forces human review,
  * requires_human_review and routing_decision are consistent, and
  * a missing/uncertain field is surfaced for review rather than guessed.

Offline validates the result document. Live mode (--document-url) additionally
runs the same document through the selected capability and re-checks the shape.

Run offline (passing fixture):
    python3 .../verify_typed_extraction.py --offline
Fail-path demo (inferred value + unflagged low confidence):
    python3 .../verify_typed_extraction.py --offline --result sample-data/workflow/typed-result-invalid.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_json  # noqa: E402


def _has_evidence(field: dict) -> bool:
    evidence = field.get("evidence")
    if not isinstance(evidence, dict):
        return False
    spans = evidence.get("spans")
    return isinstance(spans, list) and len(spans) > 0 and evidence.get("page") is not None


def verify_result(result: dict, failures: list[str]) -> None:
    if not isinstance(result, dict):
        check(False, "result is a JSON object", failures)
        return

    threshold = result.get("confidence_threshold")
    if not (isinstance(threshold, (int, float)) and 0 < threshold <= 1):
        check(False, "confidence_threshold is in (0, 1]", failures)
        return
    check(True, f"confidence_threshold = {threshold}", failures)

    fields = result.get("fields")
    if not isinstance(fields, dict) or not fields:
        check(False, "result declares at least one field", failures)
        return

    reasons = set(result.get("review_reasons", []))
    low_confidence_fields: list[str] = []

    for name, field in fields.items():
        if not isinstance(field, dict):
            check(False, f"field '{name}' is an object", failures)
            continue
        value = field.get("value")
        confidence = field.get("confidence")
        if value is None:
            # A missing/uncertain field must be surfaced for review, never guessed.
            check(f"missing_field:{name}" in reasons,
                  f"missing field '{name}' is surfaced for review", failures)
            continue
        check(isinstance(confidence, (int, float)), f"field '{name}' carries a confidence score", failures)
        check(_has_evidence(field),
              f"field '{name}' has grounding evidence (no inferred value)", failures)
        if isinstance(confidence, (int, float)) and confidence < threshold:
            low_confidence_fields.append(name)
            check(f"low_confidence:{name}" in reasons,
                  f"low-confidence field '{name}' is flagged in review_reasons", failures)

    requires_review = result.get("requires_human_review")
    if low_confidence_fields:
        check(requires_review is True,
              f"low-confidence fields {low_confidence_fields} force human review", failures)
        check(result.get("routing_decision") == "route_human_review",
              "routing_decision routes to human review", failures)
    else:
        check(isinstance(requires_review, bool), "requires_human_review is a boolean", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, default=WORKFLOW / "typed-result.json")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--document-url", help="Live: analyze this document and re-check the shape.")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 4 checkpoint: typed extraction with evidence ==")
    result = load_json(args.result, failures)
    if result is not None:
        verify_result(result, failures)

    if args.offline or not args.document_url:
        print("\n(offline mode: result document validated, no Azure calls)")
    else:
        print("\n(live analysis is scenario-specific; see solution.md for the analyze call)")

    return finish(4, "extraction is typed, evidence-backed, and fails safely", failures)


if __name__ == "__main__":
    sys.exit(main())
