#!/usr/bin/env python3
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover - handled in package checks
    requests = None

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:  # pragma: no cover - graceful fallback when rich is missing
    Console = None
    Panel = None
    Table = None

ROOT = Path.cwd()
ENV_PATH = ROOT / ".env"
REQUIRED_VARS = [
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_SUBSCRIPTION_ID",
    "AZURE_RESOURCE_GROUP",
]
OPTIONAL_VARS = [
    "AZURE_AI_MODEL_DEPLOYMENT_NAME",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_DEPLOYMENT_NAME",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_INDEX_NAME",
    "AZURE_FOUNDRY_KNOWLEDGE_BASE_NAME",
    "AZURE_FOUNDRY_AGENT_NAME",
    "APPLICATIONINSIGHTS_CONNECTION_STRING",
    "ACTION_API_URL",
    "ACTION_MCP_URL",
]
PACKAGE_CHECKS = [
    ("azure-ai-projects", "azure.ai.projects"),
    ("azure-ai-agents", "azure.ai.agents"),
    ("azure-ai-inference", "azure.ai.inference"),
    ("azure-ai-evaluation", "azure.ai.evaluation"),
    ("azure-core", "azure.core"),
    ("azure-search-documents", "azure.search.documents"),
    ("azure-identity", "azure.identity"),
    ("flask", "flask"),
    ("openai", "openai"),
    ("python-dotenv", "dotenv"),
    ("requests", "requests"),
    ("jupyter", "jupyter_core"),
    ("ipykernel", "ipykernel"),
    ("rich", "rich"),
]
STATUS_STYLE = {
    "PASS": "bold green",
    "WARN": "bold yellow",
    "FAIL": "bold red",
}


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def resolved_env(file_values: dict[str, str]) -> dict[str, str]:
    merged = dict(file_values)
    for key, value in os.environ.items():
        if value:
            merged[key] = value
    return merged


def style_status(status: str) -> str:
    if Console is None:
        return status
    return f"[{STATUS_STYLE[status]}]{status}[/{STATUS_STYLE[status]}]"


class Reporter:
    def __init__(self) -> None:
        self.console = Console() if Console else None
        self.rows: list[tuple[str, str, str]] = []
        self.critical_failures = 0

    def add(self, check: str, status: str, details: str, critical: bool = False) -> None:
        self.rows.append((check, status, details))
        if critical and status == "FAIL":
            self.critical_failures += 1

    def render(self) -> None:
        if self.console and Table and Panel:
            table = Table(title="AI Starter Kit RVAS Environment Validation")
            table.add_column("Check", style="cyan", no_wrap=True)
            table.add_column("Status", no_wrap=True)
            table.add_column("Details", style="white")
            for check, status, details in self.rows:
                table.add_row(check, style_status(status), details)
            self.console.print(table)

            passed = sum(1 for _, status, _ in self.rows if status == "PASS")
            warned = sum(1 for _, status, _ in self.rows if status == "WARN")
            failed = sum(1 for _, status, _ in self.rows if status == "FAIL")
            summary_style = "green" if failed == 0 else "red"
            self.console.print(
                Panel(
                    f"[bold]Summary[/bold]\nPassed: {passed}\nWarnings: {warned}\nFailures: {failed}",
                    border_style=summary_style,
                )
            )
        else:
            print("AI Starter Kit RVAS Environment Validation")
            print("=" * 40)
            for check, status, details in self.rows:
                print(f"- {check}: {status} - {details}")


def main() -> int:
    reporter = Reporter()

    python_ok = sys.version_info >= (3, 11)
    reporter.add(
        "Python version",
        "PASS" if python_ok else "FAIL",
        f"Detected {sys.version.split()[0]} (requires >= 3.11)",
        critical=True,
    )

    missing_packages: list[str] = []
    for distribution, module_name in PACKAGE_CHECKS:
        try:
            metadata.version(distribution)
            importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover - depends on local env
            missing_packages.append(f"{distribution} ({exc})")

    if missing_packages:
        reporter.add(
            "Python packages",
            "FAIL",
            "Missing or not importable: " + "; ".join(missing_packages),
            critical=True,
        )
    else:
        reporter.add(
            "Python packages",
            "PASS",
            "All required packages imported successfully.",
            critical=True,
        )

    env_values = load_env_file(ENV_PATH)
    merged_env = resolved_env(env_values)
    set_required = [key for key in REQUIRED_VARS if merged_env.get(key)]
    missing_required = [key for key in REQUIRED_VARS if not merged_env.get(key)]
    set_optional = [key for key in OPTIONAL_VARS if merged_env.get(key)]
    missing_optional = [key for key in OPTIONAL_VARS if not merged_env.get(key)]

    if not ENV_PATH.exists():
        reporter.add(
            ".env file",
            "FAIL",
            "No .env file found in the repository root.",
            critical=True,
        )
    elif missing_required:
        reporter.add(
            ".env file",
            "FAIL",
            f"Set required: {', '.join(set_required) or 'none'} | Missing required: {', '.join(missing_required)} | Optional set: {', '.join(set_optional) or 'none'} | Optional missing: {', '.join(missing_optional) or 'none'}",
            critical=True,
        )
    else:
        reporter.add(
            ".env file",
            "PASS",
            f"Set required: {', '.join(set_required)} | Optional set: {', '.join(set_optional) or 'none'} | Optional missing: {', '.join(missing_optional) or 'none'}",
            critical=True,
        )

    endpoint = merged_env.get("AZURE_AI_PROJECT_ENDPOINT")
    if endpoint and requests is not None:
        try:
            response = requests.get(endpoint, timeout=10)
            status = "PASS" if response.status_code < 500 else "FAIL"
            reporter.add(
                "Foundry project endpoint",
                status,
                f"Reachable at {endpoint} (HTTP {response.status_code})",
                critical=True,
            )
        except Exception as exc:  # pragma: no cover - depends on local env
            reporter.add(
                "Foundry project endpoint",
                "FAIL",
                f"Connectivity test failed for {endpoint}: {exc}",
                critical=True,
            )
    elif endpoint and requests is None:
        reporter.add(
            "Foundry project endpoint",
            "FAIL",
            "requests is not installed, so endpoint connectivity could not be checked.",
            critical=True,
        )
    else:
        reporter.add(
            "Foundry project endpoint",
            "WARN",
            "Skipped because AZURE_AI_PROJECT_ENDPOINT is not configured.",
        )

    az_path = shutil.which("az")
    if not az_path:
        reporter.add(
            "Azure CLI",
            "FAIL",
            "Azure CLI is not installed or not on PATH.",
            critical=True,
        )
    else:
        try:
            result = subprocess.run(
                [az_path, "account", "show", "--output", "json"],
                check=True,
                capture_output=True,
                text=True,
            )
            details = result.stdout.strip().replace("\n", " ")
            reporter.add("Azure CLI", "PASS", f"Authenticated. {details[:180]}", critical=True)
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip() or "Run 'az login' to authenticate."
            reporter.add("Azure CLI", "FAIL", stderr, critical=True)

    reporter.render()
    return 1 if reporter.critical_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
