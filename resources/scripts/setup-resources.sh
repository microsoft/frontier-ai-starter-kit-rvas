#!/usr/bin/env bash
# ============================================================================
# DEPRECATED — compatibility wrapper only.
#
# This script has been superseded by the keyless provisioning paths:
#
#   azd up                  (preferred — Bicep, keyless RBAC)
#   ./scripts/deploy.sh     (Bash fallback — same footprint, no keys written)
#
# Key-based provisioning and key retrieval have been removed from this repo.
# Authentication is DefaultAzureCredential (keyless-first).
#
# This wrapper delegates to scripts/deploy.sh when possible, or exits with
# clear instructions when delegation is unsafe.
# ============================================================================
set -Eeuo pipefail

YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

warn() { printf "%b%s%b\n" "$YELLOW" "$1" "$RESET" >&2; }
info() { printf "%b%s%b\n" "$CYAN"   "$1" "$RESET"; }

warn "-----------------------------------------------------------------------"
warn "DEPRECATED: resources/scripts/setup-resources.sh"
warn ""
warn "This script no longer provisions resources directly."
warn "The golden provisioning paths for this hackathon are:"
warn ""
warn "  1. azd up                 (preferred — Bicep + keyless RBAC)"
warn "  2. ./scripts/deploy.sh    (Bash fallback, same .env contract)"
warn ""
warn "Key-based auth has been removed; use DefaultAzureCredential instead."
warn "-----------------------------------------------------------------------"

# Locate deploy.sh relative to this script's directory.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_SCRIPT="${SCRIPT_DIR}/../../scripts/deploy.sh"

if [[ -x "$DEPLOY_SCRIPT" ]]; then
  info "Delegating to scripts/deploy.sh $*"
  exec "$DEPLOY_SCRIPT" "$@"
else
  warn "Could not find scripts/deploy.sh at: ${DEPLOY_SCRIPT}"
  warn "Please run one of the provisioning paths listed above manually."
  exit 1
fi
