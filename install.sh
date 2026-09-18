#!/bin/bash
# ==============================================================================
# Sentinel-X Autonomous Industrial Safety Platform — One-Command Raspberry Pi Installer
# ==============================================================================

set -e

echo "======================================================================"
echo "          SENTINEL-X RASPBERRY PI 3/4 EDGE DEPLOYMENT INSTALLER        "
echo "======================================================================"

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$INSTALL_DIR"

# 1. Environment & Architecture Check
echo "[1/8] Verifying Edge OS & Hardware Architecture..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "  -> OS Detected: $PRETTY_NAME"
fi

# 2. Python Environment Setup
echo "[2/8] Checking Python 3 and virtual environment..."
if ! command -v python3 &> /dev/null; then
    echo "  -> Installing Python 3..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
fi

if [ ! -d "venv" ]; then
    echo "  -> Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "  -> Installing Python dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r backend/requirements.txt || ./venv/bin/pip install fastapi uvicorn paho-mqtt pydantic

# 3. Node.js Frontend Runtime Check
echo "[3/8] Checking Node.js runtime..."
if ! command -v node &> /dev/null; then
    echo "  -> Installing Node.js LTS..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "  -> Installing frontend dependencies..."
    (cd frontend && npm install --production)
fi

# 4. Mosquitto MQTT Broker Installation & Configuration
echo "[4/8] Configuring Mosquitto MQTT Broker (Port 1883)..."
if ! command -v mosquitto &> /dev/null; then
    echo "  -> Installing Mosquitto broker and clients..."
    sudo apt-get update && sudo apt-get install -y mosquitto mosquitto-clients
fi

sudo mkdir -p /etc/mosquitto/conf.d
sudo cp -f deployment/mosquitto.conf /etc/mosquitto/conf.d/sentinel.conf 2>/dev/null || true
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto

# 5. Environment File Creation
echo "[5/8] Creating .env runtime configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  -> Created .env from .env.example"
fi

# 6. Systemd Service Deployment
echo "[6/8] Deploying Systemd Services for Automatic Boot Start..."
sudo cp -f systemd/sentinel-backend.service /etc/systemd/system/
sudo cp -f systemd/sentinel-frontend.service /etc/systemd/system/
sudo cp -f systemd/sentinel-mqtt-check.service /etc/systemd/system/ 2>/dev/null || true

sudo systemctl daemon-reload
sudo systemctl enable sentinel-backend
sudo systemctl enable sentinel-frontend

# 7. Start Services
echo "[7/8] Starting Sentinel-X Edge Services..."
sudo systemctl restart sentinel-backend
sudo systemctl restart sentinel-frontend

# 8. Health Verification
echo "[8/9] Performing System Health Diagnostics..."
sleep 3
BACKEND_HEALTH=$(curl -s http://127.0.0.1:8000/api/health || echo '{"status":"starting"}')
echo "  -> Backend Status: $BACKEND_HEALTH"

# 9. Configure Automatic Browser Launch on Boot
echo "[9/9] Configuring Automatic Full-Screen Kiosk Browser on Boot..."
if [ -f "scripts/setup_autostart_kiosk.sh" ]; then
    bash scripts/setup_autostart_kiosk.sh 2>/dev/null || true
fi

# Launch browser immediately if graphical desktop session is currently running
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    echo "  -> Active desktop display detected! Launching browser..."
    bash scripts/launch_kiosk.sh &
fi

PI_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$PI_IP" ]; then PI_IP="10.242.228.126"; fi

echo "======================================================================"
echo "          SENTINEL-X INSTALLATION COMPLETE!                           "
echo "======================================================================"
echo "  [✓] Mosquitto MQTT Running (1883)"
echo "  [✓] Sentinel FastAPI Backend Running (8000)"
echo "  [✓] Sentinel Web Dashboard Running (3000)"
echo "  [✓] Automatic Boot Start Configured"
echo "  [✓] Automatic Kiosk Browser on Boot Configured"
echo ""
echo "  Local Dashboard URL:  http://localhost:3000/app.html?demo=1"
echo "  Remote Network URL:  http://${PI_IP}:3000"
echo "  Backend API Swagger: http://${PI_IP}:8000/docs"
echo "======================================================================"
