"""
Sentinel-X Communication: MQTT Adapter
======================================
Interface for ingesting telemetry from distributed ESP32-S3 sensor nodes
and publishing local safety events over MQTT.
Gracefully operates with paho-mqtt when installed, or simulated loopback mode when running standalone.
"""

import json
import time
from typing import Dict, Any, Callable, Optional, List
from pydantic import BaseModel

class MQTTMessage(BaseModel):
    topic: str
    payload: Dict[str, Any]
    timestamp: float = 0.0
    qos: int = 1

class MQTTAdapter:
    def __init__(self, broker: str = "localhost", port: int = 1883, client_id: str = "sentinel-rpi5-gw"):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.connected = False
        self._subscriptions: Dict[str, List[Callable]] = {}
        self._sent_messages: List[MQTTMessage] = []
        self._client = None
        self._init_client()

    def _init_client(self):
        try:
            import paho.mqtt.client as mqtt
            self._client = mqtt.Client(client_id=self.client_id)
            self._client.on_connect = self._on_connect
            self._client.on_message = self._on_message
        except ImportError:
            # Fallback simulator mode when running in lightweight test environments
            self._client = None
            self.connected = True

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            for topic in self._subscriptions:
                self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            callbacks = self._subscriptions.get(msg.topic, [])
            for cb in callbacks:
                cb(msg.topic, payload)
        except Exception:
            pass

    def connect(self) -> bool:
        if self._client:
            try:
                self._client.connect_async(self.broker, self.port, 60)
                self._client.loop_start()
                self.connected = True
                return True
            except Exception:
                self.connected = False
                return False
        else:
            self.connected = True
            return True

    def disconnect(self):
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
        self.connected = False

    def subscribe(self, topic: str, callback: Callable[[str, Dict[str, Any]], None]):
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(callback)
        if self._client and self.connected:
            self._client.subscribe(topic)

    def publish(self, topic: str, payload: Dict[str, Any], qos: int = 1) -> bool:
        msg = MQTTMessage(topic=topic, payload=payload, timestamp=time.time(), qos=qos)
        self._sent_messages.append(msg)
        if len(self._sent_messages) > 100:
            self._sent_messages.pop(0)

        if self._client and self.connected:
            try:
                self._client.publish(topic, json.dumps(payload), qos=qos)
                return True
            except Exception:
                return False
        return True

    def get_recent_messages(self) -> List[MQTTMessage]:
        return self._sent_messages[-20:]

mqtt_adapter = MQTTAdapter()
