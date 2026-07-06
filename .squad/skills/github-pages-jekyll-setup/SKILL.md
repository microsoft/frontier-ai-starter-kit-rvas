# SKILL: GitHub Pages Jekyll Setup

## What This Skill Covers
Setting up a session repository for GitHub Pages delivery with Jekyll, contributor templates, and repo bootstrap automation.

## When to Use
- Bootstrapping a docs-first repository that publishes from `docs/`
- Adding a minimal Pages pipeline for Jekyll + `just-the-docs`
- Standardizing repo scaffolding so forks are easy to self-host and extend

## The Pattern

### Pages Workflow
1. Trigger deployment only when `docs/**` changes on `main`
2. Use `ruby/setup-ruby` with a `docs/Gemfile`
3. Build with `bundle exec jekyll build --source docs --destination _site`
4. Upload `_site` as the Pages artifact and deploy with `actions/deploy-pages`

### Repo Bootstrap
- Create empty activity/doc/resource folders with `.gitkeep` so the intended structure survives the first commit
- Put Python/Azure prerequisites in repo-root `requirements.txt` and `.env.example`
- Add an idempotent post-create script to install dependencies, seed `.env`, and show next steps
- Provide organizer-facing provisioning automation that checks for existing resources before creating anything

### Contributor Hygiene
- Ignore generated Python, Jekyll, Azure, and local editor files without hiding tracked template files
- Add issue templates for broken instructions and content improvements
- Add a PR template that forces contributors to state testing and affected activities

## Anti-Patterns to Avoid
- Deploying Pages on every push regardless of whether docs changed
- Hard-coding secrets into scripts or committed `.env` files
- Non-idempotent provisioning scripts that fail on reruns
- Publishing facilitator-only solution content to the public docs site
