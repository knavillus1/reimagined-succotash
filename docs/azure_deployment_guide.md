# 🚀 Deploying a FastAPI + Vite App to Azure Web App Service

This guide walks through deploying your full-stack app (FastAPI backend, Vite frontend) to an Azure Web App Service, using Bicep for infrastructure and GitHub Actions for deployment.

---

## 🔧 Prerequisites

- Azure subscription (Free or paid)
- Web App and Linux App Plan deployed via Bicep
- GitHub repository connected to Azure
- `.infra` directory with `main.bicep` and `dev.parameters.json`

---

## 1. ✅ Confirm Runtime Compatibility

Ensure the selected Azure region supports the `linuxFxVersion` you specified in your Bicep file. If `PYTHON|3.13` fails, downgrade to:

```bicep
param linuxFxVersion string = 'PYTHON|3.12'
2. 🪄 Serve Vite Frontend with FastAPI

In your backend/app/main.py, mount the Vite build output:

from pathlib import Path
from fastapi.staticfiles import StaticFiles

static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
After each frontend build, copy the dist/ folder into backend/app/static.

3. 🤖 Add GitHub Action for CI/CD

Create .github/workflows/deploy.yml:

name: Build & Deploy to Azure Web App
on:
  push:
    branches: [main]

env:
  AZURE_WEBAPP_NAME: knavillus10-portfolio-webapp
  PYTHON_VERSION: "3.12"
  NODE_VERSION:  "20"

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Build frontend
        working-directory: frontend
        run: |
          npm ci
          npm run build

      - name: Copy frontend build to backend
        run: |
          rm -rf backend/app/static || true
          mkdir -p backend/app/static
          cp -r frontend/dist/* backend/app/static/

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install Python dependencies
        run: |
          pip install -r requirements.txt --target site-packages

      - name: Zip deploy package
        run: |
          zip -r deploy.zip backend site-packages requirements.txt

      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          package: deploy.zip
4. 🔁 Set Startup Command in Azure Portal

Go to:

App Service → Configuration → General settings → Startup Command
Add:

gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.app.main:app
5. ⚙️ Set Required App Settings

Setting	Value	Purpose
WEBSITE_RUN_FROM_PACKAGE	1	Use deployed ZIP directly
SCM_DO_BUILD_DURING_DEPLOYMENT	false	Skip Kudu/Oryx build
WEBSITE_NODE_DEFAULT_VERSION	20	Set default Node version
GUNICORN_CMD_ARGS (optional)	--timeout 60	Tune Gunicorn worker settings
6. 🚀 Deploy Your App

Commit the workflow and push to main
GitHub Actions will build and deploy the app
Visit your deployed site at:
https://<webAppName>.azurewebsites.net
🛠 Troubleshooting

Symptom	Fix
ModuleNotFoundError	Ensure site-packages is included in the zip
Frontend returns 404s	Confirm static files copied to backend/app/static
"Runtime not found" error	Use `PYTHON
🌱 What’s Next?

🔐 [ ] Add a custom domain and free HTTPS cert
📈 [ ] Upgrade to B1 plan for "Always On"
🧠 [ ] Enable Application Insights or Log Stream for debugging