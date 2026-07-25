#!/usr/bin/env python3
"""Content Understanding scenario validator — offline structural gate.

Checks (all offline, no Azure, SDK, or network calls):
- manifest wiring (required files, 7 lessons mapped 1:1 to 7 build modules in order);
- every lesson uses the 7-section technical-build contract;
- the accelerator Bicep is parameterised, deployable, and free of inline secrets;
- the synthetic fixture pack is internally consistent and correctly hashed;
- each module verification script passes on the shipped fixtures.

    python3 scenarios/content-understanding/validate.py
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ACCELERATOR = ROOT / "accelerator"
SAMPLE_DATA = ACCELERATOR / "sample-data"

REQUIRED_MANIFEST_FIELDS = {
    "facilitator": "FACILITATOR.md",
    "validator": "validate.py",
    "accelerator": "accelerator/README.md",
}

REQUIRED_LESSON_HEADINGS = (
    "## What you build",
    "## Choose your path",
    "## Implementation",
    "## Verify",
    "## Troubleshooting",
    "## Decision record",
    "## Next module",
)

FORBIDDEN_HEADINGS = (
    "## Audience",
    "## Preparation",
    "## Timed activity",
    "## Timed exercise",
    "## Artifact",
    "## Expected output",
    "## Debrief",
)

MODULE_CHECKPOINTS = (
    "verify_foundation.py",
    "verify_document_source.py",
    "verify_extraction_selection.py",
    "verify_typed_extraction.py",
    "verify_human_review.py",
    "verify_prove_and_observe.py",
    "verify_deploy.py",
)

# verify_foundation.py asserts a deployed .env contract, so it cannot pass before provisioning.
# Every other checkpoint must pass offline on the shipped fixtures.
SKIP_OFFLINE_RUN = {"verify_foundation.py"}

SECRET_PATTERNS = (
    re.compile(
        r"(?i)\b(password|pwd|secret|apikey|api_key|accountkey|connectionstring)\b\s*[:=]\s*'[^']+'"
    ),
    re.compile(r"listKeys\("),
)


def _validate_manifest(errors: list[str]) -> dict:
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"manifest.json is invalid: {error}")
        return {}
    for field, expected_value in REQUIRED_MANIFEST_FIELDS.items():
        if manifest.get(field) != expected_value:
            errors.append(f"manifest {field!r} must be {expected_value!r}")
        elif not (ROOT / expected_value).is_file():
            errors.append(f"manifest {field!r} points at a missing file: {expected_value}")

    lessons = manifest.get("lessons", [])
    modules = manifest.get("build_modules", [])
    if len(lessons) != 7:
        errors.append(f"manifest must define exactly 7 lessons, found {len(lessons)}")
    if len(modules) != 7:
        errors.append(f"manifest must define exactly 7 build_modules, found {len(modules)}")
    for index, (lesson, module) in enumerate(zip(lessons, modules), start=1):
        if lesson.get("id") != module.get("id"):
            errors.append(
                f"lesson #{index} id {lesson.get('id')!r} does not match "
                f"build_module id {module.get('id')!r}"
            )
    for module in modules:
        for path in module.get("implementation_paths", []):
            if not (ROOT / path).exists():
                errors.append(f"build module {module.get('id')} references a missing path: {path}")
    return manifest


def _validate_lessons(manifest: dict, errors: list[str]) -> None:
    for lesson in manifest.get("lessons", []):
        lesson_path = ROOT / lesson.get("path", "")
        if not lesson_path.is_file():
            errors.append(f"missing lesson: {lesson.get('path')!r}")
            continue
        text = lesson_path.read_text(encoding="utf-8")
        name = lesson_path.name
        positions = []
        for heading in REQUIRED_LESSON_HEADINGS:
            index = text.find(heading)
            if index == -1:
                errors.append(f"{name} is missing section {heading!r}")
            positions.append(index)
        present = [position for position in positions if position != -1]
        if present != sorted(present):
            errors.append(f"{name} sections are out of the required contract order")
        for heading in FORBIDDEN_HEADINGS:
            if heading in text:
                errors.append(f"{name} uses retired heading {heading.strip()!r}")


def _validate_bicep(errors: list[str]) -> None:
    bicep_path = ACCELERATOR / "main.bicep"
    if not bicep_path.is_file():
        errors.append("accelerator/main.bicep is missing")
        return
    bicep = bicep_path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^\s*resource\s+", bicep):
        errors.append("accelerator/main.bicep must declare deployable resources")
    if not re.search(r"(?m)^\s*param\s+", bicep):
        errors.append("accelerator/main.bicep must be parameterised")
    for pattern in SECRET_PATTERNS:
        if pattern.search(bicep):
            errors.append(
                f"accelerator/main.bicep appears to contain an inline secret "
                f"(pattern: {pattern.pattern!r})"
            )


def _validate_pack(errors: list[str]) -> None:
    """The synthetic pack is the scenario's teaching contract, so it must stay self-consistent."""
    try:
        pack = json.loads((SAMPLE_DATA / "manifest.json").read_text(encoding="utf-8"))
        contract = json.loads((SAMPLE_DATA / "result-contract.json").read_text(encoding="utf-8"))
        golden_cases = json.loads((SAMPLE_DATA / "golden-cases.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"sample-data pack is unreadable: {error}")
        return

    if pack.get("data_classification") != "synthetic":
        errors.append("sample-data pack must be marked data_classification 'synthetic'")

    required_keys = contract["required_keys"]
    value_types = {
        "string": str,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    golden_ids = set()
    for fixture in pack.get("fixtures", []):
        fixture_id = fixture["id"]
        source = SAMPLE_DATA / fixture["path"]
        expected_path = SAMPLE_DATA / fixture["expected_result"]
        if not source.is_file():
            errors.append(f"fixture {fixture_id} source is missing: {fixture['path']}")
            continue
        if not expected_path.is_file():
            errors.append(f"fixture {fixture_id} expected result is missing")
            continue
        if fixture.get("split") == "golden":
            golden_ids.add(fixture_id)

        record = json.loads(expected_path.read_text(encoding="utf-8"))
        for key in required_keys:
            if key not in record:
                errors.append(f"expected result {fixture_id} is missing required key {key!r}")
                continue
            expected_type = value_types[contract["field_value_types"][key]]
            if not isinstance(record[key], expected_type):
                errors.append(
                    f"expected result {fixture_id} key {key!r} must be "
                    f"{contract['field_value_types'][key]}"
                )
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if record.get("source_sha256") != digest:
            errors.append(
                f"expected result {fixture_id} source_sha256 does not match {fixture['path']}"
            )

    case_ids = {case["fixture_id"] for case in golden_cases.get("cases", [])}
    if case_ids != golden_ids:
        errors.append(
            f"golden-cases.json must cover exactly the golden fixtures: {sorted(case_ids)} "
            f"!= {sorted(golden_ids)}"
        )


def _validate_checkpoints(errors: list[str]) -> None:
    scripts_dir = ACCELERATOR / "scripts"
    for script in MODULE_CHECKPOINTS:
        script_path = scripts_dir / script
        if not script_path.is_file():
            errors.append(f"missing module checkpoint: accelerator/scripts/{script}")
            continue
        if script in SKIP_OFFLINE_RUN:
            continue
        result = subprocess.run(
            [sys.executable, str(script_path), "--offline"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            tail = (
                result.stdout.strip().splitlines()[-1]
                if result.stdout.strip()
                else result.stderr.strip()
            )
            errors.append(f"scripts/{script} failed offline (exit {result.returncode}): {tail}")


def validate() -> list[str]:
    errors: list[str] = []
    manifest = _validate_manifest(errors)
    if manifest:
        _validate_lessons(manifest, errors)
    _validate_bicep(errors)
    _validate_pack(errors)
    _validate_checkpoints(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Validation passed: manifest, 7 technical-build lessons, deployable Bicep, "
        "synthetic pack, and offline module checkpoints are consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
