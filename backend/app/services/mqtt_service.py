"""
Sentinel-X MQTT Ingestion Service
===================================
Listens to Mosquitto broker on 1883 for Node 1 and Node 2 combined & legacy telemetry.
Ingests JSON payloads directly into authorative twin_state_manager.
"""

import json
import logging
import threading
import time
import os
from typing import Optional

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

from app.services.twin_state_manager import twin_state_manager

logger = logging.getLogger("sentinel.mqtt")

class SentinelMQTTService:
    def __init__(self):
        self.host = os.environ.get("MQTT_HOST", "127.0.0.1")
        self.port = int(os.environ.get("MQTT_PORT", 1883))
        self.client = None
        self.connected = False
        self.worker_thread = None
        self.should_run = False

    def start(self):
        if mqtt is None:
            logger.warning("[MQTT] paho-mqtt module not installed. Falling back to background polling.")
            twin_state_manager.mqtt_status = "NOT_INSTALLED"
            return

        self.should_run = True
        self.worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self.worker_thread.start()

    def _run_loop(self):
        while self.should_run:
            try:
                self.client = mqtt.Client(client_id=f"sentinel-backend-{int(time.time())}")
                self.client.on_connect = self._on_connect
                self.client.on_disconnect = self._on_disconnect
                self.client.on_message = self._on_message
                
                logger.info(f"[MQTT] Connecting to Mosquitto broker at {self.host}:{self.port}...")
                self.client.connect(self.host, self.port, keepalive=60)
                self.client.loop_forever()
            except Exception as e:
                self.connected = False
                twin_state_manager.mqtt_status = "DISCONNECTED"
                logger.warning(f"[MQTT] Connection retry in 5s due to: {e}")
                time.sleep(5)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            twin_state_manager.mqtt_status = "CONNECTED"
            logger.info("[MQTT] Subscribed to production & legacy Sentinel telemetry topics.")
            # Subscribe to primary combined topics
            client.subscribe("sentinel/node01/telemetry")
            client.subscribe("sentinel/node02/telemetry")
            # Subscribe to legacy topics
            client.subscribe("sentinel/node1/#")
            client.subscribe("sentinel/node2/#")
        else:
            self.connected = False
            twin_state_manager.mqtt_status = f"ERROR_RC_{rc}"

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        twin_state_manager.mqtt_status = "DISCONNECTED"
        logger.warning(f"[MQTT] Disconnected from Mosquitto broker (rc={rc}).")

    def _on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            topic = msg.topic
            
            # Legacy topic handling
            if topic.startswith("sentinel/node1/") and not topic.endswith("/telemetry"):
                metric = topic.split("/")[-1]
                val = float(payload_str) if "." in payload_str else int(payload_str)
                twin_state_manager.update_node1({metric: val})
                return
            elif topic.startswith("sentinel/node2/") and not topic.endswith("/telemetry"):
                metric = topic.split("/")[-1]
                val = float(payload_str) if "." in payload_str else int(payload_str)
                twin_state_manager.update_node2({metric: val})
                return

            # Primary Combined Topics
            data = json.loads(payload_str)
            node_id = data.get("node_id", "").upper()
            
            if "NODE-01" in node_id or topic == "sentinel/node01/telemetry":
                twin_state_manager.update_node1(data)
            elif "NODE-02" in node_id or topic == "sentinel/node02/telemetry":
                twin_state_manager.update_node2(data)

        except Exception as e:
            logger.error(f"[MQTT] Error parsing payload on {msg.topic}: {e}")

    def stop(self):
        self.should_run = False
        if self.client:
            self.client.disconnect()

mqtt_service = SentinelMQTTService()
