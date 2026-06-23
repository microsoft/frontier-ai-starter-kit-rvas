---
title: FAQ
nav_order: 7
---

# FAQ

## Do I need Azure experience?

No. This hackathon assumes curiosity, basic Python comfort, and a willingness to learn by doing. Microsoft Foundry experience is not required.

## What does a “devcontainer” mean?

A devcontainer is a prebuilt development environment that opens your project with the right tools, versions, and settings already configured. It helps everyone work in the same setup instead of spending the event debugging laptop differences.

## My Azure subscription is expired / I don't have one: what do I do?

Talk to your event organizer or coach first. Most events use Azure Pass, Azure for Students, or a pre-approved subscription path. You need working Azure access before the Foundations section can begin.

## Can I work in my own language (not Python)?

Usually yes for experimentation and integration, but the guided materials are optimized for Python-first teams. If you switch languages, expect to translate some examples on your own.

## What if I fall behind? Can I skip challenges?

Yes. The challenges are designed as a progression, but event-day reality matters. Coaches can help you decide which challenges to compress or skip while still keeping the overall learning arc intact.

## Is there a time limit?

Yes. Most events run in one day, with about 6–8 hours of challenge time. Each challenge includes an expected duration so teams can self-manage pace.

## Where do I save my work?

Save changes in your Codespace or your local clone of the repository. Commit early if your event encourages it, and keep notes on prompt decisions, evaluation results, and deployment settings.

## What happens after the hackathon?

You leave with a working project foundation, a clearer understanding of Microsoft Foundry, and a repo you can keep extending. Many teams continue by improving the app UX, expanding data sources, or productionizing deployment.

## Can we use this with a real customer scenario?

Yes. Use the [Customer Outcome Canvas]({{ '/customer-outcome' | relative_url }}) before the event to define the user, business outcome, safe knowledge sources, governed actions, eval prompts, and final demo story. If customer data is not ready, run the Northfield scenario first and use it as the reference architecture for follow-up work.

## Coach: How do I get the solution guides?

Clone the repo and open `challenges/*/solution.md`. Solution guides are intentionally kept out of the published Pages site so coaches can use them selectively.

---

## Foundry troubleshooting

### The agent answers but never cites a source

Check two things: (1) your agent instructions must explicitly ask for citations — the line "Always cite your sources as [source]" is required; the tool retrieves chunks but the model only surfaces them if instructed. (2) the index must have a retrievable `source` field set to the document name; without it there is nothing to cite.

### I got a 403 / "Unauthorized" querying the index

The Foundry project managed identity is missing RBAC roles on the AI Search resource. It needs both **Search Index Data Contributor** and **Search Service Contributor**. `azd up` assigns these automatically; if it didn't, assign them in the portal: AI Search → Access control (IAM) → Add role assignment.

### What is the difference between a Foundry resource and a Foundry project?

A **Foundry resource** is the Azure resource group–level container (formerly "hub"). A **Foundry project** lives inside it and holds your deployments, connections, agents, and knowledge bases. Think of the resource as the facility and the project as your team's workspace within it. The `.env` key `AZURE_AI_PROJECT_ENDPOINT` points to the project, not the resource.

### `python validate.py --step N` fails even though the portal shows things are working

Common causes: (1) `.env` has stale or mismatched values — re-run `azd up` or check the portal for the exact endpoint and deployment names; (2) the deployment status is still **Updating** — wait for **Succeeded/Ready**; (3) case mismatch in index or connection names — they are case-sensitive. Run `grep -E "AZURE_SEARCH_INDEX_NAME|AZURE_SEARCH_CONNECTION_NAME" .env` and compare against the portal.

### `azd up` fails with quota or region errors

Some regions lack capacity for certain model SKUs. Use the Bash fallback `./scripts/deploy.sh` and pick a region from the event's approved list when prompted. If you cannot provision in any region, ask your event organizer — most events have a pre-approved subscription path.

### Traces are not appearing in Application Insights

Two common causes: (1) the tracing environment variables were not set **before** importing the Foundry SDK — set `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` at the top of your script or in `.env`, then restart your Python process; (2) Application Insights has a 1–3 minute ingestion lag — wait a few minutes and refresh the Live Metrics or Traces view.
