---
marp: true
theme: default
paginate: true
title: "AI Grounding / IQ — Customer Delivery Workshop"
version: "1.0.0"
footer: "Customer Delivery · AI Grounding / IQ"
---

# AI Grounding / IQ
## Choose trusted context for one customer decision

**Today:** agree the decision, access boundary, source pattern, and proof plan.

---

# 1. Start with a decision

| Prompt | Capture |
|---|---|
| Who is deciding or acting? | named role |
| What changes if the answer is good? | measurable action |
| What must never happen? | failure boundary |

Example: “A service coordinator can explain the approved returns exception before accepting a request.”

---

# 2. Draw the access boundary

- Which groups can see which records?
- Is permission trimming required at answer time?
- Which system remains the source of record?
- What geographic, retention, and sensitivity constraints apply?

**Decision:** no source enters the pilot without an owner and an access decision.

---

# 3. Choose the experience first

**Copilot Studio + SharePoint** fits when the work is a business workflow in Microsoft 365 and SharePoint is the governed knowledge home.

Choose a **Foundry-built experience** when the product needs custom orchestration, application integration, or a composable context layer.

Do not migrate content just to make an architecture diagram cleaner.

---

# 4. Match context to the work

| Need | Lead with |
|---|---|
| Approved documents and process content | SharePoint / Foundry IQ |
| Governed analytical facts and metrics | Fabric IQ |
| Work signals and Microsoft 365 context | Work IQ |
| Curated public information with attribution | Web IQ |

One outcome can use more than one source—only with an explicit boundary.

---

# 5. Decide the source and IQ pattern

For each candidate source, record:

1. owner and update cadence  
2. permissions and sensitivity  
3. citation or provenance expectation  
4. freshness need  
5. failure mode when unavailable  

The pattern is approved only when the source owner accepts it.

---

# 6. Define the golden dataset now

Bring 20–40 representative questions or tasks:

- routine cases
- ambiguous wording
- stale or conflicting content
- access-denied cases
- high-impact exceptions

For each: expected action, permitted sources, required citation, and reviewer.

---

# 7. Agree what “good” means

| Measure | Pilot threshold |
|---|---|
| Grounded answer/action correctness | agreed with business reviewer |
| Unsupported claims | zero for high-impact tasks |
| Correct access behavior | all access tests pass |
| Evidence returned | source and date where needed |

Measure latency and cost, but do not trade away access control or evidence.

---

# 8. Operate the knowledge, not just the assistant

- Source owner: approves content and retirement
- Service owner: handles incidents and change windows
- Evaluator: reviews golden-set drift
- Security/privacy owner: reviews access changes

Review evidence after source changes, permission changes, and model/context changes.

---

# 9. Pilot decision record

**We will:** ground *[role]* for *[decision]* using *[approved pattern]*.  
**We will not:** *[non-goals]*.  
**We will prove:** *[golden-set measures]*.  
**We will revisit:** *[date / trigger]*.

---

# 10. Next workshop actions

1. Confirm source owners and access boundary.
2. Select the smallest valuable source set.
3. Write the golden dataset before connecting production content.
4. Search current Microsoft documentation and load the relevant implementation guidance.
5. Pilot with operating evidence; expand only after the review.
