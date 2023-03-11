targetScope = 'subscription' //setting target scope to subscription scope sets a requirement for scope when deployming modules

param cAppsName string
param acrName string
param dbImageName string 
param apiImageName string
param location string =  'uksouth'
param resourceGroupName string = 'rg-rhemasearch-dev'
// param environment string = 'dev'


module rgModule 'modules/rg-rhemasearch.bicep' = {
  name : '${deployment().name}--resourcegroup'
  params: {
    location: location
    resourceGroupName: resourceGroupName
  }
}

// module acrModule 'modules/container-registry.bicep' = {
//   name: '${deployment().name}--container-registry'
//   params: {
//     acrName: acrName
//     location: location
//     dockerRegimageName: imageName
//   }
//   dependsOn: [
//     rgModule
//   ]
//   scope: resourceGroup(resourceGroupName)
// }

module cAppsEnvModule 'modules/containerapps/containerapps-env.bicep' = {
  name: '${deployment().name}--containerapps-env'
  params: {
    location: location
    cAppsName: cAppsName
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
    dbImageName: dbImageName
    cAppsName: cAppsName
  }
  dependsOn: [
    rgModule
    cAppsEnvModule
  ]
  scope: resourceGroup(resourceGroupName)
}

module apiModule 'modules/containerapps/api-service.bicep' = {
  name: '${deployment().name}--api-service'
  params: {
    location: location
    containerAppsEnvName: cAppsEnvModule.outputs.cAppsEnvName
    dbFQDN: databaseModule.outputs.containerAppFQDN
    apiImageName: apiImageName
    cAppsName: cAppsName
  }
  dependsOn: [
    rgModule
    cAppsEnvModule
    databaseModule
  ]
  scope: resourceGroup(resourceGroupName)
}

output databaseFQDN string = databaseModule.outputs.containerAppFQDN
output apiFQDN string = apiModule.outputs.APIFQDN
