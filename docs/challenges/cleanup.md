---
title: "Wrap-Up: Cleanup & Cost Hygiene"
parent: Challenges
nav_order: 40
---

# Wrap-Up — Cleanup & Cost Hygiene

> **The last step of every event.** You provisioned real Azure resources (Foundry, AI Search, App
> Insights, ACR) and ran local processes (the Action Tools backend + MCP server). When the hackathon
> is over, **tear it all down** so nobody leaks Azure spend after the event.

Cleanup is driven by one idempotent, `.env`-aware script:
[`scripts/cleanup.sh`](https://github.com/olivomarco/ai-hackathon/blob/main/scripts/cleanup.sh). It
reuses **only** the variable names from the `.env` contract — it never invents, renames, or persists
new env vars.

## Safe by default (dry-run first)

A bare run **only prints** what it would tear down. Nothing destructive happens until you pass
`--yes`, and the resource group is shown first and is **never** deleted blindly.

```bash
./scripts/cleanup.sh                 # dry-run: show targets + costs, change nothing
./scripts/cleanup.sh --yes           # actually tear down (azd down + local procs)
./scripts/cleanup.sh --local-only    # only stop local Action Tools processes
./scripts/cleanup.sh --yes --purge   # also --purge soft-deletable resources (Foundry / AI)
```

## What to clean up

- **Azure resources** — `azd down` removes the resource group provisioned by `azd up` (Foundry + AI
  Search + App Insights + ACR). Add `--purge` to clear soft-deleted Foundry/AI resources so their
  names are immediately reusable.
- **Local processes** — the Action Tools REST API and FastMCP server you started locally. Use
  `--local-only` to stop just those without touching the cloud.
- **Costs to watch** — AI Search and any provisioned-throughput model deployments are the usual spend
  drivers; the dry-run prints them so you can confirm before deleting.

## Recommended flow

1. **Demo done?** Run the dry-run (`./scripts/cleanup.sh`) and read the target list.
2. Stop local processes first if you only paused for the day: `./scripts/cleanup.sh --local-only`.
3. When the event is fully over, tear everything down: `./scripts/cleanup.sh --yes` (add `--purge` if
   you want the resource names freed immediately).

> **Coaches:** make this the final agenda item. A two-minute teardown at the end of the day prevents
> surprise bills on participant subscriptions a week later.
