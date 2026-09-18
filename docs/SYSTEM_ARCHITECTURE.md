# 📐 Sentinel-X System Architecture

**Document Version:** 2.4.0 (SIH 2026 Canonical Specification)  
**System Identity:** Autonomous Multi-Hazard Resilience and Emergency Communication Platform  
**Core Axiom:** *When infrastructure fails, safety must continue.*

---

## 1. Canonical End-to-End System Flow

```
PHYSICAL ENVIRONMENT
        ↓
DISTRIBUTED SENSOR NODES (PT100, ADXL345, ACS712, VL53L1X, MQ135)
        ↓
ESP32-S3 EDGE SENSOR LAYER (100Hz Sampling, WDT, SECP256R1 Signing)
        ↓
SENSOR VALIDATION (Physical Plausibility, Range & Rate Limits)
        ↓
SENSOR TRUST ENGINE (Z-Score, Cross-Sensor Confirmation, Byzantine Quarantine)
        ↓
ANOMALY / TINYML ENGINE (Advisory Autoencoder & 1D-CNN Anomaly Scores 0.0–1.0)
        ↓
MULTI-SENSOR EVIDENCE FUSION (Bayesian/Dempster-Shafer Confidence Weighted)
        ↓
DETERMINISTIC SAFETY & RISK ENGINE (Rule-Based ISO 13849 Threshold State Machine)
        ↓
AUTONOMOUS LOCAL SAFETY RESPONSE (415V Relay Trip in <800ms, 110dB Siren, Strobe)
        ↓
LOCAL DATA PERSISTENCE (SQLite WAL Ring Buffer + Secondary USB Blackbox)
        ↓
COMMUNICATION RESILIENCE MANAGER (Priority: Internet → HF Packet Radio → Sat → Offline)
        ↓
MISSION COMMAND CENTER & SCADA COCKPIT
        ↓
OPERATIONAL DIGITAL TWIN (Three.js 60 FPS WebGL Engine)
        ↓
INCIDENT RECONSTRUCTION & FORENSICS (Poisson Surface Replay)
```

---

## 2. Layer-by-Layer Architectural Breakdown

### 2.1 Tier 1: Physical Environment & Sensor Probes
- Industrial machinery (induction drive motors, helical gear reducers, spherical roller bearings, conveyor belts).
- Environmental basins (river watersheds, flash flood drainage sumps, dam monoliths, high-altitude mountain posts).
- Multi-modal physical transducers:
  - **Thermal:** PT100 RTD 4-wire bridge / MLX90614 contactless infrared.
  - **Kinematic & Acoustic:** ADXL345 / ADXL355 3-axis high-g accelerometers (0.1–2000 Hz).
  - **Electrical:** ACS712 / SCT-013 Hall-effect current transformers (0–100A RMS).
  - **Spatial:** VL53L1X Time-of-Flight LiDAR barrier (0.05–4.0m range).
  - **Atmospheric / Fire:** MQ135 toxic gas electrochemical probe + IR optical particulate smoke sensors.

### 2.2 Tier 2: ESP32-S3 Edge Sensor Micro-Controller
- Dual-core Xtensa LX7 @ 240 MHz running FreeRTOS.
- **Hardware Watchdog Timer (WDT):** 1200ms hard timeout. If firmware hangs, autonomous hardware reset occurs.
- **Sampling Frequency:** Deterministic 100Hz ADC/SPI/I2C acquisition loop.
- **Cryptographic Packet Integrity:** Micro-ECC ECDSA SECP256R1 packet signing with 32-bit CRC.
- **Local Fallback Protection:** Hardcoded thermal/current threshold trip pin to open motor contactor even if RPi 5 is disconnected.

### 2.3 Tier 3: Sensor Trust & Validation Engine
- Evaluates raw readings across 5 explicit states:
  - `VERIFIED` (Score 95–100%): Cross-validated by neighboring nodes and physical physics model.
  - `TRUSTED` (Score 80–94%): Within normal operating envelope and temporal rate-of-change limits.
  - `DEGRADED` (Score 50–79%): High noise variance or elevated internal ADC temperature drift.
  - `SUSPICIOUS` (Score 20–49%): Unphysical spike or single-sensor disagreement with redundant cluster.
  - `QUARANTINED` (Score 0–19%): Confirmed sensor failure or deliberate signal spoofing; isolated from risk decision.

### 2.4 Tier 4: TinyML Advisory Anomaly Engine
- Executes quantized on-device neural models:
  - **Autoencoder:** Detects reconstruction error on multi-axis vibration spectrum (FFT).
  - **1D Convolutional Neural Network:** Detects abnormal current inrush profiles and water stage rate-of-rise surges.
  - **Isolation Forest:** Multi-variate outlier identification.
- **Crucial Safety Rule:** TinyML outputs an **advisory anomaly score (0.0–1.0)**. It is **NEVER** allowed to command safety actuators directly.

### 2.5 Tier 5: Deterministic Safety & Risk Engine
- Implements an absolute, auditable deterministic state machine:
  - `NORMAL` (Risk 0–24): Standard operational envelope.
  - `WATCH` (Risk 25–49): Elevated telemetry; rate-of-change monitoring active.
  - `WARNING` (Risk 50–74): Operator alert triggered; siren chirps; non-critical load shed.
  - `CRITICAL` (Risk 75–100): **Hardware interlock activates in <800ms**. Dual-contactor opens, 110dB siren activates, strobe pulses.
- **Decoupled from Cloud:** Decision logic resides 100% locally on the edge controller.

### 2.6 Tier 6: Local Data Persistence & Storage
- **Primary:** SQLite with Write-Ahead Logging (WAL) enabled on Raspberry Pi 5. Configured for 500,000 continuous event ring-buffer.
- **Secondary / Backup:** Automated mirroring to physical USB flash partition (`/mnt/sentinel-data/`).
- **Store-and-Forward Queue:** Tracks every critical packet across 5 states: `PENDING` $\rightarrow$ `RETRYING` $\rightarrow$ `SENT` $\rightarrow$ `ACKNOWLEDGED` $\rightarrow$ `SYNCHRONIZED`.

### 2.7 Tier 7: Communication Resilience Manager
- Hierarchical transmission failover:
  1. **Primary IP:** Wi-Fi 802.11ax / Gigabit Ethernet REST & WebSocket stream.
  2. **Secondary HF Packet Radio:** High-frequency AX.25 / packet radio simulation with CRC32, noise injection, and ACK confirmation.
  3. **Tertiary Satellite Adapter:** SatNOGS / Libre Space ground station REST interface.
  4. **Quaternary Isolated Mode:** Complete radio silence; local safety loop executes autonomously.

### 2.8 Tier 8: Mission Cockpit & 3D Operational Digital Twin
- Dark-mode technical SCADA interface built with Three.js (WebGL) running at 60 FPS.
- Interactive spatial anchors, raycasted object hover inspection, live FFT waveforms, and photo-reconstructed facility twin generation.

---

## 3. Structural Guarantees & Safety Invariants

1. **Zero Single Points of Failure:** Loss of Internet, cloud server, or remote dashboard does NOT impair local safety tripping.
2. **Deterministic Precedence:** Hard mathematical safety bounds always override AI probabilistic guesses.
3. **No Phantom Telemetry:** Loss of network connection queues packets locally; data is NEVER silently dropped.
4. **Byzantine Resilience:** A malfunctioning or spoofed sensor reporting 180°C is quarantined without triggering false plant shutdowns.
