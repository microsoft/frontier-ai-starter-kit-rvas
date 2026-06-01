# History Archive — Rusty

> Archived 2026-06-01 by Scribe (history.md exceeded 15360 B). Verbatim prior history below; active history.md now carries a tight summary.

---

## Learnings

### 2026-06-01 — Applied 3-rung ladder + consistent banner to all 4 Advanced READMEs (V3 implemented)
- **Scope:** edited the four `challenges/advanced-*/README.md` only. Did NOT touch any `validate.py`, `solution.md`, root README, or `docs/`. No `.env` var names or validator contracts changed — rung (b) passes the SAME validator. One surgical code edit outside the READMEs: removed the telegraphing `tool_approvals = []  # < PLACEHOLDER >` breadcrumb line from `advanced-action-tools/agent_with_actions.py` (kept the TODO prose so the guided beginner can still finish).
- **Standardized banner format (now on ALL four):** `> ⏱ **Guided ~X** · 🛠 **Build-from-scratch ~Y** · ⭐… · **Prereqs:** Foundations end-state` — placed as a blockquote directly under the H1, above the existing "Tier 2 · Advanced — modular" prereq blockquote. **Two of four had NO banner before** (Action Tools and Eval — times lived only in PLAN-V2); Tracing and Deploy had a "Why this challenge" section but still no time/difficulty banner. All four now carry it.
- **Final dual-time labels (from PLAN-V3 §2.5; Deploy reconciled per my memo §5.5 to "~60–90 min"):**
  - Action Tools — Guided ~45 min / scratch ~1.5 hr / ⭐⭐⭐
  - Evaluation & Red Teaming — Guided ~1.25 hr / scratch ~2 hr / ⭐⭐⭐⭐
  - Tracing & Observability — Guided ~1 hr / scratch ~1.5 hr / ⭐⭐⭐⭐
  - Deploy as a Hosted Agent — Guided ~60–90 min / scratch ~1.5 hr / ⭐⭐⭐⭐⭐
- **Rung structure (no beginner content deleted):** wrapped existing Steps under a new `## Rung (a) — Guided path` heading (kept verbatim as the on-ramp); added `## Rung (b) — Build-from-scratch path` (contract + "same validate.py grades it"); converted/added `## Rung (c) — Stretch goals` (renamed existing `## Stretch goals` in Tracing & Deploy; net-new in Action Tools & Eval). Added a 1-line "three rungs / same validate.py" intro after the files list in each.
- **Exact build-from-scratch contracts embedded (verbatim from CURRICULUM-REASSESSMENT §2 table):**
  - Action Tools: "Attach the `northfield_actions` MCP server as a tool; implement a human-approval loop using `McpTool` / `RequiredMcpToolCall` / `SubmitToolApprovalAction` / `ToolApproval`. Acceptance: no action runs without an approve; a denial creates nothing."
  - Eval: "Write `evaluate.py`: load the JSONL, call the agent per `query`, score Groundedness/Relevance/Coherence/Fluency with `azure-ai-evaluation`, add a custom 1–5 domain evaluator, exit non-zero below `--gate`."
  - Tracing: "Emit GenAI spans to App Insights and reconstruct one question end-to-end. Acceptance: model + retrieval spans for one `operation_Id`, with token + latency, surfaced in portal Tracing AND a KQL query you wrote."
  - Deploy: "Containerize the Foundations agent, serve the `responses` protocol on 8088, deploy with `azd ai agent`, invoke over the production endpoint, prove anonymous calls get 401/403. Acceptance: live grounded answer + rejected anon call."
- **Stretch goals (rung c) wired from PLAN-V3 §2.1–2.4:** Action Tools = build the MCP server end-to-end (`waive_late_fee`) + selective approval policy; Eval = mandatory automated `RedTeam().scan()` + real GitHub Actions CI gate + trace-to-eval correlation; Tracing = `TelemetryManager` + custom `northfield.answers.uncited` metric + batch-run timechart; Deploy = blue/green v2 + auth hardening (prove 403 on missing role).
- **Expected-output anchors (§4 #7):** added a "**Your run should look like this:**" snippet near the thinnest Checkpoint in each (Action Tools Step 4 approval+ticket; Eval Step 2 aggregate score table; Tracing Step 2 Q/A/response-id; Deploy Step 3 grounded answer + `403` on anon curl). These are *runtime* output snippets, distinct from the existing `# expected:` validator lines.
- **"Why now" stakes (§4 #2):** Action Tools and Eval lacked a stakes hook, so added a 2-sentence "**Why now:**" tied to a real consequence (wrongful course hold blocks registration; invented financial-aid deadline / injected-doc instruction harms a student). Tracing and Deploy already had a "Why this challenge" section — left intact, banner added above it.
- **De-guiding kept surgical:** only softened load-bearing telegraphs in the GUIDED path where PLAN-V3 §2.1 named them (removed the `tool_approvals` breadcrumb in the starter; replaced README Step 2 "(already sketched in main())" with a discover-the-attribute hint). Did NOT strip the guided code from Tracing/Deploy — that stripping lives in rung (b), preserving the beginner on-ramp.
- **Reusable instinct:** the cheapest way to add a difficulty ladder to an existing guided challenge is *additive labelling* — wrap (don't rewrite) the current steps as rung (a), append rung (b) as a contract block that points at the SAME validator, and promote the existing stub stretch list to rung (c). Zero new validators, beginner path untouched.

### 2026-06-01 — Advanced-tier curriculum reassessment (feeds Danny's PLAN-V3)
- **Deliverable:** `CURRICULUM-REASSESSMENT.md` at repo root (separate file from Danny's PLAN-V3 to avoid write conflict). Analysis only — did NOT edit challenge content.
- **Headline timing verdict:** Advanced tier *reads* as ~4.5 hr but genuine build/authoring effort is ~1.5–2 hr. The clock is padded by **waiting** (App Insights 1–3 min ingestion lag; async hosted provisioning) and **copy-paste** (Tracing + Deploy print every line of code inline; Action Tools = fill 2 placeholders; Eval = add 1 evaluator rule). User's "short + over-guided" instinct is correct.
- **Per-challenge audit (steps / real-code):** Action Tools 5 steps, 2 real-code (heavy guidance, clock roughly honest). Eval & Red Team 5 steps, 1 real-code (richest concept, thinnest authoring). Tracing 4 steps, 0-from-blank (inflated as a "build"; mostly wait). Deploy 4 steps, 0-from-blank BUT clock is OPTIMISTIC — real container build + preview `azd ai agent` + async = highest failure surface; budget 90 min not 60.
- **Core proposal — 3-rung difficulty ladder** per Advanced challenge: (a) guided [current], (b) build-from-scratch [strip the starter, give only the API contract + acceptance criteria], (c) stretch [open]. Same `validate.py` grades all three → zero new validators. §2 specifies exactly what to strip per challenge.
- **Pick-your-scenario [FWH]:** Northfield spine is already domain-generic (retriever+KB / 3-tool action agent / eval set / tracing). Keep the 3-verb tool invariant (create ticket / place hold / book slot) byte-stable; swap only corpus + tool labels + persona + eval rows. Proposed alts: Mercy General (healthcare), NorthPeak (retail), Riverton 311 (gov). Recommend shipping Northfield canonical + ONE alt (retail) wired to Extra F as the [FWH] lab-generator analog.
- **Gap found:** 2 of 4 Advanced READMEs have NO time/difficulty banner in the participant README — estimates live only in PLAN-V2. Top 2 pedagogy borrows: consistent per-challenge time+difficulty banner [FWH/ATA] and cleanup/cost-hygiene script + wrapup [FWH].
- **Reusable instinct:** when auditing "is it really X hours," separate **wall-clock** from **hands-on-keyboard effort** — copy-paste + ingestion/provisioning waits inflate the former without adding the latter.

### Project Context
- **Project:** WTH (What The Hack) AI Hackathon — Microsoft Foundry format
- **Repo:** ai-hackathon
- **Stack:** Microsoft Foundry AI, GitHub Pages (Jekyll/static), Markdown, GitHub Actions
- **Participants:** Students (new to AI) + Coaches (facilitators)
- **Goal:** Create a complete, deliverable WTH hackathon format with a polished GitHub Pages site
- **Requested by:** Marco Olivo
- **Date:** 2026-05-28

### Challenge Writing Learnings
- WTH student guides work best when they move from motivation to action: introduction, concrete build steps, success checks, docs, hints, then stretch goals.
- Coach guides should emphasize facilitation over answer-giving: timing, diagnostic questions, and likely blockers are as important as the walkthrough.
- Early challenges need extra scaffolding for Azure concepts such as hubs, projects, deployments, endpoints, and content safety because the audience is new to AI and Azure.
- Reusing a single domain theme across challenges (Northfield University) creates continuity and makes later RAG and evaluation work feel intentional instead of disconnected.
- Sample RAG corpora are more useful when each file includes realistic deadlines, office hours, and contacts so retrieval can answer precise questions.
- Completed challenge documentation for Challenges 03-06 on 2026-05-28T16:23:27.374+01:00, including student README guides, coach solution guides, a recorded decision note, and continuity of the University Q&A Assistant narrative across orchestration, RAG, evaluation, and deployment.

### Archived — 2026-05-28 work (summarized 2026-06-01 for size)
Condensed from Content Audit, Humanizer Pass, Inline-Challenge-Content, CSS-fix, and Scribe finalization sessions. Reusable facts retained:
- **Foundry rebrand:** "Azure AI Foundry" → "Microsoft Foundry" for portal/product text only; SDK package names (`azure-ai-projects`, `azure-ai-inference`) unchanged. Audit `solution.md` separately — it lags README updates.
- **azure-ai-projects 2.x:** `from_connection_string()` removed → `AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential())` + `.get_openai_client()` + `openai.responses.create()`. Canonical env var `FOUNDRY_PROJECT_ENDPOINT` (replaces `AZURE_AI_ENDPOINT`/`AZURE_AI_KEY`). `gpt-4.1-mini` = current fast model (was `gpt-4o-mini`). New portal has no Hub step → "Foundry resource + Project". (Prompt Flow has since been CUT entirely.)
- **Humanizer tells:** em dashes pervasive (` — ` in definition lists → `: `; `Title — Coach's Guide` H1 → `Title: Coach's Guide`); keep emojis inside `<span class="meta-badge">` (structural UI), strip them from YAML `title:`/`<h1>`/plain headings; promotional words ("powerful", "showcase", "strong"); rule-of-three. Keep link-label dashes like `[00 — Setup]`.
- **Docs inlining (pre-V2):** challenge content was inlined into `docs/challenges/*` + per-challenge coach pages (`nav_exclude: true`) because Jekyll can't `include_relative` outside source — created a README↔docs two-source drift risk. (V2 later replaced this with the 1:1 mirror.)
- **Platform note:** serial agent dispatch avoids 401/race outages seen with parallel spawn.
- Earlier Scribe finalization (2026-05-28) merged 3 inbox decisions, wrote orch/session logs, committed `.squad/`. The 2026-06-01 V2 direction (Prompt Flow CUT; core spine 00–07; Northfield "IQ" narrative) is captured in `.squad/decisions.md`.

---

## Session Update — 2026-06-01: Authored Tier 1 Foundations challenge

**Session:** Write `challenges/foundations/` README + solution (4 stepped, guided challenge)
**Requested by:** Marco Olivo

### What changed
- **`challenges/foundations/README.md`** rewritten from the seeded challenge-00 setup doc into ONE guided, linear challenge with 4 ordered steps, each in the §3 STEP template (Goal → Tasks → Success Criteria → Checkpoint). Added two-tier intro, scenario table, End-state Checkpoint (`--all`), and a "What's next" Advanced-tier table.
- **`challenges/foundations/solution.md`** rewritten as a coach guide covering all 4 steps: facilitation, full runnable reference snippets, reference system/agent instructions, pitfalls, timing, and a Checkpoint command-contract table for Basher.
- **Harvested-then-removed** three v1 folders via `git rm -r`: `challenge-01-first-model`, `challenge-02-prompt-engineering`, `challenge-04-rag`. Content folded into Steps 2/3/4 first.

### Authoring learnings
- **STEP template discipline:** Success Criteria must be observable/checkable ("agent returns a cited answer"), never learning objectives ("understand RAG"). Every step ends in a `python validate.py --step N` Checkpoint; `--all` asserts the end-state. Authoring to the validator contract (not implementing it — Basher owns `validate.py`) keeps the README/QA boundary clean.
- **Harvest mapping that worked:** ch01 model-deploy + Playground → Step 2; ch02 system-instruction parts → Step 2, persona/guardrails → Step 3; ch04 RAG → Step 4 fully reframed as AI Search index + Foundry IQ knowledge base with NO Prompt Flow nodes (dropped the `rag-flow.dag.yaml` artifact entirely).
- **SDK currency (verified against repo SDK refs):** agents are VERSIONED — `project.agents.create_version(agent_name=..., definition=PromptAgentDefinition(model=, instructions=, tools=[...]))`, NOT the legacy `create_agent`. Drive via Responses API with `extra_body={"agent": {"name": ..., "type": "agent_reference"}}`. Grounding tool = `AzureAISearchToolDefinition` + `AzureAISearchToolResource(indexes=[AISearchIndexResource(index_connection_id=conn.id, index_name=, query_type=AzureAISearchQueryType.VECTOR_SEMANTIC_HYBRID)])`. Connection resolved via `project.connections.get(AZURE_SEARCH_CONNECTION_NAME)`.
- **Env contract:** `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_DEPLOYMENT_NAME`, `AZURE_SEARCH_ENDPOINT`, `AZURE_SEARCH_INDEX_NAME`, `AZURE_SEARCH_CONNECTION_NAME` — all auto-written by `azd up`. Step 4 RBAC blocker is the #1 pitfall: project MI needs Search Index Data Contributor + Search Service Contributor.
- **Citation lesson hook:** the FAFSA question (March 1 priority deadline + school code 041777, from `financial-aid.md`) is the canonical grounded-vs-ungrounded contrast — concrete enough that a hallucination is obvious. Reused as the Step 4 / `--all` verification probe.
- **No answer leakage:** README carries only starter snippets with placeholders/outlines (e.g. `step4_index.py` is an outline, not full code); full runnable code + reference instructions live ONLY in solution.md.

### 2026-06-01 — Curriculum V2 implemented (cross-agent note)
Curriculum V2 is now built to disk (staged, not committed). Final shape: **two-tier** — Tier 1 Foundations (4 ordered steps) + Tier 2 (4 Advanced challenges + 6 Extras). **Prompt Flow fully removed** (deps, devcontainer, challenges, docs). `docs/` mirrors `challenges/` 1:1 with coach siblings. Decision inbox merged into `.squad/decisions.md` (28 entries); session log: `.squad/log/2026-06-01T100000Z-curriculum-v2-build.md`.

### 2026-06-01 — Curriculum V3 proposed (cross-agent note)
V3 planning is **proposed, not implemented**. `CURRICULUM-REASSESSMENT.md` (Rusty) delivers the time+guidance audit, the 3-rung difficulty ladder (graded by the same `validate.py` → zero new validators), and the reskin contract; `PLAN-V3.md` (Danny) adopts them into the 3-tier tree (Foundations → Advanced → MAF Capstone) + de-guided Advanced. Linus's Foundations step deep-links are staged. No challenge content or `.env.sample` changed; no commit. Decisions in the new "Curriculum V3" section of `.squad/decisions.md`; session log: `.squad/log/2026-06-01T120000Z-curriculum-v3-assessment.md`.

### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: all **4 Advanced READMEs
de-guided** to the 3-rung ladder (a guided / b build-from-scratch / c stretch) with a consistent
⏱/🛠/⭐ banner, "why now" hooks, and output anchors; same `validate.py` grades every rung; one
breadcrumb PLACEHOLDER removed from `advanced-action-tools/agent_with_actions.py`. Alongside:
Tier 3 Capstone live (Danny + Basher validator), `scripts/cleanup.sh` + lab-generator (Livingston),
three-tier README/docs (Linus, mirroring my dual-time labels). Inbox merged into `.squad/decisions.md`
("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log:
`.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
