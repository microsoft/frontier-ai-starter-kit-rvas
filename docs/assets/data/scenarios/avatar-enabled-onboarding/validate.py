#!/usr/bin/env python3
"""Static validation for the avatar-onboarding technical build scenario.

Checks (all offline, no Azure calls):
- manifest wiring (required files, 7 lessons mapped 1:1 to 7 build modules in order);
- every lesson uses the new 7-section technical-build contract;
- the accelerator Bicep is parameterised, deployable, and free of inline secrets;
- the fictional sample-data pack is internally consistent (via mock_renderer);
- each offline verification script passes on the shipped fixtures.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "accelerator"))
from mock_renderer import PackRejectedError, validate_pack  # noqa: E402


REQUIRED_MANIFEST_FIELDS = {
    "facilitator": "FACILITATOR.md",
    "local_demo": "local-demo.md",
    "validator": "validate.py",
    "solution": "solution.md",
}

# The new technical-build lesson contract: these H2 sections, in this order.
REQUIRED_LESSON_HEADINGS = (
    "## What you build",
    "## Choose your path",
    "## Implementation",
    "## Verify",
    "## Troubleshooting",
    "## Decision record",
    "## Next module",
)

# Retired headings that must never reappear in a lesson.
FORBIDDEN_HEADINGS = (
    "## Audience",
    "## Preparation",
    "## Timed activity",
    "## Timed exercise",
    "## Artifact",
    "## Expected output",
    "## Debrief",
    "## Decision\n",
    "## Prerequisites",
    "## Build steps",
    "## Files and commands",
    "## Checkpoint",
    "## Evidence",
    "## Common failures",
)

# Offline verification scripts that must pass on the shipped fixtures.
OFFLINE_VERIFY_SCRIPTS = (
    "verify_capability.py",
    "verify_content_pipeline.py",
    "verify_experience.py",
    "verify_approval.py",
    "verify_operate.py",
)

# Heuristic inline-secret patterns that must not appear in Bicep.
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
            idx = text.find(heading)
            if idx == -1:
                errors.append(f"{name} is missing section {heading!r}")
            positions.append(idx)
        present = [p for p in positions if p != -1]
        if present != sorted(present):
            errors.append(f"{name} sections are out of the required contract order")
        for heading in FORBIDDEN_HEADINGS:
            if heading in text:
                errors.append(f"{name} uses retired heading {heading.strip()!r}")
        if "**Default:" not in text and "**Default " not in text:
            errors.append(f"{name} 'Choose your path' must state a bolded **Default:**")
        if "| ---" not in text and "|---" not in text:
            errors.append(f"{name} must include at least one comparison table")


def _validate_bicep(errors: list[str]) -> None:
    bicep_path = ROOT / "accelerator" / "main.bicep"
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
    try:
        validate_pack(ROOT / "accelerator" / "sample-data")
    except PackRejectedError as error:
        errors.append(f"sample-data pack rejected: {error}")


def _validate_offline_scripts(errors: list[str]) -> None:
    scripts_dir = ROOT / "accelerator" / "scripts"
    for script in OFFLINE_VERIFY_SCRIPTS:
        script_path = scripts_dir / script
        if not script_path.is_file():
            errors.append(f"missing verification script: scripts/{script}")
            continue
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            tail = (
                result.stdout.strip().splitlines()[-1]
                if result.stdout.strip()
                else result.stderr.strip()
            )
            errors.append(
                f"scripts/{script} failed offline (exit {result.returncode}): {tail}"
            )


def validate() -> list[str]:
    errors: list[str] = []
    manifest = _validate_manifest(errors)
    if manifest:
        _validate_lessons(manifest, errors)
    _validate_bicep(errors)
    for relative_path in ("FACILITATOR.md", "local-demo.md", "solution.md"):
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing {relative_path}")
    _validate_pack(errors)
    _validate_offline_scripts(errors)
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
        "fictional pack, and offline verification scripts are consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
