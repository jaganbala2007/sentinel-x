# 🧪 Sentinel-X Fault Injection & Stress Testing Lab

**Document Version:** 2.4.0  
**Purpose:** Controlled Physical and Cyber Fault Injection Framework for SIH Judges  
**Verification:** Validates edge resilience under failure modes

---

## 1. Fault Injection Test Catalog

```mermaid
flowchart LR
    subgraph INJECTORS ["Controlled Fault Injectors"]
        F1["1. Sensor Drift / Thermal Inrush (+45°C)"]
        F2["2. Byzantine Sensor Spoof (180°C Glitch)"]
        F3["3. Mechanical Vibration Shock (12.4 mm/s)"]
        F4["4. Pinch-Point Zone Intrusion (0.4m)"]
        F5["5. Complete Internet Outage (Ethernet Cut)"]
        F6["6. Power Degradation (AC Lost, Battery 25%)"]
    end

    subgraph RESPONSES ["Deterministic Sentinel-X Defenses"]
        R1["TinyML Anomaly Alert + Rule Escalation"]
        R2["Trust Drops to 12% → QUARANTINED (No False Trip)"]
        R3["ISO 10816 Limit Exceeded → 415V Relay Trip (<800ms)"]
        R4["Worker Safety E-Stop Interlock Triggered"]
        R5["Isolated Mode Active → Events Queued to SQLite WAL"]
        R6["Load Shedding Active → Core Safety Survives >18h"]
    end

    F1 --> R1
    F2 --> R2
    F3 --> R3
    F4 --> R4
    F5 --> R5
    F6 --> R6
```

---

## 2. Step-by-Step Fault Verification Guide

### Test 1: Byzantine Sensor Spoofing
- **Command / Trigger:** In the Mission Cockpit, select `INJECT FAULT: SPOOF PT100 (180°C)`.
- **Expected System Response:**
  1. Sensor Trust Engine detects a $11,200^\circ\text{C/s}$ step rate-of-change violation.
  2. PT100 Trust Score drops from 99% to 12.5% (`QUARANTINED`).
  3. Risk Engine **DOES NOT TRIP** the motor.
  4. SCADA Cockpit highlights the faulty node in orange/red with explanation: *"Unphysical thermal gradient without mechanical load correlation."*

### Test 2: Catastrophic Internet Disconnect
- **Command / Trigger:** Toggle `COMMUNICATION BLACKOUT` switch in the cockpit.
- **Expected System Response:**
  1. Primary Internet indicator turns red (`FAILED`).
  2. System enters **Isolated Autonomous Mode**.
  3. Induce physical or simulated thermal overload: **Hardware relay trips locally in <800ms**.
  4. Local SQLite WAL and USB Blackbox record the incident (`PENDING_STORE_FORWARD`).
  5. HF Packet Radio simulation transmits emergency alert packet.
  6. Reconnect Internet: Store-and-forward queue synchronizes all records with zero data loss.
