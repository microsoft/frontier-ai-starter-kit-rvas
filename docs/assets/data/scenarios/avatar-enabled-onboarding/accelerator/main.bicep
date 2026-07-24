// ============================================================================
// Avatar-enabled Onboarding scenario — deployable experience footprint.
//
// Provisions the resources a governed, avatar-led onboarding experience needs:
//   • Microsoft Foundry account (Cognitive Services kind=AIServices) + project.
//     The AIServices account also fronts Azure AI Speech (text-to-speech avatar
//     batch/real-time, Voice Live) — a custom subdomain is set so the Speech data
//     plane accepts Microsoft Entra tokens (keyless).
//   • A chat deployment (grounded drafting + help) and an embedding deployment
//     (vectorising approved HR/onboarding content for the knowledge base).
//   • Azure AI Search with semantic ranking (grounded assistant knowledge base).
//   • Storage: an approved-content container (governed source pipeline) and an
//     experience-output container (rendered avatar videos / transcripts).
//   • Log Analytics + Application Insights (tracing + evaluation correlation).
//   • Project connections to AI Search and Application Insights.
//   • Keyless RBAC wiring, including the Speech data-plane role.
//
// Resource types and API versions mirror the kit's azd-deployed infra/resources.bicep.
// No secrets are declared here: authentication is managed identity + RBAC.
// Avatar, Voice Live, and custom-voice features are region-gated — deploy into a
// region that supports them (see the scenario lessons for the verified region check).
// ============================================================================
targetScope = 'resourceGroup'

@description('Region for all resources. Must support Foundry, Azure AI Search, and the chosen Speech avatar/Voice Live capability.')
param location string = resourceGroup().location

@description('Tags applied to every resource.')
param tags object = {}

@minLength(5)
@maxLength(12)
@description('Unique token used to name globally-unique resources.')
param resourceToken string

@description('Optional human principal objectId so an engineer can use the data planes keylessly. Empty in CI.')
param principalId string = ''

@description('Chat model used for grounded drafting and help.')
param chatModelName string = 'gpt-4.1-mini'

@description('Chat model version. Empty means "let the platform pick the default".')
param chatModelVersion string = ''

param chatModelDeploymentName string = 'chat'
param chatModelSkuName string = 'GlobalStandard'
param chatModelCapacity int = 30

@description('Embedding model used to vectorise approved onboarding content.')
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

@description('Blob container that holds the approved onboarding corpus for the knowledge base.')
param approvedContentContainerName string = 'approved-content'

@description('Blob container that holds rendered avatar experience output (video, transcript, captions).')
param experienceOutputContainerName string = 'experience-output'

// Built-in role definition IDs (subscription-scoped resourceIds).
var roleCognitiveServicesUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908')
var roleCognitiveServicesOpenAIUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
// Cognitive Services Speech User — Speech is data-plane heavy; the generic contributor roles grant no Speech access.
var roleCognitiveServicesSpeechUser = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'f2dc8367-1007-4938-bd23-fe263f013447')
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
// Storage — approved source content + rendered experience output
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

resource experienceOutput 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: experienceOutputContainerName
  properties: {
    publicAccess: 'None'
  }
}

// ---------------------------------------------------------------------------
// Azure AI Search — grounded assistant knowledge base
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
// Microsoft Foundry account (+ Speech data plane) + project
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
    // A custom subdomain is required for Microsoft Entra token auth on the Speech data plane.
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
    displayName: 'Avatar-enabled onboarding pilot'
    description: 'Governed, accessible avatar-led onboarding grounded in approved content with human approval.'
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

// Search indexers read approved onboarding content from blob storage.
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

// The project writes rendered experience output to blob storage.
resource projectStorageRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, project.id, roleStorageBlobDataContributor)
  scope: storage
  properties: {
    principalId: project.identity.principalId
    roleDefinitionId: roleStorageBlobDataContributor
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

// Speech data plane (avatar batch/real-time synthesis, Voice Live) for the engineer, keylessly.
resource userSpeechRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(foundry.id, principalId, roleCognitiveServicesSpeechUser)
  scope: foundry
  properties: {
    principalId: principalId
    roleDefinitionId: roleCognitiveServicesSpeechUser
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
output AZURE_AI_MODEL_DEPLOYMENT_NAME string = chatModelDeploymentName
output AZURE_AI_EMBEDDING_DEPLOYMENT_NAME string = embeddingModelDeploymentName
output AZURE_AI_CHAT_MODEL_NAME string = chatModelName
output AZURE_AI_EMBEDDING_MODEL_NAME string = embeddingModelName
output AZURE_SPEECH_RESOURCE_ID string = foundry.id
output AZURE_SPEECH_ENDPOINT string = 'https://${foundry.name}.cognitiveservices.azure.com'
output AZURE_SPEECH_REGION string = location
output AZURE_SEARCH_ENDPOINT string = 'https://${search.name}.search.windows.net'
output AZURE_SEARCH_CONNECTION_NAME string = searchConnection.name
output AZURE_STORAGE_ACCOUNT_NAME string = storage.name
output AZURE_STORAGE_CONTAINER_NAME string = approvedContentContainerName
output AZURE_EXPERIENCE_OUTPUT_CONTAINER_NAME string = experienceOutputContainerName
output APPLICATIONINSIGHTS_RESOURCE_ID string = appInsights.id
