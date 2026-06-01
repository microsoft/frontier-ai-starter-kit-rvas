#!/usr/bin/env python3
"""Checkpoints for Advanced · Evaluation & Red Teaming.

Each step's Checkpoint runs `python validate.py --step N`. The checks are
intentionally lightweight and offline so a coach can verify progress without
burning evaluation quota. The final `--all` asserts the challenge end-state.

    python validate.py --step 1     # dataset present & well-formed
    python validate.py --step 2     # evaluate.py runs (dry-run, custom-only)
    python validate.py --step 3     # custom evaluator wired & scoring
    python validate.py --step 4     # adversarial seed set present & labeled
    python validate.py --all        # everything above
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATASET = HERE / "assets" / "northfield-eval.jsonl"
ADVERSARIAL = HERE / "assets" / "adversarial-seed.jsonl"
EVALUATE = HERE / "evaluate.py"
MIN_ROWS = 25
REQUIRED_KEYS = {"query", "context", "ground_truth"}
ADV_CATEGORIES = {"jailbreak", "harmful-content", "indirect-prompt-injection", "self-harm-adjacent"}


def _fail(step: str, msg: str) -> bool:
    print(f"❌ Step {step} FAIL — {msg}")
    return False


def check_step1() -> bool:
    if not DATASET.exists():
        return _fail("1", f"missing dataset {DATASET}")
    rows = [json.loads(l) for l in DATASET.read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(rows) < MIN_ROWS:
        return _fail("1", f"dataset has {len(rows)} rows; need ≥ {MIN_ROWS} (no tiny 10-row sets)")
    for i, r in enumerate(rows):
        if not REQUIRED_KEYS.issubset(r):
            return _fail("1", f"row {i} missing keys {REQUIRED_KEYS - set(r)}")
    topics = {r.get("topic") for r in rows}
    if len(topics) < 5:
        return _fail("1", f"only {len(topics)} topics; broaden coverage across the FAQ corpus")
    if not any(r.get("category") == "abstain" for r in rows):
        return _fail("1", "no abstain/out-of-scope rows; add cases the agent should decline")
    print(f"✅ Step 1 PASS — {len(rows)} rows, {len(topics)} topics, abstain cases present")
    return True


def check_step2() -> bool:
    if not EVALUATE.exists():
        return _fail("2", f"missing {EVALUATE}")
    proc = subprocess.run(
        [sys.executable, str(EVALUATE), "--dataset", str(DATASET), "--dry-run", "--custom-only"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return _fail("2", f"evaluate.py exited {proc.returncode}\n{proc.stderr[-400:]}")
    if "Aggregate scores" not in proc.stdout:
        return _fail("2", "evaluate.py did not print an aggregate score table")
    print("✅ Step 2 PASS — evaluate.py runs and reports aggregate scores")
    return True


def check_step3() -> bool:
    sys.path.insert(0, str(HERE))
    try:
        from evaluate import NorthfieldDomainEvaluator
    except Exception as exc:
        return _fail("3", f"cannot import NorthfieldDomainEvaluator: {exc}")
    ev = NorthfieldDomainEvaluator()
    good = ev(query="contact?", response="Email finaid@northfield.edu.",
              ground_truth="Email finaid@northfield.edu.", category="factual")
    bad = ev(query="parking fee?", response="The fee is $200.",
             ground_truth="I don't have that info.", category="abstain")
    if good["northfield_domain_score"] <= bad["northfield_domain_score"]:
        return _fail("3", "custom evaluator does not reward grounded/abstained answers over fabricated ones")
    print(f"✅ Step 3 PASS — custom evaluator discriminates "
          f"(grounded={good['northfield_domain_score']:.1f} > fabricated={bad['northfield_domain_score']:.1f})")
    return True


def check_step4() -> bool:
    if not ADVERSARIAL.exists():
        return _fail("4", f"missing adversarial seed set {ADVERSARIAL}")
    rows = [json.loads(l) for l in ADVERSARIAL.read_text(encoding="utf-8").splitlines() if l.strip()]
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


CHECKS = {1: check_step1, 2: check_step2, 3: check_step3, 4: check_step4}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=sorted(CHECKS))
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        ok = all(check() for check in (CHECKS[s] for s in sorted(CHECKS)))
        print("\n✅ ALL CHECKPOINTS PASS" if ok else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
        return 0 if ok else 1
    return 0 if CHECKS[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
