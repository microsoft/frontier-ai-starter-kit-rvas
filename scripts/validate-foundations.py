#!/usr/bin/env python3
"""WTH AI Hackathon — Foundations END-STATE validator (the single Path-B checkpoint).

Asserts that the Foundations end-state exists and works:

  CHECK 1  .env contract is present and populated.
  CHECK 2  Azure AI Search index exists and has documents.
  CHECK 3  The grounded agent exists (or the index is queryable as a fallback).
  CHECK 4  The agent answers a Northfield question with at least one citation
           (degrades to a direct grounded Search query if the preview agent
           surface is unavailable, so the checkpoint still proves grounding).

Exit code 0 = green (Path B teams may start Advanced challenges).
Exit code 1 = not ready.

Live Azure calls are GUARDED: missing creds/SDKs/resources produce a clear FAIL
message rather than a stack trace.

Usage:
    python scripts/validate-foundations.py
    python scripts/validate-foundations.py --question "How do I apply for financial aid?"
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

GREEN, YELLOW, RED, CYAN, RESET = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[0;36m", "\033[0m"


def ok(m: str) -> None:
    print(f"{GREEN}✅ {m}{RESET}")


def warn(m: str) -> None:
    print(f"{YELLOW}⚠  {m}{RESET}")


def bad(m: str) -> None:
    print(f"{RED}❌ {m}{RESET}")


def info(m: str) -> None:
    print(f"{CYAN}{m}{RESET}")


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_env() -> dict:
    """Load .env (simple parser) layered over the real environment."""
    env = dict(os.environ)
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip())
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Foundations end-state.")
    parser.add_argument(
        "--question",
        default="How do I apply for financial aid at Northfield?",
        help="Grounded question used for the citation check.",
    )
    args = parser.parse_args()

    env = load_env()
    failures = 0

    # ----- CHECK 1: .env contract --------------------------------------------
    info("CHECK 1 — .env contract")
    required = [
        "AZURE_SEARCH_ENDPOINT",
        "AZURE_SEARCH_INDEX_NAME",
        "AZURE_AI_PROJECT_ENDPOINT",
        "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    ]
    missing = [k for k in required if not env.get(k)]
    if missing:
        bad(f"Missing required vars: {', '.join(missing)}")
        bad("Run 'azd up' (or ./scripts/deploy.sh), then 'azd env get-values > .env'.")
        return 1
    ok(".env present with required Foundry + Search variables.")

    index_name = env["AZURE_SEARCH_INDEX_NAME"]
    search_endpoint = env["AZURE_SEARCH_ENDPOINT"]

    # ----- dependency + auth guards ------------------------------------------
    try:
        from azure.identity import DefaultAzureCredential
        from azure.search.documents import SearchClient
        from azure.search.documents.indexes import SearchIndexClient
    except ImportError as e:
        bad(f"Missing SDK ({e}). Run: pip install -r requirements.txt")
        return 1

    try:
        cred = DefaultAzureCredential()
    except Exception as e:  # noqa: BLE001
        bad(f"Could not build DefaultAzureCredential ({e}). Run: az login")
        return 1

    # ----- CHECK 2: index exists + has documents -----------------------------
    info("\nCHECK 2 — AI Search index exists and is populated")
    try:
        idx_client = SearchIndexClient(endpoint=search_endpoint, credential=cred)
        names = [i for i in idx_client.list_index_names()]
        if index_name not in names:
            bad(f"Index '{index_name}' not found. Run ./scripts/setup-foundations.sh")
            return 1
        search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=cred)
        count = search_client.get_document_count()
        if count <= 0:
            bad(f"Index '{index_name}' exists but is empty. Run ./scripts/setup-foundations.sh")
            return 1
        ok(f"Index '{index_name}' exists with {count} documents.")
    except Exception as e:  # noqa: BLE001
        bad(f"Could not query Search ({e}). Check RBAC + 'az login'.")
        return 1

    # ----- CHECK 3 + 4: grounded answer with a citation ----------------------
    info("\nCHECK 3/4 — grounded answer with a citation")
    agent_name = env.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant")
    project_endpoint = env["AZURE_AI_PROJECT_ENDPOINT"]
    answered_by_agent = False

    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=project_endpoint, credential=cred)
        # Confirm the agent exists.
        agent = None
        try:
            for a in project.agents.list_agents():
                if getattr(a, "name", None) == agent_name:
                    agent = a
                    break
        except Exception:  # noqa: BLE001
            agent = None

        if agent is not None:
            ok(f"Agent '{agent_name}' exists (id={getattr(agent, 'id', '?')}).")
            try:
                thread = project.agents.threads.create()
                project.agents.messages.create(thread_id=thread.id, role="user", content=args.question)
                run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
                msgs = list(project.agents.messages.list(thread_id=thread.id))
                text = " ".join(
                    getattr(c, "text", {}).get("value", "")
                    for m in msgs
                    for c in getattr(m, "content", [])
                    if getattr(m, "role", "") == "assistant"
                )
                has_citation = bool(text) and (
                    "[" in text or "source" in text.lower() or ".md" in text.lower()
                )
                if text:
                    answered_by_agent = True
                    if has_citation:
                        ok("Agent returned a grounded answer WITH a citation.")
                    else:
                        warn("Agent answered but no citation detected — review grounding config.")
                        failures += 1
            except Exception as e:  # noqa: BLE001
                warn(f"Agent exists but invocation surface unavailable ({e}); using Search fallback.")
        else:
            warn(f"Agent '{agent_name}' not found; using Search-grounding fallback for the checkpoint.")
    except Exception as e:  # noqa: BLE001
        warn(f"azure-ai-projects agent surface unavailable ({e}); using Search-grounding fallback.")

    # Fallback proof of grounding: the index returns a relevant, citable result.
    if not answered_by_agent:
        try:
            results = list(search_client.search(search_text=args.question, top=3))
            if results and any(r.get("source") for r in results):
                top = results[0]
                ok(f"Search grounding works — top hit cites source '{top.get('source')}'.")
            else:
                bad("Search returned no citable result for the question.")
                failures += 1
        except Exception as e:  # noqa: BLE001
            bad(f"Search fallback query failed ({e}).")
            failures += 1

    # ----- verdict -----------------------------------------------------------
    print()
    if failures == 0:
        ok("FOUNDATIONS END-STATE: PASS — Path B teams may start Advanced challenges.")
        return 0
    bad(f"FOUNDATIONS END-STATE: NOT READY ({failures} issue(s)). See messages above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
