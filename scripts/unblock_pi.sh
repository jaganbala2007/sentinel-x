#!/bin/bash
# ==============================================================================
# Sentinel-X Emergency Raspberry Pi Unblock & Rescue Tool
# ==============================================================================
# Use this script if:
#   1. Chromium full-screen Kiosk mode is blocking the desktop/terminal
#   2. Systemd services are stuck in a restart loop causing high CPU
#   3. You need to instantly regain full control of the Raspberry Pi OS
# ==============================================================================

echo "======================================================================"
echo "          SENTINEL-X EMERGENCY RASPBERRY PI UNBLOCK TOOL              "
echo "======================================================================"

# 1. Kill any blocking browser instances
echo "[1/4] Closing full-screen Kiosk browsers..."
killall chromium-browser chromium chrome firefox 2>/dev/null || true

# 2. Stop all Sentinel-X background systemd services
echo "[2/4] Stopping background edge services..."
sudo systemctl stop sentinel-frontend 2>/dev/null || true
sudo systemctl stop sentinel-backend 2>/dev/null || true

# 3. Disable autostart entries to prevent automatic locking on reboot
echo "[3/4] Removing automatic kiosk startup hooks..."
rm -f "$HOME/.config/autostart/sentinel-kiosk.desktop" 2>/dev/null || true
if [ -f "$HOME/.config/lxsession/LXDE-pi/autostart" ]; then
    sed -i '/launch_kiosk.sh/d' "$HOME/.config/lxsession/LXDE-pi/autostart" 2>/dev/null || true
fi
if [ -f "$HOME/.config/wayfire.ini" ]; then
    sed -i '/sentinel_kiosk/d' "$HOME/.config/wayfire.ini" 2>/dev/null || true
fi

# 4. Clean up zombie python/node processes
echo "[4/4] Cleaning zombie processes and freeing memory..."
killall -9 uvicorn 2>/dev/null || true
pkill -f "python3.*app.main" 2>/dev/null || true
pkill -f "node.*server.js" 2>/dev/null || true

echo "======================================================================"
echo "  [✓] RASPBERRY PI OS UNBLOCKED & RESTORED TO NORMAL!                 "
echo "======================================================================"
echo "  • Desktop and terminal are completely free."
echo "  • Kiosk autostart disabled."
echo "  • Memory and CPU freed."
echo "======================================================================"
