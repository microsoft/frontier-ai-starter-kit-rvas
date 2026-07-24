#!/usr/bin/env python3
"""Module 7 checkpoint — the reviewable workflow is deployable and governed.

Validates the deploy manifest (sample-data/workflow/deploy-manifest.json):
  * Entra ID auth with a managed identity and no keys,
  * an authenticated endpoint,
  * Application Insights monitoring with GenAI tracing enabled,
  * a rollback strategy, and
  * the module-6 evaluation gate has passed.

Offline validates the manifest. Live mode (--endpoint) confirms the deployed
endpoint rejects an unauthenticated request (expects 401/403).

Run offline:
    python3 .../verify_deploy.py --offline
Fail-path demo:
    python3 .../verify_deploy.py --offline --manifest /dev/null
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import WORKFLOW, check, finish, load_json  # noqa: E402


def verify_manifest(manifest: dict, failures: list[str]) -> None:
    if not isinstance(manifest, dict):
        check(False, "manifest is a JSON object", failures)
        return
    check(manifest.get("auth_mode") == "entra_id", "auth_mode is entra_id", failures)
    check(manifest.get("managed_identity") is True, "a managed identity is used", failures)
    check(manifest.get("keyless") is True, "deployment is keyless", failures)
    check(manifest.get("authenticated_endpoint") is True, "the endpoint is authenticated", failures)
    monitoring = manifest.get("monitoring", {})
    check(isinstance(monitoring, dict) and monitoring.get("application_insights") is True,
          "Application Insights monitoring is enabled", failures)
    check(isinstance(monitoring, dict) and monitoring.get("genai_tracing") is True,
          "GenAI tracing is enabled", failures)
    rollback = manifest.get("rollback", {})
    check(isinstance(rollback, dict) and bool(rollback.get("strategy")), "a rollback strategy is defined", failures)
    check(manifest.get("evaluation_gate_passed") is True, "the module-6 evaluation gate has passed", failures)


def verify_live(endpoint: str, failures: list[str]) -> None:
    try:
        import urllib.error
        import urllib.request

        request = urllib.request.Request(endpoint, method="GET")
        try:
            urllib.request.urlopen(request, timeout=10)  # noqa: S310 - controlled endpoint
            check(False, "unauthenticated request was accepted (endpoint is not protected)", failures)
        except urllib.error.HTTPError as error:
            check(error.code in (401, 403),
                  f"unauthenticated request rejected with {error.code}", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"could not probe endpoint: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=WORKFLOW / "deploy-manifest.json")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--endpoint", help="Live: probe this endpoint expecting 401/403 when unauthenticated.")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 7 checkpoint: deploy the reviewable workflow ==")
    manifest = load_json(args.manifest, failures)
    if manifest is not None:
        verify_manifest(manifest, failures)

    if args.offline or not args.endpoint:
        print("\n(offline mode: manifest validated, no Azure calls)")
    elif not failures:
        verify_live(args.endpoint, failures)

    return finish(7, "the pilot is authenticated, monitored, and rollback-ready", failures)


if __name__ == "__main__":
    sys.exit(main())
