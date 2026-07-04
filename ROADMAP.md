# Sentinel-X Roadmap

This document outlines the planned development trajectory for Sentinel-X from the current simulation release through full enterprise production deployment.

> ✅ Completed &nbsp;|&nbsp; 🚧 In Progress &nbsp;|&nbsp; 📋 Planned &nbsp;|&nbsp; 🔬 Research

---

## Phase 1 — Foundation (v1.0.x) ✅ COMPLETE

*Target: Q2 2026 — Portfolio simulation release*

| Feature | Status | Notes |
|---|---|---|
| Three.js 3D Digital Twin (client-side) | ✅ | Full FBX model, OrbitControls, simulations |
| Multi-role authentication gate + OTP | ✅ | 4 roles, session management |
| 2D UWB floor map with live tracking | ✅ | Canvas-rendered, zone breach detection |
| 4× Simulated CCTV YOLOv11 feeds | ✅ | PPE, restricted zone, conveyor, fall detection |
| AI Agent Mesh panel + Oracle terminal | ✅ | Commands: /status /leak /fire /shutdown |
| Chart.js safety analytics (Grafana mode) | ✅ | 4 chart types, CSV/PDF/Excel export |
| Wearable simulator (smartwatch + phone) | ✅ | SOS broadcast, biometric vitals |
| OpenAPI interactive console | ✅ | Swagger-style with mock response payloads |
| FastAPI backend stubs (all 3 routers) | ✅ | Alerts, Sensors, Machine Control |
| Docker Compose full-stack deployment | ✅ | FastAPI + PostgreSQL + Redis + MQTT + Nginx |
| 6-job GitHub Actions CI/CD pipeline | ✅ | Lint, test, docs, Docker, security |
| Professional documentation suite | ✅ | Architecture, API, manual, data flow, DB schema |

---

## Phase 2 — Real AI Integration (v1.1 — v1.3)

*Target: Q3 2026*

| Feature | Status | Notes |
|---|---|---|
| **v1.1** YOLOv11 ONNX via WebAssembly | 📋 | Run real inference in-browser using `ort-web` |
| **v1.1** Live webcam PPE detection demo | 📋 | Browser camera → YOLOv11 → bounding boxes |
| **v1.2** MQTT → WebSocket live telemetry bridge | 📋 | Real sensor data to cockpit via FastAPI WebSocket |
| **v1.2** PostgreSQL real alert persistence | 📋 | Replace mock data with Alembic migrations |
| **v1.2** Redis telemetry cache layer | 📋 | 30s TTL with real sensor writes |
| **v1.3** Gemini API LLM root cause analysis | 📋 | Auto-generate incident reports from telemetry |
| **v1.3** JWT role-based authentication | 📋 | Replace sessionStorage with proper JWT tokens |
| **v1.3** Expanded OpenAPI test suite | 📋 | 20+ pytest cases with mock fixtures |

---

## Phase 3 — Edge Hardware Deployment (v2.0)

*Target: Q4 2026*

| Feature | Status | Notes |
|---|---|---|
| **v2.0** NVIDIA Jetson Orin NX deployment stack | 📋 | JetPack 6.0, TensorRT FP16 optimization |
| **v2.0** YOLOv11 TensorRT engine conversion | 📋 | `.pt → .engine` for 32ms inference |
| **v2.0** Modbus/TCP PLC integration | 📋 | Real Siemens S7-1200 machine override |
| **v2.0** Multi-Agent Mesh C++ consensus engine | 🔬 | Distributed edge consensus < 15ms |
| **v2.0** UWB indoor positioning integration | 📋 | DW3000 module, TDOA algorithm |
| **v2.0** LoRaWAN environmental sensor gateway | 📋 | Dragino LA66, CO2/H2S ingestion |
| **v2.0** MQTT Mosquitto production broker | 📋 | TLS, ACL, clustering |
| **v2.1** Smart Helmet BLE firmware (Zephyr RTOS) | 🔬 | Heart rate, SpO2, UWB, fall detection |
| **v2.1** WearOS smartwatch companion app | 📋 | SOS broadcast, vitals push |
| **v2.1** Android/iOS field worker app | 📋 | Zone risk warnings, navigation |

---

## Phase 4 — Enterprise & Compliance (v3.0)

*Target: 2027*

| Feature | Status | Notes |
|---|---|---|
| **v3.0** ATEX Zone 1 certified enclosures | 🔬 | IECEx/ATEX for explosive environments |
| **v3.0** ISO 45001:2018 compliance module | 📋 | Automated OSHA/ISO report generation |
| **v3.0** Predictive maintenance (acoustic ML) | 🔬 | Bearing wear detection via vibration FFT |
| **v3.0** Digital twin synchronization engine | 📋 | BIM → Three.js auto-import pipeline |
| **v3.0** Multi-site federation | 📋 | Central command for multiple factory instances |
| **v3.0** Kubernetes horizontal scaling | 📋 | K8s HPA, Helm charts, multi-region |
| **v3.0** SOC 2 Type II audit preparation | 🔬 | Security, availability, confidentiality |

---

## Research Directions

| Topic | Priority | Description |
|---|---|---|
| Digital DNA Fatigue Coefficient™ | 🔬 High | Validated biometric model for cognitive fatigue prediction |
| Dynamic Risk Field probabilistic model | 🔬 High | Bayesian risk grid with spatial-temporal correlation |
| Federated learning across factories | 🔬 Medium | Privacy-preserving model improvement across customer sites |
| Acoustic bearing fault detection | 🔬 Medium | MFCC + LSTM for predictive maintenance |
| LLM-powered incident root cause analysis | 📋 Medium | Fine-tuned safety-domain LLM on incident databases |

---

## Release Schedule

```
v1.0.0  ─── Jul 2026 ─── ✅ Portfolio simulation release
v1.1.0  ─── Aug 2026 ─── 📋 YOLOv11 WebAssembly browser inference
v1.2.0  ─── Sep 2026 ─── 📋 Live MQTT telemetry + PostgreSQL
v1.3.0  ─── Oct 2026 ─── 📋 Gemini LLM integration + JWT auth
v2.0.0  ─── Dec 2026 ─── 📋 Full Jetson Orin edge hardware stack
v2.1.0  ─── Feb 2027 ─── 📋 Smart Helmet firmware + wearable apps
v3.0.0  ─── Jul 2027 ─── 📋 Enterprise compliance + multi-site
```

---

*Want to contribute to a specific phase? See [CONTRIBUTING.md](CONTRIBUTING.md).*  
*Have a feature idea? Open a [Feature Request](https://github.com/jaganbala2007/sentinel-x/issues/new?template=feature_request.md).*
