# Fictional approved-content pack

This complete, non-production fixture is deliberately synthetic. It has no employee data, customer policy, vendor integration, credentials, or real-person likeness. Replace every value only with customer-approved content and retain the traceability fields. A generated summary is never an authority for policy.

| File | Purpose |
| --- | --- |
| `claims.json` | Atomic approved claims, source references, owners, review dates, and help paths. |
| `approvals.json` | Recorded demo approvals and publication conditions. |
| `storyboard-script.json` | Versioned spoken script, scenes, claim links, disclosure, and accessibility requirements. |
| `transcript.txt` | Caption/transcript equivalent for the approved script. |
| `accessible-fallback.html` | Semantic, keyboard-friendly non-avatar alternative. |
| `feedback-fixture.json` | Aggregated synthetic pilot evidence, without identifiers. |

`../mock_renderer.py` accepts this pack only when every script segment exactly matches its linked approved claim and all required human approvals are present. It writes a deterministic traceable JSON artifact; it does not render media or call a service.
