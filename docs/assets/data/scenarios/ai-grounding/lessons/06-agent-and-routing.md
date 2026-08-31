# Module 6 — Add agent and live-data routing only when justified

Module 5 produced a working grounded answer. Do not add an agent by default. Add one only when you
can name what it contributes. This module makes you name it, then build it correctly.

![Routing boundaries](../diagrams/06-routing-boundaries.png)

## What you build

1. A written justification, or a decision not to build an agent.
2. An agent with explicit source-routing rules across knowledge and live data.
3. A routing test proving policy questions and live-data questions reach different sources.

## Choose your path

Start with the test that decides whether to continue.

**You do not need an agent if** one knowledge source answers everything, the interaction is
single-turn question-and-answer, no action is taken for the user, and no live system is consulted.
Module 5 already shipped what you need. Deploy it and move to module 7.

**You need an agent when** the assistant must choose sources, call a live system, take an action, or
keep multi-turn state. Otherwise, it is architecture for its own sake.

| Option | What it adds | Cost | When it wins |
| --- | --- | --- | --- |
| No agent — module 5's retrieval path | Nothing; ships today | None | Single-source Q&A. Genuinely common; genuinely underused |
| **A. Foundry agent + knowledge tool** *(default when an agent is justified)* | Multi-turn, versioned, traceable, tool-capable | Low — one API surface | The normal case |
| B. Multi-source routing inside one knowledge base | Retrieval instructions steer across sources; one call, merged ranking | Low | Sources are all *knowledge*, not systems |
| C. Agent + separate live-data tool (Fabric IQ, MCP, OpenAPI) | Explicit routing between "what the policy says" and "what is true right now" | Medium | Live operational data is in play |
| D. Multi-agent workflow | Specialist agents with a planner | High — orchestration, latency, debugging | Genuinely distinct specialisations. Rarely justified in a pilot |

**Default: Option A**, extended with C when live data is required. Use B *inside* A when extra
sources are documents rather than systems. One knowledge base with good `retrieval_instructions`
beats three tools the agent must choose between.

**Avoid D in a pilot.** Multi-agent orchestration adds latency, cost, and failure modes. Customers
rarely evaluate it honestly against one well-instructed agent. If you truly need it, use the
[Magentic Workflows activity](../../../activities/extra-magentic-workflows/README.md), but earn it first.

**Use this rule:** index knowledge and route to systems. A policy document belongs in the knowledge
base. Case status, inventory, and live metrics belong behind a tool called at question time. Indexing
live data produces confidently cited stale numbers that look correct.

**Migration cost.** No-agent → A is cheap; retrieval and evaluations carry over. A → C is additive.
A/C → D needs a redesign and new metric baselines.

## Implementation

Use the repo's validator-backed activity code and current Microsoft Learn guidance.

### Option A — Foundry agent with a knowledge tool

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    AzureAISearchTool, AzureAISearchToolResource,
    AISearchIndexResource, AzureAISearchQueryType,
)
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
connection_id = project.connections.get(os.environ["AZURE_SEARCH_CONNECTION_NAME"]).id

agent = project.agents.create_version(
    agent_name="grounding-assistant",
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        instructions=ROUTING_INSTRUCTIONS,
        tools=[AzureAISearchTool(
            azure_ai_search=AzureAISearchToolResource(indexes=[
                AISearchIndexResource(
                    project_connection_id=connection_id,
                    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
                    query_type=AzureAISearchQueryType.SEMANTIC,
                    top_k=5,
                ),
            ])
        )],
    ),
)
print(f"{agent.name} version {agent.version}")
```

Invoke it through the Responses API:

```python
openai = project.get_openai_client()
resp = openai.responses.create(
    input="Can a coordinator approve an unused standard return on day 30?",
    extra_body={"agent_reference": {"name": "grounding-assistant", "type": "agent_reference"}},
)
print(resp.output_text)
```

`create_version` matters because agents are **versioned**. Every instruction change produces a new
version, so you can attribute an evaluation result to one version. Record it in the decision record
and every evaluation run, or you cannot explain last week's score changes.

If you built a Foundry IQ knowledge base in module 3, attach that instead of the raw index — the
agent then inherits query planning, multi-source merging, and permission-aware retrieval rather than
querying one index directly.

### Writing routing instructions that actually route

This prompt has a testable outcome, so treat it as code:

```text
You answer questions for returns coordinators.

Sources, in priority order:
1. Approved policy knowledge — returns policy, exceptions, and published service notices.
   Use for any question about what is allowed, who approves it, or what the process is.
2. Live case data (tool: case_lookup) — the current state of a specific order or case.
   Use whenever the question names an order id, a case id, or asks what is happening "now".

Rules:
- Never answer a live-data question from policy knowledge. Call the tool.
- Never answer a policy question from live data.
- When published notices conflict, use the one with the most recent effective date.
- Cite the document id for every policy claim, and the case id for every live claim.
- If neither source covers the question, say: "I don't have approved information on that."
- Never reveal that a document exists if retrieval did not return it to you.
```

Vague instructions produce vague routing. "Use the appropriate source" does not route anything.

### Option B — Multi-source routing inside one knowledge base

Add sources to the knowledge base from module 3 and steer with `retrieval_instructions`:

```python
knowledge_base = KnowledgeBase(
    name=os.environ["AZURE_KNOWLEDGE_BASE_NAME"],
    knowledge_sources=[
        KnowledgeSourceReference(name="approved-content-ks"),
        KnowledgeSourceReference(name="sharepoint-hr-ks"),
    ],
    retrieval_instructions=(
        "Use approved-content-ks for returns policy, exceptions, and service notices. "
        "Use sharepoint-hr-ks only for internal staff process questions. "
        "Prefer the most recent effective date when sources disagree."
    ),
    ...
)
```

All sources use one ranking pipeline and return merged. That works better than tool-choice routing
when every source is a document, because the model does not have to guess before seeing anything.

### Option C — Live data as a routed tool

Two supported shapes:

1. **Fabric IQ as a remote knowledge source** — *Fabric Data Agent* (answers with embedded
   resources) or *Fabric Ontology* (entity- and relationship-based answers), both preview. Fabric
   enforces its own permissions: semantic model RLS and workspace RBAC. The
   [Fabric IQ activity](../../../activities/extra-fabric-iq/README.md) builds this end-to-end.
2. **Governed structured-data copilot** — use this when the live source is a semantic model or
   approved structured-data endpoint and the boundary is query allowlists, RLS/masking, and
   provenance. The
   [Governed Data Copilot activity](../../../activities/extra-governed-data-copilot/README.md)
   builds the deny-by-default control plane.
3. **An MCP or OpenAPI tool on the agent** — for a line-of-business system with an API. The
   [action tools activity](../../../activities/advanced-action-tools/README.md) builds this,
   including the human-approval loop.

The answer must show the boundary. "Per RET-POL-2026-01 you may approve this; case 44810 is
currently awaiting carrier evidence" separates policy from live data. A blended paragraph does not.

**If the tool takes an action**, such as issuing a credit or releasing a hold, add a human approval
step. Read-only retrieval is recoverable. Actions are not.

### Option D — Multi-agent workflow

Covered by the [Magentic Workflows activity](../../../activities/extra-magentic-workflows/README.md).
Before using it, write down the specific question that one agent with two tools answers worse. If
you cannot write it, you have the answer.

## Verify

This module catches an agent that calls tools by reflex instead of abstaining, or answers "what is
happening now" from a stale index. Route the four cases through the deployed agent, then confirm it
did not worsen retrieval.

**1. Route the four cases and read the answers.** Send each through the deployed agent with the
Responses API:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                          credential=DefaultAzureCredential())
openai = project.get_openai_client()

cases = {
    "policy":      "Can a coordinator approve an unused standard return on day 30?",
    "live":        "What is the current status of order 44810?",
    "mixed":       "Can I refund order 44810, and what does policy allow for its condition?",
    "out-of-scope":"What is the office coffee order for next week?",
}
for label, q in cases.items():
    resp = openai.responses.create(
        input=q,
        extra_body={"agent_reference": {"name": "grounding-assistant", "type": "agent_reference"}},
    )
    print(f"\n[{label}] {resp.output_text}")
```

The `out-of-scope` answer must be exactly `I don't have approved information on that.` An agent that
calls the tool and improvises has failed. The `live` answer must name the case ID, not quote policy.
The `mixed` answer must cite the policy document ID and case ID separately. The `policy` answer must
cite a document ID.

**2. Confirm the agent did not lower recall.** Re-run the module 5 baseline against the same knowledge
base:

```bash
python3 scenarios/ai-grounding/accelerator/scripts/grounded_answer.py \
  --knowledge-base "$AZURE_KNOWLEDGE_BASE_NAME"
```

The `recall@5` line must match the value from module 5. If it drops, the agent's query rewriting
hurts retrieval. Fix it here, rather than discovering it as an unexplained evaluation regression.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Agent answers live-data questions from the index | Routing instructions too vague, or live data was indexed | Name the trigger conditions explicitly; remove live data from the index |
| Tool never called | Tool description too abstract for the model to match | Rewrite the description around user phrasing, not internal system names |
| Tool called for everything | No negative condition in the instructions | State when *not* to call it |
| `403` from the agent to Search | Project managed identity lacks **Search Index Data Contributor** and **Search Service Contributor** | Assign both on the search service; module 1's Bicep does this |
| Answers changed after a redeploy | New agent version, silently | Pin and log `agent.version` in every run and every evaluation |
| Latency doubled | Multiple tool round trips per question | Reduce sources, lower reasoning effort, or drop back to the module 5 path |
| Citations vanish once the agent is added | Agent instructions did not restate the citation rule | Restate it; the tool's behaviour does not carry into the agent's output contract |
| Agent reveals restricted document titles | Retrieval passed metadata the instructions did not suppress | Re-run module 2's permission probe against the *agent*, not just retrieval |

## Decision record

Record whether an agent was justified and the capability that justified it, or the decision not to
build one; routing rules and test result; agent name and **version**; authoritative live-data system
and owner; action-capable tools and human approval point; and re-measured `recall@5`.

## Next module

[Module 7 — Evaluate and trace](07-evaluate-and-trace.md) proves the whole thing with
numbers, red-teams it, makes it observable, and decides whether it ships.
