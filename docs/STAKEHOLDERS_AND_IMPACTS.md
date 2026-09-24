# 🛡️ SENTINEL-X — STAKEHOLDERS & OPERATIONAL IMPACTS SLIDE (PPT SPECIFICATION)

> **Designed for SIH 2026 Problem Statement 26223 | Tata Steel Mines & Heavy Industrial Smelters**  
> **Visual Reference & Asset Location:**
> - 🌐 **Interactive PPT Slide & 4K PNG Exporter:** [`stakeholders-impacts.html`](file:///e:/tata%20updated/tata/stakeholders-impacts.html) or [`frontend/src/stakeholders-impacts.html`](file:///e:/tata%20updated/tata/frontend/src/stakeholders-impacts.html)
> - 📐 **Direct Vector SVG for PowerPoint:** [`docs/STAKEHOLDERS_AND_IMPACTS.svg`](file:///e:/tata%20updated/tata/docs/STAKEHOLDERS_AND_IMPACTS.svg)
> - 🎯 **PowerPoint Slide Placement:** **Slide 5: Operational Impact, Stakeholders & Scalability**

---

## 🎨 SLIDE VISUAL ARCHITECTURE

The layout matches the 4-stage sequential persona timeline with top cloud callouts, middle action triggers, bottom impact containers, and an overarching regulatory governance column on the right:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [STAKEHOLDERS & IMPACTS]                                                         [Tata Steel & Deep Extraction Mines Scenario]   │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                                  │
│   ┌────────────────────┐            ┌────────────────────┐            ┌────────────────────┐            ┌────────────────────┐   │
│   │ Smart Voice / SOS  │            │ AI Engine Assigns  │            │ 3D Twin Cross-Val  │            │ ERP / SAP Sync     │   │
│   │ Hazard Logged      │            │ Nearest Crew       │            │ Multi-Sensor Trust │            │ Operations Storage │   │
│   └─────────┬──────────┘            └─────────┬──────────┘            └─────────┬──────────┘            └─────────┬──────────┘   │
│             │                                 │                                 │                                 │              │
│      ①      ▼          Electrical / Gas       ②      ▼          Status & SMP           ③      ▼          Duty Verification     ④      ▼   │
│   [MINER] ──────▶  [Hazard Detected]  ──▶  [TECH]  ──────▶  [SMP Cleared]   ──▶ [SUPVR] ──────▶ [Shift Handover] ──▶ [MGMT]     │
│             │                                 │                                 │                                 │              │
│   ┌─────────┴──────────┐            ┌─────────┴──────────┐            ┌─────────┴──────────┐            ┌─────────┴──────────┐   │
│   │ • Less Fatigue     │            │ • Sub-800ms Trip   │            │ • Digital Audits   │            │ • RUL Analytics    │   │
│   │ • Task Focus       │            │ • Situational IoT  │            │ • WAL Blackbox     │            │ • Zero Downtime    │   │
│   │ • Hands-free SOS   │            │ • SMP Compliance   │            │ • Continuous Safe  │            │ • Enterprise Scale │   │
│   │ • Safe Evacuation  │            │ • Fast Dispatch    │            │ • Prevents Cave-in │            │ • Capex Protection │   │
│   └────────────────────┘            └────────────────────┘            └────────────────────┘            └────────────────────┘   │
│                                                                                                                                  │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 🏛️ GOVERNMENT & REGULATORY BODIES (DGMS, NDMA, Ministry of Mines, PESO)                                                  │   │
│   │ • Real-time un-falsifiable edge blackbox logs directly mapping to DGMS statutory mining safety norms.                    │   │
│   │ • Targeted cross-industry data analytics supporting proactive national safety policy & early warning protocols.          │   │
│   └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 SLIDE CONTENT (EXACT POWERPOINT COPY)

### 🏷️ Header
* **Main Title:** `STAKEHOLDERS & IMPACTS`
* **Badge / Context:** `Tata Steel Mines & Smelters • High-Consequence Hazard Containment`

---

### ① Stakeholder 1: MINE OPERATOR (*Underground Miner / Field Crew)
* **Top AI / System Callout:**
  > *"The operator reports the hazard through smart hands-free voice controls or rugged wearable SOS badge."*
* **Trigger Action:**
  > **Electrical / Gas Hazard Detected**  
  > *Notices an exposed live 415V cable or methane ($CH_4$) / carbon monoxide ($CO$) seepage; logged into local Sentinel-X edge terminal.*
* **Quantifiable Impacts:**
  * 🧠 **Reduced Cognitive Fatigue & Laser-Sharp Task Focus** (No manual paper logbooks or delayed telephone switchboards).
  * 🛡️ **Enhanced Life Safety & Instant Hands-Free SOS** (Dynamic 3D evacuation route avoids walking into toxic gas plumes).

---

### ② Stakeholder 2: MINE OPERATOR (*Technician / Rapid Responder)
* **Top AI / System Callout:**
  > *"The Edge Brain AI verifies the anomaly in <800ms and autonomously dispatches the nearest response crew."*
* **Trigger Action:**
  > **Issue Status & SMP Checklist**  
  > *Executes local hardware trip, isolates contactor, and completes digital Safety Management Plan (SMP) checklist on rugged field tablet.*
* **Quantifiable Impacts:**
  * ⚡ **Deterministic Sub-800ms Safety Interlock** (Local optocoupled relay trips before combustible gas ignites).
  * 📑 **Auditable SMP Digital Checklist & Real-Time IoT Awareness** (Clear task documentation, zero missing steps, optimal resource dispatch).

---

### ③ Stakeholder 3: MINE SUPERVISOR (*Safety Officer / Shift Controller)
* **Top AI / System Callout:**
  > *"The 3D Digital Twin cross-validates field repair work against real-time multi-sensor telemetry using the AI trust engine."*
* **Trigger Action:**
  > **Duty Verification & Smooth Shift Handover**  
  > *Verifies physical sensor readings returned to baseline ($<25^\circ\text{C}$, $0\text{ ppm}$ gas) and signs digital shift handover.*
* **Quantifiable Impacts:**
  * 🔍 **Simplified Digital Audits with Real-Time Zero-Tamper Logs** (SQLite Write-Ahead Log records every action with millisecond timestamps).
  * ⚠️ **Proactive Anomaly Prevention** (Continuous spatial monitoring stops minor electrical faults from escalating into mine-wide explosions).

---

### ④ Stakeholder 4: MINE MANAGEMENT (*Tata Steel GM Operations & Plant Leadership)
* **Top AI / System Callout:**
  > *"Enterprise ERP / SAP integration enhances multi-mine operational visibility and centralized disaster records."*
* **Trigger Action:**
  > **Data Utilization & Predictive ROI**  
  > *Leverages TinyML Remaining Useful Life (RUL) and hazard heatmaps for condition-based maintenance and CAPEX planning.*
* **Quantifiable Impacts:**
  * 📈 **Zero Unplanned Outages & Massive CAPEX Savings** (Eliminates ₹50Cr+ production halts from catastrophic smelter or ventilation failures).
  * 📊 **Enterprise-Wide Regulatory Compliance** (Consolidated multi-site safety scorecards and incident replay capability).

---

### 🏛️ Regulatory Column: GOVERNMENT & REGULATORY BODIES
*(DGMS - Directorate General of Mines Safety, NDMA, Ministry of Mines, PESO, State Pollution Control Boards)*
* 🛰️ **Real-Time Data Oversight & Compliance Monitoring:**  
  *Un-falsifiable edge-stamped telemetry logs ensure complete transparency without relying on delayed self-reporting.*
* 📜 **Targeted Regulatory Policymaking & National Safety Benchmarking:**  
  *Aggregated cross-industry hazard trend data enables the formulation of proactive mining safety codes and automated disaster warning protocols.*

---

## 🎤 SPEAKER SCRIPT (60 SECONDS FOR SIH JURY)

> *"Respected Judges, disaster management succeeds or fails on how seamlessly technology empowers every human stakeholder in the operational chain."*
>
> *"In our Tata Steel scenario, when an underground miner detects an electrical spark or gas leak, they don’t waste crucial minutes on phone calls—they trigger an instant hands-free voice or SOS alert. Within 800 milliseconds, our Sentinel-X edge engine validates the reading, trips the local 415V breaker to prevent an explosion, and routes the nearest technician with safe 3D coordinates."*
>
> *"The technician clears the digital SMP checklist on a tablet, which the Shift Supervisor cross-validates against live 3D sensor telemetry before authorizing a safe shift handover. Finally, all incident events sync seamlessly into Tata Steel's enterprise SAP ERP and provide DGMS inspectors with unalterable cryptographic blackbox logs."*
>
> *"This transforms mine safety from reactive post-disaster finger-pointing into a proactive, closed-loop life-safety ecosystem."*

---

## 🚀 HOW TO INSERT INTO YOUR POWERPOINT DECK

### Method 1: Using the Interactive 4K Exporter (Recommended)
1. Double-click [`stakeholders-impacts.html`](file:///e:/tata%20updated/tata/stakeholders-impacts.html) in Windows Explorer to open it in your browser (Chrome/Edge).
2. Click the blue button **"📸 Export High-Res PNG (For PPT)"**.
3. It will immediately download a crisp **3840×1450 (4K resolution)** image (`SENTINEL_X_STAKEHOLDERS_IMPACTS_MINES.png`).
4. Drag and drop this PNG onto **Slide 5** of your PowerPoint template!

### Method 2: Direct Vector SVG (Infinite Crispness)
1. Open your PowerPoint (`.pptx`) file.
2. Select **Insert ➔ Pictures ➔ This Device**.
3. Select [`docs/STAKEHOLDERS_AND_IMPACTS.svg`](file:///e:/tata%20updated/tata/docs/STAKEHOLDERS_AND_IMPACTS.svg).
4. *Tip:* In PowerPoint, you can right-click the SVG and choose **"Convert to Shape"** to customize colors or fonts directly inside PowerPoint!

### Method 3: Copy Text Directly
1. In the HTML tool, click **"📋 PPT Slide Copy & Notes"** and then **"📋 Copy All Text"**.
2. Paste directly into your PowerPoint slide text boxes and speaker notes.
