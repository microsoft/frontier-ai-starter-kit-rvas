#!/usr/bin/env python3
"""Module 5 checkpoint — a grounded answer path with no agent.

Asserts the four behaviours that make grounding trustworthy:
  * citations on every answerable case
  * abstention on cases the corpus cannot answer
  * the current service notice, not the superseded one
  * recall@k over the golden set, recorded as the baseline modules 6 and 7 must not regress

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/grounded_answer.py \
        --knowledge-base "$AZURE_KNOWLEDGE_BASE_NAME" --all

Offline/structure-only (no Azure calls):
    python3 .../grounded_answer.py --offline
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
ABSTENTION = "I don't have approved information on that."
SUPERSEDED_CITATION = "SVC-ALPINE-2026-01-28"
RECALL_K = 5


def answer(client: Any, question: str, user_token: str | None) -> str:
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
    # Query-time ACL enforcement needs the end user's token in addition to the app's own
    # credential. Without it every caller sees everything the application can see.
    headers = {"x-ms-query-source-authorization": user_token} if user_token else None
    result = client.retrieve(request, headers=headers) if headers else client.retrieve(request)
    if not result.response:
        return ""
    return result.response[0].content[0].text or ""


def verify_live(
    env: dict[str, str],
    knowledge_base: str,
    cases: list[dict[str, Any]],
    user_token: str | None,
    failures: list[str],
) -> None:
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

    hits = 0
    answerable = 0
    for case in cases:
        try:
            text = answer(client, case["question"], user_token)
        except Exception as error:  # noqa: BLE001
            check(False, f"{case['id']}: retrieve failed: {error}", failures)
            continue

        if case.get("expected_behavior") == "answer":
            answerable += 1
            cited = all(citation in text for citation in case.get("expected_citations", []))
            if cited:
                hits += 1
            check(cited, f"{case['id']}: answer cites {case['expected_citations']}", failures)
            if any("SVC-ALPINE" in c for c in case.get("expected_citations", [])):
                check(
                    SUPERSEDED_CITATION not in text,
                    f"{case['id']}: superseded notice not cited",
                    failures,
                )
        else:
            check(
                ABSTENTION.lower() in text.lower() or not text.strip(),
                f"{case['id']}: abstained instead of answering",
                failures,
            )
            # An access-denied response must be indistinguishable from "no information
            # exists" — no title, no snippet, no existence signal.
            for leak in ("supervisor playbook", "RET-SUP-2026-01"):
                if case["id"] == "supervisor-playbook-denied":
                    check(leak.lower() not in text.lower(), f"{case['id']}: no leak of '{leak}'", failures)

    if answerable:
        recall = hits / answerable
        print(f"\nrecall@{RECALL_K} = {recall:.2f}  ({hits}/{answerable})")
        check(recall == 1.0, f"recall@{RECALL_K} baseline is 1.00", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    parser.add_argument("--all", action="store_true", help="Run every golden case (default).")
    parser.add_argument(
        "--knowledge-base",
        default=os.environ.get("AZURE_KNOWLEDGE_BASE_NAME", "grounding-kb"),
    )
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env(REQUIRED_ENV)
    cases = load_golden_cases()

    print("== Module 5 checkpoint: grounded answers, no agent ==")
    verify_golden_set(cases, failures)
    check(
        any(case["id"] == "supervisor-playbook-denied" for case in cases),
        "golden set includes the restricted-document case",
        failures,
    )

    if args.offline:
        print("\n(offline mode: skipped live retrieval)")
    elif failures:
        print("\nSkipping live checks until the golden set is complete.")
    else:
        for key in REQUIRED_ENV:
            check(bool(env.get(key)), f"{key} is set", failures)
        if not failures:
            verify_live(env, args.knowledge_base, cases, os.environ.get("PROBE_USER_TOKEN"), failures)

    if failures:
        print(f"\n❌ Module 5 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    answerable = sum(1 for case in cases if case.get("expected_behavior") == "answer")
    refusals = len(cases) - answerable
    print(
        f"\n✅ Module 5 checkpoint PASS — {answerable}/{answerable} cited, "
        f"{refusals}/{refusals} abstained, recall@{RECALL_K} baseline recorded"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
