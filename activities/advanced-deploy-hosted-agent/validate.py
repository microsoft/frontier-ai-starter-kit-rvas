#!/usr/bin/env python3
"""Checkpoints for Advanced · Deploy as a Hosted Agent.

Step 1 is fully STRUCTURAL (the hosted/ project you scaffold: azure.yaml +
agent source + Dockerfile) and runs offline. Steps 2-4 need a live deployment, so
they are GUARDED and degrade to a clear message when creds / the SDK / the
deployed agent are unavailable. `--dry-run` forces the offline path everywhere.

    python validate.py --step 1     # hosted/azure.yaml + agent source + Dockerfile are valid
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
import sys
from pathlib import Path

GREEN, YELLOW, RED, CYAN, RESET = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[0;36m", "\033[0m"

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
HOSTED = HERE / "hosted"
AZURE_YAML = HOSTED / "azure.yaml"
INVOKE = HERE / "invoke_hosted.py"


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


def _agent_name(env: dict, track: str) -> str:
    name = (env.get("AZURE_FOUNDRY_AGENT_NAME") or "northfield-iq-assistant").strip()
    if track == "customer" and name == "northfield-iq-assistant":
        warn("--track customer: AZURE_FOUNDRY_AGENT_NAME is not set, so the Northfield default is being used.")
    return name


# --------------------------------------------------------------------------- #
# Step 1 — unified azure.yaml + hosted source project present and valid         #
# --------------------------------------------------------------------------- #
def check_step1(env: dict, dry_run: bool, track: str) -> bool:
    if not AZURE_YAML.exists():
        return _fail("1", f"missing {AZURE_YAML.relative_to(HERE)} — run 'azd ai agent init' (README Step 1)")
    raw = AZURE_YAML.read_text(encoding="utf-8")
    manifest = None
    try:
        import yaml

        manifest = yaml.safe_load(raw)
    except ImportError:
        warn("PyYAML not installed — falling back to text checks on azure.yaml")
    except Exception as exc:  # noqa: BLE001
        return _fail("1", f"azure.yaml is not valid YAML ({exc})")

    if manifest is not None:
        services = manifest.get("services") or {}
        agents = [
            service for service in services.values()
            if isinstance(service, dict) and service.get("host") == "azure.ai.agent"
        ]
        if not agents:
            return _fail("1", "azure.yaml must declare a service with host: azure.ai.agent")
        agent_service = agents[0]
        if agent_service.get("kind") != "hosted":
            return _fail("1", "the azure.ai.agent service must declare kind: hosted")
        protocols = agent_service.get("protocols") or []
        protocol_names = {(p or {}).get("protocol") for p in protocols if isinstance(p, dict)}
        if "responses" not in protocol_names:
            return _fail("1", "the hosted agent service must declare protocol: responses")
        response_versions = {
            str((p or {}).get("version"))
            for p in protocols
            if isinstance(p, dict) and (p or {}).get("protocol") == "responses"
        }
        if "2.0.0" not in response_versions:
            return _fail("1", "the Responses protocol version must be 2.0.0")
        project_dir = HOSTED / str(agent_service.get("project") or "")
        if not agent_service.get("project") or not project_dir.is_dir():
            return _fail("1", "the hosted agent service 'project' directory does not exist")
        if not (project_dir / "Dockerfile").exists():
            return _fail("1", f"missing {(project_dir / 'Dockerfile').relative_to(HERE)}")
        code_config = agent_service.get("codeConfiguration") or {}
        entry_point = code_config.get("entryPoint") if isinstance(code_config, dict) else None
        if entry_point and not (project_dir / str(entry_point)).exists():
            return _fail("1", f"codeConfiguration.entryPoint does not exist: {entry_point}")
        if not entry_point and not agent_service.get("startupCommand"):
            return _fail("1", "the hosted agent service needs codeConfiguration.entryPoint or startupCommand")
    else:
        required = ("azure.ai.agent", "kind: hosted", "protocol: responses", "version: 2.0.0")
        missing = [value for value in required if value not in raw]
        if missing:
            return _fail("1", f"azure.yaml is missing current hosted-agent fields: {', '.join(missing)}")

    if track == "customer" and "northfield" in raw.lower():
        warn("--track customer: hosted/azure.yaml still contains Northfield text; adapt the agent before demo.")
    ok("✅ Step 1 PASS — azure.yaml + hosted Responses service + source project present and valid")
    return True


# --------------------------------------------------------------------------- #
# Step 2 — hosted agent deployed, version active                              #
# --------------------------------------------------------------------------- #
def check_step2(env: dict, dry_run: bool, track: str) -> bool:
    agent_name = _agent_name(env, track)
    if dry_run:
        if not AZURE_YAML.exists():
            return _fail("2", "scaffold hosted/azure.yaml first (Step 1)")
        ok(f"✅ Step 2 PASS (dry-run) — azure.yaml ready to deploy '{agent_name}' (live status skipped)")
        return True
    endpoint = (env.get("AZURE_AI_PROJECT_ENDPOINT") or "").strip()
    if not endpoint:
        return _fail("2", "AZURE_AI_PROJECT_ENDPOINT missing from .env")
    base = f"{endpoint.rstrip('/')}/agents/{agent_name}/endpoint/protocols/openai/responses"
    try:
        import httpx
    except ImportError as exc:
        return _fail("2", f"httpx not installed ({exc})")
    try:
        response = httpx.post(base, json={"input": "deployment probe"}, timeout=15.0)
        if response.status_code in (401, 403):
            ok(f"✅ Step 2 PASS — hosted endpoint for '{agent_name}' exists and requires authentication")
            return True
        if response.status_code == 200:
            return _fail("2", "hosted endpoint answered anonymously; authentication must be required")
        return _fail(
            "2",
            f"hosted endpoint returned {response.status_code}; run 'azd deploy' from hosted/ "
            "and wait for the version to become ready",
        )
    except Exception as exc:  # noqa: BLE001
        return _fail("2", f"hosted endpoint probe failed ({exc}); run 'azd deploy' from hosted/")


# --------------------------------------------------------------------------- #
# Step 3 — live endpoint answers authed calls, rejects anonymous              #
# --------------------------------------------------------------------------- #
def check_step3(env: dict, dry_run: bool, track: str) -> bool:
    agent_name = _agent_name(env, track)
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

        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
        prompt = "ping" if track == "customer" else "Where is the registrar?"
        authed = httpx.post(base, json={"input": prompt},
                            headers={"Authorization": f"Bearer {token_provider()}"}, timeout=30.0)
        if authed.status_code != 200:
            return _fail("3", f"authenticated call returned {authed.status_code}; check the per-agent identity + roles")
    except Exception as exc:  # noqa: BLE001
        return _fail("3", f"authenticated call failed ({exc}); run 'az login'")
    ok("✅ Step 3 PASS — live endpoint answers authenticated calls and rejects anonymous")
    return True


# --------------------------------------------------------------------------- #
# Step 4 — hosted run observable (run history / App Insights)                 #
# --------------------------------------------------------------------------- #
def check_step4(env: dict, dry_run: bool, track: str) -> bool:
    agent_name = _agent_name(env, track)
    if dry_run:
        ok("✅ Step 4 PASS (dry-run) — observability wiring assumed from Tracing activity (live query skipped)")
        return True
    workspace = (env.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID") or "").strip()
    if not workspace:
        return _fail("4", "AZURE_LOG_ANALYTICS_WORKSPACE_ID is required for live hosted-run proof; "
                          "use --dry-run for structural validation")
    try:
        from azure.identity import DefaultAzureCredential
        from azure.monitor.query import LogsQueryClient, LogsQueryStatus
        from datetime import timedelta

        client = LogsQueryClient(DefaultAzureCredential())
        query = (f'dependencies | where timestamp > ago(1h) '
                 f'| where cloud_RoleName has "{agent_name}" | count')
        resp = client.query_workspace(workspace, query, timespan=timedelta(hours=1))
        if resp.status == LogsQueryStatus.SUCCESS and resp.tables and resp.tables[0].rows:
            n = resp.tables[0].rows[0][0]
            if n and int(n) > 0:
                ok(f"✅ Step 4 PASS — {n} hosted run span(s) visible in App Insights")
                return True
        return _fail("4", "no hosted-run spans found; invoke the hosted agent, wait for telemetry "
                          "propagation, and retry")
    except ImportError as exc:
        return _fail("4", f"azure-monitor-query not installed ({exc})")
    except Exception as exc:  # noqa: BLE001
        return _fail("4", f"live hosted trace query failed ({exc}); verify login, workspace RBAC, "
                          "and telemetry configuration")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Deploy-as-a-Hosted-Agent checkpoints.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=(1, 2, 3, 4))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no Azure calls).")
    parser.add_argument("--track", choices=("upskill", "customer"), default="upskill",
                        help="upskill = Northfield reference; customer = your own scenario "
                             "(relaxes the Northfield corpus assumption, expects --question).")
    args = parser.parse_args()

    env = load_env()
    if args.dry_run:
        info("(dry-run: offline structural checks only — no Azure calls)\n")
    if args.track == "customer":
        info("(track: customer — validating YOUR scenario, not Northfield)\n")

    checks = {
        1: lambda: check_step1(env, args.dry_run, args.track),
        2: lambda: check_step2(env, args.dry_run, args.track),
        3: lambda: check_step3(env, args.dry_run, args.track),
        4: lambda: check_step4(env, args.dry_run, args.track),
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
