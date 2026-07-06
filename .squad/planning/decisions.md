# Decisions Archive

## 2026-05-28

### Decision: Apply just-the-docs Default Layout to All Pages

**Date:** 2026-05-28  
**Author:** Linus (Site/Chrome specialist)  
**Status:** Implemented

---

#### What Was Wrong

`curl -sL https://olivomarco.github.io/ai-starter-kit-rvas/` returned raw HTML fragments — `<div>`, `<h1>`, `<h2>` — with no `<html>`, `<head>`, `<link rel="stylesheet">`, or `<body>` tag.

**Root cause:** No page had `layout: default` in its front-matter, and `docs/_config.yml` had no `defaults:` block to set a fallback. Jekyll converts Markdown to an HTML fragment but never wraps it in a layout unless told to. The just-the-docs `_layouts/default.html` is the file that injects the full HTML shell — `<html><head>` with the stylesheet `<link>`, sidebar, search bar, header, and footer. Without it, visitors see unstyled, chrome-less content.

##### Secondary issue: `_sass/custom.scss` at wrong path

`docs/_sass/custom.scss` existed but was **not** being auto-included by just-the-docs. JTD's convention is `_sass/custom/custom.scss`. The file was sitting in `_sass/` directly, making all custom styles dead code.

##### Tertiary issue: stale title

`docs/_config.yml` `title:` still read `": Build Intelligent Apps with Azure AI Foundry"` after the project-wide rename to "Microsoft Foundry".

---

#### The Fix

##### Fix 1 — `defaults:` block in `_config.yml`

```yaml
defaults:
  - scope:
      path: ""
    values:
      layout: default
```

Jekyll's `defaults:` lets you set front-matter values for any path glob. `path: ""` matches every file in the site. This means every page that does not explicitly declare a `layout:` gets `layout: default` injected, causing JTD's full HTML shell to wrap the converted Markdown.

##### Fix 2 — Move `_sass/custom.scss` → `_sass/custom/custom.scss`

just-the-docs 0.12 auto-imports `_sass/custom/custom.scss` at the end of its Sass pipeline. The file was at `_sass/custom.scss` (wrong), so none of the custom styles (hero panels, callouts, difficulty badges, etc.) were ever compiled into the output CSS. Moving the file to the expected path activates them.

##### Fix 3 — Correct site title

Changed `title:` from `": Build Intelligent Apps with Azure AI Foundry"` to `": Build Intelligent Apps with Microsoft Foundry"` to match the rest of the content.

---

#### Why JTD 0.12 Needs Explicit `defaults:` When Pages Lack `layout:` Front-Matter

Jekyll has no "automatic layout" feature — it only applies a layout when:
1. The page's own front-matter declares `layout: <name>`, or
2. A matching `defaults:` rule in `_config.yml` injects one.

Some themes (e.g., Minima) declare `layout: default` in their own `_layouts/` definitions so that pages inherit it via Jekyll's layout chain. just-the-docs does **not** do this — its `default` layout is the top-level entry point, not a base inherited automatically.

Therefore, a fresh JTD site with no `defaults:` block and no per-page `layout:` in front-matter will build successfully (no errors) but output completely unstyled, shell-less HTML fragments. The Sass pipeline and all theme assets compile fine — they just never get linked to any page. This is a known "silent failure" mode for JTD.

The `defaults:` fix is the recommended solution in JTD's documentation and is what the JTD starter template includes out of the box.

---

### Decision: Difficulty Badge Contrast Fix in Hero Panels

**Date:** 2026-05-28
**Author:** Linus (Site / Chrome specialist)
**Status:** Applied

---

#### Bug Observed

On `https://olivomarco.github.io/ai-starter-kit-rvas/activities/activity-00.html`, the
`.difficulty-badge.difficulty-1` badge ("⭐ Beginner") was invisible inside the hero panel.
It rendered as white text on a `#edf8f0` near-white light-green background — essentially
unreadable.

#### Root Cause

`.hero-panel` sets `color: white` (dark blue bg, all text white). The cascade rule:

```scss
.hero-panel h1, .hero-panel p, .hero-panel a, .hero-panel strong { color: inherit; }
```

propagates white text to descendants. `.meta-badge` explicitly declares `color: #fff` with
a dark translucent background — fine. But `.difficulty-badge` had **no explicit `color:`
declaration**, so it inherited the parent's white text and rendered it on its own light
pastel background (e.g. `#edf8f0`). Result: invisible.

#### Two-Layer Fix Applied

##### 1. Primary fix — explicit color on `.difficulty-badge`

Added `color: #1f2937` (dark slate) directly to the base `.difficulty-badge` rule so all
badges, everywhere in the document, always carry their own readable text color regardless
of parent context.

##### 2. Defensive fix — `.hero-panel .difficulty-badge` scoped override

Added a hero-scoped override:

```scss
.hero-panel .difficulty-badge {
  color: #1f2937;
}
```

This is belt-and-suspenders: even if a future refactor drops or changes the base
`.difficulty-badge` color, hero panel placements are protected by a higher-specificity rule.

#### Colour Ramp Sanity Check

| Class         | Background | Semantic Meaning |
|---------------|------------|-----------------|
| `.difficulty-1` | `#edf8f0` | Light green — Beginner ✅ |
| `.difficulty-2` | `#eef6ff` | Light blue — Easy ✅ |
| `.difficulty-3` | `#f4f0ff` | Light purple — Intermediate ✅ |
| `.difficulty-4` | `#fff3e6` | Light orange — Advanced ✅ |
| `.difficulty-5` | `#ffe8e8` | Light red — Expert ✅ |

Palette is intuitive (cool→warm, easy→hard). No changes made.

---

### Decision: Inline Activity Content Instead of GitHub Links

**Date:** 2026-05-28  
**Author:** Rusty (Content / Editorial)  
**Status:** Accepted

---

#### Decision

All hands-on activity content (Step-by-step, Success Criteria, Tips, Advanced) has been inlined directly into the `docs/activities/activity-XX.md` Pages files rather than linking out to the source READMEs in `activities/*/` via GitHub blob/tree URLs.

---

#### Why inline instead of `include_relative`

Jekyll's `include_relative` tag resolves paths relative to the current file and the Jekyll source directory. The source activity READMEs live in `activities/activity-XX-NAME/README.md` at the repository root, which is **outside** the Jekyll source directory (`docs/`). Jekyll cannot include files from outside its source directory, making `include_relative` (or `{% include %}` with a base-path workaround) unworkable without restructuring the repository layout.

Alternatives considered:

- **Symlinks**: Not supported by GitHub Pages builds running on the Actions `jekyll-build-pages` action.
- **Pre-build copy step**: Would require a custom workflow step to copy files before Jekyll builds, adding CI complexity and still creating duplication.
- **Direct inlining**: Straightforward, no build changes required, and works with the current Jekyll/Pages setup. Chosen for its simplicity.

---

#### Drift risk: two sources of truth

Inlining creates a **known drift risk** between:

- `activities/activity-XX-NAME/README.md` (the Codespaces working-folder version, used inside the dev container)
- `docs/activities/activity-XX.md` (the Pages-rendered version, viewed in the browser)

Future content updates — new steps, corrected commands, SDK version changes — **must be applied to both files**. The recommended workflow is:

1. Edit `activities/activity-XX-NAME/README.md` first (the authoritative hands-on guide).
2. Reflect the same changes in `docs/activities/activity-XX.md` (the Pages version).
3. If a facilitator solution changes, update both `activities/activity-XX-NAME/solution.md` and `docs/activities/activity-XX-facilitator.md`.

A future automation option would be a CI check that detects out-of-sync section content between the two files and raises a PR review comment. This has not been implemented yet.

---

#### `nav_exclude: true` for facilitator pages

The 7 new `docs/activities/activity-XX-facilitator.md` pages are set to `nav_exclude: true` in their front-matter. This hides them from the just-the-docs sidebar navigation so students browsing the site do not encounter the solution path before attempting the activity.

They are still:

- **rendered by Jekyll** and accessible at their URL (e.g., `/activities/activity-00-facilitator`)
- **indexed by search** (`search_exclude: false`) so facilitators can find them via the site search bar
- **linked from the Facilitator Hub** (`/facilitator-hub`) in the per-activity facilitator notes table

The choice of `nav_exclude: true` over a separate authentication layer reflects the event context: this is a facilitated session with trusted facilitators, not a public exam. The soft barrier (not in the nav, not advertised to students) is sufficient. Full access control would require a backend that GitHub Pages cannot provide.

---

#### References

- [Jekyll include_relative documentation](https://jekyllrb.com/docs/includes/)
- `docs/facilitator-hub.md`: facilitator landing page with per-activity facilitator notes table
- `docs/activities/activity-XX-facilitator.md`: the 7 new facilitator pages created in this session
