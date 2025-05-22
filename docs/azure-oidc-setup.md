# ✅ GitHub Actions Authorization for Azure (OIDC-based)

This repository uses GitHub Actions to deploy Azure infrastructure using [Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview). Authentication is handled via **federated identity (OIDC)**, so no secrets or credentials are hardcoded in workflows.

---

## 🔧 File Structure and Key Artifacts

This setup relies on two main directories:

| Path                     | Purpose |
|--------------------------|---------|
| `/infra/`                | Contains the [Bicep](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview) infrastructure-as-code templates and environment parameter files |
| `/.github/workflows/`    | Contains the GitHub Actions workflow that triggers Azure deployment on commit to `main` |

---

### ➕ `/infra/main.bicep`

Defines the resources to be deployed — such as your App Service plan and Web App. This file is parameterized so it can be reused across environments.

---

### 📁 `/infra/dev.parameters.json`

Supplies values for `main.bicep` during development deployments (e.g., region, SKU, web app name).

---

### ⚙️ `/.github/workflows/deploy.yml`

This workflow automatically runs on push to `main`, authenticates to Azure using OIDC, and deploys the Bicep template using `azure/arm-deploy@v2`.

---

## 🔐 Authorization Setup Steps (One-Time)

Follow these steps to allow GitHub Actions to deploy to your Azure subscription securely.

---

### 1. Register an App in Microsoft Entra ID

1. Go to **Azure Portal** → **Microsoft Entra ID** → **App registrations**
2. Click **"New registration"**
3. Use these settings:
   - **Name**: `github-bicep-deployer`
   - **Supported account types**: **Single tenant**
4. Click **Register**

---

### 2. Add a Federated Credential

1. In your App Registration:
   → **Certificates & secrets** → **Federated credentials** → **+ Add credential**
2. Choose **GitHub Actions deploying Azure resources**
3. Fill:
   - **Organization**: Your GitHub username/org (e.g. `knavillus10`)
   - **Repository**: This repo’s name (e.g. `portfolio-infra`)
   - **Entity type**: `Branch`
   - **Branch**: `main`
4. Click **Add**

---

### 3. Assign the App Access to Azure Resources

1. Go to the Resource Group (e.g., `knavillus10-portfolio`)
2. Click **Access control (IAM)** → **+ Add → Add role assignment**
3. Role: `Website Contributor` (for Web Apps)
4. Assign to: the **App registration** from Step 1

---

### 4. Add GitHub Repository Secrets

In GitHub:

1. Go to:  
   → **Settings → Secrets and variables → Actions**
2. Add the following secrets:

| Name | Value |
|------|-------|
| `AZURE_CLIENT_ID`     | App Registration → Application (client) ID |
| `AZURE_TENANT_ID`     | App Registration → Directory (tenant) ID |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscriptions → Your subscription ID |

---

## ✅ What Happens on Deployment

When you push to `main`:
- GitHub Actions triggers `/.github/workflows/deploy.yml`
- It authenticates to Azure using OIDC and those repo secrets
- It deploys `/infra/main.bicep` using `/infra/dev.parameters.json` to the specified resource group

You can validate changes using:
```bash
az deployment group what-if \
  --resource-group knavillus10-portfolio \
  --template-file infra/main.bicep \
  --parameters infra/dev.parameters.json
