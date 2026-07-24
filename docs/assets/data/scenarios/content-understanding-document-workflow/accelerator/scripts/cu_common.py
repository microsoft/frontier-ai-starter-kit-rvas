"""Shared helpers for the Content Understanding scenario checkpoint scripts.

Kept dependency-free so every ``verify_*.py`` script can run offline (``--offline``)
with only the Python standard library. Live checks import the Azure SDKs lazily.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ACCELERATOR = Path(__file__).resolve().parent.parent
ENV_FILE = ACCELERATOR / ".env"
SAMPLE_DATA = ACCELERATOR / "sample-data"
WORKFLOW = SAMPLE_DATA / "workflow"

# Any env variable whose name contains one of these is a leaked secret in a
# keyless-first contract.
FORBIDDEN_ENV_SUBSTRINGS = ("API_KEY", "ACCOUNT_KEY", "CONNECTION_STRING", "SAS_TOKEN", "SECRET")


def load_env() -> dict[str, str]:
    """Load the .env contract (and process env) into a plain dict."""
    import os

    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    values.update({key: val for key, val in os.environ.items() if val})
    return values


def load_json(path: Path, failures: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        failures.append(f"missing required file: {path}")
    except json.JSONDecodeError as error:
        failures.append(f"invalid JSON in {path}: {error.msg}")
    return None


def check(passed: bool, message: str, failures: list[str]) -> bool:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)
    return passed


def no_leaked_secrets(env: dict[str, str], failures: list[str]) -> None:
    leaked = [key for key in env if any(bad in key.upper() for bad in FORBIDDEN_ENV_SUBSTRINGS)]
    check(not leaked, f"no key/secret variables in the contract (found: {leaked or 'none'})", failures)


def finish(module_number: int, name: str, failures: list[str]) -> int:
    if failures:
        print(f"\n❌ Module {module_number} checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print(f"\n✅ Module {module_number} checkpoint PASS — {name}")
    return 0
