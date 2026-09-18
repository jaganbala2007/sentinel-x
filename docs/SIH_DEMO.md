# 🎯 Sentinel-X Official SIH 2026 Judge Demonstration Guide

**Duration:** 5–7 Minutes  
**Objective:** Prove physical autonomy, Byzantine sensor resilience, zero-loss communication blackout survival, and photo-assisted digital twin generation.  
**Audience:** Technical SIH Judges, Industrial Safety Experts, Disaster Management Evaluators.

---

## 28-Step Interactive Judge Demonstration Script

| Step | Action in SCADA Cockpit (`http://localhost:3000/app.html`) | What the System Does | What the Judge Sees & Verifies |
| :---: | :--- | :--- | :--- |
| **1–4** | Open dashboard; observe baseline state. | Real ESP32 100Hz telemetry ingested by local RPi 5. | Industrial Conveyor operating nominal (`0 Threats`). 3D twin running at 60 FPS. |
| **5–8** | Click **"Next Step: Bearing Wear & Inrush"**. | Injects mechanical vibration (5.8 mm/s) and thermal rise (84°C). | TinyML Autoencoder triggers advisory alert (Anomaly score: 0.78). Trust Engine verifies sensor plausibility. |
| **9–12** | Click **"Next Step: Critical Overload & Trip"**. | Vibration exceeds 7.2 mm/s (ISO 10816 Class II Critical). | **Autonomous relay trip in <800ms**. Conveyor stops, 110dB siren fires, strobe flashes. Incident written to SQLite WAL. |
| **13–16**| Click **"Next Step: Inject Byzantine Spoof"**. | Injects false 180°C glitch into single node. | Trust drops to 12.5% (`QUARANTINED`). **System prevents false plant trip** using remaining trusted sensors. |
| **17–20**| Click **"Next Step: Sever Internet Connection"**. | Simulates total WAN blackout. | Primary status turns red (`FAILED`). System enters **Isolated Autonomous Mode**. Telemetry queued to local SQLite WAL. |
| **21–22**| Click **"Next Step: HF Radio Packet Broadcast"**. | Dispatches emergency packet via HF Radio simulation. | HF simulation generates AX.25 frame with CRC32 and simulated ionospheric propagation. |
| **23–24**| Click **"Next Step: Reconnect Internet & Sync"**. | Internet connection restored. | Store-and-forward queue synchronizes all backlogged incidents without dropping a single sample. |
| **25–28**| Click **"Next Step: Photo Digital Twin Replay"**. | Ingests multi-view field photos via Neural SfM. | Reconstructs watertight 3D digital twin matching the uploaded photos and replays full incident timeline. |

---

## Final Demonstration Badge Summary

At the conclusion of Step 28, the cockpit displays:

$$\boxed{\text{DETECTED} \quad\bullet\quad \text{VERIFIED} \quad\bullet\quad \text{PROTECTED} \quad\bullet\quad \text{STORED} \quad\bullet\quad \text{COMMUNICATED} \quad\bullet\quad \text{RECONSTRUCTED}}$$
