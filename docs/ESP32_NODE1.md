# ESP32 NODE 01 — ENVIRONMENTAL & WORKER SAFETY

## Controller & Role
- **Microcontroller:** ESP32 Dev Module (WROOM-32)
- **Node Identifier:** `NODE-01`
- **Role:** Environmental atmosphere tracking, worker presence detection, and local hazard buzzer.

---

## Authoritative Pinout
| Sensor / Output | Pin on ESP32 | Protocol / Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **DHT22 DATA** | `GPIO 27` | Single-Bus Digital | Ambient Temperature (°C) & Relative Humidity (%) |
| **MQ-135 AO** | `GPIO 34` | Analog (ADC1_CH6) | Hazardous gas / air quality raw ADC (via 5V $\to$ 3.3V voltage divider) |
| **PIR OUT** | `GPIO 26` | Digital In | Worker motion / presence (0: No Motion, 1: Motion Detected) |
| **Buzzer** | `GPIO 25` | Digital Out | Local piezo hazard alert (Active HIGH on critical hazard) |

---

## MQTT Telemetry Topic & Payload
- **Topic:** `sentinel/node01/telemetry`
- **Rate:** 1 Hz (1000 ms non-blocking timer)

```json
{
  "node_id": "NODE-01",
  "timestamp": 214346,
  "pir": 0,
  "gas": 420,
  "temperature": 32.9,
  "humidity": 82.8
}
```

---

## Flashing Instructions (Arduino IDE / PlatformIO)
1. Open `firmware/node01/node01_esp32.ino`.
2. Required Libraries: `PubSubClient`, `DHT sensor library`, `ArduinoJson`.
3. Configure `WIFI_SSID`, `WIFI_PASS`, `MQTT_HOST` (e.g. `10.242.228.126`), `MQTT_PORT` (`1883`).
4. Select Board: `ESP32 Dev Module`, Flash Speed: `921600`.
5. Upload and open Serial Monitor at `115200 baud`.
