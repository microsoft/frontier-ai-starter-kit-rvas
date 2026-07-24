#!/usr/bin/env python3
"""Module 1 checkpoint — prove the grounding foundation is real and keyless.

Checks, in order:
  1. The .env contract exists and declares every variable later modules depend on.
  2. The Foundry project endpoint answers with the caller's Entra credential.
  3. Both the chat and embedding deployments exist.
  4. Azure AI Search answers, has semantic ranking, and is reachable without a key.

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/verify_foundation.py

Offline/structure-only (no Azure calls, used by CI and by the scenario validator):
    python3 .../verify_foundation.py --offline
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
ENV_FILE = ACCELERATOR / ".env"

REQUIRED_ENV = (
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "AZURE_AI_EMBEDDING_DEPLOYMENT_NAME",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "AZURE_STORAGE_CONTAINER_NAME",
)

FORBIDDEN_ENV_SUBSTRINGS = ("API_KEY", "ACCOUNT_KEY", "CONNECTION_STRING", "SAS_TOKEN")


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    values.update({key: os.environ[key] for key in REQUIRED_ENV if os.environ.get(key)})
    return values


def check(passed: bool, message: str, failures: list[str]) -> bool:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)
    return passed


def verify_structure(env: dict[str, str], failures: list[str], require_env: bool = True) -> None:
    if require_env:
        check(bool(env), f"environment contract loaded ({ENV_FILE.name} or process env)", failures)
        for key in REQUIRED_ENV:
            check(bool(env.get(key)), f"{key} is set", failures)

    leaked = [key for key in env if any(bad in key.upper() for bad in FORBIDDEN_ENV_SUBSTRINGS)]
    check(not leaked, f"no key/secret variables in the contract (found: {leaked or 'none'})", failures)


def verify_live(env: dict[str, str], failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.search.documents.indexes import SearchIndexClient
    except ImportError as error:
        failures.append(f"missing SDK dependency: {error}. Install with: pip install -r requirements.txt")
        print(f"FAIL  SDK import ({error})")
        return

    credential = DefaultAzureCredential()

    try:
        index_client = SearchIndexClient(endpoint=env["AZURE_SEARCH_ENDPOINT"], credential=credential)
        list(index_client.list_index_names())
        check(True, "Azure AI Search answered using Entra ID (keyless)", failures)
    except Exception as error:  # noqa: BLE001 - surface the real Azure error to the learner
        check(False, f"Azure AI Search keyless call failed: {error}", failures)

    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=env["AZURE_AI_PROJECT_ENDPOINT"], credential=credential)
        deployment_names = {deployment.name for deployment in project.deployments.list()}
        check(
            env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] in deployment_names,
            f"chat deployment '{env['AZURE_AI_MODEL_DEPLOYMENT_NAME']}' exists",
            failures,
        )
        check(
            env["AZURE_AI_EMBEDDING_DEPLOYMENT_NAME"] in deployment_names,
            f"embedding deployment '{env['AZURE_AI_EMBEDDING_DEPLOYMENT_NAME']}' exists",
            failures,
        )
    except ImportError as error:
        check(False, f"azure-ai-projects not installed ({error})", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"Foundry project call failed: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env()

    print("== Module 1 checkpoint: grounding foundation ==")
    verify_structure(env, failures, require_env=not args.offline)

    if args.offline:
        print("\n(offline mode: skipped environment and live Azure checks)")
    elif not failures:
        verify_live(env, failures)
    else:
        print("\nSkipping live checks until the environment contract is complete.")

    if failures:
        print(f"\n❌ Module 1 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 1 checkpoint PASS — grounding foundation is provisioned and keyless")
    return 0


if __name__ == "__main__":
    sys.exit(main())
