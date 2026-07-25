#!/usr/bin/env python3
"""Module 1 checkpoint — the capability decision record is complete and self-consistent.

This is a structural, offline check: it does not call Azure. It asserts that the dated
capability decision names a service, API, region, identity, pricing note, accessibility
alternatives, disclosure, and — critically — that the responsible-AI gating is internally
consistent (custom avatar/voice ⇒ limited-access registration + talent consent + disclosure).

Run:
    python3 scenarios/avatar-onboarding/accelerator/scripts/verify_capability.py
    python3 .../verify_capability.py --decision path/to/capability-decision.json
    python3 .../verify_capability.py --offline   # same checks; no Azure either way
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
DEFAULT_DECISION = ACCELERATOR / "sample-data" / "capability-decision.json"

SUPPORTED_CAPABILITIES = {
    "speech-tts-avatar-batch",
    "speech-tts-avatar-realtime",
    "voice-live-realtime-avatar",
    "voice-live-audio",
    "speech-tts-audio-only",
    "video-translation",
}
REQUIRED_TOP_FIELDS = (
    "decision_id", "decided_at", "decided_by", "pilot_scope", "selected_capability",
    "verification", "api", "region", "identity", "pricing_note",
    "accessibility", "consent_and_gating", "disclosure_statement",
)


def check(passed: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)


def verify(decision_path: Path, failures: list[str]) -> None:
    if not decision_path.is_file():
        check(False, f"decision record exists at {decision_path}", failures)
        return
    try:
        data = json.loads(decision_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        check(False, f"decision record is valid JSON ({error})", failures)
        return

    for field in REQUIRED_TOP_FIELDS:
        check(field in data and data[field] not in (None, "", [], {}),
              f"decision declares {field!r}", failures)

    capability = data.get("selected_capability")
    check(capability in SUPPORTED_CAPABILITIES,
          f"selected_capability {capability!r} is a supported Azure capability", failures)

    verification = data.get("verification", {})
    check(bool(verification.get("fetched_on")) and bool(verification.get("docs")),
          "decision cites dated Microsoft Learn verification (fetched_on + docs)", failures)

    accessibility = data.get("accessibility", {})
    check(
        accessibility.get("captions") is True
        and accessibility.get("transcript") is True
        and accessibility.get("non_avatar_fallback") is True,
        "decision commits to captions, transcript, and a non-avatar fallback",
        failures,
    )

    check(bool(str(data.get("disclosure_statement", "")).strip()),
          "decision includes a synthetic-media disclosure statement", failures)

    gating = data.get("consent_and_gating", {})
    uses_custom_avatar = bool(gating.get("uses_custom_avatar"))
    uses_custom_voice = bool(gating.get("uses_custom_or_personal_voice"))
    if uses_custom_avatar or uses_custom_voice:
        # Limited-access gating: custom avatar and custom/personal voice require registration,
        # explicit talent consent, and disclosure — verified on learn.microsoft.com 2026-07-24.
        check(bool(gating.get("limited_access_registration_required")),
              "custom avatar/voice ⇒ limited_access_registration_required is true", failures)
        check(bool(gating.get("talent_consent_required")),
              "custom avatar/voice ⇒ talent_consent_required is true", failures)
        check(str(gating.get("limited_access_form", "")).startswith("http"),
              "custom avatar/voice ⇒ a limited-access registration form is recorded", failures)
    else:
        check(gating.get("disclosure_required") is True,
              "standard avatar/voice still requires user disclosure", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision", type=Path, default=DEFAULT_DECISION,
                        help="path to the capability decision record JSON")
    parser.add_argument("--offline", action="store_true",
                        help="structure-only; this check never calls Azure regardless")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 1 checkpoint: capability decision record ==")
    verify(args.decision, failures)

    if failures:
        print(f"\n❌ Module 1 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 1 checkpoint PASS — capability decision is complete and RAI-consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
