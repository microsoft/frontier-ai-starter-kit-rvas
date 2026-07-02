#!/usr/bin/env python3
"""Structural checkpoints for the Tier 3 Capstone · Northfield IQ, the Team (MAF).

    python validate.py --all                 # all required structural checks
    python validate.py --all --path ./mycap  # point at the learner's capstone dir
    python validate.py --step 1              # >=3 agent/executor roles defined
    python validate.py --step 2              # parallel fan-out topology present
    python validate.py --step 3              # typed (Pydantic) contracts in use
    python validate.py --list                # which criteria are auto vs coach-judged

This is a LIGHT, headless validator for the STRUCTURAL subset of the capstone
acceptance criteria (PLAN-V3 §3.7 / README "Acceptance criteria"). It is a design
brief, not a fixed scaffold, so this script does NOT expect specific filenames —
it scans every *.py under --path and grades by AST + text heuristics. The visual
(DevUI), narrated-demo, tracing, and hosted-background criteria are confirmed LIVE
with a coach and are intentionally NOT asserted here.

Stdlib only (argparse, ast, pathlib, re) — runs anywhere, no external deps.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- name heuristics ---------------------------------------------------------
ROUTER_RE = re.compile(r"triage|router|route|classif|dispatch", re.IGNORECASE)
SPECIALIST_RE = re.compile(
    r"knowledge|action|escalat|synth|specialist|search|retriev|agent|executor",
    re.IGNORECASE,
)
EDGE_BUILDERS = {"add_edge", "add_fan_out_edges", "add_fan_in_edges", "add_chain"}
START_BUILDERS = {"set_start_executor", "set_start", "set_start_node"}
EXECUTOR_FACTORY_RE = re.compile(r"(Executor|Agent)$")
KB_RE = re.compile(
    r"AZURE_SEARCH|AzureAISearch|university-faq|SearchClient|SearchIndex|"
    r"foundry[_ ]?iq|knowledge.?base|search.?index|grounding|ai\.search",
    re.IGNORECASE,
)
APPROVAL_RE = re.compile(
    r"RequiredFunctionToolCall|RequiredMcpToolCall|ToolOutput|SubmitToolOutputsAction|"
    r"SubmitToolApprovalAction|submit_tool_outputs|"
    r"ACTION_MCP_URL|ACTION_API_URL|northfield_actions|McpTool|FunctionTool|approval",
    re.IGNORECASE,
)
PYDANTIC_RE = re.compile(r"BaseModel|pydantic", re.IGNORECASE)
SEND_RE = re.compile(r"send_message|yield_output")
REGEX_PARSE_RE = re.compile(r"re\.(search|match|findall|split)\s*\(")


def _fail(step: str, msg: str) -> bool:
    print(f"❌ Step {step} FAIL — {msg}")
    return False


def _ok(step: str, msg: str) -> bool:
    print(f"✅ Step {step} PASS — {msg}")
    return True


def _node_name(node: ast.AST) -> str:
    """Best-effort readable identifier for an AST node."""
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover - defensive, ast.unparse is 3.9+
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return node.attr
        return ""


def _call_func_name(call: ast.Call) -> str:
    func = call.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return ""


class Scan:
    """Aggregated structural evidence across all *.py in the learner's capstone dir."""

    def __init__(self) -> None:
        self.files: list[Path] = []
        self.text: str = ""
        self.executors: set[str] = set()       # discovered agent/executor identifiers
        self.edges: list[tuple[str, str]] = []  # (src, dst) graph edges
        self.starts: set[str] = set()
        self.has_pydantic_model = False
        self.has_send = False
        self.has_regex_parse = False
        self.parsed_ok = 0
        self.parse_errors: list[str] = []

    @property
    def out_degree(self) -> dict[str, int]:
        seen: dict[str, set[str]] = {}
        for src, dst in self.edges:
            if src != dst:
                seen.setdefault(src, set()).add(dst)
        return {k: len(v) for k, v in seen.items()}

    @property
    def in_degree(self) -> dict[str, int]:
        seen: dict[str, set[str]] = {}
        for src, dst in self.edges:
            if src != dst:
                seen.setdefault(dst, set()).add(src)
        return {k: len(v) for k, v in seen.items()}


def _collect(scan: Scan, tree: ast.AST) -> None:
    for node in ast.walk(tree):
        # class X(BaseModel) -> typed contract; class X(Executor) -> executor role
        if isinstance(node, ast.ClassDef):
            base_names = {_node_name(b) for b in node.bases}
            if any("BaseModel" in b for b in base_names):
                scan.has_pydantic_model = True
            if any(re.search(r"Executor|Agent", b) for b in base_names):
                scan.executors.add(node.name)
        # @executor / @agent decorated functions
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                dname = _node_name(dec)
                if re.search(r"\bexecutor\b|\bagent\b", dname, re.IGNORECASE):
                    scan.executors.add(node.name)
        # assignment: foo = SomethingExecutor(...) / SomethingAgent(...)
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            fname = _call_func_name(node.value)
            if EXECUTOR_FACTORY_RE.search(fname) or re.search(
                r"ChatAgent|AzureAIAgent|create_agent", fname
            ):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        scan.executors.add(tgt.id)
        # calls: add_edge / set_start_executor / send_message / yield_output
        if isinstance(node, ast.Call):
            fname = _call_func_name(node)
            if fname in EDGE_BUILDERS and len(node.args) >= 2:
                src = _node_name(node.args[0])
                # support fan-out helpers: add_edge(a, b) or add_fan_out_edges(a, [b, c])
                dst_arg = node.args[1]
                if isinstance(dst_arg, (ast.List, ast.Tuple, ast.Set)):
                    for elt in dst_arg.elts:
                        scan.edges.append((src, _node_name(elt)))
                        scan.executors.update({src, _node_name(elt)})
                else:
                    dst = _node_name(dst_arg)
                    scan.edges.append((src, dst))
                    scan.executors.update({src, dst})
            if fname in START_BUILDERS and node.args:
                start = _node_name(node.args[0])
                scan.starts.add(start)
                scan.executors.add(start)
            if fname in {"send_message", "yield_output"}:
                scan.has_send = True


def scan_path(path: Path) -> Scan:
    scan = Scan()
    if path.is_file() and path.suffix == ".py":
        pyfiles = [path]
    else:
        pyfiles = sorted(
            p for p in path.rglob("*.py") if p.name != Path(__file__).name
        )
    for p in pyfiles:
        try:
            src = p.read_text(encoding="utf-8")
        except Exception:
            continue
        scan.files.append(p)
        scan.text += "\n" + src
        try:
            tree = ast.parse(src, filename=str(p))
        except SyntaxError as exc:
            scan.parse_errors.append(f"{p.name}: {exc}")
            continue
        scan.parsed_ok += 1
        _collect(scan, tree)
    # text-level fallbacks (catch graphs/contracts the AST walk may miss)
    if PYDANTIC_RE.search(scan.text):
        scan.has_pydantic_model = scan.has_pydantic_model or bool(
            re.search(r"class\s+\w+\s*\(\s*[\w.]*BaseModel", scan.text)
        )
    if SEND_RE.search(scan.text):
        scan.has_send = True
    if REGEX_PARSE_RE.search(scan.text):
        scan.has_regex_parse = True
    return scan


# --- the three required structural checks ------------------------------------

def check_agents(scan: Scan) -> bool:
    if not scan.files:
        return _fail("1", "no *.py files found under --path — point at the capstone dir")
    roles = sorted(scan.executors)
    routers = [r for r in roles if ROUTER_RE.search(r)]
    specialists = [r for r in roles if r not in routers and SPECIALIST_RE.search(r)]
    if len(roles) < 3:
        return _fail(
            "1",
            f"found {len(roles)} agent/executor role(s) {roles or '[]'}; need ≥3 "
            "(≥1 triage/router + ≥2 specialists)",
        )
    if not routers:
        return _fail(
            "1",
            f"found {len(roles)} roles but none named like a router/triage "
            "(triage|router|classif|dispatch) — name your classifier explicitly",
        )
    if len(specialists) < 2:
        return _fail(
            "1",
            f"found router {routers} but only {len(specialists)} specialist role(s) — need ≥2",
        )
    return _ok(
        "1",
        f"{len(roles)} roles discovered — router={routers[0]!r}, "
        f"specialists≥2 ({specialists[:3]})",
    )


def check_fanout(scan: Scan) -> bool:
    if not scan.edges:
        return _fail(
            "2",
            "no graph edges found (add_edge / add_fan_out_edges) — wire the WorkflowBuilder",
        )
    out_deg = scan.out_degree
    in_deg = scan.in_degree
    fan_out_srcs = [n for n, d in out_deg.items() if d >= 2]
    fan_in_dsts = [n for n, d in in_deg.items() if d >= 2]
    if not fan_out_srcs:
        return _fail(
            "2",
            "no node fans out to ≥2 specialists — triage must add_edge to ≥2 executors",
        )
    fanin = (
        f"; fan-in at {fan_in_dsts[0]!r} (≥2 incoming)"
        if fan_in_dsts
        else "; ⚠ no fan-in/synthesizer join detected yet (add converging edges)"
    )
    return _ok(
        "2",
        f"fan-out from {fan_out_srcs[0]!r} → {out_deg[fan_out_srcs[0]]} branches{fanin}",
    )


def check_typed_contracts(scan: Scan) -> bool:
    if not scan.has_pydantic_model:
        return _fail(
            "3",
            "no Pydantic BaseModel message type found — define typed contracts, not prose",
        )
    if not scan.has_send:
        return _fail(
            "3",
            "Pydantic models defined but no send_message/yield_output — pass typed objects between hops",
        )
    warn = (
        "  ⚠ hint: re.search/match seen in source — ensure it's not parsing prose between hops"
        if scan.has_regex_parse
        else ""
    )
    msg = "typed Pydantic contracts in use (BaseModel + send_message/yield_output)"
    print(f"✅ Step 3 PASS — {msg}")
    if warn:
        print(warn)
    return True


# --- advisory (NOT required for exit 0; README marks these coach-confirmed) ---

def advise_reuse(scan: Scan, track: str) -> None:
    kb = bool(KB_RE.search(scan.text))
    approval = bool(APPROVAL_RE.search(scan.text))
    kb_mark = "✅" if kb else "➖"
    ap_mark = "✅" if approval else "➖"
    print("\n— advisory (coach-confirmed live, not gating) —")
    if track == "customer":
        print(f"  {kb_mark} Knowledge specialist reuses your grounded retrieval (AI Search / Foundry IQ)")
        print(f"  {ap_mark} Action specialist reuses your governed action loop (FunctionTool/MCP + approval)")
        if "northfield" in scan.text.lower() or "university-faq" in scan.text.lower():
            print("  ⚠ --track customer: Northfield defaults still appear in source; adapt roles/corpus before demo")
    else:
        print(f"  {kb_mark} Knowledge specialist reuses Foundations KB (AI Search / Foundry IQ)")
        print(f"  {ap_mark} Action specialist reuses Action Tools approval loop (FunctionTool + approval)")
    if not (kb and approval):
        print("    note: reuse is graded LIVE with your coach — these are hints, not failures")


CHECKS = {1: check_agents, 2: check_fanout, 3: check_typed_contracts}

LIST_TEXT = """\
Capstone · Multi-Agent — what validate.py grades

AUTO-GRADED (structural, headless — this script):
  Step 1  ≥3 agent/executor roles (≥1 triage/router + ≥2 specialists)
  Step 2  parallel fan-out topology present (a node with ≥2 outgoing edges;
          fan-in/synthesizer join reported as a hint)
  Step 3  typed Pydantic contracts between agents (BaseModel + send_message/
          yield_output; no free-text-only message passing)

ADVISORY (printed, NOT gating — README marks these coach-confirmed):
  +  ≥1 specialist reuses the Foundations KB; ≥1 reuses the Action Tools approval loop
COACH-JUDGED / MANUAL (live with your coach — never asserted here):
  manual  Both sequential AND parallel topologies shown
  manual  Run visualized in DevUI (green/purple/black state)
  manual  Traced end-to-end — multi-agent span tree by operation_Id
  manual  2-minute demo narrates one question's journey through the team
  manual  (Stretch) hosted background/long-running run that survives a closed tab
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the structural subset of the Capstone acceptance criteria."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=sorted(CHECKS))
    group.add_argument("--all", action="store_true")
    group.add_argument("--list", action="store_true",
                       help="List which criteria are auto-graded vs coach-judged.")
    parser.add_argument(
        "--path", default=str(HERE),
        help="Path or dir of the learner's capstone source (default: this challenge dir).",
    )
    parser.add_argument("--track", choices=("upskill", "customer"), default="upskill",
                        help="upskill = Northfield reference; customer = your own scenario "
                             "(relaxes the Northfield corpus assumption, expects --question).")
    args = parser.parse_args()

    if args.list:
        if args.track == "customer":
            print("(track: customer — validating YOUR scenario, not Northfield)\n")
        print(LIST_TEXT)
        return 0
    if args.track == "customer":
        print("(track: customer — validating YOUR scenario, not Northfield)\n")

    path = Path(args.path).expanduser().resolve()
    if not path.exists():
        print(f"❌ --path not found: {path}")
        return 1
    scan = scan_path(path)
    if scan.parse_errors:
        print("(note: some files could not be parsed and were skipped)")
        for e in scan.parse_errors:
            print(f"  ⚠ {e}")
        print()

    if args.all:
        ok = all(CHECKS[s](scan) for s in sorted(CHECKS))
        advise_reuse(scan, args.track)
        if ok:
            print("\n✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, "
                  "typed contracts in use")
        else:
            print("\n❌ ONE OR MORE STRUCTURAL CHECKS FAILED")
        return 0 if ok else 1

    return 0 if CHECKS[args.step](scan) else 1


if __name__ == "__main__":
    raise SystemExit(main())
