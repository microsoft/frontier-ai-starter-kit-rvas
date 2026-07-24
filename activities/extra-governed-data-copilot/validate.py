#!/usr/bin/env python3
"""Offline structural checkpoints for Extra · Governed Data Copilot.

    python validate.py --step 1 --path activities/extra-governed-data-copilot
    python validate.py --all --dry-run

This validator never imports learner code or makes Azure, connector, model, or network calls.
It checks the learner-authored governed_data_copilot.py with conservative AST/text heuristics.
"""
from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET_NAME = "governed_data_copilot.py"

SECRET_ASSIGNMENT = re.compile(
    r"""(?ix)
    \b(?:api[_-]?key|client[_-]?secret|connection[_-]?string|password|access[_-]?token)\b
    \s*=\s*
    (?!\s*(?:os\.environ|os\.getenv|environ\.get|None\b|""|''))["'][^"'\n]{8,}["']
    """
)


def fail(step: int, message: str) -> bool:
    print(f"❌ Step {step} FAIL — {message}")
    return False


def source_at(path: Path) -> tuple[str, ast.AST] | tuple[None, None]:
    target = path / TARGET_NAME
    if not target.exists():
        return None, None
    source = target.read_text(encoding="utf-8")
    try:
        return source, ast.parse(source, filename=str(target))
    except SyntaxError as exc:
        print(f"❌ Artifact FAIL — {TARGET_NAME} is not valid Python: {exc}")
        return None, None


def assigned_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    names.add(target.id.upper())
    return names


def has_default_credential(tree: ast.AST, source: str) -> bool:
    imported = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "azure.identity"
        and any(alias.name == "DefaultAzureCredential" for alias in node.names)
        for node in ast.walk(tree)
    )
    constructed = any(
        isinstance(node, ast.Call)
        and (
            isinstance(node.func, ast.Name) and node.func.id == "DefaultAzureCredential"
            or isinstance(node.func, ast.Attribute) and node.func.attr == "DefaultAzureCredential"
        )
        for node in ast.walk(tree)
    )
    return imported and constructed and "DefaultAzureCredential" in source


def check_step1(path: Path) -> bool:
    source, tree = source_at(path)
    if source is None or tree is None:
        return fail(1, f"missing or invalid {path / TARGET_NAME}")
    names = assigned_names(tree)
    has_query_allowlist = any(
        marker in names for marker in ("ALLOWED_QUERIES", "APPROVED_QUERIES", "QUERY_ALLOWLIST")
    )
    has_field_allowlist = any(
        marker in names for marker in ("APPROVED_FIELDS", "ALLOWED_FIELDS", "FIELD_ALLOWLIST")
    )
    if not (has_query_allowlist and has_field_allowlist):
        return fail(1, "define explicit query and field allowlists (for example ALLOWED_QUERIES and APPROVED_FIELDS)")
    if "semantic_model" not in source.lower() and "model_version" not in source.lower():
        return fail(1, "record the semantic model and/or its version in the governed contract or provenance")
    print("✅ Step 1 PASS — explicit query/field allowlists and semantic-model contract found")
    return True


def check_step2(path: Path) -> bool:
    source, tree = source_at(path)
    if source is None or tree is None:
        return fail(2, f"missing or invalid {path / TARGET_NAME}")
    if not has_default_credential(tree, source):
        return fail(2, "use and construct DefaultAzureCredential for keyless data access")
    if SECRET_ASSIGNMENT.search(source):
        return fail(2, "possible hardcoded secret found; use keyless identity rather than embedding credentials")
    print("✅ Step 2 PASS — DefaultAzureCredential present and no obvious hardcoded secret assignment")
    return True


def check_step3(path: Path) -> bool:
    source, tree = source_at(path)
    if source is None or tree is None:
        return fail(3, f"missing or invalid {path / TARGET_NAME}")
    lower = source.lower()
    guard_names = {
        node.name.lower()
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    named_guard = any(
        token in name for name in guard_names
        for token in ("validate", "allow", "approve", "guard")
    )
    parameterized = any(
        token in lower
        for token in ("parameters=", "params=", "query_id", "registered_query", "bound parameter")
    )
    rejection = any(token in lower for token in ("raise valueerror", "permissionerror", "not approved", "deny"))
    if not ((named_guard and rejection) or parameterized):
        return fail(3, "validate a named query/arguments before execution, or use an equivalent registered parameterized-query guard")
    if re.search(r"""(?i)(?:f["']|["']).*(?:select|dax|kql).*\{.*\}""", source):
        return fail(3, "possible interpolated query text found; use registered queries with typed parameters instead")
    print("✅ Step 3 PASS — registered/parameterized query validation guard found")
    return True


def check_step4(path: Path) -> bool:
    source, tree = source_at(path)
    if source is None or tree is None:
        return fail(4, f"missing or invalid {path / TARGET_NAME}")
    lower = source.lower()
    if "provenance" not in lower:
        return fail(4, "return result provenance (query ID, model/version, fields, parameters, and snapshot)")
    if not any(token in lower for token in ("accessdenied", "access_denied", "access denied", "permissionerror", "forbidden", "not authorized")):
        return fail(4, "handle access-denied/authorization outcomes explicitly")
    if not any(token in lower for token in ("uncertain", "stale", "incomplete", "ambiguous", "cannot verify")):
        return fail(4, "handle stale, incomplete, or uncertain results without treating them as zero")
    if not any(token in lower for token in ("requires_human_review", "human review", "human_review")):
        return fail(4, "mark sensitive or high-impact output for human review")
    print("✅ Step 4 PASS — provenance, access/uncertainty handling, and human-review path found")
    return True


CHECKS = {1: check_step1, 2: check_step2, 3: check_step3, 4: check_step4}


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline validator for Governed Data Copilot.")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--step", type=int, choices=sorted(CHECKS), help="Run one checkpoint.")
    choice.add_argument("--all", action="store_true", help="Run every checkpoint.")
    parser.add_argument("--path", type=Path, default=HERE,
                        help="Directory containing governed_data_copilot.py (default: this activity).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Explicitly confirm offline-only structural validation; no Azure calls are ever made.")
    args = parser.parse_args()
    path = args.path.resolve()
    if args.dry_run:
        print("(dry-run: offline AST/text checks only — no Azure or network calls)\n")
    if args.all:
        results = [CHECKS[step](path) for step in sorted(CHECKS)]
        ok = all(results)
        print("\n✅ ALL CHECKPOINTS PASS" if ok else "\n❌ ONE OR MORE CHECKPOINTS FAILED")
        return 0 if ok else 1
    return 0 if CHECKS[args.step](path) else 1


if __name__ == "__main__":
    raise SystemExit(main())
