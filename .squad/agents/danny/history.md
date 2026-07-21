# Danny — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** AI Starter Kit — Microsoft Foundry format · **Repo:** ai-starter-kit-rvas · **Requested by:** Marco Olivo.
- Stack: Microsoft Foundry AI, GitHub Pages (Jekyll/just-the-docs), Markdown, GitHub Actions. Audience: students (new to AI) + facilitators. Role: Lead & Content Architect.

## Durable learnings / gotchas
- **STEP template** (Goal → Tasks → Success Criteria → Checkpoint); Success Criteria must be observable; every step ends in `python validate.py --step N`. I author *to* the validator contract; Basher owns `validate.py`.
- **Prompt Flow is CUT** entirely — re-express RAG/eval on Agents + AI Search + Foundry IQ + MCP + MAF.
- **Hosted-agent gotchas:** `azd ai agent deploy` exit 0 ≠ done (gate on `status==active` or get `424`); `az acr build` needs `--source-acr-auth-id "[caller]"` + fresh tags; two-identity model (caller bearer vs per-agent MI — `403` ⇒ caller missing `Azure AI User`); bind `0.0.0.0:8088` + declare `responses` v1.0.0.
- **Tracing:** GenAI instrumentation env flags must be set ABOVE all `azure.ai.*` imports or message content is dropped.
- **Search-Before-Implement:** preview MAF/Foundry surfaces (WorkflowBuilder, ChatAgent/Magentic, voicelive, Fabric tool) are never hard-coded — confirm via microsoft-docs/foundry-mcp; reference snippets marked "illustrative."
- **Env discipline:** keep `.env.sample` byte-for-byte; reuse existing vars only; new vars go through Livingston's Bicep outputs, never hand-edited.

## What I built (cumulative, staged — not committed)
- Authored Advanced **Tracing & Observability** + rewrote **Deploy as a Hosted Agent** (Prompt Flow removed).
- Authored FIVE Extras (Fabric IQ, Voice Live, Magentic, Hosted Long-Running, Copilot-Assisted); build-ui left to Linus.
- Authored **PLAN-V3.md** (3-tier tree: Foundations → Advanced → MAF Capstone; de-guided Advanced; 11-idea backlog).
- Authored **Tier 3 Capstone** (`activities/capstone-multi-agent/README.md` + `solution.md`) as a LOW-guidance design brief; reconciled `PLAN-V2.md` (superseded-in-part pointer). Validator PASS string handed to Basher: `✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use`.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** to disk (staged, not committed): Tier 3 MAF Capstone **live** (README + solution + Basher `validate.py`); 4 Advanced READMEs **de-guided** to the 3-rung ladder (Rusty); `scripts/cleanup.sh` + lab-generator shipped (Livingston); root `README.md` + `docs/` migrated to **three-tier** (Linus). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

### 2026-06-01 — Audit consolidation follow-through (QA closeout)
- Capstone student + mirrored docs updated to reflect that `activities/capstone-multi-agent/validate.py` exists now (removed "forthcoming" language).
- Foundations mirrored docs no longer link to learner-created files as GitHub blob URLs; those references are now plain file paths to avoid 404s before learners create files.
- Root README wording normalized to "Microsoft Foundry model catalog" and facilitator-facing role phrasing kept Foundry-first.

### 2026-06-01 — Learning note (stale wording hygiene)
- When a validator exists in-repo, checkpoint text must reference the real path (`activities/capstone-multi-agent/validate.py`) and avoid future-tense wording (e.g., "authored separately" or "forthcoming").

### 2026-06-23 — customer-activity-forge skill authored
- **New skill:** `.github/skills/customer-activity-forge/SKILL.md` — a FULL working skill (not a stub). Purpose: outcome-first idea generation for session participants who have a customer name + industry but no idea what to build.
- **Effort-tag vocabulary (canonical):** `Starter` (Foundations only, ~2 hr), `Core` (Foundations + one Advanced, sweet spot, ~6–8 hr day), `Stretch` (3+ tiers or Capstone/MAF).
- **Sweet-spot rule encoded in skill:** "grounded agent + one governed action" = Core. Anything below that bar is trivial; anything requiring multi-system data engineering is over-complex.
- **Tier/tech names used in skill (match these everywhere):** Foundations · Action Tools · Evaluation & Red Teaming · Tracing & Observability · Deploy as Hosted Agent · Capstone · Extra — Fabric IQ · Extra — Voice Live · Extra — Magentic Workflows · Extra — Build a UI. These are the exact labels from `docs/index.md` and `activities/` folder names.
- **skills-lock.json:** confirmed no entry needed. That file tracks remote github-sourced skills (with `computedHash`). Local `.github/skills/*` skills are not registered there; the skill is live immediately.
- **Canvas linkage:** skill Part E pre-fills the Customer Outcome Canvas Pre-work table (`docs/customer-outcome.md`) for the top idea so the participant carries it straight into the Foundations activity.
