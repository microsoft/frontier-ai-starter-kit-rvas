#!/usr/bin/env python3
"""Checkpoints for Advanced · Evaluation & Red Teaming.

Each step's Checkpoint runs `python validate.py --step N`. The checks are
intentionally lightweight and offline so a facilitator can verify progress without
burning evaluation quota. The final `--all` asserts the activity end-state.

    python validate.py --step 1     # dataset present & well-formed
    python validate.py --step 2     # evaluate.py runs (dry-run, custom-only)
    python validate.py --step 3     # custom evaluator wired & scoring
    python validate.py --step 4     # adversarial seed set present & labeled
    python validate.py --all        # everything above
"""
from __future__ import annotations

import argparse
import json
import os
import re

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv optional; .env may already be exported in the shell
    pass

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_DATASET = HERE / "assets" / "sample-eval.jsonl"
DEFAULT_ADVERSARIAL = HERE / "assets" / "adversarial-seed.jsonl"
EVALUATE = HERE / "evaluate.py"
MIN_ROWS = 25
REQUIRED_KEYS = {"query", "context", "ground_truth"}
ADV_CATEGORIES = {"jailbreak", "harmful-content", "indirect-prompt-injection", "self-harm-adjacent"}


def _fail(step: str, msg: str) -> bool:
    print(f"❌ Step {step} FAIL — {msg}")
    return False


def _warn_customer_default(track: str, path: Path, default: Path, artifact: str) -> None:
    if track == "customer" and path.resolve() == default.resolve():
        print(f"⚠  --track customer: pass your own {artifact}; the sample organization default is only a shape check.")


def check_step1(dataset: Path, track: str) -> bool:
    _warn_customer_default(track, dataset, DEFAULT_DATASET, "evaluation dataset with --dataset")
    if not dataset.exists():
        return _fail("1", f"missing dataset {dataset}")
    rows = [json.loads(l) for l in dataset.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(rows) < MIN_ROWS:
        return _fail("1", f"dataset has {len(rows)} rows; need ≥ {MIN_ROWS} (no tiny 10-row sets)")
    for i, r in enumerate(rows):
        if not REQUIRED_KEYS.issubset(r):
            return _fail("1", f"row {i} missing keys {REQUIRED_KEYS - set(r)}")
    topics = {r.get("topic") for r in rows}
    if len(topics) < 5:
        label = "scenario corpus" if track == "customer" else "FAQ corpus"
        return _fail("1", f"only {len(topics)} topics; broaden coverage across the {label}")
    if not any(r.get("category") == "abstain" for r in rows):
        return _fail("1", "no abstain/out-of-scope rows; add cases the agent should decline")
    print(f"✅ Step 1 PASS — {len(rows)} rows, {len(topics)} topics, abstain cases present")
    return True


def check_step2(dataset: Path, track: str) -> bool:
    _warn_customer_default(track, dataset, DEFAULT_DATASET, "evaluation dataset with --dataset")
    if not EVALUATE.exists():
        return _fail("2", f"missing {EVALUATE}")
    proc = subprocess.run(
        [sys.executable, str(EVALUATE), "--dataset", str(dataset), "--dry-run", "--custom-only"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return _fail("2", f"evaluate.py exited {proc.returncode}\n{proc.stderr[-400:]}")
    if "Aggregate scores" not in proc.stdout:
        return _fail("2", "evaluate.py did not print an aggregate score table")
    print("✅ Step 2 PASS — evaluate.py runs and reports aggregate scores")
    return True


def check_step3(track: str) -> bool:
    sys.path.insert(0, str(HERE))
    try:
        from evaluate import SampleOrganizationDomainEvaluator
    except Exception as exc:
        if track == "customer" and EVALUATE.exists():
            src = EVALUATE.read_text(encoding="utf-8")
            if re.search(r"class\s+\w*Evaluator\b", src) and "score" in src.lower():
                print("✅ Step 3 PASS — custom evaluator structure present (customer scenario; manual discrimination proof required)")
                return True
        return _fail("3", f"cannot import SampleOrganizationDomainEvaluator: {exc}")
    if track == "customer":
        print("⚠  --track customer: default SampleOrganizationDomainEvaluator is still present; adapt the evaluator rules to your domain before demo.")
    ev = SampleOrganizationDomainEvaluator()
    good = ev(query="contact?", response="Email finaid@sample.edu.",
              ground_truth="Email finaid@sample.edu.", category="factual")
    bad = ev(query="parking fee?", response="The fee is $200.",
             ground_truth="I don't have that info.", category="abstain")
    if good["sample_domain_score"] <= bad["sample_domain_score"]:
        return _fail("3", "custom evaluator does not reward grounded/abstained answers over fabricated ones")
    print(f"✅ Step 3 PASS — custom evaluator discriminates "
          f"(grounded={good['sample_domain_score']:.1f} > fabricated={bad['sample_domain_score']:.1f})")
    return True


def check_step4(adversarial: Path, track: str) -> bool:
    _warn_customer_default(track, adversarial, DEFAULT_ADVERSARIAL, "adversarial set with --adversarial")
    if not adversarial.exists():
        return _fail("4", f"missing adversarial seed set {adversarial}")
    rows = [json.loads(l) for l in adversarial.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(rows) < 5:
        return _fail("4", f"only {len(rows)} adversarial prompts; need ≥ 5")
    cats = {r.get("category") for r in rows}
    if not (cats & ADV_CATEGORIES):
        return _fail("4", f"no recognized attack categories; expected some of {ADV_CATEGORIES}")
    if not any("injected_context" in r for r in rows):
        return _fail("4", "no prompt-injection-via-document case (injected_context) present")
    if not all("expected_behavior" in r for r in rows):
        return _fail("4", "every adversarial row needs an expected_behavior to grade against")
    print(f"✅ Step 4 PASS — {len(rows)} adversarial prompts across {len(cats)} categories, injection case present")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=(1, 2, 3, 4))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--track", choices=("reference", "customer"), default="reference",
                        help="reference = sample organization reference; customer = your own scenario "
                             "(relaxes the sample organization corpus assumption, expects --question).")
    parser.add_argument("--dataset", default=DEFAULT_DATASET, type=Path,
                        help="Evaluation JSONL to validate (customer track: your scenario dataset).")
    parser.add_argument("--adversarial", default=DEFAULT_ADVERSARIAL, type=Path,
                        help="Adversarial JSONL to validate (customer track: your scenario attacks).")
    args = parser.parse_args()
    if args.track == "customer":
        print("(track: customer — validating YOUR scenario, not sample organization)\n")

    checks = {
        1: lambda: check_step1(args.dataset, args.track),
        2: lambda: check_step2(args.dataset, args.track),
        3: lambda: check_step3(args.track),
        4: lambda: check_step4(args.adversarial, args.track),
    }

    if args.all:
        ok = all(checks[s]() for s in sorted(checks))
        print("\n✅ ALL CHECKPOINTS PASS" if ok else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
        return 0 if ok else 1
    return 0 if checks[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
