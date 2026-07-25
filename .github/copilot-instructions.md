# GitHub Copilot — Workspace Instructions

## The golden rule: Search Before Implement

Before writing **any** Azure / Microsoft Foundry SDK code, or before describing a fast-moving
Azure / Foundry capability:

1. **Search Microsoft Learn through the `microsoft-docs` MCP server** (the MS Learn MCP server) for
   the **current** API surface, SDK syntax, and product guidance. Use `foundry-mcp` as well for
   Foundry-native operations such as model catalog, agents, toolboxes, knowledge bases, and evals.
   Foundry features here are fast-moving and many are **preview** — never rely on memorized
   signatures.
2. **Load** the matching skill from `.github/skills/` for the proven pattern.
3. **Implement** against the verified signature.
4. **Validate** with the activity's `validate.py` / checkpoint.

> **Microsoft Learn MCP = current facts. Skills = proven patterns.** Use both, in that order.

## Scenario and writing philosophy

- Lead with clarity and simplicity. Use correct technical terms where they help, then explain them
  in plain language so customers can follow and act.
- Avoid product-first jargon, over-specific architecture labels, and unnecessary complexity. Start
  from the customer outcome, the decision they need to make, and the evidence they need to trust it.
- Treat each scenario track as a starter kit for an AI scenario. A customer should be able to pick a
  track, run the guided path, and adapt the result to their environment.
- Do not bake a complete solution for the customer. Provide reusable building blocks, safe defaults,
  validation, and clear seams so teams can compose their own outcome.
- For each lesson, consider whether one or more beautiful Excalidraw diagrams would make an
  important concept easier to understand or remember. Include diagrams when they add visual
  information that text alone does not carry; use zero diagrams when they would be decorative or
  redundant.
- Assume more scenario tracks will be added. Keep language, folders, validators, and lesson patterns
  reusable across tracks instead of hard-coding one journey.
- In content, do not add "Verified on <date>" or "Tested on <date>" statements. The content is
  expected to be evergreen and continuously updated.
