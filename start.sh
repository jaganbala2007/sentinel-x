#!/bin/bash
# ==============================================================================
# Sentinel-X One-Command Start Script
# ==============================================================================

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "======================================================================"
echo "          STARTING SENTINEL-X EDGE PLATFORM SERVICES                  "
echo "======================================================================"

# 1. Start Mosquitto Broker
sudo systemctl start mosquitto 2>/dev/null || true

# 2. Start Backend & Frontend via Systemd if configured
if systemctl is-enabled sentinel-backend &>/dev/null; then
    sudo systemctl start sentinel-backend
    sudo systemctl start sentinel-frontend
    echo "[✓] Systemd services started."
else
    echo "[*] Systemd not configured yet. Starting in background..."
    if [ -f "venv/bin/uvicorn" ]; then
        nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend > logs/backend.log 2>&1 &
    fi
    if [ -d "frontend" ]; then
        (cd frontend && nohup node server.js > ../logs/frontend.log 2>&1 &)
    fi
    echo "[✓] Background processes started."
fi

PI_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$PI_IP" ]; then PI_IP="127.0.0.1"; fi

echo "======================================================================"
echo "  [✓] SENTINEL-X IS ONLINE"
echo "  • Local Dashboard:  http://localhost:3000/app.html?demo=1"
echo "  • Network URL:      http://${PI_IP}:3000"
echo "  • API Docs:         http://${PI_IP}:8000/docs"
echo "======================================================================"
