// ============================================================================
// AI Grounding scenario — deployable grounding footprint.
//
// Provisions the resources a grounded, permission-aware assistant needs:
//   • Microsoft Foundry account (Cognitive Services kind=AIServices) + project
//   • A chat deployment (answering + agentic query planning)
//   • An embedding deployment (vector/hybrid retrieval)
//   • Azure AI Search with semantic ranking (knowledge base / agentic retrieval backend)
//   • Storage account + container (blob knowledge source for approved content)
//   • Log Analytics + Application Insights (tracing and evaluation correlation)
//   • Project connections to AI Search and Application Insights
//   • Keyless RBAC wiring between the identities that must talk to each other
//
// Resource types and API versions mirror the kit's azd-deployed infra/resources.bicep.
// No secrets are declared here: authentication is managed identity + RBAC.
// ============================================================================
targetScope = 'resourceGroup'

@description('Region for all resources. Must support Foundry, agentic retrieval, and your chosen models.')
param location string = resourceGroup().location

@description('Tags applied to every resource.')
param tags object = {}

@minLength(5)
@maxLength(12)
@description('Unique token used to name globally-unique resources.')
param resourceToken string

@description('Optional human principal objectId so an engineer can use the data planes keylessly. Empty in CI.')
param principalId string = ''

@description('Chat model used for answering and for agentic query planning.')
param chatModelName string = 'gpt-4.1-mini'

@description('Chat model version. Empty means "let the platform pick the default".')
param chatModelVersion string = ''

param chatModelDeploymentName string = 'chat'
param chatModelSkuName string = 'GlobalStandard'
param chatModelCapacity int = 30

@description('Embedding model used to vectorize approved content.')
param embeddingModelName string = 'text-embedding-3-large'
param embeddingModelVersion string = ''
param embeddingModelDeploymentName string = 'embedding'
param embeddingModelSkuName string = 'Standard'
param embeddingModelCapacity int = 30

@description('Azure AI Search tier. Basic or higher is required to use a managed identity for model access.')
@allowed([
  'basic'
  'standard'
  'standard2'
])
param searchSku string = 'basic'

@description('Blob container that holds the approved corpus for the blob knowledge source.')
param approvedContentContainerName string = 'approved-content'

// Built-in role definition IDs (subscription-scoped resourceIds).
var roleCognitiveServicesUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908')
var roleCognitiveServicesOpenAIUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
var roleSearchIndexDataContributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '8ebe5a00-799e-43f5-93ac-243d3dce84a7')
var roleSearchServiceContributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7ca78c08-252a-4471-8644-bb5ff32d4ba0')
var roleStorageBlobDataReader = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1')
var roleStorageBlobDataContributor = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')

// ---------------------------------------------------------------------------
// Observability
// ---------------------------------------------------------------------------
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
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
// Approved-content storage (source for a blob knowledge source)
// ---------------------------------------------------------------------------
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'st${resourceToken}'
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    // Keyless-first: shared key access is disabled so ingestion must use Entra ID.
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource approvedContent 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: approvedContentContainerName
  properties: {
    publicAccess: 'None'
  }
}

// ---------------------------------------------------------------------------
// Azure AI Search — knowledge base / agentic retrieval backend
// ---------------------------------------------------------------------------
resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: 'srch-${resourceToken}'
  location: location
  tags: tags
  sku: { name: searchSku }
  identity: { type: 'SystemAssigned' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    semanticSearch: 'standard'
    authOptions: { aadOrApiKey: { aadAuthFailureMode: 'http401WithBearerChallenge' } }
    disableLocalAuth: false
  }
}

// ---------------------------------------------------------------------------
// Microsoft Foundry account + project
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
      ...empty(chatModelVersion) ? {} : {
        version: chatModelVersion
      }
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
    raiPolicyName: 'Microsoft.DefaultV2'
  }
}

// Deployments must be created serially on the same account.
resource embeddingDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-04-01-preview' = {
  parent: foundry
  name: embeddingModelDeploymentName
  dependsOn: [chatDeployment]
  sku: {
    name: embeddingModelSkuName
    capacity: embeddingModelCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      ...empty(embeddingModelVersion) ? {} : {
        version: embeddingModelVersion
      }
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: foundry
  name: 'proj-${resourceToken}'
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    displayName: 'AI Grounding pilot'
    description: 'Grounded, permission-aware assistant for one bounded customer decision.'
  }
}

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
// RBAC — keyless wiring
// ---------------------------------------------------------------------------
// Search calls the embedding/chat models for ingestion and query planning.
resource searchToFoundryRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, search.id, roleCognitiveServicesUser)
  scope: foundry
  properties: {
    principalId: search.identity.principalId
    roleDefinitionId: roleCognitiveServicesUser
    principalType: 'ServicePrincipal'
  }
}

// Search indexers read approved content from blob storage.
resource searchToStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, search.id, roleStorageBlobDataReader)
  scope: storage
  properties: {
    principalId: search.identity.principalId
    roleDefinitionId: roleStorageBlobDataReader
    principalType: 'ServicePrincipal'
  }
}

// The project queries the knowledge base / index.
resource projectSearchDataRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roleSearchIndexDataContributor)
  scope: search
  properties: {
    principalId: project.identity.principalId
    roleDefinitionId: roleSearchIndexDataContributor
    principalType: 'ServicePrincipal'
  }
}

resource projectSearchServiceRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(search.id, project.id, roleSearchServiceContributor)
  scope: search
  properties: {
    principalId: project.identity.principalId
    roleDefinitionId: roleSearchServiceContributor
    principalType: 'ServicePrincipal'
  }
}

// Optional: the engineer running the lessons locally, keylessly.
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

resource userStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(storage.id, principalId, roleStorageBlobDataContributor)
  scope: storage
  properties: {
    principalId: principalId
    roleDefinitionId: roleStorageBlobDataContributor
    principalType: 'User'
  }
}

// ---------------------------------------------------------------------------
// Outputs — these become the .env contract used by every later lesson.
// ---------------------------------------------------------------------------
output AZURE_AI_PROJECT_ENDPOINT string = 'https://${foundry.name}.services.ai.azure.com/api/projects/${project.name}'
output AZURE_AI_FOUNDRY_ENDPOINT string = 'https://${foundry.name}.services.ai.azure.com'
output AZURE_AI_FOUNDRY_ACCOUNT_NAME string = foundry.name
output AZURE_AI_PROJECT_NAME string = project.name
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = chatModelDeploymentName
output AZURE_AI_EMBEDDING_DEPLOYMENT_NAME string = embeddingModelDeploymentName
output AZURE_AI_CHAT_MODEL_NAME string = chatModelName
output AZURE_AI_EMBEDDING_MODEL_NAME string = embeddingModelName
output AZURE_SEARCH_ENDPOINT string = 'https://${search.name}.search.windows.net'
output AZURE_SEARCH_SERVICE_NAME string = search.name
output AZURE_SEARCH_CONNECTION_NAME string = searchConnection.name
output AZURE_STORAGE_ACCOUNT_NAME string = storage.name
output AZURE_STORAGE_CONTAINER_NAME string = approvedContentContainerName
output APPLICATIONINSIGHTS_RESOURCE_ID string = appInsights.id
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_LOCATION string = location
