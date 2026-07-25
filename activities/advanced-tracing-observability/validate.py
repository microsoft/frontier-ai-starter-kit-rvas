#!/usr/bin/env python3
"""Checkpoints for Advanced · Tracing & Observability.

The artifacts in this activity are mostly files you author (trace_setup.py,
traced_run.py, correlate.kql), so most checks are STRUCTURAL and run fully
offline. The one live check (Step 2 — spans actually landed in App Insights)
is GUARDED and degrades to a clear message when creds / the SDK / a workspace
are unavailable. `--dry-run` forces the offline path everywhere (no network).

    python validate.py --step 1     # trace_setup.py wires instrumentation (env flags before instrument())
    python validate.py --step 2     # traced_run.py emits a run / a GenAI span is queryable
    python validate.py --step 3     # message-content capture enabled (model+retrieval spans readable)
    python validate.py --step 4     # correlate.kql present and correlates one operation_Id end-to-end
    python validate.py --all
    python validate.py --all --dry-run
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

GREEN, YELLOW, RED, CYAN, RESET = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[0;36m", "\033[0m"

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
TRACE_SETUP = HERE / "trace_setup.py"
TRACED_RUN = HERE / "traced_run.py"
CORRELATE = HERE / "correlate.kql"
LAST_RESPONSE_ID = HERE / ".last-response-id"

ENABLE_FLAG = "AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING"
CAPTURE_FLAG = "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"


def ok(m: str) -> None:
    print(f"{GREEN}{m}{RESET}")


def warn(m: str) -> None:
    print(f"{YELLOW}⚠  {m}{RESET}")


def info(m: str) -> None:
    print(f"{CYAN}{m}{RESET}")


def _fail(step: str, msg: str) -> bool:
    print(f"{RED}❌ Step {step} FAIL — {msg}{RESET}")
    return False


def load_env() -> dict:
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


def _flag_set_line(src: str, flag: str) -> int | None:
    for i, line in enumerate(src.splitlines()):
        if flag in line and "=" in line and "os.environ" in line:
            return i
    return None


# --------------------------------------------------------------------------- #
# Step 1 — instrumentation wired, env flags set before instrument()            #
# --------------------------------------------------------------------------- #
def check_step1(env: dict, dry_run: bool) -> bool:
    if not TRACE_SETUP.exists():
        return _fail("1", f"missing {TRACE_SETUP.name} — author it (see README Step 1)")
    src = TRACE_SETUP.read_text(encoding="utf-8")
    enable_at = _flag_set_line(src, ENABLE_FLAG)
    capture_at = _flag_set_line(src, CAPTURE_FLAG)
    if enable_at is None or capture_at is None:
        return _fail("1", f"both {ENABLE_FLAG} and {CAPTURE_FLAG} must be set via os.environ in {TRACE_SETUP.name}")
    instrument_at = next(
        (i for i, line in enumerate(src.splitlines()) if "AIProjectInstrumentor().instrument()" in line),
        None,
    )
    if instrument_at is None:
        return _fail("1", "enable client-side instrumentation with AIProjectInstrumentor().instrument()")
    if enable_at > instrument_at or capture_at > instrument_at:
        return _fail("1", "set both tracing flags before AIProjectInstrumentor().instrument()")
    if "configure_azure_monitor" not in src:
        return _fail("1", "wire spans to App Insights with configure_azure_monitor(...)")
    if not dry_run and not (env.get("APPLICATIONINSIGHTS_CONNECTION_STRING") or "get_application_insights_connection_string" in src):
        warn("APPLICATIONINSIGHTS_CONNECTION_STRING not in .env and no runtime resolve() found — "
             "the connection must be resolvable at run time")
    ok("✅ Step 1 PASS — instrumentation wired, env flags set before instrument()")
    return True


# --------------------------------------------------------------------------- #
# Step 2 — a run emitted >= 1 GenAI span                                       #
# --------------------------------------------------------------------------- #
def check_step2(env: dict, dry_run: bool) -> bool:
    if not TRACED_RUN.exists():
        return _fail("2", f"missing {TRACED_RUN.name} — author it (see README Step 2)")
    src = TRACED_RUN.read_text(encoding="utf-8")
    if "enable_tracing" not in src:
        return _fail("2", f"{TRACED_RUN.name} must import/call enable_tracing() from trace_setup first")
    if "responses.create" not in src:
        return _fail("2", "drive the agent with responses.create so a span is emitted")
    if "agent_reference" not in src:
        return _fail("2", "route the traced call through the versioned agent with agent_reference")
    if ".last-response-id" not in src or "response.id" not in src:
        return _fail("2", "persist response.id to .last-response-id so the live check can query that run")
    if dry_run:
        ok("✅ Step 2 PASS (dry-run) — traced_run.py calls enable_tracing() then drives the agent")
        return True

    # Live: query App Insights for the exact response emitted by traced_run.py.
    workspace = env.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID", "")
    if not workspace:
        return _fail("2", "AZURE_LOG_ANALYTICS_WORKSPACE_ID is required for the live span query; "
                          "use --dry-run for a structural-only check")
    if not LAST_RESPONSE_ID.exists():
        return _fail("2", "missing .last-response-id; run traced_run.py and wait for telemetry first")
    response_id = LAST_RESPONSE_ID.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", response_id):
        return _fail("2", ".last-response-id is empty or malformed; rerun traced_run.py")
    try:
        from azure.identity import DefaultAzureCredential
        from azure.monitor.query import LogsQueryClient, LogsQueryStatus
        from datetime import timedelta

        client = LogsQueryClient(DefaultAzureCredential())
        query = (
            "dependencies | where timestamp > ago(1h) "
            f'| where tostring(customDimensions) has "{response_id}" '
            "| count"
        )
        resp = client.query_workspace(workspace, query, timespan=timedelta(hours=1))
        if resp.status == LogsQueryStatus.SUCCESS and resp.tables and resp.tables[0].rows:
            n = resp.tables[0].rows[0][0]
            if n and int(n) > 0:
                ok(f"✅ Step 2 PASS — {n} span(s) found for response {response_id}")
                return True
        return _fail("2", f"no spans found for response {response_id}; wait for telemetry "
                          "propagation and retry")
    except ImportError as exc:
        return _fail("2", f"azure-monitor-query not installed ({exc})")
    except Exception as exc:  # noqa: BLE001
        return _fail("2", f"live span query failed ({exc}); verify Azure login, workspace RBAC, and telemetry")


# --------------------------------------------------------------------------- #
# Step 3 — message-content capture enabled (spans expose prompt/answer)        #
# --------------------------------------------------------------------------- #
def check_step3(env: dict, dry_run: bool) -> bool:
    if not TRACE_SETUP.exists():
        return _fail("3", f"missing {TRACE_SETUP.name}")
    src = TRACE_SETUP.read_text(encoding="utf-8")
    if _flag_set_line(src, CAPTURE_FLAG) is None:
        return _fail("3", f"{CAPTURE_FLAG} must be enabled so model/retrieval spans expose prompt + answer")
    ok("✅ Step 3 PASS — message-content capture enabled; span tree is readable in the Tracing tab")
    return True


# --------------------------------------------------------------------------- #
# Step 4 — correlate.kql correlates one operation end-to-end                   #
# --------------------------------------------------------------------------- #
def check_step4(env: dict, dry_run: bool) -> bool:
    if not CORRELATE.exists():
        return _fail("4", f"missing {CORRELATE.name} — save your end-to-end correlation query")
    kql = CORRELATE.read_text(encoding="utf-8").lower()
    if "operation_id" not in kql:
        return _fail("4", "correlate.kql must correlate by operation_Id (one request, every span)")
    if not any(tbl in kql for tbl in ("dependencies", "union", "requests", "traces")):
        return _fail("4", "correlate.kql should query the span tables (dependencies / requests / traces)")
    ok("✅ Step 4 PASS — correlate.kql correlates one operation_Id across the span tables")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Tracing & Observability checkpoints.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=(1, 2, 3, 4))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no Azure calls).")
    parser.add_argument("--track", choices=("reference", "customer"), default="reference",
                        help="reference = sample organization reference; customer = your own scenario "
                             "(relaxes the sample organization corpus assumption, expects --question).")
    args = parser.parse_args()

    env = load_env()
    if args.dry_run:
        info("(dry-run: offline structural checks only — no Azure calls)\n")
    if args.track == "customer":
        info("(track: customer — validating YOUR scenario, not sample organization)\n")

    checks = {
        1: lambda: check_step1(env, args.dry_run),
        2: lambda: check_step2(env, args.dry_run),
        3: lambda: check_step3(env, args.dry_run),
        4: lambda: check_step4(env, args.dry_run),
    }

    if args.all:
        results = [checks[n]() for n in (1, 2, 3, 4)]
        if all(results):
            ok("\n✅ ALL CHECKPOINTS PASS" + (" (dry-run)" if args.dry_run else ""))
            return 0
        print(f"{RED}\n❌ ONE OR MORE CHECKPOINTS FAILED{RESET}")
        return 1
    return 0 if checks[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
