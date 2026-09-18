#!/bin/bash
# Sentinel-X Service Update Script
set -e
echo "Updating Sentinel-X Package..."
git pull origin main 2>/dev/null || true
if [ -d "venv" ]; then
    ./venv/bin/pip install -r backend/requirements.txt
fi
sudo systemctl restart sentinel-backend
sudo systemctl restart sentinel-frontend
echo "[✓] Sentinel-X Updated & Restarted."
