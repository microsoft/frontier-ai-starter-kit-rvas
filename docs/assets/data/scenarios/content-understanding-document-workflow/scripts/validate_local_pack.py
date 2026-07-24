#!/usr/bin/env python3
"""Validate the synthetic Content Understanding workshop pack without network access."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK_ROOT = SCRIPT_ROOT / "accelerator" / "sample-data"
DEFAULT_EVIDENCE_PATH = SCRIPT_ROOT / "evidence" / "local-validation.json"
ALLOWED_FIXTURE_SUFFIXES = {".md", ".txt", ".html"}
SYNTHETIC_MARKER = "SYNTHETIC DEMONSTRATION DATA"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate synthetic fixtures and optionally compare structured local results."
    )
    parser.add_argument(
        "--pack-root",
        type=Path,
        default=DEFAULT_PACK_ROOT,
        help="Fixture-pack directory (default: accelerator/sample-data).",
    )
    parser.add_argument(
        "--actual-dir",
        type=Path,
        help="Directory of result JSON files named after expected files, for exact comparison.",
    )
    parser.add_argument(
        "--evidence-file",
        type=Path,
        default=DEFAULT_EVIDENCE_PATH,
        help="Deterministic JSON evidence output path.",
    )
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path}")
    except json.JSONDecodeError as error:
        errors.append(f"Invalid JSON in {path}: {error.msg}")
    return None


def safe_path(root: Path, relative_path: str, errors: list[str]) -> Path | None:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        errors.append(f"Path escapes pack root: {relative_path}")
        return None
    return candidate


def matches_type(value: Any, expected_type: str) -> bool:
    type_checks = {
        "string": lambda item: isinstance(item, str),
        "boolean": lambda item: isinstance(item, bool),
        "array": lambda item: isinstance(item, list),
        "object": lambda item: isinstance(item, dict),
    }
    return expected_type in type_checks and type_checks[expected_type](value)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_result(
    result: Any, expected_path: Path, contract: dict[str, Any], errors: list[str]
) -> bool:
    if not isinstance(result, dict):
        errors.append(f"Expected result must be an object: {expected_path}")
        return False
    valid = True
    for key in contract["required_keys"]:
        if key not in result:
            errors.append(f"Expected result missing {key}: {expected_path}")
            valid = False
            continue
        expected_type = contract["field_value_types"][key]
        if not matches_type(result[key], expected_type):
            errors.append(
                f"Expected result key {key} has wrong type in {expected_path}; "
                f"expected {expected_type}"
            )
            valid = False
    return valid


def write_evidence(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    pack_root = args.pack_root.resolve()
    manifest = load_json(pack_root / "manifest.json", errors)
    contract = load_json(pack_root / "result-contract.json", errors)
    golden_cases = load_json(pack_root / "golden-cases.json", errors)
    checked_fixtures: list[dict[str, str]] = []
    actual_comparisons: list[dict[str, str]] = []

    if not isinstance(manifest, dict) or not isinstance(contract, dict) or not isinstance(golden_cases, dict):
        report = {
            "actual_comparisons": actual_comparisons,
            "checked_fixtures": checked_fixtures,
            "errors": errors,
            "fixture_count": 0,
            "golden_case_count": 0,
            "valid": False,
            "validator": "content-understanding-local-pack-v1",
        }
        write_evidence(args.evidence_file, report)
        print(f"INVALID: {len(errors)} error(s); evidence: {args.evidence_file}")
        return 1

    required_contract_keys = {"required_keys", "field_value_types"}
    if not required_contract_keys.issubset(contract):
        errors.append("Result contract lacks required_keys or field_value_types.")
    elif not all(
        key in contract["field_value_types"] for key in contract["required_keys"]
    ):
        errors.append("Result contract is missing a type for at least one required key.")
    if errors:
        report = {
            "actual_comparisons": actual_comparisons,
            "checked_fixtures": checked_fixtures,
            "errors": errors,
            "fixture_count": 0,
            "golden_case_count": 0,
            "valid": False,
            "validator": "content-understanding-local-pack-v1",
        }
        write_evidence(args.evidence_file, report)
        print(f"INVALID: {len(errors)} error(s); evidence: {args.evidence_file}")
        return 1

    fixtures = manifest.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        errors.append("Manifest must contain at least one fixture.")
        fixtures = []

    fixture_by_id: dict[str, dict[str, Any]] = {}
    expected_by_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    for entry in fixtures:
        if not isinstance(entry, dict):
            errors.append("Manifest fixture entry must be an object.")
            continue
        required_entry_keys = {"id", "path", "split", "expected_result"}
        if not required_entry_keys.issubset(entry):
            errors.append(f"Manifest fixture missing required keys: {entry}")
            continue
        fixture_id = entry["id"]
        if not isinstance(fixture_id, str) or fixture_id in fixture_by_id:
            errors.append(f"Fixture ids must be unique strings: {fixture_id}")
            continue
        fixture_by_id[fixture_id] = entry

        fixture_path = safe_path(pack_root, entry["path"], errors)
        expected_path = safe_path(pack_root, entry["expected_result"], errors)
        if fixture_path is None or expected_path is None:
            continue
        if fixture_path.suffix not in ALLOWED_FIXTURE_SUFFIXES:
            errors.append(f"Fixture uses a non-local teaching suffix: {fixture_path}")
        if not fixture_path.is_file():
            errors.append(f"Missing fixture: {fixture_path}")
            continue
        source_text = fixture_path.read_text(encoding="utf-8")
        if SYNTHETIC_MARKER not in source_text:
            errors.append(f"Fixture lacks the synthetic-data marker: {fixture_path}")

        expected = load_json(expected_path, errors)
        if not validate_result(expected, expected_path, contract, errors):
            continue
        if expected["document_id"] != fixture_id:
            errors.append(f"Expected document_id does not match manifest id: {fixture_id}")
        actual_hash = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
        if expected["source_sha256"] != actual_hash:
            errors.append(f"Source hash mismatch for fixture: {fixture_id}")
        expected_by_id[fixture_id] = (expected_path, expected)
        checked_fixtures.append(
            {
                "expected_result": str(expected_path.relative_to(pack_root)),
                "fixture_id": fixture_id,
                "fixture_path": str(fixture_path.relative_to(pack_root)),
                "source_sha256": actual_hash,
            }
        )

    golden_cases_list = golden_cases.get("cases")
    if not isinstance(golden_cases_list, list):
        errors.append("Golden-case suite must contain a cases array.")
        golden_cases_list = []
    golden_ids: set[str] = set()
    for case in golden_cases_list:
        if not isinstance(case, dict):
            errors.append("Golden case must be an object.")
            continue
        fixture_id = case.get("fixture_id")
        expected_result = case.get("expected_result")
        if fixture_id in golden_ids:
            errors.append(f"Golden fixture repeated: {fixture_id}")
        golden_ids.add(fixture_id)
        fixture = fixture_by_id.get(fixture_id)
        if fixture is None or fixture.get("split") != "golden":
            errors.append(f"Golden case is not a golden manifest fixture: {fixture_id}")
        elif fixture.get("expected_result") != expected_result:
            errors.append(f"Golden expected-result mismatch: {fixture_id}")

    manifest_golden_ids = {
        fixture_id
        for fixture_id, fixture in fixture_by_id.items()
        if fixture.get("split") == "golden"
    }
    if golden_ids != manifest_golden_ids:
        errors.append("Golden cases do not exactly cover manifest golden fixtures.")

    for fixture_id, fixture in fixture_by_id.items():
        correction_reference = fixture.get("correction")
        if not correction_reference:
            continue
        correction_path = safe_path(pack_root, correction_reference, errors)
        if correction_path is None:
            continue
        correction = load_json(correction_path, errors)
        expected = expected_by_id.get(fixture_id, (None, None))[1]
        if not isinstance(correction, dict) or expected is None:
            continue
        change = correction.get("correction")
        if (
            correction.get("fixture_id") != fixture_id
            or correction.get("expected_result") != fixture["expected_result"]
            or not isinstance(change, dict)
        ):
            errors.append(f"Invalid correction linkage: {correction_path}")
            continue
        field = change.get("field")
        corrected_value = change.get("corrected_value")
        if field not in expected["fields"] or expected["fields"][field] == corrected_value:
            errors.append(f"Correction does not change a known expected field: {correction_path}")

    if args.actual_dir:
        actual_dir = args.actual_dir.resolve()
        for fixture_id, (expected_path, expected) in sorted(expected_by_id.items()):
            actual_path = actual_dir / expected_path.name
            actual = load_json(actual_path, errors)
            status = "match" if canonical_json(actual) == canonical_json(expected) else "mismatch"
            actual_comparisons.append(
                {
                    "fixture_id": fixture_id,
                    "result_file": str(actual_path),
                    "status": status,
                }
            )
            if status == "mismatch":
                errors.append(f"Actual result differs from expected result: {actual_path}")

    report = {
        "actual_comparisons": actual_comparisons,
        "checked_fixtures": checked_fixtures,
        "errors": errors,
        "fixture_count": len(checked_fixtures),
        "golden_case_count": len(golden_ids),
        "valid": not errors,
        "validator": "content-understanding-local-pack-v1",
    }
    write_evidence(args.evidence_file, report)
    status = "VALID" if not errors else "INVALID"
    print(f"{status}: {len(checked_fixtures)} fixture(s); evidence: {args.evidence_file}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
