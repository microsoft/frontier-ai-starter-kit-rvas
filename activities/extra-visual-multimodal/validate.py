#!/usr/bin/env python3
"""Offline structural checks for Extra · Visual Multimodal.

The validator deliberately does not import learner code or Azure SDK packages. It checks only
visible AST/text signals in visual_multimodal.py and never makes a network or Azure call.
"""
from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET_NAME = "visual_multimodal.py"
STEP_LABELS = {
    1: "safe image intake",
    2: "keyless authentication",
    3: "task and image analysis",
    4: "structured result schema",
    5: "confidence and uncertainty handling",
    6: "human review and evidence boundary",
}
SECRET_NAME = re.compile(r"(?:api[_-]?key|secret|token|password|connection[_-]?string)", re.I)
SECRET_VALUE = re.compile(
    r"(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]+|"
    r"(?:sk-[A-Za-z0-9_-]{12,}|AccountKey=|SharedAccessSignature=)",
    re.I,
)


def source_path(path: Path) -> Path:
    return path if path.suffix == ".py" else path / TARGET_NAME


def fail(step: int, message: str) -> bool:
    print(f"❌ Step {step} FAIL — {message}")
    return False


def has_call(tree: ast.AST, names: set[str]) -> bool:
    return any(
        isinstance(node, ast.Call)
        and (
            (isinstance(node.func, ast.Name) and node.func.id in names)
            or (isinstance(node.func, ast.Attribute) and node.func.attr in names)
        )
        for node in ast.walk(tree)
    )


def has_class_base(tree: ast.AST, bases: set[str]) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in bases:
                    return True
                if isinstance(base, ast.Attribute) and base.attr in bases:
                    return True
    return False


def hardcoded_secrets(tree: ast.AST, text: str) -> list[str]:
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names = [
            target.id
            for target in targets
            if isinstance(target, ast.Name)
        ]
        value = node.value
        if any(SECRET_NAME.search(name) for name in names) and isinstance(value, ast.Constant):
            if isinstance(value.value, str) and value.value:
                findings.append(", ".join(names))
    if SECRET_VALUE.search(text):
        findings.append("secret-like literal")
    return findings


def check_step1(tree: ast.AST, text: str) -> tuple[bool, str]:
    reads_bytes = "read_bytes" in text or (
        has_call(tree, {"open"}) and ("rb" in text or "read(" in text)
    )
    validates_type = any(token in text.lower() for token in (
        "suffix", "content_type", "mimetype", "image/jpeg", "image/png", "allowed_extensions",
    ))
    validates_size = any(token in text.lower() for token in (
        "max_bytes", "max_size", "stat().st_size", "len(image", "file_size",
    ))
    if reads_bytes and validates_type and validates_size:
        return True, "local image intake checks type and size before analysis"
    return False, "need image-byte loading plus format/type and size validation"


def check_step2(tree: ast.AST, text: str) -> tuple[bool, str]:
    if "DefaultAzureCredential" in text and has_call(tree, {"DefaultAzureCredential"}):
        return True, "DefaultAzureCredential is instantiated"
    return False, "instantiate DefaultAzureCredential (keyless-first)"


def check_step3(tree: ast.AST, text: str) -> tuple[bool, str]:
    client = "ImageAnalysisClient" in text or "multimodal" in text.lower()
    input_call = "image_data" in text or "analyze_from_url" in text or "image_url" in text
    minimum_task = any(token in text for token in (
        "VisualFeatures.READ", "VisualFeatures.CAPTION", "VisualFeatures.TAGS",
        "visual_features", "structured_output",
    ))
    if client and input_call and minimum_task:
        return True, "analysis path selects an image task/feature"
    return False, "show image analysis/multimodal input and an explicit selected task or feature"


def check_step4(tree: ast.AST, text: str) -> tuple[bool, str]:
    schema = (
        has_class_base(tree, {"BaseModel", "TypedDict"})
        or "@dataclass" in text
        or "json_schema" in text
        or "\"properties\"" in text
    )
    fields = sum(
        token in text.lower()
        for token in ("summary", "visible_sign_text", "observed_route_cues", "confidence", "review_required")
    )
    if schema and fields >= 3:
        return True, "structured observation schema is present"
    return False, "define a typed/schema result with observation and review fields"


def check_step5(tree: ast.AST, text: str) -> tuple[bool, str]:
    lower = text.lower()
    if "confidence" in lower and any(token in lower for token in (
        "uncert", "threshold", "low_confidence", "abstain", "insufficient",
    )):
        return True, "confidence is paired with an uncertainty path"
    return False, "include confidence plus uncertainty/threshold/abstain handling"


def check_step6(tree: ast.AST, text: str) -> tuple[bool, str]:
    lower = text.lower()
    review = any(token in lower for token in ("review_required", "human review", "escalat"))
    evidence = any(token in lower for token in ("trace", "evaluation", "eval", "request_id"))
    if review and evidence:
        return True, "human review boundary and evaluation/trace evidence are present"
    return False, "include review/escalation and a trace or evaluation evidence signal"


def run_step(step: int, tree: ast.AST, text: str, secrets: list[str]) -> bool:
    if secrets:
        return fail(step, f"possible hardcoded secret: {', '.join(secrets)}")
    checker = {
        1: check_step1, 2: check_step2, 3: check_step3, 4: check_step4,
        5: check_step5, 6: check_step6,
    }[step]
    ok, message = checker(tree, text)
    if ok:
        print(f"✅ Step {step} PASS — {message}")
        return True
    return fail(step, message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline checks for visual_multimodal.py; no Azure calls.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=tuple(STEP_LABELS))
    group.add_argument("--all", action="store_true", help="run all static checkpoints")
    parser.add_argument("--path", type=Path, default=HERE,
                        help="activity directory or learner visual_multimodal.py path")
    parser.add_argument("--dry-run", action="store_true",
                        help="state the offline plan; checks remain local and make no Azure calls")
    args = parser.parse_args()

    target = source_path(args.path)
    if args.dry_run:
        requested = list(STEP_LABELS) if args.all else [args.step]
        print(f"DRY RUN — would statically inspect {target} for: "
              + ", ".join(STEP_LABELS[step] for step in requested))
        print("No learner code, SDK package, credential, network, or Azure call is executed.")
    if not target.is_file():
        print(f"❌ Missing learner artifact: {target}")
        return 1

    text = target.read_text(encoding="utf-8")
    try:
        tree = ast.parse(text, filename=str(target))
    except SyntaxError as exc:
        print(f"❌ Cannot parse {target}: {exc.msg} (line {exc.lineno})")
        return 1

    secrets = hardcoded_secrets(tree, text)
    steps = list(STEP_LABELS) if args.all else [args.step]
    outcomes = [run_step(step, tree, text, secrets) for step in steps]
    if args.all:
        print("\n✅ ALL CHECKPOINTS PASS" if all(outcomes) else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
    return 0 if all(outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
