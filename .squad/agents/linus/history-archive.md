# History Archive — Linus

> Archived 2026-06-01 by Scribe (history.md exceeded 15360 B). Verbatim prior history below; active history.md now carries a tight summary.

---

## Learnings

### 2026-06-01 — Curriculum V3: three-tier README + Capstone docs nav (PLAN-V3 §5.1/§5.2)
- **README.md (Task A):** Reframed "two tiers" → "three tiers" in the intro paragraph and the `## Challenges` lead-in (grep confirms `two tiers`=0, `three tiers`=2). Inlined a trimmed PLAN-V3 §1 ASCII tree (trunk → fan → summit) under the Challenges lead-in. Converted the Advanced table from a single Duration column to **dual time columns (Guided / Build-from-scratch)** using Rusty's final labels: Action Tools ~45 min / ~1.5 hr ⭐⭐⭐ (relabelled from the old 1.25 hr), Eval ~1.25 hr / ~2 hr ⭐⭐⭐⭐, Tracing ~1 hr / ~1.5 hr ⭐⭐⭐⭐, Deploy ~60–90 min / ~1.5 hr ⭐⭐⭐⭐⭐. Added a **### Tier 3 — Capstone** section after the Advanced table (description + table with time 2–2.5 hr core +stretches, prereqs Foundations+Action Tools, "make it your own" line). Re-slotted the Extras line: Magentic + Hosted Long-Running = **capstone-feeders**, Build a UI = **capstone companion**, Fabric/Voice/Copilot = **deepeners**. Updated totals: **~7.25 hr Foundations+Advanced guided + ~2.5 hr Capstone** (multi-day story; kept the 1-day variant = Foundations + 2–3 Advanced). Updated the Repository Structure tree to add `challenges/capstone-multi-agent/` and `scripts/cleanup.sh`.
- **Capstone anchor-slug gotcha:** Deep-linked the README to `challenges/capstone-multi-agent/README.md#the-agent-org-chart-role-as-agent`. Source heading is `## The agent org-chart (role-as-agent)` — GitHub strips `(` and `)` but the surrounding hyphen-in-`role-as-agent` is literal, so the slug is `the-agent-org-chart-role-as-agent` (single hyphens; no double-hyphen here since the parens were adjacent to no extra spaces). Verified the heading exists at line 54 before linking.
- **docs/ (Task B):** Created the Capstone mirror pair `docs/challenges/capstone-multi-agent.md` (nav_order **30**) + `capstone-multi-agent-coach.md` (nav_order **130**, `nav_exclude: true`) — band continues the scheme (foundations 1; Advanced 10–13 / coach 110–113; Extras 20–25 / coach 121–125; **Capstone 30 / coach 130**). Generated them faithfully with a **throwaway `/tmp/_mirror_capstone.py`** (same drift-free pattern as the V2 mirror; deleted after) that prepends frontmatter and rewrites links: `solution.md`→`<slug>-coach`, `README.md`→`<slug>`, every other relative repo link → absolute `https://github.com/olivomarco/ai-hackathon/{blob|tree}/main/<normpath>`. All 7 rewritten participant-page links verified to point at real files (`.env.sample`, `foundry-workflows/SKILL.md`, 5 challenge READMEs). Coach page has no markdown links.
- **index.md:** Two-Tier → **Three-Tier + Two-Paths**; reused the §1 ASCII tree at the top; Advanced table gained a **Guided / Scratch** column with the dual-time labels; Extras table gained a **Tree role** column (capstone-feeder / companion / deepener, reordered accordingly); added a **## Tier 3 · Capstone** section with a card table + `Start the Capstone →` button + make-it-your-own line. All sibling links use bare docs slugs (JTD relative).
- **Cleanup page:** Created `docs/challenges/cleanup.md` ("Wrap-Up — Cleanup & Cost Hygiene", parent: Challenges, nav_order **40**) pointing at `scripts/cleanup.sh` (Livingston's). Chose a Challenges child (band 40, after Capstone 30) over a new top-level page to avoid renumbering existing top-level nav_orders (Home 1 … FAQ 6). Documented the script's dry-run-by-default safety + `--yes`/`--local-only`/`--purge` flags read straight from the script header.
- **No collisions / no breakage:** verified zero nav_order collisions among `docs/challenges/*.md`; the 4 Foundations step deep-links I fixed last session are untouched (grep still finds all 4). No challenge READMEs, validate.py, solution.md, PLAN-V2/V3, scripts, or `.env.sample` edited. No git commit.

### 2026-06-01 — Deep-linked Foundations step titles (README + docs)
- **Problem:** Root `README.md` Tier 1 table listed Steps 1–4 as plain text while Tier 2 linked every title. Foundations is a single file (`challenges/foundations/README.md`) with `## Step N` headings, so the fix = deep-link each step title to its heading anchor.
- **Read real headings (never guessed anchors).** Exact source headings:
  - `## Step 1 — Setup & Provisioning (Foundry + AI Search)`
  - `## Step 2 — Model Selection & the Playground`
  - `## Step 3 — Your First Agent`
  - `## Step 4 — Knowledge Base: Index + Foundry IQ  *(← Foundations end-state)*` (note: **two spaces** before `*(`)
- **GitHub anchor algorithm** (verified with a Python repro of `[^\w \-]` strip → spaces→hyphens, no hyphen collapsing): em dash `—`, `&`, `()`, `+`, `:`, `*`, `←` are all stripped but the surrounding spaces each still become a hyphen → **double/triple hyphens are correct, not typos**:
  - `#step-1--setup--provisioning-foundry--ai-search`
  - `#step-2--model-selection--the-playground`
  - `#step-3--your-first-agent`
  - `#step-4--knowledge-base-index--foundry-iq---foundations-end-state` (triple hyphen from the two spaces + stripped `*(←`)
- **Edits:** README Tier 1 table titles wrapped in relative links + added `[Open the full Foundations brief →]` line under the subheading. Mirrored in `docs/challenges/index.md` (cross-page `foundations#step-...`) and `docs/challenges/foundations.md` scenario table (in-page `#step-...`). Jekyll frontmatter / `nav_order` untouched.
- **Convention:** in-repo nav uses relative links only (no `https://github.com/.../blob` URLs).

### Project Context
- **Project:** WTH (What The Hack) AI Hackathon — Microsoft Foundry format
- **Repo:** ai-hackathon
- **Stack:** Microsoft Foundry AI, GitHub Pages (Jekyll/static), Markdown, GitHub Actions
- **Participants:** Students (new to AI) + Coaches (facilitators)
- **Goal:** Create a complete, deliverable WTH hackathon format with a polished GitHub Pages site
- **Requested by:** Marco Olivo
- **Date:** 2026-05-28


### 2026-05-28T16:23:27.374+01:00 — Jekyll site build learnings
- `just-the-docs` treats `color_scheme: default` as a custom scheme name, so the site needs `_sass/color_schemes/default.scss` to build cleanly.
- The participant-facing site works best as a fast, searchable front door: a strong home hero, a plain-language setup guide, challenge stubs for navigation, and a coach-only boundary that keeps solutions out of Pages.
- For local verification, `bundle exec jekyll build -d .site-check` in `docs/` is enough to validate navigation, Markdown rendering, and custom styling before deployment.

### 2026-05-28T20:15:00+01:00 — GitHub Pages CSS fix (root-cause investigation)
- JTD theme requires `docs/assets/css/just-the-docs-default.scss` with Liquid front-matter (`---\n---`) as the stylesheet entry point. Without it Jekyll never compiles the theme CSS, and the layout renders as a naked HTML fragment.
- JTD also requires the `jekyll-include-cache` plugin; its layouts use `{% include_cached %}` which errors silently without the plugin, further breaking layout application.
- `_config.yml` `url` must match the actual GitHub Pages domain (`olivomarco.github.io`, not `microsoft.github.io`) — a mismatched domain causes asset resolution failures even if CSS compiles.
- Always verify `aux_links` and `nav_external_links` point to the correct org/repo after a repo fork or rename — these URLs are easy to miss and affect all site-level links.
- The upstream `just-the-docs-default.scss` on `main` uses Liquid `{% include css/just-the-docs.scss.liquid %}`, not a plain `@import` — fetch the actual upstream file to confirm format before creating it.


---

## Team Update — 2026-05-28 Session Complete

**Session:** Fact-check & CSS fix (multi-batch agent work)

**Major Outcomes:**
- **Microsoft Foundry rebrand applied** — All challenges verified & updated (Azure AI Foundry → Microsoft Foundry)
- **CSS rendering restored** — GitHub Pages now displays with full just-the-docs theme
- **Content verified against current docs** — All SDK versions, deployment patterns, and terminology current (no breaking changes)
- **Humanizer pass complete** — 28 files cleaned of AI-generated patterns (emojis, em dashes, promotional vocab)
- **Cross-page links fixed** — Challenge discovery pages now render without 404s
- **Platform resilience discovered** — Serial agent dispatch works around 401 outages (parallel spawn causes race conditions)

**Next:** Marco needs to `git push` to deploy CSS fix to live site; maintainers must run `cd docs && bundle install` to regenerate Gemfile.lock.

---

## Team Update — 2026-05-28T21:00:00+01:00 — Layout defaults fix

**Session:** Diagnosed & fixed missing `layout: default` — site was returning bare HTML fragments with no chrome

**Root cause confirmed:** No page declared `layout:` in front-matter and `_config.yml` had no `defaults:` block. Jekyll compiled Markdown to fragments but never applied JTD's `_layouts/default.html` shell, so no `<html>`, `<head>`, stylesheet link, sidebar, or body ever rendered. CSS compiled fine — it just was never linked.

**Changes made:**
- `docs/_config.yml` — added `defaults:` block setting `layout: default` for all pages (`path: ""`); fixed stale title (`"Azure AI Foundry"` → `"Microsoft Foundry"`)
- `docs/_sass/custom/custom.scss` — moved from wrong path (`_sass/custom.scss`) to JTD's auto-include path (`_sass/custom/custom.scss`); all custom styles now active
- `.squad/decisions/inbox/linus-layout-defaults.md` — full decision record written

**Deployed:** Committed and pushed to `main`; Pages workflow triggered.

---

## Team Update — 2026-05-28T21:08:00+01:00 — Difficulty badge contrast fix

**Session:** Fixed invisible `.difficulty-badge` text inside `.hero-panel`

**Root cause confirmed:** `.hero-panel` sets `color: white` on its dark-blue background. The cascade rule `{ color: inherit; }` propagated white text to all descendants. `.meta-badge` has its own explicit `color: #fff` + dark bg — fine. But `.difficulty-badge` declared no `color:` at all, so it inherited white text and rendered it on its light pastel backgrounds (`#edf8f0`, etc.) — invisible.

**Changes made:**
- `docs/_sass/custom/custom.scss` — added `color: #1f2937` to `.difficulty-badge` base rule (primary fix); added `.hero-panel .difficulty-badge { color: #1f2937; }` scoped override (defensive belt-and-suspenders)
- `.squad/decisions/inbox/linus-difficulty-badge-contrast.md` — full decision record written
- Colour ramp verified: green → blue → purple → orange → red (easy → hard) — palette correct, no changes needed

**Deployed:** Committed and pushed to `main`; Pages workflow triggered.

---

## Team Update — 2026-05-28T21:25:00+01:00 — Session finalization (Scribe)

**Session:** css-rendering-and-in-pages-content-final-fix (final orchestration)

**Scribe actions completed:**
- Merged `.squad/decisions/inbox/` (3 decision files: linus-layout-defaults.md, linus-difficulty-badge-contrast.md, rusty-inline-challenge-content.md) → `decisions.md`
- Wrote orchestration logs for linus-4 (d65afcf), linus-5 (ec87c21), rusty-5 (62d08e5)
- Wrote session log documenting the three-agent flow and technical decisions
- Updated agent history files (linus, rusty)
- Staged and committed `.squad/` files to main with chore message

**Status:** Session archived. All decisions, logs, and orchestration records persisted.

---

## Team Update — 2026-05-28T21:22:00+01:00 — Jekyll Kramdown markdown="1" fix

**Session:** Fix broken markdown rendering inside HTML block elements

**Root cause confirmed:** Jekyll's Kramdown processor does NOT process markdown content (tables, lists, links, emphasis) inside HTML block-level elements unless the wrapping element carries the `markdown="1"` attribute. Marco screenshotted the broken "Per-challenge coach notes" table in coach-hub.md rendering as raw pipe characters instead of HTML.

**Changes made (4 edits):**
- `docs/coach-hub.md:80` — `<div class="challenge-card">` → `<div class="challenge-card" markdown="1">` (fixes the broken table)
- `docs/setup.md:31` — `<div class="callout-tip">` → `<div class="callout-tip" markdown="1">` (fixes link rendering in Codespaces tip)
- `docs/setup.md:57` — `<div class="callout-warning">` → `<div class="callout-warning" markdown="1">` (fixes link rendering in manual setup warning)
- `docs/setup.md:98` — `<div class="callout-info">` → `<div class="callout-info" markdown="1">` (fixes code and emphasis in validation tip)

**Verification:** `grep -rn '<div class=' docs/ --include="*.md" | grep -v 'markdown="1"' | grep -v 'hero-panel\|quick-grid\|quick-card\|meta-strip\|cta-row\|table-wrapper'` returns zero lines (no broken divs remain).

**Style rule (new):** Every `<div class="callout-*">` or `<div class="challenge-card">` that wraps markdown body content MUST include the `markdown="1"` attribute. Exception: hero-panel, quick-grid, quick-card, meta-strip, cta-row, table-wrapper (no markdown inside).

**Decision record:** `.squad/decisions/inbox/linus-markdown-attr-callouts.md`

**Deployed:** Committed and pushed to `main`; Pages workflow triggered.

---

## Team Update — 2026-05-28T21:30:00+01:00 — Hero panel secondary button contrast fix

**Session:** Fix invisible secondary CTA in homepage hero

**Root cause confirmed:** `.hero-panel` sets `color: #fff` (white text) that cascades to child elements. The secondary "Coaches: Start here" buttons at lines 13 and 67 of `docs/index.md` used plain `.btn` class which JTD renders with a near-white background — resulting in white text on white background, invisible to users.

**Changes made (two-layer fix):**
- `docs/_sass/custom/custom.scss` — added `.hero-panel .btn:not(.btn-primary):not(.btn-purple)` scoped CSS rule setting `color: #1f2937` (dark gray) and `background: rgba(255, 255, 255, 0.92)` with hover enhancement
- `docs/index.md:13` — `<a class="btn" ...>` → `<a class="btn btn-outline" ...>` (adds JTD's outlined-button pattern for secondary CTAs on dark backgrounds)
- `docs/index.md:67` — `<a class="btn btn-lg" ...>` → `<a class="btn btn-outline btn-lg" ...>` (same fix, large variant)
- `.squad/decisions/inbox/linus-hero-btn-contrast.md` — full decision record written

**Forward guidance:** ALL secondary/plain `.btn` elements placed inside a `.hero-panel` must use the `btn-outline` class to ensure readability and consistent UX (outlined style signals secondary action). If a new button is added to `.hero-panel`, pair it with `btn-outline` automatically.

**Deployed:** Committed and pushed to `main`; Pages workflow triggered.

---

### 2026-06-01 — Curriculum V2 direction (Scribe note)
- `PLAN-V2.md` is the new curriculum direction (Proposed): agent-era rearchitecture, core spine 00–07, one-artifact-many-acts Northfield "IQ" Assistant narrative.
- **Prompt Flow is CUT** per Marco's directive — old Challenge 03 removed; dependent RAG/eval steps re-expressed on Agents + AI Search + Foundry IQ + MCP + MAF; `promptflow*` deps leave the devcontainer.
- See `.squad/decisions.md` and `.squad/log/2026-06-01-curriculum-v2-planning.md`.

### 2026-06-01 — docs/ restructured to mirror the final challenge content 1:1
- Replaced the old linear `challenge-00..06` docs pages with a **two-tier mirror**: `docs/challenges/foundations.md` (one anchored page, `## Step N` headings) + 4 Advanced + 6 Extras, each with a `-coach.md` sibling (`nav_exclude: true`). 24 mirror pages total (12 student + 12 coach).
- **Fidelity trick:** generated the mirror with a one-shot Python script (`scripts/_mirror_docs.py`, deleted after) that `cat`s the real `challenges/*/{README,solution}.md` + prepends frontmatter. Hand-copying ~24 large files would have drifted from the source. Faithful 1:1 mirror > manual transcription.
- **Link rewrites in the generator:** `](solution.md)` → `](<slug>-coach)`, `](README.md)` → `](<slug>)`, and every relative repo link → absolute GitHub blob/tree URL (`https://github.com/olivomarco/ai-hackathon/blob|tree/main/...`, resolved via `os.path.normpath`; trailing-slash → `tree`, else `blob`). http/#/mailto left untouched. This keeps published-site links from 404ing.
- **nav_order map:** foundations 1; Advanced 10–13; Extras 20–25; coach pages = student+100 with `nav_exclude: true`. No collisions (verified). Top-level pages 1–6.
- **index.md (Challenges)** rewritten to Two-Tier + **Two-Paths** run guide (Path A Beginner linear; Path B Advanced-skip bootstrap `azd up` → `setup-foundations.sh` → `validate-foundations.py`) with the PLAN-V2 §1.5 ASCII diagram. **Home `index.md`** reconciled away from "seven challenges" to the two-tier framing.
- **Prompt Flow swept** from `docs/coach-hub.md` (removed the `03 Prompt Flow` timing row + the "Prompt flow output is weird" blocker row; rebuilt the per-challenge coach-links table to the 11 new coach pages). Remaining grep hits are only the **deliberate "No Prompt Flow" notes** in `advanced-deploy-hosted-agent{,-coach}.md` mirrored from source — acceptable.
- **Jekyll caveat:** full `bundle exec jekyll build` can't run in this env (gems not installed; real build is GitHub Pages CI). Validated all 28 pages' frontmatter structure with a dep-free Python check instead — 0 problems.
- **Build-a-UI Extra** (`challenges/extra-build-ui/{README,solution}.md`) authored earlier (5 steps, Extras banner, credential-holding BFF + SSE streaming + citations panel + action-approval card) and mirrored into docs as part of this pass.

### 2026-06-01 — Curriculum V2 implemented (cross-agent note)
Curriculum V2 is now built to disk (staged, not committed). Final shape: **two-tier** — Tier 1 Foundations (4 ordered steps) + Tier 2 (4 Advanced challenges + 6 Extras). **Prompt Flow fully removed** (deps, devcontainer, challenges, docs). `docs/` mirrors `challenges/` 1:1 with coach siblings. Decision inbox merged into `.squad/decisions.md` (28 entries); session log: `.squad/log/2026-06-01T100000Z-curriculum-v2-build.md`.

### 2026-06-01 — Curriculum V3 proposed (cross-agent note)
V3 planning is **proposed, not implemented**. Linus deep-linked the 4 Tier 1 Foundations step titles to verified GitHub heading anchors in `README.md` + mirrored in `docs/` (staged). `PLAN-V3.md` (Danny) + `CURRICULUM-REASSESSMENT.md` (Rusty) propose the 3-tier tree, de-guided Advanced, and MAF capstone — the future migration adds a three-tier README + Tier 3 docs nav. No challenge content or `.env.sample` changed; no commit. Decisions in the new "Curriculum V3" section of `.squad/decisions.md`; session log: `.squad/log/2026-06-01T120000Z-curriculum-v3-assessment.md`.

### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: root `README.md` reframed to
**three tiers** (intro + lead-in, trimmed ASCII tree, dual-time Advanced table mirroring Rusty's
labels, new Tier 3 Capstone section, Extras re-slot, repo-tree update); `docs/challenges/capstone-multi-agent.md`
(+ `-coach`) created, `docs/challenges/index.md` updated to three-tier, `docs/challenges/cleanup.md`
wrap-up added (`nav_order` collisions checked — none). Alongside: Capstone live (Danny + Basher),
Advanced de-guided (Rusty), cleanup + lab-generator (Livingston). Inbox merged into `.squad/decisions.md`
("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log:
`.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.
