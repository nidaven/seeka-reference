param containerAppsEnvName string
param location string
param dockerImage string
// param acrLoginServer string
// param imageName string

// @description('user-assigned identity for pull acr images')
// param uai string

resource cAppEnv 'Microsoft.App/managedEnvironments@2022-10-01' existing = {
  name: containerAppsEnvName
}


resource databaseService 'Microsoft.App/containerApps@2022-10-01' = {
  name: 'rhemasearch-database-service'
  location : location
  // identity: {
  //   type: 'UserAssigned'
  //   userAssignedIdentities: {
  //     '${uai}' : {}
  //   }
  // }
  properties: {
    environmentId: cAppEnv.id
    template: {
      containers: [
        {
          name: 'rhemasearch-database'
          image: 'nidaven/rhemasearch_db:0.1'
          resources: {
            cpu: 1
            memory: '2Gi'
          }
          //TODO: add resources that can be used by the container app
        }
      ]
      scale: {
        minReplicas: 1
        rules: [
          {
            name: 'http-requests'
            http: {
              metadata: {
                concurrentRequests: '5'
              }
            }
          }
        ]
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
        {
          name: 'reg-pswd'
          value: '2992n@V!Ad14c11e18'
        }
      ]
      registries: [
        {
          // identity: uai
          server: 'docker.io'
          username: 'nidaven'
          passwordSecretRef: 'reg-pswd'
        }
      ]
    }
  }

}

output containerAppFQDN string = databaseService.properties.configuration.ingress.fqdn
