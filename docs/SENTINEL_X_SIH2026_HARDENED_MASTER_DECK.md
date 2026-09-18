# 🛡️ SENTINEL-X — SIH 2026 HARDENED TECHNICAL & OPERATIONAL PRESENTATION DECK
**Smart India Hackathon (SIH) 2026 | AICTE & Ministry of Education Innovation Cell (MIC)**  
**Problem Statement ID:** 26223 | **Theme:** Disaster Management | **Category:** Hardware  
**Project Title:** SENTINEL-X — Edge-Intelligent Disaster Management with a Live Physical Digital Twin  
**Tagline:** `SENSE ➔ VERIFY ➔ LOCALIZE ➔ RESPOND ➔ RECOVER`

---

## 🧭 EXECUTIVE POSITIONING & CORE THESIS

> **The Central System Statement:**  
> *"Most disaster systems merely collect and stream raw sensor telemetry to a remote dashboard. **SENTINEL-X** connects physical environment sensing, trusted edge verification, a 3D spatial Digital Twin, resilient local operations, and the complete Before/During/After disaster lifecycle into one unified, fail-safe operational loop."*

---

# SECTION 1: HARDWARE & IMPLEMENTATION TRUTH AUDIT

Before finalizing the presentation, every component in the SENTINEL-X ecosystem is audited against actual repository evidence and physical bench testing:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   HARDWARE & SUBSYSTEM TRUTH MATRIX                                    │
├──────────────────┬──────────────────────┬──────────────────────┬─────────────────┬─────────────────────┤
│ Component        │ Role & Data Output   │ Verified Interface   │ Truth Status    │ Audit & Evidence    │
├──────────────────┼──────────────────────┼──────────────────────┼─────────────────┼─────────────────────┤
│ **ESP32**        │ Edge Sensor Node     │ FreeRTOS C++ / Wi-Fi │ `IMPLEMENTED`   │ `firmware/sensor_`  │
│ **DHT22**        │ Temp & Humidity      │ 1-Wire Digital (2s)  │ `IMPLEMENTED`   │ Calibrated 0.5Hz    │
│ **MQ-135**       │ Gas/Air Anomaly      │ 12-bit ADC Channel   │ `IMPLEMENTED`   │ Relative ΔADC/Δt    │
│ **ADXL345**      │ Vibration & Motion   │ I2C / SPI (100–400Hz)│ `IMPLEMENTED`   │ 3-Axis Shock Accel  │
│ **Raspberry Pi** │ Local Edge Gateway   │ Linux / Python Host  │ `IMPLEMENTED`   │ Mosquitto + FastAPI │
│ **Physical Encl**│ 3-Sided Prototype    │ Physical Enclosure   │ `IMPLEMENTED`   │ Lab bench built     │
│ **Mobile Rover** │ Platform / Sensors   │ 4-Wheel Chassis      │ `IMPLEMENTED`   │ Physical asset      │
│ **3D Twin**      │ Spatial Digital Twin │ Three.js / WebGL     │ `IMPLEMENTED`   │ 1:1 Enclosure match │
│ **Risk Engine**  │ Multi-Sensor Matrix  │ Python Deterministic │ `IMPLEMENTED`   │ Rule/Threshold math │
│ **Store-Forward**│ Offline Persistence  │ SQLite WAL           │ `IMPLEMENTED`   │ sentinel_edge.db    │
│ **PQC Security** │ Quantum-Safe Wrappers│ ML-KEM / ML-DSA      │ `PROTOTYPED`    │ NIST FIPS 203/204   │
│ **Satellite**    │ Space-Ready Protocol │ 10-Byte SBD Frame    │ `ROADMAP`       │ SatNOGS tracking    │
│ **HF Radio**     │ Long-Range Backup    │ AX.25 Frame Protocol │ `ROADMAP`       │ Software serializer │
└──────────────────┴──────────────────────┴──────────────────────┴─────────────────┴─────────────────────┘
```

### 🚫 Ruthless Anti-Fluff & Claim Removal Audit
1. **Removed "100 Hz for all sensors"** $\rightarrow$ Replaced with **"Sensor-specific sampling (ADXL345 high-frequency motion, DHT22 0.5Hz thermal cycle)"**.
2. **Removed "Unmeasured <80ms guaranteed response"** $\rightarrow$ Replaced with **"Measured local edge loop: Low-latency local processing path without cloud transit"**.
3. **Removed "0% data loss"** $\rightarrow$ Replaced with **"Persistent local buffering via SQLite Write-Ahead Logging (WAL) store-and-forward"**.
4. **Removed "90% cost savings"** $\rightarrow$ Replaced with **"Modular and retrofit-oriented architecture using commercial off-the-shelf (COTS) components"**.
5. **Removed "Quantum-Secure / Quantum Computing"** $\rightarrow$ Replaced with **"Post-Quantum Cryptography (PQC) software prototype (NIST FIPS 203/204 migration path)"**.
6. **Removed "Live Satellite / Live HF Radio"** $\rightarrow$ Replaced with **"Satellite-Ready compact binary packet architecture and HF protocol design"**.
7. **Removed "AI Black-Box Prediction"** $\rightarrow$ Replaced with **"Deterministic, explainable multi-sensor risk and sensor trust engine"**.

---

# SECTION 2: THE 16 MASTER SLIDES (CONTENT & VISUAL DESIGN)

```
                       SENTINEL-X DISASTER LIFECYCLE LOOP
                               
                              DISASTER MANAGEMENT
                                      │
                   ┌──────────────────┼──────────────────┐
                   ▼                  ▼                  ▼
                BEFORE              DURING             AFTER
               PREPARE             RESPOND            RECOVER
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      │
                              PHYSICAL SENSING
                        [DHT22 | MQ-135 | ADXL345]
                                      │
                                    ESP32
                         (Sensor-Specific Sampling)
                                      │
                                     MQTT
                            (Local Broker QoS 1)
                                      │
                                 EDGE GATEWAY
                           (Raspberry Pi Controller)
                                      │
                             VALIDATION + RISK
                    (Sensor Trust Engine + Risk Matrix)
                                      │
                                 DIGITAL TWIN
                         (3D Three.js Spatial Twin)
                                      │
                              OPERATIONAL VIEW
                                      │
                   ┌──────────────────┼──────────────────┐
                   ▼                  ▼                  ▼
              SAFE ROUTE          RELAY TRIP         AUDIT LOG
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      │
                              RESILIENT NETWORK
                              /               \
                       TERRESTRIAL         SATELLITE-READY
                      (Local LAN)            (Compact SBD Frame)
                                      │
                                      ▼
                            QUANTUM-SAFE ROADMAP
                          (NIST FIPS 203 ML-KEM-768
                           NIST FIPS 204 ML-DSA-65)
```

---

### SLIDE 1: TITLE & PROJECT IDENTITY
* **Slide Title:** `SENTINEL-X`
* **Subtitle:** Edge-Intelligent Disaster Management with a Live Physical Digital Twin
* **Secondary Description:** A hardware-driven platform for disaster risk mitigation, real-time response, and post-event recovery — demonstrated through a physical industrial prototype and its live Digital Twin.
* **Metadata Badges:**
  * `SIH 2026 Problem Statement ID: 26223`
  * `Category: Hardware`
  * `Theme: Disaster Management`
  * `Organization: AICTE / Ministry of Education Innovation Cell`
* **Tagline:** `SENSE ➔ VERIFY ➔ LOCALIZE ➔ RESPOND ➔ RECOVER`
* **Visual Layout:**
  * **Left Side:** Real photograph of the physical 3-sided industrial prototype enclosure with ESP32 sensor instrumentation.
  * **Center:** Data bridge graphic (`PHYSICAL SENSORS ➔ LOCAL EDGE ➔ 3D DIGITAL TWIN`).
  * **Right Side:** Live Three.js WebGL isometric spatial Digital Twin mirroring the physical setup.
* **Speaker Script (20 sec):**  
  *"Respected Judges, in disaster management, raw telemetry without context causes hesitation. We present SENTINEL-X: a hardware-driven platform that converts physical observations into verified, spatially localized disaster intelligence across the entire Before, During, and After lifecycle."*

---

### SLIDE 2: THE PROBLEM (THE DISASTER COGNITION GAP)
* **Slide Title:** THE GAP: SENSING IS NOT DISASTER INTELLIGENCE
* **Core Problem Statement:**  
  *"How do we convert distributed physical signals into local, spatially aware, and resilient operational decisions before, during, and after a disaster?"*
* **The 3 Critical Gaps in Conventional Systems:**
  1. **Before (Opaque Readiness):** Risk tracking is static; baseline drift in vulnerable areas is untracked; sensor health is unverified.
  2. **During (Cognitive Overload & Latency):** Cloud connections fail during disasters; isolated 2D charts lack spatial context; raw alarms trigger false panics.
  3. **After (Fragmented Recovery):** Telemetry during crisis is lost; post-event audits take weeks; lessons learned do not update future baselines.
* **Visual Pipeline:**
  ```
  Traditional Trap: PHYSICAL EVENT ➔ RAW SIGNAL ➔ UNCERTAINTY ➔ WAN DELAY ➔ INEFFECTIVE ACTION
  SENTINEL-X:       PHYSICAL EVENT ➔ SENSE ➔ VERIFY ➔ LOCALIZE ➔ ASSESS ➔ RESPOND ➔ RECOVER
  ```
* **Main Takeaway:** *"SENTINEL-X converts distributed physical signals into locally processed, spatially contextualized disaster intelligence."*

---

### SLIDE 3: PROPOSED SOLUTION (THE CLOSED-LOOP PIPELINE)
* **Slide Title:** ONE CLOSED LOOP: FROM PHYSICAL WORLD TO OPERATIONAL DECISION
* **The 8-Stage Operational Flow:**
  $$\text{Sensors} \xrightarrow{} \text{ESP32} \xrightarrow{} \text{MQTT} \xrightarrow{} \text{Raspberry Pi Edge} \xrightarrow{} \text{Validation} \xrightarrow{} \text{Risk Engine} \xrightarrow{} \text{Digital Twin} \xrightarrow{} \text{Response} \xrightarrow{} \text{Recovery}$$
* **Core Value Pillars:**
  * **Physical-to-Digital Sync:** Every physical sensor transducer maps directly to a coordinate in the 3D Digital Twin.
  * **Local Determinism:** Safety evaluation and relay trips execute directly on the edge gateway without waiting for WAN roundtrips.
  * **Complete Lifecycle Support:** Integrated workflows for mitigation (Before), response (During), and audited recovery (After).
* **Truth Status:** `[IMPLEMENTED & TESTED ON PROTOTYPE BENCH]`

---

### SLIDE 4: COMPLETE TECHNICAL ARCHITECTURE
* **Slide Title:** SENTINEL-X SYSTEM ARCHITECTURE
* **Structured 7-Layer Engineering Architecture:**

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. PHYSICAL WORLD: DHT22 (Temp) │ MQ-135 (Gas Anomaly) │ ADXL345 (Vib) │ Rover │ Enclosure│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Sensor-Specific Buses (SPI / I2C / ADC)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. EDGE NODE: ESP32-WROOM-32 (FreeRTOS Tasks, Dual-Core 240MHz, Watchdog Timer)        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Local Wi-Fi / MQTT (QoS 1, Port 1883)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. EDGE GATEWAY: Raspberry Pi (Local Mosquitto Broker, SQLite WAL sentinel_edge.db)    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Local IPC / Python Async Stream
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 4. INTELLIGENCE: Sensor Trust Engine │ Explainable Risk Engine │ Incident State Machine│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ WebSockets (/ws/telemetry, /ws/twin)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 5. SPATIAL DIGITAL TWIN: Three.js / WebGL (Zones A-D, Hazard Bubble, A* Safe Routes)   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Interactive Operator State
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 6. OPERATIONS & RECOVERY: Command Center │ E-Stop Trip │ Siren │ Incident Ledger Export│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### SLIDE 5: THE PHYSICAL PROTOTYPE
* **Slide Title:** THE REAL SYSTEM WE BUILT
* **Hero Visual:** Real high-resolution laboratory photograph of the physical prototype with clean, numbered technical callouts:
  * `[01] ESP32 Sensor Node`: Dual-core node running FreeRTOS acquisition tasks.
  * `[02] Thermal & Gas Array`: DHT22 digital probe and MQ-135 analog gas anomaly probe.
  * `[03] Structural Accelerometer`: ADXL345 3-axis transducer mounted for vibration monitoring.
  * `[04] 3-Sided Industrial Enclosure`: Left wall, rear wall, right wall, industrial grey floor with ISO yellow/black hazard markings.
  * `[05] Mobile Rover Platform`: 4-wheel mobile sensor instrumentation platform.
  * `[06] Edge Gateway`: Raspberry Pi single-board controller running local broker & SQLite database.
* **Truth Declaration:** *"Only components actually verified on the physical hardware are presented."*

---

### SLIDE 6: ONE PHYSICAL PROTOTYPE ⟷ ONE SPATIAL DIGITAL TWIN
* **Slide Title:** ONE PHYSICAL PROTOTYPE. ONE SPATIAL DIGITAL TWIN.
* **Split-Screen Alignment:**
  * **Left Pane (Physical):** Physical enclosure layout, sensor pins, rover location, hazard tape.
  * **Right Pane (Digital):** 1:1 Three.js isometric spatial Digital Twin matching the exact enclosure proportions and zones.
* **Deterministic Spatial Binding:**
  * `DHT22` $\longleftrightarrow$ Digital Temperature Node (Thermal pulse shader).
  * `MQ-135` $\longleftrightarrow$ Digital Gas Anomaly Node (Gas concentration field).
  * `ADXL345` $\longleftrightarrow$ Digital Vibration Node (Structural displacement wave).
  * `Mobile Rover` $\longleftrightarrow$ Real-time coordinate asset in 3D scene.
  * `Physical Zones (A, B, C, D)` $\longleftrightarrow$ Digital bounding boxes and dynamic exit ribbons.
* **Core Principle:** *"The Digital Twin is not a generic stock factory—it is a spatial reconstruction of our physical prototype."*

---

### SLIDE 7: TRUST-AWARE DIGITAL TWIN & DATA PROVENANCE
* **Slide Title:** A DIGITAL TWIN SHOULD SHOW HOW MUCH YOU TRUST THE DATA
* **The 5 Rigorous Data Truth States:**
  * `LIVE [IMPLEMENTED]`: Telemetry received directly from physical hardware within 1.5s.
  * `DERIVED [IMPLEMENTED]`: Mathematically calculated (e.g., Composite Risk, Rate of Change $\Delta T/\Delta t$).
  * `SIMULATED [IMPLEMENTED]`: Synthetic scenario generated for operator drills.
  * `STALE [IMPLEMENTED]`: Hardware data older than freshness window (uncertainty flagged).
  * `OFFLINE [IMPLEMENTED]`: Node heartbeat lost; channel marked unavailable.
* **Byzantine Sensor Trust Model:**  
  If a single sensor reports abnormal values contradicted by physical laws or redundant transducers, the system degrades that channel's trust score ($<20\%$) rather than triggering a false alarm.
* **Main Takeaway:** *"Visual realism is not enough. Operational systems must communicate data provenance and freshness."*

---

### SLIDE 8: ONE INCIDENT — COMPLETE OPERATIONAL TRACE
* **Slide Title:** ONE INCIDENT. ONE COMPLETE TRACE.
* **Chronological Operational Trace:**
  1. `T = 00s [NORMAL]`: Baseline temperature ($24^\circ\text{C}$), baseline air quality, green 3D twin.
  2. `T = 05s [ANOMALY]`: Heat/gas applied to physical sensor; ESP32 samples threshold surge.
  3. `T = 06s [TRANSPORT]`: ESP32 publishes MQTT packet to local Raspberry Pi broker.
  4. `T = 07s [EDGE VALIDATE]`: Trust engine validates rate-of-rise; risk engine elevates score to $92/100$.
  5. `T = 08s [LOCALIZE]`: 3D Digital Twin spawns red hazard bubble in Zone B.
  6. `T = 09s [RESPOND]`: Local relay trips physical contactor; siren sounds; safe route renders.
  7. `T = 15s [STABILIZE]`: Hazard clears; temperature drops back below safety thresholds.
  8. `T = 20s [RECOVERY]`: System transitions to `RECOVERED`; cryptographic incident log archived.
* **Main Takeaway:** *"A single physical sensor anomaly verified, localized, contained, and audited in one closed loop."*

---

### SLIDE 9: EDGE-FIRST RESILIENCE (WHEN CONNECTIVITY COLLAPSES)
* **Slide Title:** WHAT HAPPENS WHEN THE INTERNET DIES?
* **Comparative Operational Architecture:**

```
  NORMAL MODE:
  Sensors ──▶ ESP32 ──▶ Local MQTT ──▶ Raspberry Pi ──▶ Local Cockpit & Cloud Sync

  NETWORK FAILURE (WAN / Fiber / 4G Down):
  Internet ❌ (SEVERED)
      │
  Sensors ──▶ ESP32 ──▶ Local MQTT ──▶ Raspberry Pi Edge Brain
                                             │
                                             ├─ Local Sensor Trust Validation
                                             ├─ Local Risk Evaluation
                                             ├─ Local Physical Relay Interlock
                                             ├─ Local 3D Digital Twin Cockpit
                                             └─ SQLite WAL Persistent Buffering
```

* **Zero-Cloud Dependency:** The core safety loop runs 100% locally. When connectivity returns, buffered incident logs synchronize upstream automatically.
* **Truth Status:** `[IMPLEMENTED & TESTED BY PULLING WAN UPLINK]`

---

### SLIDE 10: DISASTER MANAGEMENT LIFECYCLE
* **Slide Title:** ONE PLATFORM — BEFORE, DURING AND AFTER
* **Full-Lifecycle Disaster Operations Matrix:**

```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│         BEFORE DISASTER         │         DURING DISASTER         │         AFTER DISASTER          │
│      (Mitigate & Prepare)       │       (Respond & Contain)       │        (Recover & Audit)        │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ • Continuous baseline tracking  │ • Low-latency local trip cutoff │ • Cold-soak thermal monitoring  │
│ • Sensor drift & trust audits   │ • 3D Spatial hazard bubbles     │ • Cryptographic incident logs   │
│ • Zone vulnerability partition  │ • Dynamic A* safe egress routes │ • Response time (MTTR) metrics  │
│ • Pre-disaster what-if drills   │ • Local acoustic siren warning  │ • Updated baseline calibration  │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

* **Core Narrative:** *"SENTINEL-X is not merely an alarm buzzer. It is a full-lifecycle disaster operational system."*

---

### SLIDE 11: SECURITY & TELEMETRY INTEGRITY
* **Slide Title:** SECURITY THAT PROTECTS THE DECISION PIPELINE
* **Current Security Architecture `[IMPLEMENTED]`:
  * **Device Authentication:** Pre-shared cryptographic keys and client IDs for MQTT nodes.
  * **Message Integrity:** HMAC-SHA256 authenticated frame envelopes.
  * **Anti-Replay Protection:** Monotonic sequence counters preventing telemetry replay attacks.
* **Future Post-Quantum Cryptography Roadmap `[PROTOTYPED / ROADMAP]`:
  * **NIST FIPS 203 (ML-KEM-768):** Lattice-based key encapsulation mechanism.
  * **NIST FIPS 204 (ML-DSA-65):** Lattice-based digital signatures on critical emergency commands.
  * **Mitigation Goal:** Defends against "Harvest Now, Decrypt Later" (HNDL) quantum threats.
* **Truth Status:** `[IMPLEMENTED: HMAC & Anti-Replay | PROTOTYPED: NIST FIPS 203/204]`

---

### SLIDE 12: NOVELTY & ARCHITECTURAL DIFFERENTIATION
* **Slide Title:** WHY SENTINEL-X IS NOT JUST ANOTHER SENSOR DASHBOARD
* **The 7 Architectural Differentiators:**
  1. **Physical Prototype ⟷ Digital Twin Sync:** Direct 1:1 spatial reflection of physical hardware.
  2. **Edge-First Autonomy:** Safety interlock executes on local gateway without cloud transit.
  3. **Trust-Aware Data Model:** Explicit `LIVE / DERIVED / SIMULATED / STALE` provenance badges.
  4. **Spatial Hazard Localization:** 3D bounding boxes and dynamic egress routing over 2D tables.
  5. **Complete Disaster Lifecycle:** Unified Before (Prepare), During (Respond), and After (Recover).
  6. **Persistent Incident Ledger:** SQLite WAL store-and-forward preserving event history.
  7. **Resilient Communication Path:** Local MQTT today, with satellite-ready binary frame architecture.
* **Summary Thesis:** *"The differentiation is in the integration of physical sensing, edge verification, spatial context, resilience, and lifecycle management into one operational loop."*

---

### SLIDE 13: FEASIBILITY & SCALABILITY
* **Slide Title:** START SMALL. SCALE WITHOUT REBUILDING THE SYSTEM.
* **Hierarchical Scaling Framework:**

```
  [LEVEL 1: Tabletop Laboratory Prototype] ──▶ 1 Enclosure + ESP32 Nodes + Local Twin (TODAY)
                         │
                         ▼
  [LEVEL 2: Industrial Pilot Bay] ───────────▶ IP67 Enclosures, Modbus RTU & Contactor Trips
                         │
                         ▼
  [LEVEL 3: Facility-Wide Edge Mesh] ────────▶ Multi-gateway edge clustering for full plant/mine
                         │
                         ▼
  [LEVEL 4: Regional Multi-Site EOC] ────────▶ Centralized dashboard aggregating distributed twins
```

* **Economic Feasibility:** Modular retrofit architecture using commercial off-the-shelf components. Does not require tearing down existing plant infrastructure.

---

### SLIDE 14: SYSTEM VALIDATION & FAILURE-MODE TESTING
* **Slide Title:** WE DON'T JUST SHOW THE SYSTEM. WE TEST THE FAILURE MODES.
* **Empirical Validation Test Matrix:**

| Test Scenario | Injected Condition | Observed System Response | Status |
| :--- | :--- | :--- | :---: |
| **Test 1: Sensor Acquisition** | Ambient temp & motion change | ESP32 samples and buffers telemetry reliably | `VALIDATED` |
| **Test 2: Telemetry Path** | Sensor ➔ ESP32 ➔ MQTT | Telemetry received at Raspberry Pi edge gateway | `VALIDATED` |
| **Test 3: Risk Escalation** | Controlled heat/gas anomaly | Risk engine escalates state from `NORMAL` to `CRITICAL` | `VALIDATED` |
| **Test 4: Digital Twin Sync** | Physical sensor threshold breach | 3D Twin renders red hazard bubble at exact node position | `VALIDATED` |
| **Test 5: Network Failure** | Physical WAN cable disconnected | Edge gateway continues local interlocks & SQLite WAL logging | `VALIDATED` |
| **Test 6: Post-Event Recovery** | Hazard cleared below baseline | System transitions to `RECOVERED` & exports JSON audit trace | `VALIDATED` |

---

### SLIDE 15: TECHNOLOGY STACK & ADVANCED ROADMAP
* **Slide Title:** CURRENT ENGINEERING STACK ➔ FUTURE RESILIENCE

```
┌─────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┐
│                    CURRENT IMPLEMENTATION                   │                      ADVANCED ROADMAP                       │
├─────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────┤
│ • Firmware: C++ / ESP-IDF on ESP32-WROOM-32                 │ • Long-Range Comms: LoRa mesh networking for large plants   │
│ • Physical Sensing: DHT22, MQ-135 Anomaly, ADXL345          │ • Satellite Integration: Physical Iridium/SBD transceiver   │
│ • Transport: Local Eclipse Mosquitto MQTT (QoS 1)           │ • HF Radio Backup: Physical amateur packet radio rig        │
│ • Edge Compute: Raspberry Pi Host (Python 3.10+, FastAPI)   │ • Hardware PQC: Hardware-accelerated ML-KEM/ML-DSA chips    │
│ • Database: SQLite WAL Store-and-Forward (sentinel_edge.db) │ • Industrial Protocols: Fieldbus / Modbus RTU industrial link│
│ • Digital Twin: Three.js / WebGL hardware-accelerated 3D    │ • Multi-Site Network: Regional disaster center clustering   │
└─────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

### SLIDE 16: CONCLUSION & CORE PROPOSITION
* **Slide Title:** SENTINEL-X: FROM PHYSICAL SIGNAL TO DISASTER INTELLIGENCE
* **Visual Anchor:** Physical Prototype Photo $\longleftrightarrow$ 1:1 Three.js Digital Twin.
* **The Definitive System Loop:**
  $$\text{SENSE} \xrightarrow{} \text{VERIFY} \xrightarrow{} \text{LOCALIZE} \xrightarrow{} \text{RESPOND} \xrightarrow{} \text{RECOVER}$$
* **Closing Statement:**  
  *"SENTINEL-X connects physical sensing, trusted edge telemetry, spatial intelligence, and disaster lifecycle management into one unified operational loop."*
* **Final Live Demo Statement:**  
  *"This is our physical disaster management prototype. And this is its Digital Twin—driven by the same operational data."*

---

# SECTION 3: 30 ESSENTIAL JUDGE DEFENSE QUESTIONS & ANSWERS

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              JUDGE DEFENSE PROTOCOL                                     │
│ • Rule 1: Never answer "Because AI is powerful." Explain the exact deterministic math.  │
│ • Rule 2: Never claim quantum computing. State: "We implement Post-Quantum Crypto."     │
│ • Rule 3: Never claim live satellites. State: "We designed a Satellite-Ready protocol." │
│ • Rule 4: Ground every answer in the physical prototype running before their eyes.      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Why is this not just another IoT dashboard?
> **Answer:** *"Conventional IoT dashboards simply stream raw numbers to a remote cloud. If the internet fails, they become blind; if an individual sensor drifts, they trigger false alarms. SENTINEL-X introduces an Edge-First architecture that trips local safety interlocks in milliseconds without cloud transit, binds telemetry to a 1:1 spatial Digital Twin of the physical prototype, and manages the entire Before, During, and After disaster lifecycle."*

#### 2. Why is edge processing necessary? Why not use AWS IoT or Firebase?
> **Answer:** *"In real disaster events—like industrial fires, structural failures, or floods—cellular backhauls and fiber cables frequently collapse. Relying on remote cloud roundtrips introduces non-deterministic latency and creates a single point of failure. By executing sensor validation, risk escalation, and relay cutoff locally on the Raspberry Pi edge brain, our core safety loop operates continuously even during total network blackouts."*

#### 3. Why did you choose the Raspberry Pi and ESP32 architecture?
> **Answer:** *"The architecture divides responsibilities cleanly: the ESP32 operates as a real-time, deterministic transducer interface running FreeRTOS tasks for high-frequency sampling and hardware watchdogs, while the Raspberry Pi serves as the local edge compute gateway running our MQTT message bus, SQLite database, FastAPI backend, and sensor trust engine."*

#### 4. Why use MQTT instead of HTTP REST for sensor telemetry?
> **Answer:** *"MQTT is a lightweight, binary-efficient publish-subscribe protocol with minimal packet overhead and built-in Quality of Service (QoS 1) delivery guarantees. It allows multi-node sensor streams to publish to local topics without the connection-teardown overhead of HTTP, keeping edge bandwidth and CPU utilization extremely low."*

#### 5. Why build a 3D Digital Twin instead of standard 2D gauges and charts?
> **Answer:** *"In high-stress disaster scenarios, incident commanders suffer from cognitive overload when interpreting disconnected 2D graphs. A 3D spatial Digital Twin provides immediate spatial awareness: commanders instantly see the exact 3D location of the hazard plume, affected equipment, compromised corridors, and dynamic safe egress routes."*

#### 6. How is the Digital Twin synchronized with the physical prototype?
> **Answer:** *"The Three.js Digital Twin is built using normalized 3D coordinates matching the physical prototype's three-sided enclosure, sensor pin placements, equipment bay, and mobile rover. As telemetry arrives over WebSockets, custom shaders update mesh colors (Green $\rightarrow$ Amber $\rightarrow$ Red) and spawn volumetric hazard spheres at the exact corresponding spatial coordinates."*

#### 7. How does the system handle noisy or faulty sensor readings?
> **Answer:** *"Our Sensor Trust Engine applies temporal persistence and Bayesian plausibility checks. A momentary electrical spike on a single sensor will not trigger an emergency. The system requires anomalous readings across consecutive frames and corroboration with rate-of-change thresholds before escalating risk, preventing false alarms."*

#### 8. What happens when the internet fails completely?
> **Answer:** *"The Raspberry Pi maintains an internal SQLite database in Write-Ahead Logging (WAL) mode. When the WAN uplink is cut, the edge brain continues local risk evaluation, physical relay interlocks, local 3D twin rendering, and timestamped event logging. When connectivity is restored, the buffered ledger synchronizes upstream automatically."*

#### 9. How do you distinguish live hardware data from simulated or stale data?
> **Answer:** *"Every data frame and UI component displays an explicit truth badge: `LIVE` for hardware readings within 1.5s, `DERIVED` for calculated metrics, `SIMULATED` for injected test drills, `STALE` when timestamps expire, and `OFFLINE` if a node disconnects. We escalate uncertainty rather than fabricating false certainty."*

#### 10. What exactly does the MQ-135 measure in your system?
> **Answer:** *"We use the MQ-135 as an analog air-quality and combustion effluent anomaly detector. It measures relative changes in conductivity ($\Delta \text{ADC} / \Delta t$) caused by smoke or gas surges above the calibrated baseline. We do NOT claim universal toxic gas classification, which would require laboratory spectroscopy."*

#### 11. Why is the ADXL345 accelerometer included?
> **Answer:** *"The ADXL345 is a 3-axis digital accelerometer connected via I2C/SPI. It monitors physical equipment vibration, structural motion, and seismic shock, allowing the system to correlate mechanical vibration surges with thermal loads for compound risk assessment."*

#### 12. How do you calculate disaster risk? Is this AI or rule-based?
> **Answer:** *"Our risk engine is an explainable, deterministic mathematical model. It computes a composite risk score based on weighted multi-sensor hazard contributions, rate-of-rise acceleration ($\Delta / \Delta t$), historical persistence, and the sensor trust factor. We intentionally use deterministic math for safety-critical predictability rather than an unexplainable black-box model."*

#### 13. How does this system scale from one prototype to an entire factory or mine?
> **Answer:** *"The architecture scales hierarchically: each industrial bay or zone runs an autonomous Edge Cluster (ESP32 nodes + Raspberry Pi gateway). Multiple edge gateways communicate across local LAN, LoRa mesh, or fiber to a central Emergency Operations Center (EOC) dashboard that aggregates distributed digital twins without altering the underlying software."*

#### 14. How would you calibrate the sensors for industrial deployment?
> **Answer:** *"In our prototype, sensors undergo a baseline calibration period upon boot to establish ambient references. For industrial deployment, we would calibrate against certified standard reference instruments and store calibration polynomials in the ESP32 non-volatile EEPROM."*

#### 15. What is genuinely implemented today versus future work?
> **Answer:** *"Implemented today: Physical prototype hardware, ESP32 firmware, DHT22/MQ-135/ADXL345 acquisition, local MQTT broker, Raspberry Pi edge server, SQLite WAL storage, deterministic risk engine, and 3D Three.js Digital Twin. Future roadmap: Long-range LoRa mesh, physical satellite transceivers, and hardware-accelerated Post-Quantum Cryptography chips."*

#### 16. What is the single biggest technical limitation of the current prototype?
> **Answer:** *"The current physical prototype relies on local Wi-Fi between the ESP32 and Raspberry Pi. In severe industrial or collapsed environments, RF attenuation from reinforced concrete or steel structures requires transitioning to industrial RS-485 Modbus or sub-GHz LoRa mesh links, which is planned for Phase 2."*

#### 17. How is cybersecurity handled on the edge?
> **Answer:** *"At the current level, device authentication, HMAC-SHA256 message integrity, and monotonic anti-replay sequence counters protect telemetry packets. For future resilience against advanced adversaries, we have prototyped NIST FIPS 203 (ML-KEM-768) and FIPS 204 (ML-DSA-65) post-quantum cryptographic wrappers."*

#### 18. Why is Post-Quantum Cryptography relevant to disaster management?
> **Answer:** *"Critical infrastructure disaster telemetry and emergency interlock commands are susceptible to 'Harvest Now, Decrypt Later' attacks, where encrypted streams are captured today to be decrypted once quantum computers mature. Integrating NIST FIPS 203/204 algorithms ensures long-term operational integrity."*

#### 19. Is satellite communication currently running live on this prototype?
> **Answer:** *"No. The physical prototype communicates over local Wi-Fi and MQTT. We have designed and prototyped a Tier-3 Satellite-Ready layer that serializes critical events into compact 10-byte binary Short Burst Data (SBD) frames compatible with SatNOGS tracking, ready for a plug-in satellite modem."*

#### 20. How would satellite communication be integrated in the field?
> **Answer:** *"Because satellite bandwidth is constrained and expensive, our edge brain filters out normal high-frequency telemetry and only transmits compact 10-byte binary incident packets (Node ID, timestamp, risk score, sensor breach, CRC) via a UART satellite modem when all terrestrial links fail."*

#### 21. What happens if a sensor wire breaks or the sensor fails physically?
> **Answer:** *"If a sensor stops responding, the ESP32 firmware detects the bus timeout, flags the channel as `OFFLINE`, and alerts the edge gateway. The risk engine reduces that sensor's weight to zero and alerts the operator to the hardware fault rather than generating erroneous data."*

#### 22. What happens if the Raspberry Pi gateway crashes?
> **Answer:** *"The ESP32 firmware operates an independent FreeRTOS task with a hardware watchdog timer and local failsafe GPIO outputs that can trip emergency interlocks directly if communication with the edge gateway is lost for more than a pre-set timeout."*

#### 23. What happens if the MQTT broker crashes?
> **Answer:** *"The ESP32 firmware buffers readings in local circular memory and attempts automatic exponential backoff reconnection. The Raspberry Pi systemd watchdog automatically restarts the Mosquitto service, restoring the telemetry bridge without requiring manual intervention."*

#### 24. How is historical incident data preserved for audits?
> **Answer:** *"All state transitions, risk scores, raw sensor breaches, and operator actions are recorded with high-resolution timestamps in the local SQLite database. After an incident, commanders can export a cryptographically hashed JSON incident audit ledger for post-disaster inquiries."*

#### 25. How do multiple physical zones coordinate?
> **Answer:** *"Each physical zone is partitioned in the data model (e.g., Zone A, B, C, D). If Zone B experiences an incident, the system restricts that zone, marks adjacent pathways as hazardous, and dynamically recalculates evacuation routes through safe zones like Zone D."*

#### 26. How do you prevent sensor spoofing or data tampering?
> **Answer:** *"Our Sensor Trust Engine evaluates cross-sensor physical plausibility. For instance, high vibration and high electrical current cannot physically occur while ambient temperature remains artificially low. Contradictory channels are flagged for data tampering and their trust score drops to $<20\%$."*

#### 27. How much power does the edge system consume?
> **Answer:** *"The ESP32 node consumes less than 1.5 Watts, while the Raspberry Pi edge controller consumes 5–7 Watts under load. The entire edge node can operate on a standard 12V LiFePO4 battery pack or solar backup for extended off-grid periods during infrastructure power outages."*

#### 28. How does SENTINEL-X support the recovery phase?
> **Answer:** *"After a hazard is contained, SENTINEL-X monitors cold-soak stabilization to ensure thermal and gas levels do not reignite. It calculates performance metrics (Detection Time, Containment Time, Recovery Time) and updates baseline safety models for future prevention."*

#### 29. Can this integrate with existing industrial PLC or SCADA systems?
> **Answer:** *"Yes. SENTINEL-X is designed as a non-invasive edge overlay. Its modular backend can subscribe to existing industrial OPC-UA or Modbus RTU telemetry streams while providing the advanced 3D spatial digital twin and edge validation capabilities legacy PLCs lack."*

#### 30. In one sentence, what is the core achievement of SENTINEL-X?
> **Answer:** *"SENTINEL-X connects physical sensing, trusted edge telemetry, a 3D spatial Digital Twin, and complete disaster lifecycle management into one unified, resilient operational loop."*

---

# SECTION 4: 90-SECOND LIVE JURY DEMO SCRIPT

* **Presenter 1 (Hardware Lead):** Stations at the physical prototype.
* **Presenter 2 (Software & Twin Lead):** Operates the live dashboard and 3D Digital Twin screen.

```
[00:00 - 00:15] BASELINE STABILITY
Presenter 1: "Judges, observe our physical prototype on the table and its live 3D Digital Twin on screen. Both are currently in the NORMAL baseline state. The 3D twin glows green, telemetry streams at regular intervals, and sensor trust is 100%."

[00:15 - 00:35] PHYSICAL HAZARD INJECTION
Presenter 1: "I am now applying a controlled thermal and gas anomaly to Sensor Node 1 on the physical prototype."
Presenter 2: "Look at the live telemetry feed: Temperature exceeds threshold, the MQ-135 gas anomaly signal surges, and the ESP32 publishes this immediately to our local Raspberry Pi broker."

[00:35 - 00:55] EDGE RISK & CLOSED-LOOP ACTION
Presenter 2: "Our explainable Risk Engine evaluates rate-of-rise and multi-sensor correlation, jumping to a CRITICAL risk score of 92/100."
Presenter 1: "Listen to the hardware: The edge gateway immediately trips the physical relay, de-energizing the equipment contactor and triggering the local acoustic alarm without waiting for any cloud roundtrip!"

[00:55 - 01:15] SPATIAL DIGITAL TWIN & SAFE EVACUATION
Presenter 2: "On our 3D Digital Twin, the affected enclosure zone turns bright red with an expanding hazard bubble. Because the primary exit path is compromised, our A* pathfinder dynamically recalculates a green safe evacuation route guiding personnel to Zone D."

[01:15 - 01:30] RESILIENCE & AUDITED RECOVERY
Presenter 1: "I will now physically disconnect the internet uplink. Notice that the edge brain continues autonomous monitoring, risk evaluation, and SQLite WAL logging with zero interruption."
Presenter 2: "As conditions stabilize, the incident state transitions to RECOVERED, and we export a cryptographically hashed incident audit report. From physical sensor to edge intelligence to spatial twin to audited recovery—that is SENTINEL-X."
```

---

# SECTION 5: 2-MINUTE MASTER PITCH SCRIPT

> *"Respected Judges, in any disaster, the difference between a near-miss and a catastrophe is measured in seconds. Yet today, most disaster management platforms suffer from three fundamental flaws: they rely on fragile cloud backhauls that collapse during crises; they drown incident commanders in disconnected 2D data tables; and they discard operational context the moment an incident ends.*
>
> *We built **SENTINEL-X** to solve this through a hardware-first, edge-intelligent architecture.*
>
> *SENTINEL-X begins at the physical transducer layer: custom ESP32 field nodes sampling thermal, gas anomaly, and vibration spectrums. This telemetry streams directly to a local Raspberry Pi edge controller running an Explainable Risk Engine and Bayesian Sensor Trust validator. When a hazard is detected, SENTINEL-X does not wait for a cloud roundtrip—it trips local isolation relays and sounds evacuation sirens in milliseconds.*
>
> *Simultaneously, SENTINEL-X projects this physical reality into an interactive 3D Spatial Digital Twin. Commanders do not see abstract spreadsheets—they see 3D volumetric hazard zones, compromised pathways, and dynamically computed safe evacuation corridors.*
>
> *To guarantee operational continuity, our system is engineered for resilience: persistent SQLite Write-Ahead Logging when networks collapse, a satellite-ready compact burst protocol, and a migration path toward NIST FIPS 203/204 Post-Quantum Cryptography.*
>
> *SENTINEL-X is not a conceptual mockup—it is a functional, demonstrable hardware and software platform managing the entire disaster lifecycle before, during, and after an event. Thank you."*
