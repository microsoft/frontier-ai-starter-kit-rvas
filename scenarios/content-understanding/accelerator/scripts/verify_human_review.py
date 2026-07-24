#!/usr/bin/env python3
"""Module 5 checkpoint — review, correction, and handoff leave a trace.

Validates the approval trace (sample-data/workflow/approval-trace.json):
  * a named reviewer identity and a timestamp,
  * a review outcome from the allowed set,
  * every correction records field, original value, corrected value, and reason
    (so it is reusable as evaluation evidence and never silently overwrites the
    original extraction), and
  * an approved handoff names the downstream seam.

Offline only — this is a workflow-evidence checkpoint.

Run:
    python3 .../verify_human_review.py --offline
Fail-path demo:
    python3 .../verify_human_review.py --offline --trace /dev/null
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_json  # noqa: E402

OUTCOMES = {"approved", "approved_with_correction", "rejected", "returned_for_more_info"}


def verify_trace(trace: dict, failures: list[str]) -> None:
    if not isinstance(trace, dict):
        check(False, "trace is a JSON object", failures)
        return
    check(bool(trace.get("reviewer_id")), "a named reviewer identity is recorded", failures)
    check(bool(trace.get("reviewed_at")), "a review timestamp is recorded", failures)
    outcome = trace.get("review_outcome")
    check(outcome in OUTCOMES, f"review_outcome is one of {sorted(OUTCOMES)}", failures)

    corrections = trace.get("corrections", [])
    if outcome == "approved_with_correction":
        check(bool(corrections), "approved_with_correction includes at least one correction", failures)
    for index, correction in enumerate(corrections):
        label = f"correction[{index}]"
        if not isinstance(correction, dict):
            check(False, f"{label} is an object", failures)
            continue
        for key in ("field", "original_value", "corrected_value", "reason"):
            check(key in correction, f"{label} records '{key}'", failures)
        if "original_value" in correction and "corrected_value" in correction:
            check(correction["original_value"] != correction["corrected_value"],
                  f"{label} actually changes the value", failures)

    handoff = trace.get("handoff")
    if isinstance(handoff, dict) and handoff.get("approved"):
        check(bool(handoff.get("target_seam")), "approved handoff names a downstream seam", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", type=Path, default=WORKFLOW / "approval-trace.json")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 5 checkpoint: review, correction, and handoff ==")
    trace = load_json(args.trace, failures)
    if trace is not None:
        verify_trace(trace, failures)
    print("\n(offline mode: workflow-evidence checkpoint, no Azure calls)")
    return finish(5, "reviewer corrections and the approval trace are retained", failures)


if __name__ == "__main__":
    sys.exit(main())
