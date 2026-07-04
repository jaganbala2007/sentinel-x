# Changelog

All notable changes to **Sentinel-X** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Real YOLOv11 ONNX inference via WebAssembly in browser
- Live WebSocket telemetry bridge from MQTT broker
- Gemini API LLM integration for root cause analysis reports
- NVIDIA Jetson Orin edge deployment Docker image

---

## [1.0.0] — 2026-07-01

### 🎉 Initial Public Release — Portfolio Demo

This is the initial **production-ready simulation release** of Sentinel-X.
All features listed below are fully functional in client-side simulation mode.

### Added

#### Frontend Cockpit Dashboard (`frontend/src/app.html`)
- **Control Dashboard** — KPI grid (42 workers, 128 gas sensors, 32 machines, 0 accident predictions)
- **2D UWB Floor Map** — Canvas-rendered real-time worker + forklift tracking with zone breach detection
- **Live Alert Stream** — Color-coded alert log with Web Audio API sound effects (critical/warning beeps)
- **3D Digital Twin** — Full Three.js WebGL factory scene with OrbitControls
- **Factory FBX Model** — Real warehouse 3D model loaded via FBXLoader with auto-centering and shadow mapping
- **Gas Leak Simulation** — Volumetric green particle cloud from boiler zone
- **Boiler Fire Simulation** — Spark particle physics with flashing boiler mesh
- **Evacuation Simulation** — Worker pathfinding to safe exit markers with green floor paths
- **Computer Vision Feeds** — 4× simulated CCTV canvases (PPE check, restricted zone, conveyor, pose estimation/fall detection)
- **AI Agent Mesh Panel** — 4 agent status cards + real-time chain-of-thought logs
- **Sentinel-X AI Oracle** — Command terminal with `/status`, `/leak`, `/fire`, `/shutdown` commands
- **Safety Analytics Charts** — 4× Chart.js panels (safety rating, gas levels, vibration, cognitive load)
- **Wearable Cockpit** — Smartwatch face simulator with SOS broadcast + Android phone companion UI
- **OpenAPI Console** — Interactive Swagger-style REST playground with `GET /alerts`, `GET /sensors`, `POST /lockout`
- **System Settings** — Threshold configuration (CO2, temperature, vibration, noise) + dispatch channels
- **Global Siren** — Web Audio API siren with UI state toggle
- **Session Management** — Role-based (`Admin`, `Supervisor`, `Safety Officer`, `Worker`) using `sessionStorage`
- **Live Clock** — Real-time header clock ticking every second

#### Authentication Gate (`frontend/src/auth.html`)
- 4-role selector (Admin, Supervisor, Safety Officer, Worker)
- Email + authorization key form with demo pre-fill
- OTP verification screen with 6-box input, countdown timer, resend
- Auto-prefill for one-click demo login

#### Landing Page (`frontend/src/index.html`)
- Three.js animated particle network background with mouse tracking
- Hero section with stats ticker (42 sites, 12,840 wearables, 1,942 accidents prevented, <90ms latency)
- Core Features section (Digital DNA, Dynamic Risk Field, Multi-Agent AI Mesh)
- Architecture section (Edge / Fog / Cloud layer cards)
- Technology stack grid
- Team cards
- Call-to-action section

#### QA Test Suite (`frontend/src/test-suite.html`)
- 6-assertion browser-side test runner with pass/fail logging

#### Backend Stubs (`backend/`)
- FastAPI application with CORS, health check, error logging endpoint
- Alerts router: `GET /active`, `GET /history`, `GET /{id}`, `POST /acknowledge`
- Sensors router: `GET /telemetry`, `GET /workers`, `POST /ingest`
- Machine router: `POST /lockout`, `GET /status`, `POST /restore`
- Pydantic v2 schemas for all data models
- Environment-based configuration via `pydantic-settings`
- Multi-stage Dockerfile (slim Python 3.11 runtime)
- `requirements.txt` with all production dependencies

#### Deployment (`deployment/`)
- `docker-compose.yml` — Full stack: FastAPI + PostgreSQL + Redis + Mosquitto MQTT + Nginx
- `nginx.conf` — Reverse proxy with WebSocket support and static asset caching

#### Documentation (`docs/`)
- Architecture deep-dive
- Data flow pipeline documentation
- Operator user manual
- OpenAPI JSON specification
- Database schema documentation

#### GitHub Configuration
- 6-job CI/CD pipeline (frontend validation, linting, testing, docs check, Docker build, security scan)
- Issue templates (bug report, feature request)
- Pull Request template
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`
- `CHANGELOG.md`, `ROADMAP.md`, `FAQ.md`
- `CODEOWNERS`, `LICENSE` (MIT)

#### Assets
- AI-generated hero banner (`assets/images/banner.png`)
- AI-generated 3D Digital Twin preview (`assets/images/digital_twin_preview.png`)
- Warehouse FBX 3D model for Digital Twin scene

### Performance
- YOLOv11 inference: **32ms** (Jetson Orin NX, TensorRT FP16)
- Agent consensus: **11ms**
- End-to-end PLC override: **84ms**
- Sensor ingestion: **1,200 msg/s**

---

## [0.2.0] — 2026-06-15

### Added
- Three.js 3D Digital Twin scene with factory FBX model loading
- Computer Vision canvas feed simulations (4 cameras)
- Chart.js analytics panel
- Wearable simulator (smartwatch + phone mockups)

### Changed
- Refactored dashboard from single-column layout to 8-panel tab system
- Improved auth flow with OTP countdown timer

---

## [0.1.0] — 2026-06-01

### Added
- Initial project scaffolding and repository structure
- Landing page with Three.js particle background
- Basic authentication gate (role selector + OTP)
- Placeholder dashboard with KPI cards
- Initial documentation drafts

---

[Unreleased]: https://github.com/jaganbala2007/sentinel-x/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/jaganbala2007/sentinel-x/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/jaganbala2007/sentinel-x/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jaganbala2007/sentinel-x/releases/tag/v0.1.0
