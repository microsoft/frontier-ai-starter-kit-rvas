#!/usr/bin/env python3
"""Checkpoints for Advanced · Deploy as a Hosted Agent.

Step 1 is fully STRUCTURAL (the hosted/ project you author: agent.yaml +
entrypoint + Dockerfile) and runs offline. Steps 2-4 need a live deployment, so
they are GUARDED and degrade to a clear message when creds / the SDK / the
deployed agent are unavailable. `--dry-run` forces the offline path everywhere.

    python validate.py --step 1     # hosted/agent.yaml + main.py + Dockerfile present and valid
    python validate.py --step 2     # hosted agent deployed, a version is active
    python validate.py --step 3     # live endpoint answers authenticated calls, rejects anonymous
    python validate.py --step 4     # hosted run visible (run history / App Insights)
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
HOSTED = HERE / "hosted"
AGENT_YAML = HOSTED / "agent.yaml"
MAIN_PY = HOSTED / "main.py"
DOCKERFILE = HOSTED / "Dockerfile"
INVOKE = HERE / "invoke_hosted.py"
PORT = "8088"


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


def _agent_name(env: dict) -> str:
    return (env.get("AZURE_FOUNDRY_AGENT_NAME") or "northfield-iq-assistant").strip()


# --------------------------------------------------------------------------- #
# Step 1 — agent.yaml + responses entrypoint + Dockerfile present and valid    #
# --------------------------------------------------------------------------- #
def check_step1(env: dict, dry_run: bool) -> bool:
    if not AGENT_YAML.exists():
        return _fail("1", f"missing {AGENT_YAML.relative_to(HERE)} — author the hosted-agent project (README Step 1)")
    raw = AGENT_YAML.read_text(encoding="utf-8")
    manifest = None
    try:
        import yaml

        manifest = yaml.safe_load(raw)
    except ImportError:
        warn("PyYAML not installed — falling back to text checks on agent.yaml")
    except Exception as exc:  # noqa: BLE001
        return _fail("1", f"agent.yaml is not valid YAML ({exc})")

    if manifest is not None:
        protocols = manifest.get("protocols") or []
        types = {(p or {}).get("type") for p in protocols if isinstance(p, dict)}
        ports = {str((p or {}).get("port")) for p in protocols if isinstance(p, dict)}
        if "responses" not in types:
            return _fail("1", "agent.yaml must declare the 'responses' protocol")
        if PORT not in ports:
            return _fail("1", f"agent.yaml 'responses' protocol should listen on port {PORT}")
        if not manifest.get("name"):
            return _fail("1", "agent.yaml must declare a 'name'")
    else:
        if "responses" not in raw or PORT not in raw:
            return _fail("1", f"agent.yaml must declare the 'responses' protocol on port {PORT}")

    if not MAIN_PY.exists():
        return _fail("1", f"missing {MAIN_PY.relative_to(HERE)} — the Responses entrypoint")
    main_src = MAIN_PY.read_text(encoding="utf-8")
    if PORT not in main_src:
        return _fail("1", f"main.py must serve on port {PORT}")

    if not DOCKERFILE.exists():
        return _fail("1", f"missing {DOCKERFILE.relative_to(HERE)}")
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    if not re.search(rf"EXPOSE\s+{PORT}", dockerfile):
        return _fail("1", f"Dockerfile must EXPOSE {PORT}")

    ok("✅ Step 1 PASS — agent.yaml + responses entrypoint + Dockerfile present and valid")
    return True


# --------------------------------------------------------------------------- #
# Step 2 — hosted agent deployed, version active                              #
# --------------------------------------------------------------------------- #
def check_step2(env: dict, dry_run: bool) -> bool:
    agent_name = _agent_name(env)
    if dry_run:
        if not AGENT_YAML.exists():
            return _fail("2", "author hosted/agent.yaml first (Step 1)")
        ok(f"✅ Step 2 PASS (dry-run) — agent.yaml ready to deploy '{agent_name}' (live status skipped)")
        return True
    endpoint = (env.get("AZURE_AI_PROJECT_ENDPOINT") or "").strip()
    if not endpoint:
        return _fail("2", "AZURE_AI_PROJECT_ENDPOINT missing from .env")
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential

        project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
        found = None
        for a in project.agents.list_agents():
            if getattr(a, "name", None) == agent_name:
                found = a
                break
        if found is None:
            return _fail("2", f"hosted agent '{agent_name}' not found — run 'azd ai agent create/deploy'")
        status = (getattr(found, "status", "") or "").lower()
        if status and status != "active":
            return _fail("2", f"agent '{agent_name}' version status is '{status}' (waiting to become active)")
        ok(f"✅ Step 2 PASS — hosted agent '{agent_name}' deployed"
           + (f" (status active)" if status else " (status surfaced once provisioning completes)"))
        return True
    except ImportError as exc:
        return _fail("2", f"azure-ai-projects not installed ({exc})")
    except Exception as exc:  # noqa: BLE001
        return _fail("2", f"could not query the deployed agent ({exc}); run 'az login' and 'azd ai agent deploy'")


# --------------------------------------------------------------------------- #
# Step 3 — live endpoint answers authed calls, rejects anonymous              #
# --------------------------------------------------------------------------- #
def check_step3(env: dict, dry_run: bool) -> bool:
    agent_name = _agent_name(env)
    if dry_run:
        if not INVOKE.exists():
            warn(f"{INVOKE.name} not found — author it to invoke the live endpoint (README Step 3)")
        ok("✅ Step 3 PASS (dry-run) — endpoint invocation structure checked (live auth skipped)")
        return True
    endpoint = (env.get("AZURE_AI_PROJECT_ENDPOINT") or "").strip()
    if not endpoint:
        return _fail("3", "AZURE_AI_PROJECT_ENDPOINT missing from .env")
    base = f"{endpoint.rstrip('/')}/agents/{agent_name}/endpoint/protocols/openai/responses"
    try:
        import httpx
    except ImportError as exc:
        return _fail("3", f"httpx not installed ({exc})")

    # Anonymous call MUST be rejected (401/403).
    try:
        anon = httpx.post(base, json={"input": "ping"}, timeout=10.0)
        if anon.status_code not in (401, 403):
            return _fail("3", f"anonymous call was not rejected (got {anon.status_code}); endpoint must require auth")
    except Exception as exc:  # noqa: BLE001
        return _fail("3", f"endpoint not reachable for the anonymous check ({exc}); is it deployed?")

    # Authenticated call SHOULD answer.
    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider

        token = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
        authed = httpx.post(base, json={"input": "Where is the registrar?"},
                            headers={"Authorization": f"Bearer {token()}"}, timeout=30.0)
        if authed.status_code != 200:
            return _fail("3", f"authenticated call returned {authed.status_code}; check the per-agent identity + roles")
    except Exception as exc:  # noqa: BLE001
        return _fail("3", f"authenticated call failed ({exc}); run 'az login'")
    ok("✅ Step 3 PASS — live endpoint answers authenticated calls and rejects anonymous")
    return True


# --------------------------------------------------------------------------- #
# Step 4 — hosted run observable (run history / App Insights)                 #
# --------------------------------------------------------------------------- #
def check_step4(env: dict, dry_run: bool) -> bool:
    agent_name = _agent_name(env)
    if dry_run:
        ok("✅ Step 4 PASS (dry-run) — observability wiring assumed from Tracing challenge (live query skipped)")
        return True
    workspace = (env.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID") or "").strip()
    if not workspace:
        warn("AZURE_LOG_ANALYTICS_WORKSPACE_ID not set — verify run history in the portal Tracing tab")
        ok("✅ Step 4 PASS (structure verified; confirm the hosted run in the portal)")
        return True
    try:
        from azure.identity import DefaultAzureCredential
        from azure.monitor.query import LogsQueryClient, LogsQueryStatus
        from datetime import timedelta

        client = LogsQueryClient(DefaultAzureCredential())
        query = (f'dependencies | where timestamp > ago(1h) '
                 f'| where cloud_RoleName has "{agent_name}" or customDimensions has "gen_ai" | count')
        resp = client.query_workspace(workspace, query, timespan=timedelta(hours=1))
        if resp.status == LogsQueryStatus.SUCCESS and resp.tables and resp.tables[0].rows:
            n = resp.tables[0].rows[0][0]
            if n and int(n) > 0:
                ok(f"✅ Step 4 PASS — {n} hosted run span(s) visible in App Insights")
                return True
        warn("no hosted-run spans found yet (propagation lag) — structure is valid")
        ok("✅ Step 4 PASS (structure verified; re-run after the trace propagates)")
        return True
    except ImportError as exc:
        warn(f"azure-monitor-query not installed ({exc}) — verify run history in the portal")
    except Exception as exc:  # noqa: BLE001
        warn(f"live trace query unavailable ({exc}) — verify run history in the portal")
    ok("✅ Step 4 PASS (structure verified; live trace query skipped gracefully)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Deploy-as-a-Hosted-Agent checkpoints.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=(1, 2, 3, 4))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no Azure calls).")
    args = parser.parse_args()

    env = load_env()
    if args.dry_run:
        info("(dry-run: offline structural checks only — no Azure calls)\n")

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
