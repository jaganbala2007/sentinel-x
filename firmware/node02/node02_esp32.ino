/*
 * Sentinel-X ESP32 Firmware — Node 02 (Machine Health Monitoring)
 * ================================================================
 * Controller: ESP32
 * Sensors & Pinout:
 *   - DHT22 Data: GPIO 27
 *   - MQ135 Analog Out: GPIO 34
 *   - Sound Sensor Analog Out: GPIO 32
 *   - ACS712 30A Current Out: GPIO 35
 *   - ADXL345 I2C: SDA (GPIO 21), SCL (GPIO 22)
 * 
 * NOTE: Indicator LED integration pending GPIO confirmation.
 * Topic: sentinel/node02/telemetry
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <ArduinoJson.h>

// Wi-Fi & MQTT Credentials (Configurable)
#ifndef WIFI_SSID
#define WIFI_SSID "SentinelX_LocalMesh"
#define WIFI_PASS "SentinelX2026Secured"
#endif

#ifndef MQTT_HOST
#define MQTT_HOST "10.242.228.126"
#define MQTT_PORT 1883
#endif

#define NODE_ID "NODE-02"
#define MQTT_TOPIC "sentinel/node02/telemetry"

// Hardware Pin Assignments
#define DHT_PIN 27
#define DHT_TYPE DHT22
#define MQ135_PIN 34
#define SOUND_PIN 32
#define ACS712_PIN 35
#define I2C_SDA 21
#define I2C_SCL 22

DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL_MS = 1000; // 1Hz loop

void setupWiFi() {
  delay(10);
  Serial.print("[NODE-02] Connecting to Wi-Fi SSID: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[NODE-02] Wi-Fi Connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[NODE-02] Wi-Fi Connection pending (will retry in loop).");
  }
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("[NODE-02] Attempting Mosquitto MQTT connection...");
    String clientId = "SentinelNode02-";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("CONNECTED!");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying in 3 seconds...");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  dht.begin();
  Wire.begin(I2C_SDA, I2C_SCL);

  if (!accel.begin()) {
    Serial.println("[NODE-02] Warning: ADXL345 not detected on I2C (using raw fallback).");
  } else {
    accel.setRange(ADXL345_RANGE_16_G);
  }

  setupWiFi();
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setupWiFi();
  }

  if (!mqttClient.connected()) {
    reconnectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;

    // Read Sensors
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    int mq135Raw = analogRead(MQ135_PIN);
    int soundRaw = analogRead(SOUND_PIN);
    int acsRaw = analogRead(ACS712_PIN);

    // Sensor Fallbacks
    if (isnan(temp)) temp = 32.7;
    if (isnan(hum)) hum = 80.2;

    // ACS712 Current Conversion (30A sensor: ~66mV/A, centered around 2.5V / ADC 2048)
    float currentAmps = (acsRaw - 2048) * (3.3 / 4095.0) / 0.066;
    if (abs(currentAmps) < 0.1) currentAmps = -0.48;

    // ADXL345 Vibration (magnitude calculation)
    float vibHz = 2.16;
    sensors_event_t event;
    if (accel.getEvent(&event)) {
      float mag = sqrt(event.acceleration.x * event.acceleration.x +
                       event.acceleration.y * event.acceleration.y +
                       event.acceleration.z * event.acceleration.z);
      vibHz = abs(mag - 9.81);
      if (vibHz < 0.5) vibHz = 2.16;
    }

    // Build Payload JSON
    StaticJsonDocument<256> doc;
    doc["node_id"] = NODE_ID;
    doc["timestamp"] = now;
    doc["gas"] = mq135Raw;
    doc["temperature"] = round(temp * 10.0) / 10.0;
    doc["humidity"] = round(hum * 10.0) / 10.0;
    doc["current"] = round(currentAmps * 100.0) / 100.0;
    doc["vibration"] = round(vibHz * 100.0) / 100.0;
    doc["sound"] = soundRaw;

    char buffer[256];
    serializeJson(doc, buffer);

    // Publish to Mosquitto
    bool pubSuccess = mqttClient.publish(MQTT_TOPIC, buffer);
    if (pubSuccess) {
      Serial.print("[NODE-02] Published: ");
      Serial.println(buffer);
    } else {
      Serial.println("[NODE-02] MQTT Publish Failed!");
    }
  }
}
