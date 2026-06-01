#!/usr/bin/env python3
"""Checkpoints for Advanced · Action Tools.

    python validate.py --step 1   # provided backend reachable (REST health)
    python validate.py --step 2   # agent wiring file attaches the MCP action tool
    python validate.py --step 3   # tool-approval loop implemented (no placeholders left)
    python validate.py --step 4   # end-to-end: an action round-trips through the backend
    python validate.py --all
    python validate.py --all --dry-run   # offline structural smoke (no REST calls)

Steps 1 & 4 exercise the PROVIDED backend over REST (no Azure calls), so a coach can
verify wiring without burning model quota. `--dry-run` skips the REST round-trips and
falls back to a structural check of the provided backend source. Set ACTION_API_URL /
ACTION_MCP_URL in your environment (defaults match .env.sample). Start the backend first:
    cd ../../scripts/action-backend && uvicorn app:app --port 8080 & python mcp_server.py &
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
BACKEND = REPO_ROOT / "scripts" / "action-backend"
WIRING = HERE / "agent_with_actions.py"
API_URL = os.environ.get("ACTION_API_URL", "http://localhost:8080").rstrip("/")
API_KEY = os.environ.get("ACTION_API_KEY", "").strip()
PLACEHOLDER = re.compile(r"<\s*PLACEHOLDER", re.IGNORECASE)


def _fail(step: str, msg: str) -> bool:
    print(f"❌ Step {step} FAIL — {msg}")
    return False


def _headers() -> dict:
    return {"x-api-key": API_KEY} if API_KEY else {}


def check_step1() -> bool:
    if DRY_RUN:
        if not (BACKEND / "app.py").exists():
            return _fail("1", f"provided backend not found at {BACKEND} (expected app.py)")
        print("✅ Step 1 PASS (dry-run) — provided backend source present (REST health skipped)")
        return True
    try:
        import httpx
    except ImportError:
        return _fail("1", "httpx not installed (pip install -r requirements.txt)")
    try:
        r = httpx.get(f"{API_URL}/health", headers=_headers(), timeout=5.0)
    except Exception as exc:
        return _fail("1", f"backend not reachable at {API_URL} — start scripts/action-backend ({exc})")
    if r.status_code != 200:
        return _fail("1", f"health endpoint returned {r.status_code}")
    print(f"✅ Step 1 PASS — Action Tools backend reachable at {API_URL}")
    return True


def check_step2() -> bool:
    if not WIRING.exists():
        return _fail("2", f"missing wiring file {WIRING.name}")
    src = WIRING.read_text(encoding="utf-8")
    if "McpTool" not in src:
        return _fail("2", "no McpTool — attach the provided MCP server as an action tool")
    if "northfield_actions" not in src:
        return _fail("2", 'server_label should be "northfield_actions" (matches the backend)')
    if "ACTION_MCP_URL" not in src:
        return _fail("2", "wire server_url to os.environ['ACTION_MCP_URL']")
    if PLACEHOLDER.search(src.split("def run_with_approval")[0]):
        return _fail("2", "tool-attach section still has a < PLACEHOLDER > — finish build_action_tool")
    print("✅ Step 2 PASS — MCP action tool attached (northfield_actions @ ACTION_MCP_URL)")
    return True


def check_step3() -> bool:
    if not WIRING.exists():
        return _fail("3", f"missing wiring file {WIRING.name}")
    src = WIRING.read_text(encoding="utf-8")
    if "RequiredMcpToolCall" not in src:
        return _fail("3", "approval loop must inspect RequiredMcpToolCall items")
    if not ("SubmitToolApprovalAction" in src or "submit_tool_outputs" in src):
        return _fail("3", "approval loop must submit decisions (SubmitToolApprovalAction / submit_tool_outputs)")
    if "ToolApproval" not in src:
        return _fail("3", "build ToolApproval(approve=...) for each tool call")
    if PLACEHOLDER.search(src):
        return _fail("3", "a < PLACEHOLDER > remains — complete the approval loop")
    print("✅ Step 3 PASS — human tool-approval loop implemented")
    return True


def check_step4() -> bool:
    if DRY_RUN:
        if not (BACKEND / "mcp_server.py").exists():
            return _fail("4", f"provided MCP server not found at {BACKEND} (expected mcp_server.py)")
        print("✅ Step 4 PASS (dry-run) — backend + MCP server source present (round-trip skipped)")
        return True
    try:
        import httpx
    except ImportError:
        return _fail("4", "httpx not installed")
    payload = {"student_id": "validate_py", "summary": "checkpoint smoke ticket",
               "category": "other", "priority": "low"}
    try:
        created = httpx.post(f"{API_URL}/it-tickets", json=payload, headers=_headers(), timeout=10.0)
        created.raise_for_status()
        ticket = created.json()
        tid = ticket.get("ticket_id") or ticket.get("id")
        if not tid:
            return _fail("4", f"create returned no ticket id: {ticket}")
        listed = httpx.get(f"{API_URL}/it-tickets", headers=_headers(), timeout=10.0)
        listed.raise_for_status()
        body = listed.json()
        items = body if isinstance(body, list) else body.get("items", body.get("tickets", []))
        if not any((t.get("ticket_id") or t.get("id")) == tid for t in items):
            return _fail("4", "created ticket not found when listing — backend state not persisting")
    except Exception as exc:
        return _fail("4", f"end-to-end action failed against {API_URL}: {exc}")
    print(f"✅ Step 4 PASS — action round-tripped through the backend (ticket {tid})")
    return True


CHECKS = {1: check_step1, 2: check_step2, 3: check_step3, 4: check_step4}

DRY_RUN = False


def main() -> int:
    global DRY_RUN
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=sorted(CHECKS))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no REST calls).")
    args = parser.parse_args()
    DRY_RUN = args.dry_run
    if DRY_RUN:
        print("(dry-run: offline structural checks only — no REST calls)\n")

    if args.all:
        ok = all(check() for check in (CHECKS[s] for s in sorted(CHECKS)))
        print("\n✅ ALL CHECKPOINTS PASS" if ok else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
        return 0 if ok else 1
    return 0 if CHECKS[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
