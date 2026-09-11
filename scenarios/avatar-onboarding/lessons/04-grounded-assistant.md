# Module 4 — Build the grounded assistant behind the experience

The avatar is a mouth. This module builds the brain: a grounded assistant that drafts onboarding
script text **only** from the approved claim set, **cites** every claim, **refuses** requests it
cannot ground, and **hands off** to a human help path. If the assistant invents a benefit, the avatar
will repeat it.

This module applies [Foundations](../../../activities/foundations/README.md) **Steps 3–4** to
onboarding. Build the mechanics there, then apply the onboarding rules below. Prompt Flow is outside
this curriculum; use agents + tools + retrieval.

![Grounded assistant boundary](../diagrams/04-grounded-assistant-boundary.png)

## What you build

1. A grounded generation path, model-with-retrieval **or** a Foundry agent, that produces script
   text traceable to approved claims.
2. Guardrails: cite every claim, **abstain** when no approved claim covers the question, and
   **escalate** to the claim's `help_path`.
3. A retrieval boundary that limits the assistant to approved content (module 3's corpus / knowledge
   base).

## Choose your path

| Option | What it is | Grounding | Build effort | Best when |
| --- | --- | --- | --- | --- |
| **A. Model + retrieval (grounded prompt)** *(default)* | Chat deployment + your retrieval over the claim set, with a strict system prompt | You control the prompt and the citations | Low | The claim set is small and you want maximum control over refusal/citation |
| B. Foundry agent + knowledge base | A named, versioned Foundry agent with a knowledge tool | Managed retrieval + citations from the knowledge base | Medium | You want a reusable, governed agent that other channels share |
| C. Foundry agent + agentic retrieval (Foundry IQ) | Agent over a permission-aware knowledge base | Query planning + answer synthesis + ACL enforcement | Medium/High | Content spans systems and needs permission-aware retrieval |

**Default: Option A** for the pilot: a chat deployment retrieves from the small approved claim set,
and its system prompt forbids ungrounded statements. It is the smallest setup with tight control
over the two behaviours that matter here: **cite** and **refuse**. Choose **B** when you want a
named, versioned agent shared across channels (including module 5 Option C, Voice Live). Choose
**C** when retrieval must be permission-aware across systems.

**Migration cost.** A → B/C retains the claim set, module-7 golden questions, and refusal contract;
only the drafting call becomes an agent invocation. B → A is trivial. Build the module-7 evaluation
set once because all three options use it.

## Implementation

### Option A — Model + retrieval (default)

**Ground on the claim set and forbid invention.** Make the system prompt explicit:

```python
SYSTEM_PROMPT = """You draft onboarding script text for a synthetic avatar presenter.
Rules:
1. State only facts present in the provided APPROVED CLAIMS. Never paraphrase policy.
2. For each sentence, cite the claim_id you used.
3. If no approved claim covers the request, start with "NO_APPROVED_CLAIM", then name the relevant help_path.
4. Never invent benefits, dates, amounts, or obligations.
"""
```

**Draft against approved claims only** (keyless, `DefaultAzureCredential`):

```python
import json, os
from pathlib import Path
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

claims = json.loads(Path("scenarios/avatar-onboarding/accelerator/sample-data/claims.json").read_text())
approved = "\n".join(f'{c["claim_id"]}: {c["approved_wording"]} (help: {c["help_path"]})'
                     for c in claims["claims"])

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_AI_FOUNDRY_ENDPOINT"],
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
)

def draft(question: str) -> str:
    resp = client.chat.completions.create(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"APPROVED CLAIMS:\n{approved}\n\nDraft: {question}"},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content
```

> Search before you implement. Confirm the current `AzureOpenAI` / Foundry chat signature and
> `api_version` against Microsoft Learn because the SDK surface changes. The onboarding rule is fixed:
> **draft only from `claims.json`, cite `claim_id`, refuse with `NO_APPROVED_CLAIM`.**

**Enforce refusal downstream.** Module 5's renderer rejects script segments whose spoken text is
not an *exact* approved claim. A paraphrase or invented sentence cannot render. The model is the
first gate; the renderer is the backstop.

### Option B — Foundry agent + knowledge base

Build the agent in [Foundations Step 4](../../../activities/foundations/README.md). Use a named,
versioned agent with a knowledge tool over module 3's corpus, the "onboarding script drafter"
persona, and the same refusal instruction. Store its name in `.env` (`AZURE_FOUNDRY_AGENT_NAME`) so
module 5 Option C (Voice Live agent mode) and module 7 (evaluation) can reuse it. The agent returns
knowledge-base citations; confirm that they map to approved claim ids.

### Option C — Foundry agent + agentic retrieval (Foundry IQ)

When retrieval must be permission-aware, use a Foundry IQ knowledge base behind the agent. Use the
preview API version for query planning and answer synthesis, pass the end-user token in
`x-ms-query-source-authorization`, and keep the "approved claims only" instruction. Verified facts
from the AI Grounding stack:
<https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base>

The assistant may draft *candidate* script text under any option. A **human still approves** the
final wording in module 6. The assistant speeds authoring. It does not grant publication.

## Verify

Test the two behaviours that make this assistant safe to put behind a face: it must **cite**
on-claim answers and **refuse** off-claim ones. Run both against your deployment, not a fixture.
This grounded call uses your Entra identity, with no key:

```bash
set -a; source scenarios/avatar-onboarding/accelerator/.env; set +a
TOKEN=$(az account get-access-token --scope https://cognitiveservices.azure.com/.default --query accessToken -o tsv)

ask () {
  CLAIMS=$(jq -r '.claims[] | "\(.claim_id): \(.approved_wording) (help: \(.help_path))"' \
    scenarios/avatar-onboarding/accelerator/sample-data/claims.json)
  jq -n --arg q "$1" --arg claims "$CLAIMS" '{
    temperature: 0,
    messages: [
      {role:"system", content:"You draft onboarding script text. Use the exact wording of facts in APPROVED CLAIMS and cite the claim_id you used. If no approved claim covers the request, start with NO_APPROVED_CLAIM, then name the relevant help_path. Never invent benefits, dates, or amounts."},
      {role:"user", content:("APPROVED CLAIMS:\n" + $claims + "\n\nDraft: " + $q)}
    ]}' | curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d @- \
    "$AZURE_AI_FOUNDRY_ENDPOINT/openai/deployments/$AZURE_AI_MODEL_DEPLOYMENT_NAME/chat/completions?api-version=2024-10-21" \
    | jq -r '.choices[0].message.content'
}
```

**1. An on-claim question is answered from an approved claim and cites it.**

```bash
ask "When do I select benefits?"
```

Good output states the approved wording and names `ONB-001`. If it paraphrases the policy or drops
the citation, tighten the system prompt and keep `temperature` at 0. A paraphrased policy becomes
an unapproved claim.

**2. An off-claim question is refused, not invented.**

```bash
ask "How much is the parking subsidy?"
```

The only acceptable output is `NO_APPROVED_CLAIM` and the help path. A plausible dollar figure is a
confident, replayable, made-up number spoken by a face. If you get one, do not render the assistant.
A `401`/`403` means you are missing the **Cognitive Services OpenAI User** role on the account.
Grant it and stay keyless.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Assistant invents a benefit/amount | Weak system prompt or content not constrained to claims | Enforce "approved claims only", `temperature=0`, and the exact refusal token |
| Cites a claim id that doesn't exist | Model hallucinated a citation | Validate every returned `claim_id` against `claims.json`; drop unknown citations |
| Refuses valid on-claim questions | Approved context omitted the claim | For A, inspect the loaded `claims.json`; for B/C, check retrieval and index contents |
| `401`/`403` calling the model | Missing Cognitive Services OpenAI User role or wrong endpoint | Assign the role; use `AZURE_AI_FOUNDRY_ENDPOINT`; keyless via `DefaultAzureCredential` |
| Agent answers from outside the corpus | Knowledge tool scope too broad | Scope the knowledge tool to the approved corpus only |
| Paraphrased policy reaches the script | Free-text drafting | The renderer requires exact-claim spoken text; author claims, not prose |

## Next module

[Module 5 — Generate the accessible avatar experience](05-experience-generation.md) turns an approved
script revision into a disclosed, captioned experience with a non-avatar fallback.
