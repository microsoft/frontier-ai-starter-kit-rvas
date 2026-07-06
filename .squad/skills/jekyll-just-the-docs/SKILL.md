# SKILL: Jekyll + Just the Docs Event Site

## What This Skill Covers
Building a polished GitHub Pages documentation site in `docs/` with Jekyll and the `just-the-docs` theme for sessions, workshops, or training content.

## When to Use
- Creating a participant-facing GitHub Pages site for an event or curriculum
- Turning a repo into a searchable docs experience with sidebar navigation
- Shipping site scaffolding before full content is available

## The Pattern

### Core Structure
- `docs/_config.yml` for site metadata, nav behavior, search, links, and plugins
- `docs/index.md` as the high-clarity landing page with a strong CTA
- `docs/setup.md`, `docs/facilitator-hub.md`, and `docs/faq.md` for fast answers on event day
- `docs/activities/index.md` plus `docs/activities/activity-NN.md` stubs to keep navigation stable while content arrives in waves

### Styling Strategy
- Extend `just-the-docs`; do not fight it
- Put custom layout and component styles in `docs/_sass/custom.scss`
- Use a dedicated color scheme file when the config references a named scheme such as `default`: `docs/_sass/color_schemes/default.scss`
- Favor small, memorable UI moves: hero section, activity badges, scan-friendly callouts, responsive table handling

### Content Strategy
- Keep the home page outcome-oriented: what this is, who it is for, what to do next
- Make setup instructions branch by participant reality: Codespaces, local devcontainer, manual fallback
- Separate facilitator guidance from student guidance without exposing full solutions publicly
- Use placeholder activity pages early so links and sidebar structure do not churn later

### Local Validation
1. Create `docs/Gemfile` with Jekyll + `just-the-docs`
2. Run `bundle install` inside `docs/`
3. Run `bundle exec jekyll build -d .site-check`
4. Verify generated HTML for key pages and navigation targets

## Pitfalls to Avoid
- Setting `color_scheme: default` without creating `_sass/color_schemes/default.scss`
- Publishing facilitator solutions on the public Pages site
- Relying on dense prose instead of scan-friendly sections and tables
- Leaving activity navigation incomplete until the content wave is finished
