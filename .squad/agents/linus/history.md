# Linus — History (tight summary)

> Older detail archived to `history-archive.md` (2026-06-01, size gate). This file keeps the durable facts + current state.

## Project Context
- **Project:** AI Starter Kit RVAS — Microsoft Foundry format · **Repo:** ai-starter-kit-rvas · **Requested by:** Marco Olivo.
- Role: Frontend Dev / Docs. GitHub Pages site uses Jekyll + **just-the-docs (JTD)**.

## Durable learnings / gotchas (JTD + docs)
- **JTD build essentials:** needs `docs/assets/css/just-the-docs-default.scss` with Liquid front-matter as the stylesheet entry; needs `jekyll-include-cache` plugin; `_config.yml` `url` must match the real Pages domain (`olivomarco.github.io`); add a `defaults:` block setting `layout: default` for all pages or pages render as bare HTML fragments. Custom SCSS must live at `_sass/custom/custom.scss` (auto-include path).
- **Kramdown rule:** any `<div class="callout-*">` / `<div class="activity-card">` wrapping markdown body MUST carry `markdown="1"`, else tables/links render as raw pipes. Exceptions: hero-panel, quick-grid, quick-card, meta-strip, cta-row, table-wrapper.
- **Contrast rule:** `.hero-panel` cascades white text — secondary `.btn` inside it must use `btn-outline`; `.difficulty-badge` needs an explicit `color: #1f2937`.
- **GitHub anchor algorithm** (verified via Python repro of `[^\w \-]` strip → spaces→hyphens, no collapsing): stripped punctuation between spaces yields **double/triple hyphens that are correct** (e.g. Step 4 `…foundry-iq---foundations-end-state` from two spaces + stripped `*(←`). Always read the real heading before deriving a slug.
- **docs mirror fidelity:** generate the `docs/activities/*` mirror with a throwaway Python script (cat real `activities/*/{README,solution}.md` + prepend frontmatter + rewrite links: `solution.md`→`<slug>-facilitator`, `README.md`→`<slug>`, other relative repo links → absolute `github.com/microsoft/frontier-ai-starter-kit-rvas/{blob|tree}/main/…`). Faithful 1:1 > hand-copy.
- **nav_order bands:** foundations 1; Advanced 10–13 / facilitator 110–113; Extras 20–25 / facilitator 121–125; **Capstone 30 / facilitator 130**; cleanup 40. Facilitator pages = student+100 with `nav_exclude: true`. Verify zero collisions.
- **In-repo nav** uses relative links only (no blob URLs); published docs mirror uses absolute URLs.
- Jekyll can't fully build in this env (gems absent — real build is Pages CI); validate frontmatter with a dep-free Python check instead.

## What I built (cumulative, staged — not committed)
- Restored JTD CSS/layout (multiple root-cause fixes); humanizer + contrast + markdown="1" passes.
- Restructured `docs/` to a 1:1 mirror of `activities/` (24 pages: 12 student + 12 facilitator) + Two-Path run guide; swept Prompt Flow from docs.
- Authored **Build-a-UI** Extra (BFF + SSE streaming + citations + action-approval card).
- Deep-linked the 4 Foundations step titles to verified heading anchors (README + docs).
- **Migrated root README + docs/ to three-tier** (V3): dual-time Advanced table mirroring Rusty's labels, new Tier 3 Capstone section, Extras re-slot (feeders/companion/deepeners), repo-tree update; created `docs/activities/capstone-multi-agent.md` (+ `-facilitator`), updated `index.md`, added `docs/activities/cleanup.md`.

## Current state
### 2026-06-01 — PLAN-V3 IMPLEMENTED (cross-agent note)
PLAN-V3 is now **implemented** (staged, not committed). My piece: root `README.md` reframed to three tiers (trimmed ASCII tree, dual-time Advanced table, Tier 3 Capstone section, Extras re-slot, repo-tree); `docs/activities/capstone-multi-agent.md` (+ `-facilitator`) created, `index.md` updated to three-tier, `docs/activities/cleanup.md` wrap-up added (no nav_order collisions). Alongside: Capstone live (Danny + Basher), Advanced de-guided (Rusty), cleanup + lab-generator (Livingston). Inbox merged into `.squad/decisions.md` ("Curriculum V3 — Three-Tier IMPLEMENTATION (BUILT)"); session log: `.squad/log/2026-06-01T123500Z-plan-v3-implementation.md`.

## Learnings
### 2026-06-01 — HOME page was stale two-tier
- `docs/index.md` (Jekyll Home, title: Home, nav_order: 1) was still **two-tier**: frontmatter description, "What is this?" prose, the "Two tiers, two paths" quick-card, and the "## Two tiers" heading all omitted Tier 3 Capstone. The Foundations Step table rows were **plain text with NO links**.
- Fixed to **three-tier**: description + prose + quick-card + heading now say three tiers; added a Tier 3 Capstone blurb + table + "Start the Capstone →" button linking `activities/capstone-multi-agent`.
- Linked all 4 Foundations steps to their verified heading anchors using the home-page prefix `activities/foundations#...` (home page links use the `activities/` prefix, unlike `activities/index.md` which uses bare `foundations#...`).
- **Canonical source of truth = `docs/activities/index.md`** (already correct three-tier). The Home page is a summary mirror of it — keep them aligned, do not let Home drift.

### 2026-06-01 — Docs visual refresh + markdown spacing normalization
- A maintainable Just-the-Docs redesign can stay inside `docs/_sass/custom/custom.scss` + `docs/_sass/color_schemes/default.scss` without changing layouts/plugins: typography, tokenized colors, nav polish, hero treatment, card/table surfaces, and button hierarchy all updated in theme-safe CSS only.
- For this repo, broad markdown rendering defects were primarily spacing-separation issues (heading/list/code block adjacency). A conservative normalization pass that inserts blank lines around headings, list blocks, and checkpoint code fences fixed defects without changing wording/content architecture.
- `bundle exec jekyll build` is still the right sanity check, but in this environment it fails until `bundle install` is run in `docs/` (missing gem set). When gems are absent, diff review + structural spacing checks are the practical fallback.

### 2026-06-01 — Cross-agent note (Scribe merge batch)
- Basher completed a markdown QA audit for the docs UI/formatting pass and flagged no blocking regressions; completion arrived as silent execution, so the Scribe batch recorded it via orchestration log evidence.

### 2026-06-01 — ASCII follow-up: explicit fan-out + wrap-safe architecture lines
- In `docs/activities/extra-magentic-workflows.md`, ambiguous fan-out labels were replaced with a branch-per-target layout ending in four labeled boxes (`Triage`, `Knowledge`, `Action`, `Escalation`) so mapping is explicit at a glance.
- In `docs/activities/extra-build-ui.md`, the long architecture line was split into shorter lines (`BFF / proxy`, credential hop, endpoint path, runtime branch, knowledge/action branch) to reduce markdown line-wrap risk without changing semantics.
- Verification pattern: re-read only touched diagram blocks after patch and check for connector continuity (`|`, `v`, `+-->`, `-->`) to avoid introducing malformed ASCII links while doing targeted doc fixes.

### 2026-06-01 — Cross-agent note (diagram-fix batch closed)
- Basher QA audit and follow-up review criteria were satisfied for the two remaining ASCII defects.
- Scribe merged related decision records and logged the batch under orchestration + session logs.
