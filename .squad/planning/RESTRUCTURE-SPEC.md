# RESTRUCTURE SPEC — Two-Tier Curriculum (Foundations + Advanced)

> **Build spec for the team.** Authored by Danny (Lead & Content Architect), 2026-06-01.
> Source of truth for the locked structure in [PLAN-V2.md](PLAN-V2.md). Rusty (content),
> Livingston (DevOps), Linus (frontend/docs), and Basher (QA/coach) build against this.
>
> **Locked model:** Tier 1 **Foundations** = ONE guided, linear challenge with 4 ordered STEPS
> (everyone does it). Tier 2 **Advanced** = modular, self-contained challenges, any order, all
> assuming the Foundations end-state. A **bootstrap skip-path** materializes the Foundations
> end-state in ~10–15 min with a single checkpoint. **Prompt Flow is removed everywhere.**

---

## 1. New `challenges/` Folder Layout

One folder per unit. Each folder contains exactly two authored files plus an optional `validate.py`:

- `README.md` — **student-facing** (the challenge/steps).
- `solution.md` — **coach-facing** (facilitation, pitfalls, answers — never leaked to students).
- `validate.py` — **optional but recommended** — implements the Checkpoints (see §3).
- `assets/` — optional, per-unit images/snippets/datasets.

```text
challenges/
  foundations/                         # TIER 1 — single guided challenge, Steps 1–4
    README.md                          #   stepped: Step 1→2→3→4, each with a Checkpoint
    solution.md                        #   coach guide for all 4 steps
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

- Tier 1: the single folder is **`foundations/`** (no number prefix — it is one challenge with steps).
- Advanced challenges: prefix **`advanced-`** + kebab slug.
- Extras: prefix **`extra-`** + kebab slug.
- No numeric ordering prefixes on Advanced/Extra folders — they are **pickable in any order**, and a
  number would imply a sequence that does not exist.

---

## 2. Old → New Folder Map (with `git mv` guidance)

The physical repo today holds the **v1** folders (`challenge-00-setup` … `challenge-06-deploy`).
Below maps each to the new layout. **Preserve git history** with `git mv` where a folder is renamed;
**harvest-then-remove** where v1 content is folded into the stepped Foundations README; **delete** the
Prompt Flow folder outright.

| OLD folder (v1) | Action | NEW destination | Notes |
|---|---|---|---|
| `challenge-00-setup/` | `git mv` (seed) | `challenges/foundations/` | Becomes the seed of the stepped challenge; Rusty rewrites `README.md` into Step 1 + adds Steps 2–4 |
| `challenge-01-first-model/` | **harvest → remove** | folded into `foundations/` **Step 2** | Reuse model-deploy/Playground content as Step 2; then `git rm -r` after harvest |
| `challenge-02-prompt-engineering/` | **harvest → remove** | folded into `foundations/` **Step 2–3** | System-instruction content → Step 2; agent persona/guardrails → Step 3; then `git rm -r` |
| `challenge-03-prompt-flow/` | **DELETE** | — | **Prompt Flow is cut.** `git rm -r challenges/challenge-03-prompt-flow` — do **not** migrate |
| `challenge-04-rag/` | **harvest → remove** | folded into `foundations/` **Step 4** | RAG content reframed as Index + Foundry IQ knowledge base (no Prompt Flow nodes); then `git rm -r` |
| `challenge-05-evaluation/` | `git mv` | `challenges/advanced-evaluation-redteam/` | Rename; expand with red-teaming + `evaluate.py` |
| `challenge-06-deploy/` | `git mv` | `challenges/advanced-deploy-hosted-agent/` | Rename; re-target from flow-deploy to hosted-agent (`azd ai agent`) |
| *(none — new content)* | **create** | `challenges/advanced-action-tools/` | New: MCP action tool + provided backend |
| *(none — new content)* | **create** | `challenges/advanced-tracing-observability/` | New: OTel GenAI → App Insights → KQL |
| *(none — new content)* | **create** | `challenges/extra-fabric-iq/` | New |
| *(none — new content)* | **create** | `challenges/extra-voice-live/` | New |
| *(none — new content)* | **create** | `challenges/extra-magentic-workflows/` | New |
| *(none — new content)* | **create** | `challenges/extra-hosted-longrunning/` | New |
| *(none — new content)* | **create** | `challenges/extra-build-ui/` | New |
| *(none — new content)* | **create** | `challenges/extra-copilot-assisted/` | New |

### 2.1 Concrete `git mv` / `git rm` sequence (Livingston runs once)

```bash
cd /home/marco/ai-hackathon

# 1. Seed Foundations from the setup challenge (preserves history)
git mv challenges/challenge-00-setup challenges/foundations

# 2. Rename the two Advanced challenges that have v1 ancestors
git mv challenges/challenge-05-evaluation  challenges/advanced-evaluation-redteam
git mv challenges/challenge-06-deploy      challenges/advanced-deploy-hosted-agent

# 3. DELETE Prompt Flow (cut — no migration)
git rm -r challenges/challenge-03-prompt-flow

# 4. Harvest content from these into foundations/README.md (Steps 2–4) BEFORE removing.
#    Do the content move in a PR with Rusty, then remove the now-empty v1 folders:
git rm -r challenges/challenge-01-first-model
git rm -r challenges/challenge-02-prompt-engineering
git rm -r challenges/challenge-04-rag

# 5. Create the net-new Advanced + Extra folders (empty README/solution scaffolds)
mkdir -p challenges/advanced-action-tools \
         challenges/advanced-tracing-observability \
         challenges/extra-fabric-iq \
         challenges/extra-voice-live \
         challenges/extra-magentic-workflows \
         challenges/extra-hosted-longrunning \
         challenges/extra-build-ui \
         challenges/extra-copilot-assisted
```

> **Harvest-before-remove discipline:** Steps 4/3/2 of `foundations/README.md` reuse text from the
> v1 `challenge-04-rag`, `challenge-02-prompt-engineering`, and `challenge-01-first-model` READMEs.
> Do the copy in the same PR that `git rm`s them so no content is lost. Coach `solution.md` files
> from those v1 folders are harvested into `foundations/solution.md`.

---

## 3. Standard STEP Template (copy-paste skeleton)

Every **Foundations step** and every **Advanced/Extra challenge step** MUST use this exact four-part
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
> _Coach note (solution.md only): <facilitation tip, common pitfall, the actual answer/snippet>._
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
- Coach answers live **only** in `solution.md` (or in `> _Coach note_` blocks that are stripped from the
  student build) — never inline in the student `README.md`.

### 3.2 Advanced/Extra README header banner (paste at top of each)

```markdown
> **Tier 2 · Advanced — modular.** You can attempt this in any order with the other Advanced
> challenges. **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ
> Assistant). Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
```

---

## 4. New `docs/challenges/` Page Layout (Jekyll, mirror 1:1)

Linus updates the `just-the-docs` site so the discovery layer mirrors the folder layout. Foundations is
**one parent page with four step sub-pages (or one long page with anchors)**; each Advanced/Extra is one
page + a coach sibling.

```text
docs/challenges/
  index.md                              # nav landing — Two-Tier overview + Two Paths (A/B) + diagram
  foundations.md                        # Tier 1 page — Steps 1–4 (single page, anchored) ; nav_order 1
  foundations-coach.md                  # coach companion for Foundations

  advanced-action-tools.md              # Tier 2 — one page per Advanced challenge
  advanced-action-tools-coach.md
  advanced-evaluation-redteam.md
  advanced-evaluation-redteam-coach.md
  advanced-tracing-observability.md
  advanced-tracing-observability-coach.md
  advanced-deploy-hosted-agent.md
  advanced-deploy-hosted-agent-coach.md

  extra-fabric-iq.md                    # Tier 2 — Extras
  extra-fabric-iq-coach.md
  extra-voice-live.md
  extra-voice-live-coach.md
  extra-magentic-workflows.md
  extra-magentic-workflows-coach.md
  extra-hosted-longrunning.md
  extra-hosted-longrunning-coach.md
  extra-build-ui.md
  extra-build-ui-coach.md
  extra-copilot-assisted.md
  extra-copilot-assisted-coach.md
```

### 4.1 Old → New docs page map

| OLD page | Action | NEW page |
|---|---|---|
| `challenge-00.md` / `-coach.md` | merge → | `foundations.md` (Step 1 section) / `foundations-coach.md` |
| `challenge-01.md` / `-coach.md` | merge → | `foundations.md` (Step 2 section) / `foundations-coach.md` |
| `challenge-02.md` / `-coach.md` | merge → | `foundations.md` (Step 3 section) / `foundations-coach.md` |
| `challenge-03.md` / `-coach.md` | **DELETE** (Prompt Flow) | — |
| `challenge-04.md` / `-coach.md` | merge → | `foundations.md` (Step 4 section) / `foundations-coach.md` |
| `challenge-05.md` / `-coach.md` | rename → | `advanced-evaluation-redteam.md` / `-coach.md` |
| `challenge-06.md` / `-coach.md` | rename → | `advanced-deploy-hosted-agent.md` / `-coach.md` |
| *(new)* | create → | `advanced-action-tools.md` / `-coach.md` |
| *(new)* | create → | `advanced-tracing-observability.md` / `-coach.md` |
| *(new)* | create → | all `extra-*.md` / `-coach.md` |

### 4.2 Jekyll nav frontmatter

- `foundations.md`: `parent: Challenges`, `nav_order: 1`, `has_children: false` (single anchored page).
  Add a "Tier 1 · Foundations" kicker. Step headings use `## Step 1 …` anchors for the sidebar TOC.
- Each Advanced page: `parent: Challenges`, `nav_order: 10,11,12,13` (group Advanced together).
- Each Extra page: `parent: Challenges`, `nav_order: 20+` (group Extras together).
- Coach pages: either `nav_exclude: true` (hidden, linked from Coach Hub) **or** placed under a
  `Coach Hub` parent — keep consistent with the existing `coach-hub.md` pattern.
- Update `docs/challenges/index.md` table to show **Two Tiers + Two Paths** (replace the old 7-row
  linear table) and embed the same ASCII/Mermaid two-path diagram used in PLAN-V2 §1.5.

---

## 5. Prompt Flow Removal Checklist (verify nothing remains)

Owner: Livingston (execute) + Basher (verify). Honors the binding directive in `.squad/decisions.md`.

- [ ] **Delete** `challenges/challenge-03-prompt-flow/` (`git rm -r`).
- [ ] **Delete** `docs/challenges/challenge-03.md` and `challenge-03-coach.md`.
- [ ] **`requirements.txt`:** remove `promptflow`, `promptflow-tools` (and any `promptflow-*` extras).
      Add `azure-ai-agents`, `azure-monitor-opentelemetry`, `azure-core-tracing-opentelemetry`;
      `agent-framework` (extras), `azure-ai-voicelive` (Extra B). Pin to FWH's tested set.
- [ ] **Devcontainer** (`.devcontainer/devcontainer.json`): remove the `ms-toolsai.promptflow` VS Code
      extension; ensure `azd`, `az`, Node/npx, Docker present.
- [ ] **Docs nav:** remove Prompt Flow from `docs/challenges/index.md`, any sidebar/`_config.yml` refs,
      Getting Started, and FAQ.
- [ ] **Grep sweep** (must return zero hits in shipped content):
      ```bash
      grep -ri "prompt[ -]*flow\|promptflow\|pf flow\|\.flow\.dag" \
        --include="*.md" --include="*.txt" --include="*.json" --include="*.yml" \
        challenges/ docs/ resources/ requirements.txt .devcontainer/ || echo "CLEAN"
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
- [ ] Author `challenges/foundations/README.md` as **Steps 1–4** (harvest v1 Ch00/01/02/04 content),
      each step in the §3 STEP template; end-state = grounded IQ Assistant.
- [ ] Author `challenges/foundations/solution.md` (coach, all 4 steps).
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
- [ ] Restructure `docs/challenges/` to the §4 layout (foundations page + per-Advanced/Extra pages +
      coach siblings); apply old→new page map (§4.1) and nav frontmatter (§4.2).
- [ ] Rewrite `docs/challenges/index.md` to **Two Tiers + Two Paths** with the diagram from PLAN-V2 §1.5.
- [ ] Build **Extra E (UI)** content/page; keep the Jekyll site building (verify Pages workflow).

### Basher (DevRel / Coach / QA)
- [ ] Author **Advanced: Evaluation + Red Teaming** dataset + `evaluate.py` (with Rusty); expand the
      Northfield eval set beyond tiny samples.
- [ ] Author/verify each coach `solution.md`; ensure no answer leakage into student `README.md`.
- [ ] Implement/verify per-step & per-challenge **`validate.py`** Checkpoints.
- [ ] Run the Prompt Flow removal **grep sweep** (§5) and sign off "CLEAN".
- [ ] QA every unit against the STEP template (Goal/Tasks/Success/Checkpoint all present).

---

## 7. Definition of Done (restructure)

- [ ] `challenges/` matches §1 exactly; old→new map (§2) fully executed; Prompt Flow folder gone.
- [ ] `docs/challenges/` mirrors `challenges/` 1:1 (§4); Jekyll site builds; nav shows Two Tiers.
- [ ] Every `README.md` step uses the §3 STEP template; every Checkpoint is runnable or portal-verifiable.
- [ ] Bootstrap skip-path passes `validate-foundations.py` green from a clean environment.
- [ ] Prompt Flow grep sweep returns **CLEAN**; `requirements.txt`/devcontainer updated.
- [ ] Decision summary recorded in `.squad/decisions/`.
</content>
</invoke>
