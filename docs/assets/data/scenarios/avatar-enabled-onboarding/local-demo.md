# Local demo

This demo is local, deterministic, and dependency-free. It uses only fictional content and writes JSON; it does not generate media, contact a service, or use a vendor SDK.

From `scenarios/avatar-onboarding`:

```bash
python3 validate.py
python3 accelerator/mock_renderer.py \
  --data-dir accelerator/sample-data \
  --output-dir accelerator/demo-artifacts
python3 -m json.tool accelerator/demo-artifacts/mock-rendered-onboarding.json
```

Open `accelerator/sample-data/accessible-fallback.html` in a browser to demonstrate the non-avatar experience. Read `transcript.txt` as the captions/transcript equivalent.

The artifact contains the publication and approval IDs, every rendered segment's claim and source link, required accessibility files, and SHA-256 hashes of the consumed fixture files. Re-running the command with unchanged inputs produces byte-identical JSON.

To demonstrate the control boundary, change a `spoken_text` value or remove an approval in a copy of the fixture, then run the renderer against that copy. It exits nonzero and writes no artifact. Do not edit the canonical sample fixture for that demonstration.

Remove generated output when finished:

```bash
rm -rf accelerator/demo-artifacts
```
