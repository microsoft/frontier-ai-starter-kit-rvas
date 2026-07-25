# Solution notes · Extra — Governed Data Copilot

This is a reference design, not a connector recipe. The data/Foundry connector surface may be preview
or change independently of this curriculum. Search `microsoft-docs` and `foundry-mcp`, load the matching
skill, and use the signature returned there before replacing the pseudocode below.

## Stable design

Keep the volatile connector behind a tiny adapter. The stable application boundary is:

```text
intent → validate_request → execute_registered_query → normalize_result → review_gate → response
```

The LLM may select from named intents, but it never emits a query language expression. The adapter
only accepts a registered query ID and validated, typed parameters. Define the query templates in the
semantic model/data service where possible; do not store a broad query template in the prompt.

```python
# governed_data_copilot.py — illustrative pseudocode; replace only the adapter
# with the current, Docs-verified connector call.
from azure.identity import DefaultAzureCredential
from dataclasses import dataclass
from datetime import datetime, timezone

APPROVED_FIELDS = frozenset({
    "service_area", "waiting_count", "median_wait_minutes",
    "capacity_status", "snapshot_at",
})

ALLOWED_QUERIES = {
    "queue_overview": {
        "fields": APPROVED_FIELDS,
        "parameters": {"service_area": {"advising", "financial_aid", "registrar"}},
        "aggregate_only": True,
    },
    "capacity_risk": {
        "fields": frozenset({"service_area", "waiting_count", "capacity_status", "snapshot_at"}),
        "parameters": {"service_area": {"advising", "financial_aid", "registrar"}},
        "aggregate_only": True,
    },
}

@dataclass
class GovernedResult:
    rows: list[dict]
    provenance: dict
    requires_human_review: bool
    uncertainty: str | None = None

def validate_request(query_id: str, parameters: dict) -> dict:
    spec = ALLOWED_QUERIES.get(query_id)
    if spec is None:
        raise ValueError("Query is not approved.")
    if set(parameters) != set(spec["parameters"]):
        raise ValueError("Unexpected or missing parameter.")
    for name, value in parameters.items():
        if value not in spec["parameters"][name]:
            raise ValueError(f"Parameter {name} is not approved.")
    return spec

def execute_governed_query(query_id: str, parameters: dict) -> GovernedResult:
    spec = validate_request(query_id, parameters)
    credential = DefaultAzureCredential()

    # PSEUDOCODE: create the current documented, read-only data/semantic-model client
    # with `credential`; execute the registered query_id using typed `parameters`.
    # Do not concatenate parameters into SQL/DAX/KQL/OData and do not use a preview
    # Foundry class name unless current Docs/MCP verification supplied it.
    raw = current_connector_execute_registered_query(
        credential=credential, query_id=query_id, parameters=parameters
    )

    retrieved_at = datetime.now(timezone.utc).isoformat()
    provenance = {
        "query_id": query_id,
        "semantic_model": "sample organizationServiceOperations",
        "semantic_model_version": raw.model_version,
        "approved_fields": sorted(spec["fields"]),
        "parameters": parameters,
        "snapshot_at": raw.snapshot_at,
        "retrieved_at": retrieved_at,
        "access_scope": "Platform-enforced Entra/RLS and column masking.",
    }
    uncertain = raw.is_stale or raw.is_incomplete
    return GovernedResult(
        rows=raw.aggregate_rows,
        provenance=provenance,
        requires_human_review=uncertain or raw.high_impact,
        uncertainty="Result may be stale or incomplete." if uncertain else None,
    )
```

`current_connector_execute_registered_query` is intentionally undefined. It is the one integration
point learners implement after verifying the live service API. The rest of the pattern is ordinary,
testable Python and should stay stable across connector changes.

## Keyless access pattern

1. Assign a managed identity to the deployed workload; use the developer's signed-in identity locally.
2. Authenticate with `DefaultAzureCredential`, passing that credential to the Docs-verified client.
3. Grant the identity only data-plane read access required by the semantic model/end-point. Configure
   RLS and column masking on the data platform—not in application code.
4. Verify locally with `az login`; in hosted environments verify the managed identity has the same
   least-privilege permissions. Never substitute a shared key when a denial occurs.

The credential chooses the appropriate supported identity source. No client secret, API key, database
password, or connection string belongs in `governed_data_copilot.py`.

## Validation and response rules

- **Query validation:** reject unknown IDs, unapproved output fields, unexpected parameters, wrong
  parameter types, and values outside enumeration/range constraints before a connector call.
- **Result validation:** accept only the fields declared by the registered query; treat missing,
  masked, stale, or incomplete values as uncertainty, not zero.
- **Provenance:** retain query ID, model/version, approved field set, validated arguments, snapshot,
  retrieval time, and access/RLS statement with the answer and audit event.
- **Access denial:** return a neutral “not authorized or unavailable” outcome; do not enumerate
  protected rows, fall back to another identity, or infer their existence.
- **Human review:** make recommendations and action-like wording conditional on review when output is
  sensitive, ambiguous, sparse, stale, or high impact. The reviewer validates context and decides.

## Test matrix

| Input | Expected result |
|---|---|
| `queue_overview`, `{"service_area": "advising"}` | Validated aggregate plus provenance |
| Unknown query ID | Denied before connector invocation |
| `{"service_area": "advising", "field": "student_name"}` | Denied for unexpected parameter/field |
| Connector reports 403 | Access-denied response, no retry with escalation |
| Empty/stale response | Uncertain outcome, not “no students waiting” |
| “Should we close walk-ins?” | Evidence may be shown; `requires_human_review=True` before any decision |

## Optional retrieval complement

Azure AI Search can retrieve policy or process documentation, but it is not part of this required
path. If used, cite its document provenance separately from the structured-data provenance and never
let policy-retrieval text expand the data allowlist.
