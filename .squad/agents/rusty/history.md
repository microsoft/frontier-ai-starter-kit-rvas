# Rusty — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** AI Starter Kit RVAS — Microsoft Foundry format · **Repo:** ai-starter-kit-rvas · **Requested by:** Marco Olivo.
- Role: Curriculum Designer. Audience: students (new to AI) + facilitators. Single domain theme = Northfield University for continuity.

## Durable learnings / gotchas
- **Activity shape:** motivation → concrete build steps → success checks → docs → hints → stretch. Facilitator guides emphasize facilitation (timing, diagnostic questions, blockers) over answers.
- **Timing instinct:** separate **wall-clock** from **hands-on-keyboard effort** — copy-paste steps + ingestion/provisioning waits (App Insights 1–3 min lag, async hosted provisioning) inflate the clock without adding work.
- **3-rung ladder is the cheap fix:** (a) guided [wrap existing steps verbatim], (b) build-from-scratch [strip starter, give API contract + acceptance criteria], (c) stretch. **Same `validate.py` grades all three → zero new validators.** Additive labelling, beginner on-ramp untouched.
- **Reskin contract:** Northfield spine is domain-generic; keep the 3-verb tool invariant (create ticket / place hold / book slot) byte-stable; swap only corpus + tool labels + persona + eval rows.
- **SDK currency:** agents are versioned — `create_version(... PromptAgentDefinition(...))`, not legacy `create_agent`; drive via Responses API; grounding via `AzureAISearchToolDefinition` + `VECTOR_SEMANTIC_HYBRID`. Env auto-written by `azd up`; Step 4 RBAC (Search Index Data Contributor + Search Service Contributor) is the #1 pitfall.
- **Foundry rebrand:** "Azure AI Foundry" → "Microsoft Foundry" for portal/product text only; SDK package names unchanged. Humanizer tells: em-dash overuse, promotional words, rule-of-three.

## What I built (cumulative, staged — not committed)
- Authored **Tier 1 Foundations** (`activities/foundations/` README + solution, 4 stepped guided activity); harvested + git-rm'd v1 ch01/02/04.
- Authored **CURRICULUM-REASSESSMENT.md** (timing audit + 3-rung ladder + reskin contract feeding PLAN-V3).
- **De-guided all 4 Advanced READMEs** to the 3-rung ladder + consistent banner; finalized dual-time labels; removed one breadcrumb PLACEHOLDER from `advanced-action-tools/agent_with_actions.py`. No validator/solution/root-README/docs/`.env` changes.

## Final dual-time labels (mirrored by Linus in root README)
Action Tools ~45 min / ~1.5 hr ⭐⭐⭐ · Eval & Red Teaming ~1.25 hr / ~2 hr ⭐⭐⭐⭐ · Tracing ~1 hr / ~1.5 hr ⭐⭐⭐⭐ · Deploy ~60–90 min / ~1.5 hr ⭐⭐⭐⭐⭐.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: all 4 Advanced READMEs de-guided to the 3-rung ladder with ⏱/🛠/⭐ banner, "why now" hooks, output anchors; same `validate.py` grades every rung. Alongside: Tier 3 Capstone live (Danny + Basher validator), `scripts/cleanup.sh` + lab-generator (Livingston), three-tier README/docs (Linus, mirroring my labels). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

### 2026-06-01 — ASCII diagram repair pass (docs + README)
- Ran a repo-wide scan of text-fenced markdown blocks and patched only malformed/over-wide flow and architecture diagrams.
- Normalized diagram arrows to `-->` in edited blocks and replaced fragile unicode/emoji-heavy rails with compact ASCII lines.
- Kept changes constrained to diagram fences (no activity logic rewrites) and re-checked text-fence width so diagrams remain readable in Just-the-Docs/GitHub Pages layouts.

### 2026-06-01 — Cross-agent note (diagram-fix batch)
- Basher QA found two residual issues after the broad ASCII pass: malformed branch fan-out in Magentic workflows docs and one over-wide architecture line in Build UI docs.
- Linus completed the targeted follow-up fixes; batch was closed through Scribe merge and orchestration logging.

### 2026-06-01 — Participant/facilitator markdown terminology audit (Foundry + setup)
- Revalidated curriculum wording against current Microsoft Learn pages (`what-is-foundry`, `navigate-from-classic`, hosted-agent quickstart/deploy pages, Azure AI Search RBAC, Fabric tool docs).
- Applied minimal wording corrections in scoped markdown only: standardized product naming to **Microsoft Foundry**, clarified role naming as **Foundry User (formerly Azure AI User)** where access guidance appears, and updated outdated Learn URL base paths from `/azure/ai-foundry/...` to `/azure/foundry/...`.
- Kept curriculum flow and activity structure unchanged; no dependency pins or validation contracts were modified.

## Learnings

### 2026-06-23 — Foundations + instructional coherence remediation

**Files changed:**
- `activities/foundations/README.md` — three-tier language fix; `.env` contract, `DefaultAzureCredential`, Responses API, and `VECTOR_SEMANTIC_HYBRID` concept primers added inline; customer corpus preparation guidance added to Step 4 Task 1.
- `docs/activities/foundations.md` — mirror of all README changes (same content, JTD formatting preserved).
- `activities/foundations/solution.md` — customer corpus guidance section added to Step 4 indexing guidance (facilitator-facing).
- `docs/activities/foundations-facilitator.md` — mirror of solution.md Step 4 corpus guidance.
- `docs/customer-outcome.md` — corpus preparation sub-section added under Pre-work canvas table (min useful size, safe data, formats, PDFs/SharePoint, Northfield fallback).
- `docs/faq.md` — Foundry-specific troubleshooting section added: citations/grounding, 403/RBAC, resource vs. project, validator failures, quota/region, tracing delays.
- `docs/resources.md` — Azure AI Inference SDK demoted to secondary; new Azure AI Projects & Foundry SDK section added as primary with `azure-ai-projects` readme, Foundry get-started, agents quickstart, and samples links.
- `docs/facilitator-hub.md` — pre-event Customer Outcome Canvas timing row added (20–30 min); Extras timing row added to Advanced table; Tier 3 Capstone pacing table added; Extras-to-canvas choice guide added.

**Pattern learned:** Concept primers (`.env`, `DefaultAzureCredential`, Responses API, `VECTOR_SEMANTIC_HYBRID`) work best as `>` blockquote callouts placed immediately before the first task that relies on the concept — not as a glossary section or footnote. This keeps them discoverable in reading order without inflating the step length.


**Decision approved by Marco Olivo.** Repositioned the session from co-equal modes to outcome-first: Customer Build / Bring-Your-Own-Outcome is now the **primary motion**; Northfield University Upskill path is the **secondary / fallback**.

**Files changed:**
- `docs/index.md` — Hero tagline, "What is this?" paragraph, quick-grid cards, and mode table reordered (Customer Build first); added "Which path is right for you?" mode comparison table; added Customer Activity-Forge callout and pointer; final CTA button row updated.
- `docs/customer-outcome.md` — Intro rewritten as the DEFAULT starting point (not "more than upskilling"); mode table reordered (Customer Build primary); added "Don't have a customer or idea yet?" section pointing to `.github/skills/customer-activity-forge/` with explanation of how its output maps to the pre-work canvas fields.
- `README.md` — "What is AI Starter Kit RVAS?" rewritten so the evolving artifact defaults to the participant's own application; Northfield framed as guided fallback; section heading renamed to "Two ways to run it: Customer Build or Upskill"; mode table reordered; Customer Activity-Forge on-ramp added; Getting Started step 3 reordered (Customer Build first) with Activity-Forge pointer.
- `docs/facilitator-hub.md` — Pre-event checklist expanded with three-branch decision tree (has scenario → canvas; no scenario → run Activity-Forge → canvas; no scenario + pure upskill → Northfield); "During the event" bullet updated to start from team outcome; "Anchor customer work in outcomes" subsection expanded with a step-by-step Customer Activity-Forge facilitation guide; Northfield retained as safe fallback.

**Skill referenced:** Customer Activity-Forge at `.github/skills/customer-activity-forge/` — on-ramp for "I want to build something real but don't have an idea yet."
