#!/usr/bin/env python3
"""Checkpoints for Advanced · Action Tools.

    python validate.py --step 1   # provided backend reachable (REST health)
    python validate.py --step 2   # agent wiring file wires the provided REST backend as a FunctionTool
    python validate.py --step 3   # tool-approval loop implemented (no placeholders left)
    python validate.py --step 4   # end-to-end: an action round-trips through the backend
    python validate.py --all
    python validate.py --all --dry-run   # offline structural smoke (no REST calls)

Steps 1 & 4 exercise the PROVIDED backend over REST (no Azure calls), so a facilitator can
verify wiring without burning model quota. `--dry-run` skips the REST round-trips and
falls back to a structural check of the provided backend source. Set ACTION_API_URL in
your environment (default matches .env.sample). Start the backend first:
    cd ../../scripts/action-backend && uvicorn app:app --port 8080
"""
from __future__ import annotations

import argparse
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv optional; .env may already be exported in the shell
    pass
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
TRACK = "upskill"


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
    if "FunctionTool" not in src:
        return _fail("2", "no FunctionTool — wrap the three action callables as a FunctionTool")
    northfield_actions = ("create_it_ticket", "place_course_hold", "book_advising_slot")
    missing = [fn for fn in northfield_actions if fn not in src]
    if TRACK == "upskill" and missing:
        return _fail("2", f"define all three action functions; missing: {', '.join(missing)}")
    if TRACK == "customer" and not missing:
        print("⚠  --track customer: default Northfield action names are still present; replace/adapt them for your workflow before demo.")
    if "ACTION_API_URL" not in src:
        return _fail("2", "wire tool execution to ACTION_API_URL (the provided REST backend)")
    if PLACEHOLDER.search(src.split("def run_with_approval")[0]):
        return _fail("2", "tool-definition section still has a < PLACEHOLDER > — finish build_action_tools")
    label = "northfield actions" if TRACK == "upskill" else "customer action tools"
    print(f"✅ Step 2 PASS — action FunctionTool defined ({label} @ ACTION_API_URL)")
    return True


def check_step3() -> bool:
    if not WIRING.exists():
        return _fail("3", f"missing wiring file {WIRING.name}")
    src = WIRING.read_text(encoding="utf-8")
    if "RequiredFunctionToolCall" not in src:
        return _fail("3", "approval loop must inspect RequiredFunctionToolCall items")
    if "submit_tool_outputs" not in src:
        return _fail("3", "approval loop must submit decisions via submit_tool_outputs")
    if "ToolOutput" not in src:
        return _fail("3", "build ToolOutput(tool_call_id=..., output=...) for each decision")
    if PLACEHOLDER.search(src):
        return _fail("3", "a < PLACEHOLDER > remains — complete the approval loop")
    print("✅ Step 3 PASS — human tool-approval loop implemented")
    return True


def check_step4() -> bool:
    if DRY_RUN:
        if not (BACKEND / "app.py").exists():
            return _fail("4", f"provided REST backend not found at {BACKEND} (expected app.py)")
        print("✅ Step 4 PASS (dry-run) — provided REST backend source present (round-trip skipped)")
        return True
    try:
        import httpx
    except ImportError:
        return _fail("4", "httpx not installed")
    if TRACK == "customer":
        print("⚠  --track customer: custom action side effects are scenario-specific; validating backend reachability only.")
        try:
            r = httpx.get(f"{API_URL}/health", headers=_headers(), timeout=5.0)
        except Exception as exc:
            return _fail("4", f"backend not reachable at {API_URL} ({exc})")
        if r.status_code != 200:
            return _fail("4", f"health endpoint returned {r.status_code}")
        print(f"✅ Step 4 PASS — customer action backend reachable at {API_URL} (manual side-effect proof required)")
        return True
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
    global DRY_RUN, TRACK
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=sorted(CHECKS))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no REST calls).")
    parser.add_argument("--track", choices=("upskill", "customer"), default="upskill",
                        help="upskill = Northfield reference; customer = your own scenario "
                             "(relaxes the Northfield corpus assumption, expects --question).")
    args = parser.parse_args()
    DRY_RUN = args.dry_run
    TRACK = args.track
    if DRY_RUN:
        print("(dry-run: offline structural checks only — no REST calls)\n")
    if TRACK == "customer":
        print("(track: customer — validating YOUR scenario, not Northfield)\n")

    if args.all:
        ok = all(check() for check in (CHECKS[s] for s in sorted(CHECKS)))
        print("\n✅ ALL CHECKPOINTS PASS" if ok else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
        return 0 if ok else 1
    return 0 if CHECKS[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
