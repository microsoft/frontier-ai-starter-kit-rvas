---
title: "Extra: Build a UI"
parent: Challenges
nav_order: 24
---

# Extra · Build a UI — Wrap the Assistant in a Web App

> **Tier 2 · Extra — modular.** You can attempt this in any order with the other Extras.
> **Prerequisite: the Foundations end-state** (a deployed, grounded Northfield IQ Assistant).
> Complete Foundations, **or** run the bootstrap skip-path:
> `azd up && ./scripts/setup-foundations.sh && python scripts/validate-foundations.py`.
>
> **Specific prereq:** the **Advanced · Deploy as a Hosted Agent** challenge — this Extra puts a
> browser front-end on the **live Responses endpoint** you shipped there. For the action-approval
> panel (Step 4), also complete **Advanced · Action Tools** (`ACTION_API_URL`).

> 🎤 **Demo wow-factor:** a student types *"What's the FAFSA deadline?"* into a real chat window and
> watches the answer stream in **with a citations panel** beside it — then asks the agent to *open an
> IT ticket* and has to click **Approve** before anything happens. The same grounded, governed agent,
> now with a face.

## Why this challenge

Everything so far has been driven from a notebook, a script, or `curl`. That's right for building —
but no student is going to `POST /responses` from a terminal. To make the Northfield IQ Assistant feel
real, it needs a **web UI**: a chat window that streams answers, a **citations panel** that shows which
FAQ document each answer came from, and an **action-approval prompt** so a human stays in the loop
before the agent does anything with consequences.

You will **not** call the model from the browser. A bearer token in client-side JavaScript is a leaked
credential. Instead you build a thin **backend-for-frontend (BFF)** that holds the credential, talks to
the hosted agent over the Responses protocol, and exposes a small same-origin API to your page. Then
you deploy the whole thing — static front-end + BFF — to Azure and wire **CORS** correctly.

```text
   browser (chat UI)
      |
      | fetch /api/chat (same-origin; no secrets in JS)
      v
   BFF / proxy
      |-- DefaultAzureCredential --> hosted agent
      |                              (/protocols/openai/responses)
      |
      +--> runs in Container Apps or SWA+Functions
                                     |
                                     +--> knowledge base + MCP action tool
                                         (citations + actions)

```

## What you will need

- The Foundations `.env` (or bootstrap `.env`) with at least:
  - `AZURE_AI_PROJECT_ENDPOINT` — your Foundry project endpoint
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME` — the chat model deployment
  - `AZURE_FOUNDRY_AGENT_NAME` — the Northfield IQ Assistant agent name (e.g. `northfield-iq-assistant`)
  - `ACTION_API_URL` — the Action Tools REST backend base URL (only if you did Action Tools, for Step 4)
- The **hosted agent endpoint** from the Deploy challenge (the agent answers authenticated Responses
  calls).

- Node 18+ **or** Python 3.11+ for the BFF, and the Azure CLI (`az login`). `azd` if you deploy with it.

> 💡 You can build the front-end in any stack — plain HTML/JS is enough. The graded parts are the
> **three UI affordances** (chat, citations, approval) and a **secret-free browser**, not the framework.

---

## Step 1 — Scaffold the UI and a credential-holding BFF

**Goal:** A local web page talks to a thin backend that proxies to the hosted agent — and no Azure
credential ever reaches the browser.

**Tasks:**

1. Create `challenges/extra-build-ui/web/` with a minimal front-end: an `index.html` chat window
   (message list + input box + send button) and a `citations` side panel that starts empty.

2. Create `challenges/extra-build-ui/server/` — a thin BFF that exposes `POST /api/chat`. It reads the
   user message, attaches a bearer token via `DefaultAzureCredential`, and forwards to the hosted
   agent's Responses route
   (`{AZURE_AI_PROJECT_ENDPOINT}/agents/{AZURE_FOUNDRY_AGENT_NAME}/endpoint/protocols/openai/responses`).
   Sketch (Python/FastAPI):

   ```python
   # server/app.py
   import os
   from fastapi import FastAPI
   from pydantic import BaseModel
   from openai import OpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider

   app = FastAPI()
   _token = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
   _base = os.environ["AZURE_AI_PROJECT_ENDPOINT"].rstrip("/")
   _agent = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant")

   class ChatIn(BaseModel):
       message: str

   @app.post("/api/chat")
   def chat(body: ChatIn):
       client = OpenAI(
           base_url=f"{_base}/agents/{_agent}/endpoint/protocols/openai",
           api_key="placeholder",
           default_headers={"Authorization": f"Bearer {_token()}"},
       )
       resp = client.responses.create(input=body.message)
       return {"answer": resp.output_text, "raw": resp.model_dump()}

   ```

3. Run both locally (`uvicorn server.app:app --port 5000` + serve `web/`) and confirm a typed question
   round-trips through the BFF to the live agent and back into the chat window.

**Success Criteria:**

- [ ] Typing a question in the page returns the agent's answer in the chat window.
- [ ] **No bearer token, key, or `AZURE_*` secret appears anywhere in browser-delivered JS/HTML** (check
      DevTools → Sources / Network).

- [ ] The BFF authenticates with `DefaultAzureCredential` — no API key is pasted.

**Checkpoint:**

```bash
python validate.py --step 1
# expected: "✅ Step 1 PASS — UI calls the hosted agent through a secret-free BFF"

```

> _Coach note: see solution.md._

---

## Step 2 — Stream the answer into the chat window

**Goal:** Answers appear token-by-token (or chunk-by-chunk) instead of after a long blank pause.

**Tasks:**

1. Switch the BFF to **stream** the Responses output (`stream=True`) and relay it to the browser as
   **Server-Sent Events** (`text/event-stream`) over `GET/POST /api/chat/stream`.

2. In the page, consume the stream with `EventSource` (or `fetch` + `ReadableStream`) and append each
   delta to the in-flight assistant message so the answer grows live.

3. Add minimal UX: a "typing…" indicator while streaming, disable the send button mid-stream, and
   re-enable it when the stream closes.

**Success Criteria:**

- [ ] The answer renders progressively (visible deltas), not in a single late dump.
- [ ] The send button is disabled while a response is streaming and re-enabled when it completes.

**Checkpoint:**

```bash
python validate.py --step 2
# expected: "✅ Step 2 PASS — answers stream into the chat window via SSE"

```

> _Coach note: see solution.md._

---

## Step 3 — Render the citations panel

**Goal:** Every grounded answer shows **which Northfield FAQ documents** it came from, beside the chat.

**Tasks:**

1. In the BFF, pull the **citations / source annotations** out of the Responses payload (the grounded
   agent attaches the knowledge-base sources — inspect `resp.model_dump()` for the annotation/citation
   fields) and return them as a structured `sources` array alongside `answer`.

2. In the page, render each source in the **citations panel**: the document name (e.g.
   `financial-aid.md`) and the quoted snippet, as a numbered list that maps to the `[source]` markers
   in the answer text.

3. Ask the canonical grounded question — *"What is Northfield's FAFSA priority deadline and school
   code?"* — and confirm the panel lists the financial-aid source the answer cites.

**Success Criteria:**

- [ ] A grounded answer populates the citations panel with at least one real source document name.
- [ ] An answer with no grounding (or an abstention) shows an empty/"no sources" panel — it never
      fabricates a citation.

**Checkpoint:**

```bash
python validate.py --step 3
# expected: "✅ Step 3 PASS — citations panel renders real knowledge-base sources"

```

> _Coach note: see solution.md._

---

## Step 4 — Surface the action-approval prompt in the UI

**Goal:** When the agent wants to run an action tool, the UI **pauses and asks the human** to approve
or deny — the Action Tools governance loop, now with a button.

**Tasks:**

1. When the run comes back as `requires_action` (a `RequiredFunctionToolCall` from the action backend), have
   the BFF return the **pending tool call** — tool name + arguments — instead of an answer.

2. In the page, render an **approval card**: show the tool (`create_it_ticket`), its arguments
   (`student_id`, `summary`, …), and **Approve** / **Deny** buttons. Nothing runs until the user clicks.

3. On the click, `POST /api/chat/approve` with the decision; the BFF submits the `ToolOutput` and
   resumes the run, then streams the final result (the new `ticket_id`, or a clean "no action taken"
   on deny).

**Success Criteria:**

- [ ] Asking to *"open a high-priority WiFi ticket"* shows an approval card with the tool name +
      arguments **before** anything is created.

- [ ] **Approve** creates the record (visible via the Action Tools backend); **Deny** creates nothing.

**Checkpoint:**

```bash
python validate.py --step 4
# expected: "✅ Step 4 PASS — UI approval gates the action; approve creates, deny cancels"

```

**Full run:**

```text
python validate.py --all
# expected: "✅ ALL CHECKPOINTS PASS"

```

> _Coach note: see solution.md._

---

## Step 5 — Deploy the app to Azure (Container Apps or Static Web Apps)

**Goal:** The UI + BFF run in Azure with a public URL, the BFF authenticates with a **managed identity**,
and CORS is scoped — not wildcarded.

**Tasks:**

1. Pick a target:
   - **Azure Container Apps** — containerize the BFF (it can also serve the static `web/` build) and
     `az containerapp up` it. Simplest single-service path.

   - **Static Web Apps + Functions** — deploy `web/` as the static front-end and the BFF as the linked
     **Functions API**, so the browser calls a same-origin `/api/*`.

2. Replace `DefaultAzureCredential`'s local-dev login with a **system-assigned managed identity** on the
   hosted BFF, and grant that identity the **`Foundry User` (formerly `Azure AI User`)** role on the project so it can invoke the
   hosted agent.

3. Configure **CORS**: allow only your front-end origin (the SWA/Container Apps URL) on the BFF — never
   `*`. Confirm the deployed page loads, chats, cites, and gates actions exactly as it did locally.

**Success Criteria:**

- [ ] The app is reachable at a public Azure URL and answers a grounded question end-to-end.
- [ ] The BFF uses a **managed identity** (no credentials in app settings) with `Foundry User` (formerly `Azure AI User`) on the
      project.

- [ ] CORS allows **only** the front-end origin; a request from an unlisted origin is rejected.

**Checkpoint:** *Portal/URL state* — the public app answers, cites, and shows the approval card; the
BFF's identity is a managed identity and CORS is origin-scoped.

> _Coach note: see solution.md._

---

## Done — what you shipped

- A real **web UI** for the Northfield IQ Assistant: streaming chat, a **citations panel**, and a
  human **action-approval** card.

- A **secret-free browser** — the credential lives only in the BFF — deployed to Azure with a managed
  identity and origin-scoped CORS.

## Stretch goals

- Add a **conversation thread** (multi-turn) by passing the previous response id, so follow-up questions
  keep context.

- Show **per-answer trace links** that deep-link into the Tracing tab / App Insights (reuse the
  Tracing challenge's `operation_Id`).

- Add a **markdown renderer** so the agent's lists and links format nicely, and a copy-to-clipboard on
  each answer.

## Learning resources

- [Azure Container Apps quickstart](https://learn.microsoft.com/azure/container-apps/get-started)
- [Static Web Apps with an API](https://learn.microsoft.com/azure/static-web-apps/add-api)
- [Responses & Invocations protocols](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents#protocols-responses-and-invocations)
- [Managed identities for Azure resources](https://learn.microsoft.com/azure/active-directory/managed-identities-azure-resources/overview)
- [Configure CORS in Azure Container Apps](https://learn.microsoft.com/azure/container-apps/cors)
