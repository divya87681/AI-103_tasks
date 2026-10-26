targetScope = 'resourceGroup'

@description('Deployment location')
param location string = resourceGroup().location

@description('Unique prefix for training resources')
@minLength(3)
@maxLength(20)
param prefix string = 'ai103training'

@description('Select the service to configure')
@allowed([
  'Translator'
  'Language'
  'CustomVisionTraining'
  'CustomVisionPrediction'
  'Vision'
  'PostgreSQL'
])
param serviceKind string = 'Translator'

@description('Azure AI Translator pricing tier')
@allowed([
  'F0'
  'S1'
])
param translatorSku string = 'F0'

@description('Azure AI Language pricing tier')
@allowed([
  'F0'
  'S'
])
param languageSku string = 'F0'

@description('Custom Vision training pricing tier')
@allowed([
  'F0'
  'S0'
])
param customVisionTrainingSku string = 'F0'

@description('Custom Vision prediction pricing tier')
@allowed([
  'F0'
  'S0'
])
param customVisionPredictionSku string = 'F0'

@description('Azure AI Vision pricing tier')
@allowed([
  'F0'
  'S1'
])
param visionSku string = 'F0'

@description('PostgreSQL administrator login')
param postgresqlAdministratorLogin string = 'pgadminuser'

@description('PostgreSQL administrator password; provide securely at validation or deployment time')
@secure()
@minLength(8)
param postgresqlAdministratorPassword string

var accountSuffix = serviceKind == 'Translator' ? 'tr' : serviceKind == 'Language' ? 'lang' : serviceKind == 'CustomVisionTraining' ? 'cvtrain' : serviceKind == 'CustomVisionPrediction' ? 'cvpred' : 'vision'

var accountKind = serviceKind == 'Translator' ? 'TextTranslation' : serviceKind == 'Language' ? 'TextAnalytics' : serviceKind == 'CustomVisionTraining' ? 'CustomVision.Training' : serviceKind == 'CustomVisionPrediction' ? 'CustomVision.Prediction' : 'ComputerVision'

var accountSku = serviceKind == 'Translator' ? translatorSku : serviceKind == 'Language' ? languageSku : serviceKind == 'CustomVisionTraining' ? customVisionTrainingSku : serviceKind == 'CustomVisionPrediction' ? customVisionPredictionSku : visionSku

var accountName = take(
  '${prefix}${accountSuffix}${uniqueString(resourceGroup().id)}',
  63
)

var postgresqlServerName = take(
  toLower('${prefix}-pg-${uniqueString(resourceGroup().id)}'),
  63
)

// Existing Azure AI services remain available.
// PostgreSQL is selected separately using serviceKind.
resource aiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = if (serviceKind != 'PostgreSQL') {
  name: accountName
  location: location
  kind: accountKind
  sku: {
    name: accountSku
  }
  properties: {
    customSubDomainName: accountName
    publicNetworkAccess: 'Enabled'
  }
}

// Day 05: Azure Database for PostgreSQL Flexible Server.
resource postgresqlServer 'Microsoft.DBforPostgreSQL/flexibleServers@2025-08-01' = if (serviceKind == 'PostgreSQL') {
  name: postgresqlServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: postgresqlAdministratorLogin
    administratorLoginPassword: postgresqlAdministratorPassword
    version: '16'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    network: {
      publicNetworkAccess: 'Enabled'
    }
  }
}

// Create the application database inside the PostgreSQL server.
resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2025-08-01' = if (serviceKind == 'PostgreSQL') {
  parent: postgresqlServer
  name: 'knowledge_repository'
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// General outputs; blank when PostgreSQL is selected.
output accountResourceName string = serviceKind == 'PostgreSQL' ? '' : (aiAccount.?name ?? '')
output accountEndpoint string = serviceKind == 'PostgreSQL' ? '' : (aiAccount.?properties.?endpoint ?? '')
output accountKind string = serviceKind == 'PostgreSQL' ? '' : (aiAccount.?kind ?? '')
output accountLocation string = serviceKind == 'PostgreSQL' ? '' : (aiAccount.?location ?? '')
output accountSkuName string = serviceKind == 'PostgreSQL' ? '' : (aiAccount.?sku.?name ?? '')

// Preserve Day 01 Translator output names.
output translatorResourceName string = serviceKind == 'Translator' ? (aiAccount.?name ?? '') : ''
output translatorEndpoint string = serviceKind == 'Translator' ? (aiAccount.?properties.?endpoint ?? '') : ''
output translatorLocation string = serviceKind == 'Translator' ? (aiAccount.?location ?? '') : ''
output translatorSkuName string = serviceKind == 'Translator' ? (aiAccount.?sku.?name ?? '') : ''

// Preserve Day 04 Azure AI Vision output names.
output visionResourceName string = serviceKind == 'Vision' ? (aiAccount.?name ?? '') : ''
output visionEndpoint string = serviceKind == 'Vision' ? (aiAccount.?properties.?endpoint ?? '') : ''
output visionLocation string = serviceKind == 'Vision' ? (aiAccount.?location ?? '') : ''
output visionSkuName string = serviceKind == 'Vision' ? (aiAccount.?sku.?name ?? '') : ''

// Day 05 PostgreSQL outputs.
output postgresqlServerResourceName string = serviceKind == 'PostgreSQL' ? (postgresqlServer.?name ?? '') : ''
output postgresqlServerFqdn string = serviceKind == 'PostgreSQL' ? (postgresqlServer.?properties.?fullyQualifiedDomainName ?? '') : ''
output postgresqlDatabaseName string = serviceKind == 'PostgreSQL' ? (postgresqlDatabase.?name ?? '') : ''