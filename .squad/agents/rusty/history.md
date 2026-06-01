# Rusty — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** WTH AI Hackathon — Microsoft Foundry format · **Repo:** ai-hackathon · **Requested by:** Marco Olivo.
- Role: Curriculum Designer. Audience: students (new to AI) + coaches. Single domain theme = Northfield University for continuity.

## Durable learnings / gotchas
- **Challenge shape:** motivation → concrete build steps → success checks → docs → hints → stretch. Coach guides emphasize facilitation (timing, diagnostic questions, blockers) over answers.
- **Timing instinct:** separate **wall-clock** from **hands-on-keyboard effort** — copy-paste steps + ingestion/provisioning waits (App Insights 1–3 min lag, async hosted provisioning) inflate the clock without adding work.
- **3-rung ladder is the cheap fix:** (a) guided [wrap existing steps verbatim], (b) build-from-scratch [strip starter, give API contract + acceptance criteria], (c) stretch. **Same `validate.py` grades all three → zero new validators.** Additive labelling, beginner on-ramp untouched.
- **Reskin contract:** Northfield spine is domain-generic; keep the 3-verb tool invariant (create ticket / place hold / book slot) byte-stable; swap only corpus + tool labels + persona + eval rows.
- **SDK currency:** agents are versioned — `create_version(... PromptAgentDefinition(...))`, not legacy `create_agent`; drive via Responses API; grounding via `AzureAISearchToolDefinition` + `VECTOR_SEMANTIC_HYBRID`. Env auto-written by `azd up`; Step 4 RBAC (Search Index Data Contributor + Search Service Contributor) is the #1 pitfall.
- **Foundry rebrand:** "Azure AI Foundry" → "Microsoft Foundry" for portal/product text only; SDK package names unchanged. Humanizer tells: em-dash overuse, promotional words, rule-of-three.

## What I built (cumulative, staged — not committed)
- Authored **Tier 1 Foundations** (`challenges/foundations/` README + solution, 4 stepped guided challenge); harvested + git-rm'd v1 ch01/02/04.
- Authored **CURRICULUM-REASSESSMENT.md** (timing audit + 3-rung ladder + reskin contract feeding PLAN-V3).
- **De-guided all 4 Advanced READMEs** to the 3-rung ladder + consistent banner; finalized dual-time labels; removed one breadcrumb PLACEHOLDER from `advanced-action-tools/agent_with_actions.py`. No validator/solution/root-README/docs/`.env` changes.

## Final dual-time labels (mirrored by Linus in root README)
Action Tools ~45 min / ~1.5 hr ⭐⭐⭐ · Eval & Red Teaming ~1.25 hr / ~2 hr ⭐⭐⭐⭐ · Tracing ~1 hr / ~1.5 hr ⭐⭐⭐⭐ · Deploy ~60–90 min / ~1.5 hr ⭐⭐⭐⭐⭐.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: all 4 Advanced READMEs de-guided to the 3-rung ladder with ⏱/🛠/⭐ banner, "why now" hooks, output anchors; same `validate.py` grades every rung. Alongside: Tier 3 Capstone live (Danny + Basher validator), `scripts/cleanup.sh` + lab-generator (Livingston), three-tier README/docs (Linus, mirroring my labels). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
