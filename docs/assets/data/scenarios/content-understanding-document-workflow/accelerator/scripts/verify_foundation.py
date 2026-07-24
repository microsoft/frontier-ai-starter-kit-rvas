#!/usr/bin/env python3
"""Module 1 checkpoint — the document-workflow foundation is real and keyless.

Checks:
  1. The .env contract exists and declares every variable later modules depend on.
  2. No key/secret variables leaked into the contract.
  3. (live) The Foundry project answers with the caller's Entra credential and the
     chat + embedding deployments exist.
  4. (live) The inbound and quarantine blob containers are reachable without a key.

Run:
    python3 scenarios/content-understanding/accelerator/scripts/verify_foundation.py
Offline (structure only, no Azure calls):
    python3 .../verify_foundation.py --offline
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cu_common import check, finish, load_env, no_leaked_secrets  # noqa: E402

REQUIRED_ENV = (
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZURE_CONTENT_UNDERSTANDING_ENDPOINT",
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "AZURE_AI_EMBEDDING_DEPLOYMENT_NAME",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "AZURE_DOCUMENTS_CONTAINER_NAME",
    "AZURE_QUARANTINE_CONTAINER_NAME",
)


def verify_structure(env: dict[str, str], failures: list[str]) -> None:
    check(bool(env), "environment contract loaded (.env or process env)", failures)
    for key in REQUIRED_ENV:
        check(bool(env.get(key)), f"{key} is set", failures)
    no_leaked_secrets(env, failures)


def verify_live(env: dict[str, str], failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
    except ImportError as error:
        check(False, f"missing SDK dependency: {error} (pip install -r requirements.txt)", failures)
        return

    credential = DefaultAzureCredential()

    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=env["AZURE_AI_PROJECT_ENDPOINT"], credential=credential)
        deployment_names = {deployment.name for deployment in project.deployments.list()}
        check(env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] in deployment_names,
              f"chat deployment '{env['AZURE_AI_MODEL_DEPLOYMENT_NAME']}' exists", failures)
        check(env["AZURE_AI_EMBEDDING_DEPLOYMENT_NAME"] in deployment_names,
              f"embedding deployment '{env['AZURE_AI_EMBEDDING_DEPLOYMENT_NAME']}' exists", failures)
    except Exception as error:  # noqa: BLE001 - surface the real Azure error
        check(False, f"Foundry project call failed: {error}", failures)

    try:
        from azure.storage.blob import BlobServiceClient

        account = env["AZURE_STORAGE_ACCOUNT_NAME"]
        service = BlobServiceClient(f"https://{account}.blob.core.windows.net", credential=credential)
        existing = {container.name for container in service.list_containers()}
        for key in ("AZURE_DOCUMENTS_CONTAINER_NAME", "AZURE_QUARANTINE_CONTAINER_NAME"):
            check(env[key] in existing, f"blob container '{env[key]}' reachable keyless", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"blob keyless call failed: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env()

    print("== Module 1 checkpoint: document-workflow foundation ==")
    verify_structure(env, failures)

    if args.offline:
        print("\n(offline mode: skipped live Azure checks)")
    elif not failures:
        verify_live(env, failures)
    else:
        print("\nSkipping live checks until the environment contract is complete.")

    return finish(1, "foundation is provisioned and keyless", failures)


if __name__ == "__main__":
    sys.exit(main())
