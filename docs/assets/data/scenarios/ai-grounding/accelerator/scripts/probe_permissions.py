#!/usr/bin/env python3
"""Module 2 checkpoint — prove the permission boundary is enforced at retrieval time.

This catches the expensive failure: retrieval that looks perfect in a demo because the
caller is an administrator, then leaks on day one of the pilot.

The probe runs each query twice — once as an identity that *should* see the content, once
as an identity that should *not* — and asserts the restricted identity gets nothing back:
no content, no title, no snippet, no "this document exists" signal.

Query-time ACL enforcement in Azure AI Search needs BOTH:
  * the application's own RBAC role, sent in the Authorization header, and
  * the end-user identity, sent in the `x-ms-query-source-authorization` header.
See https://learn.microsoft.com/azure/search/search-query-access-control-rbac-enforcement

Usage:
    # Validate the probe plan without calling Azure
    python3 probe_permissions.py --offline

    # Live probe against a Foundry IQ knowledge base
    python3 probe_permissions.py --knowledge-base grounding-kb

    # Live probe against a plain search index
    python3 probe_permissions.py --index approved-content-index

The restricted identity comes from PROBE_TENANT_ID / PROBE_CLIENT_ID / PROBE_CLIENT_SECRET
(or the matching flags). Requires preview SDK packages:
    pip install --pre azure-search-documents azure-identity
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
DEFAULT_PLAN = ACCELERATOR / "permission-probe.json"
SEARCH_SCOPE = "https://search.azure.com/.default"


def load_env() -> dict[str, str]:
    env_file = ACCELERATOR / ".env"
    values: dict[str, str] = {}
    if env_file.is_file():
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    values.update(os.environ)
    return values


def load_plan(path: Path) -> dict:
    if not path.is_file():
        raise SystemExit(
            f"No probe plan at {path}. Module 2 shows the schema: a list of cases, each with "
            "id, query, expect_visible, and expect_hidden."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def validate_plan(plan: dict) -> list[str]:
    problems: list[str] = []
    cases = plan.get("cases", [])
    if not cases:
        problems.append("plan declares no cases")
    seen: set[str] = set()
    for position, case in enumerate(cases):
        label = case.get("id", f"case[{position}]")
        for field in ("id", "query", "expect_visible", "expect_hidden"):
            if field not in case:
                problems.append(f"{label}: missing '{field}'")
        if case.get("id") in seen:
            problems.append(f"{label}: duplicate case id")
        seen.add(case.get("id", ""))
        if not case.get("expect_hidden"):
            problems.append(
                f"{label}: 'expect_hidden' is empty — a probe that never expects a denial proves nothing"
            )
    return problems


def retrieve_from_knowledge_base(env, credential, user_token: str, name: str, query: str) -> str:
    """Return the raw retrieval payload as a lowercase string for leak inspection."""
    from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
    from azure.search.documents.knowledgebases.models import (
        KnowledgeBaseMessage,
        KnowledgeBaseMessageTextContent,
        KnowledgeBaseRetrievalRequest,
    )

    client = KnowledgeBaseRetrievalClient(
        endpoint=env["AZURE_SEARCH_ENDPOINT"],
        knowledge_base_name=name,
        credential=credential,
    )
    request = KnowledgeBaseRetrievalRequest(
        messages=[
            KnowledgeBaseMessage(
                role="user", content=[KnowledgeBaseMessageTextContent(text=query)]
            )
        ]
    )
    result = client.retrieve(
        request,
        headers={"x-ms-query-source-authorization": user_token},
    )
    return json.dumps(result.as_dict(), default=str).lower()


def retrieve_from_index(env, credential, user_token: str, index: str, query: str) -> str:
    from azure.search.documents import SearchClient

    client = SearchClient(
        endpoint=env["AZURE_SEARCH_ENDPOINT"], index_name=index, credential=credential
    )
    documents = list(
        client.search(
            search_text=query,
            top=10,
            headers={"x-ms-query-source-authorization": user_token},
        )
    )
    return json.dumps([dict(doc) for doc in documents], default=str).lower()


def run_live(plan: dict, env: dict[str, str], args) -> list[str]:
    from azure.identity import ClientSecretCredential, DefaultAzureCredential

    if not (args.client_id and args.client_secret and args.tenant_id):
        raise SystemExit(
            "A permission probe needs a second, lower-privileged identity. Set "
            "PROBE_TENANT_ID/PROBE_CLIENT_ID/PROBE_CLIENT_SECRET, or use --offline to validate the plan only."
        )

    app_credential = DefaultAzureCredential()
    authorized_user = DefaultAzureCredential()
    restricted_user = ClientSecretCredential(args.tenant_id, args.client_id, args.client_secret)

    authorized_token = authorized_user.get_token(SEARCH_SCOPE).token
    restricted_token = restricted_user.get_token(SEARCH_SCOPE).token

    def retrieve(user_token: str, query: str) -> str:
        if args.knowledge_base:
            return retrieve_from_knowledge_base(
                env, app_credential, user_token, args.knowledge_base, query
            )
        return retrieve_from_index(env, app_credential, user_token, args.index, query)

    failures: list[str] = []
    for case in plan["cases"]:
        label = case["id"]
        try:
            allowed_payload = retrieve(authorized_token, case["query"])
            denied_payload = retrieve(restricted_token, case["query"])
        except Exception as error:  # noqa: BLE001 — show the learner the real Azure error
            print(f"FAIL  {label}: retrieval error: {error}")
            failures.append(f"{label}: retrieval error: {error}")
            continue

        for expected in case["expect_visible"]:
            ok = expected.lower() in allowed_payload
            print(f"{'PASS ' if ok else 'FAIL '} {label}: authorized identity sees '{expected}'")
            if not ok:
                failures.append(f"{label}: authorized identity could not see '{expected}'")

        for forbidden in case["expect_hidden"]:
            leaked = forbidden.lower() in denied_payload
            print(
                f"{'FAIL ' if leaked else 'PASS '} {label}: restricted identity cannot see '{forbidden}'"
            )
            if leaked:
                failures.append(f"{label}: LEAK — restricted identity retrieved '{forbidden}'")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    surface = parser.add_mutually_exclusive_group()
    surface.add_argument("--knowledge-base", help="Foundry IQ / agentic retrieval knowledge base name.")
    surface.add_argument("--index", help="Azure AI Search index name.")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--offline", action="store_true", help="Validate the probe plan only.")
    parser.add_argument("--tenant-id", default=os.environ.get("PROBE_TENANT_ID"))
    parser.add_argument("--client-id", default=os.environ.get("PROBE_CLIENT_ID"))
    parser.add_argument("--client-secret", default=os.environ.get("PROBE_CLIENT_SECRET"))
    args = parser.parse_args()

    print("== Module 2 checkpoint: permission boundary ==")
    plan = load_plan(args.plan)

    failures = validate_plan(plan)
    for problem in failures:
        print(f"FAIL  plan: {problem}")
    if not failures:
        print(f"PASS  probe plan is well formed ({len(plan['cases'])} case(s))")

    if args.offline:
        print("\n(offline mode: plan validated, no Azure calls)")
    elif failures:
        print("\nFix the probe plan before running it against Azure.")
    else:
        if not (args.knowledge_base or args.index):
            raise SystemExit("Pass --knowledge-base or --index for a live probe.")
        failures.extend(run_live(plan, load_env(), args))

    if failures:
        print(f"\n❌ Module 2 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 2 checkpoint PASS — the permission boundary held")
    return 0


if __name__ == "__main__":
    sys.exit(main())
