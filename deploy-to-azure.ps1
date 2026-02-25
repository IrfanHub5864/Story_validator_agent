# Azure Deployment Script for Story Validator
# This script deploys the Story Validator app to Azure Container Apps
# Prerequisites: Azure CLI, Docker, and PowerShell 5.1+

# ==================== CONFIGURATION ====================
$RG = "rg-story-validator"
$LOC = "centralindia"  # Change to your preferred region
$ACR = "acrstoryvalidator123"  # MUST be globally unique - change this!
$ENV = "env-story-validator"
$APP = "app-story-validator"
$IMAGE = "$ACR.azurecr.io/story-validator:v1"

# ==================== SECRETS ====================
# IMPORTANT: Update these with your actual values
$REVIEW_API_KEY = "my-secret-123"  # Change this!
$AZURE_PAT = "<NEW_PAT>"  # Get from https://dev.azure.com/_usersettings/tokens
$GROQ_API_KEY = "<NEW_GROQ_KEY>"  # Get from https://console.groq.com/keys
$AZURE_ORG_URL = "https://dev.azure.com/UserStoryValidatorOrg/"
$AZURE_PROJECT = "UserStoryValidator"

Write-Host "================================"
Write-Host "Story Validator - Azure Deployment"
Write-Host "================================"

# Check prerequisites
Write-Host "`n[*] Checking prerequisites..."
$commands = @("az", "docker")
foreach ($cmd in $commands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "[!] $cmd is not installed. Install it via: winget install --id=<ID>"
        exit 1
    }
}

# Login to Azure
Write-Host "`n[1/6] Logging in to Azure..."
az login
if ($LASTEXITCODE -ne 0) { exit 1 }

# Get subscription ID
$SUBSCRIPTION = az account show --query id -o tsv
Write-Host "[OK] Using subscription: $SUBSCRIPTION"

# Create resource group
Write-Host "`n[2/6] Creating resource group: $RG"
az group create -n $RG -l $LOC
if ($LASTEXITCODE -ne 0) { exit 1 }

# Create ACR
Write-Host "`n[3/6] Creating Azure Container Registry: $ACR"
az acr create -n $ACR -g $RG --sku Basic
if ($LASTEXITCODE -ne 0) { exit 1 }

# Login to ACR
Write-Host "`n[3b/6] Logging in to ACR..."
az acr login -n $ACR
if ($LASTEXITCODE -ne 0) { exit 1 }

# Create Container Apps Environment
Write-Host "`n[4/6] Creating Container Apps Environment: $ENV"
az containerapp env create -n $ENV -g $RG -l $LOC
if ($LASTEXITCODE -ne 0) { exit 1 }

# Build and push Docker image
Write-Host "`n[5/6] Building and pushing Docker image..."
Write-Host "Building image: story-validator:latest"
docker build -t story-validator:latest .
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "Tagging image: $IMAGE"
docker tag story-validator:latest $IMAGE
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "Pushing to ACR..."
docker push $IMAGE
if ($LASTEXITCODE -ne 0) { exit 1 }

# Get ACR credentials
Write-Host "`n[5b/6] Retrieving ACR credentials..."
$ACR_USER = az acr credential show -n $ACR --query username -o tsv
$ACR_PASS = az acr credential show -n $ACR --query "passwords[0].value" -o tsv

# Deploy Container App
Write-Host "`n[6/6] Deploying Container App: $APP"
az containerapp create `
  -n $APP `
  -g $RG `
  --environment $ENV `
  --image $IMAGE `
  --ingress external `
  --target-port 8000 `
  --min-replicas 0 `
  --max-replicas 1 `
  --registry-server "$ACR.azurecr.io" `
  --registry-username $ACR_USER `
  --registry-password $ACR_PASS `
  --secrets `
    review-api-key="$REVIEW_API_KEY" `
    azure-pat="$AZURE_PAT" `
    groq-api-key="$GROQ_API_KEY" `
  --env-vars `
    AZURE_ORG_URL="$AZURE_ORG_URL" `
    AZURE_PROJECT="$AZURE_PROJECT" `
    REVIEW_API_KEY=secretref:review-api-key `
    AZURE_PAT=secretref:azure-pat `
    GROQ_API_KEY=secretref:groq-api-key `
    PORT=8000

if ($LASTEXITCODE -ne 0) { 
    Write-Host "[!] Deployment failed"
    exit 1 
}

# Get the app URL
Write-Host "`n[+] Deployment successful!"
$APP_URL = az containerapp show -n $APP -g $RG --query properties.configuration.ingress.fqdn -o tsv
Write-Host "`n================================"
Write-Host "App URL: https://$APP_URL"
Write-Host "================================"

# Display next steps
Write-Host "`nNext steps:"
Write-Host "1. Open: https://$APP_URL"
Write-Host "2. Enter a Work Item ID from your Azure DevOps project"
Write-Host "3. Click Review Story to validate"
Write-Host "`nTo update the app, re-run steps 5-6 with a new image tag"
