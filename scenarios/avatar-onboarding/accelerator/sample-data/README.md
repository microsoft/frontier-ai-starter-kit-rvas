# Fictional approved-content pack

This complete, non-production fixture is deliberately synthetic. It contains no employee data,
customer policy, vendor integration, credentials, or real-person likeness. Keep this repository
fictional. Use a separate, approved location for customer content and retain the traceability fields.

| File | Purpose |
| --- | --- |
| `claims.json` | Atomic approved claims, source references, owners, review dates, and help paths. |
| `approvals.json` | Recorded demo approvals and publication conditions. |
| `storyboard-script.json` | Versioned spoken script, scenes, claim links, disclosure, and accessibility requirements. |
| `transcript.txt` | Caption/transcript equivalent for the approved script. |
| `accessible-fallback.html` | Semantic, keyboard-friendly non-avatar alternative. |
| `feedback-fixture.json` | Aggregated synthetic pilot evidence, without identifiers. |

`../content_pack.py` accepts this pack only when every script segment exactly matches its linked
approved claim and all required demo approval rows are present. `build_artifact` returns a
deterministic, traceable dictionary. The caller must serialize it if a JSON file is needed.
The approval record ID, publication ID, and locale must be non-empty text. The module does not
render media or call a service.
