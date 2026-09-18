#!/bin/bash
# Sentinel-X One-Command Start Script
set -e

echo "Starting Sentinel-X Edge Services..."
sudo systemctl start mosquitto
sudo systemctl start sentinel-backend
sudo systemctl start sentinel-frontend

echo "[✓] Sentinel-X Services Started."
echo "Dashboard: http://localhost:3000"
