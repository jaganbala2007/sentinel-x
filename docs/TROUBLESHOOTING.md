# SENTINEL-X FIELD TROUBLESHOOTING GUIDE

## 1. Quick Diagnostic Checklist
Run the diagnostic script on the Raspberry Pi:
```bash
./status.sh
```

---

## 2. MQTT Telemetry Verification
Check if Mosquitto is actively receiving telemetry from the ESP32 nodes:
```bash
# Subscribe to all Sentinel telemetry topics
mosquitto_sub -h 127.0.0.1 -p 1883 -t "sentinel/#" -v
```
Expected output:
```
sentinel/node01/telemetry {"node_id":"NODE-01","timestamp":214346,"pir":0,"gas":420,"temperature":32.9,"humidity":82.8}
sentinel/node02/telemetry {"node_id":"NODE-02","timestamp":356447,"gas":374,"temperature":32.7,"humidity":80.2,"current":-0.66,"vibration":2.16,"sound":336}
```

If no output appears:
- Verify ESP32 is connected to the same Wi-Fi subnet as the Raspberry Pi.
- Ping the Raspberry Pi from another machine on the LAN: `ping 10.242.228.126`.
- Verify Mosquitto is listening on all interfaces (`listener 1883 0.0.0.0` and `allow_anonymous true` in `/etc/mosquitto/conf.d/sentinel.conf`).

---

## 3. Backend Diagnostics
Verify FastAPI is healthy and serving authoritative digital twin state:
```bash
# Check health
curl -s http://127.0.0.1:8000/api/health

# Check state
curl -s http://127.0.0.1:8000/api/v1/twin/state | python3 -m json.tool
```

Inspect service logs:
```bash
journalctl -u sentinel-backend -n 50 -f
```

---

## 4. Web Dashboard Verification
Check frontend service:
```bash
journalctl -u sentinel-frontend -n 50 -f
```
Access dashboard in browser at `http://localhost:3000` or `http://10.242.228.126:3000`.

---

## 5. Systemd Service Restarts
```bash
# Restart everything
sudo systemctl restart mosquitto
sudo systemctl restart sentinel-backend
sudo systemctl restart sentinel-frontend
```
