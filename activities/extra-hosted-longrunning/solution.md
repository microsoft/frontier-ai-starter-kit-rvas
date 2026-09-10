# Implementation notes — Hosted long-running agents

This extension starts after [Deploy as a Hosted Agent](../advanced-deploy-hosted-agent/README.md).
Reuse its container, managed identity, remote endpoint, and platform observability configuration.
Do not create a second deployment path here.

Use `background=True` only for work that needs to outlive the caller. Persist the platform response
handle, then retrieve it later from a fresh process. In-memory state is not a durable handoff.

Worker tools must use authenticated remote URLs. `localhost` points at the container, not the
developer machine.

For the evidence contract, use [Tracing & Observability](../advanced-tracing-observability/README.md):
correlate the response handle to the App Insights spans and inspect duration. A complete demo shows
an immediate submission, a later retrieval, and the correlated trace.
