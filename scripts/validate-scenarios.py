#!/usr/bin/env python3
"""Offline checks for scenario build-curriculum structure and safe blueprints."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = ROOT / "scenarios"
REQUIRED_MODULE_SIGNALS = (
    "what you build",
    "choose your path",
    "implementation",
    "verify",
    "next module",
)
RETIRED_WORKSHOP_SIGNALS = (
    "## audience",
    "## preparation",
    "## timed activity",
    "## timed exercise",
    "## artifact",
    "## expected output",
    "## debrief",
)


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS  {message}")
    else:
        print(f"FAIL  {message}")
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    manifests = sorted(SCENARIOS.glob("*/manifest.json"))
    check(bool(manifests), "scenario manifests exist", failures)
    for manifest_path in manifests:
        scenario_root = manifest_path.parent
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        scenario_id = manifest["id"]
        print(f"\n{scenario_id}")
        blueprint = scenario_root / "accelerator" / "main.bicep"
        source = blueprint.read_text(encoding="utf-8") if blueprint.is_file() else ""
        check(blueprint.is_file(), "Bicep blueprint exists", failures)
        # This text check does not replace Bicep compilation or a deployment review.
        secret_assignment = re.compile(
            r"\b(?:password|apiKey|accountKey|sharedAccessKey)\s*[:=]\s*['\"][^'\"]+['\"]",
            re.IGNORECASE,
        )
        check(
            not secret_assignment.search(source),
            "Bicep blueprint has no obvious literal secret assignments",
            failures,
        )
        if source:
            check("param " in source, "Bicep blueprint is parameterised", failures)

        data_root = scenario_root / "accelerator" / "sample-data"
        fixtures = [item for item in data_root.rglob("*") if item.is_file() and item.name != "README.md"]
        check(bool(fixtures), "synthetic sample fixtures exist", failures)

        for lesson in manifest.get("lessons", []):
            lesson_path = scenario_root / lesson["path"]
            text = lesson_path.read_text(encoding="utf-8").lower() if lesson_path.is_file() else ""
            check(lesson_path.is_file(), f"lesson {lesson['id']} exists", failures)
            missing = [signal for signal in REQUIRED_MODULE_SIGNALS if signal not in text]
            detail = f" (missing: {', '.join(missing)})" if missing else ""
            check(not missing, f"lesson {lesson['id']} has the build-module contract{detail}", failures)
            retired = [signal for signal in RETIRED_WORKSHOP_SIGNALS if signal in text]
            check(not retired, f"lesson {lesson['id']} drops the retired workshop template", failures)

        modules = manifest.get("build_modules", [])
        check(bool(modules), "manifest declares build modules", failures)
        module_ids: set[str] = set()
        for module in modules:
            module_id = module.get("id", "<missing>")
            complete = all(module.get(field) for field in ("id", "title", "summary", "outcome"))
            check(complete, f"build module {module_id} declares id, title, summary, and outcome", failures)
            check(module_id not in module_ids, f"build module {module_id} is unique", failures)
            module_ids.add(module_id)
            for implementation_path in module.get("implementation_paths", []):
                check(
                    (scenario_root / implementation_path).exists(),
                    f"build module {module_id} implementation path {implementation_path} exists",
                    failures,
                )

        lesson_ids = [lesson["id"] for lesson in manifest.get("lessons", [])]
        check(
            lesson_ids == [module.get("id") for module in modules],
            f"one build module per lesson, with matching IDs and order ({len(lesson_ids)} lessons, {len(modules)} modules)",
            failures,
        )

    print("\nSCENARIO VALIDATION PASSED" if not failures else f"\nSCENARIO VALIDATION FAILED ({len(failures)} issues)")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
