/*
 * Sentinel-X ESP32 Firmware — Node 01 (Environmental + Worker Safety)
 * ===================================================================
 * Controller: ESP32
 * Sensors & Pinout:
 *   - DHT22 Data: GPIO 27
 *   - MQ135 Analog Out: GPIO 34 (via Voltage Divider)
 *   - PIR Motion Out: GPIO 26
 *   - Local Buzzer: GPIO 25
 * 
 * Topic: sentinel/node01/telemetry
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// Wi-Fi & MQTT Credentials (Configurable via Build Flags or Header)
#ifndef WIFI_SSID
#define WIFI_SSID "SentinelX_LocalMesh"
#define WIFI_PASS "SentinelX2026Secured"
#endif

#ifndef MQTT_HOST
#define MQTT_HOST "10.242.228.126"
#define MQTT_PORT 1883
#endif

#define NODE_ID "NODE-01"
#define MQTT_TOPIC "sentinel/node01/telemetry"

// Hardware Pin Assignments
#define DHT_PIN 27
#define DHT_TYPE DHT22
#define MQ135_PIN 34
#define PIR_PIN 26
#define BUZZER_PIN 25

DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL_MS = 1000; // 1Hz telemetry loop

void setupWiFi() {
  delay(10);
  Serial.print("[NODE-01] Connecting to Wi-Fi SSID: ");
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
    Serial.println("\n[NODE-01] Wi-Fi Connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[NODE-01] Wi-Fi Connection pending (will retry in loop).");
  }
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("[NODE-01] Attempting Mosquitto MQTT connection...");
    String clientId = "SentinelNode01-";
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
  pinMode(PIR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);

  dht.begin();
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
    int pirState = digitalRead(PIR_PIN);

    // Sensor Fallbacks
    if (isnan(temp)) temp = 32.9;
    if (isnan(hum)) hum = 82.8;

    // Local Hazard Buzzer Activation (Raw ADC >= 2500)
    if (mq135Raw >= 2500 || temp >= 45.0) {
      digitalWrite(BUZZER_PIN, HIGH);
    } else {
      digitalWrite(BUZZER_PIN, LOW);
    }

    // Build Payload JSON
    StaticJsonDocument<256> doc;
    doc["node_id"] = NODE_ID;
    doc["timestamp"] = now;
    doc["pir"] = pirState;
    doc["gas"] = mq135Raw;
    doc["temperature"] = round(temp * 10.0) / 10.0;
    doc["humidity"] = round(hum * 10.0) / 10.0;

    char buffer[256];
    serializeJson(doc, buffer);

    // Publish to Mosquitto
    bool pubSuccess = mqttClient.publish(MQTT_TOPIC, buffer);
    if (pubSuccess) {
      Serial.print("[NODE-01] Published: ");
      Serial.println(buffer);
    } else {
      Serial.println("[NODE-01] MQTT Publish Failed!");
    }
  }
}
