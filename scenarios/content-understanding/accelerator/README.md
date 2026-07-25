# Content Understanding accelerator

This accelerator has two parts: a synthetic local workflow pack for workshop validation and an
optional Bicep foundation for a clean Azure demo subscription. It is not a landing zone and it is
not production approval.

## Use it in the workshop

1. Copy `parameters.example.json` and replace only the placeholders with approved planning references. Never add keys, endpoints, or customer data.
2. Review the output with the platform, security, data, and workflow owners.
3. Record the three decisions emitted by the accelerator: current service support, approved environment/access model, and evaluation/review requirements.
4. Use the safe fixtures in `sample-data/` for the local exercise. No Azure service, SDK, endpoint, or secret is involved.

## Before any implementation

Verify the current Content Understanding setup, supported formats, regional availability, identity
model, and invocation surface in current Microsoft documentation. Then decide whether to use the
optional Bicep foundation, an existing customer environment, or a different approved deployment
pattern.

Use the scenario validator (`python3 validate.py`) to check the synthetic pack and expected structured results.
