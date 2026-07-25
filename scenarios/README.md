# Scenario contribution contract

A scenario is a customer-delivery playbook, not a technology tutorial. It contains a client
conversation, reusable lessons, source-controlled slides, and a deliberately small accelerator.

## Required files

```text
scenarios/<folder-name>/
  manifest.json
  README.md
  FACILITATOR.md
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
  "customer_outcome": "What becomes faster, safer, cheaper, or more reliable",
  "maturity": "initial",
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
  "slides": "slides.md",
  "accelerator": "accelerator/README.md",
  "facilitator": "FACILITATOR.md",
  "local_demo": "local-demo.md",
  "validator": "validate.py"
}
```

## Acceptance checklist

- The scenario starts from a customer outcome, not a product.
- Every lesson names the decision, inputs, proof, and next decision.
- Every scenario names the decision gates that determine which reference-library mechanics are
  needed. Do not revive legacy application paths; extract only the source, access, action, trust,
  operating, and deployment decisions that help the customer choose what to build next.
- Every lesson follows the practical build-module contract: visible inputs, implementation steps,
  expected evidence, local or service validation, and the next customer decision.
- Every lesson considers Excalidraw diagrams. Include one or more when a diagram conveys important
  visual information the learner should understand or retain; include zero when a diagram would be
  decorative or redundant.
- Slides can be used with a customer without exposing internal implementation detail.
- Slides use Marp-compatible Markdown. Open them through `docs/slides.html?id=<scenario-id>` and
  use the browser's **Print / save as PDF** action for a customer-deck export.
- The accelerator has a minimal safe-demo path and a bring-your-own-environment path.
- No accelerator provisions an enterprise landing zone.
- Preview and fast-moving services instruct the reader to search current Microsoft documentation
  and MCP tools before writing SDK code.
- Data ownership, access, evaluation, and operating evidence are explicit from the first lesson.
- Synthetic sample data, expected outputs, and a local no-credential demo are present for every
  scenario; each is clearly replaceable by approved customer data.
- A named owner and maturity label are present; update the scenario changelog when material changes.
