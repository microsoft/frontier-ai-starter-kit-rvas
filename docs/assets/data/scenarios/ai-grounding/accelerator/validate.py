#!/usr/bin/env python3
"""AI Grounding scenario validator — the pilot-readiness gate.

Structural checks over the accelerator plus every module checkpoint in offline mode.

    python3 scenarios/ai-grounding/accelerator/validate.py --offline   # structure only (default)
    python3 scenarios/ai-grounding/accelerator/validate.py --all       # every module checkpoint
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENARIO = ROOT.parent
SAMPLE_DATA = ROOT / "sample-data"
SCRIPTS = ROOT / "scripts"

REQUIRED_LESSON_SECTIONS = (
    "What you build",
    "Choose your path",
    "Implementation",
    "Verify",
    "Troubleshooting",
    "Decision record",
    "Next module",
)

RETIRED_LESSON_SECTIONS = (
    "Audience",
    "Preparation",
    "Timed activity",
    "Artifact",
    "Expected output",
    "Debrief",
)

MODULE_CHECKPOINTS = (
    "verify_foundation.py",
    "probe_permissions.py",
    "build_knowledge_source.py",
    "verify_retrieval.py",
    "compare_models.py",
    "grounded_answer.py",
    "verify_routing.py",
    "verify_surface.py",
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
    """The Bicep is deployable now, so the guardrail is parameterised and secret-free."""
    bicep = (ROOT / "main.bicep").read_text(encoding="utf-8")
    if not re.search(r"(?m)^\s*resource\s+", bicep):
        fail("main.bicep must declare real, deployable resources")
    if not re.search(r"(?m)^param\s+", bicep):
        fail("main.bicep must be parameterised")
    forbidden = ("clientsecret", "client_secret", "apikey =", "accountkey=", "sharedaccesskey")
    lowered = bicep.lower()
    if any(value in lowered for value in forbidden):
        fail("main.bicep includes a forbidden secret-like setting")
    if "allowSharedKeyAccess: false" not in bicep:
        fail("storage must disable shared-key access (keyless-first)")


def check_lessons() -> None:
    lessons = sorted((SCENARIO / "lessons").glob("*.md"))
    if len(lessons) != 8:
        fail(f"expected 8 lessons, one per build module, found {len(lessons)}")
    for lesson in lessons:
        text = lesson.read_text(encoding="utf-8")
        missing = [field for field in REQUIRED_LESSON_SECTIONS if f"## {field}" not in text]
        if missing:
            fail(f"{lesson.name} is missing required sections: {', '.join(missing)}")
        retired = [field for field in RETIRED_LESSON_SECTIONS if f"## {field}" in text]
        if retired:
            fail(f"{lesson.name} uses retired workshop sections: {', '.join(retired)}")


def check_manifest_alignment() -> None:
    manifest = json.loads((SCENARIO / "manifest.json").read_text(encoding="utf-8"))
    lesson_ids = [lesson["id"] for lesson in manifest["lessons"]]
    module_ids = [module["id"] for module in manifest["build_modules"]]
    if lesson_ids != module_ids:
        fail(f"lessons must map 1:1 to build modules in order: {lesson_ids} != {module_ids}")
    for lesson in manifest["lessons"]:
        if not (SCENARIO / lesson["path"]).is_file():
            fail(f"lesson path does not exist: {lesson['path']}")
    for module in manifest["build_modules"]:
        for path in module.get("implementation_paths", []):
            if not (SCENARIO / path).exists():
                fail(f"build module {module['id']} references a missing path: {path}")


def check_evidence() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "prepare_local_corpus.py")],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"local simulation failed:\n{result.stdout}{result.stderr}")
    evidence = json.loads((ROOT / "evidence" / "local-retrieval-evidence.json").read_text(encoding="utf-8"))
    if not evidence["deterministic"] or evidence["summary"]["failed_case_ids"]:
        fail("evidence must be deterministic and all golden cases must pass")
    for case in evidence["cases"]:
        if not case["passed"]:
            fail(f"golden case failed: {case['id']}")
        if case["expected_behavior"] == "refuse" and case["outcome"]["citations"]:
            fail(f"refusal case cited a source: {case['id']}")


def check_module_checkpoints() -> None:
    """Every module ships a runnable checkpoint, and each one passes offline."""
    for script in MODULE_CHECKPOINTS:
        path = SCRIPTS / script
        if not path.is_file():
            fail(f"module checkpoint is missing: scripts/{script}")
        result = subprocess.run(
            [sys.executable, str(path), "--offline"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(f"scripts/{script} --offline failed:\n{result.stdout}{result.stderr}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only (default).")
    parser.add_argument("--all", action="store_true", help="Also run every module checkpoint offline.")
    args = parser.parse_args()

    check_source_metadata()
    check_blueprint()
    check_lessons()
    check_manifest_alignment()
    check_evidence()

    if args.all:
        check_module_checkpoints()
        print("AI Grounding validation passed — structure and all 8 module checkpoints.")
    else:
        print("AI Grounding accelerator validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
