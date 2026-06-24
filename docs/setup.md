---
title: Getting Started
nav_order: 3
---

# Getting Started

Use this page to get your environment ready before the Foundations challenge. The fastest route is GitHub Codespaces, but you have two fallback paths if your event or device needs them.

## Prerequisites

- A GitHub account with access to Codespaces or permission to clone the repo locally
- An Azure subscription through Azure Pass, Azure for Students, or a trial/subscription provided by your event
- Basic Python familiarity: running scripts, installing packages, and reading terminal output
- A modern browser and a stable internet connection for Microsoft Foundry

## Choose your setup path

Your setup is the same in both event modes. **Upskill Mode** uses the Northfield University reference
scenario. **Customer Build Mode** starts from the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}) after your environment is ready, then maps the same challenges to a customer scenario.

### 1. GitHub Codespaces (recommended)

Best for most participants. You get a ready-to-use cloud dev environment with the right tools preinstalled.

1. Click the badge below.
2. Choose the default branch and create a new Codespace.
3. Wait for the container to finish starting.
4. Open the integrated terminal when VS Code loads.
5. Continue with Azure sign-in and the Foundations challenge.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/frontier-foundry-hackathon)

<div class="callout-tip" markdown="1">
<strong>Tip:</strong> Codespaces is the safest event-day option because everyone works in the same environment, with fewer laptop-specific issues to debug.
</div>

### 2. Local Dev Container

Use this when Codespaces is unavailable but you can run containers locally.

1. Install Visual Studio Code.
2. Install Docker Desktop and confirm containers start successfully.
3. Install the Dev Containers extension in VS Code.
4. Clone the repository to your machine.
5. Open the repo in VS Code and choose <strong>Reopen in Container</strong> when prompted.
6. Wait for the container build to finish, then open a terminal.

### 3. Manual Setup

Choose this only if you cannot use containers.

1. Install Python 3.11+.
2. Install the Azure CLI.
3. Clone this repository.
4. Create and activate a virtual environment.
5. Install the project requirements from `requirements.txt`.
6. Use the same challenge guides as container users after environment validation passes.

<div class="callout-warning" markdown="1">
<strong>Warning:</strong> Manual setup is more sensitive to local machine differences. If you hit package or CLI issues, ask a coach early instead of losing time during Foundations.
</div>

## Codespaces setup: step by step

1. Open the repository in Codespaces using the badge above.
2. Wait until the status bar shows the container is ready.
3. In the terminal, sign in to Azure:

```bash
az login

```

4. If your event uses a provided subscription, switch to it after sign-in:

```bash
az account set --subscription "<your-subscription-name-or-id>"

```

5. Confirm you can open Microsoft Foundry in the browser and reach the correct tenant.
6. Choose your event mode: Northfield for upskilling, or the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}) for a customer engagement.
7. Move to Foundations to provision the Foundry resource and project.

## Azure subscription options

| Option | Best for | Notes |
|--------|----------|-------|
| Azure Pass | Organized events | Usually distributed by the event team; follow the redemption instructions you were given. |
| Azure for Students | University participants | Great if you qualify and need a self-service route with no credit card. |
| Azure trial / existing subscription | Independent participants | Works well if you already have access and can create the needed AI resources. |

## Post-setup verification

After your environment is open and Azure sign-in succeeds, run the validation script from the repo root:

```bash
python resources/scripts/validate-environment.py

```

A successful run should confirm your local tooling, Python environment, and Azure connectivity are ready for the Foundations challenge.

<div class="callout-info" markdown="1">
<strong>Heads up:</strong> If the validation script reports missing environment variables, copy `.env.sample` to `.env` and fill in the values provided for your event before retrying.
</div>

## Troubleshooting

| Issue | Likely cause | Fix |
|------|--------------|-----|
| Codespace takes too long to start | Region or quota delay | Refresh once, then retry creation; if it persists, switch to a local dev container. |
| Docker container fails locally | Docker Desktop not running or low resources | Start Docker Desktop, free disk space, then reopen in container. |
| `az login` fails | Wrong tenant or blocked pop-up flow | Retry with the correct account; use device code login if needed. |
| Azure subscription not visible | Azure Pass not redeemed or wrong directory | Confirm redemption, then check `az account list --output table`. |
| Python command not found | Manual setup incomplete | Install Python 3.11+ and reopen the terminal before retrying. |
| Validation script errors | Missing tools, auth, or branch setup | Fix the first reported error, rerun, and escalate to a coach if it repeats. |
