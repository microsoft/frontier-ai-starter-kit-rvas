#!/usr/bin/env python3
"""Module 3 — create the Foundry IQ knowledge source and knowledge base.

Managed ingestion: the blob knowledge source generates its own data source, skillset,
indexer, and index. ACL carry-forward is enabled so module 2's permission boundary can be
enforced at query time.

Current Microsoft Learn guidance:
  https://learn.microsoft.com/azure/search/agentic-knowledge-source-overview
  https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base

Requires the preview package for ACL carry-forward, query planning, and answer synthesis:
    pip install --pre azure-search-documents azure-identity

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/build_knowledge_source.py

Offline/structure-only (no Azure calls):
    python3 .../build_knowledge_source.py --offline
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
ENV_FILE = ACCELERATOR / ".env"

REQUIRED_ENV = (
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "AZURE_AI_CHAT_MODEL_NAME",
    "AZURE_AI_EMBEDDING_DEPLOYMENT_NAME",
    "AZURE_AI_EMBEDDING_MODEL_NAME",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "AZURE_STORAGE_CONTAINER_NAME",
)

DEFAULT_KNOWLEDGE_SOURCE = "approved-content-ks"
DEFAULT_KNOWLEDGE_BASE = "grounding-kb"

RETRIEVAL_INSTRUCTIONS = (
    "Use approved-content-ks for questions about returns policy, exceptions, and published "
    "service notices. When two notices cover the same subject, prefer the one with the most "
    "recent effective date."
)

ANSWER_INSTRUCTIONS = (
    "Answer only from retrieved documents and cite the document id for every claim. "
    "Do not infer, combine rules into new rules, or use general knowledge. "
    "If the retrieved documents do not contain the answer, reply exactly: "
    '"I don\'t have approved information on that."'
)


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    for key in REQUIRED_ENV:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def check(passed: bool, message: str, failures: list[str]) -> bool:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)
    return passed


def verify_structure(env: dict[str, str], failures: list[str], require_env: bool) -> None:
    if require_env:
        for key in REQUIRED_ENV:
            check(bool(env.get(key)), f"{key} is set", failures)

    # The two instruction blocks are the answer contract module 5 asserts against.
    check("cite the document id" in ANSWER_INSTRUCTIONS, "answer instructions require citations", failures)
    check("Do not infer" in ANSWER_INSTRUCTIONS, "answer instructions forbid inference", failures)
    check(
        "I don't have approved information on that." in ANSWER_INSTRUCTIONS,
        "answer instructions specify an exact abstention string",
        failures,
    )
    check(
        "most recent effective date" in RETRIEVAL_INSTRUCTIONS,
        "retrieval instructions state a recency preference",
        failures,
    )


def build(env: dict[str, str], source_name: str, base_name: str, failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.search.documents.indexes import SearchIndexClient
        from azure.search.documents.indexes.models import (
            AzureBlobKnowledgeSource,
            AzureBlobKnowledgeSourceParameters,
            AzureOpenAIVectorizerParameters,
            KnowledgeBase,
            KnowledgeBaseAzureOpenAIModel,
            KnowledgeSourceAzureOpenAIVectorizer,
            KnowledgeSourceContentExtractionMode,
            KnowledgeSourceIngestionParameters,
            KnowledgeSourceReference,
        )
    except ImportError as error:
        check(
            False,
            f"SDK import failed ({error}). Install the preview package: "
            "pip install --pre azure-search-documents azure-identity",
            failures,
        )
        return

    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(endpoint=env["AZURE_SEARCH_ENDPOINT"], credential=credential)

    chat_params = AzureOpenAIVectorizerParameters(
        resource_url=env["AZURE_AI_FOUNDRY_ENDPOINT"],
        deployment_name=env["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        model_name=env["AZURE_AI_CHAT_MODEL_NAME"],
    )
    embedding_params = AzureOpenAIVectorizerParameters(
        resource_url=env["AZURE_AI_FOUNDRY_ENDPOINT"],
        deployment_name=env["AZURE_AI_EMBEDDING_DEPLOYMENT_NAME"],
        model_name=env["AZURE_AI_EMBEDDING_MODEL_NAME"],
    )

    # Keyless: the search service managed identity reads the container, so the connection
    # string carries the resource id rather than an account key.
    blob_connection = (
        f"ResourceId=/subscriptions/{env['AZURE_SUBSCRIPTION_ID']}"
        f"/resourceGroups/{env['AZURE_RESOURCE_GROUP']}"
        f"/providers/Microsoft.Storage/storageAccounts/{env['AZURE_STORAGE_ACCOUNT_NAME']};"
    )

    knowledge_source = AzureBlobKnowledgeSource(
        name=source_name,
        azure_blob_parameters=AzureBlobKnowledgeSourceParameters(
            connection_string=blob_connection,
            container_name=env["AZURE_STORAGE_CONTAINER_NAME"],
            is_adls_gen2=False,
            ingestion_parameters=KnowledgeSourceIngestionParameters(
                chat_completion_model=KnowledgeBaseAzureOpenAIModel(
                    azure_open_ai_parameters=chat_params
                ),
                embedding_model=KnowledgeSourceAzureOpenAIVectorizer(
                    azure_open_ai_parameters=embedding_params
                ),
                content_extraction_mode=KnowledgeSourceContentExtractionMode.MINIMAL,
                # ACL carry-forward. Without this, module 2's permission boundary cannot be
                # enforced at query time no matter what headers you send.
                ingestion_permission_options=["user_ids", "group_ids"],
            ),
        ),
    )

    try:
        # Ordering is enforced by the service: the source must exist before the base.
        index_client.create_or_update_knowledge_source(knowledge_source)
        check(True, f"knowledge source '{source_name}' created or updated", failures)
    except Exception as error:  # noqa: BLE001 - surface the real Azure error
        check(False, f"knowledge source create failed: {error}", failures)
        return

    knowledge_base = KnowledgeBase(
        name=base_name,
        knowledge_sources=[KnowledgeSourceReference(name=source_name)],
        retrieval_instructions=RETRIEVAL_INSTRUCTIONS,
        answer_instructions=ANSWER_INSTRUCTIONS,
        output_mode="answerSynthesis",
        models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=chat_params)],
    )

    try:
        index_client.create_or_update_knowledge_base(knowledge_base)
        check(True, f"knowledge base '{base_name}' created or updated", failures)
    except Exception as error:  # noqa: BLE001
        check(False, f"knowledge base create failed: {error}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    parser.add_argument("--knowledge-source", default=DEFAULT_KNOWLEDGE_SOURCE)
    parser.add_argument("--knowledge-base", default=os.environ.get("AZURE_KNOWLEDGE_BASE_NAME", DEFAULT_KNOWLEDGE_BASE))
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env()

    print("== Module 3: build the knowledge source and knowledge base ==")
    verify_structure(env, failures, require_env=not args.offline)

    if args.offline:
        print("\n(offline mode: skipped environment checks and Azure calls)")
    elif failures:
        print("\nSkipping Azure calls until the environment contract is complete.")
    else:
        for key in ("AZURE_SUBSCRIPTION_ID", "AZURE_RESOURCE_GROUP"):
            if not env.get(key):
                env[key] = os.environ.get(key, "")
                check(bool(env[key]), f"{key} is set (needed for the keyless blob connection)", failures)
        if not failures:
            build(env, args.knowledge_source, args.knowledge_base, failures)

    if failures:
        print(f"\n❌ Module 3 build FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 3 build OK — knowledge source and knowledge base are configured")
    return 0


if __name__ == "__main__":
    sys.exit(main())
