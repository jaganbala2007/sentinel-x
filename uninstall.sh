#!/bin/bash
# Sentinel-X Service Uninstaller Script
echo "Uninstalling Sentinel-X Services..."
sudo systemctl stop sentinel-frontend || true
sudo systemctl stop sentinel-backend || true
sudo systemctl disable sentinel-frontend || true
sudo systemctl disable sentinel-backend || true
sudo rm -f /etc/systemd/system/sentinel-backend.service
sudo rm -f /etc/systemd/system/sentinel-frontend.service
sudo systemctl daemon-reload
echo "[✓] Sentinel-X Services Removed."
