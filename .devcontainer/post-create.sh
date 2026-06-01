#!/usr/bin/env bash
set -Eeuo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

success() {
  printf "%b%s%b\n" "$GREEN" "$1" "$RESET"
}

warn() {
  printf "%b%s%b\n" "$YELLOW" "$1" "$RESET"
}

info() {
  printf "%b%s%b\n" "$CYAN" "$1" "$RESET"
}

info "Setting up the WTH AI Foundry Hackathon workspace..."

if [[ -f requirements.txt ]]; then
  info "Installing Python requirements from requirements.txt"
  pip install -r requirements.txt
  success "Python dependencies are installed."
else
  warn "requirements.txt was not found; skipping pip install."
fi

if [[ ! -f .env && -f .env.sample ]]; then
  cp .env.sample .env
  success "Created .env from .env.sample (placeholder values — fill in after 'azd up')."
elif [[ -f .env ]]; then
  warn ".env already exists; leaving it unchanged."
else
  warn ".env.sample was not found; skipping environment bootstrap."
fi

printf "\n%b==============================================%b\n" "$GREEN" "$RESET"
printf "%b  Welcome to the WTH AI Foundry Hackathon!  %b\n" "$GREEN" "$RESET"
printf "%b==============================================%b\n\n" "$GREEN" "$RESET"

printf "%bChallenge quick links%b\n" "$CYAN" "$RESET"
printf "  • Foundations (Steps 1–4): challenges/foundations/\n"
printf "  • Advanced — Action Tools: challenges/advanced-action-tools/\n"
printf "  • Advanced — Evaluation & Red Teaming: challenges/advanced-evaluation-redteam/\n"
printf "  • Advanced — Tracing & Observability: challenges/advanced-tracing-observability/\n"
printf "  • Advanced — Deploy as a Hosted Agent: challenges/advanced-deploy-hosted-agent/\n"
printf "  • Extras: challenges/extra-*/\n"
printf "  • Docs site: docs/\n\n"

warn "Next steps:"
printf "  1. Run: az login\n"
printf "  2. Provision: azd up   (or ./scripts/deploy.sh)\n"
printf "  3. Bootstrap end-state: ./scripts/setup-foundations.sh && python scripts/validate-foundations.py\n"
