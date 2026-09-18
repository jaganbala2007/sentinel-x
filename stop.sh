#!/bin/bash
# Sentinel-X One-Command Stop Script
set -e

echo "Stopping Sentinel-X Edge Services..."
sudo systemctl stop sentinel-frontend || true
sudo systemctl stop sentinel-backend || true

echo "[✓] Sentinel-X Services Stopped Safely."
