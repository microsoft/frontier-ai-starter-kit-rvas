targetScope = 'resourceGroup'

@description('Human-readable identifier for the planned Content Understanding demonstration.')
param demonstrationName string = 'content-understanding-safe-demo'

@description('Target region to verify with current service documentation; this template does not deploy to it.')
param plannedLocation string = '<supported-region>'

@description('Approved reference to the environment selected by the platform team. Do not include keys or secrets.')
param environmentReference string = '<approved-environment-reference>'

@description('Repository-relative path to the safe local fixture pack used for the facilitated exercise.')
param fixturePackPath string = '../sample-data'

@description('Whether a human review queue is required for the proposed workflow.')
param requiresHumanReview bool = true

@description('Project role that must approve use of any non-synthetic document.')
param dataApprovalOwner string = '<data-approval-owner>'

var blueprint = {
  purpose: 'Plan a safe Content Understanding demonstration without creating or reading Azure resources.'
  demonstrationName: demonstrationName
  plannedLocation: plannedLocation
  environmentReference: environmentReference
  fixturePackPath: fixturePackPath
  requiresHumanReview: requiresHumanReview
  dataApprovalOwner: dataApprovalOwner
  decisionsRequired: [
    'Confirm current regional availability and supported service setup from Microsoft documentation.'
    'Confirm the approved environment, workload identity, access controls, and retention approach.'
    'Confirm the SME schema, expected outcomes, review policy, and promotion evidence.'
  ]
}

output implementationBlueprint object = blueprint
output templateMode string = 'blueprint-only-no-resources'
