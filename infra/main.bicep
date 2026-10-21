
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

var accountSuffix = serviceKind == 'Translator' ? 'tr' : serviceKind == 'Language' ? 'lang' : serviceKind == 'CustomVisionTraining' ? 'cvtrain' : 'cvpred'

var accountKind = serviceKind == 'Translator' ? 'TextTranslation' : serviceKind == 'Language' ? 'TextAnalytics' : serviceKind == 'CustomVisionTraining' ? 'CustomVision.Training' : 'CustomVision.Prediction'

var accountSku = serviceKind == 'Translator' ? translatorSku : serviceKind == 'Language' ? languageSku : serviceKind == 'CustomVisionTraining' ? customVisionTrainingSku : customVisionPredictionSku

var accountName = take(
  '${prefix}${accountSuffix}${uniqueString(resourceGroup().id)}',
  63
)

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

// Preserve Day 01 Translator output names.
output translatorResourceName string = serviceKind == 'Translator' ? aiAccount.name : ''
output translatorEndpoint string = serviceKind == 'Translator' ? aiAccount.properties.endpoint : ''
output translatorLocation string = serviceKind == 'Translator' ? aiAccount.location : ''
output translatorSkuName string = serviceKind == 'Translator' ? aiAccount.sku.name : ''
