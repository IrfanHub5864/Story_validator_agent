# 🚀 Story Validator - Deployment & UI Guide

## Quick Start

### Prerequisites
Before deploying to Azure, ensure you have:

1. **Azure CLI** - Install via:
   ```powershell
   winget install --id Microsoft.AzureCLI
   ```

2. **Docker Desktop** - Install via:
   ```powershell
   winget install --id Docker.DockerDesktop
   ```
   ⚠️ **Note**: You may need to restart your system for Docker to work properly.

3. **Azure Subscription** - Create one at https://azure.microsoft.com/free/

4. **Azure DevOps Account** - https://dev.azure.com

### Step 1: Prepare Your Credentials

Before running the deployment script, gather:

1. **Azure DevOps Personal Access Token (PAT)**
   - Go to: https://dev.azure.com/_usersettings/tokens
   - Click "New Token"
   - Name: `StoryValidator`
   - Scopes: Select `Work Item (Read & Write)`
   - Copy the token (you can only see it once!)

2. **Groq API Key** (for AI evaluation)
   - Go to: https://console.groq.com/keys
   - Create a new API key
   - Copy it

3. **Review API Key** (Optional - for securing your API)
   - Create a secure string, e.g., `my-secret-123`
   - Or use a tool: https://www.uuidgenerator.net/

### Step 2: Update Deployment Script

Edit `deploy-to-azure.ps1` and update these values:

```powershell
$ACR = "acrstoryvalidator123"  # ← CHANGE THIS (must be globally unique!)
$REVIEW_API_KEY = "my-secret-123"  # ← CHANGE THIS
$AZURE_PAT = "<NEW_PAT>"  # ← PASTE YOUR PAT HERE
$GROQ_API_KEY = "<NEW_GROQ_KEY>"  # ← PASTE YOUR GROQ KEY HERE
$AZURE_ORG_URL = "https://dev.azure.com/YourOrg/"  # ← UPDATE YOUR ORG
$AZURE_PROJECT = "YourProject"  # ← UPDATE YOUR PROJECT
```

### Step 3: Run the Deployment Script

```powershell
cd "C:\story-validator-cli1 - Copy"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy-to-azure.ps1
```

The script will:
1. ✅ Check prerequisites
2. ✅ Create a resource group
3. ✅ Create an Azure Container Registry (ACR)
4. ✅ Create a Container Apps Environment
5. ✅ Build your Docker image
6. ✅ Push to ACR
7. ✅ Deploy the app

Once complete, you'll get a **public URL** to access your app!

---

## 🎨 Using the Web UI

### Features

The new web interface includes:

✨ **Review Button**
- Enter a Work Item ID from Azure DevOps
- Click "Review Story" to start validation
- Optional: Force re-review even if unchanged

🔐 **API Key Protection** (if configured)
- Secure endpoint for API calls
- Optional password protection

📊 **Live Results Display**
- See AI evaluation results in real-time
- Formatted review from the agent
- Clear success/error messages

### Testing Locally

Before deploying to Azure, test locally:

```powershell
cd "C:\story-validator-cli1 - Copy"
& ".\.venv\Scripts\Activate.ps1"
$env:PORT="8000"
python app.py
```

Then open: http://127.0.0.1:8000

---

## 🔧 API Usage

### Direct API Call (for CI/CD integration)

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "my-secret-123"  # Your review API key
}
$body = @{
    work_item_id = 1234
    force = $false
} | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "https://app-story-validator.azurecontainerapps.io/review" `
  -Headers $headers `
  -Body $body
```

### Response Format

**Success:**
```json
{
  "status": "commented",
  "message": "Review completed and comment posted to Azure DevOps.",
  "work_item_id": 1234,
  "result": "..evaluation report.."
}
```

**Skipped (already evaluated):**
```json
{
  "status": "skipped",
  "message": "Story unchanged since last review. No new comment added.",
  "work_item_id": 1234
}
```

---

## 🐛 Troubleshooting

### Docker not found
- Install Docker Desktop: `winget install --id Docker.DockerDesktop`
- Restart your system

### ACR name already taken
- Registry names must be globally unique
- Change `$ACR` to something like `acrstoryvalidator{random}`

### Azure authentication fails
- Run: `az logout` then `az login`
- Ensure you have contributor access to the subscription

### Container app won't start
Check logs:
```powershell
az containerapp logs show -n app-story-validator -g rg-story-validator --tail 100
```

### API returns 500 error
- Verify Azure DevOps PAT is correct
- Verify Groq API key works
- Check environment variables are set correctly

---

## 📈 Scaling & Monitoring

### View logs in Azure Portal

```powershell
az containerapp logs show -n app-story-validator -g rg-story-validator --tail 200
```

### Update the app (new deployment)

```powershell
# Edit code, then:
docker build -t story-validator:v2 .
docker tag story-validator:v2 acrstoryvalidator123.azurecr.io/story-validator:v2
docker push acrstoryvalidator123.azurecr.io/story-validator:v2

az containerapp update -n app-story-validator -g rg-story-validator `
  --image acrstoryvalidator123.azurecr.io/story-validator:v2
```

### Configure auto-scaling

```powershell
az containerapp update -n app-story-validator -g rg-story-validator `
  --min-replicas 0 `
  --max-replicas 5
```

---

## 🧹 Cleanup (Delete all resources)

```powershell
az group delete -n rg-story-validator --yes
```

This will delete the resource group and all associated resources.

---

## 📚 Additional Resources

- [Azure Container Apps Docs](https://learn.microsoft.com/en-us/azure/container-apps/)
- [Azure CLI Reference](https://learn.microsoft.com/en-us/cli/azure/)
- [Docker Documentation](https://docs.docker.com/)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/)

---

Need help? Check the logs or create an issue! 🎉
