# 🚀 QUICK START - Azure DevOps Extension

## What You Now Have

An **Azure DevOps Extension** that adds a "Review with AI Agent" button to every work item page.

### Step 1: Ensure Backend is Running

Your Flask app must be deployed somewhere accessible. Options:

**A) Azure Container Apps** (Recommended for production)
```powershell
cd "C:\story-validator-cli1 - Copy"
.\deploy-to-azure.ps1
```
This will give you a public URL like: `https://app-story-validator.azurecontainerapps.io`

**B) Local Testing** (Dev machine only)
```powershell
cd "C:\story-validator-cli1 - Copy"
& ".\.venv\Scripts\Activate.ps1"
$env:PORT="8000"
python app.py
```
URL will be: `http://127.0.0.1:8000`

---

## Step 2: Create & Publish Extension

### 2.1 Install Node.js (if you don't have it)
```powershell
winget install --id OpenJS.NodeJS
```

### 2.2 Navigate to Extension Folder
```powershell
cd "C:\story-validator-cli1 - Copy\extension"
```

### 2.3 Run Setup Script (Easiest)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup-and-publish.ps1
```

**OR** Do it manually:

```powershell
# Install packaging tool
npm install -g tfx-cli

# Validate your extension
tfx extension validate --manifest-globs vss-extension.json

# Create package
tfx extension create --manifest-globs vss-extension.json --publishers StoryValidatorOrg
```

---

## Step 3: Publish to Azure DevOps Marketplace

Go to: https://dev.azure.com/_usersettings/tokens

1. Click **New Token**
2. Name: `ExtensionPublisher`
3. Scopes: Check **Manage extensions**
4. Copy the token

Then run:
```powershell
cd "C:\story-validator-cli1 - Copy\extension"

tfx extension publish `
  --manifest-globs vss-extension.json `
  --publishers StoryValidatorOrg `
  --token <PASTE_YOUR_TOKEN_HERE>
```

---

## Step 4: Install Extension in Your Organization

1. Go to: https://marketplace.visualstudio.com/publishers/StoryValidatorOrg
2. Find **"Story Validator - AI Review"**
3. Click **Install**
4. Select your Azure DevOps organization
5. Click **Confirm**

---

## Step 5: Configure Extension

1. Open your Azure DevOps project
2. Go to **Project Settings** → **Extensions**
3. Find **"Story Validator - AI Review"**
4. Click **Settings**
5. Enter:
   - **API URL**: Your Flask app URL
     - If deployed: `https://app-story-validator.azurecontainerapps.io`
     - If local: `http://127.0.0.1:8000`
   - **API Key**: (leave empty if no auth needed)

---

## 🎯 Using the Extension

1. Open **Azure DevOps**
2. Go to **Boards** → **Work Items**
3. Click on any **User Story**
4. Look for **"Review with AI Agent"** button in toolbar
5. Click it
6. Popup appears: **"Reviewing Story..."** (loading)
7. Popup shows: **"✓ Review Completed"**
8. Story comment is **automatically posted** to work item

---

## 🧪 Testing

### Test the Button Works
1. Make sure Flask app is running
2. Make sure extension is installed
3. Open a work item
4. Click button → Popup should appear

### Test the API Directly
```powershell
$headers = @{ "Content-Type"="application/json" }
$body = @{ work_item_id = 1234; force = $false } | ConvertTo-Json

Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/review" `
  -Headers $headers `
  -Body $body
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Button doesn't appear | Refresh page (F5), check extension is installed |
| Button doesn't work | Check Flask app is running, check API URL in settings |
| "Review completed" but no comment | Check Azure PAT token in `.env` is valid |
| API returns 500 error | Check Flask console logs |

---

## 📝 Project Structure

```
story-validator-cli1 - Copy/
├── app.py                           # Flask backend
├── engine/                          # Review logic
├── extension/                       # NEW: Azure DevOps Extension
│   ├── vss-extension.json          # Extension config
│   ├── src/
│   │   ├── work-item-review.html   # Button UI
│   │   └── work-item-review.js     # Button logic
│   ├── README.md                   # Full docs
│   ├── package.json                # Dependencies
│   └── setup-and-publish.ps1       # Setup script
├── deploy-to-azure.ps1             # Deploy Flask backend
└── AZURE_DEPLOYMENT_GUIDE.md       # Backend deployment guide
```

---

## ✅ Summary

**What happens when user clicks button:**

```
Click "Review with AI Agent"
    ↓
Extension calls: POST /review?work_item_id=1234
    ↓
Backend talks to Azure DevOps (fetches story)
    ↓
Backend asks Groq AI to evaluate story
    ↓
Backend posts comment to work item
    ↓
Popup shows: "✓ Review Completed"
    ↓
All team sees comment on work item
```

**That's it!** No HTML page, no separate UI—everything in Azure DevOps. ✨

---

Need help? Run through the steps above or check the troubleshooting section.
