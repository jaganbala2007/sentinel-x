#!/bin/bash
# ==============================================================================
# Sentinel-X Diagnostic Status Script
# ==============================================================================
echo "======================================================================"
echo "          SENTINEL-X EDGE DIAGNOSTICS & HARDWARE STATUS               "
echo "======================================================================"

echo -n "Mosquitto MQTT (1883): "
systemctl is-active mosquitto 2>/dev/null || echo "INACTIVE"

echo -n "Sentinel Backend (8000): "
systemctl is-active sentinel-backend 2>/dev/null || (pgrep -f "uvicorn" >/dev/null && echo "ACTIVE (standalone)" || echo "INACTIVE")

echo -n "Sentinel Frontend (3000): "
systemctl is-active sentinel-frontend 2>/dev/null || (pgrep -f "node.*server.js" >/dev/null && echo "ACTIVE (standalone)" || echo "INACTIVE")

echo "----------------------------------------------------------------------"
echo "Authoritative State Check (curl http://127.0.0.1:8000/api/v1/twin/state):"
curl -s --connect-timeout 2 http://127.0.0.1:8000/api/v1/twin/state | python3 -m json.tool 2>/dev/null || curl -s --connect-timeout 2 http://127.0.0.1:8000/api/v1/twin/state || echo "[!] Backend not responding."
echo ""
echo "======================================================================"
