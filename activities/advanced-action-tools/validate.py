#!/usr/bin/env python3
"""Checkpoints for Advanced · Action Tools.

    python validate.py --step 1   # provided backend reachable (REST health)
    python validate.py --step 2   # agent wiring file wires the provided REST backend as a FunctionTool
    python validate.py --step 3   # tool-approval loop implemented (no placeholders left)
    python validate.py --step 4   # end-to-end: an action round-trips through the backend
    python validate.py --all
    python validate.py --all --dry-run   # offline structural smoke (no REST calls)

Steps 1 & 4 exercise the PROVIDED backend over REST (no Azure calls). Step 4 drives the
learner's real approval-loop function with a deterministic fake Responses client, so broken
dispatch or FunctionCallOutput wiring cannot pass merely because the backend works. `--dry-run`
skips REST calls and performs structural checks. Set ACTION_API_URL in your environment. Start:
    cd ../../scripts/action-backend && uvicorn app:app --port 8080
"""
from __future__ import annotations

import argparse
import ast
import builtins
import importlib.util
import json
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv optional; .env may already be exported in the shell
    pass
import re
import sys
from pathlib import Path
from types import SimpleNamespace

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
    northfield_actions = ("create_it_ticket", "place_course_hold", "book_advising_slot")
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return _fail("2", f"{WIRING.name} is not valid Python ({exc})")
    tool_names = {
        keyword.value.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "FunctionTool"
        for keyword in node.keywords
        if keyword.arg == "name"
        and isinstance(keyword.value, ast.Constant)
        and isinstance(keyword.value.value, str)
    }
    missing = [fn for fn in northfield_actions if fn not in tool_names]
    if TRACK == "upskill" and missing:
        return _fail("2", f"declare explicit FunctionTool schemas for: {', '.join(missing)}")
    if TRACK == "customer" and tool_names.issuperset(northfield_actions):
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
    if 'type == "function_call"' not in src:
        return _fail("3", "approval loop must inspect Responses function_call items")
    if "FunctionCallOutput" not in src:
        return _fail("3", "return each approval decision with FunctionCallOutput")
    if "conversations.create" not in src or "conversation=conversation.id" not in src:
        return _fail("3", "continue the tool-call turn in one Foundry conversation")
    if "agent_reference" not in src:
        return _fail("3", "route both Responses calls through the versioned prompt agent")
    if "Approve" not in src or "input(" not in src:
        return _fail("3", "show each requested action and collect an explicit human approval")
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
    if TRACK == "customer":
        try:
            import httpx
        except ImportError:
            return _fail("4", "httpx not installed")
        print("⚠  --track customer: custom action side effects are scenario-specific; validating backend reachability only.")
        try:
            r = httpx.get(f"{API_URL}/health", headers=_headers(), timeout=5.0)
        except Exception as exc:
            return _fail("4", f"backend not reachable at {API_URL} ({exc})")
        if r.status_code != 200:
            return _fail("4", f"health endpoint returned {r.status_code}")
        print(f"✅ Step 4 PASS — customer action backend reachable at {API_URL} (manual side-effect proof required)")
        return True

    try:
        import httpx
    except ImportError:
        return _fail("4", "httpx not installed")

    payload = {"student_id": "validate_py", "summary": "checkpoint smoke ticket",
               "category": "other", "priority": "low"}

    class FakeResponses:
        def __init__(self):
            self.calls = []

        def create(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                return SimpleNamespace(
                    id="validation-response-1",
                    output=[
                        SimpleNamespace(
                            type="function_call",
                            name="create_it_ticket",
                            arguments=json.dumps(payload),
                            call_id="validation-call-1",
                        )
                    ],
                    output_text="",
                )
            return SimpleNamespace(
                id="validation-response-2",
                output=[],
                output_text="Ticket created.",
            )

    class FakeOpenAI:
        def __init__(self):
            self.responses = FakeResponses()
            self.conversations = SimpleNamespace(
                create=lambda: SimpleNamespace(id="validation-conversation-1"),
                delete=lambda **_kwargs: None,
            )

    try:
        spec = importlib.util.spec_from_file_location("agent_with_actions_validation", WIRING)
        if spec is None or spec.loader is None:
            return _fail("4", f"could not load {WIRING.name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        fake_openai = FakeOpenAI()
        original_input = builtins.input
        builtins.input = lambda _prompt="": "y"
        try:
            module.run_with_approval(
                fake_openai,
                "northfield-iq-actions",
                "Open a low-priority checkpoint ticket for validate_py.",
            )
        finally:
            builtins.input = original_input

        calls = fake_openai.responses.calls
        if len(calls) != 2:
            return _fail("4", f"approval loop made {len(calls)} Responses calls; expected 2")
        if calls[0].get("conversation") != "validation-conversation-1":
            return _fail("4", "initial request did not use the created conversation")
        continuation = calls[1]
        if continuation.get("conversation") != "validation-conversation-1":
            return _fail("4", "approval loop did not continue in the created conversation")
        outputs = continuation.get("input") or []
        output_call_id = (
            outputs[0].get("call_id")
            if outputs and isinstance(outputs[0], dict)
            else getattr(outputs[0], "call_id", None) if outputs else None
        )
        if len(outputs) != 1 or output_call_id != "validation-call-1":
            return _fail("4", "approval loop did not submit the matching FunctionCallOutput")

        listed = httpx.get(f"{API_URL}/it-tickets", headers=_headers(), timeout=10.0)
        listed.raise_for_status()
        body = listed.json()
        items = body if isinstance(body, list) else body.get("items", body.get("tickets", []))
        matches = [
            t for t in items
            if t.get("student_id") == payload["student_id"] and t.get("summary") == payload["summary"]
        ]
        if not matches:
            return _fail("4", "approved call did not create the expected backend ticket")
    except Exception as exc:
        return _fail("4", f"approval-loop round trip failed against {API_URL}: {exc}")
    tid = matches[-1].get("ticket_id") or matches[-1].get("id")
    print(f"✅ Step 4 PASS — approval loop created backend ticket {tid}")
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
