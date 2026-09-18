Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "              SENTINEL-X DISASTER INTELLIGENCE PLATFORM" -ForegroundColor White
Write-Host "                   Smart India Hackathon 2026" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan

$PythonExe = "C:\Users\jagan\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path $PythonExe)) {
    $PythonExe = "python"
}

$RootDir = $PSScriptRoot
if (-not $RootDir) { $RootDir = Get-Location }

Write-Host "[*] Starting FastAPI Backend on http://localhost:8080 ..." -ForegroundColor Yellow
Start-Process -FilePath $PythonExe -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload --app-dir backend" -WorkingDirectory $RootDir

Start-Sleep -Seconds 3

Write-Host "[*] Starting Node.js Frontend on http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process -FilePath "node" -ArgumentList "server.js" -WorkingDirectory (Join-Path $RootDir "frontend")

Start-Sleep -Seconds 1
Write-Host "[*] Opening Cockpit Dashboard..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host "`nSentinel-X is running!" -ForegroundColor Cyan
Write-Host "  - Cockpit Dashboard: http://localhost:3000"
Write-Host "  - REST API & Swagger: http://localhost:8080/docs"
Write-Host "  - SIH 2026 23-Step Demo: http://localhost:8080/api/v1/sih-demo/steps"
