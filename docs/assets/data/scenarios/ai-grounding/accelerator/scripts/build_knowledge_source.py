#!/usr/bin/env python3
"""Create the Foundry IQ knowledge source and knowledge base.

Managed ingestion: the blob knowledge source generates its own data source, skillset,
indexer, and index. The permission configuration still needs implementation: the flat
blob source below does not map the fixture role labels to per-document permissions.

Current Microsoft Learn guidance:
  https://learn.microsoft.com/azure/search/agentic-knowledge-source-overview
  https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base

Requires the preview package for ACL carry-forward, query planning, and answer synthesis:
    pip install --pre azure-search-documents azure-identity

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/build_knowledge_source.py
"""
from __future__ import annotations

import argparse
import os
import sys
from _shared import check, load_env

REQUIRED_ENV = (
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_AI_FOUNDRY_ENDPOINT",
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "AZURE_AI_CHAT_MODEL_NAME",
    "AZURE_AI_EMBEDDING_DEPLOYMENT_NAME",
    "AZURE_AI_EMBEDDING_MODEL_NAME",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "AZURE_STORAGE_CONTAINER_NAME",
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_RESOURCE_GROUP",
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
                # Unresolved: flat Blob Storage uses RBAC scopes, not per-file user/group ACLs.
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
        retrieval_instructions=RETRIEVAL_INSTRUCTIONS.replace(DEFAULT_KNOWLEDGE_SOURCE, source_name),
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
    parser.add_argument("--knowledge-source", default=DEFAULT_KNOWLEDGE_SOURCE)
    parser.add_argument("--knowledge-base", default=os.environ.get("AZURE_KNOWLEDGE_BASE_NAME", DEFAULT_KNOWLEDGE_BASE))
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env(REQUIRED_ENV)

    print("== Building the knowledge source and knowledge base ==")
    for key in REQUIRED_ENV:
        check(bool(env.get(key)), f"{key} is set", failures)
    if failures:
        print("\nComplete the environment contract before running this against Azure.")
        return 1

    build(env, args.knowledge_source, args.knowledge_base, failures)

    if failures:
        print(f"\nBuild failed ({len(failures)} issue(s)):")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(
        f"\nKnowledge source '{args.knowledge_source}' and knowledge base '{args.knowledge_base}' are configured.\n"
        "Ingestion runs asynchronously — give the indexer a few minutes before you query."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
