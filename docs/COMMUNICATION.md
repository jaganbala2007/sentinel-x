# Sentinel-X Communication Resilience Subsystem

**Protocol Hierarchy:** Broadband Internet $\rightarrow$ HF Packet Radio (AX.25) $\rightarrow$ Satellite IoT $\rightarrow$ Store-and-Forward  

---

## 1. Multi-Tier Backhaul Hierarchy

```
[ESP32-S3 SENSORS] ──► [RPI 5 EDGE GATEWAY]
                             │
       ┌─────────────────────┼─────────────────────┐
       │ (Priority 1)        │ (Priority 2)        │ (Priority 3)
       ▼                     ▼                     ▼
[BROADBAND / LTE]    [HF PACKET RADIO]      [SATELLITE IoT]
 • TLS 1.3 / MQTT     • 7.105 MHz (40m)     • Iridium SBD
 • High Bandwidth     • AX.25 / FX.25       • 340-Byte Burst
 • 28 ms Latency      • Ionospheric NVIS    • LEO Uplink
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                             ▼ (If ALL links fail)
                 ┌───────────────────────┐
                 │ AUTONOMOUS BLACKOUT   │
                 │ • SQLite Flash WAL    │
                 │ • Local Sirens Active │
                 │ • Sync on Return      │
                 └───────────────────────┘
```

---

## 2. Why HF Packet Radio (7.105 MHz AX.25) Instead of LoRa?

| Dimension | LoRa / LoRaWAN (868 / 915 MHz) | HF Packet Radio (7.105 MHz AX.25) |
| :--- | :--- | :--- |
| **Propagation Mode** | Line-of-Sight (UHF Groundwave) | Near-Vertical Incidence Skywave (NVIS) |
| **Mountain Terrain Blockage**| High (Signals blocked by ridges & valleys)| Zero (Signals reflect off ionosphere downward) |
| **Rain & Cloudburst Fade** | Moderate-to-Severe attenuation | Completely unaffected by atmospheric rain |
| **Effective Range** | 2–10 km in rough terrain | **500 km radius blanket coverage** |
| **Infrastructure Reliance**| Requires local gateway towers on ridges | **Zero telecommunications infrastructure** |

---

## 3. Compact Packet Serialization Format

To guarantee transmission reliability over low-bandwidth emergency links (1200 Baud AFSK and Satellite SBD), telemetry is formatted into a **24-byte compact binary frame**:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Magic: 'S'  |   Magic: 'X'  | Version: 0x02 | Node Number   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Sequence Number                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Timestamp (Seconds)                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|      Water Level (cm)         |   Rate of Rise (mm / min)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Baro Pressure (daPa)      | Soil Sat (%)  |  Battery (%)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Safety State  | Confidence (%)|         CRC-16-CCITT          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
Total Frame Size: **24 Bytes**.  
At 1200 Baud, total transmission time is under **160 milliseconds**.
