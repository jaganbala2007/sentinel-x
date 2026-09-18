#!/bin/bash
# ==============================================================================
# Sentinel-X Automatic Kiosk Browser Launcher for Raspberry Pi Display
# ==============================================================================

echo "[Sentinel-X] Waiting for web server to become ready on http://localhost:3000..."

# Wait up to 30 seconds for web dashboard to respond
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null; then
        echo "[Sentinel-X] Web dashboard is ONLINE!"
        break
    fi
    sleep 2
done

# Disable screen blanking & power saving
if command -v xset &> /dev/null; then
    xset s off 2>/dev/null || true
    xset -dpms 2>/dev/null || true
    xset s noblank 2>/dev/null || true
fi

# Detect and launch Chromium in full-screen Kiosk mode
DASHBOARD_URL="http://localhost:3000/app.html?demo=1"

if command -v chromium-browser &> /dev/null; then
    echo "[Sentinel-X] Launching Chromium in Kiosk mode..."
    chromium-browser --noerrdialogs --disable-infobars --kiosk --incognito "$DASHBOARD_URL" &
elif command -v chromium &> /dev/null; then
    echo "[Sentinel-X] Launching Chromium in Kiosk mode..."
    chromium --noerrdialogs --disable-infobars --kiosk --incognito "$DASHBOARD_URL" &
else
    echo "[Sentinel-X] Chromium not found. Attempting default browser..."
    xdg-open "$DASHBOARD_URL" &
fi
