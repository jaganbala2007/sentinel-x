# 🛡️ SENTINEL-X — OFFICIAL SIH 2026 EXACT 6-SLIDE MASTER DECK
**Smart India Hackathon (SIH) 2026 | Ministry of Education Innovation Cell (MIC) & AICTE**  
**Problem Statement ID:** 26223 | **Theme:** Disaster Management | **Category:** Hardware  
**Strict SIH Submission Format:** Exactly 6 Slides  

---

## 🧭 CORE VALUE PROPOSITION
> *"Most disaster management systems merely collect and stream raw sensor telemetry to a remote dashboard. **SENTINEL-X** connects physical environment sensing, trusted edge verification, a 3D spatial Digital Twin, resilient local operations, and the complete Before/During/After disaster lifecycle into one unified, fail-safe operational loop."*

---

# 📑 THE EXACT 6-SLIDE SUBMISSION

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                OFFICIAL SIH 6-SLIDE MASTER DECK                                 │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────┤
│ **SLIDE 1**  │ **Title, Problem Statement & Team Identity**                                     │
│ **SLIDE 2**  │ **Proposed Solution & Disaster Lifecycle (Before / During / After)**             │
│ **SLIDE 3**  │ **Technical Approach, Hardware Architecture & 3D Spatial Digital Twin**          │
│ **SLIDE 4**  │ **Feasibility, Viability, Edge Resilience & Engineering Challenges**             │
│ **SLIDE 5**  │ **Impact, Operational Benefits & Deployment Scalability**                        │
│ **SLIDE 6**  │ **Technology Stack, Authoritative Research & References**                        │
└──────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ SLIDE 1: PROBLEM STATEMENT & PROJECT IDENTITY

### 1. Slide Metadata & Header
* **Problem Statement ID:** 26223
* **Problem Statement Title:** Student Innovation - Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.
* **Category:** Hardware
* **Theme:** Disaster Management
* **Organization:** AICTE / Ministry of Education Innovation Cell
* **Project Name:** `SENTINEL-X`
* **Subtitle:** Edge-Intelligent Disaster Management with a Live Physical Digital Twin
* **Tagline:** `SENSE ➔ VERIFY ➔ LOCALIZE ➔ RESPOND ➔ RECOVER`

### 2. The Disaster Response Gap (Problem Addressed)
* **The Core Problem:** How do we convert distributed physical signals into local, spatially aware, and resilient operational decisions before, during, and after a disaster occurs?
* **3 Major Vulnerabilities in Existing Solutions:**
  * **Before (Opaque Readiness):** Risk tracking is static; baseline drift in vulnerable industrial/urban zones is unmonitored; sensor health is unverified.
  * **During (Cognitive Overload & Latency):** Cloud connections collapse during crises; isolated 2D charts fail to give spatial context; raw alarms cause false evacuations.
  * **After (Fragmented Recovery):** Telemetry during crises is lost; damage audits take weeks; lessons learned do not update future readiness models.

### 3. Visual Layout & Hero Elements
* **Left Half:** Real photograph of the physical 3-sided industrial prototype enclosure with labeled ESP32 sensor instrumentation.
* **Center Bridge:** Data flow arrow (`PHYSICAL SENSORS ➔ LOCAL EDGE GATEWAY ➔ 3D SPATIAL TWIN`).
* **Right Half:** 1:1 matching Three.js WebGL isometric spatial Digital Twin.
* **Speaker Script (20 sec):**  
  *"Respected Judges, in disaster management, raw telemetry without spatial context causes fatal hesitation. We present SENTINEL-X: a hardware-driven, edge-first platform that converts physical observations into verified, spatially localized disaster intelligence across the entire Before, During, and After lifecycle."*

---

## 🖥️ SLIDE 2: PROPOSED SOLUTION & DISASTER LIFECYCLE

### 1. The Closed-Loop Operational Solution
**SENTINEL-X** is an edge-first disaster management platform that validates physical environmental signals locally, computes deterministic risk, renders a live 3D spatial Digital Twin of the physical site, executes rapid local emergency interlocks, and maintains operational continuity through network blackouts.

### 2. The Closed-Loop Operational Flow
$$\text{Physical Environment} \xrightarrow{\text{Sensors}} \text{ESP32 Nodes} \xrightarrow{\text{Local MQTT}} \text{Raspberry Pi} \xrightarrow{\text{Trust Engine}} \text{Risk Engine} \xrightarrow{\text{3D Digital Twin}} \text{Local Interlock} \xrightarrow{\text{Audited Recovery}}$$

### 3. Complete 3-Phase Disaster Lifecycle Matrix

```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│         BEFORE DISASTER         │         DURING DISASTER         │         AFTER DISASTER          │
│      (Mitigate & Prepare)       │       (Respond & Contain)       │        (Recover & Audit)        │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ • Continuous baseline tracking  │ • Low-latency local relay cutoff│ • Cold-soak thermal monitoring  │
│ • Sensor Trust & health audits  │ • 3D Spatial hazard zone bubble │ • Cryptographic incident logs   │
│ • Zone vulnerability partition  │ • Dynamic A* safe egress routes │ • Response time (MTTR) metrics  │
│ • Pre-disaster what-if drills   │ • Local acoustic siren warning  │ • Updated baseline safety model │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

### 4. Data Trust & Truth Badges
Every data point displayed in the interface and telemetry stream carries a visible provenance badge:
* `LIVE [IMPLEMENTED]`: Telemetry received directly from physical hardware within 1.5 seconds.
* `DERIVED [IMPLEMENTED]`: Mathematically calculated (e.g., Risk Score, Rate of Change $\Delta T/\Delta t$).
* `SIMULATED [IMPLEMENTED]`: Synthetic scenario generated for emergency training drills.
* `STALE / OFFLINE`: Node timeout detected; uncertainty is escalated rather than fabricating false certainty.

---

## 🖥️ SLIDE 3: TECHNICAL APPROACH, HARDWARE & DIGITAL TWIN

### 1. Physical Hardware Instrumentation `[IMPLEMENTED]`
* **Field Sensor Node (`ESP32-WROOM-32 / ESP32-S3` @ 240MHz):**
  * `DHT22 [IMPLEMENTED]`: Ambient thermal & humidity monitoring ($-40^\circ\text{C} \text{ to } +80^\circ\text{C} \pm 0.5^\circ\text{C}$).
  * `MQ-135 [IMPLEMENTED]`: Analog air-quality and combustion effluent anomaly signal ($\Delta \text{ADC} / \Delta t$).
  * `ADXL345 [IMPLEMENTED]`: 3-Axis digital accelerometer for vibration spectrum & seismic shock ($\pm 16\text{g}$).
  * `Optocoupled Power Relay [IMPLEMENTED]`: Hardware trip circuit cutting contactors in milliseconds.
* **Edge Gateway (`Raspberry Pi 4 / 5`):** Local Eclipse Mosquitto MQTT broker (QoS 1), FastAPI ASGI server, and SQLite WAL database.
* **Physical Demonstration Enclosure:** 3-sided industrial enclosure (left, right, rear walls, grey floor with ISO yellow/black hazard markings, 4-wheel mobile rover platform).

### 2. 3D Spatial Digital Twin (Three.js / WebGL) `[IMPLEMENTED]`
* **1:1 Spatial Mapping:** Direct isometric reconstruction matching the exact physical prototype proportions and zones (no generic stock factory).
* **Real-Time Spatial Binding:**
  * Physical sensor pins pulse green/amber/red based on live operational states.
  * Thermal/gas threshold breaches trigger dynamic 3D volumetric hazard bounding spheres.
  * A* vector pathfinder recalculates safe exit routes around restricted corridors in real time.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   LAYERED SYSTEM ARCHITECTURE                                   │
│  [1. PHYSICAL] DHT22 Temp │ MQ-135 Gas Anomaly │ ADXL345 Vibration │ Relays │ 110dB Siren        │
│                                           │ (Sensor-Specific Buses: SPI / I2C / ADC)            │
│  [2. FIRMWARE] ESP32 FreeRTOS Task Scheduling & Hardware Watchdog (1.2s)                         │
│                                           │ (Local Wi-Fi / MQTT Port 1883)                      │
│  [3. EDGE CORE] Raspberry Pi: Mosquitto Broker │ SQLite WAL Engine (sentinel_edge.db)           │
│                                           │ (WebSockets /ws/telemetry & /ws/twin)               │
│  [4. DECISION] Explainable Risk Engine │ Bayesian Sensor Trust Validator │ Incident State Machine│
│                                           │ (WebGL 60 FPS Hardware Acceleration)                │
│  [5. SPATIAL UI] Three.js Digital Twin │ Zone A-D Partitioning │ Dynamic A* Evacuation Routing  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ SLIDE 4: FEASIBILITY, VIABILITY, RESILIENCE & CHALLENGES

### 1. Edge-First Resilience (When Connectivity Fails)
```
  [Tier 1: Terrestrial High-Speed LAN / 4G]   (Normal Operations | Low Latency)
                        │ (Physical Backhaul Severed)
                        ▼
  [Tier 2: Emergency HF Packet Radio]         (7.105 MHz AX.25 Frame Protocol | Range 500+ km) [ROADMAP]
                        │ (Severe RF Blockade)
                        ▼
  [Tier 3: LEO Satellite Burst Protocol]      (10-Byte Compact Binary SBD | SatNOGS) [ROADMAP]
                        │ (Total Atmospheric Blackout)
                        ▼
  [Tier 4: SQLite WAL Local Store & Forward]  (Autonomous Local Edge Brain & Interlock) [IMPLEMENTED]
```
* **Local Operational Continuity:** The edge brain evaluates risk, renders the local 3D twin, trips relays, and buffers all events in SQLite Write-Ahead Logging (`sentinel_edge.db`) with automatic upstream sync upon reconnection.

### 2. Quantum-Safe Cryptography Roadmap `[PROTOTYPED]`
* **NIST FIPS 203 (ML-KEM-768):** Lattice-based key encapsulation defending against "Harvest Now, Decrypt Later" quantum attacks.
* **NIST FIPS 204 (ML-DSA-65):** Anti-tamper digital signatures on emergency command packets.

### 3. Engineering Challenges & Mitigations Matrix

| Identified Engineering Risk | Technical Root Cause | SENTINEL-X Mitigation Strategy |
| :--- | :--- | :--- |
| **Sensor Drift / Noise** | Thermal and humidity fluctuations | Bayesian Kalman filter & baseline rate-of-rise tracking ($\Delta / \Delta t$) |
| **False Positive Alarms** | Single-sensor momentary spikes | Multi-sensor cross-correlation & temporal persistence ($>3$ frames) |
| **Complete Internet Outage** | Physical fiber break / tower damage | Edge-first autonomy + SQLite WAL store-and-forward queueing |
| **Sensor Spoofing / Tampering** | Malicious data injection on field lines| Cross-sensor physical plausibility consensus (drops trust to $<20\%$) |
| **Constrained Satellite Link** | Limited satellite uplink bandwidth | Compact 10-byte binary emergency burst protocol |

---

## 🖥️ SLIDE 5: IMPACT, BENEFITS & DEPLOYMENT SCALABILITY

### 1. Multi-Dimensional Impact Analysis
* **Life Safety & Human Impact:** Reduces disaster awareness time from minutes to milliseconds; provides dynamic safe evacuation routes that prevent workers from fleeing into active hazard plumes.
* **Operational Resilience:** Eliminates single-point cloud failures; guarantees local safety interlocks and alarms operate off-grid.
* **Economic Viability:** Modular retrofit architecture using commercial off-the-shelf (COTS) components; avoids costly total teardowns of existing industrial infrastructure.

### 2. Hierarchical Deployment Scalability Framework
```
  [LEVEL 1: Tabletop Laboratory Prototype] ──▶ 1 Enclosure + ESP32 Nodes + Local 3D Twin (TODAY)
                         │
                         ▼
  [LEVEL 2: Industrial Pilot Bay] ───────────▶ IP67 Field Enclosures, Modbus RTU & 415V Contactor Trips
                         │
                         ▼
  [LEVEL 3: Facility-Wide Edge Mesh] ────────▶ Multi-gateway edge clustering for full plant/mine coverage
                         │
                         ▼
  [LEVEL 4: Regional Multi-Site Network] ────▶ Centralized EOC dashboard aggregating distributed digital twins
```

---

## 🖥️ SLIDE 6: TECHNOLOGY STACK, RESEARCH & REFERENCES

### 1. Layered Technology Stack
* **Hardware:** ESP32-WROOM-32 / ESP32-S3, Raspberry Pi 4/5, DHT22, MQ-135, ADXL345, Optocoupled Relays, 110dB Siren.
* **Firmware:** C++ / ESP-IDF with FreeRTOS deterministic task scheduling.
* **Edge Backend:** Python 3.10+, FastAPI (ASGI), SQLite (Write-Ahead Logging mode), Eclipse Mosquitto MQTT.
* **Digital Twin & Frontend:** Three.js (WebGL 3D Engine), HTML5, Tailwind CSS, Vanilla JavaScript (ES6+), WebSockets.
* **Security & Space Protocols:** NIST FIPS 203/204 PQC (ML-KEM/ML-DSA), SatNOGS / TinyGS SBD serializer, AX.25.

### 2. Authoritative Research References
1. **NIST Special Publication 800-208 / FIPS 203 & 204 (2024):** *Standards for Post-Quantum Key Encapsulation and Digital Signatures.*
2. **ISO 10816-3:** *Mechanical vibration — Evaluation of machine vibration by measurements on non-rotating parts.*
3. **IEC 61508 / ISO 13849:** *Functional Safety of Electrical / Electronic / Programmable Electronic Safety-Related Systems.*
4. **OASIS Standard:** *MQTT Version 5.0 Core Specification (2019).*
5. **Libre Space Foundation:** *SatNOGS Open-Source Global Satellite Ground Station Network Architecture (2024).*

---

# ⏱️ JURY DEMO & PITCH SCRIPTS (FOR LIVE EVALUATION)

### 90-Second Live Jury Demo Script
* **[00:00 - 00:15] Baseline:** Show physical prototype and 3D Three.js twin in `NORMAL` green baseline (1.0 Hz telemetry, 100% trust).
* **[00:15 - 00:35] Physical Hazard:** Apply thermal/gas anomaly to ESP32 Node 1. Live MQTT telemetry spikes on screen.
* **[00:35 - 00:55] Edge Interlock:** Risk Engine evaluates rate-of-rise, hitting 92/100 (`CRITICAL`). Raspberry Pi trips physical relay and sounds 110dB siren locally!
* **[00:55 - 01:15] Spatial Twin:** 3D Digital Twin renders red hazard bubble and dynamically draws green safe evacuation ribbon around blocked Corridor B.
* **[01:15 - 01:30] Resilience & Recovery:** Unplug network cable; show edge autonomy in SQLite WAL mode; reset system and export cryptographic audit JSON log.

---

### 2-Minute Master Pitch Script
> *"Respected Judges, in any disaster, the difference between a near-miss and a catastrophe is measured in seconds. Yet today, most disaster management platforms suffer from three fatal flaws: they depend on fragile cloud backhauls that collapse during crises; they drown incident commanders in raw 2D data tables; and they discard operational context the moment an incident ends.*
>
> *We built **SENTINEL-X** to solve this through a hardware-first, edge-intelligent architecture.*
>
> *SENTINEL-X begins at the physical transducer layer: custom ESP32 field nodes sampling thermal, gas anomaly, and vibration spectrums. This telemetry streams directly to a local Raspberry Pi edge controller running an Explainable Risk Engine and Bayesian Sensor Trust validator. When a hazard is detected, SENTINEL-X does not wait for a cloud roundtrip—it trips local isolation relays and sounds evacuation sirens in milliseconds.*
>
> *Simultaneously, SENTINEL-X projects this physical reality into an interactive 3D Spatial Digital Twin. Commanders do not see abstract spreadsheets—they see 3D volumetric hazard zones, compromised pathways, and dynamically computed safe evacuation corridors.*
>
> *To guarantee operational continuity, our system features multi-tier resilience with persistent SQLite Write-Ahead Logging when networks collapse, a satellite-ready compact burst protocol, and a migration path toward NIST FIPS 203/204 Post-Quantum Cryptography.*
>
> *SENTINEL-X is not a conceptual mockup—it is a functional, demonstrable hardware and software platform managing the entire disaster lifecycle before, during, and after an event. Thank you."*
