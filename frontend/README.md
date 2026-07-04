# Sentinel-X Frontend

Client-side cockpit simulation dashboard, authentication gate, and landing page.

**Zero dependencies required to run** — pure HTML5, Vanilla JS, and CDN-loaded libraries.

## Overview

| File | Purpose | Size |
|---|---|---|
| `src/index.html` | Landing page with Three.js particle background | ~32KB |
| `src/auth.html` | Multi-role authentication gate with OTP | ~18KB |
| `src/app.html` | Full 8-panel cockpit dashboard | ~122KB |
| `src/test-suite.html` | Browser-side QA test runner | ~12KB |
| `server/dev-server.ps1` | PowerShell HTTP dev server (port 8000) | ~5KB |
| `server/run.bat` | Windows one-click launcher | ~1KB |

## Running Locally

```powershell
# Windows — one-click
double-click frontend/server/run.bat

# Or manually
cd frontend/server
powershell -ExecutionPolicy Bypass -File dev-server.ps1

# Open browser at http://localhost:8000
```

## Dashboard Panels

The cockpit (`app.html`) includes **8 fully interactive panels**:

### 1. Control Dashboard
- KPI grid: Active workers, gas sensors, machinery vitals, accident predictions
- **2D UWB Floor Map** — Canvas-rendered real-time worker + forklift position tracking with zone breach detection
- **Live Alert Stream** — Real-time color-coded log with Web Audio API sound effects

### 2. 3D Digital Twin
- **Three.js WebGL** factory scene with real FBX warehouse model
- OrbitControls (orbit, pan, zoom)
- **Emergency simulations**: Gas Leak, Boiler Fire, Evacuation
- **Lighting presets**: Sunny, Night, Stormy
- **Camera presets**: Boiler Area, Conveyor Line
- **Time-travel scrubber** for historical scenario replay

### 3. Computer Vision
- 4 simulated CCTV canvases running at ~30 FPS
- **CCTV 01**: Gate PPE compliance check (green bounding boxes)
- **CCTV 02**: Compressor zone intrusion detection (red alarm on breach)
- **CCTV 03**: Conveyor belt asset tracking
- **CCTV 04**: Assembly floor pose estimation + fall detection

### 4. AI Agent Mesh
- Live status board for 4 agents (Vision, Prediction, Route Planner, Emergency)
- **Chain-of-Thought logs** — scrolling agent communication stream
- **AI Oracle Terminal** — interactive command chat:
  - `/status` — Full safety analysis
  - `/leak` — Trigger gas leak simulation
  - `/fire` — Trigger boiler fire simulation
  - `/shutdown` — Issue PLC lockout

### 5. Safety Analytics
- 4 Chart.js panels (Grafana mode):
  - Historical safety rating (line)
  - Gas concentration by zone (bar)
  - Boiler vibration frequency (line)
  - Worker cognitive load/HRV (area)
- Export: PDF, Excel, CSV

### 6. Wearable Cockpit
- Smartwatch face with live heart rate (±1 BPM drift simulation)
- **SOS Broadcast button** — triggers evacuation simulation + alert cascade
- Phone companion mockup with real-time zone risk status

### 7. OpenAPI Console
- Interactive Swagger-style endpoint playground
- Try: `GET /alerts/active`, `GET /sensors/telemetry`, `POST /machine/lockout`

### 8. System Settings
- Sensor threshold configuration (CO2, temperature, vibration, noise)
- Notification dispatch rules (SMS, WhatsApp, PLC auto-shutdown)

## Libraries Used (CDN)

| Library | Version | Purpose |
|---|---|---|
| Tailwind CSS | Latest | Utility-first styling |
| Three.js | r128 | 3D Digital Twin rendering |
| OrbitControls | r128 | Camera navigation |
| FBXLoader | r128 | 3D factory model loading |
| Chart.js | Latest | Analytics charts |
| Lucide Icons | Latest | Clean icon set |
| Google Fonts | — | Outfit + JetBrains Mono |

## Authentication Flow

```
Role Selection → Email + Key Form → Loading State → OTP Screen (pre-filled) → Dashboard
```

Credentials are stored in `sessionStorage` and cleared on logout.

## Demo Credentials

| Role | Email | OTP |
|---|---|---|
| Admin | `admin@sentinel.x` | `094821` |
| Supervisor | `supervisor@sentinel.x` | `384912` |
| Safety Officer | `officer@sentinel.x` | `849127` |
| Worker | `worker@sentinel.x` | `201948` |

## Performance Notes

- The FBX model (`~44MB`) loads over local HTTP — allow 5–15s
- Canvas animations run at `requestAnimationFrame` (60fps target)
- Web Audio API used for alert sounds — may require user gesture to initialize
- Three.js WebGL requires hardware acceleration enabled in browser
