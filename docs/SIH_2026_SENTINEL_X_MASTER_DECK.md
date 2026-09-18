# 🛡️ SENTINEL-X — SIH 2026 ADVANCED TECHNICAL & OPERATIONAL DECK
**Smart India Hackathon (SIH) 2026 | Ministry of Education & AICTE**  
**Problem Statement ID:** 26223 | **Category:** Hardware | **Theme:** Disaster Management  
**Project:** SENTINEL-X (Quantum-Secure, Edge-Intelligent Disaster Management with a Live Physical Digital Twin)  
**Core Motto:** `SENSE ➔ VERIFY ➔ UNDERSTAND ➔ RESPOND ➔ RECOVER`

---

## 🧭 EXECUTIVE SUMMARY & CORE THESIS

> **Central System Statement:**  
> *"Most systems merely collect and stream raw sensor telemetry to a remote dashboard. **SENTINEL-X** connects the physical disaster environment, edge validation intelligence, a 3D spatial Digital Twin, resilient multi-tier communications, and the complete Before/During/After disaster lifecycle into a unified, fail-safe operational loop."*

---

# SECTION 1: MASTER SLIDE-BY-SLIDE PRESENTATION CONTENT (16 SLIDES)

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
                   [DHT22 | MQ-135 | ADXL345 | PT100 | VL53L1X]
                                      │
                                    ESP32
                         (Deterministic Sampling @ 100Hz)
                                      │
                                     MQTT
                            (Local Broker QoS 1)
                                      │
                                 EDGE GATEWAY
                           (Raspberry Pi 4 / 5 SBC)
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
              SAFE ROUTE          E-STOP TRIP        AUDIT LOG
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      │
                              RESILIENT NETWORK
                              /               \
                       TERRESTRIAL         SATELLITE-READY
                      (4G / HF AX.25)        (SatNOGS / TinyGS)
                                      │
                                      ▼
                           QUANTUM-SAFE SECURITY
                          (NIST FIPS 203 ML-KEM-768
                           NIST FIPS 204 ML-DSA-65)
```

---

### SLIDE 1 — TITLE & PROJECT IDENTITY
* **Slide Title:** `SENTINEL-X`
* **Subtitle:** Quantum-Secure, Edge-Intelligent Disaster Management with a Live Physical Digital Twin
* **Secondary Description:** A hardware-driven platform for disaster risk mitigation, real-time response, and post-event recovery — demonstrated through an industrial physical prototype.
* **Metadata Badges:**
  * `SIH 2026 Problem Statement ID: 26223`
  * `Theme: Disaster Management`
  * `Category: Hardware & Edge Computing`
  * `Organization: AICTE / Ministry of Education Innovation Cell`
* **Visual Layout:**
  * **Left Pane (Physical Reality):** Photograph of the physical industrial prototype enclosure, mobile rover platform, and ESP32 sensor instrumentation.
  * **Center Pane (Data Flow):** Low-latency data bridge icon (`PHYSICAL ➔ EDGE ➔ DIGITAL`).
  * **Right Pane (Digital Reality):** Real-time 3D Three.js Digital Twin mirroring the exact physical layout.
* **Speaker Script (30 sec):**  
  *"Respected Judges, in high-stakes disaster scenarios, isolated sensor data leads to operational ambiguity. We present SENTINEL-X: a hardware-backed disaster management platform that converts physical observations into local, verified, spatially aware operational decisions across the entire Before, During, and After disaster lifecycle."*

---

### SLIDE 2 — THE DISASTER RESPONSE GAP (PROBLEM STATEMENT)
* **Slide Title:** THE CRITICAL DISASTER RESPONSE GAP
* **Core Problem Statement:**  
  *"How do we convert distributed physical signals into local, spatially aware, and resilient operational decisions before, during, and after a disaster occurs?"*
* **The 3-Phase Operational Breakdown:**
  1. **BEFORE (Fragmented Preparedness):** Risk indices are static spreadsheets; sensor readiness is opaque; blind spots exist in vulnerable industrial/urban zones.
  2. **DURING (The Cognitive Overload Dilemma):** Sensors produce noisy, unverified data; terrestrial backhauls collapse; isolated 2D charts fail to give incident commanders spatial context.
  3. **AFTER (Disjointed Recovery):** Post-event reconstruction relies on lost or fragmented telemetry; damage audits take weeks; lessons are never fed back into the next readiness cycle.
* **Visual Representation:**
  ```
  Traditional Trap: SENSE ➔ RAW TELEMETRY ➔ UNCERTAINTY ➔ WAN LATENCY ➔ DELAYED RESPONSE
  SENTINEL-X Loop:  SENSE ➔ LOCAL VERIFY ➔ SPATIAL TWIN ➔ AUTONOMOUS TRIP ➔ AUDITED RECOVERY
  ```
* **Truth State Declaration:** `[FIELD OBSERVATION & DISASTER LITERATURE REVIEWED]`

---

### SLIDE 3 — PROPOSED SOLUTION: THE EDGE-FIRST OPERATIONAL LOOP
* **Slide Title:** SENTINEL-X: FROM TRANSDUCER TO ACTIONABLE COCKPIT
* **Solution Architecture:** An integrated 8-stage pipeline operating entirely on local infrastructure without mandatory cloud dependency:
  $$\text{Physical Environment} \xrightarrow{\text{Sensors}} \text{ESP32 Nodes} \xrightarrow{\text{MQTT}} \text{Edge SBC Gateway} \xrightarrow{\text{Trust Validation}} \text{Risk Engine} \xrightarrow{\text{3D Spatial Twin}} \text{Command / Interlock} \xrightarrow{\text{Recovery}}$$
* **Core Value Pillars:**
  * **Local Determinism:** Sub-800ms trip latency from threshold breach to physical actuator cutoff.
  * **Spatial Situational Awareness:** Replacing 2D graphs with real-time 3D bounding boxes and dynamic egress vectors.
  * **Full Lifecycle Support:** Integrated Before (Predict/Mitigate), During (Respond/Contain), and After (Recover/Audit) workflows.
* **Truth State Declaration:** `[IMPLEMENTED & TESTED IN REPOSITORY]`

---

### SLIDE 4 — NOVELTY & DIFFERENTIATION MATRIX
* **Slide Title:** BEYOND CONVENTIONAL IOT: ENGINEERING DIFFERENTIATION
* **Comparative Evaluation:**

| Feature Dimension | Conventional IoT Platforms | Legacy SCADA / PLC Systems | SENTINEL-X Solution |
| :--- | :--- | :--- | :--- |
| **Computing Model** | Cloud-Centric (High WAN dependency) | Local Closed-Loop (No spatial UI) | **Edge-First + Distributed Broker [IMPLEMENTED]** |
| **Data Trust & Truth** | Accepts raw sensor readings unconditionally | Simple wire-break detection | **Byzantine Consensus & Anti-Spoofing [IMPLEMENTED]** |
| **Spatial Cognition** | 2D Gauge Dashboards | Static 2D P&ID Schematics | **3D Three.js Physical Digital Twin [IMPLEMENTED]** |
| **Incident Lifecycle** | Passive Alerting (SMS/Email) | Hardware E-Stop only | **8-State Machine (Watch ➔ Recovery) [IMPLEMENTED]** |
| **Network Resilience** | Fails completely on link drop | Hardwired Fieldbus only | **4-Tier Failover: LAN ➔ HF ➔ Sat ➔ WAL [PROTOTYPED]** |
| **Security Posture** | Legacy TLS 1.2 / RSA | Perimeter Isolation | **NIST FIPS 203/204 Post-Quantum Ready [PROTOTYPED]** |

---

### SLIDE 5 — PHYSICAL PROTOTYPE & INSTRUMENTATION
* **Slide Title:** FROM CONCEPT TO PHYSICAL SYSTEM: BENCHMARK PROTOTYPE
* **Physical Demonstration Enclosure Anatomy:**
  * **Three-Sided Industrial Enclosure:** Left wall, rear wall, right wall, open observation front with industrial texture rendering.
  * **Zoned Floor Matrix:** Industrial grey floor plate with ISO 3864 yellow/black hazard perimeter markings ($350\text{mm} \times 280\text{mm}$).
  * **Mobile Rover / Equipment Platform:** 4-wheel mobile sensor platform carrying dynamic environmental probes.
* **Component Specification & Instrumentation Callouts:**
  * `DHT22 [IMPLEMENTED]`: Calibrated ambient temperature ($-40^\circ\text{C} \text{ to } +80^\circ\text{C} \pm 0.5^\circ\text{C}$) and relative humidity.
  * `MQ-135 [IMPLEMENTED]`: Analog/Digital Gas & Air-Quality Anomaly Signal (CO, Ethanol, Smoke particulate baseline surge).
  * `ADXL345 [IMPLEMENTED]`: 3-Axis digital accelerometer via SPI/I2C for vibration spectrum & seismic shock monitoring ($\pm 16\text{g}$).
  * `ESP32-WROOM-32 / ESP32-S3 [IMPLEMENTED]`: Dual-core Xtensa LX7 @ 240MHz executing deterministic 100Hz FreeRTOS sampling loops.
  * `Raspberry Pi 4 / 5 [IMPLEMENTED]`: Quad-core Cortex-A72/A76 host running Mosquitto MQTT, FastAPI, SQLite WAL, and WebSockets.
  * `Optocoupled Power Relay [IMPLEMENTED]`: Hardware interlock cutting power to equipment contactors within 80ms.

---

### SLIDE 6 — COMPLETE TECHNICAL ARCHITECTURE
* **Slide Title:** END-TO-END LAYERED SYSTEM ARCHITECTURE
* **Layer Breakdown:**
  1. **Physical & Transducer Layer:** Multi-sensor array with analog signal conditioning, SPI/I2C buses, and physical trip relays.
  2. **Device Firmware Layer:** FreeRTOS dual-task architecture on ESP32 (Core 0: Sensor acquisition; Core 1: MQTT packetization).
  3. **Communication Backbone Layer:** Mosquitto MQTT message broker on `sentinel/telemetry/#` and `sentinel/commands/#` (QoS 1).
  4. **Edge Intelligence & Storage Layer:** Local Python 3.10+ FastAPI ASGI server, SQLite Write-Ahead Logging (`sentinel_edge.db`), and deterministic rule engines.
  5. **3D Digital Twin & Application Layer:** Three.js / WebGL hardware-accelerated 60 FPS spatial visualizer with real-time shader bindings.
  6. **Security & Resilience Layer:** Local monotonic anti-replay counters, HMAC-SHA256 frame hashing, and NIST FIPS 203/204 PQC migration wrappers.

---

### SLIDE 7 — THE 3D SPATIAL DIGITAL TWIN
* **Slide Title:** THE PHYSICAL PROTOTYPE HAS A LIVE DIGITAL TWIN
* **Hero Visualization:**
  * **Left:** Actual photograph of the physical 3-sided industrial prototype.
  * **Right:** 1:1 isometric WebGL digital twin matching exact relative proportions, floor markings, and equipment positions.
* **Spatial Synchronization Capabilities:**
  * **Physical Sensor ⟷ Digital Pin:** Telemetry updates trigger dynamic color shifts (Green $\rightarrow$ Amber $\rightarrow$ Red) and volumetric pulse spheres.
  * **Physical Hazard Zone ⟷ Digital Bounding Box:** Temperature/gas breach expands a 3D translucent danger bubble.
  * **Dynamic Egress Routing:** A* vector pathfinding recalculates safe exit routes around restricted hazard zones in real time.
  * **Camera View Modes:** Operator Cockpit, Isometric Overview, Drone Fly-Through, and First-Person Egress Path.

---

### SLIDE 8 — DIGITAL TWIN TECHNICAL DATA MODEL
* **Slide Title:** DIGITAL TWIN OBJECT MODEL & SPATIAL SCHEMA
* **Standardized Entity Schema (`UniversalObject3D`):**
```json
{
  "id": "NODE-ESP32-ZONEC",
  "type": "SENSOR_TRANSDUCER",
  "position": { "x": 1.45, "y": 0.85, "z": -0.60 },
  "rotation": { "x": 0.0, "y": 90.0, "z": 0.0 },
  "scale": { "x": 1.0, "y": 1.0, "z": 1.0 },
  "zone": "ZONE_B_COMPRESSOR",
  "operational_state": "WARNING",
  "data_truth_state": "LIVE",
  "telemetry": {
    "temperature_c": 54.2,
    "gas_raw_adc": 1820,
    "vibration_rms_mms": 4.15
  },
  "risk_contribution": 45.8,
  "sensor_confidence": 0.982
}
```
* **Coordinate Conventions:** Right-handed Cartesian space normalized to enclosure envelope ($X = \text{Lateral}, Y = \text{Vertical}, Z = \text{Depth}$).

---

### SLIDE 9 — DATA TRUST & CYBER-INTEGRITY MODEL
* **Slide Title:** EVERY DATA POINT HAS A RIGOROUS TRUTH STATE
* **The 6 Data Trust States:**
  * `LIVE`: Directly sampled from physical ESP32 hardware within the last 1500ms.
  * `DERIVED`: Numerically calculated by edge algorithms (e.g., Risk Score, Rate of Change $\Delta T/\Delta t$, Moving RMS).
  * `SIMULATED`: Generated by synthetic fault injection for training and validation.
  * `STALE`: Valid hardware reading whose timestamp exceeds the 3.0-second freshness window.
  * `OFFLINE`: Complete hardware heartbeat timeout ($>5.0\text{s}$); node marked unavailable.
  * `ROADMAP`: Future hardware/protocol integration placeholders clearly labeled for transparency.
* **Byzantine Anti-Spoofing Consensus:**  
  If an analog channel reports a baseline reading ($22^\circ\text{C}$) while adjacent thermal and current transducers indicate heavy overload, the system computes a low Cross-Sensor Plausibility Index, degrades channel confidence to $<20\%$, and alerts the incident commander of data tampering.

---

### SLIDE 10 — EXPLAINABLE RISK & SENSOR CORRELATION
* **Slide Title:** CORRELATE BEFORE YOU ESCALATE: DETERMINISTIC RISK ENGINE
* **Mathematical Risk Formulation:**
  $$\text{Risk Score} = \min\left(100, \left(\sum_{i=1}^{n} w_i \cdot H_i + B_{\Delta} + B_{\text{hist}}\right) \times \left(0.5 + 0.5 \times \frac{\text{Trust Score}}{100}\right)\right)$$
* **Multi-Sensor Attribution Matrix:**
  * **Gas Signal ($MQ\text{-}135$):** $>2500\text{ ADC} \rightarrow +35\text{ pts}$ | $>1500\text{ ADC} \rightarrow +20\text{ pts}$ | $>800\text{ ADC} \rightarrow +10\text{ pts}$
  * **Thermal Load ($DHT22$):** $\ge 50.0^\circ\text{C} \rightarrow +30\text{ pts}$ | $\ge 38.0^\circ\text{C} \rightarrow +20\text{ pts}$ | $\ge 32.0^\circ\text{C} \rightarrow +8\text{ pts}$
  * **Vibration ($ADXL345$):** $\ge 6.0\text{ mm/s} \rightarrow +30\text{ pts}$ | $\ge 3.0\text{ mm/s} \rightarrow +18\text{ pts}$ | $\ge 1.5\text{ mm/s} \rightarrow +8\text{ pts}$
  * **Temporal Rate of Surge ($\Delta / \Delta t$):** Rapid acceleration of any parameter adds $+10\text{ pts}$.
* **Classification Bounds:**
  * $0\text{–}29$: `NORMAL` (Green) | $30\text{–}54$: `WATCH` (Amber) | $55\text{–}79$: `WARNING` (Orange) | $80\text{–}100$: `CRITICAL` (Red)

---

### SLIDE 11 — INCIDENT STATE MACHINE & OPERATIONAL WORKFLOW
* **Slide Title:** THE SYSTEM THINKS IN FORMAL STATES, NOT JUST RAW ALERTS
* **8-Stage Operational State Progression:**
```
  [NORMAL] ──(Threshold Drift)──▶ [WATCH] ──(Correlated Spike)──▶ [ALERT]
                                                                     │
  [STABILIZING] ◀──(Siren/Interlock Active)── [CONTAINMENT] ◀──(Risk ≥ 80)── [INCIDENT]
        │
        ▼
  [RECOVERY] ──(Post-Event Audit & All-Clear Verification)──▶ [NORMAL BASELINE]
```
* **Deterministic Transitions:**
  * `NORMAL ➔ WATCH`: Single sensor anomaly exceeds $1.5\sigma$ standard deviation for $>3$ consecutive frames.
  * `WATCH ➔ ALERT`: Rate of change ($\Delta T/\Delta t$) exceeds critical slope; warning beacon triggered.
  * `ALERT ➔ INCIDENT`: Multi-sensor correlation cross-validates hazard; Risk Score $\ge 80$; E-stop relay trips; 110dB siren activates.
  * `INCIDENT ➔ CONTAINMENT`: Commander acknowledges; physical area cordoned off; dynamic safe routes displayed.
  * `CONTAINMENT ➔ RECOVERY`: Telemetry drops below safe thresholds; post-event incident log hashed and exported.

---

### SLIDE 12 — DISASTER LIFECYCLE: BEFORE, DURING & AFTER
* **Slide Title:** ONE PLATFORM FOR THE COMPLETE DISASTER LIFECYCLE
* **Full-Lifecycle Capability Matrix:**

```
┌────────────────────────────┬────────────────────────────┬────────────────────────────┐
│      BEFORE DISASTER       │      DURING DISASTER       │       AFTER DISASTER       │
│   (Mitigate & Prepare)     │   (Respond & Contain)      │    (Recover & Learn)       │
├────────────────────────────┼────────────────────────────┼────────────────────────────┤
│ • Baseline drift tracking  │ • Sub-second trip interlock│ • Cold-soak stabilization  │
│ • Sensor health audits     │ • 3D Spatial hazard bubbles│ • Cryptographic event logs │
│ • Zone vulnerability checks│ • Dynamic A* egress routes │ • Damage index calculation │
│ • Battery / UPS readiness  │ • Local 110dB siren strobe │ • MTTR / MTBF calculations │
│ • Pre-incident drills      │ • Edge autonomy active     │ • Updated baseline models  │
└────────────────────────────┴────────────────────────────┴────────────────────────────┘
```

---

### SLIDE 13 — QUANTUM-SAFE SECURITY & TELEMETRY INTEGRITY
* **Slide Title:** POST-QUANTUM CRYPTOGRAPHIC RESILIENCE FOR TELEMETRY
* **The Emerging Vulnerability:** Disaster and industrial control networks are vulnerable to **Harvest Now, Decrypt Later (HNDL)** attacks where adversaries store intercepted operational streams for future quantum decryption.
* **PQC Layer Architecture `[PROTOTYPED IN BACKEND]`:
  * **Key Encapsulation (KEM):** **NIST FIPS 203 (ML-KEM-768 / Crystals-Kyber)** generates 32-byte shared secrets encapsulated in 1088-byte ciphertexts.
  * **Digital Signatures (DSA):** **NIST FIPS 204 (ML-DSA-65 / Crystals-Dilithium)** signs telemetry frames with lattice-based mathematical proofs.
  * **Anti-Replay Mechanism:** Monotonic packet counters and HMAC-SHA256 authenticated envelopes prevent replay attacks.
* **Status Statement:** *The cryptographic layer provides a live software prototype of NIST FIPS 203/204 algorithms ready for deployment over standard TLS/DTLS tunnels.*

---

### SLIDE 14 — RESILIENT COMMUNICATIONS & SATELLITE-READY FAILOVER
* **Slide Title:** 4-TIER COMMUNICATION FAILOVER: WHEN NETWORKS COLLAPSE
* **The Failover Hierarchy:**
```
  [Tier 1: High-Speed Terrestrial Ethernet / 4G / Wi-Fi]  (Latency: <30ms | Normal Operations)
                           │ (Physical Backhaul Severed)
                           ▼
  [Tier 2: Emergency HF Packet Radio (7.105 MHz AX.25)]   (Range: 500+ km | Text & Status)
                           │ (Local RF Interference)
                           ▼
  [Tier 3: LEO Satellite Burst (SatNOGS / TinyGS / SBD)]  (Orbital Uplink | 10-Byte Critical Frame)
                           │ (Total RF Blockade)
                           ▼
  [Tier 4: Local Edge Store-and-Forward (SQLite WAL)]      (0% Data Loss | Fully Autonomous)
```
* **Compact 10-Byte Satellite Emergency Burst Format:**
  $$\text{Payload (10B)} = \underbrace{\text{Magic}(2\text{B})}_{\text{0x5358}} + \underbrace{\text{Seq}(2\text{B})}_{\text{UInt16}} + \underbrace{\text{Risk}(2\text{B})}_{\text{Int16}} + \underbrace{\text{Temp}(2\text{B})}_{\text{Int16}} + \underbrace{\text{Vib}(2\text{B})}_{\text{Int16}}$$
* **Status Statement:** *Local Store-and-Forward and SatNOGS ground-station telemetry tracking are fully implemented; physical satellite transceivers are represented via standardized SBD frame serializers.*

---

### SLIDE 15 — FEASIBILITY, SCALABILITY & DEPLOYMENT ROADMAP
* **Slide Title:** FEASIBILITY, VIABILITY & SYSTEM ROADMAP
* **Multi-Dimensional Viability:**
  * **Technical Feasibility:** Built on mature, commercially available embedded platforms (ESP32-S3, Raspberry Pi, Standard SPI/I2C transducers).
  * **Economic Viability:** Low-cost retrofit architecture; instrumentation cost is $<5\%$ of traditional industrial SCADA overhauls.
  * **Operational Viability:** Works completely offline; requires no cloud infrastructure or recurring SaaS subscriptions for core safety.
* **Phased Growth Roadmap:**
  * **Level 1 (Current):** Laboratory Tabletop Prototype with Live 3D Twin and Sensor Array.
  * **Level 2 (6 Months):** Industrial Pilot Enclosure with IP67 field nodes and Modbus RTU integration.
  * **Level 3 (12 Months):** Multi-Gateway LoRa mesh network for facility-wide coverage.
  * **Level 4 (24 Months):** Regional multi-site command center with hardware PQC cryptographic modules and certified satellite uplinks.

---

### SLIDE 16 — LIVE DEMONSTRATION & AUTHORITATIVE REFERENCES
* **Slide Title:** LIVE SYSTEM VERIFICATION & RESEARCH FOUNDATION
* **Live Proof Flow (The Complete Operational Loop in 90 Seconds):**
  1. Show baseline prototype in `NORMAL` (Green 3D twin).
  2. Inject thermal/gas hazard on physical sensor.
  3. ESP32 publishes MQTT telemetry $\rightarrow$ Edge gateway validates $\rightarrow$ Risk score jumps to $92/100$.
  4. 3D Digital Twin renders red hazard bubble $\rightarrow$ E-stop relay trips $\rightarrow$ Siren sounds $\rightarrow$ Dynamic safe egress path renders.
  5. Sever WAN link $\rightarrow$ Edge continues autonomously $\rightarrow$ Reconnect $\rightarrow$ Event ledger syncs.
* **Authoritative Technical References:**
  1. *NIST Special Publication 800-208 / FIPS 203 & 204 (Post-Quantum Cryptography Standardization, 2024)*
  2. *ISO 10816-3: Mechanical Vibration — Evaluation of Machine Vibration by Measurements on Non-Rotating Parts*
  3. *OASIS Standard: MQTT Version 5.0 Core Specification (2019)*
  4. *IEC 61508 / ISO 13849: Functional Safety of Electrical/Electronic/Programmable Safety-Related Systems*
  5. *Libre Space Foundation: SatNOGS Open Satellite Network Documentation (2024)*

---

# SECTION 2: VISUAL SLIDE DESIGN & COLOR PALETTE SPECIFICATION

### Design Aesthetics & Visual Tokens
* **Base Theme:** Dark Industrial Command Center (High-contrast, professional, zero neon/cyberpunk cliches).
* **Color Hierarchy:**
  * **Backgrounds:** Charcoal / Slate Grey (`#0b0f19`, `#111827`, `#1f2937`)
  * **Structural Borders & Cards:** Industrial Steel Border (`#374151`, `#4b5563`)
  * **Primary Data Flow:** Cyan / Cold Blue (`#0284c7`, `#38bdf8`)
  * **Normal / Safe State:** ISO Industrial Green (`#16a34a`, `#22c55e`)
  * **Warning / Elevated State:** Safety Amber / Warning Yellow (`#d97706`, `#f59e0b`)
  * **Critical / Incident State:** High-Visibility Red (`#dc2626`, `#ef4444`)
  * **Text Typography:** Clean Sans-Serif (`Inter`, `Roboto Mono` for numbers and coordinates)

---

# SECTION 3: COMPLETE TECHNICAL SUBSYSTEM ARCHITECTURES

## A. HARDWARE ARCHITECTURE & BILL OF MATERIALS (BOM)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ESP32 SENSOR FIELD NODE                            │
│                                                                             │
│  ┌────────────────────────┐                   ┌──────────────────────────┐  │
│  │   DHT22 Temp/Humidity  │─── GPIO 4 (1-Wire)│                          │  │
│  └────────────────────────┘                   │                          │  │
│  ┌────────────────────────┐                   │      ESP32-WROOM-32      │  │
│  │    MQ-135 Gas/Smoke    │─── GPIO 34 (ADC)  │      Dual-Core 240MHz    │  │
│  └────────────────────────┘                   │     FreeRTOS 100Hz Task  │  │
│  ┌────────────────────────┐                   │                          │  │
│  │  ADXL345 3-Axis Vib    │─── GPIO 21/22(I2C)│                          │  │
│  └────────────────────────┘                   └─────────────┬────────────┘  │
│  ┌────────────────────────┐                                 │               │
│  │  Hardware Trip Relay   │◀── GPIO 18 (Opto-Isolated)──────┘               │
│  └────────────────────────┘                                                 │
└──────────────────────────────────────────────────────────────┼──────────────┘
                                                               │ Wi-Fi / MQTT
                                                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RASPBERRY PI 4 / 5 EDGE BRAIN                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Eclipse Mosquitto MQTT Broker (Local message bus, Port 1883)          │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ FastAPI Python 3.10+ Engine (Sensor Trust + Risk + State Machine)     │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ SQLite Write-Ahead Logging (WAL) Database (sentinel_edge.db)          │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ 110dB Siren & Strobe Beacon Relay Driver (GPIO 17 & 27)               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Bill of Materials (BOM) Table

| Component Name | Model / Specification | Interface / Bus | Functional Role | Implementation State |
| :--- | :--- | :--- | :--- | :---: |
| **Edge Compute Gateway** | Raspberry Pi 4 Model B (4GB) | PCIe / USB 3.0 / GPIO | Edge core, local database, broker & API host | `IMPLEMENTED` |
| **Field Sensor MCU** | ESP32-WROOM-32D | Wi-Fi / FreeRTOS | Multi-sensor acquisition & MQTT transmission | `IMPLEMENTED` |
| **Thermal Probe** | DHT22 / AM2302 | 1-Wire Digital (GPIO4) | Ambient temperature and humidity tracking | `IMPLEMENTED` |
| **Gas / Effluent Sensor** | MQ-135 Gas Sensor Module | Analog 12-bit ADC | Air-quality anomaly and combustion effluent surge | `IMPLEMENTED` |
| **Vibration Transducer** | ADXL345 3-Axis Digital | I2C / SPI (400kHz) | Mechanical shock & structural vibration spectrum | `IMPLEMENTED` |
| **Isolation Relay** | 4-Channel 5V Optocoupled | Active-Low GPIO | Tripping contactors & high-power acoustic sirens | `IMPLEMENTED` |
| **Acoustic Evacuation** | 12V 110dB Multi-Tone Siren | Dry Relay Contact | Physical evacuation alarm on critical events | `IMPLEMENTED` |
| **Optical Warning Beacon** | 12V High-Intensity Amber Strobe| Dry Relay Contact | Visual perimeter danger indicator | `IMPLEMENTED` |

---

## B. DIGITAL TWIN SPATIAL ARCHITECTURE & SCENE GRAPH

### Scene Node Hierarchy
```
SCENE_ROOT (Three.js Scene)
 ├── INDUSTRIAL_ENCLOSURE_GROUP
 │    ├── FLOOR_SLAB (Grey matte material with yellow/black hazard perimeter markings)
 │    ├── REAR_WALL (Industrial paneling shader)
 │    ├── LEFT_WALL (Perimeter fence texture)
 │    └── RIGHT_WALL (Zone boundary mesh)
 ├── SENSOR_NODE_GROUP
 │    ├── NODE_01_MESH (ESP32 Node 1 bounding box + Pin Indicator)
 │    └── NODE_02_MESH (ESP32 Node 2 bounding box + Pin Indicator)
 ├── ASSET_GROUP
 │    ├── MOBILE_ROVER_PLATFORM (Rover body, 4 wheels, dynamic coordinates)
 │    ├── DRIVE_MOTOR_MESH (Induction motor geometry with thermal shader binding)
 │    └── COMPRESSOR_UNIT (Vibration target geometry)
 ├── DYNAMIC_HAZARD_OVERLAYS
 │    ├── THERMAL_VOLUMETRIC_BUBBLE (Translucent expanding red sphere)
 │    ├── GAS_PLUME_PARTICLES (Bounded particle cloud)
 │    └── RESTRICTED_ZONE_BOX (Dynamic red corridor interlock barrier)
 └── EGRESS_NAVIGATION_GROUP
      └── DYNAMIC_PATH_RIBBON (A* calculated safe exit path to Zone D)
```

---

## C. EDGE INTELLIGENCE, RISK FORMULATION & TRUST ENGINE

### 1. Bayesian Sensor Trust & Plausibility Filter
* **Input Vector:** $\vec{S} = [T_{\text{dht}}, G_{\text{mq}}, V_{\text{adxl}}]$
* **Step 1: Noise Filtering:** Kalman filter estimate for continuous states:
  $$\hat{x}_k = \hat{x}_k^- + K_k (z_k - H \hat{x}_k^-)$$
* **Step 2: Plausibility Audit:** Evaluate physical consistency rules:
  $$\text{Consistency Score } C = \begin{cases} 
    1.0 & \text{if } \text{abs}(T_i - \bar{T}_{\text{zone}}) < 3\sigma \text{ and } \text{RateOfRise} < \text{Limit} \\
    0.2 & \text{if sensor value contradicts redundant transducers (Spoofing Flag)}
  \end{cases}$$
* **Step 3: Trust Factor Output:** Fused Trust Index $\tau \in [0.0, 1.0]$ passed to the risk engine.

---

## D. POST-QUANTUM CRYPTOGRAPHY (PQC) & SATELLITE FAILOVER

### 1. Post-Quantum Security Flow
```
[ESP32 / Edge Node]                                      [Central Command / EOC]
        │                                                           │
        │── 1. Request PQC Handshake ──────────────────────────────▶│
        │                                                           │
        │◀── 2. Return ML-KEM-768 Public Key (1184 Bytes) ──────────│
        │                                                           │
        │── 3. Encapsulate Secret -> Ciphertext (1088 Bytes) ──────▶│
        │                                                           │
        │   [Both Derive Identical 32-Byte Quantum-Safe Secret]    │
        │                                                           │
        │── 4. Signed Telemetry Envelope (ML-DSA-65 Signature) ────▶│
```

---

# SECTION 4: FEASIBILITY, IMPACT & VIABILITY REPORT

### 1. Technical Feasibility Analysis
* **Readily Sourced Hardware:** Every sensor and micro-controller utilizes standard commercial COTS (Commercial-Off-The-Shelf) hardware with established supply chains in India.
* **Low Latency Profile:**
  * Sensor sampling to ESP32 buffer: $<10\text{ ms}$
  * Local MQTT publish to Raspberry Pi: $<15\text{ ms}$
  * Edge validation & risk engine evaluation: $<25\text{ ms}$
  * Hardware relay actuation: $<30\text{ ms}$
  * **Total Closed-Loop Interlock Latency: $\approx 80\text{ ms}$ (Hard guarantee $<800\text{ ms}$)**.

### 2. Economic Viability & Cost Comparison

| Deployment Item | Conventional Industrial SCADA / DCS | SENTINEL-X Edge Solution | Cost Advantage |
| :--- | :--- | :--- | :--- |
| **Sensor Node Cost (per point)** | ₹35,000 – ₹75,000 (Proprietary fieldbus) | ₹1,800 – ₹3,500 (ESP32 + COTS) | **~90% Savings** |
| **Central Controller / Gateway** | ₹2,50,000+ (Industrial PLC Rack) | ₹7,500 (Raspberry Pi 4/5 SBC) | **~95% Savings** |
| **Software Licensing** | ₹1,50,000 / year (Proprietary SCADA) | ₹0 (Open-Source Core, Zero SaaS lock-in) | **100% Elimination** |
| **Installation & Retrofitting** | Requires plant shutdown & rewiring | Non-invasive wireless / edge overlay | **Minimal Downtime** |

---

# SECTION 5: JUDGE DEFENSE & Q&A GUIDE (24 ESSENTIAL QUESTIONS)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           JUDGE DEFENSE GOLDEN RULES                                    │
│ 1. Never say "We use AI" if it's a deterministic formula. Call it "Deterministic Risk". │
│ 2. Never say "We have Quantum Computing". Say "We implement Post-Quantum Cryptography". │
│ 3. Never say "We have a live satellite in orbit". Say "Satellite-Ready SBD Protocol".   │
│ 4. Always ground your answer in the physical prototype running before their eyes.       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Q1: What is truly novel about SENTINEL-X? Why isn't this just another IoT dashboard?
> **Answer:** *"Conventional IoT dashboards simply stream raw numbers to a remote cloud database. If the internet fails, they become blind; if an individual sensor drifts, they issue false alarms. SENTINEL-X introduces three core innovations: (1) An Edge-First deterministic safety loop that trips physical interlocks in under 80ms locally without cloud dependency; (2) A 3D Spatial Digital Twin synchronized with our physical prototype that renders dynamic hazard perimeters and egress routes; and (3) Complete Before, During, and After disaster lifecycle management with cryptographic event auditing."*

#### Q2: Why is edge computing necessary here? Why not use AWS IoT or Firebase?
> **Answer:** *"In severe disaster scenarios—such as industrial fires, earthquakes, or urban flash floods—cellular towers and fiber backhauls are often the first infrastructure to collapse. Sending raw 100Hz telemetry to a cloud broker introduces 200–500ms of non-deterministic WAN latency and creates a single point of failure. By computing sensor trust, risk escalation, and relay cutoff directly on the local Raspberry Pi edge controller, our core safety loop continues uninterrupted even during complete network blackouts."*

#### Q3: Is the 3D Digital Twin an actual CAD model of a random factory, or is it bound to your prototype?
> **Answer:** *"Our 3D Digital Twin is an exact 1:1 spatial reconstruction of the physical three-sided industrial enclosure sitting on the table. Every sensor pin, yellow/black safety marking, and mobile rover coordinate in the 3D Three.js scene graph maps directly to physical coordinates on our hardware prototype."*

#### Q4: What happens if an individual sensor fails or gives false readings?
> **Answer:** *"Our Sensor Trust Engine applies temporal persistence and Bayesian plausibility checks. If a single sensor experiences an abrupt spike without corroborating telemetry from adjacent transducers (for example, high gas without thermal change or rate-of-rise confirmation), the system flags it as `WATCH`, degrades that channel's trust weight to $<20\%$, and escalates the uncertainty to the operator rather than triggering a false alarm."*

#### Q5: Is the MQ-135 sensor a calibrated toxic gas detector?
> **Answer:** *"No, and we explicitly declare that in our engineering documentation. The MQ-135 is utilized as an analog air-quality and combustion effluent anomaly indicator. It detects relative surges above baseline levels ($\Delta ADC / \Delta t$) rather than calibrated parts-per-million gas identification, which would require laboratory optical spectroscopy."*

#### Q6: How does the system handle complete internet disconnection?
> **Answer:** *"The Raspberry Pi edge gateway maintains an internal SQLite database operating in Write-Ahead Logging (WAL) mode. When the WAN link drops, the system seamlessly transitions to Tier-4 Autonomous Edge Mode: telemetry, risk states, and timestamped actions buffer locally in the WAL queue while local sirens and interlocks remain fully operational. Once network connectivity is restored, the buffered queue synchronizes upstream automatically with zero data loss."*

#### Q7: Where is Quantum technology used in your project?
> **Answer:** *"We do NOT use quantum computers. We have implemented Post-Quantum Cryptography (PQC) based on NIST FIPS 203 (ML-KEM-768 for lattice-based key encapsulation) and NIST FIPS 204 (ML-DSA-65 for lattice-based digital signatures). This protects critical disaster telemetry and command streams against 'Harvest Now, Decrypt Later' quantum attacks."*

#### Q8: Where is Satellite communication used, and is it live today?
> **Answer:** *"The current physical prototype operates over a local Wi-Fi and MQTT network. However, our communication architecture includes a prototyped Tier-3 Satellite-Ready layer that formats 10-byte binary Short Burst Data (SBD) packets and integrates with SatNOGS open ground station tracking. It is architected so a physical satellite modem (like Iridium SBD) can be plugged directly into the UART port without rewriting any application logic."*

#### Q9: What happens after the disaster is contained? How is recovery handled?
> **Answer:** *"Once the risk engine confirms environmental variables have returned below safety thresholds, the system transitions into the `STABILIZING` and `RECOVERY` states. It freezes the incident timeline, calculates key performance metrics (Time to Detect, Time to Acknowledge, Time to Contain), and generates a cryptographically signed JSON Incident Audit Report for post-disaster analysis."*

#### Q10: How scalable is this platform from a single prototype to a city or large plant?
> **Answer:** *"Our architecture is inherently modular. Each physical zone operates an autonomous Edge Cluster (Raspberry Pi + ESP32 nodes). Multiple edge clusters communicate via lightweight MQTT bridges or mesh networks to a Central Emergency Operations Center (EOC). You can scale from 1 enclosure to 500 industrial bays without re-architecting the core software."*

---

# SECTION 6: 90-SECOND LIVE DEMONSTRATION SCRIPT

* **Presenter 1 (Hardware Lead):** Standing by the physical prototype.
* **Presenter 2 (Software / Twin Lead):** Operating the Command Center laptop screen.

```
[00:00 - 00:15] BASELINE STABILITY
Presenter 1: "Judges, observe our physical prototype on the left and its live 3D Digital Twin on the right. Currently, both are in the NORMAL state. The Three.js twin is glowing green, telemetry is streaming at 1.0 Hz, and sensor trust is 100%."

[00:15 - 00:35] HAZARD INJECTION & SENSING
Presenter 1: "I am now introducing a thermal and air-quality hazard to ESP32 Node 1 on the prototype."
Presenter 2: "Notice the telemetry panel: Temperature rises above 50°C and MQ-135 gas signal surges. The ESP32 publishes to our local MQTT broker on the Raspberry Pi."

[00:35 - 00:55] EDGE RISK & CLOSED-LOOP INTERLOCK
Presenter 2: "Our Explainable Risk Engine calculates a composite risk score of 94/100. Instantly, the Incident State transitions from NORMAL to CRITICAL."
Presenter 1: "Listen to the hardware: The edge gateway has tripped the physical relay, de-energizing the equipment contactor and sounding the 110dB acoustic siren in under 80ms!"

[00:55 - 01:15] SPATIAL TWIN & DYNAMIC EGRESS
Presenter 2: "On the 3D Digital Twin, the affected zone turns high-visibility red with an expanding hazard bubble. Because Corridor B is compromised, our A* pathfinder dynamically computes a green safe evacuation route guiding personnel to Zone D."

[01:15 - 01:30] RESILIENCE & RECOVERY AUDIT
Presenter 1: "I will now physically unplug the network router. Notice that the Edge Brain continues autonomous monitoring and logging in SQLite WAL mode."
Presenter 2: "As the hazard clears, we click 'Acknowledge & Recover'. The system resets the relay, returns to baseline, and exports a cryptographically hashed incident audit report. From physical transducer to edge intelligence to spatial twin to recovery—that is SENTINEL-X."
```

---

# SECTION 7: 2-MINUTE MASTER PITCH SCRIPT

> *"Respected Evaluators, in any disaster, the difference between a near-miss and a catastrophe is measured in seconds. Yet today, most disaster management systems suffer from three critical flaws: they rely on fragile cloud backhauls that fail during emergencies; they overwhelm commanders with raw 2D charts; and they discard operational context the moment an incident ends.*
>
> *We built **SENTINEL-X** to bridge this gap through a hardware-first, edge-intelligent architecture.*
>
> *At its core, SENTINEL-X starts at the physical transducer layer: custom ESP32 field nodes sampling thermal, gas, and vibration spectrums at 100Hz. This telemetry feeds directly into a local Raspberry Pi edge controller running an Explainable Risk Engine and Bayesian Sensor Trust validator. When a hazard is detected, SENTINEL-X does not wait for a cloud round-trip; it trips local isolation relays and sounds evacuation sirens within 80 milliseconds.*
>
> *Simultaneously, SENTINEL-X projects this physical reality into an interactive 3D Spatial Digital Twin built in Three.js. Commanders do not see abstract data tables—they see 3D volumetric hazard zones, compromised pathways, and dynamically routed safe evacuation corridors.*
>
> *To guarantee operational continuity, our system is engineered for resilience: a 4-tier communication failover that operates locally via SQLite Write-Ahead Logging when networks collapse, with a satellite-ready burst architecture and NIST FIPS 203/204 Post-Quantum Cryptographic protection.*
>
> *SENTINEL-X is not a conceptual mockup—it is a functional, demonstrable hardware and software platform managing the entire disaster lifecycle before, during, and after an event. Thank you."*
