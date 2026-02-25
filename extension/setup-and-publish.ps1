#!/usr/bin/env powershell
# Azure DevOps Extension - Quick Setup and Publish Script

Write-Host "========================================"
Write-Host "Story Validator - Extension Setup"
Write-Host "========================================"

# Check if Node.js is installed
Write-Host "`n[*] Checking Node.js..."
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Node.js not found. Install from: https://nodejs.org/"
    exit 1
}
Write-Host "[+] Node.js found"

# Install tfx-cli globally
Write-Host "`n[1/4] Installing tfx-cli (extension packaging tool)..."
npm install -g tfx-cli
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Failed to install tfx-cli"
    exit 1
}
Write-Host "[+] tfx-cli installed"

# Create extension package
Write-Host "`n[2/4] Creating extension package..."
tfx extension create --manifest-globs vss-extension.json --rev-version
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to create extension package"
    exit 1
}
Write-Host "[+] Extension package created"

# Ask for publishing
Write-Host "`n[3/4] Ready to publish?"
$publish = Read-Host "Publish to Azure DevOps Marketplace? (y/n)"

if ($publish -eq "y" -or $publish -eq "yes") {
    $token = Read-Host "Enter your Azure DevOps Personal Access Token"
    $publisher = Read-Host "Enter your publisher name (e.g., StoryValidatorOrg)"
    
    Write-Host "`nPublishing extension..."
    tfx extension publish --manifest-globs vss-extension.json --publisher $publisher --auth-type pat --token $token
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] Extension published successfully!"
        Write-Host "Install at: https://marketplace.visualstudio.com/publishers/$publisher"
    } else {
        Write-Host "[ERROR] Publishing failed"
    }
} else {
    Write-Host "`nSkipped publishing. Package created but not published."
    Write-Host "To publish later, re-run this script."
}

Write-Host "`n========================================"
Write-Host "Setup complete!"
Write-Host "========================================"
