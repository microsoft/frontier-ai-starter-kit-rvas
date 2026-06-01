# Danny — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** WTH AI Hackathon — Microsoft Foundry format · **Repo:** ai-hackathon · **Requested by:** Marco Olivo.
- Stack: Microsoft Foundry AI, GitHub Pages (Jekyll/just-the-docs), Markdown, GitHub Actions. Audience: students (new to AI) + coaches. Role: Lead & Content Architect.

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
- Authored **Tier 3 Capstone** (`challenges/capstone-multi-agent/README.md` + `solution.md`) as a LOW-guidance design brief; reconciled `PLAN-V2.md` (superseded-in-part pointer). Validator PASS string handed to Basher: `✅ ALL STRUCTURAL CHECKS PASS — ≥3 agents, fan-out edge present, typed contracts in use`.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** to disk (staged, not committed): Tier 3 MAF Capstone **live** (README + solution + Basher `validate.py`); 4 Advanced READMEs **de-guided** to the 3-rung ladder (Rusty); `scripts/cleanup.sh` + lab-generator shipped (Livingston); root `README.md` + `docs/` migrated to **three-tier** (Linus). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
