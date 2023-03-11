param cAppsName string
param location string


resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: 'containerapp-log-${cAppsName}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource containerAppsEnv 'Microsoft.App/managedEnvironments@2022-06-01-preview' = {
  name: 'capps-env-${cAppsName}'
  location: location
  sku: {
    name: 'Consumption'
  }
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}


output cAppsEnvName string = containerAppsEnv.name
output cappsEnvId string = containerAppsEnv.id
output defaultDomain string = containerAppsEnv.properties.defaultDomain
