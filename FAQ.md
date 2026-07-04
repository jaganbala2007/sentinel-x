# Sentinel-X — Frequently Asked Questions

A curated list of questions from developers, recruiters, and industrial engineers.

---

## 🤔 General

### What is Sentinel-X?

Sentinel-X is an AI Cognitive Safety Operating System for industrial environments. It creates a real-time 3D Digital Twin of a factory floor, tracks workers and machinery using IoT sensors, and uses a multi-agent AI mesh to predict and prevent accidents — with safety overrides executing in under 100 milliseconds.

### Is this a real product or a demo?

The current repository (`v1.0.0`) is a **production-quality simulation** built to showcase the system architecture, technology choices, and engineering depth. All frontend features run 100% client-side with simulated data. The FastAPI backend provides real, documented REST endpoints with mock data.

The core innovation (Digital DNA profiling, Dynamic Risk Fields, Multi-Agent Mesh) is technically validated and architecturally sound — designed to run on real NVIDIA Jetson Orin hardware.

### Why build this?

> Industrial workplace accidents kill **2.3 million people per year** globally. Current safety systems react *after* incidents — Sentinel-X predicts them *before*.

### What makes Sentinel-X different from existing industrial safety systems?

| Feature | Sentinel-X | Traditional Systems |
|---|---|---|
| Incident response | Predictive (15min ahead) | Reactive (after incident) |
| Machine shutdown | < 100ms edge decision | > 500ms cloud roundtrip |
| Vision integration | YOLOv11 PPE + pose AI | Manual camera monitoring |
| Worker tracking | UWB 3D indoor positioning | No location awareness |
| System awareness | Unified 3D Digital Twin | Siloed per-sensor dashboards |

---

## 🚀 Running the Project

### How do I run the frontend simulation?

```powershell
git clone https://github.com/jaganbala2007/sentinel-x.git
cd sentinel-x/frontend/server
powershell -ExecutionPolicy Bypass -File dev-server.ps1
# Open http://localhost:8000
```

No Node.js, Python, or internet required.

### What are the demo login credentials?

| Role | Email | OTP |
|---|---|---|
| Admin | `admin@sentinel.x` | `094821` |
| Supervisor | `supervisor@sentinel.x` | `384912` |
| Safety Officer | `officer@sentinel.x` | `849127` |
| Worker | `worker@sentinel.x` | `201948` |

All credentials and OTPs are pre-filled — just click through.

### How do I start the FastAPI backend?

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8080
# Swagger UI: http://localhost:8080/docs
```

### How do I deploy the full stack?

```bash
docker-compose -f deployment/docker-compose.yml up -d
# Frontend: http://localhost:8000
# Backend API: http://localhost:8080/docs
```

### The 3D Digital Twin is loading slowly — what should I do?

The factory FBX model (`assets/3d_models/factory/1/uploads_files_2883707_warehouse6.fbx`) is ~44MB. It loads over HTTP from your local server. Ensure:
- The `dev-server.ps1` is running from the correct directory
- Use Chrome or Edge for best WebGL performance
- Loading typically completes within 5–15 seconds on local network

---

## 🤖 Technical Questions

### What is the Multi-Agent Consensus Protocol?

Four specialized agents (Vision, Prediction, Route Planner, Emergency Response) run on the fog-layer edge node. They communicate via shared memory and a lightweight priority-queue protocol. When a hazard is detected:

1. Vision AI raises a detection event
2. Prediction AI computes risk probability
3. Route Planner pre-computes evacuation paths
4. Emergency Agent issues a Modbus/TCP lockout command

Total time from detection to PLC override: **< 100ms**.

### Why Modbus/TCP for machine control?

Modbus is the dominant industrial protocol — supported by virtually every PLC (Siemens S7, Allen Bradley, Schneider, etc.) and requires no vendor lock-in. Its simplicity also minimizes attack surface in OT (Operational Technology) environments.

### What is the Digital DNA Fatigue Coefficient™?

A proprietary scalar value (0.0 = alert, 1.0 = critically fatigued) computed from:
- Heart rate variability (HRV) from smart helmet sensors
- Blood oxygen saturation (SpO2)
- Time-on-floor duration
- Historical incident proximity
- Task cognitive load classification

Workers above a threshold trigger precautionary reassignment alerts.

### Why Three.js for the Digital Twin?

- **No Unity/Unreal licensing cost** — runs in any browser
- **WebGL 2.0** standard support across all modern devices
- **GLTF/FBX asset pipeline** compatible with standard 3D tools
- **Real-time rendering** sufficient for 3D facility visualization at 60fps
- **No plugin installation** required for end users (supervisors, safety officers)

### Can this run offline / without internet?

Yes — the edge/fog layer is designed for air-gapped operation. The fog node (NVIDIA Jetson) runs all safety-critical AI inference locally. Cloud connectivity is only needed for:
- Long-term analytics storage
- AI model updates
- Multi-site federation
- Supervisor remote access

---

## 🏭 Industrial Questions

### What sensors does Sentinel-X support?

| Sensor Type | Protocol | Data |
|---|---|---|
| Gas detector (CO2, H2S, LEL) | 4-20mA → MQTT | PPM concentration |
| Temperature sensor | LoRaWAN | °C continuous |
| Vibration (accelerometer) | Modbus RTU | Hz frequency |
| Noise level | Analog → MQTT | dB |
| Smart Helmet (HR, SpO2) | BLE 5.2 | bpm, % |
| Indoor positioning | UWB (DW3000) | x,y,z coordinates |
| IP Camera | RTSP | H.264 video stream |

### Is Sentinel-X OSHA compliant?

The system is **designed to support** OSHA 1910 and 1926 compliance:
- Automated hazardous zone enforcement
- PPE detection and alerting
- Incident documentation with timestamped logs
- Evacuation route management

Full OSHA certification requires site-specific validation and is planned for v3.0.

### What is the hardware cost estimate?

| Component | Approx. Cost (USD) |
|---|---|
| NVIDIA Jetson Orin NX 16GB | $499 |
| Smart Helmet (custom BLE/UWB) | $120/unit |
| Gas Detector Array (4 sensors) | $800 |
| LoRaWAN Gateway | $200 |
| IP Camera (4K RTSP) | $150/unit |
| Industrial Switch + Cabling | $300 |
| **Total (small site, 10 workers)** | **~$4,500** |

---

## 🤝 Contributing

### How do I contribute?

See our full [Contributing Guide](CONTRIBUTING.md). We welcome bug fixes, documentation improvements, new test cases, and AI/ML enhancements.

### Can I use Sentinel-X in my own project?

Yes — it's MIT licensed. Free to use, modify, and distribute with attribution. See [LICENSE](LICENSE).

### Can I cite Sentinel-X in a research paper?

Absolutely. Please use:

```bibtex
@software{sentinelx2026,
  author = {Bala, Jagan},
  title = {Sentinel-X: AI Cognitive Safety Operating System},
  year = {2026},
  url = {https://github.com/jaganbala2007/sentinel-x},
  version = {1.0.0}
}
```

---

*Have a question not answered here? [Open a Discussion](https://github.com/jaganbala2007/sentinel-x/discussions).*
