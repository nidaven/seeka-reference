targetScope = 'subscription'

param resourceGroupName string
// param environment string
param location string

resource rg 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}

output resgrp string = rg.id
