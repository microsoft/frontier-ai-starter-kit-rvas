#!/usr/bin/env bash
# ============================================================================
# AI Starter Kit RVAS — Cleanup / cost-hygiene teardown.
#
# Backlog #7 [FWH §4.10]. Idempotent, `.env`-driven teardown so teams don't
# leak Azure spend after the event.
#
# SAFE BY DEFAULT: a bare run only PRINTS what it would tear down (dry-run).
# Nothing destructive happens until you pass --yes. The resource group is shown
# first and is NEVER deleted blindly.
#
#   ./scripts/cleanup.sh                 # dry-run: show targets, costs, no changes
#   ./scripts/cleanup.sh --yes           # actually tear down (azd down + local procs)
#   ./scripts/cleanup.sh --local-only    # only stop local Action Tools processes
#   ./scripts/cleanup.sh --yes --purge   # also --purge soft-deletable resources (Foundry/AI)
#
# Reuses ONLY the variable names from .env.sample (the .env contract). It does
# not invent, rename, or persist any new env vars.
# ============================================================================
set -Eeuo pipefail

# ---- pretty output (matches deploy.sh / setup-foundations.sh style) --------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; RESET='\033[0m'
info()  { printf "%b%s%b\n" "$CYAN"   "$1" "$RESET"; }
ok()    { printf "%b%s%b\n" "$GREEN"  "$1" "$RESET"; }
warn()  { printf "%b%s%b\n" "$YELLOW" "$1" "$RESET"; }
fail()  { printf "%b%s%b\n" "$RED"    "$1" "$RESET" >&2; exit 1; }
hr()    { printf "%b%s%b\n" "$CYAN" "────────────────────────────────────────────────────────" "$RESET"; }

# ---- flags ------------------------------------------------------------------
CONFIRM=false
LOCAL_ONLY=false
PURGE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes|-y)      CONFIRM=true; shift ;;
    --local-only)  LOCAL_ONLY=true; shift ;;
    --purge)       PURGE=true; shift ;;
    -h|--help)     grep -E '^#( |!)' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) fail "Unknown argument: $1   (try --help)" ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Run a command with a timeout when `timeout` is available; otherwise run as-is.
# Escalates to SIGKILL 5s after SIGTERM so a process that traps TERM still dies.
# Keeps azd calls from hanging when no environment can be resolved.
guarded() {
  if command -v timeout >/dev/null 2>&1; then timeout -k 5 "$@"; else shift; "$@"; fi
}

# ---- load .env (read-only — we never write it) ------------------------------
if [[ -f .env ]]; then
  set -a; # shellcheck disable=SC1091
  source .env; set +a
elif command -v azd >/dev/null 2>&1 && guarded 15 azd env get-values </dev/null >/dev/null 2>&1; then
  warn "No .env found — sourcing azd environment values for target discovery."
  set -a; eval "$(guarded 15 azd env get-values </dev/null 2>/dev/null)"; set +a
else
  warn "No .env and no azd environment found — cloud targets unknown."
  warn "Local-process cleanup can still run; cloud teardown will be skipped."
fi

# Resolve targets from the .env contract names ONLY (see .env.sample).
RG="${AZURE_RESOURCE_GROUP:-}"
SUB="${AZURE_SUBSCRIPTION_ID:-}"
LOCATION="${AZURE_LOCATION:-}"
ENV_NAME="${AZURE_ENV_NAME:-}"
FOUNDRY_EP="${AZURE_AI_FOUNDRY_ENDPOINT:-}"
SEARCH_EP="${AZURE_SEARCH_ENDPOINT:-}"
ACR_NAME="${AZURE_CONTAINER_REGISTRY_NAME:-}"
MODEL_DEPLOYMENT="${AZURE_AI_MODEL_DEPLOYMENT_NAME:-}"
ACTION_API_URL="${ACTION_API_URL:-http://localhost:8080}"
ACTION_MCP_URL="${ACTION_MCP_URL:-http://localhost:8765/mcp}"

# Derive local ports from the Action Tools URLs (no new env names introduced).
API_PORT="$(printf '%s' "$ACTION_API_URL" | sed -E 's#.*:([0-9]+).*#\1#')"
MCP_PORT="$(printf '%s' "$ACTION_MCP_URL" | sed -E 's#.*:([0-9]+).*#\1#')"
[[ "$API_PORT" =~ ^[0-9]+$ ]] || API_PORT=8080
[[ "$MCP_PORT" =~ ^[0-9]+$ ]] || MCP_PORT=8765

# ============================================================================
# 1. SHOW THE PLAN (always — this is the safe-by-default surface)
# ============================================================================
hr
info "AI Starter Kit RVAS — cleanup / cost-hygiene"
hr
echo ""
info "Cloud teardown targets (from the .env contract):"
echo "  Subscription      : ${SUB:-<unknown>}"
echo "  Resource group    : ${RG:-<unknown>}      <-- NOT deleted unless you confirm"
echo "  Location          : ${LOCATION:-<unknown>}"
echo "  azd env name      : ${ENV_NAME:-<unknown>}"
echo "  Foundry endpoint  : ${FOUNDRY_EP:-<none>}"
echo "  Model deployment  : ${MODEL_DEPLOYMENT:-<none>}"
echo "  AI Search         : ${SEARCH_EP:-<none>}"
echo "  Container registry: ${ACR_NAME:-<none>}"
echo ""
info "Local Action Tools processes (cost-free, but tidy to stop):"
echo "  REST backend (app.py / uvicorn) : port ${API_PORT}"
echo "  FastMCP server (mcp_server.py)  : port ${MCP_PORT}"
echo ""
warn "What keeps costing money if you leave this UP:"
echo "  • Model deployment capacity (PTU/GlobalStandard) — bills while provisioned."
echo "  • Azure AI Search service (Basic tier) — hourly charge regardless of queries."
echo "  • Azure Container Registry (Basic) — daily storage charge."
echo "  • Log Analytics / App Insights — ingestion + retention."
echo "  • Foundry resource + project — minimal idle, but soft-deletes linger until --purge."
echo ""
hr

# ============================================================================
# 2. DRY-RUN GATE — stop here unless --yes (or the explicit, safe --local-only)
# ============================================================================
if [[ "$CONFIRM" != true && "$LOCAL_ONLY" != true ]]; then
  warn "DRY-RUN — nothing was changed."
  echo ""
  echo "  Re-run with --yes to tear down cloud infra (azd down) + stop local procs."
  echo "  Re-run with --local-only to ONLY stop the local Action Tools processes."
  echo "  Add --purge to also hard-purge soft-deleted Foundry/AI resources."
  exit 0
fi

# ============================================================================
# 3. LOCAL PROCESS CLEANUP (safe; runs for --yes and --local-only)
# ============================================================================
stop_port() {
  local port="$1" label="$2" pids=""
  if command -v lsof >/dev/null 2>&1; then
    pids="$(lsof -t -i ":${port}" 2>/dev/null || true)"
  elif command -v fuser >/dev/null 2>&1; then
    pids="$(fuser "${port}/tcp" 2>/dev/null || true)"
  fi
  if [[ -n "$pids" ]]; then
    warn "Stopping ${label} on port ${port} (PIDs: ${pids})..."
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true
    sleep 2
    # shellcheck disable=SC2086
    kill -9 $pids 2>/dev/null || true
    ok "  ${label} stopped."
  else
    info "  ${label} on port ${port}: not running — nothing to stop."
  fi
}

info "Stopping local Action Tools processes..."
stop_port "$API_PORT" "Action REST backend"
stop_port "$MCP_PORT" "Action MCP server"

# Best-effort: stop a local Action Tools container if one is running.
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  RUNNING="$(docker ps --filter 'name=action' --format '{{.Names}}' 2>/dev/null | grep -E '.' || true)"
  if [[ -n "$RUNNING" ]]; then
    warn "Stopping Action Tools container(s): ${RUNNING}"
    # shellcheck disable=SC2086
    docker stop $RUNNING >/dev/null 2>&1 || warn "  docker stop returned non-zero (ignored)."
    ok "  Container(s) stopped."
  else
    info "  No 'action' Docker container running — nothing to stop."
  fi
else
  info "  Docker not running/installed — skipping container cleanup."
fi

if [[ "$LOCAL_ONLY" == true ]]; then
  ok ""
  ok "✅ Local-only cleanup complete. Cloud infra left untouched."
  exit 0
fi

# ============================================================================
# 4. CLOUD TEARDOWN (gated; guarded; idempotent)
# ============================================================================
if ! command -v az >/dev/null 2>&1; then
  fail "Azure CLI (az) not found — cloud teardown did not run. Install it, then retry."
fi
if ! az account show >/dev/null 2>&1; then
  fail "Not logged in to Azure — cloud teardown did not run. Run 'az login', then retry."
fi
if [[ -z "$RG" ]]; then
  fail "AZURE_RESOURCE_GROUP is empty — refusing to guess a teardown target. Aborting."
fi
if ! az group show -n "$RG" >/dev/null 2>&1; then
  ok "Resource group '${RG}' does not exist — already cleaned up. Nothing to do."
  exit 0
fi

# Prefer azd down (knows the provisioned footprint); fall back to RG delete.
if command -v azd >/dev/null 2>&1 && [[ -f "${REPO_ROOT}/azure.yaml" ]]; then
  warn "Tearing down via 'azd down' (purge=${PURGE}) — this deletes the provisioned footprint."
  if [[ "$PURGE" == true ]]; then
    guarded 1800 azd down --force --purge </dev/null \
      || fail "azd down failed — cloud teardown is incomplete. Review the output and retry."
  else
    guarded 1800 azd down --force </dev/null \
      || fail "azd down failed — cloud teardown is incomplete. Review the output and retry."
  fi
else
  warn "azd not available — deleting resource group '${RG}' directly."
  az group delete -n "$RG" --yes --no-wait \
    && ok "Resource group delete submitted (--no-wait)." \
    || fail "Resource group delete failed — cloud teardown was not submitted."
fi

# Optional: hard-purge soft-deleted Cognitive Services / Foundry accounts so the
# name frees up and no soft-delete retention lingers. Guarded behind --purge.
if [[ "$PURGE" == true ]] && [[ -n "$LOCATION" ]]; then
  info "Purging any soft-deleted Cognitive Services / Foundry accounts in ${LOCATION}..."
  DELETED="$(az cognitiveservices account list-deleted \
    --query "[?resourceGroup=='${RG}'].name" -o tsv 2>/dev/null || true)"
  if [[ -n "$DELETED" ]]; then
    while IFS= read -r acct; do
      [[ -z "$acct" ]] && continue
      warn "  Purging soft-deleted account: ${acct}"
      az cognitiveservices account purge -n "$acct" -g "$RG" -l "$LOCATION" \
        >/dev/null 2>&1 || warn "    purge returned non-zero for ${acct} (ignored)."
    done <<< "$DELETED"
    ok "  Soft-deleted account purge attempted."
  else
    info "  No soft-deleted accounts found for RG '${RG}'."
  fi
fi

ok ""
ok "✅ Teardown complete (or submitted)."
info "   Verify cost is stopped:  az group list -o table   (RG '${RG}' should be gone)"
info "   Re-provision any time with:  azd up   (or ./scripts/deploy.sh)"
