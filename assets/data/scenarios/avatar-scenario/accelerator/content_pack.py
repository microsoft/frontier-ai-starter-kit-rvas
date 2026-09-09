#!/usr/bin/env python3
"""Approved-content pack contract: validate a pack and build its traceable artifact record.

Imported by the module verification scripts and the scenario validator. It performs no media
generation, vendor SDK call, identity integration, or network call.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_APPROVER_ROLES = {
    "SME",
    "legal-compliance",
    "brand-communications",
    "content-owner",
}
PACK_FILES = (
    "claims.json",
    "approvals.json",
    "storyboard-script.json",
    "transcript.txt",
    "accessible-fallback.html",
    "feedback-fixture.json",
)


class PackRejectedError(ValueError):
    """Raised when a pack is not approved or cannot be traced to approved claims."""


def _reject(message: str) -> None:
    raise PackRejectedError(message)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        _reject(f"cannot read valid JSON from {path.name}: {error}")
    if not isinstance(value, dict):
        _reject(f"{path.name} must contain a JSON object")
    return value


def _required_text(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _reject(f"{location} must be non-empty text")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_pack(data_dir: Path) -> dict[str, Any]:
    """Validate the fictional pack and return normalized trace data without writing output."""

    if not data_dir.is_dir():
        _reject(f"data directory does not exist: {data_dir}")
    paths = {name: data_dir / name for name in PACK_FILES}
    for name, path in paths.items():
        if not path.is_file():
            _reject(f"required fixture file is missing: {name}")

    claims_document = _read_json(paths["claims.json"])
    claims = claims_document.get("claims")
    if not isinstance(claims, list) or not claims:
        _reject("claims.json must include a non-empty claims list")

    claim_by_id: dict[str, dict[str, str]] = {}
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            _reject(f"claims[{index}] must be an object")
        claim_id = _required_text(claim.get("claim_id"), f"claims[{index}].claim_id")
        if claim_id in claim_by_id:
            _reject(f"duplicate claim ID: {claim_id}")
        claim_by_id[claim_id] = {
            "approved_wording": _required_text(
                claim.get("approved_wording"), f"{claim_id}.approved_wording"
            ),
            "source_reference": _required_text(
                claim.get("source_reference"), f"{claim_id}.source_reference"
            ),
        }

    approvals = _read_json(paths["approvals.json"])
    if approvals.get("approval_status") != "approved-for-demo-only":
        _reject("approval_status must be approved-for-demo-only")
    approval_rows = approvals.get("approvals")
    if not isinstance(approval_rows, list):
        _reject("approvals.json must include an approvals list")
    approved_roles = {
        row.get("role")
        for row in approval_rows
        if isinstance(row, dict)
        and row.get("decision") == "approved"
        and isinstance(row.get("approver"), str)
        and row["approver"].strip()
        and isinstance(row.get("decided_at"), str)
        and row["decided_at"].strip()
    }
    missing_roles = REQUIRED_APPROVER_ROLES - approved_roles
    if missing_roles:
        _reject(
            "missing approved human roles: " + ", ".join(sorted(missing_roles))
        )

    storyboard = _read_json(paths["storyboard-script.json"])
    script_id = _required_text(storyboard.get("script_id"), "script_id")
    script_version = _required_text(storyboard.get("script_version"), "script_version")
    if approvals.get("script_id") != script_id or approvals.get("script_version") != script_version:
        _reject("approval record does not match the script ID and version")
    disclosure = _required_text(storyboard.get("disclosure"), "disclosure")
    segments = storyboard.get("segments")
    if not isinstance(segments, list) or not segments:
        _reject("storyboard-script.json must include a non-empty segments list")

    normalized_segments: list[dict[str, Any]] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            _reject(f"segments[{index}] must be an object")
        segment_id = _required_text(segment.get("segment_id"), f"segments[{index}].segment_id")
        spoken_text = _required_text(
            segment.get("spoken_text"), f"{segment_id}.spoken_text"
        )
        claim_ids = segment.get("approved_claim_ids")
        source_references = segment.get("source_references")
        if not isinstance(claim_ids, list) or not claim_ids or not all(
            isinstance(claim_id, str) for claim_id in claim_ids
        ):
            _reject(f"{segment_id} must link to one or more approved claim IDs")
        if not isinstance(source_references, list) or not all(
            isinstance(reference, str) for reference in source_references
        ):
            _reject(f"{segment_id} must include source references")
        linked_claims: list[dict[str, str]] = []
        for claim_id in claim_ids:
            claim = claim_by_id.get(claim_id)
            if claim is None:
                _reject(f"{segment_id} links to unknown claim {claim_id}")
            linked_claims.append({"claim_id": claim_id, **claim})
        if spoken_text not in {
            claim["approved_wording"] for claim in linked_claims
        }:
            _reject(
                f"{segment_id} spoken_text is not an exact linked approved claim"
            )
        expected_sources = {claim["source_reference"] for claim in linked_claims}
        if set(source_references) != expected_sources:
            _reject(f"{segment_id} source references do not match linked claims")
        accessibility = segment.get("accessibility")
        if not isinstance(accessibility, dict):
            _reject(f"{segment_id} must include accessibility settings")
        if (
            accessibility.get("captions") is not True
            or accessibility.get("transcript_file") != "transcript.txt"
            or accessibility.get("non_avatar_fallback") != "accessible-fallback.html"
        ):
            _reject(f"{segment_id} is missing the required accessible alternatives")
        normalized_segments.append(
            {
                "segment_id": segment_id,
                "spoken_text": spoken_text,
                "claim_links": linked_claims,
                "source_references": sorted(expected_sources),
            }
        )

    transcript = paths["transcript.txt"].read_text(encoding="utf-8")
    fallback = paths["accessible-fallback.html"].read_text(encoding="utf-8")
    if disclosure not in transcript or disclosure not in fallback:
        _reject("transcript and HTML fallback must include the disclosure")
    for segment in normalized_segments:
        if segment["spoken_text"] not in transcript:
            _reject(f"transcript is missing {segment['segment_id']} spoken text")
        if segment["spoken_text"] not in fallback:
            _reject(f"HTML fallback is missing {segment['segment_id']} spoken text")
    fallback_lower = fallback.lower()
    if "<html" not in fallback_lower or 'lang="en"' not in fallback_lower or "<main" not in fallback_lower:
        _reject("HTML fallback must provide language and main landmarks")

    feedback = _read_json(paths["feedback-fixture.json"])
    if feedback.get("publication_id") != storyboard.get("publication_id"):
        _reject("feedback fixture does not match the publication ID")
    if feedback.get("classification") != "synthetic-aggregate-demo-data":
        _reject("feedback fixture must be synthetic aggregate data")

    return {
        "claims_document": claims_document,
        "approvals": approvals,
        "storyboard": storyboard,
        "segments": normalized_segments,
        "input_hashes": {name: _sha256(path) for name, path in sorted(paths.items())},
    }


def build_artifact(pack: dict[str, Any]) -> dict[str, Any]:
    """Build an artifact with no clock or random values so unchanged inputs are reproducible."""

    storyboard = pack["storyboard"]
    approvals = pack["approvals"]
    artifact: dict[str, Any] = {
        "artifact_schema_version": "1.0",
        "renderer": "avatar-onboarding-local-mock-v1",
        "publication": {
            "publication_id": storyboard["publication_id"],
            "script_id": storyboard["script_id"],
            "script_version": storyboard["script_version"],
            "locale": storyboard["locale"],
            "disclosure": storyboard["disclosure"],
        },
        "approval": {
            "approval_record_id": approvals["approval_record_id"],
            "approval_status": approvals["approval_status"],
            "approved_roles": sorted(
                row["role"]
                for row in approvals["approvals"]
                if row["decision"] == "approved"
            ),
        },
        "rendered_segments": pack["segments"],
        "accessibility": {
            "captions": True,
            "transcript_file": "transcript.txt",
            "non_avatar_fallback": "accessible-fallback.html",
        },
        "input_sha256": pack["input_hashes"],
    }
    canonical = json.dumps(
        artifact, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    artifact["artifact_id"] = f"onboarding-artifact-{digest[:16]}"
    artifact["trace_sha256"] = digest
    return artifact
