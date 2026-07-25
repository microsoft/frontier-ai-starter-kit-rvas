#!/usr/bin/env python3
"""Module 8 checkpoint — prove the surface is safe to hand to real users.

The contract is deliberately surface-agnostic. The same manifest passes whether users meet the
agent in Teams, in Microsoft 365 Copilot, through your own app, or against a hosted endpoint —
only the `surface.option` line differs. That is the point: the surface stays a late, reversible
decision, and the release rules do not.

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/verify_surface.py --offline

Live probe — confirm the surface rejects an unauthenticated call:
    python3 .../verify_surface.py --endpoint https://<your-endpoint>
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import ACCELERATOR, check  # noqa: E402

MANIFEST = ACCELERATOR / "sample-data" / "surface-manifest.json"

SURFACE_OPTIONS = {
    "app-or-api",
    "m365-and-teams",
    "copilot-studio",
    "hosted-agent",
    "custom-ui",
}

AUTH_MODES = {"entra-user", "managed-identity"}

# A manifest full of "TBD" passes a naive schema check and tells a risk owner nothing.
PLACEHOLDERS = ("tbd", "todo", "n/a", "none", "someone", "tbc", "xxx", "<", "fixme")

MIN_PROSE = 20


def load_manifest(path: Path, failures: list[str]) -> dict[str, Any]:
    if not path.is_file():
        check(False, f"surface manifest exists: {path.name}", failures)
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        check(False, f"surface manifest is valid JSON ({error})", failures)
        return {}
    check(True, f"surface manifest loaded: {path.name}", failures)
    return data


def is_answered(value: Any, minimum: int = 1) -> bool:
    """A field counts as answered only if a human actually filled it in."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if len(text) < minimum:
        return False
    return not any(marker in text.lower() for marker in PLACEHOLDERS)


def verify_surface_choice(data: dict[str, Any], failures: list[str]) -> None:
    surface = data.get("surface", {})
    option = surface.get("option")
    check(
        option in SURFACE_OPTIONS,
        f"surface.option is one of {sorted(SURFACE_OPTIONS)} (got {option!r})",
        failures,
    )
    check(is_answered(surface.get("why"), MIN_PROSE), "surface.why explains the choice in a sentence", failures)
    check(is_answered(surface.get("who_can_use")), "surface.who_can_use names the pilot audience", failures)


def verify_agent_pinning(data: dict[str, Any], failures: list[str]) -> None:
    agent = data.get("agent", {})
    check(is_answered(agent.get("name")), "agent.name is set", failures)
    version = str(agent.get("pinned_version", "")).strip()
    check(
        bool(version) and version.lower() != "latest",
        f"agent.pinned_version pins a specific version (got {version or 'empty'!r})",
        failures,
    )
    # "Always use latest" means a version created during a debugging session becomes production.
    check(
        agent.get("version_selection") == "fixed",
        "agent.version_selection is 'fixed', not 'always-latest'",
        failures,
    )


def verify_auth(data: dict[str, Any], failures: list[str]) -> None:
    auth = data.get("auth", {})
    check(auth.get("mode") in AUTH_MODES, f"auth.mode is one of {sorted(AUTH_MODES)}", failures)
    check(auth.get("anonymous_access") is False, "auth.anonymous_access is false", failures)
    check(auth.get("keys_in_config") is False, "auth.keys_in_config is false — the pilot stays keyless", failures)


def verify_permission_boundary(data: dict[str, Any], failures: list[str]) -> None:
    perms = data.get("permissions", {})
    check(
        is_answered(perms.get("identity_evaluated_at_query_time")),
        "permissions.identity_evaluated_at_query_time names the identity",
        failures,
    )
    # Permission behaviour is a property of the whole system, and the surface is new.
    check(
        perms.get("reprobed_at_surface") is True,
        "permissions.reprobed_at_surface is true — the module 2 probe was re-run here",
        failures,
    )
    check(
        is_answered(perms.get("access_denied_behavior"), MIN_PROSE),
        "permissions.access_denied_behavior describes what a denied user sees",
        failures,
    )


def verify_observability(data: dict[str, Any], failures: list[str]) -> None:
    obs = data.get("observability", {})
    check(obs.get("tracing_enabled") is True, "observability.tracing_enabled is true in the deployed runtime", failures)
    check(is_answered(obs.get("destination")), "observability.destination names where traces land", failures)


def verify_rollback(data: dict[str, Any], failures: list[str]) -> None:
    rollback = data.get("rollback", {})
    check(
        is_answered(rollback.get("mechanism"), MIN_PROSE),
        "rollback.mechanism describes how you go back",
        failures,
    )
    check(is_answered(str(rollback.get("previous_version", ""))), "rollback.previous_version is retained", failures)


def verify_operations(data: dict[str, Any], failures: list[str]) -> None:
    ops = data.get("operations", {})
    # "The team" is not an owner. A name is.
    check(is_answered(ops.get("triage_owner")), "operations.triage_owner names a person", failures)
    check(
        is_answered(ops.get("how_users_report_a_bad_answer"), MIN_PROSE),
        "operations.how_users_report_a_bad_answer describes a real path",
        failures,
    )
    check(is_answered(ops.get("review_cadence")), "operations.review_cadence is set", failures)


def verify_exit_and_release(data: dict[str, Any], failures: list[str]) -> None:
    exit_plan = data.get("pilot_exit", {})
    # A pilot without an exit criterion becomes permanent unsupported infrastructure.
    check(
        is_answered(exit_plan.get("criterion"), MIN_PROSE),
        "pilot_exit.criterion states what ends the pilot",
        failures,
    )
    check(is_answered(exit_plan.get("review_date")), "pilot_exit.review_date is set", failures)

    evidence = data.get("evidence", [])
    check(
        isinstance(evidence, list) and len(evidence) >= 3,
        f"evidence lists at least 3 artifacts (got {len(evidence) if isinstance(evidence, list) else 0})",
        failures,
    )

    release = data.get("release_decision", {})
    check(
        release.get("outcome") in {"ship", "ship-with-conditions", "stop"},
        "release_decision.outcome is ship, ship-with-conditions, or stop",
        failures,
    )
    check(is_answered(release.get("approver")), "release_decision.approver names the risk owner", failures)


def verify_live(endpoint: str, failures: list[str]) -> None:
    """An unauthenticated caller must be refused. Anything else is a finding, not a pass."""
    request = urllib.request.Request(endpoint, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            check(False, f"unauthenticated request was refused (got {response.status} — the surface is open)", failures)
    except urllib.error.HTTPError as error:
        check(
            error.code in (401, 403),
            f"unauthenticated request was refused (got {error.code})",
            failures,
        )
    except urllib.error.URLError as error:
        check(False, f"could not reach {endpoint}: {error.reason}", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Contract checks only; no network calls.")
    parser.add_argument("--manifest", default=str(MANIFEST), help="Path to the surface manifest.")
    parser.add_argument("--endpoint", help="Probe this URL unauthenticated; expect 401 or 403.")
    args = parser.parse_args()

    failures: list[str] = []

    print("== Module 8 checkpoint: deployment surface ==")
    data = load_manifest(Path(args.manifest), failures)
    if data:
        verify_surface_choice(data, failures)
        verify_agent_pinning(data, failures)
        verify_auth(data, failures)
        verify_permission_boundary(data, failures)
        verify_observability(data, failures)
        verify_rollback(data, failures)
        verify_operations(data, failures)
        verify_exit_and_release(data, failures)

    if args.endpoint and not args.offline:
        print("\n-- live probe --")
        verify_live(args.endpoint, failures)
    elif not args.endpoint:
        print("\n(no --endpoint given: skipped the unauthenticated-access probe)")

    if failures:
        print(f"\n❌ Module 8 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 8 checkpoint PASS — the surface has an owner, a boundary, and a way back")
    return 0


if __name__ == "__main__":
    sys.exit(main())
