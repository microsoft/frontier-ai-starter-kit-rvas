
# Facilitator Guide · Extra — Build a UI (Wrap the Assistant in a Web App)

> **Facilitator-facing.** Facilitation, pitfalls, timing, and reference snippets for the Build-a-UI Extra.
> Do not paste this into the student README — answers live here only.

## Overview

This Extra is the "make it real" capstone: students put a browser front-end on the hosted agent
they shipped in Deploy as a Hosted Agent. The graded substance is three UI affordances —
streaming chat, a citations panel, and a human action-approval card — plus the one
non-negotiable security property: no credential ever reaches the browser. Everything talks to the
agent through a thin backend-for-frontend (BFF) that holds `DefaultAzureCredential`.

It is deliberately framework-agnostic. Don't let a team burn the session bootstrapping React/Vite if
plain HTML + `fetch` gets them to the three affordances faster. Steps 1–4 are local; Step 5 is the
Azure deploy (Container Apps or SWA + Functions) with managed identity + scoped CORS.

Hard prerequisite: the Deploy activity's live endpoint must answer authenticated Responses calls.
If a team hasn't done Deploy, they can point the BFF at the prompt-agent Responses route instead
(same `agent_reference` call they used in Foundations) — the UI work is identical; only the backend URL
changes. Step 4 (approval) additionally needs the Action Tools backend running (`ACTION_API_URL`).

Total time: about 1.5–2 hours if Deploy is done; longer if they also build a polished front-end.

---

## Step 1 — Scaffold the UI and a credential-holding BFF

### What good looks like

A page with a chat box calls `POST /api/chat` on a local BFF; the BFF authenticates with
`DefaultAzureCredential`, forwards to the hosted agent's Responses route, and returns the answer.
Browser DevTools shows zero secrets in delivered JS/HTML.

### The reference BFF (full, runnable — FastAPI)

```python
# server/app.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

app = FastAPI()
_token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
_base = os.environ["AZURE_AI_PROJECT_ENDPOINT"].rstrip("/")
_agent = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "northfield-iq-assistant")

def _client() -> OpenAI:
    return OpenAI(
        base_url=f"{_base}/agents/{_agent}/endpoint/protocols/openai",
        api_key=_token_provider(),
    )

class ChatIn(BaseModel):
    message: str

@app.post("/api/chat")
def chat(body: ChatIn):
    resp = _client().responses.create(input=body.message)
    return {"answer": resp.output_text, "raw": resp.model_dump()}

# Serve the static front-end same-origin so there are no CORS issues locally.
app.mount("/", StaticFiles(directory="web", html=True), name="web")

```
Run: `uvicorn server.app:app --port 5000` and open `http://localhost:5000`.

### Common pitfalls
- Calling the model from the browser. The #1 mistake — students put the endpoint + token in JS.
  That's a leaked credential. Force the proxy pattern: the browser only ever sees `/api/*`.

- CORS confusion locally. Serving `web/` from the same FastAPI app (StaticFiles mount) sidesteps
  CORS entirely for Steps 1–4; save CORS for the Step 5 deploy where origins actually differ.

- Wrong Responses route. It's
  `{AZURE_AI_PROJECT_ENDPOINT}/agents/{agent}/endpoint/protocols/openai` as the `base_url`, then
  `.responses.create(...)`. A trailing slash on the endpoint env var double-slashes the path — `rstrip("/")`.

- No Deploy done. Fall back to the prompt-agent route with
  `extra_body={"agent_reference": {"name": _agent, "type": "agent_reference"}}` — works against the Foundations agent.

---

## Step 2 — Stream the answer

### What good looks like

The BFF requests `stream=True` and relays Server-Sent Events; the page appends deltas so the answer
grows live. Send button disables mid-stream.

### Reference streaming relay

```python
from fastapi.responses import StreamingResponse

@app.post("/api/chat/stream")
def chat_stream(body: ChatIn):
    def gen():
        with _client().responses.stream(input=body.message) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    yield f"data: {event.delta}\n\n"
            yield "data: [DONE]\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")

```
Browser side: `const es = new EventSource('/api/chat/stream', ...)` (or `fetch` + `ReadableStream` for
POST bodies), append `event.data` until `[DONE]`.

### Common pitfalls
- Buffering proxies eat SSE. If deployed behind something that buffers, streaming looks broken. Set
  `X-Accel-Buffering: no` and disable response buffering on the host.

- Event-shape drift. The exact stream event type names move — have them `print(event)` once and read
  the real delta field rather than trusting this snippet verbatim (search microsoft-docs).

---

## Step 3 — Citations panel

### What good looks like

A grounded answer (FAFSA question) populates the panel with the real source doc (`financial-aid.md`);
an ungrounded/abstain answer shows "no sources" — never a fabricated citation.

### Where the citations live

The grounded agent attaches knowledge-base sources as annotations on the response output. Have
students `print(json.dumps(resp.model_dump(), indent=2))` once and find the annotation/citation array
(file name + snippet). Map those into a `sources` list the page renders. The exact field path shifts
with SDK versions — read it live, don't hard-code from memory.

### Common pitfalls
- Confusing the `[source]` text marker with structured citations. The model writes `[source]` in
  prose because the instructions asked it to; the *structured* sources come from the tool annotations.
  The panel should render the structured ones and align them to the markers.

- Fabricated citations. If the panel ever shows a source for an answer the agent abstained on, the
  mapping is wrong — they're echoing the prompt, not the retrieval. Good teachable moment.

---

## Step 4 — Action-approval card

### What good looks like

Asking to open a WiFi ticket renders an approval card (tool name + arguments) before anything runs.
Approve creates the record (check `curl http://localhost:8080/it-tickets`); Deny creates nothing. This
is the Action Tools `requires_action` loop surfaced in the browser.

### The shape

The BFF detects `run.status == "requires_action"`, returns the pending `RequiredFunctionToolCall`(s) to the
page (don't auto-approve!), and on the user's click submits a `ToolOutput(tool_call_id, output=...)`
via `submit_tool_outputs`, then resumes. Reuse the exact approval logic from the Action Tools
`solution.md` — this Extra just moves the human decision from the terminal to a button.

### Common pitfalls
- Auto-approving to "make it work." Defeats the entire point. The card must block on a human click.
- Losing the run between requests. The approval is a second HTTP call — the BFF must keep the run/
  response id around (in-memory dict keyed by a session id is fine for a workshop) to resume the right run.

- Action Tools backend not running. Step 4 needs `scripts/action-backend` up (REST :8080 + MCP :8765).

---

## Step 5 — Deploy to Azure

### What good looks like

Public URL answers, cites, and gates actions. The BFF runs under a system-assigned managed identity
granted `Foundry User` (formerly `Azure AI User`) on the project (no creds in app settings). CORS allows only the front-end
origin.

### Recommended path
- Container Apps is the least-moving-parts option: one container serves both the static `web/` build
  and the `/api/*` BFF, `az containerapp up`, enable system-assigned identity, assign `Foundry User` (formerly `Azure AI User`).

- SWA + Functions is cleaner separation (static front-end + linked Functions API, same-origin `/api`)
  but more wiring; pick it only if the team wants it.

### Common pitfalls
- `DefaultAzureCredential` works locally, 403s in the cloud. That's the identity not having
  `Foundry User` (formerly `Azure AI User`) on the project yet — assign the role to the app's managed identity, not to a user.

- Wildcard CORS. `allow_origins=["*"]` with credentials is both insecure and often rejected. Scope to
  the exact front-end origin.

- Secrets sneaking into app settings. The whole arc is keyless — if they're pasting a key into
  Container Apps settings, redirect them to managed identity.

---

## Optional checkpoint automation contract

No `validate.py` ships with this activity. If a team chooses to create one, it can implement:

| Command | Asserts |
|---|---|
| `python validate.py --step 1` | BFF proxies to the hosted agent; no secret in browser-delivered assets |
| `python validate.py --step 2` | `/api/chat/stream` returns `text/event-stream`; deltas relayed |
| `python validate.py --step 3` | A grounded answer returns a non-empty structured `sources` array |
| `python validate.py --step 4` | `requires_action` surfaces a pending tool call; approve creates, deny cancels |
| `python validate.py --all` | All of the above |

> Step 5 (Azure deploy) is portal/URL-verified — no programmatic checkpoint is required, but a facilitator
> should see the public URL chat, cite, and gate an action.

## Facilitation notes

- Keep teams off the framework rabbit hole. The grade is the three affordances + secret-free browser,
  not the CSS.

- The strongest demo is the approval card — it visibly ties together grounding (citations) and
  governance (human-in-the-loop) from the earlier Advanced activities. Encourage teams to show a
  deny as well as an approve.

- If short on time, Steps 1, 3, 4 (chat + citations + approval) are the must-haves; streaming (Step 2)
  and the Azure deploy (Step 5) are the polish.
