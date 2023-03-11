param containerAppsEnvName string
param location string
param dbImageName string
param cAppsName string

resource cAppEnv 'Microsoft.App/managedEnvironments@2022-10-01' existing = {
  name: containerAppsEnvName
}

resource databaseService 'Microsoft.App/containerApps@2022-06-01-preview' = {
  name: '${cAppsName}-db-service'
  location : location
  properties: {
    environmentId: cAppEnv.id
    template: {
      containers: [
        {
          name: 'rhema-db-service'
          image: dbImageName
          resources: {
            cpu: 1
            memory: '2Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
      }
    }
    configuration: {
      ingress: {
        external: true
        targetPort: 8888
        allowInsecure: true
        transport: 'auto'
      }
      secrets: [
      ]
      registries: [
      ]
      activeRevisionsMode: 'Single'
    }
  }

}

output containerAppFQDN string = databaseService.properties.configuration.ingress.fqdn
