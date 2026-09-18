# Sentinel-X Disaster Intelligence Platform Architecture

> **System Core Principle:**  
> *"WHEN INFRASTRUCTURE FAILS, SAFETY CONTINUES."*

---

## 1. System Topology Overview

Sentinel-X operates across a multi-tier resilient architecture designed to maintain autonomous life-safety operations when remote cloud servers, optical backhauls, and power grids collapse:

```
PHYSICAL DISASTER ENVIRONMENT
(Watershed Basin, River Gauges, Soil Saturation, Rainfall)
               │
               ▼
┌────────────────────────────────────────┐
│  DISTRIBUTED ESP32-S3 SENSOR FLEET     │
│  • Microsecond FreeRTOS task schedule  │
│  • Normalized multi-sensor drivers     │
│  • Kinematic plausibility verification │
│  • Local autonomous siren GPIO relay   │ ──► [PHYSICAL SIREN & BEACONS]
│  • Compact binary frame serialization  │     (Survives Gateway Loss!)
└──────────────────┬─────────────────────┘
                   │ UART / RS-485 / ESP-NOW
                   ▼
┌────────────────────────────────────────┐
│   RASPBERRY PI 5 EDGE GATEWAY          │
│  • Byzantine Sensor Trust Engine       │
│  • Additive Bayesian Disaster Fusion   │
│  • Local SQLite Store-and-Forward WAL  │
│  • FastAPI REST & WebSocket Server     │
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│    COMMUNICATION RESILIENCE MANAGER    │
│  ├── Priority 1: Broadband Internet    │ (TLS / MQTT Primary)
│  ├── Priority 2: HF Packet Radio       │ (7.105 MHz AX.25 NVIS Emergency)
│  ├── Priority 3: Satellite IoT         │ (Iridium SBD 340B Last Resort)
│  └── Priority 4: Autonomous Isolated   │ (SQLite Local Buffer & WAL)
└──────────────────┬─────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│   EMERGENCY OPERATIONS CENTER (EOC)    │
│  • High-Density SCADA Status Bar       │
│  • Tactical Vector GIS Topological Map │
│  • Three.js 3D Elevation Digital Twin  │
│  • Explainable AI Factor Decomposition │
│  • 5 SIH Hero Demonstration Flows      │
└────────────────────────────────────────┘
```

---

## 2. The 4 Operational System Modes

Sentinel-X transitions dynamically between 4 discrete system states depending on infrastructure availability:

| Mode | Communication Path | Sensor Health | Edge Gateway | Local Siren Relay | Cloud Sync |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MODE 1: NORMAL** | Primary Broadband / LTE | 18–20 Online (Verified) | Online (RPi 5) | Armed / Standby | Real-Time Live |
| **MODE 2: DEGRADED**| Emergency HF Packet Radio (7.105 MHz)| Verified Nodes Active | Online (RPi 5) | Armed / Standby | Emergency Bulletins Only |
| **MODE 3: EMERGENCY**| Satellite IoT Burst (LEO SBD) | Critical Nodes Prioritized| Online (RPi 5) | Actuated on High Risk| 16-Byte Telemetry Packets |
| **MODE 4: ISOLATED** | Total RF/Cellular Blackout | Local ESP32-S3 Active | Online or Degraded| **AUTONOMOUS ACTIVE** | **Buffered in SQLite WAL** |

---

## 3. Sensor Trust & Byzantine Quarantine Engine

Traditional disaster management dashboards indiscriminately average sensor values, making them vulnerable to single-point electrical shorts, calibration drift, or sensor spoofing attacks.

Sentinel-X enforces a 4-stage mathematical validation gate:
$$\text{Trust Score} = 100 - (\text{Penalty}_{\text{datum}} + \text{Penalty}_{\text{kinematic}} + \text{Penalty}_{\text{consensus}})$$

1. **Hydraulic Datum Bounds:** Rejects values outside the river basin's physical 0–12m datum.
2. **Kinematic Rate-of-Rise ($\Delta h / \Delta t$):** Evaluates whether the derivative exceeds hydrodynamic expansion limits ($> 0.50\text{ m/min}$).
3. **Spatial Consensus Correlation ($r$):** Cross-correlates telemetry with adjacent upstream/downstream nodes.
4. **Byzantine Isolation:** Any node falling below $50\%$ trust is placed in Quarantine and excluded from the Bayesian risk aggregator.

---

## 4. Additive Bayesian Risk Evidence Model

Rather than relying on ungrounded deep learning predictions, the Sentinel-X disaster engine decomposes risk confidence additively:

$$\text{Risk}(t) = W_{\text{stage}} + W_{\text{rise}} + W_{\text{rain}} + W_{\text{soil}} + W_{\text{consensus}} + W_{\text{hist}}$$

- $W_{\text{stage}}$: River stage elevation relative to baseline datum ($+35$ max)
- $W_{\text{rise}}$: Kinematic rate of rise ($+25$ max)
- $W_{\text{rain}}$: Basin precipitation intensity ($+14$ max)
- $W_{\text{soil}}$: Catchment soil saturation deficit ($+8$ max)
- $W_{\text{consensus}}$: Multi-node spatial agreement ($+10$ max)
- $W_{\text{hist}}$: Historical hydrological pattern correlation ($+2$ max)

The resulting score ($0–100$) maps deterministically to operational alert states:
- $\text{Score} < 25$: **NORMAL** (Steady monitoring)
- $25 \le \text{Score} < 45$: **WATCH** (Increased polling)
- $45 \le \text{Score} < 75$: **WARNING** (Arm HF radio, stage evacuation corridors)
- $\text{Score} \ge 75$: **CRITICAL** (Actuate acoustic sirens, dispatch municipal alerts)
