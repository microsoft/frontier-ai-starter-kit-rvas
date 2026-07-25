#!/usr/bin/env python3
"""Module 3 checkpoint — the governed content pipeline produces a typed, traceable claim set.

Offline (default structure check): every approved claim carries a stable id, exact approved
wording, an authoritative source reference, a named owner, required reviewers, and the pack
declares a version and an expiry/review date. Nothing downstream may cite content that is not
here.

Live (--live): also confirm the approved-content blob container is reachable with Entra ID and
that the approved source documents have been uploaded.

Run:
    python3 scenarios/avatar-onboarding/accelerator/scripts/verify_content_pipeline.py
    python3 .../verify_content_pipeline.py --live
    python3 .../verify_content_pipeline.py --offline    # explicit structure-only
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
DEFAULT_CLAIMS = ACCELERATOR / "sample-data" / "claims.json"
ENV_FILE = ACCELERATOR / ".env"

REQUIRED_CLAIM_FIELDS = ("claim_id", "approved_wording", "source_reference", "owner", "required_reviewers")


def check(passed: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    values.update(dict(os.environ))
    return values


def verify_structure(claims_path: Path, failures: list[str]) -> None:
    if not claims_path.is_file():
        check(False, f"claim set exists at {claims_path}", failures)
        return
    try:
        pack = json.loads(claims_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        check(False, f"claim set is valid JSON ({error})", failures)
        return

    check(bool(pack.get("version")), "pack declares a version", failures)
    check(bool(pack.get("review_by")), "pack declares an expiry/review date (review_by)", failures)
    check(bool(pack.get("content_owner")), "pack declares a content owner", failures)

    claims = pack.get("claims")
    if not isinstance(claims, list) or not claims:
        check(False, "pack has a non-empty claims list", failures)
        return
    check(True, f"pack has {len(claims)} claim(s)", failures)

    seen: set[str] = set()
    for index, claim in enumerate(claims):
        label = claim.get("claim_id", f"claims[{index}]")
        for field in REQUIRED_CLAIM_FIELDS:
            value = claim.get(field)
            check(bool(value), f"{label} declares {field!r}", failures)
        claim_id = claim.get("claim_id")
        if claim_id:
            check(claim_id not in seen, f"claim id {claim_id!r} is unique", failures)
            seen.add(claim_id)
        reviewers = claim.get("required_reviewers")
        check(isinstance(reviewers, list) and bool(reviewers),
              f"{label} names at least one required reviewer", failures)


def verify_live(env: dict[str, str], failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.storage.blob import BlobServiceClient
    except ImportError as error:
        check(False, f"missing SDK dependency: {error}", failures)
        return
    account = env.get("AZURE_STORAGE_ACCOUNT_NAME")
    container = env.get("AZURE_STORAGE_CONTAINER_NAME", "approved-content")
    if not account:
        check(False, "AZURE_STORAGE_ACCOUNT_NAME is set", failures)
        return
    try:
        client = BlobServiceClient(
            account_url=f"https://{account}.blob.core.windows.net",
            credential=DefaultAzureCredential(),
        )
        blobs = list(client.get_container_client(container).list_blob_names())
        check(bool(blobs), f"approved-content container '{container}' has uploaded blobs ({len(blobs)})", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"blob container keyless call failed: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", type=Path, default=DEFAULT_CLAIMS, help="path to the claim set JSON")
    parser.add_argument("--live", action="store_true", help="also verify the blob container (calls Azure)")
    parser.add_argument("--offline", action="store_true", help="structure-only (default)")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 3 checkpoint: governed content pipeline ==")
    verify_structure(args.claims, failures)

    if args.live and not args.offline:
        if failures:
            print("\nSkipping live checks until the claim set is valid.")
        else:
            verify_live(load_env(), failures)
    else:
        print("\n(offline mode: skipped live Azure checks)")

    if failures:
        print(f"\n❌ Module 3 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 3 checkpoint PASS — the claim set is typed, owned, versioned, and traceable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
