# Module 2 — Select the source and permission architecture

This is the module that decides whether your pilot is safe. Retrieval quality can be fixed later;
a wrong permission boundary is discovered by the wrong person.

## What you build

1. A source decision: for each fact the assistant must know, which system is authoritative.
2. A permission architecture: which identity is evaluated at query time, and where.
3. A **runnable permission probe** that proves a restricted identity retrieves nothing — no content,
   no title, no snippet, no existence signal.

## Choose your path

| Option | Sources it reaches | Permission enforcement | Build effort | Status |
| --- | --- | --- | --- | --- |
| **A. Foundry IQ knowledge base** *(default)* | Blob, ADLS Gen2, SharePoint, OneLake, Azure SQL, Fabric, Work IQ, MCP, web — one base, many sources | ACL sync + query-time enforcement under the caller's Entra identity; honours Purview sensitivity labels | Low: configure sources, no pipeline code | GA + preview mix |
| B. Direct Azure AI Search index | Whatever you index yourself | You implement it: permission metadata in filterable fields + `x-ms-query-source-authorization` | High: you own chunking, embedding, refresh, security trimming | GA |
| C. Copilot Studio + SharePoint/M365 | SharePoint, Teams, Graph-connected content | Inherited from M365; no Azure retrieval layer to secure | Lowest, but you are not building an Azure app | GA |
| D. Fabric IQ | OneLake, lakehouses, semantic models, Power BI | Fabric RBAC / RLS on the semantic model | Medium; different skill set (data, not search) | See Fabric docs |
| E. Work IQ | M365 collaboration signals: docs, meetings, chats | M365 permissions | Medium, as a remote knowledge source | Preview |
| F. Web (Bing) | Public internet | None needed — public content only | Lowest | GA |

**Default: Option A.** Foundry IQ is the managed knowledge layer built on Azure AI Search agentic
retrieval. It gives permission-aware retrieval across multiple sources without you writing an
ingestion pipeline or a security-trimming filter, and one knowledge base can serve many agents.

**Choose B instead when** you need retrieval behaviour Foundry IQ does not expose: a custom scoring
profile, an unusual chunking strategy, a non-Microsoft vector store alongside it, or strict control
over every field in the index. You are trading weeks of work for that control.

**Choose C when** the answer is "this should be a Copilot, not an app". If all the knowledge lives in
SharePoint and the user is already in Teams, building an Azure retrieval stack is waste. Say so.

**D, E, F are rarely the whole answer** — they are usually *additional* knowledge sources on an
Option A knowledge base. Fabric IQ answers "what are the numbers", Foundry IQ answers "what does the
policy say". Do not index live operational data to make it searchable; route to it.

**Migration cost.** A → B is a rebuild of the retrieval layer but the agent and evaluations survive.
B → A is usually cheap, because an existing index can be wrapped as a *search index knowledge
source*. C → A/B is a full rebuild. This asymmetry is why A is the default: it is the cheapest thing
to move away from.

### The permission decision, stated precisely

Answer these four questions before writing any code. They determine everything downstream:

1. **Whose identity is evaluated at query time** — the end user, or a service identity acting for
   everyone? If it is a service identity, every user gets the union of all permissions.
2. **Where do permissions live** — source ACLs, Entra groups, Fabric RLS, or an application table?
3. **How do permission changes propagate** — and how stale can they be before that is a breach?
4. **What happens on a denial** — the correct answer is a normal "I don't have information on that",
   not an error that confirms the document exists.

## Implementation

### Option A — Foundry IQ knowledge base

Verified against Microsoft Learn on **2026-07-24**.

**Pick your knowledge source kinds.** A knowledge base references one or more sources; retrieval
queries all of them in one request and merges results through a single ranking pipeline.

| Kind | Indexed / remote | Status |
| --- | --- | --- |
| Search index (wraps an existing index) | Indexed | GA |
| Azure blob (auto-generates the indexer pipeline) | Indexed | GA |
| OneLake (lakehouse) | Indexed | GA |
| Web (Microsoft Bing) | Remote | GA |
| Azure SQL | Indexed | preview |
| File (direct upload to Search) | Indexed | preview |
| Indexed SharePoint | Indexed | preview |
| Remote SharePoint | Remote | preview |
| Fabric Data Agent | Remote | preview |
| Fabric Ontology | Remote | preview |
| MCP server | Remote | preview |
| Work IQ | Remote | preview |

Source: <https://learn.microsoft.com/azure/search/agentic-knowledge-source-overview>

*Indexed* means content is ingested before query time. *Remote* means it is fetched at query time
through the platform's own API and never stored in Search. Remote sources are always fresh and
always slower; indexed sources are fast and can be stale.

**Turn on ACL carry-forward at ingestion.** This is the switch people forget. On an indexed source,
permission metadata is only available at query time if you asked for it at ingestion time:

```python
ingestion_parameters = KnowledgeSourceIngestionParameters(
    # ...
    # Carry user and group object IDs from the source into the index.
    ingestion_permission_options=["user_ids", "group_ids"],
)
```

**Enforce at query time.** Document visibility requires *both* headers:

- `Authorization` — the calling application's own RBAC role.
- `x-ms-query-source-authorization` — the **end user's** token.

```python
result = kb_client.retrieve(
    request,
    headers={"x-ms-query-source-authorization": user_token},
)
```

Without the second header you are querying as the application, and every user sees everything the
application can see.

**API version decides what you get.** `2026-04-01` is GA but offers minimal, extractive retrieval
only: no query planning, no answer synthesis, no configurable reasoning effort, and GA source kinds
only. `2026-05-01-preview` adds all of those. Choose deliberately and record it — this is the single
most consequential version decision in the scenario.

### Option B — Direct Azure AI Search index

You are now responsible for security trimming. The rules, verified:

- Permission metadata must live in **filterable string fields**. You never write the filter
  yourself; the engine builds an internal filter to exclude unauthorized content.
- Store `userIds` and `groupIds` as **Entra object IDs (GUIDs)**.
- At query time the service matches identities in `x-ms-query-source-authorization` against those
  stored IDs. Group expansion happens at query time through Microsoft Graph.
- Use a **preview** REST API or preview SDK package; this filtering is not in the GA surface.

```python
from azure.search.documents.indexes.models import SearchField, SearchFieldDataType

permission_fields = [
    SearchField(name="userIds", type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                filterable=True),
    SearchField(name="groupIds", type=SearchFieldDataType.Collection(SearchFieldDataType.String),
                filterable=True),
]
```

Then query exactly as in Option A, passing the end-user token in
`x-ms-query-source-authorization`.

**Know the limits before you promise anything:**

| Constraint | Value |
| --- | --- |
| ACL entries per file/directory (ADLS Gen2) | 32 |
| Permission entries per file (SharePoint) | 1,000 |
| ACL evaluation failure (e.g. Graph unavailable) | Returns **5xx**, never a partially filtered result |
| First ACL-filtered query | Higher latency; later queries are cached |

Source: <https://learn.microsoft.com/azure/search/search-query-access-control-rbac-enforcement>

**Plan for permission freshness explicitly.** How ACL changes reach the index differs by source:

- SharePoint indexer: a scheduled run picks up item-level changes; changes to a **parent** scope
  (site, library, list, folder) inherited by children require a **resync**.
- ADLS Gen2 indexer: requires a resync to refresh ACLs.
- Custom/push ingestion: you must reingest affected documents yourself.

Write down the worst-case staleness window and get the data owner to accept it in writing. "A
revoked user keeps access for up to N hours" is a decision, not an accident.

### Option C — Copilot Studio + SharePoint / M365

No Azure retrieval layer to secure — permissions are whatever SharePoint and Microsoft 365 already
enforce, evaluated as the signed-in user.

Implementation is configuration, not code: connect the SharePoint site as a knowledge source in
Copilot Studio, scope it to the approved libraries, and publish to Teams.

The work that still matters is the same governance work: confirm the site's permissions actually
reflect intent (inherited permissions on a "public" site are the usual surprise), and test with a
low-privilege account.

If you pick this, **stop building the Azure stack** and say why in the decision record. Choosing not
to build is a legitimate, valuable outcome.

### Option D — Fabric IQ (analytics and live business data)

Use when the question is "what are the numbers", not "what does the document say". Fabric IQ models
business data — ontologies, semantic models, graphs, and data agents — over OneLake and Power BI.

Two ways to reach it from this scenario:

1. **As a remote knowledge source** on your Foundry IQ knowledge base: *Fabric Data Agent* (answers
   plus embedded resources) or *Fabric Ontology* (entity- and relationship-based answers). Both are
   preview.
2. **As a separate tool on the agent** in module 6, when you want explicit routing rather than
   blended retrieval.

Permissions are enforced by Fabric — semantic model RLS and workspace RBAC. Do not copy analytical
values into a search index to make them retrievable: you will serve stale numbers with a confident
citation. Reference: <https://learn.microsoft.com/fabric/iq/overview>

### Option E — Work IQ (Microsoft 365 collaboration context)

Work IQ is the contextual layer over M365 — documents, meetings, chats, workflows. Add it as a
**remote Work IQ knowledge source** (preview) when the pilot genuinely needs "how this organization
works" rather than "what the policy says".

Permissions follow M365. Because it is remote, content is never ingested into Search, which also
means there is no ACL staleness window. Reference:
<https://learn.microsoft.com/microsoft-365-copilot/extensibility/workiq-overview>

### Option F — Web

A remote source backed by Microsoft Bing, for public, citable authority. Note one hard constraint: a
knowledge base that includes a web knowledge source **requires** an LLM for query planning; it is
optional for every other source kind.

Public content needs no permission design, but it does need an authority decision: which domains are
acceptable to cite to this customer's users.

## Verify

Write the probe plan — [`accelerator/permission-probe.json`](../accelerator/permission-probe.json):

```json
{
  "cases": [
    {
      "id": "supervisor-playbook-is-restricted",
      "query": "What discretionary goodwill credit can a supervisor approve?",
      "expect_visible": ["returns-supervisor-playbook"],
      "expect_hidden": ["goodwill credit ceiling"]
    }
  ]
}
```

`expect_visible` is asserted against the authorized identity; `expect_hidden` against the restricted
one. A case with an empty `expect_hidden` is rejected — a probe that never expects a denial proves
nothing.

```bash
# Structure only, no Azure calls
python3 scenarios/ai-grounding/accelerator/scripts/probe_permissions.py --offline

# Live, against a knowledge base
export PROBE_TENANT_ID=... PROBE_CLIENT_ID=... PROBE_CLIENT_SECRET=...
python3 scenarios/ai-grounding/accelerator/scripts/probe_permissions.py \
  --knowledge-base grounding-kb
```

Expected:

```
✅ Module 2 checkpoint PASS — the permission boundary held
```

Include at least one **existence-signal** case: query for the restricted document by title and
confirm the restricted identity gets no title, no snippet, and no count that reveals it exists.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Restricted identity sees everything | `x-ms-query-source-authorization` not sent — you are querying as the app | Pass the end-user token; app RBAC alone is not a user boundary |
| `5xx` on every filtered query | ACL evaluation failed (often Graph unavailable) | This is by design: it fails closed rather than returning partial results. Fix Graph access; do not "handle" it by dropping the filter |
| Revoked user still gets results | ACL staleness | Resync the indexer; parent-scope changes in SharePoint need a full resync |
| Group membership ignored | Group IDs not ingested, or not stored as Entra object IDs | Set `ingestion_permission_options` to include `group_ids`; store GUIDs, not display names |
| Permission filtering silently absent | Using the GA API version | Query-time ACL filtering requires the preview API/SDK |
| Works for 30 docs, leaks at scale | ACL entry limits exceeded (32 ADLS Gen2, 1,000 SharePoint) | Redesign to group-based permissions rather than per-user entries |

## Decision record

One page, kept with the pilot: the chosen option and the two runners-up with the reason each lost;
which identity is evaluated at query time; where permissions live; the accepted staleness window,
signed by the data owner; the denial behaviour; the API version and whether it is preview; and the
probe result with a date.

## Next module

[Module 3 — Ingest and index approved content](03-ingest-and-index.md) implements the source you
just chose, with chunking, embeddings, and a refresh schedule.
