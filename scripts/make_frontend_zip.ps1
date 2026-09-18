$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

Add-Type -AssemblyName System.IO.Compression.FileSystem

$workspace = "e:\tata updated\tata"
$stageDir = Join-Path $workspace "sentinel-x-frontend"
$zipPath = Join-Path $workspace "sentinel-x-frontend.zip"

Write-Host "Creating staging directory: $stageDir"
if (Test-Path $stageDir) {
    Remove-Item -Recurse -Force $stageDir
}
New-Item -ItemType Directory -Path $stageDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $stageDir "src") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $stageDir "server") -Force | Out-Null

Write-Host "Copying frontend files..."
# Root standalone files for direct double-clicking
Copy-Item (Join-Path $workspace "frontend\src\index.html") (Join-Path $stageDir "index.html")
Copy-Item (Join-Path $workspace "frontend\src\app.html") (Join-Path $stageDir "app.html")
Copy-Item (Join-Path $workspace "frontend\src\twin-engine.js") (Join-Path $stageDir "twin-engine.js")
Copy-Item (Join-Path $workspace "frontend\src\auth.html") (Join-Path $stageDir "auth.html")
Copy-Item (Join-Path $workspace "frontend\src\test-suite.html") (Join-Path $stageDir "test-suite.html")
Copy-Item (Join-Path $workspace "frontend\server.js") (Join-Path $stageDir "server.js")
Copy-Item (Join-Path $workspace "frontend\package.json") (Join-Path $stageDir "package.json")

# Copy src/ folder files
Get-ChildItem -Path (Join-Path $workspace "frontend\src") -File | Where-Object { $_.Extension -ne ".bak" } | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $stageDir "src\$($_.Name)")
}

# Copy server scripts
if (Test-Path (Join-Path $workspace "frontend\server")) {
    Copy-Item (Join-Path $workspace "frontend\server\*") (Join-Path $stageDir "server") -Recurse
}

# Add standalone Quick Start Guide
$readme = @"
# SENTINEL-X FRONTEND BUNDLE
**Autonomous Multi-Hazard Resilience & Industrial Safety Digital Twin**
*SIH 2026 Hardware Product Experience*

---

## 🚀 How to Run & Edit

### Option 1: Direct Double-Click (Zero Setup)
- Double-click **``index.html``** to open the **9-Screen Landing Experience & 3D Spatial Twin**.
- Double-click **``app.html``** to open the **Industrial Operator Cockpit & SCADA Twin**.
- Tailwind CSS and Three.js r128 load automatically via CDN without needing any build tools.

### Option 2: Live Server in VS Code
1. Open this folder in VS Code.
2. Right-click ``index.html`` or ``app.html`` -> **Open with Live Server**.

### Option 3: Full Node.js Proxy Server
1. Open terminal inside this folder.
2. Run:
   ```bash
   npm install
   node server.js
   ```
3. Open `http://localhost:3000` in your browser.
   - Automatically reverse-proxies `/api` and `/ws` to the Python FastAPI backend on `http://127.0.0.1:8080`.

---

## 📁 File Structure
- **`index.html`**: Complete 9-Screen Cinematic Industrial Experience (Verbatim Section 56 copy, interactive trust matrix, spoofing sandbox, ThreeUI spatial depth field).
- **`app.html`**: Operator Command Cockpit (Explainable AI "Why is this happening?", physical 40°C–98°C slider, 4 fault-injection drills, 20-step SIH demo wizard).
- **`twin-engine.js`**: Pure Three.js 3D Digital Twin Engine (Conveyor, motor, sensors, spatial coordinate wave depth field, zero heavy framework dependencies).
- **`auth.html`**: Role-based authentication interface.
- **`test-suite.html`**: Interactive sensor resilience verification tool.
- **`server.js`**: Node.js Express static server + reverse proxy to FastAPI backend.
- **`src/`**: Duplicate source tree for standard module structures.
"@

$readme | Out-File -FilePath (Join-Path $stageDir "README.md") -Encoding utf8

Write-Host "Creating ZIP archive at: $zipPath"
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

[System.IO.Compression.ZipFile]::CreateFromDirectory($stageDir, $zipPath)

$item = Get-Item $zipPath
Write-Host "ZIP created successfully: $($item.FullName) ($([math]::Round($item.Length / 1KB, 2)) KB)"
