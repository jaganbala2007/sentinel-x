# 🛡️ SENTINEL-X — OFFICIAL SIH 2026 6-SLIDE MASTER DECK
**Smart India Hackathon 2026 | AICTE & Ministry of Education Innovation Cell (MIC)**  
**Problem Statement ID:** 26223 | **Theme:** Disaster Management | **Category:** Hardware  
**Project Title:** SENTINEL-X — Quantum-Secure, Edge-Intelligent Disaster Management with a Live Physical Digital Twin  
**Team Name / ID:** [Your Team Name / ID] | **College:** [Your Institution Name]

---

## 🧭 THE CORE SYSTEM DIFFERENTIATION
> *"Most systems merely stream raw sensor telemetry to a remote cloud dashboard. **SENTINEL-X** connects the physical disaster environment, edge validation intelligence, a 3D spatial Digital Twin, resilient multi-tier communications, and the complete Before/During/After disaster lifecycle into one unified, fail-safe operational loop."*

---

# 📑 OFFICIAL 6-SLIDE PRESENTATION STRUCTURE

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 OFFICIAL SIH 6-SLIDE TEMPLATE                                   │
├──────────────┬──────────────────────────────────────────────────────────────────────────────────┤
│ **SLIDE 1**  │ **Title, Problem Statement ID & Team Details**                                   │
│ **SLIDE 2**  │ **Proposed Solution & Full Disaster Lifecycle (Before / During / After)**        │
│ **SLIDE 3**  │ **Technical Approach, Hardware Architecture & 3D Spatial Digital Twin**          │
│ **SLIDE 4**  │ **Feasibility, Viability, Resilience & Potential Challenges**                    │
│ **SLIDE 5**  │ **Impact, Benefits & Deployment Scalability**                                    │
│ **SLIDE 6**  │ **Technology Stack, Authoritative Research & References**                        │
└──────────────┴──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ SLIDE 1: PROBLEM STATEMENT & PROJECT IDENTITY

### 1. Slide Header & Metadata
* **Problem Statement ID:** 26223
* **Problem Statement Title:** Student Innovation - Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.
* **Category:** Hardware & Edge Computing
* **Theme:** Disaster Management
* **Organization:** AICTE / Ministry of Education Innovation Cell
* **Project Name:** `SENTINEL-X`
* **Subtitle:** Quantum-Secure, Edge-Intelligent Disaster Management with a Live Physical Digital Twin
* **Tagline:** `SENSE ➔ VERIFY ➔ UNDERSTAND ➔ RESPOND ➔ RECOVER`

### 2. Core Problem Addressed (The Disaster Response Gap)
* **The Fundamental Challenge:** How do we convert distributed physical signals into local, spatially aware, resilient decisions before, during, and after a disaster occurs?
* **3 Critical Vulnerabilities in Current Systems:**
  1. **Before (Blind Spots):** Risk analysis is static; sensor baseline drift and health states are unmonitored.
  2. **During (Cognitive Overload & Latency):** Cloud backhauls collapse in crises; 2D graphs fail to provide spatial situational awareness to field commanders; raw alerts cause false alarms.
  3. **After (Fragmented Recovery):** Post-event timelines are lost; damage audits take weeks; lessons are not fed back into future readiness models.

### 3. Visual Layout (Slide 1)
* **Left:** High-resolution photograph of the physical 3-sided industrial prototype enclosure with ESP32 sensor instrumentation.
* **Right:** 1:1 isometric Three.js 3D Digital Twin showing real-time spatial binding (`PHYSICAL ➔ EDGE ➔ DIGITAL`).

---

## 🖥️ SLIDE 2: PROPOSED SOLUTION & DISASTER LIFECYCLE

### 1. Solution Overview
**SENTINEL-X** is an edge-first disaster management platform that validates physical environmental signals locally, computes deterministic risk, renders a live 3D spatial Digital Twin of the physical site, executes sub-80ms emergency interlocks, and maintains operational continuity through network blackouts.

### 2. Full Disaster Lifecycle Framework
```
┌───────────────────────────────────┬───────────────────────────────────┬───────────────────────────────────┐
│          BEFORE DISASTER          │          DURING DISASTER          │          AFTER DISASTER           │
│       (Mitigate & Prepare)        │        (Respond & Contain)        │         (Recover & Audit)         │
├───────────────────────────────────┼───────────────────────────────────┼───────────────────────────────────┤
│ • 100Hz baseline drift monitoring │ • Sub-80ms local relay cutoff     │ • Cold-soak stabilization monitor │
│ • Sensor Trust & health auditing  │ • 3D Spatial hazard zone bubble   │ • Cryptographic incident audit log│
│ • Zone vulnerability partitioning │ • Dynamic A* safe egress ribbon   │ • MTTR & Damage index calculation │
│ • Pre-disaster what-if stress sim │ • Local 110dB acoustic evacuation │ • Updated baseline safety profile │
└───────────────────────────────────┴───────────────────────────────────┴───────────────────────────────────┘
```

### 3. End-to-End Operational Pipeline
$$\text{Physical Environment} \xrightarrow{\text{Sensors}} \text{ESP32 Nodes} \xrightarrow{\text{Local MQTT}} \text{Raspberry Pi} \xrightarrow{\text{Trust Engine}} \text{Risk Engine} \xrightarrow{\text{3D Digital Twin}} \text{Trip Interlock} \xrightarrow{\text{Recovery}}$$

### 4. Data Trust Model (Signature Engineering Feature)
Every data point carries an explicit, visible truth badge:
* `LIVE [IMPLEMENTED]`: Sampled from physical ESP32 hardware within 1.5s.
* `DERIVED [IMPLEMENTED]`: Mathematically calculated (e.g., Risk Index, Rate of Change $\Delta T/\Delta t$).
* `SIMULATED [IMPLEMENTED]`: Synthetic fault injection for emergency drills.
* `STALE / OFFLINE`: Node heartbeat timeout; uncertainty escalated instead of false certainty.

---

## 🖥️ SLIDE 3: TECHNICAL APPROACH, HARDWARE & DIGITAL TWIN

### 1. Physical Hardware Instrumentation
* **Field Sensor Node (`ESP32-S3 / WROOM` @ 240MHz):**
  * `DHT22 [IMPLEMENTED]`: Ambient thermal & humidity monitoring ($-40^\circ\text{C} \text{ to } +80^\circ\text{C} \pm 0.5^\circ\text{C}$).
  * `MQ-135 [IMPLEMENTED]`: Analog gas & air-quality anomaly signal ($\Delta \text{ADC} / \Delta t$).
  * `ADXL345 [IMPLEMENTED]`: 3-Axis digital accelerometer for vibration spectrum & seismic shock ($\pm 16\text{g}$).
  * `Optocoupled Power Relay [IMPLEMENTED]`: Hardware trip circuit cutting contactors in $<80\text{ms}$.
* **Edge Brain (`Raspberry Pi 4 / 5`):** Local Mosquitto MQTT broker (QoS 1), FastAPI ASGI server, and SQLite WAL database.

### 2. 3D Spatial Digital Twin Architecture (Three.js / WebGL)
* **Exact Physical Mapping:** 1:1 isometric reconstruction of the physical 3-sided enclosure, grey floor, yellow/black hazard markings, and 4-wheel mobile rover.
* **Spatial Telemetry Binding:**
  * Sensor nodes pulse green/amber/red based on live operational states.
  * Thermal/gas breach expands a 3D volumetric hazard bubble over affected zones.
  * A* vector pathfinding recalculates safe exit routes around restricted corridors in real time.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   LAYERED SYSTEM ARCHITECTURE                                   │
│  [1. PHYSICAL] DHT22 Temp │ MQ-135 Gas │ ADXL345 Vibration │ Optocoupled Relays │ 110dB Siren   │
│                                           │ (SPI / I2C / ADC @ 100Hz)                           │
│  [2. FIRMWARE] ESP32-S3 FreeRTOS Dual-Core Sampling & Local Hardware Watchdog (1.2s)            │
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

### 1. Multi-Tier Resilience (When Networks Fail)
```
  [Tier 1: Terrestrial High-Speed LAN / 4G]   (Normal Operations | Latency <30ms)
                        │ (Backhaul Cut)
                        ▼
  [Tier 2: Emergency HF Packet Radio]         (7.105 MHz AX.25 Frame Protocol | Range 500+ km)
                        │ (Severe RF Blockade)
                        ▼
  [Tier 3: LEO Satellite Burst Protocol]      (10-Byte Compact Binary SBD | SatNOGS / TinyGS)
                        │ (Total Atmospheric Blackout)
                        ▼
  [Tier 4: SQLite WAL Local Store & Forward]  (0% Data Loss | Autonomous Edge Brain & Trip)
```

### 2. Post-Quantum Cryptography (PQC) Security Layer `[PROTOTYPED]`
* **NIST FIPS 203 (ML-KEM-768):** Lattice-based key encapsulation preventing "Harvest Now, Decrypt Later" quantum attacks.
* **NIST FIPS 204 (ML-DSA-65):** Anti-tamper digital signatures on emergency command packets.

### 3. Engineering Challenges & Mitigations Matrix

| Identified Engineering Risk | Technical Root Cause | SENTINEL-X Mitigation Strategy |
| :--- | :--- | :--- |
| **Sensor Drift / Noise** | Environmental temperature/humidity fluctuations | Bayesian Kalman filter & baseline rate-of-rise tracking ($\Delta / \Delta t$) |
| **False Positive Alarms** | Single-sensor momentary spikes | Multi-sensor cross-correlation & temporal persistence ($>3$ frames) |
| **Complete Internet Outage** | Physical fiber break or cell tower damage | Edge-first autonomy + SQLite WAL store-and-forward queueing |
| **Sensor Spoofing / Tampering** | Malicious data injection on field wires | Physical plausibility consensus (degrades trust to $<20\%$) |
| **Bandwidth Limits (Satellite)** | Constrained orbital uplink throughput | Compact 10-byte binary emergency burst protocol |

---

## 🖥️ SLIDE 5: IMPACT, BENEFITS & DEPLOYMENT SCALABILITY

### 1. Multi-Dimensional Impact Analysis
* **Human & Life Safety:** Reduces incident awareness time from minutes to milliseconds; provides dynamic safe evacuation routes that prevent workers from fleeing into active hazard plumes.
* **Operational Resilience:** Eliminates cloud failure points; ensures critical equipment cutoff occurs in $<80\text{ms}$ locally.
* **Economic Advantage:** Replaces expensive ₹5,00,000+ proprietary industrial DCS/SCADA retrofits with modular ₹10,000 edge nodes (~90% capital expenditure savings).

### 2. Phased Deployment Scalability Hierarchy
```
  [LEVEL 1: Tabletop Laboratory Prototype] ──▶ Verified physical prototype with ESP32 & 3D Twin (TODAY)
                         │
                         ▼
  [LEVEL 2: Industrial Pilot Bay] ───────────▶ IP67 field enclosures, Modbus RTU & 415V contactor trip
                         │
                         ▼
  [LEVEL 3: Facility-Wide LoRa Mesh] ────────▶ Multi-gateway edge clustering covering entire plant / mine
                         │
                         ▼
  [LEVEL 4: Regional Multi-Site Network] ────▶ Centralized EOC dashboard aggregating distributed digital twins
```

---

## 🖥️ SLIDE 6: TECHNOLOGY STACK, RESEARCH & REFERENCES

### 1. Layered Technology Stack
* **Hardware:** ESP32-WROOM-32 / ESP32-S3, Raspberry Pi 4 (8GB), DHT22, MQ-135, ADXL345, Optocoupled Relays.
* **Firmware:** C++ / ESP-IDF, FreeRTOS deterministic task scheduling.
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

# ⏱️ JUDGE DEMONSTRATION & PITCH SCRIPTS

### 90-Second Live Jury Demo Script
* **[00:00 - 00:15] Baseline:** Show physical prototype and 3D Three.js twin in `NORMAL` green state (1.0 Hz telemetry, 100% trust).
* **[00:15 - 00:35] Hazard Injection:** Apply thermal/gas hazard to ESP32 Node 1. Live MQTT telemetry spikes on screen.
* **[00:35 - 00:55] Edge Interlock:** Explainable Risk Engine hits 94/100 (`CRITICAL`). Raspberry Pi trips physical relay and sounds 110dB siren in $<80\text{ms}$!
* **[00:55 - 01:15] Spatial Twin:** 3D Digital Twin renders red hazard bubble and dynamically draws green safe evacuation ribbon around blocked Corridor B.
* **[01:15 - 01:30] Resilience & Recovery:** Unplug network cable; show edge autonomy in SQLite WAL mode; reset system and export cryptographic audit JSON log.

---

### 2-Minute Master Pitch Script
> *"Respected Evaluators, in any disaster, the difference between a near-miss and a catastrophe is measured in seconds. Yet today, most disaster management platforms suffer from three fatal flaws: they depend on fragile cloud backhauls that collapse during crises; they drown incident commanders in raw 2D data; and they discard operational context the moment an incident ends.*
>
> *We built **SENTINEL-X** to solve this through a hardware-first, edge-intelligent architecture.*
>
> *SENTINEL-X starts at the physical transducer layer: ESP32 field nodes sampling thermal, gas, and vibration spectrums at 100Hz. This telemetry feeds directly into a local Raspberry Pi edge controller running an Explainable Risk Engine and Bayesian Sensor Trust validator. When a hazard is detected, SENTINEL-X does not wait for a cloud round-trip—it trips local isolation relays and sounds evacuation sirens in under 80 milliseconds.*
>
> *Simultaneously, SENTINEL-X projects this physical reality into a live 3D Spatial Digital Twin. Commanders do not see abstract charts—they see 3D volumetric hazard zones, compromised pathways, and dynamically computed safe evacuation corridors.*
>
> *To guarantee operational continuity, our system features 4-tier communication failover with SQLite Write-Ahead Logging when networks collapse, a satellite-ready burst architecture, and NIST FIPS 203/204 Post-Quantum Cryptography.*
>
> *SENTINEL-X is a functional, demonstrable hardware and software platform managing the entire disaster lifecycle before, during, and after an event. Thank you."*
