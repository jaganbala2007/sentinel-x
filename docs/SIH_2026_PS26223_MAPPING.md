# SENTINEL-X Alignment Matrix for SIH 2026 Problem Statement 26223

**Problem Statement Title**: Student Innovation - Disaster management includes ideas related to risk mitigation, Planning and management before, after or during a disaster.  
**Problem Statement ID**: 26223  
**Organization**: AICTE (Ministry of Education Innovation Cell)  
**Category**: Hardware  
**Theme**: Disaster Management  

---

## Executive Summary

**SENTINEL-X** is an edge-intelligent, hardware-backed disaster management platform. It combines ESP32 field sensing nodes, Raspberry Pi 4 edge controller, local Write-Ahead Logging (WAL) database, Explainable Edge Intelligence, and a 3D Three.js Spatial Digital Twin to provide full-lifecycle disaster resilience:

$$\text{BEFORE DISASTER} \longrightarrow \text{DURING DISASTER} \longrightarrow \text{AFTER DISASTER}$$

---

## Core Requirement vs. Sentinel-X Solution Matrix

| SIH PS 26223 Requirement | Sentinel-X System Solution | Technical Implementation & Ground-Truth Evidence |
| :--- | :--- | :--- |
| **1. Risk Mitigation** | Continuous Environmental Sensing & Explainable Risk Engine | Computes dynamic $Risk = Severity \times Exposure \times Vulnerability \times Confidence$. Provides factor attribution breakdown (MQ-135 Gas, DHT22 Temp, ADXL345 Vibration). |
| **2. Planning & Preparedness** | Hazard Zone Mapping & Resource Management | Partitions physical space into Zones A, B, C, D with color-coded safety states (GREEN, AMBER, ORANGE, RED, GREY). Tracks response teams and first-aid assets. |
| **3. Before Disaster** | Trend Analysis & Early Warning Engine | Evaluates rate of change ($\Delta h / \Delta t$) and triggers Level 0–3 warnings (Watch, Warning, Critical) before catastrophic escalation. |
| **4. During Disaster** | 3D Spatial Digital Twin & Evacuation Command | Interactive Three.js 3D cockpit highlighting active hazard zones, camera visual verification, blocked corridors, and safe exit routing. |
| **5. After Disaster** | Post-Disaster Recovery & Damage Assessment Engine | Freezes incident timeline, computes performance metrics (Detection Time, Ack Time, Response Time, Recovery Time), and generates official Incident Reports. |
| **6. Hardware Component** | ESP32 Sensor Nodes + Raspberry Pi 4 Edge Controller | ESP32 field sensing (DHT22, MQ-135, ADXL345) communicating via MQTT to local Raspberry Pi 4 edge controller with local USB webcam. |
| **7. Resilience & Offline Mode** | Store-and-Forward WAL Engine | Operates completely offline during WAN/cloud network failure using local SQLite WAL event buffering and automatic queue sync when connectivity resumes. |

---

## 12 Core Disaster Functions Mapping

1. **A. RISK MITIGATION**: Multi-sensor thresholding and explainable factor attribution.
2. **B. DISASTER PREPAREDNESS**: Zone partitioning (Zones A–D) and pre-disaster health checks.
3. **C. EARLY WARNING**: Level 0–3 alerts specifying What, Where, When, Why, Confidence, and Action.
4. **D. REAL-TIME MONITORING**: 1.0 Hz telemetry streaming over MQTT and WebSockets.
5. **E. INCIDENT DETECTION**: Multi-sensor cross-validation (e.g. MQ-135 + Temp + Camera = Fire).
6. **F. RESPONSE MANAGEMENT**: Commander incident command workflow (Acknowledge $\rightarrow$ Assign $\rightarrow$ Evacuate $\rightarrow$ Resolve).
7. **G. SITUATIONAL AWARENESS**: 3D spatial Three.js digital twin with interactive node/zone inspection.
8. **H. RESOURCE MANAGEMENT**: Emergency equipment & response team availability tracking.
9. **I. DAMAGE ASSESSMENT**: Post-disaster damage summary and equipment impact reporting.
10. **J. RECOVERY MANAGEMENT**: Stabilization tracking and recovery state machine transitions.
11. **K. INCIDENT ANALYSIS**: Timeline metrics (Detection Time, Ack Time, Response Time, Recovery Time).
12. **L. RESILIENCE / OFFLINE OPERATION**: Raspberry Pi 4 edge independence with SQLite WAL queue buffering.
