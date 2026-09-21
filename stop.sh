#!/bin/bash
# ==============================================================================
# Sentinel-X One-Command Stop Script
# ==============================================================================

echo "Stopping Sentinel-X Edge Services..."
sudo systemctl stop sentinel-frontend 2>/dev/null || true
sudo systemctl stop sentinel-backend 2>/dev/null || true

# Kill any standalone processes if running outside systemd
pkill -f "uvicorn.*app.main:app" 2>/dev/null || true
pkill -f "node.*server.js" 2>/dev/null || true

echo "[✓] Sentinel-X Services Stopped Safely."
