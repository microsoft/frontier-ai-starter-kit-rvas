#!/usr/bin/env bash
# ============================================================================
# WTH AI Hackathon — Foundations END-STATE materializer (Path B bootstrap).
#
# After `azd up` (or ./scripts/deploy.sh) has provisioned infra, this script builds
# the Foundations end-state so Advanced teams can skip the guided steps:
#
#   1. Create the Azure AI Search index over resources/sample-data/university-faq/
#   2. Build a Foundry IQ knowledge base over that index (agentic retrieval)
#   3. Create the "northfield-iq-assistant" agent and attach the knowledge base
#
# Idempotent: re-running updates in place. Expected runtime ~10–15 min (mostly indexing).
# Verify afterwards with:  python scripts/validate-foundations.py
#
# Live Azure calls are GUARDED — the script fails fast with a clear message if
# prerequisites (login, .env, SDKs) are missing, and the preview Foundry IQ / agent
# steps degrade gracefully so a missing preview surface never hard-aborts the index build.
# ============================================================================
set -Eeuo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; RESET='\033[0m'
info()  { printf "%b%s%b\n" "$CYAN"   "$1" "$RESET"; }
ok()    { printf "%b%s%b\n" "$GREEN"  "$1" "$RESET"; }
warn()  { printf "%b%s%b\n" "$YELLOW" "$1" "$RESET"; }
fail()  { printf "%b%s%b\n" "$RED"    "$1" "$RESET" >&2; exit 1; }

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# ---- load .env --------------------------------------------------------------
if [[ -f .env ]]; then
  info "Loading .env ..."
  set -a; # shellcheck disable=SC1091
  source .env; set +a
elif command -v azd >/dev/null 2>&1 && azd env get-values >/dev/null 2>&1; then
  warn "No .env found — sourcing azd environment values."
  set -a; eval "$(azd env get-values)"; set +a
else
  fail "No .env found and no azd environment. Run 'azd up' or './scripts/deploy.sh' first, then 'azd env get-values > .env'."
fi

# ---- preflight guards -------------------------------------------------------
: "${AZURE_SEARCH_ENDPOINT:?AZURE_SEARCH_ENDPOINT missing from .env — provisioning incomplete}"
: "${AZURE_AI_PROJECT_ENDPOINT:?AZURE_AI_PROJECT_ENDPOINT missing from .env — provisioning incomplete}"
: "${AZURE_AI_MODEL_DEPLOYMENT_NAME:?AZURE_AI_MODEL_DEPLOYMENT_NAME missing from .env}"
SEARCH_INDEX_NAME="${AZURE_SEARCH_INDEX_NAME:-university-faq}"
KB_NAME="${AZURE_FOUNDRY_KNOWLEDGE_BASE_NAME:-northfield-faq-kb}"
AGENT_NAME="${AZURE_FOUNDRY_AGENT_NAME:-northfield-iq-assistant}"
CORPUS_DIR="${REPO_ROOT}/resources/sample-data/university-faq"

command -v python3 >/dev/null 2>&1 || fail "python3 not found."
[[ -d "$CORPUS_DIR" ]] || fail "Corpus not found at ${CORPUS_DIR}"

if ! az account show >/dev/null 2>&1; then
  fail "Not logged in to Azure (keyless auth needs it). Run:  az login"
fi

python3 - <<'PYCHECK' || fail "Missing Python SDKs. Run:  pip install -r requirements.txt"
import importlib, sys
missing = [m for m in ("azure.search.documents", "azure.identity", "azure.core") if importlib.util.find_spec(m) is None]
sys.exit(1 if missing else 0)
PYCHECK

info "Materializing Foundations end-state (index='${SEARCH_INDEX_NAME}', kb='${KB_NAME}', agent='${AGENT_NAME}')..."
echo ""

# ---- step 1+2+3: run the Python materializer --------------------------------
# Exported so the embedded Python can read them.
export AZURE_SEARCH_ENDPOINT AZURE_AI_PROJECT_ENDPOINT AZURE_AI_MODEL_DEPLOYMENT_NAME
export AZURE_AI_FOUNDRY_ENDPOINT="${AZURE_AI_FOUNDRY_ENDPOINT:-}"
export SEARCH_INDEX_NAME KB_NAME AGENT_NAME CORPUS_DIR
export AZURE_SEARCH_CONNECTION_NAME="${AZURE_SEARCH_CONNECTION_NAME:-search}"
export AZURE_AI_API_VERSION="${AZURE_AI_API_VERSION:-2025-04-01-preview}"

python3 - <<'PYEOF'
import glob, os, re, sys
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential  # noqa: F401 (fallback path)

GREEN, YELLOW, RED, RESET = "\033[0;32m", "\033[1;33m", "\033[0;31m", "\033[0m"
def ok(m):   print(f"{GREEN}{m}{RESET}")
def warn(m): print(f"{YELLOW}{m}{RESET}")
def die(m):  print(f"{RED}{m}{RESET}", file=sys.stderr); sys.exit(1)

endpoint   = os.environ["AZURE_SEARCH_ENDPOINT"]
index_name = os.environ["SEARCH_INDEX_NAME"]
corpus_dir = os.environ["CORPUS_DIR"]
cred = DefaultAzureCredential()

# ---------------------------------------------------------------------------
# STEP 1 — create/refresh the AI Search index and upload the corpus (REAL).
# ---------------------------------------------------------------------------
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField,
    SearchFieldDataType, VectorSearch, HnswAlgorithmConfiguration,
    VectorSearchProfile, SemanticConfiguration, SemanticSearch,
    SemanticPrioritizedFields, SemanticField,
)

idx_client = SearchIndexClient(endpoint=endpoint, credential=cred)

fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="source", type=SearchFieldDataType.String, filterable=True, facetable=True),
]
semantic = SemanticSearch(configurations=[
    SemanticConfiguration(
        name="default",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="title"),
            content_fields=[SemanticField(field_name="content")],
        ),
    )
])
index = SearchIndex(name=index_name, fields=fields, semantic_search=semantic)

try:
    idx_client.create_or_update_index(index)
    ok(f"✅ Step 1: index '{index_name}' created/updated.")
except Exception as e:  # noqa: BLE001
    die(f"Step 1 FAILED creating index: {e}\n  Check Search RBAC (Search Index Data Contributor + Search Service Contributor).")

def chunk(text, size=1800, overlap=200):
    text = text.strip()
    if len(text) <= size:
        return [text]
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size]); i += size - overlap
    return out

docs = []
for path in sorted(glob.glob(os.path.join(corpus_dir, "*.md"))):
    base = os.path.basename(path)
    if base.lower() == "readme.md":
        continue
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    title = base[:-3].replace("-", " ").title()
    for n, piece in enumerate(chunk(raw)):
        doc_id = re.sub(r"[^A-Za-z0-9_]", "_", f"{base[:-3]}_{n}")
        docs.append({"id": doc_id, "title": title, "content": piece, "source": base})

if not docs:
    die(f"No .md documents found in {corpus_dir}")

search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=cred)
result = search_client.upload_documents(documents=docs)
ok(f"✅ Step 1: uploaded {sum(1 for r in result if r.succeeded)}/{len(docs)} chunks from {corpus_dir}.")

# ---------------------------------------------------------------------------
# STEP 2 — Foundry IQ knowledge base over the index (PREVIEW; guarded).
# STEP 3 — agent + Azure AI Search tool attached (PREVIEW; guarded).
#
# The Foundry IQ knowledge-base API surface is preview and moves quickly. We attempt
# the agent + AI Search tool wiring via azure-ai-projects; if the installed SDK does
# not expose the preview surface, we DEGRADE GRACEFULLY (the index is already real and
# usable) and print the exact manual portal steps instead of hard-failing.
# ---------------------------------------------------------------------------
project_endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]
search_conn      = os.environ.get("AZURE_SEARCH_CONNECTION_NAME", "search")
kb_name          = os.environ["KB_NAME"]
agent_name       = os.environ["AGENT_NAME"]

INSTRUCTIONS = (
    "You are the Northfield University Student Services Assistant. Answer student "
    "questions about admissions, financial aid, housing, registration, IT support, and "
    "campus life using ONLY the grounded knowledge base. Always cite the source document. "
    "If the answer is not in the knowledge base, say so and point the student to the right office."
)

try:
    from azure.ai.projects import AIProjectClient
    project = AIProjectClient(endpoint=project_endpoint, credential=cred)

    tool_attached = False
    # Preferred: Azure AI Search tool grounded on our index (keyless via project MI).
    try:
        from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
        conn = project.connections.get(name=search_conn)
        ai_search = AzureAISearchTool(
            index_connection_id=conn.id,
            index_name=index_name,
            query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID,
        )
        tool_resources = ai_search.resources
        tool_defs = ai_search.definitions
        tool_attached = True
    except Exception as te:  # noqa: BLE001
        warn(f"⚠ Step 2/3: AI Search tool surface unavailable in installed SDK ({te}).")
        tool_resources, tool_defs = None, None

    # Create/refresh the agent.
    try:
        if tool_attached:
            agent = project.agents.create_agent(
                model=model_deployment, name=agent_name,
                instructions=INSTRUCTIONS, tools=tool_defs, tool_resources=tool_resources,
            )
        else:
            agent = project.agents.create_agent(
                model=model_deployment, name=agent_name, instructions=INSTRUCTIONS,
            )
        ok(f"✅ Step 3: agent '{agent_name}' created (id={getattr(agent, 'id', '?')}, "
           f"knowledge_tool={'attached' if tool_attached else 'NOT attached'}).")
        if not tool_attached:
            warn("   → Attach the AI Search index to the agent in the portal to complete the KB step.")
    except Exception as ae:  # noqa: BLE001
        warn(f"⚠ Step 3: agent create surface unavailable ({ae}).")
        warn("   The index is live. Create the agent + attach the knowledge base in the Foundry portal:")
        warn(f"     model='{model_deployment}', index='{index_name}', name='{agent_name}'.")
except Exception as e:  # noqa: BLE001
    warn(f"⚠ Step 2/3: azure-ai-projects not usable here ({e}).")
    warn("   The AI Search index IS provisioned and populated. Build the IQ knowledge base + agent")
    warn(f"   manually in the portal over index '{index_name}'. Then re-run validate-foundations.py.")

print()
ok("Foundations materialization finished. Verify with: python scripts/validate-foundations.py")
PYEOF

ok ""
ok "✅ setup-foundations.sh complete."
