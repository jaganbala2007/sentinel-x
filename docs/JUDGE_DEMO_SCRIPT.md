# SENTINEL-X Hackathon Judge Demonstration Script
## SIH 2026 Problem Statement ID: 26223 (3–5 Minute Presentation)

This script outlines the exact live demonstration flow for hackathon judges, showcasing the complete disaster management lifecycle.

---

## Presentation Overview

**Elevator Pitch (30 Seconds)**:
> "Respected Judges, welcome to SENTINEL-X: an Edge-AI Disaster Resilience, Situational Awareness & Response System built specifically for SIH 2026 PS 26223. Unlike basic IoT dashboards or cloud-only apps, Sentinel-X combines physical ESP32 sensing, Raspberry Pi 4 edge processing, a 3D Spatial Digital Twin, multi-sensor cross validation, offline resilience, and post-disaster recovery tracking into one unified platform."

---

## 9-Scene Live Demonstration Flow

### Scene 1: Normal Operations & Spatial Digital Twin (0:00 - 0:30)
- **Action**: Show the Command Center Cockpit UI.
- **Narrative**: Point to the 3D Digital Twin showing Zones A, B, C, D in **GREEN (NORMAL)** state. Show live sensor telemetry from ESP32 Node 1 and Node 2 streaming at 1.0 Hz.

### Scene 2: Pre-Disaster Risk Increase (0:30 - 1:00)
- **Action**: Select **Preparedness / Risk Mitigation Module** tab or trigger Scenario 1 (Fire/Smoke) in Simulation Mode.
- **Narrative**: "Notice how the Explainable Risk Score increases to 58/100 (WARNING state). The system breaks down exact contributing factors: Air Quality (+25), Temperature (+15), Vibration (+18)."

### Scene 3: Multi-Sensor Early Warning (1:00 - 1:30)
- **Action**: Point out the Early Warning Alert widget (Level 2: WARNING).
- **Narrative**: "Sentinel-X cross-validates MQ-135 gas readings with thermal sensors and camera feed. It displays 89% Confidence with explicit evidence array, avoiding single-sensor false alarms."

### Scene 4: Critical Incident Detection & Zone Highlighting (1:30 - 2:00)
- **Action**: Advance scenario step to CRITICAL breach.
- **Narrative**: "Zone B immediately transitions to **RED (CRITICAL)** on both the 2D Hazard Map and the 3D Three.js Digital Twin. Automated edge interlocks engage."

### Scene 5: Offline Resilience & Store-and-Forward (2:00 - 2:30)
- **Action**: Toggle Network Mode to **OFFLINE / DISCONNECTED**.
- **Narrative**: "In a real disaster, internet connectivity often fails. Notice that Sentinel-X continues local edge monitoring uninterrupted on the Raspberry Pi 4, queueing all events in an offline SQLite WAL database."

### Scene 6: Incident Command & Evacuation Management (2:30 - 3:00)
- **Action**: Switch role to **DISASTER COMMANDER**. Click **Acknowledge Incident**, **Trigger Zone B Evacuation**, and **Assign Hazmat Response Team RES-01**.
- **Narrative**: "The Commander receives spatial evacuation routes, marks blocked corridors, and deploys emergency resources."

### Scene 7: Incident Stabilization & Recovery (3:00 - 3:30)
- **Action**: Click **Neutralize & Resolve Incident**.
- **Narrative**: "Telemetry normalizes, Zone B turns back to GREEN, and the Disaster State Machine moves to RESOLVED."

### Scene 8: Post-Disaster Report & Damage Assessment (3:30 - 4:00)
- **Action**: Open the **Post-Disaster Recovery Module** tab and view the generated **Incident Report RPT-INC-8901**.
- **Narrative**: "The system freezes the incident timeline and displays calculated metrics: Detection Time (3.2s), Ack Time (14.5s), Response Time (32s), Recovery Time (7.1 mins)."

### Scene 9: Network Reconnection & Queue Synchronization (4:00 - 4:30)
- **Action**: Reconnect Network Mode.
- **Narrative**: "When connectivity returns, all 37 buffered offline records synchronize automatically to central servers."
