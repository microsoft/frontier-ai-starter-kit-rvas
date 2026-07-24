#!/usr/bin/env python3
"""Code-driven evaluation for the Northfield IQ Assistant.

Runs the built-in Azure AI quality evaluators (Groundedness, Relevance,
Coherence, Fluency) plus a custom Northfield domain evaluator over a JSONL
dataset, prints per-row and aggregate scores, and exits non-zero when the
mean of any gated metric falls below a threshold (the CI-gate concept).

Usage
-----
    # quality eval over the shipped dataset (calls your grounded agent for each row)
    python activities/advanced-evaluation-redteam/evaluate.py

    # custom evaluator only, no LLM-judge cost
    python activities/advanced-evaluation-redteam/evaluate.py --custom-only

    # gate the run in CI: fail if any mean score < 3.5 (1-5 scale)
    python activities/advanced-evaluation-redteam/evaluate.py --gate 3.5

Environment (.env, from the Foundations end-state)
--------------------------------------------------
    AZURE_AI_PROJECT_ENDPOINT       # https://<res>.services.ai.azure.com/api/projects/<proj>
    AZURE_OPENAI_ENDPOINT           # Foundry account endpoint from .env
    AZURE_AI_MODEL_DEPLOYMENT_NAME  # judge model deployment, e.g. gpt-4o
    AZURE_FOUNDRY_AGENT_NAME        # the grounded agent created in Foundations Step 3/4

Auth is keyless via DefaultAzureCredential (run `az login` first).
"""
from __future__ import annotations

import argparse
import json
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv optional; .env may already be exported in the shell
    pass
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- #
# Custom domain evaluator — runs locally, no LLM judge, no Azure calls.        #
# Checks Northfield-specific quality signals the generic metrics miss.         #
# --------------------------------------------------------------------------- #
NORTHFIELD_CONTACT = re.compile(r"[a-z]+@northfield\.edu", re.IGNORECASE)
ABSTAIN_PHRASES = (
    "don't have",
    "do not have",
    "not list",
    "does not contain",
    "contact the university",
    "contact finaid",
)


class NorthfieldDomainEvaluator:
    """Custom evaluator: rewards grounded contact info and correct abstention.

    Score is 1.0-5.0 so it sits on the same scale as the built-in evaluators.
    - +contact: answer surfaces a *@northfield.edu address or campus phone when
      the ground truth contains one.
    - +abstain: for `category == "abstain"` rows, the answer must decline / defer
      rather than fabricate an answer.
    - -hallucinated_email: penalize any email that is NOT @northfield.edu.
    """

    def __call__(self, *, query: str, response: str, ground_truth: str = "", category: str = "", **_):
        score = 3.0
        reasons = []

        response_words = set(re.findall(r"[a-z0-9]{4,}", response.lower()))
        truth_words = set(re.findall(r"[a-z0-9]{4,}", ground_truth.lower()))
        overlap = len(response_words & truth_words)
        if not response.strip():
            score -= 2.0
            reasons.append("empty response")
        elif truth_words and overlap < 2:
            score -= 1.0
            reasons.append("little evidence of the expected grounded answer")
        elif truth_words:
            score += 1.0
            reasons.append("matches grounded answer content")

        gt_wants_contact = bool(NORTHFIELD_CONTACT.search(ground_truth)) or "(555)" in ground_truth
        if gt_wants_contact:
            if NORTHFIELD_CONTACT.search(response) or "(555)" in response:
                score += 1.0
                reasons.append("included grounded contact")
            else:
                score -= 1.0
                reasons.append("missing expected contact")

        if category == "abstain":
            if any(p in response.lower() for p in ABSTAIN_PHRASES):
                score += 2.0
                reasons.append("correctly abstained")
            else:
                score -= 2.0
                reasons.append("failed to abstain on out-of-scope/unknown query")

        foreign_emails = [
            e for e in re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response)
            if "northfield.edu" not in e.lower()
        ]
        if foreign_emails:
            score -= 2.0
            reasons.append(f"hallucinated/foreign contact: {foreign_emails}")

        score = max(1.0, min(5.0, score))
        return {"northfield_domain_score": score, "northfield_reason": "; ".join(reasons) or "baseline"}


# --------------------------------------------------------------------------- #
# Agent invocation — get a live answer for each dataset query.                 #
# Falls back to the dataset's ground_truth in --dry-run so the harness is      #
# runnable before the agent exists (useful for wiring/CI smoke tests).         #
# --------------------------------------------------------------------------- #
def get_agent_response(openai_client, agent_name: str, query: str) -> str:
    """Run one query against the grounded Northfield agent and return its text."""
    response = openai_client.responses.create(
        input=query,
        extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
    )
    return getattr(response, "output_text", "") or ""


def build_rows(
    dataset: Path,
    dry_run: bool,
    use_dataset_responses: bool,
    openai_client,
    agent_name: str,
) -> list[dict]:
    rows = []
    for line in dataset.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        if dry_run:
            item["response"] = item.get("ground_truth", "")
        elif use_dataset_responses:
            if "response" not in item:
                raise ValueError("every row must include response when --use-dataset-responses is set")
        else:
            item["response"] = get_agent_response(openai_client, agent_name, item["query"])
        rows.append(item)
    return rows


def run_builtin_evaluators(rows: list[dict]) -> dict[str, list[float]]:
    """Score Groundedness, Relevance, Coherence, Fluency with azure-ai-evaluation."""
    from azure.ai.evaluation import (
        CoherenceEvaluator,
        FluencyEvaluator,
        GroundednessEvaluator,
        RelevanceEvaluator,
    )
    from azure.identity import DefaultAzureCredential

    model_config = {
        "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
        "azure_deployment": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    }
    credential = DefaultAzureCredential()
    evaluators = {
        "groundedness": GroundednessEvaluator(model_config, credential=credential),
        "relevance": RelevanceEvaluator(model_config, credential=credential),
        "coherence": CoherenceEvaluator(model_config, credential=credential),
        "fluency": FluencyEvaluator(model_config, credential=credential),
    }
    scores: dict[str, list[float]] = {name: [] for name in evaluators}
    for row in rows:
        for name, ev in evaluators.items():
            try:
                if name == "groundedness":
                    res = ev(query=row["query"], context=row.get("context", ""), response=row["response"])
                elif name == "fluency":
                    res = ev(response=row["response"])
                else:
                    res = ev(query=row["query"], response=row["response"])
                scores[name].append(float(res[name]))
            except Exception as exc:  # keep the batch alive on a single bad row
                print(f"  ! {name} failed on '{row['query'][:40]}...': {exc}", file=sys.stderr)
    return scores


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the Northfield IQ Assistant.")
    parser.add_argument("--dataset", default=HERE / "assets" / "northfield-eval.jsonl", type=Path)
    parser.add_argument("--gate", type=float, default=None,
                        help="Fail (exit 1) if any gated metric mean < this value (1-5).")
    parser.add_argument("--custom-only", action="store_true",
                        help="Run only the custom Northfield evaluator (no LLM-judge cost).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Use ground_truth as the response instead of calling the agent.")
    parser.add_argument(
        "--use-dataset-responses",
        action="store_true",
        help="Score each row's existing response field without calling the agent.",
    )
    args = parser.parse_args()

    if not args.dataset.exists() and not args.dataset.is_absolute():
        activity_relative = HERE / args.dataset
        if activity_relative.exists():
            args.dataset = activity_relative

    if not args.dataset.exists():
        print(f"❌ dataset not found: {args.dataset}")
        return 2

    openai_client = None
    agent_name = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "")
    if not args.dry_run and not args.use_dataset_responses:
        if not agent_name:
            print("❌ AZURE_FOUNDRY_AGENT_NAME is required for a live evaluation.")
            return 2
        try:
            from azure.ai.projects import AIProjectClient
            from azure.identity import DefaultAzureCredential

            project = AIProjectClient(
                endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                credential=DefaultAzureCredential(),
            )
            if not any(getattr(agent, "name", None) == agent_name for agent in project.agents.list()):
                print(f"❌ agent '{agent_name}' not found in the configured project.")
                return 2
            openai_client = project.get_openai_client()
        except Exception as exc:
            print(f"❌ could not initialize the live agent evaluation ({exc})")
            return 2

    try:
        rows = build_rows(
            args.dataset,
            args.dry_run,
            args.use_dataset_responses,
            openai_client,
            agent_name,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"❌ invalid evaluation dataset: {exc}")
        return 2
    print(f"Loaded {len(rows)} rows from {args.dataset}"
          + (" (dry-run: response=ground_truth)" if args.dry_run else "")
          + (" (using dataset responses)" if args.use_dataset_responses else ""))

    # Custom evaluator (always runs — cheap, local).
    custom = NorthfieldDomainEvaluator()
    custom_scores = []
    for row in rows:
        out = custom(**row)
        custom_scores.append(out["northfield_domain_score"])
    all_scores: dict[str, list[float]] = {"northfield_domain": custom_scores}

    # Built-in LLM-judge evaluators.
    if not args.custom_only:
        all_scores.update(run_builtin_evaluators(rows))

    # Report.
    print("\n=== Aggregate scores (1-5) ===")
    means: dict[str, float] = {}
    for name, vals in all_scores.items():
        if vals:
            means[name] = statistics.mean(vals)
            print(f"  {name:18s} mean={means[name]:.2f}  n={len(vals)}")

    # CI gate.
    if args.gate is not None:
        incomplete = {
            name: len(vals)
            for name, vals in all_scores.items()
            if len(vals) != len(rows)
        }
        if incomplete:
            print(
                "\n❌ GATE FAILED — incomplete evaluator coverage: "
                + ", ".join(f"{name}={count}/{len(rows)}" for name, count in incomplete.items())
            )
            return 1
        failed = {k: v for k, v in means.items() if v < args.gate}
        if failed:
            print(f"\n❌ GATE FAILED (threshold {args.gate}): "
                  + ", ".join(f"{k}={v:.2f}" for k, v in failed.items()))
            return 1
        print(f"\n✅ GATE PASSED — all metrics ≥ {args.gate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
