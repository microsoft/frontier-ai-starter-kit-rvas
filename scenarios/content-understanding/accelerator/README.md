# Content Understanding blueprint

`main.bicep` is intentionally **blueprint-only**. It declares no Azure resources and never references an existing resource. A what-if returns the planning object; a deployment also leaves an Azure Resource Manager deployment-history record. It is not provisioning guidance.

## Use it in the workshop

1. Copy `parameters.example.json` and replace only the placeholders with approved planning references. Never add keys, endpoints, or customer data.
2. Review the output with the platform, security, data, and workflow owners.
3. Record the three decisions emitted by the blueprint: current service support, approved environment/access model, and evaluation/review requirements.
4. Use the safe fixtures in `sample-data/` for the local exercise. No Azure service, SDK, endpoint, or secret is involved.

## Before any implementation

Verify the current Content Understanding setup, supported formats, regional availability, identity model, and invocation surface in current Microsoft documentation. Then create a separate, reviewed implementation design. This folder intentionally makes no claim about the required Azure resource type, analyzer API, or portable Studio export behavior.

Use the scenario's [local demo runbook](../LOCAL_DEMO.md) to validate the synthetic pack and expected structured results.
