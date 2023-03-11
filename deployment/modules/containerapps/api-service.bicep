// TODO: add
param containerAppsEnvName string
param location string
// param acrLoginServer string
// param imageName string

// @description('user-assigned identity for pull acr images')
// param uai string

resource cAppEnv 'Microsoft.App/managedEnvironments@2022-10-01' existing = {
  name: containerAppsEnvName
}

resource APIService 'Microsoft.App/containerApps@2022-06-01-preview' = {
  name: 'api-service'
  location : location

  properties: {
    environmentId: cAppEnv.id
    template: {
      containers: [
        {
          name: 'api-service'
          image: 'docker.io/nidaven/rhemasearch:0.2'
          resources: {
            cpu: 1
            memory: '2Gi'
          }
          env: [
            {
              name: 'DB_FQDN'
              value: 'https://seeka-search-docker.redmoss-0aaa867a.uksouth.azurecontainerapps.io'
            }
            {
              name: 'OPENAI_API_KEY'
              // secretRef: 'openai-api-secret' 
              value: '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'
            }
          ]
          //TODO: add resources that can be used by the container app
        }
      ]
      scale: {
        minReplicas: 0
      }
    }
    configuration: {
      ingress: {
        external: true
        targetPort: 8081
        allowInsecure: true
        transport: 'auto'
      }
      secrets: [
        {
          name: 'reg-pswd'
          value: '2992n@V!Ad14c11e18'
        }
        {
          name: 'openai-api-secret'
          value: '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'
        }
      ]
      registries: [
        // {
        //   server: 'docker.io'
        //   username: 'nidaven'
        //   passwordSecretRef: 'reg-pswd'
        // }
      ]
      activeRevisionsMode: 'Single'
    }
  }

}

output APIFQDN string = APIService.properties.configuration.ingress.fqdn
