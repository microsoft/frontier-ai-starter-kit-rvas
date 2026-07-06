# Extra · Copilot-Assisted Build (microsoft/skills)

> Tier 2 · Extra — modular & cross-cutting. You can attempt this in any order.
> Prerequisite: the Foundations end-state is recommended, but the hard minimum is Foundations
> Step 1 (infra + `.env` live). Complete Foundations, or run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> Best done *after* you've felt the manual path on at least one challenge — the contrast is the lesson.

> ⚙️ Infra prerequisite: no new Azure resources. Everything you need ships in this repo:
> [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md),
> [`.vscode/mcp.json`](../../.vscode/mcp.json) (the 3 MCP servers), and the
> [`.github/skills/`](../../.github/skills/) Foundry skill stubs. You need GitHub Copilot enabled in your
> editor and `npx` available.
>
> 🎤 Demo wow-factor: Copilot builds a Foundry tool after fetching current SDK syntax from
> `microsoft-docs` — and the team can compare that grounded result with an ungrounded draft.

## Why this challenge

Every other challenge taught you to search before you implement by hand. This one makes Copilot
do it. With the three MCP servers and the Foundry skills loaded, GitHub Copilot has a required path
for checking current SDK signatures before it writes code. You'll re-build one challenge you already
did manually, then compare the grounded output with an ungrounded draft so the difference is visible.

The doctrine, straight from this repo's [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md):

> MCP = fresh information. Skills = proven patterns. Use both, in that order.

The three MCP servers (from [`.vscode/mcp.json`](../../.vscode/mcp.json)):

| Server | Use it for |
|---|---|
| `azure` | Azure resource ops, deployments, RBAC, quota |
| `foundry-mcp` | Foundry-native: model catalog, agents, knowledge bases, evals |
| `microsoft-docs` | Real-time Microsoft Learn search — current SDK syntax before you code |

---

## Step 1 — Confirm the Copilot enablement layer is live

**Goal:** Your editor has the instructions, the 3 MCP servers, and the Foundry skills available.

**Tasks:**
1. Open [`.vscode/mcp.json`](../../.vscode/mcp.json) and start/verify the three servers (`azure`,
   `foundry-mcp`, `microsoft-docs`) are connected in your editor's MCP panel.
2. Open [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) and read the
   "Search Before Implement" golden rule — this is the behavior you're about to exploit.
3. List the available skills under [`.github/skills/`](../../.github/skills/) (e.g.
   `foundry-projects-resources`, `foundry-models`, `foundry-iq-knowledge-bases`, `foundry-toolboxes`,
   `foundry-observability`, `foundry-hosted-agents`, `foundry-workflows`). Install the one matching your
   target challenge on demand: `npx skills add microsoft/skills --skill <name>`.

**Success Criteria:**
- [ ] All three MCP servers show connected in the editor.
- [ ] You can name the skill that maps to the challenge you'll rebuild.

**Checkpoint:** *Editor state* — MCP panel shows `azure`, `foundry-mcp`, `microsoft-docs` connected.

---

## Step 2 — Pick a challenge and rebuild it agent-assisted

**Goal:** Re-create one challenge's core artifact by prompting Copilot, not by hand.

**Tasks:**
1. Choose one challenge you already did manually (good picks: Foundations Step 3 — create an
   agent; or Action Tools — attach an MCP tool).
2. Prompt Copilot to build it, explicitly asking it to search first, e.g.:
   *"Using the `foundry-projects-resources` skill, and after checking `microsoft-docs` for the current
   `azure-ai-projects` agent-create API, write code to create the Northfield IQ agent against
   `AZURE_AI_PROJECT_ENDPOINT` with deployment `AZURE_AI_MODEL_DEPLOYMENT_NAME`."*
3. When prompted this way, Copilot will typically call `microsoft-docs` / `foundry-mcp` first, then
   generate. Whether the tool call is shown depends on your editor/agent mode — if Copilot skips the
   lookup, tell it to *search the docs first*. Run the result against your live `.env`.

**Success Criteria:**
- [ ] You prompted Copilot to search first, and it performed a doc/MCP lookup before writing the SDK
      code (when your editor surfaces tool calls, you can watch it happen in the chat).
- [ ] The generated code runs against your real Foundry project (uses the authoritative env names).

**Checkpoint:** *Editor + run state* — ideally the chat transcript shows a `microsoft-docs`/`foundry-mcp`
call before code generation; either way, the generated script runs green against your project.

---

## Step 3 — Prove grounding beats guessing

**Goal:** Measure whether MCP-grounding prevented stale or guessed SDK calls.

**Tasks:**
1. Ask Copilot the *same* task with MCP context vs. a deliberately under-specified prompt that
   invites it to guess. Compare the two outputs.
2. Identify at least one place the grounded answer used a current signature the un-grounded one got
   wrong or stale (e.g. a renamed class, a changed parameter, a new API version).
3. Capture the contrast for your readout — this is the teaching artifact.

**Success Criteria:**
- [ ] You can point to a concrete API detail the grounded build got right and the guess got wrong.
- [ ] Your write-up states *why* MCP grounding reduces hallucinated SDK calls.

**Checkpoint:** *Artifact* — a short before/after note (grounded vs guessed) showing the corrected API
detail, shared with your coach.

---

## What you built

Not a new feature — a new way of building. You configured Copilot to fetch current APIs before
it codes, then documented the concrete API detail that grounding corrected.
