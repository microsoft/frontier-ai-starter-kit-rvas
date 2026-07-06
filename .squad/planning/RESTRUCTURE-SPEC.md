# RESTRUCTURE SPEC — Two-Tier Curriculum (Foundations + Advanced)

> **Build spec for the team.** Authored by Danny (Lead & Content Architect), 2026-06-01.
> Source of truth for the locked structure in [PLAN-V2.md](PLAN-V2.md). Rusty (content),
> Livingston (DevOps), Linus (frontend/docs), and Basher (QA/facilitator) build against this.
>
> **Locked model:** Tier 1 **Foundations** = ONE guided, linear activity with 4 ordered STEPS
> (everyone does it). Tier 2 **Advanced** = modular, self-contained activities, any order, all
> assuming the Foundations end-state. A **bootstrap skip-path** materializes the Foundations
> end-state in ~10–15 min with a single checkpoint. **Prompt Flow is removed everywhere.**

---

## 1. New `activities/` Folder Layout

One folder per unit. Each folder contains exactly two authored files plus an optional `validate.py`:

- `README.md` — **student-facing** (the activity/steps).
- `solution.md` — **facilitator-facing** (facilitation, pitfalls, answers — never leaked to students).
- `validate.py` — **optional but recommended** — implements the Checkpoints (see §3).
- `assets/` — optional, per-unit images/snippets/datasets.

```text
activities/
  foundations/                         # TIER 1 — single guided activity, Steps 1–4
    README.md                          #   stepped: Step 1→2→3→4, each with a Checkpoint
    solution.md                        #   facilitator guide for all 4 steps
    validate.py                        #   validate.py --step {1..4}  and  --all (end-state)
    assets/

  advanced-action-tools/               # TIER 2 — modular, any order
    README.md
    solution.md
    validate.py
  advanced-evaluation-redteam/
    README.md
    solution.md
    validate.py
  advanced-tracing-observability/
    README.md
    solution.md
    validate.py
  advanced-deploy-hosted-agent/
    README.md
    solution.md
    validate.py

  extra-fabric-iq/                     # TIER 2 — Extras (modular, optional)
    README.md
    solution.md
  extra-voice-live/
    README.md
    solution.md
  extra-magentic-workflows/
    README.md
    solution.md
  extra-hosted-longrunning/
    README.md
    solution.md
  extra-build-ui/
    README.md
    solution.md
  extra-copilot-assisted/
    README.md
    solution.md
```

### 1.1 Naming rules (locked)

- Tier 1: the single folder is **`foundations/`** (no number prefix — it is one activity with steps).
- Advanced activities: prefix **`advanced-`** + kebab slug.
- Extras: prefix **`extra-`** + kebab slug.
- No numeric ordering prefixes on Advanced/Extra folders — they are **pickable in any order**, and a
  number would imply a sequence that does not exist.

---

## 2. Old → New Folder Map (with `git mv` guidance)

The physical repo today holds the **v1** folders (`activity-00-setup` … `activity-06-deploy`).
Below maps each to the new layout. **Preserve git history** with `git mv` where a folder is renamed;
**harvest-then-remove** where v1 content is folded into the stepped Foundations README; **delete** the
Prompt Flow folder outright.

| OLD folder (v1) | Action | NEW destination | Notes |
|---|---|---|---|
| `activity-00-setup/` | `git mv` (seed) | `activities/foundations/` | Becomes the seed of the stepped activity; Rusty rewrites `README.md` into Step 1 + adds Steps 2–4 |
| `activity-01-first-model/` | **harvest → remove** | folded into `foundations/` **Step 2** | Reuse model-deploy/Playground content as Step 2; then `git rm -r` after harvest |
| `activity-02-prompt-engineering/` | **harvest → remove** | folded into `foundations/` **Step 2–3** | System-instruction content → Step 2; agent persona/guardrails → Step 3; then `git rm -r` |
| `activity-03-prompt-flow/` | **DELETE** | — | **Prompt Flow is cut.** `git rm -r activities/activity-03-prompt-flow` — do **not** migrate |
| `activity-04-rag/` | **harvest → remove** | folded into `foundations/` **Step 4** | RAG content reframed as Index + Foundry IQ knowledge base (no Prompt Flow nodes); then `git rm -r` |
| `activity-05-evaluation/` | `git mv` | `activities/advanced-evaluation-redteam/` | Rename; expand with red-teaming + `evaluate.py` |
| `activity-06-deploy/` | `git mv` | `activities/advanced-deploy-hosted-agent/` | Rename; re-target from flow-deploy to hosted-agent (`azd ai agent`) |
| *(none — new content)* | **create** | `activities/advanced-action-tools/` | New: MCP action tool + provided backend |
| *(none — new content)* | **create** | `activities/advanced-tracing-observability/` | New: OTel GenAI → App Insights → KQL |
| *(none — new content)* | **create** | `activities/extra-fabric-iq/` | New |
| *(none — new content)* | **create** | `activities/extra-voice-live/` | New |
| *(none — new content)* | **create** | `activities/extra-magentic-workflows/` | New |
| *(none — new content)* | **create** | `activities/extra-hosted-longrunning/` | New |
| *(none — new content)* | **create** | `activities/extra-build-ui/` | New |
| *(none — new content)* | **create** | `activities/extra-copilot-assisted/` | New |

### 2.1 Concrete `git mv` / `git rm` sequence (Livingston runs once)

```bash
cd /home/marco/ai-starter-kit-rvas

# 1. Seed Foundations from the setup activity (preserves history)
git mv activities/activity-00-setup activities/foundations

# 2. Rename the two Advanced activities that have v1 ancestors
git mv activities/activity-05-evaluation  activities/advanced-evaluation-redteam
git mv activities/activity-06-deploy      activities/advanced-deploy-hosted-agent

# 3. DELETE Prompt Flow (cut — no migration)
git rm -r activities/activity-03-prompt-flow

# 4. Harvest content from these into foundations/README.md (Steps 2–4) BEFORE removing.
#    Do the content move in a PR with Rusty, then remove the now-empty v1 folders:
git rm -r activities/activity-01-first-model
git rm -r activities/activity-02-prompt-engineering
git rm -r activities/activity-04-rag

# 5. Create the net-new Advanced + Extra folders (empty README/solution scaffolds)
mkdir -p activities/advanced-action-tools \
         activities/advanced-tracing-observability \
         activities/extra-fabric-iq \
         activities/extra-voice-live \
         activities/extra-magentic-workflows \
         activities/extra-hosted-longrunning \
         activities/extra-build-ui \
         activities/extra-copilot-assisted
```

> **Harvest-before-remove discipline:** Steps 4/3/2 of `foundations/README.md` reuse text from the
> v1 `activity-04-rag`, `activity-02-prompt-engineering`, and `activity-01-first-model` READMEs.
> Do the copy in the same PR that `git rm`s them so no content is lost. Facilitator `solution.md` files
> from those v1 folders are harvested into `foundations/solution.md`.

---

## 3. Standard STEP Template (copy-paste skeleton)

Every **Foundations step** and every **Advanced/Extra activity step** MUST use this exact four-part
shape: **Goal → Tasks → Success Criteria → Checkpoint**. Authors fill the angle-bracket placeholders.

```markdown
### Step <N> — <Step Title>

**Goal:** <One sentence: what becomes true after this step.>

**Tasks:**
1. <Do this — portal or code. Be specific; name the resource/tool/file.>
2. <Then this.>
3. <Then this.>

**Success Criteria:**
- [ ] <Observable, checkable statement, e.g. "The agent returns an answer with at least one citation.">
- [ ] <Another checkable statement.>

**Checkpoint:** <The exact command or portal state that proves the step is done.>
```text
# e.g. machine-checkable command:
python validate.py --step <N>
# expected: "✅ Step <N> PASS"
```
> _Facilitator note (solution.md only): <facilitation tip, common pitfall, the actual answer/snippet>._
```

### 3.1 Rules for the template

- **Foundations** `README.md` contains **Step 1 → Step 2 → Step 3 → Step 4** in order; Step N's
  Checkpoint is the prerequisite for Step N+1. The final Checkpoint (`--all`) asserts the **end-state**.
- **Advanced/Extra** `README.md` opens with a **"Prerequisite: Foundations end-state"** banner, then its
  own numbered Steps using the same skeleton.
- **Success Criteria** must be observable/checkable (no "understand X" — that is a learning objective,
  not a criterion).
- **Checkpoint** should prefer a `validate.py` invocation; a portal-state description is acceptable when
  no programmatic check exists.
- Facilitator answers live **only** in `solution.md` (or in `> _Facilitator note_` blocks that are stripped from the
  student build) — never inline in the student `README.md`.

### 3.2 Advanced/Extra README header banner (paste at top of each)

```markdown
> **Tier 2 · Advanced — modular.** You can attempt this in any order with the other Advanced
> activities. **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
```

---

## 4. New `docs/activities/` Page Layout (Jekyll, mirror 1:1)

Linus updates the `just-the-docs` site so the discovery layer mirrors the folder layout. Foundations is
**one parent page with four step sub-pages (or one long page with anchors)**; each Advanced/Extra is one
page + a facilitator sibling.

```text
docs/activities/
  index.md                              # nav landing — Two-Tier overview + Two Paths (A/B) + diagram
  foundations.md                        # Tier 1 page — Steps 1–4 (single page, anchored) ; nav_order 1
  foundations-facilitator.md                  # facilitator companion for Foundations

  advanced-action-tools.md              # Tier 2 — one page per Advanced activity
  advanced-action-tools-facilitator.md
  advanced-evaluation-redteam.md
  advanced-evaluation-redteam-facilitator.md
  advanced-tracing-observability.md
  advanced-tracing-observability-facilitator.md
  advanced-deploy-hosted-agent.md
  advanced-deploy-hosted-agent-facilitator.md

  extra-fabric-iq.md                    # Tier 2 — Extras
  extra-fabric-iq-facilitator.md
  extra-voice-live.md
  extra-voice-live-facilitator.md
  extra-magentic-workflows.md
  extra-magentic-workflows-facilitator.md
  extra-hosted-longrunning.md
  extra-hosted-longrunning-facilitator.md
  extra-build-ui.md
  extra-build-ui-facilitator.md
  extra-copilot-assisted.md
  extra-copilot-assisted-facilitator.md
```

### 4.1 Old → New docs page map

| OLD page | Action | NEW page |
|---|---|---|
| `activity-00.md` / `-facilitator.md` | merge → | `foundations.md` (Step 1 section) / `foundations-facilitator.md` |
| `activity-01.md` / `-facilitator.md` | merge → | `foundations.md` (Step 2 section) / `foundations-facilitator.md` |
| `activity-02.md` / `-facilitator.md` | merge → | `foundations.md` (Step 3 section) / `foundations-facilitator.md` |
| `activity-03.md` / `-facilitator.md` | **DELETE** (Prompt Flow) | — |
| `activity-04.md` / `-facilitator.md` | merge → | `foundations.md` (Step 4 section) / `foundations-facilitator.md` |
| `activity-05.md` / `-facilitator.md` | rename → | `advanced-evaluation-redteam.md` / `-facilitator.md` |
| `activity-06.md` / `-facilitator.md` | rename → | `advanced-deploy-hosted-agent.md` / `-facilitator.md` |
| *(new)* | create → | `advanced-action-tools.md` / `-facilitator.md` |
| *(new)* | create → | `advanced-tracing-observability.md` / `-facilitator.md` |
| *(new)* | create → | all `extra-*.md` / `-facilitator.md` |

### 4.2 Jekyll nav frontmatter

- `foundations.md`: `parent: Activities`, `nav_order: 1`, `has_children: false` (single anchored page).
  Add a "Tier 1 · Foundations" kicker. Step headings use `## Step 1 …` anchors for the sidebar TOC.
- Each Advanced page: `parent: Activities`, `nav_order: 10,11,12,13` (group Advanced together).
- Each Extra page: `parent: Activities`, `nav_order: 20+` (group Extras together).
- Facilitator pages: either `nav_exclude: true` (hidden, linked from Facilitator Hub) **or** placed under a
  `Facilitator Hub` parent — keep consistent with the existing `facilitator-hub.md` pattern.
- Update `docs/activities/index.md` table to show **Two Tiers + Two Paths** (replace the old 7-row
  linear table) and embed the same ASCII/Mermaid two-path diagram used in PLAN-V2 §1.5.

---

## 5. Prompt Flow Removal Checklist (verify nothing remains)

Owner: Livingston (execute) + Basher (verify). Honors the binding directive in `.squad/decisions.md`.

- [ ] **Delete** `activities/activity-03-prompt-flow/` (`git rm -r`).
- [ ] **Delete** `docs/activities/activity-03.md` and `activity-03-facilitator.md`.
- [ ] **`requirements.txt`:** remove `promptflow`, `promptflow-tools` (and any `promptflow-*` extras).
      Add `azure-ai-agents`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`;
      `agent-framework` (extras), `azure-ai-voicelive` (Extra B). Pin to FWH's tested set.
- [ ] **Devcontainer** (`.devcontainer/devcontainer.json`): remove the `ms-toolsai.promptflow` VS Code
      extension; ensure `azd`, `az`, Node/npx, Docker present.
- [ ] **Docs nav:** remove Prompt Flow from `docs/activities/index.md`, any sidebar/`_config.yml` refs,
      Getting Started, and FAQ.
- [ ] **Grep sweep** (must return zero hits in shipped content):
      ```bash
      grep -ri "prompt[ -]*flow\|promptflow\|pf flow\|\.flow\.dag" \
        --include="*.md" --include="*.txt" --include="*.json" --include="*.yml" \
        activities/ docs/ resources/ requirements.txt .devcontainer/ || echo "CLEAN"
      ```
- [ ] **Record** the removal as a completed decision entry in `.squad/decisions/`.

---

## 6. Per-Owner Task List

### Danny (Lead & Content Architect)
- [x] Lock the two-tier + bootstrap model in [PLAN-V2.md](PLAN-V2.md) and author this spec.
- [ ] Co-own the folder restructure PR (the `git mv` map in §2.1) with Livingston.
- [ ] Author **Advanced: Tracing & Observability** and co-author **Deploy as Hosted Agent**.
- [ ] Review every unit for STEP-template conformance before merge.

### Rusty (Curriculum Designer)
- [ ] Author `activities/foundations/README.md` as **Steps 1–4** (harvest v1 Ch00/01/02/04 content),
      each step in the §3 STEP template; end-state = grounded IQ Assistant.
- [ ] Author `activities/foundations/solution.md` (facilitator, all 4 steps).
- [ ] Author **Advanced: Action Tools** README + solution (wire the provided backend; do not build it).
- [ ] Co-author **Advanced: Evaluation + Red Teaming** content with Basher.
- [ ] Re-frame harvested RAG content to **Index + Foundry IQ** (strip all Prompt Flow framing).

### Livingston (DevOps & GitHub Engineer)
- [ ] Execute the `git mv` / `git rm` restructure (§2.1) — single, reviewable PR.
- [ ] `azd up` + Bicep infra (Foundry + AI Search + App Insights + ACR) with auto-`.env` + Bash fallback.
- [ ] Build the **bootstrap skip-path**: `scripts/setup-foundations.sh` + `scripts/validate-foundations.py`
      (materialize + verify the Foundations end-state — the single Path-B checkpoint).
- [ ] Ship the **Action Tools backend API + MCP server** in-repo.
- [ ] Execute the Prompt Flow removal checklist (§5); wire the Copilot enablement layer.

### Linus (Frontend Dev / Docs)
- [ ] Restructure `docs/activities/` to the §4 layout (foundations page + per-Advanced/Extra pages +
      facilitator siblings); apply old→new page map (§4.1) and nav frontmatter (§4.2).
- [ ] Rewrite `docs/activities/index.md` to **Two Tiers + Two Paths** with the diagram from PLAN-V2 §1.5.
- [ ] Build **Extra E (UI)** content/page; keep the Jekyll site building (verify Pages workflow).

### Basher (DevRel / Facilitator / QA)
- [ ] Author **Advanced: Evaluation + Red Teaming** dataset + `evaluate.py` (with Rusty); expand the
      Northfield eval set beyond tiny samples.
- [ ] Author/verify each facilitator `solution.md`; ensure no answer leakage into student `README.md`.
- [ ] Implement/verify per-step & per-activity **`validate.py`** Checkpoints.
- [ ] Run the Prompt Flow removal **grep sweep** (§5) and sign off "CLEAN".
- [ ] QA every unit against the STEP template (Goal/Tasks/Success/Checkpoint all present).

---

## 7. Definition of Done (restructure)

- [ ] `activities/` matches §1 exactly; old→new map (§2) fully executed; Prompt Flow folder gone.
- [ ] `docs/activities/` mirrors `activities/` 1:1 (§4); Jekyll site builds; nav shows Two Tiers.
- [ ] Every `README.md` step uses the §3 STEP template; every Checkpoint is runnable or portal-verifiable.
- [ ] Bootstrap skip-path passes `validate-foundations.py` green from a clean environment.
- [ ] Prompt Flow grep sweep returns **CLEAN**; `requirements.txt`/devcontainer updated.
- [ ] Decision summary recorded in `.squad/decisions/`.
</content>
</invoke>
