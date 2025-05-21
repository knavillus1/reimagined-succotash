// ──────────────────────────────────────────────────────────────
// Basic parameters
// ──────────────────────────────────────────────────────────────
@description('Azure region for all resources')
param location string = 'westus'           // matches what you built, change if quota blocks you

@description('Globally-unique web-app name')
param webAppName string                    // e.g. "knavillus10-portfolio-webapp"

@description('Plan SKU (F1 = free, B1 = Basic, P1v3 = Prod)')
@allowed([ 'F1' 'B1' 'P1v3' ])
param skuName string = 'F1'

@description('Stack+version string understood by App Service on Linux')
param linuxFxVersion string = 'PYTHON|3.13'

// convenience
var planName = '${webAppName}-plan'

// ──────────────────────────────────────────────────────────────
// App Service plan  (kind: Linux) – holds the workers
// ──────────────────────────────────────────────────────────────
resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name:  planName
  location: location
  kind: 'linux'
  sku: {
    name: skuName
    tier: skuName == 'F1' ? 'Free'
        : skuName == 'B1' ? 'Basic'
        :                    'PremiumV3'
    capacity: 1            // same as “Number of workers”
  }
  properties: {
    reserved: true         // *must* be true for Linux
  }
}

// ──────────────────────────────────────────────────────────────
// Web app itself
// ──────────────────────────────────────────────────────────────
resource site 'Microsoft.Web/sites@2023-01-01' = {
  name:  webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true                     // copied from JSON
    siteConfig: {
      linuxFxVersion: linuxFxVersion    // PYTHON|3.13
      alwaysOn: false                   // matches Free SKU default
    }
  }
}

// ──────────────────────────────────────────────────────────────
output defaultHost string = site.properties.defaultHostName
