param containerAppsEnvName string
// param logAnalyticsWorkspaceName string
// param appInsightsName string
param location string


// TODO: check costs associated with log analytics
// resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
//   name: logAnalyticsWorkspaceName
//   location: location
//   properties: any({
//     retentionInDays: 30
//     features: {
//       searchVersion: 1
//     }
//     sku: {
//       name: 'PerGB2018'
//     }
//   })
// }


//TODO: check costs associated with app insights
// resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
//   name: appInsightsName
//   location: location
//   kind: 'web'
//   properties: { 
//     Application_Type: 'web'
//   }
// }

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' = {
  name: 'containerapp-log-${containerAppsEnvName}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource containerAppsEnv 'Microsoft.App/managedEnvironments@2022-06-01-preview' = {
  name: 'capps-env-${containerAppsEnvName}'
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
// output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output defaultDomain string = containerAppsEnv.properties.defaultDomain
