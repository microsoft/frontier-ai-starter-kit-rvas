#!/usr/bin/env python3
"""Module 5 checkpoint — the generated experience is accessible and rendered from an approval.

Offline (default): validate the approved pack, render the deterministic local artifact via
``mock_renderer``, and assert the experience carries the required synthetic-media disclosure,
captions, a transcript, and a non-avatar fallback — and that every rendered segment traces to an
approved claim. It also builds the exact Speech avatar *batch synthesis* request body that the
approved script would produce, without calling Azure.

Live (--submit): submit that batch synthesis request to the Speech avatar API using a keyless
Entra token and poll until it succeeds, then report the output video URL.

Run:
    python3 scenarios/avatar-onboarding/accelerator/scripts/verify_experience.py
    python3 .../verify_experience.py --offline
    python3 .../verify_experience.py --submit           # calls the Speech avatar batch API
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ACCELERATOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ACCELERATOR))
from mock_renderer import PackRejectedError, build_artifact, validate_pack  # noqa: E402

DEFAULT_DATA_DIR = ACCELERATOR / "sample-data"
ENV_FILE = ACCELERATOR / ".env"

# Batch synthesis uses PUT/GET at avatar/batchsyntheses/{id} on
# {resource}.cognitiveservices.azure.com.
BATCH_API_VERSION = "2024-08-01"
DEFAULT_AVATAR_CHARACTER = "lisa"
DEFAULT_AVATAR_STYLE = "casual-sitting"
DEFAULT_VOICE = "en-US-AvaMultilingualNeural"


def check(passed: bool, message: str, failures: list[str]) -> None:
    print(f"{'PASS ' if passed else 'FAIL '} {message}")
    if not passed:
        failures.append(message)


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_FILE.is_file():
        for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    values.update(dict(os.environ))
    return values


def build_batch_request(artifact: dict) -> dict:
    """Build a Speech avatar batch synthesis request body from the approved artifact."""
    publication = artifact["publication"]
    locale = publication.get("locale", "en-US")
    xml_lang = "en-US" if locale == "en" else locale
    ssml_voice = os.environ.get("AZURE_SPEECH_VOICE", DEFAULT_VOICE)
    spoken = " ".join(segment["spoken_text"] for segment in artifact["rendered_segments"])
    ssml = (
        f"<speak version='1.0' xml:lang='{xml_lang}'>"
        f"<voice name='{ssml_voice}'>{spoken}</voice></speak>"
    )
    return {
        "inputKind": "SSML",
        "inputs": [{"content": ssml}],
        "avatarConfig": {
            "talkingAvatarCharacter": os.environ.get("AZURE_AVATAR_CHARACTER", DEFAULT_AVATAR_CHARACTER),
            "talkingAvatarStyle": os.environ.get("AZURE_AVATAR_STYLE", DEFAULT_AVATAR_STYLE),
            "videoFormat": "Mp4",
            "subtitleType": "soft_embedded",
        },
    }


def verify_offline(data_dir: Path, failures: list[str]) -> dict | None:
    try:
        pack = validate_pack(data_dir)
    except PackRejectedError as error:
        check(False, f"approved pack accepted by the renderer ({error})", failures)
        return None
    check(True, "approved pack accepted by the renderer", failures)
    artifact = build_artifact(pack)

    disclosure = artifact["publication"]["disclosure"]
    check(bool(disclosure.strip()), "experience carries a synthetic-media disclosure", failures)
    accessibility = artifact["accessibility"]
    check(accessibility.get("captions") is True, "captions enabled", failures)
    check(accessibility.get("transcript_file") == "transcript.txt", "transcript attached", failures)
    check(accessibility.get("non_avatar_fallback") == "accessible-fallback.html",
          "non-avatar fallback attached", failures)
    check(bool(artifact["rendered_segments"]), "experience has rendered segments", failures)
    for segment in artifact["rendered_segments"]:
        check(bool(segment.get("claim_links")),
              f"segment {segment['segment_id']} traces to an approved claim", failures)

    request = build_batch_request(artifact)
    check(request["inputKind"] in ("SSML", "PlainText"), "batch request inputKind is valid", failures)
    check(bool(request["avatarConfig"]["talkingAvatarCharacter"]),
          "batch request selects a (standard) avatar character", failures)
    print(f"\nBatch synthesis request preview (api-version={BATCH_API_VERSION}):")
    print(json.dumps(request, indent=2))
    return artifact


def submit_live(env: dict[str, str], artifact: dict, failures: list[str]) -> None:
    import urllib.error
    import urllib.request

    try:
        from azure.identity import DefaultAzureCredential
    except ImportError as error:
        check(False, f"missing SDK dependency: {error}", failures)
        return
    endpoint = env.get("AZURE_SPEECH_ENDPOINT")
    if not endpoint:
        check(False, "AZURE_SPEECH_ENDPOINT is set", failures)
        return
    token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token
    synthesis_id = f"onb-{artifact['artifact_id'][-12:]}"
    body = json.dumps(build_batch_request(artifact)).encode("utf-8")
    put_url = f"{endpoint}/avatar/batchsyntheses/{synthesis_id}?api-version={BATCH_API_VERSION}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        request = urllib.request.Request(put_url, data=body, headers=headers, method="PUT")
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed https host
            check(response.status in (200, 201), f"batch synthesis job '{synthesis_id}' submitted", failures)
    except urllib.error.HTTPError as error:
        check(False, f"batch synthesis submit failed: {error.code} {error.read().decode(errors='ignore')}", failures)
        return

    get_url = f"{endpoint}/avatar/batchsyntheses/{synthesis_id}?api-version={BATCH_API_VERSION}"
    for _ in range(60):
        with urllib.request.urlopen(  # noqa: S310 - fixed https host
            urllib.request.Request(get_url, headers={"Authorization": f"Bearer {token}"}), timeout=60
        ) as response:
            status_body = json.loads(response.read())
        status = status_body.get("status")
        if status == "Succeeded":
            check(True, f"job succeeded: {status_body.get('outputs', {}).get('result', '<no url>')}", failures)
            return
        if status == "Failed":
            check(False, f"job failed: {json.dumps(status_body.get('properties', {}))}", failures)
            return
        time.sleep(10)
    check(False, "batch synthesis job did not complete within the poll window", failures)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="approved pack directory")
    parser.add_argument("--submit", action="store_true", help="submit the batch synthesis job to Azure")
    parser.add_argument("--offline", action="store_true", help="structure-only; never call Azure")
    args = parser.parse_args()

    failures: list[str] = []
    print("== Module 5 checkpoint: accessible experience generation ==")
    artifact = verify_offline(args.data_dir, failures)

    if args.submit and not args.offline:
        if failures or artifact is None:
            print("\nSkipping live submission until the approved pack renders cleanly.")
        else:
            submit_live(load_env(), artifact, failures)
    else:
        print("\n(offline mode: did not submit to the Speech avatar API)")

    if failures:
        print(f"\n❌ Module 5 checkpoint FAILED ({len(failures)} issue(s))")
        return 1
    print("\n✅ Module 5 checkpoint PASS — accessible experience rendered from an approved revision")
    return 0


if __name__ == "__main__":
    sys.exit(main())
