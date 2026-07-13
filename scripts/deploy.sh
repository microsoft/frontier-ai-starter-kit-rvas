#!/usr/bin/env bash
# ============================================================================
# AI Starter Kit RVAS — Bash provisioning FALLBACK.
#
# Use this ONLY when `azd up` is unavailable or hits quota/region edge cases.
# It provisions the same footprint as infra/*.bicep using `az` + a few ARM REST
# calls (Foundry needs allowProjectManagement, not exposed by `az cognitiveservices`).
#
# It writes a fully-populated .env at the repo root using the SAME variable names
# as .env.sample (the .env contract).
#
# Idempotent-ish: re-running reuses existing resources by name where possible.
#
#   ./scripts/deploy.sh
#   ./scripts/deploy.sh --location eastus2 --model gpt-4o
# ============================================================================
set -Eeuo pipefail

# ---- pretty output ----------------------------------------------------------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; RESET='\033[0m'
info()  { printf "%b%s%b\n" "$CYAN"   "$1" "$RESET"; }
ok()    { printf "%b%s%b\n" "$GREEN"  "$1" "$RESET"; }
warn()  { printf "%b%s%b\n" "$YELLOW" "$1" "$RESET"; }
fail()  { printf "%b%s%b\n" "$RED"    "$1" "$RESET" >&2; exit 1; }

# ---- defaults (override via flags) -----------------------------------------
LOCATION="${AZURE_LOCATION:-swedencentral}"
ENV_NAME="${AZURE_ENV_NAME:-rvas-foundry}"
MODEL_NAME="${AZURE_AI_MODEL_NAME:-gpt-4o}"
MODEL_VERSION="${AZURE_AI_MODEL_VERSION:-2024-11-20}"
MODEL_DEPLOYMENT="${AZURE_AI_MODEL_DEPLOYMENT_NAME:-gpt-4o}"
MODEL_SKU="${AZURE_AI_MODEL_SKU:-GlobalStandard}"
MODEL_CAPACITY="${AZURE_AI_MODEL_CAPACITY:-30}"
SEARCH_INDEX_NAME="${AZURE_SEARCH_INDEX_NAME:-university-faq}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --location) LOCATION="$2"; shift 2 ;;
    --env-name) ENV_NAME="$2"; shift 2 ;;
    --model) MODEL_NAME="$2"; shift 2 ;;
    --model-version) MODEL_VERSION="$2"; shift 2 ;;
    --capacity) MODEL_CAPACITY="$2"; shift 2 ;;
    -h|--help) grep -E '^#( |!)' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) fail "Unknown argument: $1" ;;
  esac
done

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${REPO_ROOT}/.env"

# ---- preflight: graceful guards --------------------------------------------
command -v az >/dev/null 2>&1 || fail "Azure CLI (az) not found. Install: https://aka.ms/azcli"

if ! az account show >/dev/null 2>&1; then
  fail "Not logged in to Azure. Run:  az login   (then re-run this script)."
fi

SUBSCRIPTION_ID="$(az account show --query id -o tsv)"
TENANT_ID="$(az account show --query tenantId -o tsv)"
[[ -n "$SUBSCRIPTION_ID" ]] || fail "Could not resolve an active subscription. Run: az account set --subscription <id>"

SUFFIX="$(openssl rand -hex 3 2>/dev/null || echo "$RANDOM$RANDOM" | cut -c1-6)"
RG="rg-${ENV_NAME}"
FOUNDRY="aif-${SUFFIX}"
PROJECT="proj-${SUFFIX}"
SEARCH="srch-${SUFFIX}"
ACR="acr${SUFFIX}"
LAW="log-${SUFFIX}"
APPI="appi-${SUFFIX}"

info "Subscription : ${SUBSCRIPTION_ID}"
info "Location     : ${LOCATION}"
info "Resource grp : ${RG}"
info "Model        : ${MODEL_NAME} (${MODEL_VERSION}) -> deployment '${MODEL_DEPLOYMENT}'"
echo ""

PRINCIPAL_ID="$(az ad signed-in-user show --query id -o tsv 2>/dev/null || true)"

API="2025-04-01-preview"
ARM="https://management.azure.com"

# ---- resource group ---------------------------------------------------------
info "Creating resource group..."
az group create -n "$RG" -l "$LOCATION" -o none

# ---- Log Analytics + App Insights ------------------------------------------
info "Creating Log Analytics workspace..."
az monitor log-analytics workspace create -g "$RG" -n "$LAW" -l "$LOCATION" -o none
LAW_ID="$(az monitor log-analytics workspace show -g "$RG" -n "$LAW" --query id -o tsv)"

info "Creating Application Insights..."
az extension add -n application-insights --only-show-errors >/dev/null 2>&1 || true
az monitor app-insights component create --app "$APPI" -g "$RG" -l "$LOCATION" \
  --workspace "$LAW_ID" -o none
APPI_CONN="$(az monitor app-insights component show --app "$APPI" -g "$RG" --query connectionString -o tsv)"

# ---- Azure AI Search --------------------------------------------------------
info "Creating Azure AI Search (basic)..."
az search service create -g "$RG" -n "$SEARCH" -l "$LOCATION" \
  --sku basic --identity-type SystemAssigned -o none 2>/dev/null \
  || az search service create -g "$RG" -n "$SEARCH" -l "$LOCATION" --sku basic -o none
az search service update -g "$RG" -n "$SEARCH" \
  --identity-type SystemAssigned --semantic-search standard -o none
SEARCH_ENDPOINT="https://${SEARCH}.search.windows.net"

# ---- Azure Container Registry ----------------------------------------------
info "Creating Azure Container Registry..."
az acr create -g "$RG" -n "$ACR" --sku Basic -o none
ACR_LOGIN_SERVER="$(az acr show -n "$ACR" --query loginServer -o tsv)"

# ---- Foundry resource (ARM REST: needs allowProjectManagement) -------------
info "Creating Microsoft Foundry resource (AIServices, project mgmt on)..."
az rest --method put \
  --url "${ARM}/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}?api-version=${API}" \
  --body "$(cat <<JSON
{
  "location": "${LOCATION}",
  "kind": "AIServices",
  "sku": { "name": "S0" },
  "identity": { "type": "SystemAssigned" },
  "properties": {
    "allowProjectManagement": true,
    "customSubDomainName": "${FOUNDRY}",
    "publicNetworkAccess": "Enabled"
  }
}
JSON
)" -o none

info "Waiting for Foundry provisioning to succeed..."
for i in $(seq 1 36); do
  STATE="$(az rest --method get \
    --url "${ARM}/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}?api-version=${API}" \
    --query properties.provisioningState -o tsv 2>/dev/null || echo "Pending")"
  [[ "$STATE" == "Succeeded" ]] && break
  [[ "$STATE" == "Failed" ]] && fail "Foundry provisioning Failed."
  sleep 10
done
FOUNDRY_ENDPOINT="$(az cognitiveservices account show -n "$FOUNDRY" -g "$RG" --query properties.endpoint -o tsv)"

# ---- model deployment -------------------------------------------------------
info "Deploying model '${MODEL_NAME}'..."
az cognitiveservices account deployment create -g "$RG" -n "$FOUNDRY" \
  --deployment-name "$MODEL_DEPLOYMENT" \
  --model-name "$MODEL_NAME" --model-version "$MODEL_VERSION" --model-format OpenAI \
  --sku-name "$MODEL_SKU" --sku-capacity "$MODEL_CAPACITY" -o none \
  || warn "Model deployment failed (quota/region?). Set --model / --location and re-run; infra is otherwise live."

# ---- Foundry project (ARM REST) --------------------------------------------
info "Creating Foundry project..."
az rest --method put \
  --url "${ARM}/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}/projects/${PROJECT}?api-version=${API}" \
  --body "{\"location\":\"${LOCATION}\",\"identity\":{\"type\":\"SystemAssigned\"},\"properties\":{\"displayName\":\"Northfield IQ Assistant\"}}" \
  -o none || warn "Project create returned non-zero (may already exist)."

PROJECT_ENDPOINT="https://${FOUNDRY}.services.ai.azure.com/api/projects/${PROJECT}"
PROJECT_RESOURCE_URL="${ARM}/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}/projects/${PROJECT}"
PROJECT_PRINCIPAL_ID=""
for i in $(seq 1 12); do
  PROJECT_PRINCIPAL_ID="$(az rest --method get \
    --url "${PROJECT_RESOURCE_URL}?api-version=${API}" \
    --query identity.principalId -o tsv 2>/dev/null || true)"
  [[ -n "$PROJECT_PRINCIPAL_ID" ]] && break
  sleep 5
done
[[ -n "$PROJECT_PRINCIPAL_ID" ]] || fail "Foundry project managed identity was not provisioned."

SEARCH_PRINCIPAL_ID="$(az search service show -g "$RG" -n "$SEARCH" --query identity.principalId -o tsv)"
[[ -n "$SEARCH_PRINCIPAL_ID" ]] || fail "Azure AI Search managed identity was not provisioned."

# ---- Foundry project connections -------------------------------------------
info "Creating Foundry project connections..."
az rest --method put \
  --url "${PROJECT_RESOURCE_URL}/connections/search?api-version=${API}" \
  --body "$(cat <<JSON
{
  "properties": {
    "category": "CognitiveSearch",
    "target": "${SEARCH_ENDPOINT}",
    "authType": "AAD",
    "isSharedToAll": true,
    "metadata": {
      "ApiType": "Azure",
      "ResourceId": "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Search/searchServices/${SEARCH}",
      "Location": "${LOCATION}"
    }
  }
}
JSON
)" -o none

az rest --method put \
  --url "${PROJECT_RESOURCE_URL}/connections/appinsights?api-version=${API}" \
  --body "$(cat <<JSON
{
  "properties": {
    "category": "AppInsights",
    "target": "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Insights/components/${APPI}",
    "authType": "ApiKey",
    "isSharedToAll": true,
    "credentials": { "key": "${APPI_CONN}" },
    "metadata": {
      "ApiType": "Azure",
      "ResourceId": "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Insights/components/${APPI}"
    }
  }
}
JSON
)" -o none

# ---- managed-identity RBAC -------------------------------------------------
info "Granting Search roles to the Foundry project identity..."
az role assignment create --assignee-object-id "$PROJECT_PRINCIPAL_ID" --assignee-principal-type ServicePrincipal \
  --role "Search Index Data Contributor" \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Search/searchServices/${SEARCH}" \
  -o none 2>/dev/null || warn "Could not assign project Search data role (insufficient perms?)."
az role assignment create --assignee-object-id "$PROJECT_PRINCIPAL_ID" --assignee-principal-type ServicePrincipal \
  --role "Search Service Contributor" \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Search/searchServices/${SEARCH}" \
  -o none 2>/dev/null || warn "Could not assign project Search service role (insufficient perms?)."

info "Granting model access to the Search identity..."
az role assignment create --assignee-object-id "$SEARCH_PRINCIPAL_ID" --assignee-principal-type ServicePrincipal \
  --role "Cognitive Services OpenAI User" \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}" \
  -o none 2>/dev/null || warn "Could not assign Search model-access role (insufficient perms?)."

# ---- best-effort RBAC for keyless local dev --------------------------------
if [[ -n "$PRINCIPAL_ID" ]]; then
  info "Granting data-plane roles to signed-in user (keyless dev)..."
  az role assignment create --assignee-object-id "$PRINCIPAL_ID" --assignee-principal-type User \
    --role "Cognitive Services User" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}" \
    -o none 2>/dev/null || warn "Could not assign Cognitive Services User role (insufficient perms?)."
  az role assignment create --assignee-object-id "$PRINCIPAL_ID" --assignee-principal-type User \
    --role "Cognitive Services OpenAI User" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY}" \
    -o none 2>/dev/null || warn "Could not assign OpenAI User role (insufficient perms?)."
  az role assignment create --assignee-object-id "$PRINCIPAL_ID" --assignee-principal-type User \
    --role "Search Index Data Contributor" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Search/searchServices/${SEARCH}" \
    -o none 2>/dev/null || warn "Could not assign Search role (insufficient perms?)."
  az role assignment create --assignee-object-id "$PRINCIPAL_ID" --assignee-principal-type User \
    --role "Search Service Contributor" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.Search/searchServices/${SEARCH}" \
    -o none 2>/dev/null || warn "Could not assign Search service role (insufficient perms?)."
  az role assignment create --assignee-object-id "$PRINCIPAL_ID" --assignee-principal-type User \
    --role "AcrPush" \
    --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RG}/providers/Microsoft.ContainerRegistry/registries/${ACR}" \
    -o none 2>/dev/null || warn "Could not assign ACR push role (insufficient perms?)."
fi

# ---- write the .env contract ------------------------------------------------
info "Writing ${ENV_FILE} ..."
cat > "$ENV_FILE" <<ENV
# Generated by scripts/deploy.sh on $(date -u +%Y-%m-%dT%H:%M:%SZ) — DO NOT COMMIT.
AZURE_SUBSCRIPTION_ID=${SUBSCRIPTION_ID}
AZURE_TENANT_ID=${TENANT_ID}
AZURE_RESOURCE_GROUP=${RG}
AZURE_LOCATION=${LOCATION}
AZURE_ENV_NAME=${ENV_NAME}
AZURE_PRINCIPAL_ID=${PRINCIPAL_ID}

AZURE_AI_FOUNDRY_ENDPOINT=${FOUNDRY_ENDPOINT}
AZURE_OPENAI_ENDPOINT=${FOUNDRY_ENDPOINT}
AZURE_AI_PROJECT_ENDPOINT=${PROJECT_ENDPOINT}
AZURE_AI_PROJECT_NAME=${PROJECT}
AZURE_AI_MODEL_DEPLOYMENT_NAME=${MODEL_DEPLOYMENT}
AZURE_AI_MODEL_NAME=${MODEL_NAME}
AZURE_AI_API_VERSION=${API}

AZURE_SEARCH_ENDPOINT=${SEARCH_ENDPOINT}
AZURE_SEARCH_INDEX_NAME=${SEARCH_INDEX_NAME}
AZURE_SEARCH_CONNECTION_NAME=search
AZURE_FOUNDRY_KNOWLEDGE_BASE_NAME=northfield-faq-kb
AZURE_FOUNDRY_AGENT_NAME=northfield-iq-assistant

APPLICATIONINSIGHTS_CONNECTION_STRING=${APPI_CONN}
AZURE_LOG_ANALYTICS_WORKSPACE_ID=${LAW_ID}
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

AZURE_CONTAINER_REGISTRY_ENDPOINT=${ACR_LOGIN_SERVER}
AZURE_CONTAINER_REGISTRY_NAME=${ACR}

ACTION_API_URL=http://localhost:8080
ACTION_MCP_URL=http://localhost:8765/mcp
ACTION_API_KEY=
ENV

ok ""
ok "✅ Provisioning complete. Wrote ${ENV_FILE}"
ok "   Next:  ./scripts/setup-foundations.sh  &&  python scripts/validate-foundations.py"
