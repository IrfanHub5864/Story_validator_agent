# 🎯 Story Validator - Azure DevOps Extension

Built-in button on Azure DevOps work item page to review stories with AI Agent.

## 📋 What This Does

1. **Adds a button** to every Azure DevOps work item page
2. **One click review** → AI evaluates the story automatically
3. **Popup shows status** → "Review Completed"
4. **Permanent comment** posted to work item (visible to all team members)

## 🚀 Installation & Deployment

### Step 1: Install TFX CLI (one-time setup)

```powershell
npm install -g tfx-cli
```

### Step 2: Create Icon (Optional)

Create a simple 128x128 PNG image and save as `extension/img/extension-icon.png`

Or use this placeholder by running:
```powershell
cd extension
mkdir -p img
```

### Step 3: Publish to Azure DevOps Marketplace

You need:
- **Publisher Name** (unique identifier for your organization)
- **Azure DevOps Personal Access Token** (with "Manage extensions" scope)

#### Create Access Token:
1. Go to: https://dev.azure.com/_usersettings/tokens
2. Click "New Token"
3. Name: `ExtensionPublisher`
4. Scopes: Check **Manage extensions**
5. Copy the token

#### Publish Command:

```powershell
cd extension

# First time - create publisher
tfx extension create `
  --manifest-globs vss-extension.json `
  --publisher StoryValidatorOrg

# To publish (requires token)
tfx extension publish `
  --manifest-globs vss-extension.json `
  --publisher StoryValidatorOrg `
  --token <YOUR_PAT_TOKEN>
```

### Step 4: Install in Your Azure DevOps Organization

1. Go to: https://marketplace.visualstudio.com → Your Publisher
2. Find "Story Validator - AI Review"
3. Click "Install" → Select organization → Confirm

### Step 5: Configure Extension Settings

Once installed:
1. Go to your Azure DevOps project
2. **Project Settings** → **Extensions** → **Story Validator - AI Review**
3. Configure:
   - **API URL**: `https://app-story-validator.azurecontainerapps.io` (or your Flask app URL)
   - **API Key**: (leave empty if not using authentication)

---

## 🧪 Testing Locally

For local development/testing:

### Option A: Without Publishing (Local Dev)

The extension can be loaded locally using Azure DevOps Extensions Development Tool.

1. Install dev tool:
```powershell
npm install -g vss-extension-dev
```

2. Create a manifest for development:
```powershell
cd extension
```

3. Run local server pointing to your Flask backend (app.py running on port 8000)

### Option B: Test with Deployed App

1. Deploy your Flask app to Azure (using `deploy-to-azure.ps1`)
2. Update `vss-extension.json` with production API URL
3. Publish extension to marketplace
4. Install in organization

---

## 🔌 How It Works

```
User opens work item → Button appears in toolbar
                    ↓
User clicks button → Extension shows loading popup
                    ↓
JavaScript calls Flask API (/review endpoint)
                    ↓
Backend fetches story from Azure DevOps
                    ↓
AI (Groq) evaluates the story
                    ↓
Backend posts comment to work item (marked as reviewed)
                    ↓
Popup shows "Review Completed"
                    ↓
All team members see the comment on work item
```

---

## 📁 Extension Structure

```
extension/
├── vss-extension.json          # Extension manifest
├── src/
│   ├── work-item-review.html   # Button UI & popup
│   └── work-item-review.js     # Logic & API calls
├── img/
│   └── extension-icon.png      # Icon (optional)
└── README.md                   # This file
```

---

## ⚙️ Configuration

Your Flask backend (`app.py`) must be running with:

```
REVIEW_API_KEY=my-secret-123
AZURE_PAT=<your-azure-devops-pat>
GROQ_API_KEY=<your-groq-api-key>
AZURE_ORG_URL=https://dev.azure.com/YourOrg/
AZURE_PROJECT=YourProject
PORT=8000
```

---

## 🐛 Troubleshooting

### Button doesn't appear
- Check extension is installed in organization
- Refresh Azure DevOps page (F5)
- Check browser console for errors

### API call fails
- Verify Flask app is running
- Check API URL in extension settings
- Ensure API Key is correct (if configured)
- Check browser console network tab

### Review not posted to work item
- Verify Azure PAT token is valid
- Check Flask logs for errors
- Verify project/organization names in .env

---

## 📦 Publishing to Private Marketplace

If you want to keep extension private:

```powershell
tfx extension publish `
  --manifest-globs vss-extension.json `
  --publisher StoryValidatorOrg `
  --token <YOUR_PAT_TOKEN> `
  --share-with <ORG_NAME>
```

---

## 🔐 Security Notes

- Never commit API keys to repo
- Use environment variables for sensitive data
- Consider IP whitelisting if backend is exposed
- Test API authentication thoroughly

---

**Ready to deploy?** Start with Step 1! 🚀
