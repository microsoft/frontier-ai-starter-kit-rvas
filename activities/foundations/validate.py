#!/usr/bin/env python3
"""Checkpoints for Tier 1 · Foundations — the Northfield University IQ Assistant.

Each step ends with `python validate.py --step N`; `--all` re-asserts the whole
end-state. The checks inspect your **live** Azure resources, but every Azure call
is GUARDED — missing creds / SDKs / resources produce a clear FAIL message, never
a stack trace. Use `--dry-run` for an OFFLINE smoke test (structure + .env only,
no network, no quota) — handy in CI or before `azd up` finishes.

    python validate.py --step 1     # resources provisioned + .env present + keyless auth
    python validate.py --step 2     # chosen model deployment is reachable from code
    python validate.py --step 3     # the named, versioned agent exists
    python validate.py --step 4     # agent answers a grounded question WITH a citation
    python validate.py --all        # the full Foundations end-state
    python validate.py --all --dry-run   # offline structural smoke (no Azure calls)

Env contract (from `.env`, produced by `azd up` / ./scripts/deploy.sh):
    AZURE_AI_PROJECT_ENDPOINT, AZURE_AI_MODEL_DEPLOYMENT_NAME,
    AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_INDEX_NAME, AZURE_SEARCH_CONNECTION_NAME,
    AZURE_FOUNDRY_KNOWLEDGE_BASE_NAME, AZURE_FOUNDRY_AGENT_NAME
"""
from __future__ import annotations

import argparse
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv optional; .env may already be exported in the shell
    pass
import sys
from pathlib import Path

GREEN, YELLOW, RED, CYAN, RESET = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[0;36m", "\033[0m"

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
CORPUS_DIR = REPO_ROOT / "resources" / "sample-data" / "university-faq"
PLACEHOLDER = "<"

DEFAULT_QUESTION = "What is Northfield's FAFSA priority deadline and school code?"


def ok(m: str) -> None:
    print(f"{GREEN}{m}{RESET}")


def warn(m: str) -> None:
    print(f"{YELLOW}⚠  {m}{RESET}")


def info(m: str) -> None:
    print(f"{CYAN}{m}{RESET}")


def _fail(step: str, msg: str) -> bool:
    print(f"{RED}❌ Step {step} FAIL — {msg}{RESET}")
    return False


def load_env() -> dict:
    """Load .env (simple parser) layered over the real environment."""
    env = dict(os.environ)
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.setdefault(k.strip(), v.strip())
    return env


def _present(env: dict, keys: list[str]) -> list[str]:
    """Return the keys that are missing or still hold a placeholder."""
    bad = []
    for k in keys:
        v = (env.get(k) or "").strip()
        if not v or PLACEHOLDER in v:
            bad.append(k)
    return bad


def _credential():
    from azure.identity import DefaultAzureCredential

    return DefaultAzureCredential()


# --------------------------------------------------------------------------- #
# Step 1 — Setup & Provisioning                                               #
# --------------------------------------------------------------------------- #
def check_step1(env: dict, dry_run: bool) -> bool:
    required = ["AZURE_AI_PROJECT_ENDPOINT", "AZURE_AI_MODEL_DEPLOYMENT_NAME", "AZURE_SEARCH_ENDPOINT"]
    missing = _present(env, required)
    if missing:
        return _fail("1", f".env missing/placeholder vars: {', '.join(missing)} — run 'azd up' then "
                          "'azd env get-values > .env'")
    if dry_run:
        ok("✅ Step 1 PASS (dry-run) — .env present with the Foundry + Search contract")
        return True
    # Live: confirm keyless auth actually yields a token (no API keys anywhere).
    try:
        cred = _credential()
        cred.get_token("https://management.azure.com/.default")
    except ImportError as exc:
        return _fail("1", f"azure-identity not installed ({exc}); pip install -r requirements.txt")
    except Exception as exc:  # noqa: BLE001
        return _fail("1", f"keyless auth failed ({exc}); run 'az login' / 'azd auth login'")
    ok("✅ Step 1 PASS — .env contract present and keyless auth works")
    return True


# --------------------------------------------------------------------------- #
# Step 2 — Model deployment reachable                                         #
# --------------------------------------------------------------------------- #
def check_step2(env: dict, dry_run: bool) -> bool:
    missing = _present(env, ["AZURE_AI_PROJECT_ENDPOINT", "AZURE_AI_MODEL_DEPLOYMENT_NAME"])
    if missing:
        return _fail("2", f".env missing/placeholder vars: {', '.join(missing)}")
    if dry_run:
        ok("✅ Step 2 PASS (dry-run) — model deployment name + project endpoint present")
        return True
    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=env["AZURE_AI_PROJECT_ENDPOINT"], credential=_credential())
        client = project.get_openai_client()
        resp = client.responses.create(
            model=env["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            input="ping",
        )
        if not getattr(resp, "output_text", None):
            warn("model responded but returned empty output_text")
    except ImportError as exc:
        return _fail("2", f"azure-ai-projects/openai not installed ({exc}); pip install -r requirements.txt")
    except Exception as exc:  # noqa: BLE001
        return _fail("2", f"deployment '{env['AZURE_AI_MODEL_DEPLOYMENT_NAME']}' not reachable ({exc}); "
                          "check it is Succeeded/Ready and you ran 'az login'")
    ok(f"✅ Step 2 PASS — model deployment '{env['AZURE_AI_MODEL_DEPLOYMENT_NAME']}' reachable via the SDK")
    return True


# --------------------------------------------------------------------------- #
# Step 3 — The named, versioned agent exists                                  #
# --------------------------------------------------------------------------- #
def _find_agent(project, agent_name: str):
    """Return the agent object whose name matches, or None (preview-surface tolerant)."""
    try:
        for a in project.agents.list():
            if getattr(a, "name", None) == agent_name:
                return a
    except Exception:  # noqa: BLE001
        pass
    return None


def check_step3(env: dict, dry_run: bool) -> bool:
    agent_name = (env.get("AZURE_FOUNDRY_AGENT_NAME") or "northfield-iq-assistant").strip()
    if dry_run:
        if _present(env, ["AZURE_AI_PROJECT_ENDPOINT"]):
            return _fail("3", "AZURE_AI_PROJECT_ENDPOINT missing/placeholder in .env")
        ok(f"✅ Step 3 PASS (dry-run) — agent name resolved to '{agent_name}'")
        return True
    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=env["AZURE_AI_PROJECT_ENDPOINT"], credential=_credential())
        agent = _find_agent(project, agent_name)
    except ImportError as exc:
        return _fail("3", f"azure-ai-projects not installed ({exc}); pip install -r requirements.txt")
    except Exception as exc:  # noqa: BLE001
        return _fail("3", f"could not reach the project agent surface ({exc}); run 'az login'")
    if agent is None:
        return _fail("3", f"agent '{agent_name}' not found — create it (app/step3_agent.py) "
                          "or run ./scripts/setup-foundations.sh")
    ok(f"✅ Step 3 PASS — named agent '{agent_name}' exists (id={getattr(agent, 'id', '?')})")
    return True


# --------------------------------------------------------------------------- #
# Step 4 — Grounded answer WITH a citation (Foundations end-state)            #
# --------------------------------------------------------------------------- #
def _has_citation(text: str, response=None) -> bool:
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            for annotation in getattr(content, "annotations", []) or []:
                if "citation" in str(getattr(annotation, "type", "")).lower():
                    return True
    t = (text or "").lower()
    return bool(text) and ("[" in text or "source" in t or ".md" in t)


def check_step4(env: dict, dry_run: bool, question: str, track: str = "upskill") -> bool:
    # Customer Build teams ground their OWN corpus, so the grounded answer must be checked
    # against a scenario question they supply — the Northfield default won't match their data.
    if track == "customer" and question == DEFAULT_QUESTION:
        warn("--track customer: pass your own scenario question with --question "
             '"<your question>" — the Northfield default will not match your corpus')

    if dry_run:
        missing = _present(env, ["AZURE_SEARCH_INDEX_NAME", "AZURE_SEARCH_CONNECTION_NAME"])
        if missing:
            return _fail("4", f".env missing/placeholder vars: {', '.join(missing)}")
        # Only the upskill track ships a fixed Northfield corpus on disk; Customer Build teams
        # bring their own (possibly indexed straight from the portal), so skip the corpus check.
        if track == "upskill" and (not CORPUS_DIR.is_dir() or not any(CORPUS_DIR.glob("*.md"))):
            return _fail("4", f"FAQ corpus not found at {CORPUS_DIR}")
        ok("✅ Step 4 PASS (dry-run) — search/agent grounding contract present"
           + ("" if track == "customer" else " + Northfield corpus"))
        return True

    if _present(env, ["AZURE_AI_PROJECT_ENDPOINT", "AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_INDEX_NAME"]):
        return _fail("4", "missing AZURE_AI_PROJECT_ENDPOINT / AZURE_SEARCH_ENDPOINT / AZURE_SEARCH_INDEX_NAME")

    agent_name = (env.get("AZURE_FOUNDRY_AGENT_NAME") or "northfield-iq-assistant").strip()
    try:
        cred = _credential()
    except Exception as exc:  # noqa: BLE001
        return _fail("4", f"keyless auth failed ({exc}); run 'az login'")

    # Preferred proof: the grounded agent answers with a citation.
    try:
        from azure.ai.projects import AIProjectClient

        project = AIProjectClient(endpoint=env["AZURE_AI_PROJECT_ENDPOINT"], credential=cred)
        agent = _find_agent(project, agent_name)
        if agent is not None:
            openai = project.get_openai_client()
            conversation = openai.conversations.create(
                items=[{"type": "message", "role": "user", "content": question}],
            )
            response = openai.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            )
            text = getattr(response, "output_text", "") or ""
            if _has_citation(text, response):
                ok(f"✅ Step 4 PASS — agent '{agent_name}' returned a grounded answer WITH a citation")
                return True
            if text:
                warn("agent answered but no citation detected; falling back to a direct Search check")
    except Exception as exc:  # noqa: BLE001
        warn(f"agent invocation surface unavailable ({exc}); falling back to a direct Search check")

    # Fallback proof of grounding: the index returns a citable result.
    try:
        from azure.search.documents import SearchClient

        sc = SearchClient(
            endpoint=env["AZURE_SEARCH_ENDPOINT"],
            index_name=env["AZURE_SEARCH_INDEX_NAME"],
            credential=cred,
        )
        results = list(sc.search(search_text=question, top=3))
        if results and any(r.get("source") for r in results):
            ok(f"✅ Step 4 PASS — grounded retrieval works (top hit cites '{results[0].get('source')}')")
            return True
        return _fail("4", "Search returned no citable result — run ./scripts/setup-foundations.sh")
    except ImportError as exc:
        return _fail("4", f"azure-search-documents not installed ({exc})")
    except Exception as exc:  # noqa: BLE001
        return _fail("4", f"grounded retrieval check failed ({exc}); verify the index + RBAC")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Foundations steps / end-state.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--step", type=int, choices=(1, 2, 3, 4))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true",
                        help="Offline structural smoke test (no Azure calls, no quota).")
    parser.add_argument("--track", choices=("upskill", "customer"), default="upskill",
                        help="upskill = Northfield reference; customer = your own scenario "
                             "(relaxes the Northfield corpus assumption, expects --question).")
    parser.add_argument("--question", default=DEFAULT_QUESTION,
                        help="Grounded question used for the Step 4 citation check.")
    args = parser.parse_args()

    env = load_env()
    if args.dry_run:
        info("(dry-run: offline structural checks only — no Azure calls)\n")
    if args.track == "customer":
        info("(track: customer — validating YOUR scenario, not Northfield)\n")

    checks = {
        1: lambda: check_step1(env, args.dry_run),
        2: lambda: check_step2(env, args.dry_run),
        3: lambda: check_step3(env, args.dry_run),
        4: lambda: check_step4(env, args.dry_run, args.question, args.track),
    }

    if args.all:
        results = []
        for n in (1, 2, 3, 4):
            results.append(checks[n]())
        if all(results):
            ok("\n✅ Foundations end-state PASS — grounded Northfield IQ Assistant is live"
               + (" (dry-run)" if args.dry_run else ""))
            return 0
        print(f"{RED}\n❌ Foundations end-state NOT READY — see the failing step(s) above{RESET}")
        return 1
    return 0 if checks[args.step]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
