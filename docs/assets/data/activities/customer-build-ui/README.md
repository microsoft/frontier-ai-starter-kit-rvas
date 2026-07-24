
# Customer Build · Build a UI



This deepener adapts [Extra · Build a UI](activity.html?id=extra-build-ui): it uses the same browser/BFF pattern for your scenario from [Define your outcome](activity.html?id=customer-outcome). A UI can make a demo easier to understand, but it can also take time better spent proving grounding, action safety, or evaluation.

> Before you start this deepener: complete the agent you want to show. For approval cards, complete Action Tools. If a script, Playground run, or hosted endpoint already tells your story, skip this.

---

## Preflight — Confirm what the UI must show

**Why it matters for your app:** the UI should support the demo story, not become a second product build.

**Does this apply to you?** → Skip it if your audience is technical and a trace/script demo is stronger.
- Build it if stakeholders need a browser to understand the assistant.
- Adapt it if you only need one affordance: chat, citations, approval, or public URL.

**Decisions to make:**
- Which target user is this UI for?
- Which success measure must be visible: answer quality, citation trust, approval safety, or latency?
- What is the smallest UI that supports your demo story?

**Apply it to your app:** map your demo story to the required UI pieces before writing code. → [Extra · Build a UI — What you will need](activity.html?id=extra-build-ui#what-you-will-need)

**Prove you applied it:**
- [ ] You can name the user and one demo task the UI must support.
- [ ] You chose which affordances are in scope and which are out.
- [ ] You know which existing endpoint the BFF will call.

**Stuck?** [Northfield preflight](activity.html?id=extra-build-ui#what-you-will-need).

---

## Step 1 — Scaffold the UI and credential-holding BFF

**Why it matters for your app:** the browser must never hold Foundry credentials. The BFF is the safety boundary between user interface and agent endpoint.

**Does this apply to you?** → Skip it if you are not building a browser demo.
- Build it if your final demo uses any web page.
- Adapt it if your UI is Teams, mobile, or another client — keep the same "no secrets in client" rule.

**Decisions to make:**
- What front-end stack is fastest for your team?
- What same-origin API shape does your UI need?
- Which identity will the BFF use locally and in Azure?

**Apply it to your app:** create the browser and BFF around your hosted agent endpoint; do not copy secrets into delivered JS or HTML. → [Extra · Build a UI — Step 1](activity.html?id=extra-build-ui#step-1--scaffold-the-ui-and-a-credential-holding-bff)

**Prove you applied it:**
- [ ] A typed scenario question round-trips through the BFF to your agent.
- [ ] DevTools shows no bearer token, key, or `AZURE_*` secret in browser-delivered assets.
- [ ] The BFF authenticates keylessly.

**Stuck?** [Northfield Step 1](activity.html?id=extra-build-ui#step-1--scaffold-the-ui-and-a-credential-holding-bff).

---

## Step 2 — Stream the answer into the chat window

**Why it matters for your app:** streaming reduces perceived latency and makes the assistant feel alive during stakeholder demos.

**Does this apply to you?** → Skip it if your answers are short and latency is not part of the story.
- Build it if your scenario has long grounded explanations or action summaries.
- Adapt it if your client uses WebSockets or another streaming mechanism instead of SSE.

**Decisions to make:**
- Which response states should the user see: thinking, streaming, complete, error?
- What should be disabled while a response is in flight?
- How will you handle cancellation or retries?

**Apply it to your app:** relay streamed response chunks through the BFF and render them progressively. → [Extra · Build a UI — Step 2](activity.html?id=extra-build-ui#step-2--stream-the-answer-into-the-chat-window)

**Prove you applied it:**
- [ ] The answer appears progressively, not as one late block.
- [ ] The send control is disabled or guarded while streaming.
- [ ] Errors end the stream cleanly and leave the UI usable.

**Stuck?** [Northfield Step 2](activity.html?id=extra-build-ui#step-2--stream-the-answer-into-the-chat-window).

---

## Step 3 — Render the citations panel

**Why it matters for your app:** citations turn a flashy demo into a trusted answer grounded in your approved corpus.

**Does this apply to you?** → Skip it only if your scenario has no knowledge grounding.
- Build it if grounding is central to your value proposition.
- Adapt it if your sources are records, tickets, or live data instead of documents.

**Decisions to make:**
- Which source fields should users see: title, snippet, URL, timestamp, owner?
- How will the UI display abstentions or answers with no sources?
- What scenario question proves the citations are real?

**Apply it to your app:** extract source annotations in the BFF and render them beside the answer using your corpus names. → [Extra · Build a UI — Step 3](activity.html?id=extra-build-ui#step-3--render-the-citations-panel)

**Prove you applied it:**
- [ ] A grounded scenario answer shows at least one real source.
- [ ] An ungrounded or abstained answer does not fabricate a source.
- [ ] The displayed source is useful to your target user.

**Stuck?** [Northfield Step 3](activity.html?id=extra-build-ui#step-3--render-the-citations-panel).

---

## Step 4 — Surface the action-approval prompt in the UI

**Why it matters for your app:** human approval must be visible at the exact moment the agent wants to do something consequential.

**Does this apply to you?** → Skip it if your app has no action tools or all actions are read-only.
- Build it if your action candidates change records, send messages, create tickets, spend money, or affect access.
- Adapt it if approval happens outside the UI, such as email, Teams, or a case system.

**Decisions to make:**
- Which tool arguments must be shown before approval?
- Who is allowed to approve or deny?
- What is the safe denial message and what audit trail do you need?

**Apply it to your app:** render a pending tool call as an approval card and resume only after the user chooses. → [Extra · Build a UI — Step 4](activity.html?id=extra-build-ui#step-4--surface-the-action-approval-prompt-in-the-ui)

**Prove you applied it:**
- [ ] A consequential request shows an approval card before any action runs.
- [ ] Approve performs the action and shows the result.
- [ ] Deny performs nothing and explains the outcome.

**Stuck?** [Northfield Step 4](activity.html?id=extra-build-ui#step-4--surface-the-action-approval-prompt-in-the-ui).

---

## Step 5 — Deploy the app to Azure

**Why it matters for your app:** a public URL makes the demo shareable, but only if identity and CORS stay locked down.

**Does this apply to you?** → Skip it if local demo is enough and deployment time threatens your core outcome.
- Build it if stakeholders need to open the app themselves.
- Adapt it if your organization already has a preferred hosting platform.

**Decisions to make:**
- Container Apps or Static Web Apps + Functions?
- Which managed identity gets Foundry access?
- Which exact origin is allowed by CORS?

**Apply it to your app:** deploy the UI+BFF, switch to managed identity, and scope CORS to the front-end origin. → [Extra · Build a UI — Step 5](activity.html?id=extra-build-ui#step-5--deploy-the-app-to-azure-container-apps-or-static-web-apps)

**Prove you applied it:**
- [ ] The public URL answers a grounded scenario question.
- [ ] The BFF uses managed identity, not stored credentials.
- [ ] CORS rejects an unlisted origin.

**Stuck?** [Northfield Step 5](activity.html?id=extra-build-ui#step-5--deploy-the-app-to-azure-container-apps-or-static-web-apps).

---

## Deepener end-state

You have a safe browser demo for your agent: chat, citations, and approvals only where they help your story. Deepeners are optional; return to the [Customer Build Track](catalog.html?outcome=customer-build) and protect time for the outcome.
