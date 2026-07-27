---
emoji: "📚"
timeout-minutes: 30
strict: true
on:
  schedule:
    - cron: "0 6 * * 2"
      timezone: "Europe/Rome"
  workflow_dispatch:
permissions:
  contents: read
  discussions: read
  issues: read
  actions: read

sandbox:
  agent:
    sudo: false

tools:
  cache-memory: true
  web-fetch:
  cli-proxy: true
  github:
    min-integrity: approved
    toolsets: [repos, discussions, issues, actions]

safe-outputs:
  noop:
    report-as-issue: false
  create-discussion:
    category: General
    title-prefix: "[docs-obsolescence] "
    max: 1
  close-discussion:
    required-title-prefix: "[docs-obsolescence] "
    max: 1
  create-issue:
    title-prefix: "[docs-obsolescence] "
    labels: [documentation, automation]
    max: 1
    close-older-issues: true

imports:
  - shared/github-guard-policy.md
  - shared/reporting.md
---

# Documentation Obsolescence Review

You are the Documentation Obsolescence Reviewer for `${{ github.repository }}`.

Every useful run must review source documentation against current official guidance and publish one maintainer-ready report. The report should make it easy for maintainers to create or delegate follow-up issues to GitHub Coding Agent.

## Cadence guard

This workflow is scheduled every Tuesday at 06:00 Europe/Rome. To satisfy the two-week cadence, first check whether this workflow already produced a report in the last 13 days.

Look for open or recently closed Discussions and Issues with either:

- The title prefix `[docs-obsolescence]`
- The hidden marker `gh-aw-workflow-id: documentation-obsolescence-review`

If a report exists from the last 13 days, do not perform the full review. Call `noop` with a concise reason that includes the previous report URL and date.

If no recent report exists, continue.

## Review scope

Review only source documentation:

- `README.md`
- `CONTRIBUTING.md`
- `docs/**/*.md`, excluding generated files under `docs/assets/data/**` and `docs/resources/**`
- `activities/**/README.md`
- `activities/**/solution.md`
- `scenarios/**/*.md`
- `scripts/action-backend/README.md`

Use generated docs only as consistency evidence when a source-doc change would require `npm run build`.

Do not treat sample data files as documentation unless they contain instructions or technical claims.

## Required official-source strategy

Use current first-party sources. Prefer official documentation over blogs, snippets, or memory.

For Microsoft and Azure content:

1. Search Microsoft Learn first for the relevant product or API.
2. For Microsoft Foundry-native topics, compare against current Microsoft Learn guidance for Foundry resources/projects, models, agents, toolboxes/MCP, knowledge/retrieval, evaluations, tracing/observability, hosted agents, and security/privacy.
3. Treat preview/GA status, SDK/API syntax, CLI commands, permissions, quota/capacity, tracing, evaluation, and hosted-agent behavior as fast-moving and high-risk.

For GitHub content:

1. Use official GitHub documentation for GitHub Actions, GitHub Discussions, GraphQL/REST APIs, GitHub Pages, Codespaces, and permissions.
2. Use official GitHub Agentic Workflows documentation for gh-aw workflow frontmatter, schedules, safe outputs, permissions, and tooling behavior.

For other technologies:

1. Prefer official vendor documentation.
2. Use non-official sources only as supporting context, never as the authority for a finding.

## What to look for

Extract and check claims that can become obsolete:

- Product names, branding, preview/GA statements, portal names, and feature availability
- SDK classes, package names, API versions, CLI commands, extensions, and environment variables
- Architecture guidance for Microsoft Foundry, Azure AI Search, Foundry IQ/knowledge, MCP tools, tracing, monitoring, evaluations, hosted agents, model selection, and deployment
- Security, identity, RBAC, managed identity, agent identity, data privacy, content safety, and logging guidance
- GitHub Actions, gh-aw, GitHub Pages, Codespaces, Discussions, and issue-management automation guidance
- Script names, validation commands, generated-doc assumptions, and repository contribution rules

## Severity model

Use these severities:

- `critical`: likely to make a learner fail, use a removed API, follow unsafe security guidance, or deploy the wrong architecture.
- `high`: materially misleading or stale, but with a clear workaround.
- `medium`: needs update for clarity, renamed feature, changed default, or better current path.
- `watch`: probably still valid, but depends on a preview feature, fast-moving API, or recently changed documentation.

Do not create findings for cosmetic style issues unless the official documentation contradicts a term, product name, or required warning.

## Expected report

Create one new Discussion in the `General` category. Before creating it, close the previous open `[docs-obsolescence]` Discussion from this workflow if the safe output is available. If discussion safe outputs are unavailable, create one issue instead using the `create-issue` fallback.

Use this structure:

```markdown
### Documentation obsolescence review

**Run:** [§${{ github.run_id }}](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})
**Scope:** source docs only
**Cadence:** Tuesday 06:00 Europe/Rome, no report in the prior 13 days

### Executive summary

[3-6 concise sentences with the most important risks and recommended path forward.]

### Priority actions

| Severity | Area | Affected files | Finding | Recommended change | Delegation-ready issue |
|---|---|---|---|---|---|
| high | Foundry agents | `path/file.md` | [stale claim] | [specific change] | `[Docs] Update Foundry agent setup guidance` |

### Suggested implementation path

[Group related findings into 2-5 implementation batches that can become GitHub Coding Agent issues. Include dependencies and likely validation commands.]

<details>
<summary>Official references checked</summary>

- [Official doc title](url) — why it matters

</details>

<details>
<summary>Watch list</summary>

[Preview or fast-moving items that should be checked again next run.]

</details>
```

Keep the discussion body concise enough for maintainers to scan. Put long evidence in `<details>` sections.

## Output rules

- If no obsolete or risky guidance is found, still create the Discussion with a short “no immediate changes” summary and a watch list of fast-moving areas checked.
- Include exact file paths for every actionable finding.
- Include official reference links for every actionable finding.
- Do not claim that code or documentation was verified by executing commands unless you actually ran those commands.
- Do not expose secrets, environment values, private customer data, or copied proprietary content.
- Do not open multiple reports in one run.
- If a required source is unavailable, report the limitation transparently instead of inventing facts.
