# Sentinel-X Scripts

Utility and DevOps automation scripts.

## Scripts

| Script | Platform | Purpose |
|---|---|---|
| `deploy_to_github.ps1` | PowerShell | Initialize Git, structured commits, push to GitHub |
| `frontend/server/dev-server.ps1` | PowerShell | Local HTTP server for frontend development |
| `frontend/server/run.bat` | Windows Batch | One-click frontend launcher |

## Usage

### Deploy to GitHub

```powershell
# Run from scripts/ directory
cd scripts
powershell -ExecutionPolicy Bypass -File deploy_to_github.ps1
```

This script:
1. Initializes Git if not already done
2. Configures Git user identity
3. Adds GitHub remote origin
4. Creates structured commits in stages
5. Prompts you to push

### Local Dev Server

```powershell
cd frontend/server
powershell -ExecutionPolicy Bypass -File dev-server.ps1
# Opens http://localhost:8000
```
