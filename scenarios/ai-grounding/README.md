# Customer Delivery: AI Grounding / IQ

Start with the work decision, not a retrieval pattern. This workshop helps a customer choose trusted knowledge and operational context for a bounded outcome.

## Customer conversation

1. Name the user decision or task to improve.
2. Draw the access boundary: people, groups, locations, sensitivity, and systems of record.
3. Choose the context pattern:
   - **SharePoint + Copilot Studio** when the experience is a governed business workflow and the source is already SharePoint/Microsoft 365.
   - **Foundry IQ** when an application or agent needs governed, composable grounding across approved sources.
   - **Fabric IQ** when the decision depends on governed data/analytics context.
   - **Work IQ** when work signals, people context, and Microsoft 365 work context are central.
   - **Web IQ** when a curated, attributable public-web corpus is required.
4. Define the proof: a golden dataset, evaluation measures, and operating evidence.

“RAG” may describe an implementation technique; it is not the starting point for this customer conversation.

## Workshop outputs

- One outcome statement and non-goals
- An access-boundary sketch with source owners
- A context-pattern decision and alternatives rejected
- A first golden dataset with acceptance criteria
- An operating-evidence plan and review owner

## Package map

- `slides.md` — 10-slide, versioned workshop conversation
- `lessons/` — five timed facilitator modules
- `FACILITATOR.md` — workshop agenda, facilitation moves, and pilot gate
- `accelerator/` — resource-free Bicep blueprint, fictional corpus, local-only demo, validator, and evidence artifact

## Guardrails

- Do not copy customer documents into this package.
- Make Copilot Studio and SharePoint decisions before designing a custom agent.
- Verify current Foundry, Fabric, Work IQ, Web IQ, Copilot Studio, and SharePoint capabilities in Microsoft documentation before implementation.
- Use the least-privileged source connection and preserve source-level permissions where supported.
- The local corpus simulation is a transparent training fixture, not a product integration or authorization control.
