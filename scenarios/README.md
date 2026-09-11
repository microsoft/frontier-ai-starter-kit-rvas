# Scenario contribution contract

A scenario is a playbook for co-building a customer's AI use case. It breaks down architectural
decisions and guides implementation with reusable building blocks. Lessons include observable
checks, and source-controlled slides support customer discussions.

The initial tracks cover grounding, document workflows, and avatar experiences. They are starting
points for customer-specific work. Add new tracks when the existing patterns do not fit.

**State what the playbook implements and what the customer team must add.** An accelerator supplies
sample assets and code, with optional demo deployment templates. It is not a complete customer
solution or production approval.

Customers may combine parts from several tracks. Help delivery teams decompose the use case and
map each part to relevant sessions. Identify reusable lessons and prerequisites, and make uncovered
work explicit.

## Required files

```text
scenarios/<folder-name>/
  manifest.json
  README.md
  slides.md
  lessons/
  accelerator/
    README.md
    main.bicep
    parameters.example.json
    sample-data/
```

`manifest.json` is authoritative for public IDs and non-standard guide paths. It must include:

```json
{
  "id": "kebab-case-id",
  "name": "Customer-facing scenario name",
  "tagline": "One outcome-focused sentence",
  "order": 1,
  "customer_outcome": "What becomes faster, safer, cheaper, or more reliable",
  "maturity": "initial",
  "level": "guided",
  "duration_minutes": 420,
  "stage": "customer-build",
  "owner": "Named team or role",
  "decision_prompts": ["Question to ask with the customer"],
  "lessons": [
    {
      "id": "lesson-id",
      "title": "Customer decision",
      "path": "lessons/lesson-id.md",
      "reused_with": ["other-scenario-id"]
    }
  ],
  "build_modules": [
    {
      "id": "lesson-id",
      "title": "Customer decision",
      "summary": "What the team implements in this lesson",
      "outcome": "The result the team can check",
      "implementation_paths": ["accelerator/main.bicep"]
    }
  ],
  "slides": "slides.md",
  "accelerator": "accelerator/README.md"
}
```

The scenario header displays these labels:

- `level`: customer-facing build level such as `guided`, `intermediate`, or `advanced`.
- `duration_minutes`: expected guided time for the scenario path, excluding customer-specific
  integration work and production acceptance.
- `stage`: customer-facing stage/type such as `ideate`, `define`, `build`, `prove`, `pilot`, or
  `customer-build`.
- `order`: integer that fixes the scenario's position in the menu, homepage, and every generated
  listing. Scenarios without an `order` sort last, alphabetically by name.

Build modules may also store optional `level`, `duration_minutes`, and `stage` values for individual
lessons. The current lesson page does not display these labels.

**Include one build module per lesson, in the same order and with the same ID.** Each module declares
an `outcome`: one short line naming what the reader should have when the module is done. The scenario
roadmap displays it alongside the module summary.

## Acceptance checklist

- The scenario starts from a customer outcome, not a product.
- The playbook states its implementation scope and identifies customer-specific work. It does not
  promise production readiness from lesson completion or a fixed engagement duration.
- The playbook helps teams map parts of a customer use case to its lessons, including references to
  other tracks where useful. A partial match must not imply coverage of the whole use case.
- Every lesson names the decision, inputs, proof, and next decision.
- Every scenario names the decision gates that determine which reference-library mechanics are
  needed. Do not revive legacy application paths; extract only the source, access, action, trust,
  operating, and deployment decisions that help the customer choose what to build next.
- Every lesson follows the practical build-module contract: visible inputs, implementation steps,
  expected evidence, an observable Verify step, and the next customer decision.
- Every lesson's **Verify** section is observable against the reader's own resources: a real command,
  a portal pane, a returned artifact, or a service response, plus what a specific failure means. Do
  not add scripts whose only job is to assert that files in this repo are well-formed, and never
  print a success banner for work that was not actually done.
- Every lesson considers Excalidraw diagrams. Include one or more when a diagram conveys important
  visual information the learner should understand or retain; include zero when a diagram would be
  decorative or redundant.
- Diagrams must pass `npm run validate:diagrams`. Arrows that visibly connect two shapes should
  stop outside each shape, use a small gap (2px is the house default), and avoid crossing through
  unrelated boxes or ellipses. Clean straight-line diagrams may retain unbound arrows, but arrows
  must not pierce a shape, point at nothing, overlap unrelated boxes, or leave text clipped.
- Slides can be used with a customer without exposing internal implementation detail. Use one
  scenario deck with lesson sections, not separate lesson decks.
- Slides use Marp-compatible Markdown. Open the full deck through `docs/slides.html?id=<scenario-id>`
  and use the browser's **Print / save as PDF** action for a customer-deck export.
- Each lesson section has three customer-facing slides: why the decision matters, options/trade-offs
  to discuss, and the evidence the practical activity must produce. Add stable slide markers before
  those slides so lesson pages can link directly into the deck:
  `<!-- slide:id=lesson-<lesson-id>-context -->`,
  `<!-- slide:id=lesson-<lesson-id>-choices -->`, and
  `<!-- slide:id=lesson-<lesson-id>-evidence -->`.
- The accelerator has a minimal safe-demo path and a bring-your-own-environment path.
- The accelerator guide distinguishes local exercises from live-service work and states whether
  its templates create demo resources. Never describe a live-service path as offline or resource-free.
- No accelerator provisions an enterprise landing zone.
- Preview and fast-moving services instruct the reader to search current Microsoft documentation
  and MCP tools before writing SDK code.
- Data ownership, access, evaluation, and operating evidence are explicit from the first lesson.
- Synthetic sample data and expected outputs are present for every scenario; each is clearly
  replaceable by approved customer data.
- A named owner and maturity label are present; describe material changes in the pull request.
