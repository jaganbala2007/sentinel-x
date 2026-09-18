# ESP32 NODE 02 — MACHINE HEALTH & VIBRATION MONITORING

## Controller & Role
- **Microcontroller:** ESP32 Dev Module (WROOM-32)
- **Node Identifier:** `NODE-02`
- **Role:** Industrial machine motor diagnostics, current consumption, 3-axis vibration, acoustics, and machine temperature.

---

## Authoritative Pinout
| Sensor / Output | Pin on ESP32 | Protocol / Signal Type | Description |
| :--- | :--- | :--- | :--- |
| **DHT22 DATA** | `GPIO 27` | Single-Bus Digital | Machine Surface Ambient Temp (°C) & Humidity (%) |
| **MQ-135 AO** | `GPIO 34` | Analog (ADC1_CH6) | Machine ambient gas/smoke ADC |
| **Sound Sensor AO**| `GPIO 32` | Analog (ADC1_CH4) | Acoustic noise levels |
| **ACS712 30A AO** | `GPIO 35` | Analog (ADC1_CH7) | AC/DC Motor Current consumption |
| **ADXL345 SDA** | `GPIO 21` | I2C Data | 3-Axis Precision Acceleration & Vibration |
| **ADXL345 SCL** | `GPIO 22` | I2C Clock | I2C Clock Line |
| **Status Indicator**| *Unassigned* | N/A | *Indicator integration pending GPIO confirmation* |

---

## MQTT Telemetry Topic & Payload
- **Topic:** `sentinel/node02/telemetry`
- **Rate:** 1 Hz (1000 ms non-blocking timer)

```json
{
  "node_id": "NODE-02",
  "timestamp": 356447,
  "gas": 374,
  "temperature": 32.7,
  "humidity": 80.2,
  "current": -0.66,
  "vibration": 2.16,
  "sound": 336
}
```

---

## Flashing Instructions
1. Open `firmware/node02/node02_esp32.ino`.
2. Required Libraries: `PubSubClient`, `DHT sensor library`, `Wire`, `Adafruit ADXL345`, `Adafruit Unified Sensor`, `ArduinoJson`.
3. Configure `WIFI_SSID`, `WIFI_PASS`, `MQTT_HOST`, `MQTT_PORT`.
4. Upload to ESP32 Dev Module and verify Serial Output.
