// ============================================================================
// AI Starter Kit — Microsoft Foundry golden-path infrastructure (azd entry).
//
// Subscription-scoped entry point. Creates (or reuses) the resource group, then
// delegates all resource creation to ./resources.bicep. Outputs are surfaced back
// to the azd environment and become the .env contract (see .env.sample).
//
// Deploy:   azd up
// Fallback: ./scripts/deploy.sh   (Bash, for quota/region edge cases)
// ============================================================================
targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the azd environment — used to derive a unique resource token.')
param environmentName string

@minLength(1)
@description('Primary region for all resources. Pick a region with Foundry + model quota.')
@allowed([
  'eastus'
  'eastus2'
  'westus'
  'westus3'
  'northcentralus'
  'southcentralus'
  'swedencentral'
  'westeurope'
  'francecentral'
  'uksouth'
  'australiaeast'
])
param location string = 'swedencentral'

@description('Optional principal (user/SP objectId) to grant data-plane roles for keyless local dev. Leave empty in CI.')
param principalId string = ''

@description('Chat model to deploy in Foundry (model catalog name).')
param chatModelName string = 'gpt-4o'

@description('Chat model version. Leave empty to let Foundry pick the default for the model.')
param chatModelVersion string = '2024-11-20'

@description('Deployment (alias) name the agent + SDK reference. Becomes AZURE_AI_MODEL_DEPLOYMENT_NAME.')
param chatModelDeploymentName string = 'gpt-4o'

@description('Model deployment SKU/capacity tier.')
param chatModelSkuName string = 'GlobalStandard'

@description('Model deployment capacity (in thousands of TPM units).')
param chatModelCapacity int = 30

// Derive a stable-but-unique token from the subscription + environment name.
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = {
  'azd-env-name': environmentName
  project: 'ai-starter-kit-rvas-foundry'
}

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module resources 'resources.bicep' = {
  name: 'resources'
  scope: rg
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
    principalId: principalId
    chatModelName: chatModelName
    chatModelVersion: chatModelVersion
    chatModelDeploymentName: chatModelDeploymentName
    chatModelSkuName: chatModelSkuName
    chatModelCapacity: chatModelCapacity
  }
}

// --------------------------------------------------------------------------
// Outputs — captured by azd into the environment. Export with:
//   azd env get-values > .env
// Names intentionally match the .env contract in .env.sample.
// --------------------------------------------------------------------------
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name

output AZURE_AI_FOUNDRY_ENDPOINT string = resources.outputs.AZURE_AI_FOUNDRY_ENDPOINT
output AZURE_AI_PROJECT_ENDPOINT string = resources.outputs.AZURE_AI_PROJECT_ENDPOINT
output AZURE_AI_PROJECT_NAME string = resources.outputs.AZURE_AI_PROJECT_NAME
output AZURE_OPENAI_ENDPOINT string = resources.outputs.AZURE_AI_FOUNDRY_ENDPOINT
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = resources.outputs.AZURE_AI_MODEL_DEPLOYMENT_NAME
output AZURE_AI_MODEL_NAME string = resources.outputs.AZURE_AI_MODEL_NAME
output AZURE_AI_API_VERSION string = resources.outputs.AZURE_AI_API_VERSION

output AZURE_SEARCH_ENDPOINT string = resources.outputs.AZURE_SEARCH_ENDPOINT
output AZURE_SEARCH_INDEX_NAME string = resources.outputs.AZURE_SEARCH_INDEX_NAME
output AZURE_SEARCH_CONNECTION_NAME string = resources.outputs.AZURE_SEARCH_CONNECTION_NAME

output APPLICATIONINSIGHTS_CONNECTION_STRING string = resources.outputs.APPLICATIONINSIGHTS_CONNECTION_STRING
output AZURE_LOG_ANALYTICS_WORKSPACE_ID string = resources.outputs.AZURE_LOG_ANALYTICS_WORKSPACE_ID

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.AZURE_CONTAINER_REGISTRY_ENDPOINT
output AZURE_CONTAINER_REGISTRY_NAME string = resources.outputs.AZURE_CONTAINER_REGISTRY_NAME

// GenAI tracing flags — consumed by the Tracing & Observability activity.
output AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING string = 'true'
output OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT string = 'true'
