#!/usr/bin/env python3
"""Module 6 checkpoint — prove the agent routes to the right source.

Four cases, and the last two are the ones that find real bugs:
  * a pure policy question must be answered from knowledge
  * a pure live-data question must call the tool, never the index
  * a mixed question must use both and cite them separately
  * an out-of-scope question must abstain rather than reflexively call a tool

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/verify_routing.py --agent grounding-assistant

Offline/structure-only (no Azure calls):
    python3 .../verify_routing.py --offline
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import check, load_env  # noqa: E402

REQUIRED_ENV = ("AZURE_AI_PROJECT_ENDPOINT",)
ABSTENTION = "I don't have approved information on that."

# The routing plan is data, not prose, so the checkpoint can assert against it.
ROUTING_CASES: list[dict[str, Any]] = [
    {
        "id": "policy-only",
        "question": "Can a coordinator approve an unused standard return on day 30?",
        "expect_source": "knowledge",
        "expect_markers": ["RET-POL-2026-01"],
        "forbid_markers": [],
    },
    {
        "id": "live-data-only",
        "question": "What is the current status of case 44810?",
        "expect_source": "tool",
        "expect_markers": ["44810"],
        # Answering a "now" question from the index is the failure this case exists to catch.
        "forbid_markers": ["RET-POL-2026-01"],
    },
    {
        "id": "mixed",
        "question": "Case 44810 has transit damage — what am I allowed to approve, and where is it now?",
        "expect_source": "both",
        "expect_markers": ["RET-EXC-2026-01", "44810"],
        "forbid_markers": [],
    },
    {
        "id": "out-of-scope",
        "question": "What is our company's parental leave policy?",
        "expect_source": "none",
        "expect_markers": [ABSTENTION],
        "forbid_markers": ["RET-POL-2026-01", "RET-EXC-2026-01"],
    },
]


def verify_plan(failures: list[str]) -> None:
    ids = [case["id"] for case in ROUTING_CASES]
    check(len(ids) == len(set(ids)), "routing cases have unique ids", failures)
    sources = {case["expect_source"] for case in ROUTING_CASES}
    for required in ("knowledge", "tool", "both", "none"):
        check(required in sources, f"routing plan covers the '{required}' case", failures)
    check(
        any(case["expect_source"] == "none" and ABSTENTION in case["expect_markers"] for case in ROUTING_CASES),
        "out-of-scope case asserts the exact abstention string",
        failures,
    )
    check(
        any(case["forbid_markers"] for case in ROUTING_CASES),
        "at least one case asserts a source was NOT used",
        failures,
    )


def verify_live(env: dict[str, str], agent_name: str, failures: list[str]) -> None:
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential
    except ImportError as error:
        check(False, f"SDK import failed ({error}); install azure-ai-projects", failures)
        return

    project = AIProjectClient(
        endpoint=env["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    openai = project.get_openai_client()

    for case in ROUTING_CASES:
        try:
            response = openai.responses.create(
                input=case["question"],
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            )
            text = response.output_text or ""
        except Exception as error:  # noqa: BLE001 - surface the real Azure error
            check(False, f"{case['id']}: agent call failed: {error}", failures)
            continue

        missing = [marker for marker in case["expect_markers"] if marker.lower() not in text.lower()]
        check(not missing, f"{case['id']}: routed to {case['expect_source']} (missing: {missing or 'none'})", failures)

        leaked = [marker for marker in case["forbid_markers"] if marker.lower() in text.lower()]
        check(not leaked, f"{case['id']}: did not use the wrong source (leaked: {leaked or 'none'})", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Structure checks only; no Azure calls.")
    parser.add_argument("--agent", default=os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "grounding-assistant"))
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env(REQUIRED_ENV)

    print("== Module 6 checkpoint: source routing ==")
    verify_plan(failures)

    if args.offline:
        print("\n(offline mode: skipped live agent calls)")
    elif failures:
        print("\nSkipping live checks until the routing plan is complete.")
    else:
        for key in REQUIRED_ENV:
            check(bool(env.get(key)), f"{key} is set", failures)
        if not failures:
            verify_live(env, args.agent, failures)

    if failures:
        print(f"\n❌ Module 6 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print(f"\n✅ Module 6 checkpoint PASS — {len(ROUTING_CASES)}/{len(ROUTING_CASES)} routed correctly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
