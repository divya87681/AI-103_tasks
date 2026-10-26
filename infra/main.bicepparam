
using './main.bicep'

param prefix = 'ai103training'

// Day-04 validation can override the service without changing
// the shared default:
// az deployment group validate --resource-group rg-ai103-poc --template-file infra/main.bicep --parameters prefix=ai103training serviceKind=Vision visionSku=F0
