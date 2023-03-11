// TODO: add
param containerAppsEnvName string
param location string
param dbFQDN string
param apiImageName string
param cAppsName string

resource cAppEnv 'Microsoft.App/managedEnvironments@2022-10-01' existing = {
  name: containerAppsEnvName
}

resource APIService 'Microsoft.App/containerApps@2022-06-01-preview' = {
  name: '${cAppsName}-api-service'
  location : location

  properties: {
    environmentId: cAppEnv.id
    template: {
      containers: [
        {
          name: '${cAppsName}-api-service'
          image: apiImageName
          resources: {
            cpu: 1
            memory: '2Gi'
          }
          env: [
            {
              name: 'DB_FQDN'
              // value: 'https://seeka-search-docker.redmoss-0aaa867a.uksouth.azurecontainerapps.io'
              value: 'https://${dbFQDN}'
            }
            {
              name: 'OPENAI_API_KEY'
              value: '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'
              // secretRef: 'openai-api-secret'
            }
          ]
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
          name: 'openai-api-secret'
          value: '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'
        }
      ]
      registries: [
      ]
      activeRevisionsMode: 'Single'
    }
  }

}

output APIFQDN string = APIService.properties.configuration.ingress.fqdn
