#!/usr/bin/env python3
"""Offline checks for scenario workshop-kit structure and safe blueprints."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = ROOT / "scenarios"
REQUIRED_LESSON_SIGNALS = (
    "goal",
    "duration",
    "facilitator",
    "artifact",
    "expected",
    "validation",
    "debrief",
    "next decision",
)
TIMED_EXERCISE_SIGNALS = ("timed activity", "timed exercise")


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS  {message}")
    else:
        print(f"FAIL  {message}")
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    for manifest_path in sorted(SCENARIOS.glob("*/manifest.json")):
        scenario_root = manifest_path.parent
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        scenario_id = manifest["id"]
        print(f"\n{scenario_id}")
        for field in ("facilitator", "local_demo", "validator"):
            value = manifest.get(field)
            check(bool(value and (scenario_root / value).is_file()), f"{field} exists", failures)

        blueprint = scenario_root / "accelerator" / "main.bicep"
        source = blueprint.read_text(encoding="utf-8") if blueprint.is_file() else ""
        check(blueprint.is_file(), "Bicep blueprint exists", failures)
        check("\nresource " not in f"\n{source}", "Bicep blueprint declares no resources", failures)

        data_root = scenario_root / "accelerator" / "sample-data"
        fixtures = [item for item in data_root.rglob("*") if item.is_file() and item.name != "README.md"]
        check(bool(fixtures), "synthetic sample fixtures exist", failures)

        for lesson in manifest.get("lessons", []):
            lesson_path = scenario_root / lesson["path"]
            text = lesson_path.read_text(encoding="utf-8").lower() if lesson_path.is_file() else ""
            check(lesson_path.is_file(), f"lesson {lesson['id']} exists", failures)
            missing = [signal for signal in REQUIRED_LESSON_SIGNALS if signal not in text]
            if not any(signal in text for signal in TIMED_EXERCISE_SIGNALS):
                missing.append("timed activity or exercise")
            check(not missing, f"lesson {lesson['id']} has workshop contract", failures)

    print("\nSCENARIO VALIDATION PASSED" if not failures else f"\nSCENARIO VALIDATION FAILED ({len(failures)} issues)")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
