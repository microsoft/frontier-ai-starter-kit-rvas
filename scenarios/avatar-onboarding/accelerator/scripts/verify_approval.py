#!/usr/bin/env python3
"""Module 6 checkpoint — publication is gated behind human approval, with a withdrawal path.

Offline structural check: the approval record covers every required human role (SME, legal /
compliance, brand, and content owner), matches the exact script id + version it approves, and the
renderer refuses any pack that is not fully approved. It also proves the *withdrawal* path exists:
mutating the approval status must cause the renderer to reject the pack.

Run:
    python3 scenarios/avatar-onboarding/accelerator/scripts/verify_approval.py
    python3 .../verify_approval.py --offline
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ACCELERATOR))
from content_pack import (  # noqa: E402
    REQUIRED_APPROVER_ROLES,
    PackRejectedError,
    validate_pack,
)

DEFAULT_DATA_DIR = ACCELERATOR / "sample-data"


def check(passed: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)


def verify(data_dir: Path, failures: list[str]) -> None:
    approvals_path = data_dir / "approvals.json"
    if not approvals_path.is_file():
        check(False, f"approval record exists at {approvals_path}", failures)
        return
    approvals = json.loads(approvals_path.read_text(encoding="utf-8"))

    approved_roles = {
        row.get("role")
        for row in approvals.get("approvals", [])
        if isinstance(row, dict) and row.get("decision") == "approved"
    }
    missing = REQUIRED_APPROVER_ROLES - approved_roles
    check(not missing, f"all required approver roles present (missing: {sorted(missing) or 'none'})", failures)

    for row in approvals.get("approvals", []):
        if row.get("decision") == "approved":
            check(bool(row.get("approver")) and bool(row.get("decided_at")),
                  f"approval by role {row.get('role')!r} names an approver and a timestamp", failures)

    # 1. The happy path: a fully-approved pack renders.
    try:
        validate_pack(data_dir)
        check(True, "fully-approved pack is accepted (publication is allowed)", failures)
    except PackRejectedError as error:
        check(False, f"fully-approved pack should be accepted ({error})", failures)

    # 2. The gate: dropping any single required approval must block publication.
    for role in sorted(REQUIRED_APPROVER_ROLES):
        mutated = copy.deepcopy(approvals)
        mutated["approvals"] = [r for r in mutated["approvals"] if r.get("role") != role]
        blocked = _pack_rejected_with(data_dir, mutated, failures)
        check(blocked, f"removing the {role!r} approval blocks publication", failures)

    # 3. Withdrawal: flipping the status must block publication even with all sign-offs.
    withdrawn = copy.deepcopy(approvals)
    withdrawn["approval_status"] = "withdrawn"
    check(_pack_rejected_with(data_dir, withdrawn, failures),
          "withdrawing the approval status blocks publication", failures)


def _pack_rejected_with(data_dir: Path, approvals_obj: dict, failures: list[str]) -> bool:
    """Return True if the renderer rejects the pack when approvals.json is temporarily replaced."""
    approvals_path = data_dir / "approvals.json"
    original = approvals_path.read_text(encoding="utf-8")
    try:
        approvals_path.write_text(json.dumps(approvals_obj, indent=2), encoding="utf-8")
        try:
            validate_pack(data_dir)
            return False
        except PackRejectedError:
            return True
    finally:
        approvals_path.write_text(original, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="approved pack directory")
    parser.add_argument("--offline", action="store_true", help="structure-only; never call Azure")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 6 checkpoint: human approval gate ==")
    verify(args.data_dir, failures)

    if failures:
        print(f"\n❌ Module 6 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 6 checkpoint PASS — publication requires approval and withdrawal blocks it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
