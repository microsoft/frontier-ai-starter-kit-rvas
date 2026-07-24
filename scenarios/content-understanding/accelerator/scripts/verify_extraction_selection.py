#!/usr/bin/env python3
"""Module 3 checkpoint — the extraction capability is selected on the record.

Validates the extraction decision (sample-data/workflow/extraction-decision.json):
  * the selected capability is one of the verified options,
  * a concrete model/analyzer id and API version are named,
  * evidence (confidence + grounding) is required,
  * a confidence threshold in (0, 1] is set, and
  * a named fallback capability with a trigger is recorded.

Offline only — this is a design checkpoint, so there are no Azure calls.

Run:
    python3 .../verify_extraction_selection.py --offline
Fail-path demo:
    python3 .../verify_extraction_selection.py --offline --decision /dev/null
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_json  # noqa: E402

CAPABILITIES = {
    "content_understanding_prebuilt",
    "content_understanding_custom",
    "document_intelligence_prebuilt",
    "document_intelligence_custom",
    "llm_structured_outputs",
    "multimodal_vision",
}


def verify_decision(decision: dict, failures: list[str]) -> None:
    if not isinstance(decision, dict):
        check(False, "decision is a JSON object", failures)
        return
    selected = decision.get("selected_capability")
    check(selected in CAPABILITIES, f"selected_capability is one of {sorted(CAPABILITIES)}", failures)
    check(bool(decision.get("selected_model_or_analyzer")), "a concrete model/analyzer id is named", failures)
    check(bool(decision.get("api_version")), "an API version is recorded", failures)
    check(bool(decision.get("rationale")), "a rationale is recorded", failures)
    check(decision.get("requires_evidence") is True, "evidence (confidence + grounding) is required", failures)
    threshold = decision.get("confidence_threshold")
    check(isinstance(threshold, (int, float)) and 0 < threshold <= 1,
          "confidence_threshold is in (0, 1]", failures)
    fallback = decision.get("fallback_capability")
    check(fallback in CAPABILITIES and fallback != selected,
          "a distinct fallback capability is named", failures)
    check(bool(decision.get("fallback_trigger")), "a fallback trigger is recorded", failures)
    if selected == "llm_structured_outputs":
        check(bool(decision.get("evidence_strategy")),
              "llm_structured_outputs must document an evidence_strategy (no native grounding)", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", type=Path, default=WORKFLOW / "extraction-decision.json")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 3 checkpoint: extraction capability selection ==")
    decision = load_json(args.decision, failures)
    if decision is not None:
        verify_decision(decision, failures)
    print("\n(offline mode: design checkpoint, no Azure calls)")
    return finish(3, "the extraction capability and fallback are recorded", failures)


if __name__ == "__main__":
    sys.exit(main())
