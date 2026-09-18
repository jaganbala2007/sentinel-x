# Sentinel-X 90-Second SIH Jury Demonstration Script

Follow this precise sequence to demonstrate Sentinel-X to the Smart India Hackathon jury.

---

### Step 1: Steady-State Overview (First 15 Seconds)
- **Action:** Open [http://localhost:8000/frontend/src/app.html](http://localhost:8000/frontend/src/app.html) on a high-contrast display.
- **Narrative:**  
  *"Respected Jury, Sentinel-X is designed around one harsh truth: during major natural disasters, the infrastructure used to detect the disaster is often the first thing destroyed.  
  Notice our SCADA status strip: 20 ESP32-S3 sensor nodes are active across Sector B watershed, communication is on primary broadband, and our composite disaster risk is at a calm 18%."*

---

### Step 2: Hero Moment 1 — Real Disaster Inundation Surge (20 Seconds)
- **Action:** Click `[⚡ SIH DEMO SUITE]` $\rightarrow$ Click `1. REAL DISASTER SURGE` (or press Hero 1 in the SIH Demo Mode tab).
- **Observed Change:**
  - Water elevation surges to $3.85\text{m}$ at $+0.08\text{m/min}$.
  - The critical red hazard strip slides down at the top.
  - Risk jumps to **84% (Critical)**, confidence reaches **94%**.
  - In the 3D Digital Twin, the river canyon water visibly rises.
  - XAI factor decomposition updates to show $+31$ water and $+24$ rate-of-rise.
- **Narrative:**  
  *"A rapid hydraulic surge has been detected. Three adjacent catchment sensors cross-corroborate the flood wave. The local acoustic siren has fired autonomously, and evacuation corridor Alpha is armed."*

---

### Step 3: Hero Moment 2 — False Sensor Spoofing & Quarantine (20 Seconds)
- **Action:** Click `2. SENSOR SPOOFING ATTACK`.
- **Observed Change:**
  - Node-03 suddenly reports an erratic $8.90\text{m}$ reading.
  - In the Sensor Trust table, Node-03's trust score drops live: $97\% \rightarrow 82\% \rightarrow 61\% \rightarrow 41\%$.
  - Node-03 turns amber and enters **QUARANTINED**.
  - The tactical map shows Node-03 isolated in amber.
  - Crucially: **The overall disaster risk does not panic or change.**
- **Narrative:**  
  *"Node-03 has either suffered electrical failure or a spoofing injection. Our Sensor Trust Engine evaluated kinematic rate-of-change and neighbor consensus. Trust degraded to 41% and the node was quarantined. The system continues relying exclusively on verified physical consensus."*

---

### Step 4: Hero Moment 3 — Internet Severed & HF Failover (15 Seconds)
- **Action:** Click `3. INTERNET SEVERED (HF FAILOVER)`.
- **Observed Change:**
  - Top status updates to `COMM: HF PACKET ACTIVE (7.105 MHz AX.25)`.
  - Internet status indicates `FAILED`.
  - The communication sniffer shows encoded AX.25 UI frames transmitting.
- **Narrative:**  
  *"The optical fiber backhaul has been severed by a landslide. In under 18 milliseconds, the Raspberry Pi 5 edge gateway actuated 7.105 MHz AX.25 HF Packet Radio, routing telemetry over amateur NVIS skywaves directly to the remote command center."*

---

### Step 5: Hero Moment 4 & 5 — Blackout Safety & Batch Sync (20 Seconds)
- **Action:** Click `4. TOTAL BLACKOUT` then `5. NETWORK RETURN & SYNC`.
- **Observed Change:**
  - Mode switches to `MODE 4: ISOLATED`.
  - Queue count increments to 17 events stored in local SQLite.
  - When Hero 5 is clicked, progress bar syncs `1/17 ... 17/17 (100% Synced)`.
- **Narrative:**  
  *"Even under total RF and cellular isolation, local sensing and sirens continue protecting the community. 17 events were stored in local SQLite flash memory. As soon as connectivity returned, the system executed an automated cryptographic handshake and synchronized every event without dropping a single byte."*
