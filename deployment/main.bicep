targetScope = 'subscription' //setting target scope to subscription scope sets a requirement for scope when deployming modules

param cAppsName string
param acrName string
param imageName string
param location string =  'uksouth'
param resourceGroupName string = 'rg-rhemasearch-dev'
param dockerImage string
// param environment string = 'dev'


module rgModule 'modules/rg-rhemasearch.bicep' = {
  name : '${deployment().name}--resourcegroup'
  params: {
    location: location
    resourceGroupName: resourceGroupName
  }
}

// resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
//   name: '${resourceGroupName}-${environment}'
//   location: location
// }

module acrModule 'modules/container-registry.bicep' = {
  name: '${deployment().name}--container-registry'
  params: {
    acrName: acrName
    location: location
    dockerRegimageName: imageName
  }
  dependsOn: [
    rgModule
  ]
  scope: resourceGroup(resourceGroupName)
}

module cAppsEnvModule 'modules/containerapps/containerapps-env.bicep' = {
  name: '${deployment().name}--containerapps-env'
  params: {
    location: location
    containerAppsEnvName: cAppsName
  }
  dependsOn: [
    rgModule
  ]
  scope: resourceGroup(resourceGroupName)
}

module databaseModule 'modules/containerapps/database-service.bicep' = {
  name: '${deployment().name}--database-service'
  params: {
    location: location
    containerAppsEnvName: cAppsEnvModule.outputs.cAppsEnvName
    dockerImage: dockerImage
  }
  dependsOn: [
    rgModule
    cAppsEnvModule
  ]
  scope: resourceGroup(resourceGroupName)
}

output databaseFQDN string = databaseModule.outputs.containerAppFQDN
