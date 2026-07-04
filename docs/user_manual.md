# Sentinel-X Operator User Manual

**Version 1.0.0 | For: Admin, Supervisor, Safety Officer, Worker**

---

## 1. Introduction

The Sentinel-X Cockpit Dashboard is the unified control interface for your AI Safety Operating System. This manual covers:

- Accessing the system (authentication)
- Navigating the 8-panel cockpit
- Responding to alerts
- Triggering and managing emergency simulations
- Interpreting sensor telemetry
- Using the AI Oracle Terminal
- Exporting safety reports

---

## 2. Accessing the System

### 2.1 System Requirements

| Requirement | Minimum |
|---|---|
| Browser | Chrome 110+, Firefox 115+, Edge 110+ |
| GPU | Hardware-accelerated graphics (WebGL) |
| Screen | 1280×720 minimum (1920×1080 recommended) |
| Network | Local LAN access to fog server or internet (demo) |

### 2.2 Authentication

1. Navigate to the system URL (e.g., `http://localhost:8000` or deployed URL)
2. Click **"Enter Console"** on the landing page
3. **Select your Security Role** from the 4 options:
   - **Admin** — Full system access
   - **Supervisor** — Operational control
   - **Safety Officer** — Safety data and reports
   - **Worker** — Personal vitals view only
4. Your email is pre-filled based on selected role
5. Enter your **Authorization Key** (password)
6. Click **"Initiate Secure Authentication"**
7. Enter the **6-digit Security Token** shown on-screen (pre-filled for demo)
8. Click **"Verify Security Token"**

> In demo mode, all credentials and OTPs are pre-filled. Click through each screen.

---

## 3. Cockpit Dashboard Navigation

The main cockpit is divided into a **sidebar navigation** (left) and **main content area** (right).

### 3.1 Sidebar Menu

| Menu Item | Icon | Description |
|---|---|---|
| Control Dashboard | Grid | KPI overview + floor map + alerts |
| 3D Digital Twin | Cube | Interactive 3D factory visualization |
| Computer Vision | Video | CCTV AI stream analysis |
| AI Agent Mesh | Brain | Agent status + AI terminal |
| Safety Analytics | Chart | Telemetry charts + data export |
| Wearable / Watch | Watch | Worker biometrics + SOS |
| OpenAPI / Swagger | Code | REST API interactive console |
| System Settings | Gear | Thresholds + notification config |

### 3.2 Header Status Bar

The top header shows real-time system health:
- **AI Health** — Percentage of AI agents functioning normally
- **Safety Index** — Overall plant-wide OSHA safety rating
- **Alerts (24h)** — Total alerts with active alarm count
- **Global Siren** — 🔴 Button to manually activate/deactivate plant-wide siren
- **User Profile** — Current role and logout button
- **Live Clock** — Real-time UTC clock

---

## 4. Control Dashboard

The main operational overview panel.

### 4.1 KPI Cards

| Card | Meaning | Threshold |
|---|---|---|
| Active Workers | Currently tracked personnel | All must show 100% Tracking |
| Gas Sensors | Active sensor count | 0 anomalies = Normal |
| Machinery Vitals | Machines in nominal state | 32/32 = all healthy |
| Accident Predictions | AI risk predictions | 0 = No predicted incidents |

### 4.2 2D Spatial Tracking Map

- **Blue dots** — Worker nodes (UWB tracked)
- **Yellow rectangle** — Forklift patrol vehicle
- **Red shaded area** — Restricted compressor zone (Zone B)
- **Yellow dashed line** — Safety egress exit route

**Zone Breach Alert:** When a worker enters the red restricted zone, their dot turns red and an automated **Intrusion Warning** alert is logged to the Alert Stream.

### 4.3 Alert Activity Stream

- Alerts appear newest-first
- **Blue** = Informational
- **Orange** = Warning (with audio beep)
- **Red** = Critical (with alarm sound)

Click **"Clear"** to dismiss all current alerts from view (does not delete from database).

---

## 5. 3D Digital Twin

### 5.1 Camera Controls

| Control | Action |
|---|---|
| Left mouse drag | Orbit/rotate camera |
| Right mouse drag | Pan camera |
| Mouse scroll | Zoom in/out |
| Boiler Area button | Snap camera to boiler zone |
| Conveyor Line button | Snap camera to conveyor zone |

### 5.2 Emergency Simulations

Click any simulation button in the top-left control panel:

| Simulation | Effect |
|---|---|
| **Gas Leak** | Green volumetric gas cloud appears at boiler; CRITICAL alert logged; phone warning triggered |
| **Boiler Fire** | Boiler mesh flashes red/orange; spark particles emit; camera focuses on boiler |
| **Evac Route** | Green floor paths drawn to exits; workers move toward exits; evacuation alert logged |
| **Reset Scene** | All simulations cleared; workers return to patrol positions |

### 5.3 Lighting Presets

| Preset | Effect |
|---|---|
| Sunny | Standard ambient lighting |
| Night | Low ambient, dark blue sky |
| Stormy | Dim ambient, dark atmosphere |

### 5.4 Time-Travel Mode

The bottom timeline scrubber allows replaying historical scenarios:
- Drag to any hour (0–23) to simulate historical worker positions
- Click **Pause/Play** to freeze/resume live animation
- At hour 24 = **Live Stream Mode** (real-time)

---

## 6. Computer Vision Panel

Four simulated CCTV feeds running at 30fps:

| Camera | Location | AI Model | Detections |
|---|---|---|---|
| CCTV_01 | Gate PPE Guard | YOLOv11s-PPE | Helmet, vest, gloves compliance |
| CCTV_02 | Compressor Zone | YOLOv11x | Restricted area intrusion |
| CCTV_03 | Conveyor Line | YOLOv11m | Asset tracking |
| CCTV_04 | Assembly Floor | Pose Net | Behavior + fall detection |

**Fall Detection:** CCTV_04 simulates a worker fall every ~20 seconds. When detected:
- Bounding box turns red
- Label changes to **"BEHAVIOR: FALL DETECTED"**
- **CRITICAL alert** is logged
- Phone companion shows emergency warning

---

## 7. AI Agent Mesh Panel

### 7.1 Agent Status Board

| Agent | Status Colors |
|---|---|
| Nominal | Green badge |
| Warning | Yellow badge |
| Critical | Red badge |

### 7.2 AI Oracle Terminal Commands

| Command | Response |
|---|---|
| `/status` | Full system safety analysis (workers, gas, boiler, safety index) |
| `/leak` | Triggers gas leak simulation + critical alert |
| `/fire` | Triggers boiler fire simulation + critical alert |
| `/shutdown` | Issues PLC machine lockout command + success confirmation |
| Any other text | AI reasoning chain-of-thought response referencing live telemetry |

---

## 8. Safety Analytics

### 8.1 Charts

| Chart | Type | X-Axis | Y-Axis |
|---|---|---|---|
| Historical Safety Rating | Line | Time (hourly) | Safety % (95–100%) |
| Gas Concentration | Bar | Factory zones | PPM concentration |
| Boiler Core Vibration | Line | Sample sequence | Hz frequency |
| Worker Cognitive Load | Area | Worker IDs | HRV/SpO2 score |

### 8.2 Data Export

| Format | Contents |
|---|---|
| **Export PDF Report** | Opens browser print dialog for PDF |
| **Export Excel Data** | Downloads `.xls` with key metrics |
| **Export CSV Logs** | Downloads telemetry `.csv` with worker vitals |

---

## 9. Wearable Cockpit

### 9.1 Smartwatch Simulator

- Displays live heart rate (fluctuates ±1 BPM every 3 seconds)
- **SOS Broadcast button** — Press to simulate emergency SOS:
  - Triggers Evacuation simulation in 3D Twin
  - Logs CRITICAL "WORKER SOS ACTIVE" alert
  - Updates phone companion to show emergency warning

### 9.2 Phone Companion App

Shows zone safety status:
- **Green** — Zone is safe (shield-check icon)
- **Red pulsing** — Active emergency in worker's zone

---

## 10. System Settings

### 10.1 Sensor Thresholds

| Parameter | Default | Action on Exceed |
|---|---|---|
| CO2 Warning Limit | 800 PPM | Warning alert dispatched |
| Temperature Shutdown | 85°C | Machine lockout + critical alert |
| Compressor Max Vibration | 120 Hz | Warning alert + maintenance flag |
| Noise Exposure | 85 dB | Warning to affected workers |

### 10.2 Notification Dispatch

| Channel | Default | Function |
|---|---|---|
| SMS Alerts to Supervisors | ✅ Enabled | Critical events → supervisor SMS |
| WhatsApp Evacuation Logs | ✅ Enabled | Evacuation routes → all worker phones |
| Auto PLC Shutdown on Red Siren | ✅ Enabled | Siren activation → automatic machine lockout |

Click **"Save Configuration"** to apply changes to edge fog controllers.

---

## 11. Emergency Response Procedures

### Gas Leak Response
1. Alert stream shows **CRITICAL GAS LEAK DETECTED**
2. Switch to **3D Digital Twin** to view affected zone
3. Use AI Oracle: type `/shutdown` to lock out compressor
4. Trigger **Evac Route** simulation for affected zone workers
5. Activate **Global Siren** via red button in header
6. Contact emergency services

### Worker Fall Response
1. CCTV_04 shows **BEHAVIOR: FALL DETECTED**
2. Critical alert logged with timestamp and zone
3. Phone companion of nearby supervisors shows emergency warning
4. Dispatch medical team to Assembly Floor Zone A
5. Acknowledge alert in Alert Stream after response dispatched

---

## 12. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + S` | (Settings panel) Save configuration |
| `Escape` | Close modals / reset focus |

---

*For technical architecture documentation, see [architecture.md](architecture.md).*  
*For API reference, see [api_specs.json](api_specs.json).*
