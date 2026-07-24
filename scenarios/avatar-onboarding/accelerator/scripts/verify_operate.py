#!/usr/bin/env python3
"""Module 7 checkpoint — the pilot has an evidence-backed release decision.

Offline structural check: the release decision carries a scorecard that meets its own declared
thresholds (grounding pass rate, accessibility defects, red-team high-severity findings, and
unapproved-claim leaks), the trace was reviewed, and the operational feedback fixture is a
privacy-safe synthetic aggregate (no identifiers, no free-text). A decision to ship must not be
recorded unless every gate is green.

Run:
    python3 scenarios/avatar-onboarding/accelerator/scripts/verify_operate.py
    python3 .../verify_operate.py --offline
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
SAMPLE_DATA = ACCELERATOR / "sample-data"
DEFAULT_RELEASE = SAMPLE_DATA / "release-decision.json"
DEFAULT_FEEDBACK = SAMPLE_DATA / "feedback-fixture.json"


def check(passed: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)


def verify_release(release_path: Path, failures: list[str]) -> None:
    if not release_path.is_file():
        check(False, f"release decision exists at {release_path}", failures)
        return
    release = json.loads(release_path.read_text(encoding="utf-8"))
    scorecard = release.get("scorecard", {})
    thresholds = release.get("thresholds", {})
    check(bool(scorecard) and bool(thresholds), "release declares a scorecard and thresholds", failures)
    check(release.get("trace_reviewed") is True, "a trace was reviewed", failures)

    gates_green = (
        scorecard.get("grounding_pass_rate", 0) >= thresholds.get("min_grounding_pass_rate", 1)
        and scorecard.get("accessibility_defects", 1) <= thresholds.get("max_accessibility_defects", 0)
        and scorecard.get("redteam_high_severity_findings", 1) <= thresholds.get("max_redteam_high_severity_findings", 0)
        and scorecard.get("unapproved_claim_leaks", 1) <= thresholds.get("max_unapproved_claim_leaks", 0)
    )
    for name, value, bound, cmp in (
        ("grounding pass rate", scorecard.get("grounding_pass_rate"), thresholds.get("min_grounding_pass_rate"), ">="),
        ("accessibility defects", scorecard.get("accessibility_defects"), thresholds.get("max_accessibility_defects"), "<="),
        ("red-team high-severity findings", scorecard.get("redteam_high_severity_findings"), thresholds.get("max_redteam_high_severity_findings"), "<="),
        ("unapproved claim leaks", scorecard.get("unapproved_claim_leaks"), thresholds.get("max_unapproved_claim_leaks"), "<="),
    ):
        print(f"      {name}: {value} {cmp} {bound}")

    decision = release.get("decision")
    if decision == "ship-pilot":
        check(gates_green, "ship-pilot decision only when every gate is green", failures)
    else:
        check(True, f"decision recorded as {decision!r}", failures)


def verify_feedback(feedback_path: Path, failures: list[str]) -> None:
    if not feedback_path.is_file():
        check(False, f"feedback fixture exists at {feedback_path}", failures)
        return
    feedback = json.loads(feedback_path.read_text(encoding="utf-8"))
    check(feedback.get("classification") == "synthetic-aggregate-demo-data",
          "feedback fixture is a synthetic aggregate", failures)
    text = json.dumps(feedback).lower()
    for forbidden in ("email", "employee_id", "free_text", "comment"):
        check(forbidden not in text, f"feedback fixture contains no {forbidden!r} identifier/free-text", failures)
    check(not re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text),
          "feedback fixture contains no email address", failures)
    measures = feedback.get("measures", {})
    check(bool(measures), "feedback fixture reports aggregate operational measures", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE, help="release decision JSON")
    parser.add_argument("--feedback", type=Path, default=DEFAULT_FEEDBACK, help="operational feedback fixture JSON")
    parser.add_argument("--offline", action="store_true", help="structure-only; never call Azure")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 7 checkpoint: prove and operate ==")
    verify_release(args.release, failures)
    verify_feedback(args.feedback, failures)

    if failures:
        print(f"\n❌ Module 7 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 7 checkpoint PASS — release gates are green, trace reviewed, feedback privacy-safe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
