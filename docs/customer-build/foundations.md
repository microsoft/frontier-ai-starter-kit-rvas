---
title: "Chapter 1 — Ground Your App"
parent: Customer Build Track
nav_order: 10
description: Provision, choose a model, create your agent, and ground it in your own data — the Customer Build companion to Foundations.
---

# Customer Build · Chapter 1 — Ground your app

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Chapter 1 &middot; Ground" artifact="A deployed agent grounded in YOUR customer-safe corpus, answering a real scenario question with a citation." next="Once your agent cites your own data, move to Chapter 2 — Make it act." %}

This chapter is **mutuated from [Foundations](../challenges/foundations)** — same objective, same
checkpoints — but every step points at *your* scenario from
[Step 0: Define your outcome](../customer-outcome). Do the decisions here; when you need the exact
commands or code, follow the Northfield reference the step links to. **The mechanics are identical;
only the corpus, persona, and questions are yours.**

> **Before you start this chapter:** complete [Step 0](../customer-outcome). You need your target
> user, business outcome, knowledge sources, and one safe scenario question written down. No idea
> yet? Run [Idea Forge](../idea-forge) first.

---

## How to read every chapter in this track

Each step follows the same shape:

- **Why it matters for your app** — the point of the capability.
- **Does this apply to you?** — a **Build / Adapt / Skip** gate so you don't force-fit Northfield's shape.
- **Decisions to make** — the real forks for *your* scenario.
- **Apply it to your app** — what to do, linking the Northfield reference for the exact steps.
- **Prove you applied it** — a generalized validator command **and** a manual checklist.
- **Stuck?** — the known-good Northfield version to fall back on.

---

## Step 1 — Provision Foundry + Search + observability

**Why it matters for your app:** every later capability (grounding, actions, evals, tracing, deploy)
assumes live Foundry, Azure AI Search, App Insights, and a keyless `.env`. This is scenario-agnostic
plumbing.

**Does this apply to you?** → **Build it.** No app skips provisioning.

**Decisions to make:**
- **Region** — pick one with quota for the model you want (check the model catalog before you commit).
- **Subscription** — one shared subscription per team so everyone points at the same resources.
- **Naming prefix** — use a scenario/customer prefix so resources are easy to find and clean up.

**Apply it to your app:** run `azd up` exactly as the reference describes — nothing is
scenario-specific yet. → [Foundations Step 1](../challenges/foundations#step-1--setup--provisioning-foundry--ai-search)

**Prove you applied it:**
- `python challenges/foundations/validate.py --step 1` — infra + keyless auth are scenario-agnostic, so the upskill check applies unchanged.
- Checklist: ☐ `.env` has your project endpoint, model deployment, and search endpoint (no `<...>` placeholders) ☐ no API keys pasted anywhere.

**Stuck?** [Northfield Step 1](../challenges/foundations#step-1--setup--provisioning-foundry--ai-search).

---

## Step 2 — Choose a model for *your* users

**Why it matters for your app:** model choice is a real trade-off (cost, latency, tone, reasoning
depth) that your users will feel. Decide it deliberately against *your* task, not a default.

**Does this apply to you?** → **Build it**, but adapt the comparison prompts.
- **Adapt it** if your domain needs a specialized model family (e.g. long-context, reasoning, or a
  regional deployment) — compare that against the default instead of the generic pair.

**Decisions to make:**
- Which two contrasting models to compare (a capable default vs. a faster/cheaper or specialized one)?
- What are *your* 3–5 representative prompts? Use real questions your target users would ask, from
  your Step 0 *Top user tasks* — **not** the Northfield samples.
- Your first-draft **system instruction**: audience, tone, how to handle missing info, what's out of scope.

**Apply it to your app:** run the Playground comparison and reproduce it in code, substituting your
prompts and instruction. → [Foundations Step 2](../challenges/foundations#step-2--model-selection--the-playground)

**Prove you applied it:**
- `python challenges/foundations/validate.py --track customer --step 2` — confirms your chosen deployment answers via the SDK.
- Checklist: ☐ you can state one concrete trade-off you observed on *your* prompts ☐ your tuned system instruction is saved ☐ the code call is on-tone for your users.

**Stuck?** [Northfield Step 2](../challenges/foundations#step-2--model-selection--the-playground).

---

## Step 3 — Give your agent a persona and guardrails

**Why it matters for your app:** a named, versioned agent is where *your* persona, scope, and refusal
behavior live. This is what makes the assistant safe and on-brand for your users, not a raw model.

**Does this apply to you?** → **Build it.** Every Customer Build scenario needs a defined persona and
guardrails.

**Decisions to make:**
- **Persona & scope** — who the assistant is, and the exact topics it does/doesn't handle for your users.
- **Refusals** — what it must decline, escalate, or redirect. Pull these straight from your Step 0
  *Safety boundaries* (e.g. no legal/medical advice, no unapproved commitments, escalate to a human for X).
- **Uncertainty behaviour** — your wording when it doesn't know, tuned to your domain's tone.

**Apply it to your app:** create the agent in the portal and in code, using *your* name and
instructions; test that your specific refusals actually hold. → [Foundations Step 3](../challenges/foundations#step-3--your-first-agent)

**Prove you applied it:**
- `python challenges/foundations/validate.py --track customer --step 3` — confirms your named agent (from `AZURE_FOUNDRY_AGENT_NAME`) exists and is versioned.
- Checklist: ☐ an in-scope question is answered well ☐ each safety boundary from Step 0 is actually refused/escalated ☐ portal and code instructions match.

**Stuck?** [Northfield Step 3](../challenges/foundations#step-3--your-first-agent).

---

## Step 4 — Ground it in *your* data (chapter end-state)

**Why it matters for your app:** grounded answers *with citations* are what make stakeholders trust
the prototype over a generic chatbot. This is the proof point that the agent answers from *your*
trusted source of truth.

**Does this apply to you?**
- **Build it** if your outcome needs answers from documents, policies, FAQs, or manuals (most apps).
- **Adapt it** if your knowledge lives in a **database or API**, not files — note it here and deliver
  that retrieval as an action in [Chapter 2 — Action Tools](advanced-action-tools) instead.
- **Skip it** only if your app is pure action with no knowledge retrieval (rare — most demos need grounding).

**Decisions to make:**
- **Which corpus** from your Step 0 *Knowledge sources*? Is it cleared and safe (no PII/unredacted
  data)? Aim for **5–20 well-structured documents** — sparse corpora produce "I don't know" answers.
- **Chunking** vs. your document structure — keep policy details (deadlines, thresholds, steps) intact.
- **Abstention wording** — what the agent says when *your* corpus lacks the answer.

**Apply it to your app:**
1. Place your cleared docs where the indexer reads them; keep a `source` field so answers can cite.
2. Follow the indexing → knowledge base → attach-tool mechanics, substituting your files and your
   grounding instruction. → [Foundations Step 4](../challenges/foundations#step-4--knowledge-base-index--foundry-iq---foundations-end-state)
3. Not `.md`/`.txt`? Search **Microsoft Docs (MCP)** for your format, or use the portal
   **Build → Indexes → Add data** flow for PDFs/SharePoint.

**Prove you applied it:**
- `python challenges/foundations/validate.py --track customer --step 4 --question "<your real scenario question>"`
  — asserts *your* agent (or index) returns a **cited** answer to a question you provide, instead of Northfield's school code.
- Checklist: ☐ a real scenario question returns a citation to *your* source ☐ an out-of-corpus question abstains in *your* wording ☐ grounded answer is more specific than the ungrounded Step 3 answer.

**Stuck?** [Northfield Step 4](../challenges/foundations#step-4--knowledge-base-index--foundry-iq---foundations-end-state).

---

## Chapter 1 end-state

You have a **deployed agent grounded in your own customer-safe data**, answering a real scenario
question with a citation and abstaining when the corpus is silent.

```bash
python challenges/foundations/validate.py --track customer --all --question "<your real scenario question>"
```

This is the prerequisite for every later chapter. Next: **[Chapter 2 — Make your agent act](advanced-action-tools)**.
