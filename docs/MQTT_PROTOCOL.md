# Sentinel-X MQTT Protocol Specification

Broker: Mosquitto MQTT
Port: 1883

## Primary Combined Topics

### `sentinel/node01/telemetry`
Payload Schema:
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

### `sentinel/node02/telemetry`
Payload Schema:
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

## Legacy Topics Supported
- `sentinel/node1/temperature`
- `sentinel/node1/humidity`
- `sentinel/node1/gas`
- `sentinel/node1/pir`
- `sentinel/node2/temperature`
- `sentinel/node2/humidity`
- `sentinel/node2/gas`
- `sentinel/node2/sound`
- `sentinel/node2/vibration`
- `sentinel/node2/current`
