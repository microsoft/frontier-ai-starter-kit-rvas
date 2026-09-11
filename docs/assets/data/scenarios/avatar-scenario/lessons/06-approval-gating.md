# Module 6 — Gate publication behind human approval

A synthetic presenter makes a mistake more costly. It sounds confident, looks on-brand, and reaches
every new hire. Nothing publishes without **named human sign-off**. When a source changes, you can
**withdraw** the published content. This module implements the approval gate and proves that it
blocks.

![Publication approval gate](../diagrams/06-publication-gate.png)

## What you build

1. A versioned **approval record** that ties named people to the exact script id + version they
   signed.
2. A **gate** that blocks publishing until every required role approves *this* revision.
3. A **withdrawal path** that blocks publishing when you change approval status (for example, after
   a source change), even if all sign-offs exist.

The approval record template is
[`accelerator/sample-data/approvals.json`](../accelerator/sample-data/approvals.json), enforced by
[`content_pack.py`](../accelerator/content_pack.py).

## Choose your path

Where does the approval gate live and who enforces it?

| Option | Where approvals live | Enforcement | Build effort | Best when |
| --- | --- | --- | --- | --- |
| **A. Versioned approval record + renderer gate** *(default)* | JSON record versioned with the script | The renderer refuses unapproved/withdrawn packs | Low | You want a portable, auditable gate that travels with the artifact |
| B. Azure DevOps / GitHub environment approvals | Pipeline environment protection rules | Release pipeline blocks on required reviewers | Medium | Publishing is already a CI/CD release |
| C. Power Automate / Logic Apps approval flow | Approvals in M365/Teams | Flow gates the publish action | Medium | Approvers live in Teams and want native approvals |
| D. ITSM change request (ServiceNow etc.) | Change management system | Change ticket must be approved before publish | Higher | Regulated orgs requiring formal change control |

**Default: Option A.** The local validator checks a versioned demo record. It does not authenticate
reviewers or verify signatures. A publishing integration must bind approvals to immutable content
and remove withdrawn media from the serving channel. This module's Verify checks only local pack
rejection. Choose **B/C/D** when the customer's release, collaboration, or
change-control process must own sign-off. Keep the same **four required roles** and **withdrawal**
semantics.

**Migration cost.** A → B/C/D wraps the same record in a heavier workflow. The record and roles
survive. Do not drop the versioned record when you adopt a workflow tool. It is your audit trail.

## Implementation

### Option A — Versioned approval record + renderer gate (default)

**Require four named human approvals**, each tied to the exact revision. The renderer's
`REQUIRED_APPROVER_ROLES` is the contract: `SME`, `legal-compliance`, `brand-communications`,
`content-owner`.

```json
{
  "approval_record_id": "DEMO-APPROVAL-ONB-WELCOME-001-0.1.0",
  "script_id": "ONB-WELCOME-001",
  "script_version": "0.1.0",
  "approval_status": "approved-for-demo-only",
  "approvals": [
    { "role": "SME",                  "decision": "approved", "approver": "named-demo-sme",            "decided_at": "2026-07-05T09:00:00Z" },
    { "role": "legal-compliance",     "decision": "approved", "approver": "named-demo-legal-reviewer", "decided_at": "2026-07-05T09:10:00Z" },
    { "role": "brand-communications", "decision": "approved", "approver": "named-demo-brand-reviewer", "decided_at": "2026-07-05T09:20:00Z" },
    { "role": "content-owner",        "decision": "approved", "approver": "named-demo-content-owner",  "decided_at": "2026-07-05T09:30:00Z" }
  ]
}
```

Why these four for a synthetic onboarding experience:
- **SME** confirms the facts.
- **legal-compliance** confirms disclosure, consent, and regulated claims.
- **brand-communications** confirms the avatar, voice, and tone represent the organization
  acceptably.
- **content-owner** owns the published wording and its expiry.

The record must match the **exact** `script_id` + `script_version`. Approving 0.1.0 does not approve
0.2.0. Every revision needs re-approval. A small policy edit must trigger a fresh human decision.

**Implement withdrawal.** When module 3 reports a source change (a claim invalidated, past
`review_by`), flip the status and republish nothing:

```python
import json
from pathlib import Path
p = Path("scenarios/avatar-onboarding/accelerator/sample-data/approvals.json")
record = json.loads(p.read_text())
record["approval_status"] = "withdrawn"        # was: approved-for-demo-only
p.write_text(json.dumps(record, indent=2))
# The validator rejects future builds. The channel adapter must withdraw any served media.
```

### Option B — Pipeline environment approvals

Model publishing as a release to a protected environment with required reviewers. The pipeline reads
the approval record. An environment protection rule enforces the human gate before the publish step.
Keep the versioned record as the artifact reviewers approve.

### Option C — Power Automate / Logic Apps

Trigger an approval flow to the four roles in Teams. On full approval, it calls the publish action
(upload to `experience-output`, flip a "published" flag). Any rejection or later source change
triggers withdrawal. Approvers stay in their tools, while the record remains the audit trail.

### Option D — ITSM change control

Bind publishing to an approved change request. The avatar experience is a change, and its CR
references the approval record and artifact hash. Withdrawal is a follow-up change. Use this when
customer governance requires formal change management.

## Verify

A gate that never blocks proves nothing. Try to break this one, then confirm approval binds to the
exact revision. Check both against your records.

**1. Removing a required approval, or withdrawing the record, blocks publication.** Exercise the real
enforcement code against a working copy so you never mutate the signed record:

```bash
python3 - <<'PY'
import json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, "scenarios/avatar-onboarding/accelerator")
from content_pack import validate_pack, PackRejectedError

src = Path("scenarios/avatar-onboarding/accelerator/sample-data")
work = Path(tempfile.mkdtemp(prefix="verify-gate-"))/"pack"
shutil.rmtree(work, ignore_errors=True); shutil.copytree(src, work)

validate_pack(work); print("fully-approved pack: PUBLISHES")

appr = json.loads((work / "approvals.json").read_text())
appr["approvals"] = [a for a in appr["approvals"] if a["role"] != "legal-compliance"]
(work / "approvals.json").write_text(json.dumps(appr))
try:
    validate_pack(work); print("PROBLEM: published without legal-compliance")
except PackRejectedError as e:
    print("missing legal-compliance -> BLOCKED:", e)

shutil.copy(src / "approvals.json", work / "approvals.json")
appr = json.loads((work / "approvals.json").read_text())
appr["approval_status"] = "withdrawn"
(work / "approvals.json").write_text(json.dumps(appr))
try:
    validate_pack(work); print("PROBLEM: withdrawn pack still published")
except PackRejectedError as e:
    print("withdrawn status -> BLOCKED:", e)

shutil.rmtree(work, ignore_errors=True)
PY
```

Expected output: the full pack publishes, then the missing-role and withdrawn cases print
`BLOCKED`. If either prints `PROBLEM`, an unapproved or withdrawn synthetic likeness can reach new
hires. The gate must stop that.

**2. The approval is bound to this script id and version.** Approving `0.1.0` must not approve a later
edit:

```bash
jq -n \
  --slurpfile a scenarios/avatar-onboarding/accelerator/sample-data/approvals.json \
  --slurpfile s scenarios/avatar-onboarding/accelerator/sample-data/storyboard-script.json \
  '($a[0].script_id == $s[0].script_id) and ($a[0].script_version == $s[0].script_version)'
```

`true` means the sign-off matches the artifact being published. `false` means the record approves a
different revision, so a policy edit could ship without a fresh human decision. Re-approve every
revision.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Pack publishes with a missing role | Gate checks presence, not completeness | Enforce all four `REQUIRED_APPROVER_ROLES`; the check fails if any is absent |
| Old revision still publishes | Approval not bound to `script_version` | Match `script_id` + `script_version` exactly; re-approve every revision |
| Withdrawn content still served | Only future builds are blocked | Withdraw the served version through the channel adapter as well as changing `approval_status` |
| Approver name blank | Unattributed approval | Require a named `approver` and `decided_at` per row |
| Source changed, nobody notified | Missing invalidation wiring | Wire module 3's expiry/source-change to auto-withdraw |
| "Approved" but no audit trail | Approval outside the versioned record | Keep the versioned record even with a workflow tool (B/C/D) |

## Next module

[Module 7 — Evaluate, red-team, trace, and operate](07-prove-and-operate.md) proves the experience is
safe and useful, then makes the controlled release decision.
