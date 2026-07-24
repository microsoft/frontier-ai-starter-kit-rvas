#!/usr/bin/env python3
"""Offline structural checkpoints for Extra · Document Workflow.

Examples:
    python validate.py --step intake
    python validate.py --all --path .
    python validate.py --all --path ./learner-work --dry-run

No Azure SDK is imported and this program makes no network or Azure service calls.
"""
from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_NAME = "document_workflow.py"


def fail(step: str, message: str) -> bool:
    print(f"FAIL  {step}: {message}")
    return False


def passed(step: str, message: str) -> bool:
    print(f"PASS  {step}: {message}")
    return True


def source_file(path_value: str) -> Path:
    path = Path(path_value).expanduser()
    return path / SOURCE_NAME if path.is_dir() else path


def load_source(path_value: str) -> tuple[Path, str, ast.AST | None]:
    path = source_file(path_value)
    if not path.exists():
        return path, "", None
    source = path.read_text(encoding="utf-8")
    try:
        return path, source, ast.parse(source, filename=str(path))
    except SyntaxError:
        return path, source, None


def has_identifier(tree: ast.AST, name: str) -> bool:
    return any(
        isinstance(node, (ast.Name, ast.Attribute))
        and (node.id == name if isinstance(node, ast.Name) else node.attr == name)
        for node in ast.walk(tree)
    )


def check_source(path: Path, tree: ast.AST | None, step: str) -> bool:
    if not path.exists():
        return fail(step, f"missing {SOURCE_NAME} at {path}")
    if tree is None:
        return fail(step, f"{SOURCE_NAME} is not valid Python")
    return True


def check_intake(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "intake"):
        return False
    assert tree is not None
    normalized = source.lower().replace("_", "").replace("-", "")
    has_credential = has_identifier(tree, "DefaultAzureCredential")
    has_document_intelligence = (
        "documentintelligence" in normalized
        or "azure.ai.documentintelligence" in source.lower()
    )
    has_layout = "layout" in source.lower() or "ocr" in source.lower()
    if not (has_credential and has_document_intelligence and has_layout):
        return fail(
            "intake",
            "use DefaultAzureCredential plus a Document Intelligence layout/OCR call",
        )
    return passed("intake", "keyless Document Intelligence layout/OCR signal found")


def check_no_secrets(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "no-secrets"):
        return False
    forbidden = (
        r"\bAzureKeyCredential\b",
        r"\b(?:DOCUMENT_INTELLIGENCE|AZURE|API)[A-Z_]*KEY\b",
        r"\b(?:api[_-]?key|subscription[_-]?key)\s*=",
        r"\b(?:sk|eyJ)[A-Za-z0-9_-]{16,}",
        r"AccountKey\s*=",
    )
    found = [pattern for pattern in forbidden if re.search(pattern, source, re.IGNORECASE)]
    if found:
        return fail("no-secrets", "remove key credentials, key variables, and hard-coded secret-like values")
    return passed("no-secrets", "no key-based credential or secret-like text found")


def check_confidence(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "confidence"):
        return False
    assert tree is not None
    numbers = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
        and 0 < node.value <= 1
    ]
    comparisons = any(isinstance(node, ast.Compare) for node in ast.walk(tree))
    if "confidence" not in source.lower() or not numbers or not comparisons:
        return fail(
            "confidence",
            "define and compare a 0–1 confidence threshold before accepting fields",
        )
    return passed("confidence", "confidence threshold and comparison found")


def check_review(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "review"):
        return False
    assert tree is not None
    text = source.lower()
    routing_terms = ("needs_review", "human_review", "review_queue", "approval")
    if not any(term in text for term in routing_terms) or not any(
        isinstance(node, ast.If) for node in ast.walk(tree)
    ):
        return fail(
            "review",
            "route a conditional low-confidence/invalid result to human review or approval",
        )
    return passed("review", "conditional human-review routing signal found")


def check_output(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "output"):
        return False
    text = source.lower()
    required = ("status", "fields", "confidence")
    if not ("json" in text and all(field in text for field in required)):
        return fail(
            "output",
            "write structured JSON containing status, fields, and confidence",
        )
    return passed("output", "structured JSON output signal found")


def check_proof(path: Path, source: str, tree: ast.AST | None) -> bool:
    if not check_source(path, tree, "proof"):
        return False
    text = source.lower()
    if not (("trace" in text or "correlation" in text) and ("evaluat" in text or "accuracy" in text)):
        return fail(
            "proof",
            "include trace/correlation evidence and an evaluation or accuracy summary",
        )
    return passed("proof", "trace and evaluation evidence signals found")


CHECKS = {
    "intake": check_intake,
    "no-secrets": check_no_secrets,
    "confidence": check_confidence,
    "review": check_review,
    "output": check_output,
    "proof": check_proof,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Offline AST/text checks for a learner-authored document_workflow.py."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", choices=CHECKS, help="Run one named checkpoint.")
    group.add_argument("--all", action="store_true", help="Run every checkpoint.")
    parser.add_argument(
        "--path",
        default=str(HERE),
        help=f"Directory containing {SOURCE_NAME}, or the file itself (default: activity directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="State the offline mode explicitly; no service calls are ever made.",
    )
    args = parser.parse_args()
    path, source, tree = load_source(args.path)

    if args.dry_run:
        print("Dry run: static AST/text checks only; no Azure SDK, network, or service calls.\n")
    else:
        print("Offline static validation; no Azure SDK, network, or service calls.\n")

    names = list(CHECKS) if args.all else [args.step]
    results = [CHECKS[name](path, source, tree) for name in names]
    ok = all(results)
    print("\nALL CHECKPOINTS PASS" if ok else "\nONE OR MORE CHECKPOINTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
