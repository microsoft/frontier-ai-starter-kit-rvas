// Intentionally resource-free: this workshop template records a deployment choice
// without creating or altering a customer landing zone, source, or knowledge index.
targetScope = 'subscription'

@allowed([
  'clean-subscription-demo'
  'byo-existing-environment'
])
param deploymentMode string

@description('Approved Azure region for the deployment record.')
param location string

@description('Optional existing resource ID for the BYO path. No resource is read or changed.')
param existingEnvironmentResourceId string = ''

@description('Human-readable, non-deployed label for the proposed context pattern.')
param contextPattern string = 'decision-pending'

output selectedDeploymentMode string = deploymentMode
output approvedLocation string = location
output existingEnvironmentReference string = existingEnvironmentResourceId
output selectedContextPattern string = contextPattern
output implementationGate string = 'Search current Microsoft documentation and verify supported APIs before adding resources.'
