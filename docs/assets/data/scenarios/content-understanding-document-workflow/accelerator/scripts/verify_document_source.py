#!/usr/bin/env python3
"""Module 2 checkpoint — an approved document source with intake controls.

Validates the intake plan (sample-data/workflow/intake-plan.json by default):
  * a supported source kind is chosen,
  * source identity, version, permissions, and a hash are retained,
  * inbound and quarantine containers are named, and
  * quarantine rules and a retention window are declared.

Live mode (no --offline) additionally confirms both containers exist and are
reachable keyless, and that the quarantine container is not publicly accessible.

Run offline (structure only):
    python3 .../verify_document_source.py --offline
Fail-path demo (point at any file that is not a valid plan):
    python3 .../verify_document_source.py --offline --plan /dev/null
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_env, load_json  # noqa: E402

SUPPORTED_SOURCE_KINDS = {"azure_blob", "adls_gen2", "sharepoint", "onelake"}
REQUIRED_METADATA = {"source_uri", "source_version", "sha256", "permission_owner_ids"}


def verify_plan(plan: dict, failures: list[str]) -> None:
    if not isinstance(plan, dict):
        check(False, "intake plan is a JSON object", failures)
        return
    check(plan.get("source_kind") in SUPPORTED_SOURCE_KINDS,
          f"source_kind is one of {sorted(SUPPORTED_SOURCE_KINDS)}", failures)
    check(bool(plan.get("inbound_container")), "inbound_container is named", failures)
    check(bool(plan.get("quarantine_container")), "quarantine_container is named", failures)
    retained = set(plan.get("retained_metadata", []))
    missing = REQUIRED_METADATA - retained
    check(not missing, f"source identity/version/permission metadata retained (missing: {missing or 'none'})", failures)
    check(bool(plan.get("quarantine_rules")), "quarantine rules are declared", failures)
    check(isinstance(plan.get("retention_days"), int) and plan["retention_days"] > 0,
          "a positive retention window is set", failures)
    check(plan.get("keyless") is True, "intake is keyless (managed identity, not keys)", failures)


def verify_live(plan: dict, env: dict[str, str], failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient
    except ImportError as error:
        check(False, f"missing SDK dependency: {error}", failures)
        return
    try:
        account = env["AZURE_STORAGE_ACCOUNT_NAME"]
        service = BlobServiceClient(f"https://{account}.blob.core.windows.net",
                                    credential=DefaultAzureCredential())
        containers = {c.name: c for c in service.list_containers()}
        for name in (plan.get("inbound_container"), plan.get("quarantine_container")):
            check(name in containers, f"container '{name}' exists and is reachable keyless", failures)
            if name in containers:
                public = containers[name].get("public_access")
                check(not public, f"container '{name}' is not publicly accessible", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"blob keyless call failed: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=WORKFLOW / "intake-plan.json")
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 2 checkpoint: approved document source ==")
    plan = load_json(args.plan, failures)
    if plan is not None:
        verify_plan(plan, failures)

    if args.offline:
        print("\n(offline mode: plan validated, no Azure calls)")
    elif plan is not None and not failures:
        verify_live(plan, load_env(), failures)
    else:
        print("\nFix the intake plan before running it against Azure.")

    return finish(2, "the approved source and intake controls are defined", failures)


if __name__ == "__main__":
    sys.exit(main())
