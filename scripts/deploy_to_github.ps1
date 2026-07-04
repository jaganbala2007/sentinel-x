# Sentinel-X GitHub Deployment Automation Script
# This script helps initialize Git, commit files, and push to your GitHub repository.
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File deploy_to_github.ps1

$githubUsername = "jaganbala2007"
$repoName = "sentinel-x"
$remoteUrl = "https://github.com/$githubUsername/$repoName.git"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   SENTINEL-X GITHUB DEPLOYMENT UTILITY" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Git is not installed or not in your system PATH." -ForegroundColor Red
    Write-Host "Please download and install Git from: https://git-scm.com/" -ForegroundColor Yellow
    Write-Host "After installing, restart your terminal and run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Git detected." -ForegroundColor Green

# 2. Check if .git is initialized
if (!(Test-Path "../.git")) {
    Write-Host "[INFO] Initializing new Git repository..." -ForegroundColor Yellow
    git init -b main
} else {
    Write-Host "[INFO] Git repository already initialized." -ForegroundColor Green
}

# 3. Configure Git credentials if needed
$gitUser = git config user.name
if ($null -eq $gitUser -or $gitUser -eq "") {
    Write-Host "[INFO] Setting up default Git config..." -ForegroundColor Yellow
    git config user.name "jaganbala2007"
    git config user.email "jaganbala2007@github.com"
}

# 4. Add remote origin if it doesn't exist
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host "[INFO] Adding remote origin: $remoteUrl" -ForegroundColor Yellow
    git remote add origin $remoteUrl
} else {
    Write-Host "[INFO] Remote origin already exists." -ForegroundColor Green
    # Update origin URL just in case
    git remote set-url origin $remoteUrl
}

# 5. Create Git Commits
# We will do this in structured stages to demonstrate professional Git history
Write-Host "[INFO] Creating professional commit history..." -ForegroundColor Yellow

# Stage 1: Initial files and documentation
git add ../.gitignore ../LICENSE ../README.md ../docs/ ../assets/
git commit -m "chore: initial project structure and documentation setup"

# Stage 2: Community standard files
git add ../.github/ ../CODE_OF_CONDUCT.md ../CONTRIBUTING.md ../SECURITY.md ../CHANGELOG.md ../ROADMAP.md ../FAQ.md ../CODEOWNERS
git commit -m "docs: add GitHub community files, templates, and roadmap"

# Stage 3: Frontend source code
git add ../frontend/
git commit -m "feat: add client-side 3D Digital Twin simulation cockpit"

# Stage 4: Rest of the files
git add ../backend/ ../hardware/ ../firmware/ ../models/ ../datasets/ ../tests/ ../scripts/ ../deployment/
git commit -m "feat: setup architectures and module placeholders for hardware and AI edge mesh"

# 6. Prompt to Push
Write-Host ""
Write-Host "Repository commits are created locally." -ForegroundColor Green
Write-Host "Run the following command to push to your GitHub repository:" -ForegroundColor Yellow
Write-Host "git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you get authentication errors, please make sure you have created" -ForegroundColor Gray
Write-Host "the repository '$repoName' on your GitHub account: https://github.com/new" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan
