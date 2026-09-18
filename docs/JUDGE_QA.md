# ❓ Sentinel-X SIH 2026 Judge Q&A & Technical Defense

**Document Version:** 2.4.0  
**Target:** Defending Sentinel-X against rigorous questioning from industrial safety, embedded, AI, and disaster management judges.

---

### Q1: "What happens if the Internet or cloud completely fails?"
**Answer:**  
"Nothing stops in our safety loop. The cloud is strictly a non-critical monitoring observer. The Raspberry Pi 5 edge brain and ESP32-S3 sensor node run all safety algorithms locally. If internet connectivity drops, Sentinel-X switches into **Isolated Autonomous Mode**. All sensor trust calculations, deterministic risk decisions, and 415V relay trips continue in real-time (<800ms). Telemetry and incident logs are written to the local SQLite WAL ring-buffer and USB flash drive, and transmitted across secondary HF radio links. When internet returns, our store-and-forward queue synchronizes all backlogged records automatically."

---

### Q2: "What happens if one sensor malfunctions, drifts, or is maliciously spoofed?"
**Answer:**  
"Sentinel-X never blindly trusts a single sensor. Every data point passes through our **Sensor Trust Engine**. If a temperature sensor suddenly spikes from 68°C to 180°C in a single 10ms frame, the engine detects a physical rate-of-change violation ($>50^\circ\text{C/s}$), flags cross-sensor disagreement (vibration and current are nominal), and calculates a neighbor Z-score. The trust score drops to 12.5% (`QUARANTINED`). The Deterministic Safety Engine isolates the faulty reading and bases safety decisions on remaining verified sensors, **preventing catastrophic false-positive plant shutdowns**."

---

### Q3: "Why not use a Large Language Model (LLM) or deep neural network to make the safety decisions?"
**Answer:**  
"Because LLMs are non-deterministic, have variable latency (hundreds of milliseconds to seconds), can hallucinate, and fail SIL-2 auditability requirements. In Sentinel-X, **AI and TinyML are strictly advisory** for early anomaly scoring. The final life-safety actuation is governed 100% by a **Deterministic Risk Engine** running hard, auditable mathematical thresholds inspired by ISO 13849."

---

### Q4: "Is this actually running on real hardware or is it just a web simulation?"
**Answer:**  
"It is running on real physical hardware. We have an ESP32-S3 node acquiring real PT100 thermal, ADXL345 vibration, ACS712 current, and VL53L1X Time-of-Flight readings, communicating over high-speed UART/USB to a local Raspberry Pi 5 edge brain. The RPi 5 drives real optocoupled relays wired to an industrial contactor and siren. In our dashboard, we explicitly label every subsystem as `LIVE`, `HARDWARE-TESTED`, `SIMULATED`, or `ADAPTER READY` to maintain absolute engineering transparency."

---

### Q5: "How does the Photo-Assisted Digital Twin work?"
**Answer:**  
"Instead of requiring months of manual CAD modeling, operators upload multi-view field photographs. Our photogrammetry pipeline runs canvas-based color histogram sampling, keypoint matching, and DeepLabV3+ semantic classification to identify the facility archetype (conveyor, warehouse, dam, or room). It generates a watertight 3D digital twin in Three.js and anchors live 100Hz SCADA telemetry pins to the reconstructed physical objects."
