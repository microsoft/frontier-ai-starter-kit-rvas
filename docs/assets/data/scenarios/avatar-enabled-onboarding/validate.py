#!/usr/bin/env python3
"""Static validation for the avatar-onboarding scenario's local-only blueprint."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "accelerator"))
from mock_renderer import PackRejectedError, validate_pack  # noqa: E402


REQUIRED_MANIFEST_FIELDS = {
    "facilitator": "FACILITATOR.md",
    "local_demo": "local-demo.md",
    "validator": "validate.py",
}
REQUIRED_LESSON_HEADINGS = (
    "## Goal",
    "## Duration",
    "## Audience",
    "## Prep",
    "## Timed activity",
    "## Artifact",
    "## Expected output",
    "## Validation",
    "## Debrief",
    "## Next decision",
)


def validate() -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"manifest.json is invalid: {error}"]
    for field, expected_value in REQUIRED_MANIFEST_FIELDS.items():
        if manifest.get(field) != expected_value:
            errors.append(f"manifest {field!r} must be {expected_value!r}")

    bicep = (ROOT / "accelerator" / "main.bicep").read_text(encoding="utf-8")
    if re.search(r"(?m)^\s*resource\s+", bicep):
        errors.append("accelerator/main.bicep must remain resource-free")
    if "output integrationSeam object" not in bicep:
        errors.append("accelerator/main.bicep must expose the integration seam blueprint")

    for lesson in manifest.get("lessons", []):
        lesson_path = ROOT / lesson.get("path", "")
        if not lesson_path.is_file():
            errors.append(f"missing lesson: {lesson_path.relative_to(ROOT)}")
            continue
        lesson_text = lesson_path.read_text(encoding="utf-8")
        for heading in REQUIRED_LESSON_HEADINGS:
            if heading not in lesson_text:
                errors.append(
                    f"{lesson_path.relative_to(ROOT)} is missing {heading[3:]!r}"
                )

    for relative_path in ("FACILITATOR.md", "local-demo.md"):
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing {relative_path}")

    try:
        validate_pack(ROOT / "accelerator" / "sample-data")
    except PackRejectedError as error:
        errors.append(f"sample-data pack rejected: {error}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed: blueprint, manifest, lessons, and fictional pack are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
