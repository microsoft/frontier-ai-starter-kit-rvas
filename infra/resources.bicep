// ============================================================================
// AI Starter Kit — resource-group-scoped resources for the Foundry footprint.
//
// Provisions, keyless-by-default (managed identity + RBAC):
//   • Microsoft Foundry resource (Cognitive Services kind=AIServices, project mgmt on)
//   • A Foundry project (child of the account)
//   • A chat model deployment
//   • Azure AI Search (for the knowledge-base index)
//   • Log Analytics workspace + Application Insights (observability/tracing)
//   • Azure Container Registry (for hosted-agent containers)
//   • Foundry project connections to AI Search + App Insights
//   • RBAC: project MI -> Search data/control plane; optional human principal -> data planes
// ============================================================================
@description('Region for all resources.')
param location string

@description('Tags applied to every resource.')
param tags object

@description('Unique token used to name globally-unique resources.')
param resourceToken string

@description('Optional human principal objectId for keyless local dev. Empty in CI.')
param principalId string = ''

param chatModelName string
param chatModelVersion string
param chatModelDeploymentName string
param chatModelSkuName string
param chatModelCapacity int

@description('Name of the AI Search index the knowledge base will use.')
param searchIndexName string = 'university-faq'

// Built-in role definition IDs (subscription-scoped resourceIds).
var roleCognitiveServicesUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908')
var roleCognitiveServicesOpenAIUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
var roleSearchIndexDataContributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '8ebe5a00-799e-43f5-93ac-243d3dce84a7')
var roleSearchServiceContributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7ca78c08-252a-4471-8644-bb5ff32d4ba0')
var roleAcrPush = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '8311e382-0749-4cb8-b61a-304f252e45ec')

// ---------------------------------------------------------------------------
// Log Analytics + Application Insights
// ---------------------------------------------------------------------------
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
    features: { searchVersion: 1 }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${resourceToken}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    IngestionMode: 'LogAnalytics'
  }
}

// ---------------------------------------------------------------------------
// Azure AI Search — knowledge-base index backend
// ---------------------------------------------------------------------------
resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: 'srch-${resourceToken}'
  location: location
  tags: tags
  sku: { name: 'basic' }
  identity: { type: 'SystemAssigned' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    semanticSearch: 'standard'
    // Keyless-first: prefer RBAC, but keep key auth available as a fallback for the workshop.
    authOptions: { aadOrApiKey: { aadAuthFailureMode: 'http401WithBearerActivity' } }
    disableLocalAuth: false
  }
}

// ---------------------------------------------------------------------------
// Azure Container Registry — hosted-agent containers
// ---------------------------------------------------------------------------
resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: 'acr${resourceToken}'
  location: location
  tags: tags
  sku: { name: 'Basic' }
  properties: {
    adminUserEnabled: false
  }
}

// ---------------------------------------------------------------------------
// Microsoft Foundry resource (Cognitive Services, kind = AIServices)
// allowProjectManagement: true is what makes this a *Foundry* account.
// ---------------------------------------------------------------------------
resource foundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: 'aif-${resourceToken}'
  location: location
  tags: tags
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    allowProjectManagement: true
    customSubDomainName: 'aif-${resourceToken}'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

// Chat model deployment.
resource chatDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview' = {
  parent: foundry
  name: chatModelDeploymentName
  sku: {
    name: chatModelSkuName
    capacity: chatModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: chatModelName
      version: empty(chatModelVersion) ? null : chatModelVersion
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}

// Foundry project (child of the account).
resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: foundry
  name: 'proj-${resourceToken}'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    displayName: 'Northfield IQ Assistant'
    description: 'AI Starter Kit — Northfield University IQ Assistant project.'
  }
}

// Project connection: Application Insights (enables tracing/eval correlation).
resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-04-01-preview' = {
  parent: project
  name: 'appinsights'
  properties: {
    category: 'AppInsights'
    target: appInsights.id
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: {
      key: appInsights.properties.ConnectionString
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: appInsights.id
    }
  }
}

// Project connection: Azure AI Search (keyless — uses the project managed identity).
resource searchConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-04-01-preview' = {
  parent: project
  name: 'search'
  properties: {
    category: 'CognitiveSearch'
    target: 'https://${search.name}.search.windows.net'
    authType: 'AAD'
    isSharedToAll: true
    metadata: {
      ApiType: 'Azure'
      ResourceId: search.id
      Location: location
    }
  }
}

// ---------------------------------------------------------------------------
// RBAC — project managed identity gets data/control plane on AI Search (keyless).
// ---------------------------------------------------------------------------
resource projSearchDataRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roleSearchIndexDataContributor)
  scope: search
  properties: {
    principalId: project.identity.principalId
    roleDefinitionId: roleSearchIndexDataContributor
    principalType: 'ServicePrincipal'
  }
}

resource projSearchServiceRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roleSearchServiceContributor)
  scope: search
  properties: {
    principalId: project.identity.principalId
    roleDefinitionId: roleSearchServiceContributor
    principalType: 'ServicePrincipal'
  }
}

// Search MI needs to read embeddings from Foundry (integrated vectorization / agentic retrieval).
resource searchOpenAIRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, search.id, roleCognitiveServicesOpenAIUser)
  scope: foundry
  properties: {
    principalId: search.identity.principalId
    roleDefinitionId: roleCognitiveServicesOpenAIUser
    principalType: 'ServicePrincipal'
  }
}

// ---------------------------------------------------------------------------
// RBAC — optional human principal (keyless local dev). Skipped when principalId is empty.
// ---------------------------------------------------------------------------
resource userFoundryRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(foundry.id, principalId, roleCognitiveServicesUser)
  scope: foundry
  properties: {
    principalId: principalId
    roleDefinitionId: roleCognitiveServicesUser
    principalType: 'User'
  }
}

resource userOpenAIRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(foundry.id, principalId, roleCognitiveServicesOpenAIUser)
  scope: foundry
  properties: {
    principalId: principalId
    roleDefinitionId: roleCognitiveServicesOpenAIUser
    principalType: 'User'
  }
}

resource userSearchDataRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(search.id, principalId, roleSearchIndexDataContributor)
  scope: search
  properties: {
    principalId: principalId
    roleDefinitionId: roleSearchIndexDataContributor
    principalType: 'User'
  }
}

resource userSearchServiceRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(search.id, principalId, roleSearchServiceContributor)
  scope: search
  properties: {
    principalId: principalId
    roleDefinitionId: roleSearchServiceContributor
    principalType: 'User'
  }
}

resource userAcrPushRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(acr.id, principalId, roleAcrPush)
  scope: acr
  properties: {
    principalId: principalId
    roleDefinitionId: roleAcrPush
    principalType: 'User'
  }
}

// --------------------------------------------------------------------------
// Outputs
// --------------------------------------------------------------------------
output AZURE_AI_FOUNDRY_ENDPOINT string = foundry.properties.endpoint
output AZURE_AI_PROJECT_ENDPOINT string = 'https://${foundry.name}.services.ai.azure.com/api/projects/${project.name}'
output AZURE_AI_PROJECT_NAME string = project.name
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = chatModelDeploymentName
output AZURE_AI_MODEL_NAME string = chatModelName
output AZURE_AI_API_VERSION string = '2025-04-01-preview'

output AZURE_SEARCH_ENDPOINT string = 'https://${search.name}.search.windows.net'
output AZURE_SEARCH_INDEX_NAME string = searchIndexName
output AZURE_SEARCH_CONNECTION_NAME string = searchConnection.name

output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.properties.ConnectionString
output AZURE_LOG_ANALYTICS_WORKSPACE_ID string = logAnalytics.id

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = acr.properties.loginServer
output AZURE_CONTAINER_REGISTRY_NAME string = acr.name
