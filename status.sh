#!/bin/bash
# Sentinel-X Diagnostic Status Script
echo "======================================================================"
echo "          SENTINEL-X EDGE DIAGNOSTICS & HARDWARE STATUS               "
echo "======================================================================"

echo -n "Mosquitto MQTT (1883): "
systemctl is-active mosquitto || echo "INACTIVE"

echo -n "Sentinel Backend (8000): "
systemctl is-active sentinel-backend || echo "INACTIVE"

echo -n "Sentinel Frontend (3000): "
systemctl is-active sentinel-frontend || echo "INACTIVE"

echo "----------------------------------------------------------------------"
echo "Authoritative State Check (curl http://127.0.0.1:8000/api/v1/twin/state):"
curl -s http://127.0.0.1:8000/api/v1/twin/state | python3 -m json.tool 2>/dev/null || curl -s http://127.0.0.1:8000/api/v1/twin/state
echo "======================================================================"
