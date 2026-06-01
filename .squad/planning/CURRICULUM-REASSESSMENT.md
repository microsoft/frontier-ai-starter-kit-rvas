# Curriculum Reassessment — Advanced Tier

> **Author:** Rusty (Curriculum Designer) · **Date:** 2026-06-01 · **Requested by:** Marco Olivo
> **Purpose:** Focused, evidence-based curriculum-design memo to FEED Danny's `PLAN-V3.md`.
> Analysis only — no challenge content was edited.
> **Citations:** `[FWH]` = `microsoft/FrontierWeekHack`, `[ATA]` = `microsoft/azure-trust-agents`
> (see `.squad/research/frontierweekhack.md`, `.squad/research/azure-trust-agents.md`).

**The user's instinct is correct.** The Advanced tier *reads* as ~4.5 hr but the genuine
hands-on-keyboard **build** effort across all four challenges is closer to **1.5–2 hr**. The labelled
clock is padded by **waiting** (App Insights ingestion lag, async hosted provisioning) and
**copy-paste** (two of four challenges hand over every line of code inline). Almost nothing asks a
participant to start from a blank file. The fix is not "make it longer" — it's a **difficulty ladder**
that lets a strong team strip the scaffolding, plus a few proven pedagogy borrows we are leaving on
the table.

---

## 1. Honest time + guidance audit

Labelled times are from `PLAN-V2.md` §3.2. Step counts and code/conceptual classification are from a
literal read of each `challenges/*/README.md`. "Real-code" = the participant authors or completes
logic. "Provided-paste" = full code is printed inline to copy. "Conceptual/operational" = no code
authored (portal clicks, running a provided file, starting a server, verbal checkpoint).

| Challenge | Labelled time | # steps | Real-code vs conceptual/placeholder | Realistic **guided** time | Realistic **from-scratch** time | Guidance | Verdict |
|---|---|---|---|---|---|---|---|
| **Action Tools** | 1.25 hr | 5 (Step 0–4) | **2 real-code** (S2 attach `McpTool`, S3 approval loop) · 1 conceptual (S1, "confirmed verbally, no script") · 2 operational (S0 start backend, S4 curl-verify) | **50–65 min** | **2–2.5 hr** | **Heavy** — starter file with `< PLACEHOLDER >` gaps; backend pre-built | **Roughly honest on the clock, but over-guided.** The "build" is filling two placeholder blocks in a provided starter. Real value (the approval loop) is one of five steps. |
| **Evaluation & Red Teaming** | 1.25 hr | 5 (Step 1–5) | **1 real-code** (S3 add *one* rule to `NorthfieldDomainEvaluator`) · rest run the provided `evaluate.py`, click the portal, or write a prose findings note | **65–75 min** | **2.5–3 hr** | **Heavy** — `evaluate.py` harness, both datasets, `--gate`, `--dry-run` all pre-written | **Clock is honest** (red-team analysis + portal waits are real), **but the build is one evaluator rule.** Richest *conceptual* challenge; thinnest *authoring* challenge. |
| **Tracing & Observability** | 1 hr | 4 (Step 1–4) | **0 authored-from-blank** · `trace_setup.py` and `traced_run.py` are printed **in full** to copy-paste · S3 is portal-only · S4 KQL starters are provided (paste your `operation_Id`, tweak a price constant) | **45–55 min wall-clock, ~25 min effort** | **1.5 hr** | **Heavy** — every code block is inline and complete | **Inflated as a "build."** It is copy-two-files + **wait 1–3 min** + read the portal + paste an id into a given KQL query. The hour is mostly ingestion lag, not work. |
| **Deploy as a Hosted Agent** | 1 hr | 4 (Step 1–4) | **0 authored-from-blank** · `agent.yaml`, `main.py`, `Dockerfile`, `invoke_hosted.py` all printed in full · S2/S4 are CLI commands + portal | **60–90 min, high variance** | **2 hr+** | **Heavy on code, but genuinely hard infra** — preview `azd ai agent`, async provisioning, ACR build | **The clock is OPTIMISTIC, not inflated.** Copy-paste code, but real container build + async hosted deploy + preview tooling = the highest failure surface in the tier. Budget 90 min. |

**Tier totals.** Labelled **4.5 hr**; realistic **guided wall-clock ~3.5–4.5 hr**; genuine
**build/authoring effort ~1.5–2 hr**. The gap between "wall-clock" and "effort" is the whole problem:
participants spend the tier **pasting and waiting**, not **building**.

**Cross-repo calibration.** [FWH]'s comparable lifecycle (build → monitor → evaluate → deploy) is
labelled **~2 hr total** for 5 challenges and is *also* mostly copy-paste — so our per-challenge
clocks are not out of line with the genre. The difference: [FWH] is *honest that it's a guided lab*
and never claims otherwise. Our READMEs imply more authoring than they ask for. **Two of our four
advanced challenges have no time/difficulty banner in the participant README at all** (times live only
in `PLAN-V2.md`), so a participant can't even see the estimate they're being measured against.

---

## 2. Difficulty-ladder design (the core proposal)

Every Advanced challenge should ship **three rungs** off the same backbone, so it stops being pure
guided wiring. Rung (a) already exists; we add (b) and (c) as labelled sections, not new folders.

- **(a) Guided path** — the current placeholder/copy-paste style. Keep it verbatim for beginners.
- **(b) Build-from-scratch path** — same acceptance criteria, **scaffolding stripped**. Give only the
  **API/SDK contract** (class + method names, the env vars, the success checks) and let the team write
  the file. This is the rung the user is missing today.
- **(c) Stretch goals** — genuinely open, no single right answer. Most challenges already have a stub
  "Stretch goals" section; these become rung (c) and get expanded.

The same `validate.py` grades all three rungs — that's what makes the ladder cheap to add. **What to
strip to create rung (b), per challenge:**

| Challenge | Strip to create rung (b) | Hand them only (the contract) |
|---|---|---|
| **Action Tools** | Delete the `agent_with_actions.py` starter; remove the import line in S2 and the loop skeleton in S3 | "Attach the `northfield_actions` MCP server as a tool; implement a human-approval loop using `McpTool` / `RequiredMcpToolCall` / `SubmitToolApprovalAction` / `ToolApproval`. Acceptance: no action runs without an approve; a denial creates nothing." |
| **Evaluation & Red Teaming** | Remove the pre-written `NorthfieldDomainEvaluator` body and the `--gate` / `--dry-run` plumbing from the printed walkthrough | "Write `evaluate.py`: load the JSONL, call the agent per `query`, score Groundedness/Relevance/Coherence/Fluency with `azure-ai-evaluation`, add a custom 1–5 domain evaluator, exit non-zero below `--gate`." |
| **Tracing & Observability** | Remove the full `trace_setup.py` and `traced_run.py` listings; keep only the **gotcha** ("set the two env flags before any `azure.ai.*` import") and the env-var list | "Emit GenAI spans to App Insights and reconstruct one question end-to-end. Acceptance: model + retrieval spans for one `operation_Id`, with token + latency, surfaced in portal Tracing **and** a KQL query you wrote." |
| **Deploy as a Hosted Agent** | Remove the inline `agent.yaml` / `main.py` / `Dockerfile` / `invoke_hosted.py` listings | "Containerize the Foundations agent, serve the `responses` protocol on 8088, deploy with `azd ai agent`, invoke over the production endpoint, prove anonymous calls get 401/403. Acceptance: live grounded answer + rejected anon call." |

**Why this beats "add more steps":** it preserves the beginner on-ramp, gives strong teams a real
build, and adds **zero new validators**. It directly answers "is the tier too short/over-guided?" by
making depth *opt-in*. [ATA]'s single `< PLACEHOLDER FOR MCP TOOL >` (answer shown right below) is the
*beginner* calibration; rung (b) is the missing *upper* calibration.

---

## 3. Pick-your-scenario tree [FWH]

[FWH] ships **one 5-challenge spine across three interchangeable domains** (factory / claims /
callcenter) — identical code skeleton, identical Foundry concepts, learner picks the vertical that
resonates. We can do the same on the **Northfield spine** because our agent skeleton is already
domain-generic: *a retriever agent grounded in a KB + an action tool with an approval loop + an eval
dataset + a tracing setup.* Only the **surface** (corpus, tool names, persona, eval rows) is
Northfield-specific.

### What stays fixed (the shared backbone — never swapped)

The agent skeleton, the `McpTool` + approval-loop wiring, `trace_setup.py`, the `evaluate.py` harness
shape, every `validate.py` contract, the `azd`/Bicep infra, and the `.env` variable names. This is the
"one structure" half of [FWH]'s "one structure, three scenarios."

### What gets swapped per domain

1. **Data corpus** — `resources/sample-data/university-faq/*` → the new domain's FAQ docs.
2. **Action backend labels** — `scripts/action-backend/{app.py,mcp_server.py}` tool names + routes.
3. **Persona / system instructions** — Foundations Step 2/3 + the Deploy `agent.yaml` instructions.
4. **Eval + adversarial datasets** — `northfield-eval.jsonl` rows + `adversarial-seed.jsonl` phrasing
   (the *categories* — jailbreak / harmful / injection — stay; only the domain wording changes).

### Three proposed alternate domains (same skeleton, same 3-tool shape)

| Domain | Persona | KB corpus | 3 action tools (map 1:1 to current) | Effort to add |
|---|---|---|---|---|
| **Mercy General — patient services** (healthcare) | Patient-services coordinator | Visiting hours, billing, insurance, pre-admission FAQ | `create_care_request` · `flag_billing_hold` · `book_appointment` | **~1 day** — corpus + dataset rewrite is the bulk; backend is a label swap |
| **NorthPeak Outfitters — customer support** (retail/e-commerce) | Support specialist | Returns, shipping, warranty, sizing policy | `open_support_case` · `place_order_hold` · `schedule_callback` | **~1 day** — most relatable corpus to author; richest injection-via-review-text red-team cases |
| **City of Riverton 311 — municipal services** (gov/public sector) | 311 agent | Permits, trash/recycling, utilities, licensing FAQ | `open_311_ticket` · `place_utility_hold` · `book_inspection_slot` | **~1–1.5 day** — strongest "stakes" narrative (a missed permit hold has real consequences) |

**Tool-shape invariant:** every domain keeps the *same three verbs* — **create a ticket / place a
hold / book a slot** — so `agent_with_actions.py`, the approval loop, and `validate.py` are byte-for-byte
reusable. Only strings change.

**Recommended sequencing for Danny:** do **not** build all domains now. Ship **Northfield as the
canonical spine**, and capture the swap surface (the four bullets above) as a documented "reskin
contract." Then realize **one** alternate (NorthPeak retail — most relatable, best red-team material)
as proof the spine is portable. This mirrors [FWH] without tripling our authoring load. The natural
automation is **Extra F (Copilot-Assisted Build)** pointed at this reskin contract — effectively
[FWH]'s `lab-generator` meta-agent, which the dossier calls "the single most reusable asset" [FWH §4].

---

## 4. Pedagogy borrow-list (techniques we are NOT yet using)

Concrete, evidence-cited techniques from both repos, each with one line on how it applies here.

| # | Borrow | Source | How it applies to us |
|---|---|---|---|
| 1 | **DevUI visual-first before tracing** | [ATA §4.5] | Let teams *watch* the agent run as a node graph (green/purple/black) before the OTel rigor of the Tracing challenge — build intuition, then instrument. We jump straight to spans. |
| 2 | **"Why this order" narrative** | [FWH §4.2] | Add a 2-sentence rationale to each Advanced README tying the challenge to a real stake ("a wrongful course hold blocks registration"). Our READMEs explain *what*, rarely *why this is next*. |
| 3 | **Run-individually then run-orchestrated** | [ATA §4.11] | Have teams smoke-test each piece (`python <file>.py`) before wiring — isolates failures. Critical for the Deploy challenge's high failure surface. |
| 4 | **Per-challenge duration + difficulty banner — consistently** | [FWH §2], [ATA §4.9] | **Two of four Advanced READMEs show no time/difficulty at all** (times live only in `PLAN-V2.md`). Put a standard `⏱ 75 min · ⭐⭐⭐` banner at the top of every challenge so expectations are visible. |
| 5 | **Cleanup / cost-hygiene script** | [FWH §4.10] | Only Deploy has a cleanup note. Ship a per-tier `cleanup.sh` + a `wrapup.md` (recap + teardown) so teams don't leak Azure spend after the event. [FWH] does this on every track. |
| 6 | **"Why this option" decision table** | [ATA §4.7] | Add a short comparison matrix where we currently assert one path (e.g. App Insights vs OTLP vs AI Toolkit in Tracing; ACR cloud-build vs local Docker in Deploy). Teaches *judgment*, not just steps. |
| 7 | **"Your output should look like this" verification anchors** | [ATA §4.8] | Pair each Checkpoint with an expected-output snippet/screenshot to kill "am I on track?" anxiety between the long waits. |
| 8 | **Honest limitation call-outs** | [FWH §4.8] | The Deploy README already does this well ("No Prompt Flow here"). Extend the pattern — e.g. flag the App Insights ingestion lag as an *expected* wait, not a failure, up front in Tracing. |
| 9 | **Two-agent archetypes (detector-with-tool + reasoner-without)** | [FWH §4.4] | A clean, repeatable teaching frame for any future multi-agent Extra — reuse it in Magentic (Extra C) instead of inventing new roles. |

**Top 2 to adopt first** (highest value, lowest cost): **#4 (consistent time+difficulty banner)** —
it directly fixes the "does it really take the stated time?" complaint by making the estimate visible
and honest per challenge; and **#5 (cleanup/cost-hygiene script + wrapup)** — a one-file-per-tier add
that closes a real cost-leak gap both reference repos handle and we don't.

---

## 5. Handoff to PLAN-V3 (what Danny should decide)

1. **Adopt the 3-rung ladder** (§2) as the standard shape for all four Advanced challenges — it's the
   single biggest lever on "short/over-guided," and it adds no validators.
2. **Add the visible per-challenge banner** (§4 #4) and **rung labels** so depth is opt-in and honest.
3. **Document the reskin contract** (§3) now; realize **one** alternate domain (retail) as proof,
   wired to Extra F as the generator.
4. **Re-label, don't re-clock:** keep the wall-clock numbers (they're defensible) but split each into
   *"guided ~X / build-from-scratch ~Y"* so the label stops over-promising authoring.
5. **Budget Deploy at 90 min**, not 60 — it's the one challenge whose clock is optimistic, not padded.
