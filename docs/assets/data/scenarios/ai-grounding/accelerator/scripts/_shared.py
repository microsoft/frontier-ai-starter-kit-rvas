#!/usr/bin/env python3
"""Shared helpers for the AI Grounding module checkpoints.

Kept dependency-free so every `--offline` path runs in CI without the Azure SDKs installed.
"""
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
    """Load the golden question set used by modules 3 through 7."""
    if not GOLDEN_QUESTIONS.is_file():
        return []
    data = json.loads(GOLDEN_QUESTIONS.read_text(encoding="utf-8"))
    return list(data.get("cases", []))


def verify_golden_set(cases: list[dict[str, Any]], failures: list[str]) -> None:
    """A golden set without negative cases proves nothing. Enforce that here, once."""
    check(bool(cases), "golden question set loaded", failures)
    answer_cases = [case for case in cases if case.get("expected_behavior") == "answer"]
    refuse_cases = [case for case in cases if case.get("expected_behavior") == "refuse"]
    check(bool(answer_cases), f"golden set has answerable cases ({len(answer_cases)})", failures)
    check(bool(refuse_cases), f"golden set has refusal cases ({len(refuse_cases)})", failures)
    check(
        all(case.get("expected_citations") for case in answer_cases),
        "every answerable case declares expected citations",
        failures,
    )
    check(
        any("SVC-ALPINE" in citation for case in answer_cases for citation in case["expected_citations"]),
        "golden set covers the superseded-notice (recency) case",
        failures,
    )
    check(
        len({group for case in cases for group in case.get("role_groups", [])}) > 1,
        "golden set spans more than one role group",
        failures,
    )
