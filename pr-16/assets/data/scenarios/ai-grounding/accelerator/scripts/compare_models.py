#!/usr/bin/env python3
"""Compare candidate chat deployments on your own approved context.

Runs every golden question through each candidate deployment with identical role-scoped context and
identical instructions, so the only variable is the model. This is a prompt-level comparison: it
does not exercise Azure AI Search retrieval, source permissions, or live identity propagation.

Public benchmarks measure a different workload than yours. This measures yours.

Run:
    python3 scenarios/ai-grounding/accelerator/scripts/compare_models.py \
        --deployments chat chat-candidate
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _shared import ACCELERATOR, check, load_env, load_golden_cases  # noqa: E402

REQUIRED_ENV = ("AZURE_AI_PROJECT_ENDPOINT",)
SAMPLE_DATA = ACCELERATOR / "sample-data"

INSTRUCTIONS = (
    "You answer questions for a returns team using only the provided context. "
    "Cite the document id in brackets for every claim. Do not infer and do not combine "
    "rules into new rules. If the context does not answer the question, reply exactly: "
    "\"I don't have approved information on that.\""
)

ABSTENTION = "I don't have approved information on that."


def build_context(case: dict[str, Any]) -> str:
    """Build a role-scoped fixture context so restricted sources do not leak into prompt tests."""
    manifest_path = SAMPLE_DATA / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    role_groups = set(case.get("role_groups", []))
    parts: list[str] = []
    for source in manifest.get("sources", []):
        source_groups = set(source.get("access_groups", []))
        if role_groups and not role_groups.intersection(source_groups):
            continue
        path = SAMPLE_DATA / source["path"]
        parts.append(f"[{source['source_id']}]\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def score_case(case: dict[str, Any], answer: str) -> dict[str, bool]:
    if case.get("expected_behavior") == "answer":
        cited = all(citation in answer for citation in case.get("expected_citations", []))
        return {"grounded": cited, "abstained": False, "recency": cited}
    return {"grounded": True, "abstained": ABSTENTION.lower() in answer.lower(), "recency": True}


def run_candidate(project: Any, deployment: str, cases: list[dict[str, Any]]) -> dict[str, Any]:
    openai = project.get_openai_client()
    latencies: list[float] = []
    tokens_in = tokens_out = 0
    grounded = abstained = 0
    answerable = sum(1 for case in cases if case.get("expected_behavior") == "answer")
    refusals = len(cases) - answerable

    for case in cases:
        context = build_context(case)
        started = time.perf_counter()
        response = openai.responses.create(
            model=deployment,
            instructions=INSTRUCTIONS,
            input=f"Context:\n{context}\n\nQuestion: {case['question']}",
        )
        latencies.append((time.perf_counter() - started) * 1000)

        usage = getattr(response, "usage", None)
        if usage is not None:
            tokens_in += getattr(usage, "input_tokens", 0) or 0
            tokens_out += getattr(usage, "output_tokens", 0) or 0

        scores = score_case(case, response.output_text or "")
        if case.get("expected_behavior") == "answer" and scores["grounded"]:
            grounded += 1
        if case.get("expected_behavior") == "refuse" and scores["abstained"]:
            abstained += 1

    ordered = sorted(latencies)
    p95_index = max(0, int(len(ordered) * 0.95) - 1)
    return {
        "deployment": deployment,
        "grounded": f"{grounded}/{answerable}",
        "abstained": f"{abstained}/{refusals}",
        "p50": int(statistics.median(ordered)) if ordered else 0,
        "p95": int(ordered[p95_index]) if ordered else 0,
        "tok_in": tokens_in,
        "tok_out": tokens_out,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deployments", nargs="*", default=[], help="Deployment names to compare.")
    args = parser.parse_args()

    failures: list[str] = []
    env = load_env(REQUIRED_ENV)
    cases = load_golden_cases()

    if not cases:
        print("No golden questions found. Add them to golden-questions.json first.")
        return 1

    for key in REQUIRED_ENV:
        check(bool(env.get(key)), f"{key} is set", failures)
    candidates = args.deployments or [env.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "")]
    check(all(candidates), "at least one deployment name was provided", failures)
    if failures:
        print("\nSet the environment contract and name at least one deployment first.")
        return 1

    print(f"== Comparing {len(candidates)} deployment(s) over {len(cases)} golden questions ==")
    try:
        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential

        project = AIProjectClient(
            endpoint=env["AZURE_AI_PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        rows = [run_candidate(project, name, cases) for name in candidates]
    except ImportError as error:
        print(f"SDK import failed ({error}); install azure-ai-projects")
        return 1
    except Exception as error:  # noqa: BLE001
        print(f"Model comparison failed: {error}")
        return 1

    header = f"{'deployment':<18}{'grounded':>10}{'abstained':>11}{'p50(ms)':>9}{'p95(ms)':>9}{'tok_in':>9}{'tok_out':>9}"
    print("\n" + header)
    for row in rows:
        print(
            f"{row['deployment']:<18}{row['grounded']:>10}{row['abstained']:>11}"
            f"{row['p50']:>9}{row['p95']:>9}{row['tok_in']:>9}{row['tok_out']:>9}"
        )
    answerable = sum(1 for case in cases if case.get("expected_behavior") == "answer")
    print(
        f"\n{answerable} of {len(cases)} questions are answerable from the corpus. "
        "A model that grounds fewer than that is guessing; one that abstains more is over-cautious."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
