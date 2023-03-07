param acrName string //TODO: reference resource group name
param location string
param dockerRegimageName string

// @description('The code assigns a role-based access control (RBAC) resource ID for Microsoft Authorization/Role Definitions with a specific GUID')
// var acrPullRole = resourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

resource acr 'Microsoft.ContainerRegistry/registries@2022-12-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}


// @description('This module seeds the ACR with the public version of the app')
// module acrImportImage 'br/public:deployment-scripts/import-acr:3.0.1' =  {
//   name: 'importContainerImage'
//   params: {
//     acrName: acrName
//     location: location
//     images: array(dockerRegimageName)
//   }
// }
// resource uai 'Microsoft.ManagedIdentity/userAssignedIdentities@2022-01-31-preview' = {
//   name: 'id-${acrName}'
//   location: location
// }

// @description('This allows the managed identity of the container app to access the registry, note scope is applied to the wider ResourceGroup not the ACR')
// resource uaiRbac 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
//   name: guid(resourceGroup().id, uai.id, acrPullRole)
//   properties: {
//     roleDefinitionId: acrPullRole
//     principalId: uai.properties.principalId
//     principalType: 'ServicePrincipal'
//   }
// }

// output acrUai string = uai.id
output acrLoginServer string = acr.properties.loginServer
output acrId string = acr.id
// output importedImage string = acrImportImage.outputs.importedImages[0].acrHostedImage
