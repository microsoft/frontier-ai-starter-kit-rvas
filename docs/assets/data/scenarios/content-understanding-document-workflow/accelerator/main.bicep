// ============================================================================
// Content Understanding scenario — deployable document-workflow footprint.
//
// Provisions the resources a reviewable, keyless document-extraction workflow needs:
//   • Microsoft Foundry account (Cognitive Services kind=AIServices) + project.
//     This same account hosts the Content Understanding and Document Intelligence
//     Foundry Tools and your Azure OpenAI model deployments.
//   • A chat/generative deployment (Content Understanding generative fields, LLM
//     structured outputs) and an embedding deployment (Content Understanding
//     custom analyzers / knowledge sources).
//   • Storage account with an inbound container (approved document source) and a
//     quarantine container (documents that fail intake controls).
//   • Log Analytics + Application Insights (workflow tracing and evaluation).
//   • Project connection to Application Insights.
//   • Keyless RBAC wiring: the account managed identity reads documents from blob,
//     and the signed-in engineer gets keyless data-plane access.
//
// Resource types and API versions mirror the kit's azd-deployed infra/resources.bicep.
// No secrets are declared here: authentication is managed identity + Entra ID RBAC.
// ============================================================================
targetScope = 'resourceGroup'

@description('Region for all resources. Must support Foundry, Content Understanding, Document Intelligence, and your chosen models.')
param location string = resourceGroup().location

@description('Tags applied to every resource.')
param tags object = {}

@minLength(5)
@maxLength(12)
@description('Unique token used to name globally-unique resources.')
param resourceToken string

@description('Optional human principal objectId so an engineer can use the data planes keylessly. Empty in CI.')
param principalId string = ''

@description('Generative model used for Content Understanding generative/classify fields and LLM structured outputs.')
param chatModelName string = 'gpt-4.1-mini'

@description('Chat model version. Empty means "let the platform pick the default".')
param chatModelVersion string = ''

param chatModelDeploymentName string = 'chat'
param chatModelSkuName string = 'GlobalStandard'
param chatModelCapacity int = 30

@description('Embedding model used by Content Understanding custom analyzers and knowledge sources.')
param embeddingModelName string = 'text-embedding-3-large'
param embeddingModelVersion string = ''
param embeddingModelDeploymentName string = 'embedding'
param embeddingModelSkuName string = 'Standard'
param embeddingModelCapacity int = 30

@description('Blob container that receives approved, in-scope documents for extraction.')
param inboundContainerName string = 'documents-inbound'

@description('Blob container that isolates documents which fail intake controls (unapproved, wrong type, oversize).')
param quarantineContainerName string = 'documents-quarantine'

// Built-in role definition IDs (subscription-scoped resourceIds).
var roleCognitiveServicesUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908')
var roleCognitiveServicesOpenAIUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
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
// Document storage — inbound source + quarantine
// ---------------------------------------------------------------------------
resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'st${resourceToken}'
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    // Keyless-first: shared key access is disabled so intake must use Entra ID.
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

resource inboundContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: inboundContainerName
  properties: {
    publicAccess: 'None'
  }
}

resource quarantineContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: quarantineContainerName
  properties: {
    publicAccess: 'None'
  }
}

// ---------------------------------------------------------------------------
// Microsoft Foundry account + project (hosts Content Understanding, Document
// Intelligence, and the model deployments)
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
    displayName: 'Content Understanding document workflow'
    description: 'Reviewable, evidence-backed document extraction for one bounded decision.'
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

// ---------------------------------------------------------------------------
// RBAC — keyless wiring
// ---------------------------------------------------------------------------
// The Foundry account reads inbound documents from blob when analyzing by URL.
resource foundryToStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, foundry.id, roleStorageBlobDataReader)
  scope: storage
  properties: {
    principalId: foundry.identity.principalId
    roleDefinitionId: roleStorageBlobDataReader
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
// Outputs — these become the .env contract used by every later module.
// ---------------------------------------------------------------------------
output AZURE_AI_PROJECT_ENDPOINT string = 'https://${foundry.name}.services.ai.azure.com/api/projects/${project.name}'
output AZURE_AI_FOUNDRY_ENDPOINT string = 'https://${foundry.name}.services.ai.azure.com'
output AZURE_AI_SERVICES_ENDPOINT string = foundry.properties.endpoint
output AZURE_CONTENT_UNDERSTANDING_ENDPOINT string = foundry.properties.endpoint
output AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT string = foundry.properties.endpoint
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = chatModelDeploymentName
output AZURE_AI_EMBEDDING_DEPLOYMENT_NAME string = embeddingModelDeploymentName
output AZURE_AI_CHAT_MODEL_NAME string = chatModelName
output AZURE_AI_EMBEDDING_MODEL_NAME string = embeddingModelName
output AZURE_STORAGE_ACCOUNT_NAME string = storage.name
output AZURE_DOCUMENTS_CONTAINER_NAME string = inboundContainerName
output AZURE_QUARANTINE_CONTAINER_NAME string = quarantineContainerName
output APPLICATIONINSIGHTS_RESOURCE_ID string = appInsights.id
