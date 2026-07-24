#!/usr/bin/env python3
"""Module 3 checkpoint — prove retrieval works before anything is built on top of it.

Runs the golden question set against the knowledge base and asserts three things that a
naive smoke test misses:
  * answerable cases retrieve the expected source document
  * refusal cases retrieve nothing to ground on
  * the recency case retrieves the current service notice, not the superseded one

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/verify_retrieval.py \
        --knowledge-base "$AZURE_KNOWLEDGE_BASE_NAME"

Offline/structure-only (no Azure calls):
    python3 .../verify_retrieval.py --offline
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import check, load_env, load_golden_cases, verify_golden_set  # noqa: E402

REQUIRED_ENV = ("AZURE_SEARCH_ENDPOINT",)
SUPERSEDED_CITATION = "SVC-ALPINE-2026-01-28"


def retrieve(client: Any, question: str) -> str:
    from azure.search.documents.knowledgebases.models import (
        KnowledgeBaseMessage,
        KnowledgeBaseMessageTextContent,
        KnowledgeBaseRetrievalRequest,
    )

    request = KnowledgeBaseRetrievalRequest(
        messages=[
            KnowledgeBaseMessage(
                role="user",
                content=[KnowledgeBaseMessageTextContent(text=question)],
            )
        ]
    )
    result = client.retrieve(request)
    if not result.response:
        return ""
    return result.response[0].content[0].text or ""


def verify_live(env: dict[str, str], knowledge_base: str, cases: list[dict[str, Any]], failures: list[str]) -> None:
    try:
        from azure.identity import DefaultAzureCredential
        from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
    except ImportError as error:
        check(
            False,
            f"SDK import failed ({error}). Install: pip install --pre azure-search-documents azure-identity",
            failures,
        )
        return

    client = KnowledgeBaseRetrievalClient(
        endpoint=env["AZURE_SEARCH_ENDPOINT"],
        knowledge_base_name=knowledge_base,
        credential=DefaultAzureCredential(),
    )

    for case in cases:
        try:
            text = retrieve(client, case["question"])
        except Exception as error:  # noqa: BLE001 - surface the real Azure error
            check(False, f"{case['id']}: retrieve failed: {error}", failures)
            continue

        if case.get("expected_behavior") == "answer":
            missing = [c for c in case.get("expected_citations", []) if c not in text]
            check(not missing, f"{case['id']}: retrieved expected source(s) {case['expected_citations']}", failures)
            if any("SVC-ALPINE" in c for c in case.get("expected_citations", [])):
                check(
                    SUPERSEDED_CITATION not in text,
                    f"{case['id']}: superseded notice {SUPERSEDED_CITATION} was not surfaced",
                    failures,
                )
        else:
            # A refusal case must not find grounding material. Anything retrieved here
            # becomes an answer the assistant should never have been able to give.
            check(
                not text.strip(),
                f"{case['id']}: retrieved nothing to ground a refusal case on",
                failures,
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    parser.add_argument(
        "--knowledge-base",
        default=os.environ.get("AZURE_KNOWLEDGE_BASE_NAME", "grounding-kb"),
    )
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env(REQUIRED_ENV)
    cases = load_golden_cases()

    print("== Module 3 checkpoint: retrieval over approved content ==")
    verify_golden_set(cases, failures)

    if args.offline:
        print("\n(offline mode: skipped environment and live retrieval checks)")
    else:
        for key in REQUIRED_ENV:
            check(bool(env.get(key)), f"{key} is set", failures)
        if failures:
            print("\nSkipping live retrieval until the golden set and environment are complete.")
        else:
            verify_live(env, args.knowledge_base, cases, failures)

    if failures:
        print(f"\n❌ Module 3 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    answerable = sum(1 for case in cases if case.get("expected_behavior") == "answer")
    print(
        f"\n✅ Module 3 checkpoint PASS — {answerable}/{answerable} golden questions "
        "retrieved the expected source"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
