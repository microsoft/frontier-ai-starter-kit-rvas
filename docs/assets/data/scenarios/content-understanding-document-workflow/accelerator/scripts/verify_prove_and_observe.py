#!/usr/bin/env python3
"""Module 6 checkpoint — the workflow is evaluated and traced against a gate.

Validates the evaluation report (sample-data/workflow/eval-report.json):
  * declares thresholds for field accuracy, false approval, review rate, and
    injection resistance,
  * reports a metric for each threshold, and
  * every metric meets its gate (min thresholds are floors, max thresholds are
    ceilings). A single breach fails the module.

Offline mode validates the report contract and evidence references. It does not prove that a live
Foundry evaluation or tracing run occurred unless you point the evidence references to retained
trace/evaluation artifacts from your environment.

Run (passing report):
    python3 .../verify_prove_and_observe.py --offline
Fail-path demo (a false approval slipped through):
    python3 .../verify_prove_and_observe.py --offline --report sample-data/workflow/eval-report-failing.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_json  # noqa: E402

# metric_key -> (threshold_key, direction)  direction 'min' = floor, 'max' = ceiling
GATES = {
    "field_accuracy": ("field_accuracy_min", "min"),
    "false_approval_rate": ("false_approval_max", "max"),
    "review_rate": ("review_rate_max", "max"),
    "injection_resistance": ("injection_resistance_min", "min"),
}


def evidence_path_exists(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    if not path.is_absolute():
        path = WORKFLOW.parent.parent / path
    return path.is_file()


def verify_report(report: dict, failures: list[str]) -> None:
    if not isinstance(report, dict):
        check(False, "report is a JSON object", failures)
        return
    thresholds = report.get("thresholds", {})
    metrics = report.get("metrics", {})
    evidence = report.get("evidence", {})
    check(isinstance(thresholds, dict) and isinstance(metrics, dict),
          "report declares thresholds and metrics objects", failures)
    check(
        isinstance(evidence, dict)
        and bool(evidence.get("evaluation_run_id"))
        and bool(evidence.get("trace_artifact"))
        and bool(evidence.get("case_result_artifact")),
        "report records evaluation_run_id, trace_artifact, and case_result_artifact",
        failures,
    )
    check(evidence_path_exists(evidence.get("trace_artifact")),
          "trace_artifact points to a retained evidence file", failures)
    check(evidence_path_exists(evidence.get("case_result_artifact")),
          "case_result_artifact points to a retained evidence file", failures)
    check(isinstance(report.get("case_count"), int) and report["case_count"] > 0,
          "report covers at least one case", failures)

    for metric_key, (threshold_key, direction) in GATES.items():
        metric = metrics.get(metric_key)
        threshold = thresholds.get(threshold_key)
        if not isinstance(metric, (int, float)) or not isinstance(threshold, (int, float)):
            check(False, f"metric '{metric_key}' and threshold '{threshold_key}' are numbers", failures)
            continue
        ok = metric >= threshold if direction == "min" else metric <= threshold
        symbol = ">=" if direction == "min" else "<="
        check(ok, f"{metric_key}={metric} {symbol} {threshold} ({threshold_key})", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=WORKFLOW / "eval-report.json")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 6 checkpoint: evaluate and trace ==")
    report = load_json(args.report, failures)
    if report is not None:
        verify_report(report, failures)
    print("\n(offline mode: validates report contract and evidence references, no Azure calls)")
    return finish(6, "the evaluation report contract is complete and gates pass", failures)


if __name__ == "__main__":
    sys.exit(main())
