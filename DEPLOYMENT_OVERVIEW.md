# Story Validator Deployment Overview

## Goal
Deploy as an on-demand service. Validation runs only when a user clicks Review for a specific story.

## Runtime Flow
1. Client sends `POST /review` with `work_item_id`.
2. Service fetches story from Azure DevOps.
3. Service validates with model.
4. Service patches comment back to the same work item.

## Required Environment Variables
- `AZURE_ORG_URL`
- `AZURE_PROJECT`
- `AZURE_PAT`
- `GROQ_API_KEY`
- `REVIEW_API_KEY` (recommended for `/review`)
- `PORT` (optional, default `8000`)

## Local Run Commands (PowerShell)
```powershell
cd "c:\story-validator-cli1 - Copy"
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:REVIEW_API_KEY="set-a-strong-internal-key"
$env:PORT="8000"
python app.py
```

## API Test Commands (PowerShell)
```powershell
Invoke-RestMethod http://localhost:8000/healthz

$headers = @{
  "Content-Type" = "application/json"
  "X-API-Key" = "set-a-strong-internal-key"
}
$body = '{"work_item_id":12345,"force":false}'
Invoke-RestMethod -Method Post -Uri http://localhost:8000/review -Headers $headers -Body $body
```

## Docker Packaging Commands
```powershell
cd "c:\story-validator-cli1 - Copy"
docker build -t story-validator:latest .

docker run --rm -p 8000:8000 `
  -e AZURE_ORG_URL="https://dev.azure.com/<org>/" `
  -e AZURE_PROJECT="<project>" `
  -e AZURE_PAT="<pat>" `
  -e GROQ_API_KEY="<groq_key>" `
  -e REVIEW_API_KEY="<internal_key>" `
  story-validator:latest
```

## Azure Deployment Direction
Recommended: Azure App Service (Container) or Azure Container Apps with the same Docker image.
- Push image to Azure Container Registry.
- Configure env vars as app settings/secrets.
- Expose HTTPS endpoint.
- Integrate Azure DevOps button/extension to call `POST /review`.
