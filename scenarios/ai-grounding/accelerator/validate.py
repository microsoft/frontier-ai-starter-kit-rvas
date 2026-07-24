#!/usr/bin/env python3
"""Focused structural checks for the AI Grounding / IQ fictional accelerator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SAMPLE_DATA = ROOT / "sample-data"
REQUIRED_LESSON_FIELDS = (
    "Goal",
    "Duration",
    "Audience",
    "Preparation",
    "Timed activity",
    "Artifact",
    "Expected output",
    "Validation",
    "Debrief",
    "Next decision",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def check_source_metadata() -> None:
    manifest = json.loads((SAMPLE_DATA / "source-manifest.json").read_text(encoding="utf-8"))
    source_ids = set()
    for source in manifest["sources"]:
        source_id = source["source_id"]
        if source_id in source_ids:
            fail(f"duplicate source ID: {source_id}")
        source_ids.add(source_id)
        text = (SAMPLE_DATA / source["path"]).read_text(encoding="utf-8")
        for required in (f"source_id: {source_id}", "owner:", "access_groups:"):
            if required not in text:
                fail(f"{source['path']} is missing front-matter {required!r}")
        if not source["access_groups"]:
            fail(f"{source_id} has no access group")


def check_blueprint() -> None:
    bicep = (ROOT / "main.bicep").read_text(encoding="utf-8")
    if re.search(r"(?m)^\s*resource\s+", bicep):
        fail("main.bicep must remain resource-free")
    forbidden = ("tenantId", "clientSecret", "client_id", "apiKey", "connectionString")
    if any(value.lower() in bicep.lower() for value in forbidden):
        fail("main.bicep includes a forbidden identity or secret-like setting")


def check_lessons() -> None:
    lessons = sorted((ROOT.parent / "lessons").glob("*.md"))
    if len(lessons) != 5:
        fail(f"expected 5 lessons, found {len(lessons)}")
    for lesson in lessons:
        text = lesson.read_text(encoding="utf-8")
        missing = [field for field in REQUIRED_LESSON_FIELDS if f"## {field}" not in text]
        if missing:
            fail(f"{lesson.name} is missing module fields: {', '.join(missing)}")


def check_evidence() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "prepare_local_corpus.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"local simulation failed:\n{result.stdout}{result.stderr}")
    evidence_path = ROOT / "evidence" / "local-retrieval-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if not evidence["deterministic"] or evidence["summary"]["failed_case_ids"]:
        fail("evidence must be deterministic and all golden cases must pass")
    for case in evidence["cases"]:
        if not case["passed"]:
            fail(f"golden case failed: {case['id']}")
        if case["expected_behavior"] == "refuse" and case["outcome"]["citations"]:
            fail(f"refusal case cited a source: {case['id']}")


def main() -> int:
    check_source_metadata()
    check_blueprint()
    check_lessons()
    check_evidence()
    print("AI Grounding / IQ accelerator validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
