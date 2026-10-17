targetScope = 'resourceGroup'

@description('Deployment location')
param location string = resourceGroup().location

@description('Unique prefix for training resources')
@minLength(3)
@maxLength(20)
param prefix string = 'ai103training'

@description('Select the service for the current day')
@allowed([
  'Translator'
  'Language'
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

var accountName = take(
  '${prefix}${serviceKind == 'Translator' ? 'tr' : 'lang'}${uniqueString(resourceGroup().id)}',
  63
)

var accountKind = serviceKind == 'Translator' ? 'TextTranslation' : 'TextAnalytics'
var accountSku = serviceKind == 'Translator' ? translatorSku : languageSku

resource aiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
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

output accountResourceName string = aiAccount.name
output accountEndpoint string = aiAccount.properties.endpoint
output accountKind string = aiAccount.kind
output accountLocation string = aiAccount.location
output accountSkuName string = aiAccount.sku.name

// Preserve Day 01 output names for Translator deployments.
output translatorResourceName string = serviceKind == 'Translator' ? aiAccount.name : ''
output translatorEndpoint string = serviceKind == 'Translator' ? aiAccount.properties.endpoint : ''
output translatorLocation string = serviceKind == 'Translator' ? aiAccount.location : ''
output translatorSkuName string = serviceKind == 'Translator' ? aiAccount.sku.name : ''
