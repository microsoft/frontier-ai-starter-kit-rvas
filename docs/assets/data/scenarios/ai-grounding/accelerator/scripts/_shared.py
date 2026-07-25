#!/usr/bin/env python3
"""Shared helpers for the AI Grounding accelerator scripts."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

ACCELERATOR = Path(__file__).resolve().parent.parent
ENV_FILE = ACCELERATOR / ".env"
GOLDEN_QUESTIONS = ACCELERATOR / "golden-questions.json"


def load_env(required: tuple[str, ...] = ()) -> dict[str, str]:
    """Read the generated .env contract, with process environment taking precedence."""
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    for key in required:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def check(passed: bool, message: str, failures: list[str]) -> bool:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)
    return passed


def load_golden_cases() -> list[dict[str, Any]]:
    """Load the golden question set."""
    if not GOLDEN_QUESTIONS.is_file():
        return []
    data = json.loads(GOLDEN_QUESTIONS.read_text(encoding="utf-8"))
    return list(data.get("cases", []))
