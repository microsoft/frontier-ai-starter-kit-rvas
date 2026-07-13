---
title: "Prove It's Safe"
parent: Customer Build Track
nav_order: 30
description: Turn your success measures and safety boundaries into evals, red-team tests, and a release gate.
---

# Customer Build · Prove it's safe

> **Command context:** Run commands from the repository root unless a linked reference step explicitly says otherwise.

{% include journey-status.html tone="customer" path="Customer Build Track &rarr; Prove" artifact="A scenario-specific scorecard with quality rows, adversarial prompts, and a gate tied to YOUR safety boundaries." next="Once you can measure quality and safety, move to See inside it." %}

This chapter is mutuated from [Advanced · Evaluation & Red Teaming](../activities/advanced-evaluation-redteam) — same evaluation workflow, same checkpoints — but the questions, ground truth, attack prompts, and pass/fail gate come from *your* scenario in [Define your outcome](../customer-outcome).

> Before you start this chapter: have at least one grounded answer from [Ground your app](foundations), and include your actions if they are in your demo path.

---

## Step 1 — Build your quality dataset

**Why it matters for your app:** an eval set turns “it sounded good” into row-level evidence against your own success measures.

**Does this apply to you?**
- Build it if your assistant answers questions, summarizes, recommends, routes, or decides.
- Adapt it if your demo is action-heavy — evaluate the decision to call/deny/escalate, not only final prose.
- Skip it only for a throwaway UI mock with no agent behavior being claimed.

**Decisions to make:**
- Which *top user tasks* become eval rows?
- What is the trusted answer or expected behavior for each row?
- Which rows should abstain because the corpus is silent or the request crosses a safety boundary?
- What topics must be represented so the dataset is not a tiny happy path?

**Apply it to your app:** use the Northfield JSONL shape, but replace it with your scenario rows and ground truth. → [Evaluation — Step 1](../activities/advanced-evaluation-redteam#step-1--run-quality-metrics-in-the-portal)

**Prove you applied it:**
- `python activities/advanced-evaluation-redteam/validate.py --track customer --step 1 --dataset <your-eval.jsonl>`
- Checklist:
  - [ ] ≥25 scenario rows or a justified smaller pilot set
  - [ ] ≥5 topics/tasks
  - [ ] abstain/out-of-scope rows included
  - [ ] ground truth comes from trusted sources, not model output.

**Stuck?** [Northfield Step 1](../activities/advanced-evaluation-redteam#step-1--run-quality-metrics-in-the-portal).

---

## Step 2 — Run the evaluation from code

**Why it matters for your app:** code-driven evals are repeatable. They let you compare prompt, model, corpus, and tool changes without relying on memory.

**Does this apply to you?**
- Build it if you plan to change prompts, data, tools, or models during the session.
- Adapt it if live judging is too costly — run dry-run/custom-only first, then sample the expensive metrics.
- Skip it only if your prototype will be judged manually and you clearly label that limitation.

**Decisions to make:**
- Which model acts as judge?
- Which metric matters most for your outcome: groundedness, relevance, coherence, fluency, task success, refusal quality?
- What row-level failures would block the demo?

**Apply it to your app:** run the harness against your dataset and agent; use dry-run/custom-only before spending quota. → [Evaluation — Step 2](../activities/advanced-evaluation-redteam#step-2--drive-evaluation-from-code-with-evaluatepy)

**Prove you applied it:**
- `python activities/advanced-evaluation-redteam/validate.py --track customer --step 2 --dataset <your-eval.jsonl>`
- Checklist:
  - [ ] aggregate scores are recorded
  - [ ] weakest rows are reviewed manually
  - [ ] failures map to one fix: prompt, corpus, retrieval, tool, or refusal.

**Stuck?** [Northfield Step 2](../activities/advanced-evaluation-redteam#step-2--drive-evaluation-from-code-with-evaluatepy).

---

## Step 3 — Add a domain evaluator

**Why it matters for your app:** generic metrics miss domain rules: exact thresholds, contact channels, allowed commitments, escalation triggers, and “must not answer” cases.

**Does this apply to you?**
- Build it if your safety boundaries include domain-specific correctness.
- Adapt it if you only have one rule — encode that one rule and say what is still manual.
- Skip it only when generic metrics fully cover the demo claim.

**Decisions to make:**
- What one domain rule can be scored locally without an LLM judge?
- What should be rewarded: correct citation, exact policy value, right office, valid next step, proper abstention?
- What should be penalized: fabricated contact, forbidden advice, uncited commitment, unsafe tool call?

**Apply it to your app:** adapt the custom evaluator pattern from Northfield to your domain signal. → [Evaluation — Step 3](../activities/advanced-evaluation-redteam#step-3--build-a-custom-domain-evaluator)

**Prove you applied it:**
- `python activities/advanced-evaluation-redteam/validate.py --track customer --step 3`
- Checklist:
  - [ ] evaluator name/rules match your domain
  - [ ] one good and one bad answer score differently
  - [ ] rule is explainable to a stakeholder.

**Stuck?** [Northfield Step 3](../activities/advanced-evaluation-redteam#step-3--build-a-custom-domain-evaluator).

---

## Step 4 — Red-team your boundaries

**Why it matters for your app:** the dangerous failures are usually boundary failures: prompt injection, unsafe requests, private data, overreach, or tool misuse.

**Does this apply to you?**
- Build it if the agent sees user input, retrieved content, or action tools.
- Adapt it if your risk is narrow — focus attacks on that one boundary.
- Skip it only for a non-interactive demo with no safety claim; document that it was not red-teamed.

**Decisions to make:**
- Which *safety boundaries* become attack categories?
- What prompt-injection case hides instructions inside retrieved content?
- What action request should be refused, escalated, or require approval?
- What mitigation will you add after the first failure?

**Apply it to your app:** replace the Northfield adversarial seed with attacks against your corpus, users, and tools. → [Evaluation — Step 4](../activities/advanced-evaluation-redteam#step-4--red-team-the-agent-adversarial-safety)

**Prove you applied it:**
- `python activities/advanced-evaluation-redteam/validate.py --track customer --step 4 --adversarial <your-adversarial.jsonl>`
- Checklist:
  - [ ] ≥3 attack categories tested
  - [ ] prompt-injection-via-document included
  - [ ] actual vs. expected behavior recorded
  - [ ] one mitigation applied and re-tested.

**Stuck?** [Northfield Step 4](../activities/advanced-evaluation-redteam#step-4--red-team-the-agent-adversarial-safety).

---

## Step 5 — Gate the build (chapter end-state)

**Why it matters for your app:** a gate makes your scorecard operational: if the prototype regresses, it should fail before the demo or pilot.

**Does this apply to you?**
- Build it if you will keep iterating after this chapter.
- Adapt it if the gate is manual today — write the threshold and owner anyway.
- Skip it only for a one-time concept demo; keep the scorecard as a known limitation.

**Decisions to make:**
- What threshold blocks release?
- Which metrics are gating vs. advisory?
- What manual review is required for sensitive rows?
- What known risks remain in the pilot backlog?

**Apply it to your app:** set a threshold, intentionally break one prompt or row to see the gate fail, then restore it. → [Evaluation — Step 5](../activities/advanced-evaluation-redteam#step-5--gate-the-build-ci-concept)

**Prove you applied it:**
- `python activities/advanced-evaluation-redteam/validate.py --track customer --all --dataset <your-eval.jsonl> --adversarial <your-adversarial.jsonl>`
- Checklist:
  - [ ] passing threshold recorded
  - [ ] intentional regression fails
  - [ ] scorecard is ready for the 2-minute demo
  - [ ] risks/backlog are documented.

**Stuck?** [Northfield Step 5](../activities/advanced-evaluation-redteam#step-5--gate-the-build-ci-concept).

---

## Chapter end-state

You have a scenario-specific trust scorecard: quality rows, red-team attacks, a domain evaluator, and a gate tied to your safety boundaries.

```bash
python activities/advanced-evaluation-redteam/validate.py --track customer --all --dataset <your-eval.jsonl> --adversarial <your-adversarial.jsonl>
```

Next: [See inside it](advanced-tracing-observability).
