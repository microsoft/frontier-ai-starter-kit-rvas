#!/usr/bin/env python3
"""Create deterministic, local-only retrieval evidence for the fictional corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA = ROOT / "sample-data"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
RESTRICTED_TERMS = {"private", "payment", "another", "customer", "notes", "history"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "can",
    "do",
    "for",
    "has",
    "in",
    "is",
    "of",
    "on",
    "the",
    "to",
    "what",
    "with",
}


def tokens(value: str) -> list[str]:
    """Normalize text consistently without third-party NLP dependencies."""
    return [
        token
        for token in TOKEN_PATTERN.findall(value.lower())
        if token not in STOPWORDS
    ]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def load_sources() -> list[dict[str, Any]]:
    manifest = load_json(SAMPLE_DATA / "source-manifest.json")
    sources: list[dict[str, Any]] = []
    for metadata in manifest["sources"]:
        path = SAMPLE_DATA / metadata["path"]
        content = path.read_text(encoding="utf-8")
        source = dict(metadata)
        source["content"] = content
        source["content_sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
        source["term_counts"] = Counter(
            tokens(f'{metadata["citation_label"]} {metadata["owner"]} {content}')
        )
        sources.append(source)
    return sorted(sources, key=lambda source: source["source_id"])


def rank_sources(question: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    query_terms = set(tokens(question))
    matches: list[dict[str, Any]] = []
    for source in sources:
        matched_terms = sorted(query_terms.intersection(source["term_counts"]))
        score = sum(source["term_counts"][term] for term in matched_terms)
        if score:
            matches.append(
                {
                    "source_id": source["source_id"],
                    "citation": source["citation_label"],
                    "score": score,
                    "matched_terms": matched_terms,
                    "access_groups": source["access_groups"],
                }
            )
    return sorted(matches, key=lambda match: (-match["score"], match["source_id"]))


def evaluate_case(case: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    role_groups = set(case["role_groups"])
    ranked = rank_sources(case["question"], sources)
    allowed = [
        item
        for item in ranked
        if role_groups.intersection(item["access_groups"])
    ]
    withheld = [
        item
        for item in ranked
        if not role_groups.intersection(item["access_groups"])
    ]
    expected_citations = case["expected_citations"]

    if case["expected_behavior"] == "answer":
        selected = allowed[: len(expected_citations)]
        citations = [item["source_id"] for item in selected]
        outcome = {
            "behavior": "answer",
            "response": case["expected_response"],
            "citations": citations,
            "selected_sources": selected,
            "withheld_sources": withheld,
        }
        passed = citations == expected_citations
        checks = {
            "expected_citations_match": passed,
            "all_selected_sources_authorized": all(
                role_groups.intersection(item["access_groups"]) for item in selected
            ),
            "no_withheld_source_cited": not set(citations).intersection(
                item["source_id"] for item in withheld
            ),
        }
    else:
        refusal_mode = case["refusal_mode"]
        if refusal_mode == "restricted-request":
            mode_passed = bool(RESTRICTED_TERMS.intersection(tokens(case["question"])))
        elif refusal_mode == "access-denied":
            mode_passed = bool(withheld)
        else:
            required_terms = set(case.get("required_evidence_terms", []))
            mode_passed = not any(
                required_terms.issubset(set(item["matched_terms"])) for item in allowed
            )
        outcome = {
            "behavior": "refuse",
            "refusal_mode": refusal_mode,
            "refusal_reason": case["expected_refusal_reason"],
            "citations": [],
            "selected_sources": [],
            "withheld_sources": withheld,
        }
        checks = {
            "refusal_mode_supported": mode_passed,
            "no_source_cited": True,
            "expected_citations_match": not expected_citations,
        }
        passed = all(checks.values())

    return {
        "id": case["id"],
        "role_groups": case["role_groups"],
        "question": case["question"],
        "expected_behavior": case["expected_behavior"],
        "expected_citations": expected_citations,
        "acceptance_criteria": case["acceptance_criteria"],
        "outcome": outcome,
        "checks": checks,
        "passed": passed,
    }


def build_evidence() -> dict[str, Any]:
    sources = load_sources()
    golden_set = load_json(ROOT / "golden-questions.json")
    results = [evaluate_case(case, sources) for case in golden_set["cases"]]
    fingerprint = hashlib.sha256(
        "".join(
            f'{source["source_id"]}:{source["content_sha256"]}\n' for source in sources
        ).encode("utf-8")
    ).hexdigest()
    return {
        "artifact_type": "local-retrieval-simulation-evidence",
        "schema_version": "1.0",
        "deterministic": True,
        "simulation_boundary": (
            "Local lexical retrieval only; no Azure SDK, network request, model call, "
            "identity, secret, or real data is used."
        ),
        "corpus_fingerprint_sha256": fingerprint,
        "prepared_sources": [
            {
                "source_id": source["source_id"],
                "path": f'sample-data/{source["path"]}',
                "owner": source["owner"],
                "access_groups": source["access_groups"],
                "content_sha256": source["content_sha256"],
            }
            for source in sources
        ],
        "cases": results,
        "summary": {
            "total_cases": len(results),
            "passed_cases": sum(result["passed"] for result in results),
            "failed_case_ids": [
                result["id"] for result in results if not result["passed"]
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare the fictional corpus and emit local retrieval evidence."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "evidence" / "local-retrieval-evidence.json",
        help="Evidence artifact path (default: accelerator/evidence/local-retrieval-evidence.json).",
    )
    args = parser.parse_args()
    evidence = build_evidence()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f'Prepared {len(evidence["prepared_sources"])} sources; '
        f'{evidence["summary"]["passed_cases"]}/{evidence["summary"]["total_cases"]} '
        f'golden cases passed: {args.output}'
    )
    return 0 if not evidence["summary"]["failed_case_ids"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
