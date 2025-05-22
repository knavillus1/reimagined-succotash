@description('Azure region for all resources')
param location string = 'westus'

@description('Globally-unique web-app name')
param webAppName string

@description('Plan SKU (F1 = free, B1 = Basic, P1v3 = Prod)')
@allowed([ 'F1' 'B1' 'P1v3' ])
param skuName string = 'F1'

@description('Stack+version string understood by App Service on Linux')
param linuxFxVersion string = 'PYTHON|3.13'

var planName = '${webAppName}-plan'

// 🔧 Fix: extract tier into a variable
var tier = skuName == 'F1' ? 'Free' :
           skuName == 'B1' ? 'Basic' :
                             'PremiumV3'

resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name:  planName
  location: location
  kind: 'linux'
  sku: {
    name: skuName
    tier: tier
    capacity: 1
  }
  properties: {
    reserved: true
  }
}

resource site 'Microsoft.Web/sites@2023-01-01' = {
  name:  webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      alwaysOn: false
    }
  }
}

output defaultHost string = site.properties.defaultHostName
