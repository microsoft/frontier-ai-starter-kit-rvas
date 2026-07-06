# GitHub Copilot — Workspace Instructions

> AI Starter Kit RVAS · *Build Intelligent Agents with Microsoft Foundry*.
> Copilot is your always-available pair-programmer here. It does **not** hand you answers —
> it walks the **same path the activities teach**, using fresh API signatures from MCP and
> proven patterns from the Foundry skills.

## The golden rule: Search Before Implement

Before writing **any** Azure / Microsoft Foundry SDK code:

1. **Search** the `microsoft-docs` MCP server (and `foundry-mcp` for Foundry-native ops) for the
   **current** API surface. Foundry features here are fast-moving and many are **preview** — never
   rely on memorized signatures.
2. **Load** the matching skill from `.github/skills/` for the proven pattern.
3. **Implement** against the verified signature.
4. **Validate** with the activity's `validate.py` / checkpoint.

> **MCP = fresh information. Skills = proven patterns.** Use both, in that order.

## MCP servers (configured in `.vscode/mcp.json`)

| Server | Use it for |
|---|---|
| `azure` | Azure resource management, deployments, RBAC, quota (`@azure/mcp`). |
| `foundry-mcp` | Foundry-native ops: model catalog, agents, toolboxes, knowledge bases, evals. |
| `microsoft-docs` | Real-time Microsoft Learn search — current SDK syntax before you code. |

## Skills in this repo (`.github/skills/`)

Each folder is a **minimal stub** that points at the upstream
[`microsoft/skills`](https://github.com/microsoft/skills) source. Install the full skill on demand
with `npx skills add microsoft/skills --skill <name>` rather than vendoring everything (loading all
skills causes "context rot").

| Skill | Maps to |
|---|---|
| `foundry-projects-resources` | Foundations · Step 1 (provision Foundry + project + connections) |
| `foundry-models` | Foundations · Step 2 (deploy/compare models, capacity, quota) |
| `foundry-iq-knowledge-bases` | Foundations · Step 4 (Index + Foundry IQ knowledge base) |
| `foundry-toolboxes` | Advanced · Action Tools (bundle MCP/Search/Code Interpreter tools) |
| `foundry-observability` | Advanced · Tracing & Observability + Evaluation & Red Teaming |
| `foundry-hosted-agents` | Advanced · Deploy as a Hosted Agent (`azd ai agent`, `agent.yaml`) |
| `foundry-workflows` | Extras · Magentic / MAF multi-agent workflows |

## Project conventions

- **Provisioning** is `azd up` + Bicep (`infra/`); `scripts/deploy.sh` is the Bash fallback. Outputs
  become the `.env` contract — see `.env.sample`. **Never commit a real `.env`** or any secret.
- **Auth is keyless-first**: prefer `DefaultAzureCredential` over keys. Run `az login` for local dev.
- **Tracing**: set `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` and
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` **before importing** the Foundry SDK.
- **Action Tools** env names are authoritative in `.env.sample`: `ACTION_API_URL`, `ACTION_MCP_URL`,
  `ACTION_API_KEY`. Match them everywhere.
- **Prompt Flow is removed** from this curriculum. Do not suggest `promptflow`, `.flow.dag`, or any
  Prompt Flow construct — use **agents + tools + MCP** instead.
- Python pins live in `requirements.txt`; the Action Tools backend has its own
  `scripts/action-backend/requirements.txt`.
