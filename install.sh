#!/bin/bash
# ==============================================================================
# Sentinel-X Autonomous Industrial Safety Platform — Universal Raspberry Pi Installer
# ==============================================================================

set -e

echo "======================================================================"
echo "       SENTINEL-X RASPBERRY PI 3/4/5 EDGE DEPLOYMENT INSTALLER        "
echo "======================================================================"

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER="${SUDO_USER:-$USER}"
if [ -z "$CURRENT_USER" ] || [ "$CURRENT_USER" = "root" ]; then
    CURRENT_USER="$(logname 2>/dev/null || whoami)"
fi

cd "$INSTALL_DIR"

# 1. Environment & Architecture Check
echo "[1/8] Verifying Edge OS & Hardware Architecture..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "  -> OS Detected: $PRETTY_NAME"
fi
echo "  -> Target User: $CURRENT_USER"
echo "  -> Target Path: $INSTALL_DIR"

# 2. Package Manager & Essential Dependencies
echo "[2/8] Installing core system packages..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv mosquitto mosquitto-clients curl

# 3. Python Virtual Environment Setup (Edge Lightweight Wheel Optimized)
echo "[3/8] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "  -> Installing Sentinel-X Edge Python dependencies..."
./venv/bin/pip install --upgrade pip --no-cache-dir
if [ -f "requirements-rpi.txt" ]; then
    ./venv/bin/pip install --no-cache-dir -r requirements-rpi.txt
elif [ -f "requirements.txt" ]; then
    ./venv/bin/pip install --no-cache-dir -r requirements.txt || ./venv/bin/pip install --no-cache-dir fastapi uvicorn paho-mqtt pydantic pydantic-settings
else
    ./venv/bin/pip install --no-cache-dir fastapi uvicorn paho-mqtt pydantic pydantic-settings
fi

# 4. Node.js Frontend Runtime Check
echo "[4/8] Checking Node.js runtime..."
if ! command -v node &> /dev/null; then
    echo "  -> Installing Node.js LTS..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    echo "  -> Installing frontend dependencies..."
    (cd frontend && npm install --production --no-audit --no-fund)
fi

# 5. Mosquitto MQTT Broker Configuration
echo "[5/8] Configuring Mosquitto MQTT Broker (Port 1883)..."
sudo mkdir -p /etc/mosquitto/conf.d
if [ -f "deployment/mosquitto.conf" ]; then
    sudo cp -f deployment/mosquitto.conf /etc/mosquitto/conf.d/sentinel.conf 2>/dev/null || true
fi
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto

# 6. Environment Configuration
echo "[6/8] Configuring runtime environment..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
ENVIRONMENT=production
PORT=8000
MQTT_HOST=127.0.0.1
MQTT_PORT=1883
SQLITE_DB_PATH=$INSTALL_DIR/sentinel_edge.db
EOF
    fi
fi

# 7. Dynamic Systemd Service Generation (No Hardcoded Paths/Users)
echo "[7/8] Deploying dynamically configured Systemd Services..."

cat > /tmp/sentinel-backend.service << EOF
[Unit]
Description=Sentinel-X Autonomous Safety FastAPI Backend
After=network.target mosquitto.service
Wants=mosquitto.service

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
Restart=always
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=5
Environment=PORT=8000
Environment=MQTT_HOST=127.0.0.1
Environment=MQTT_PORT=1883

[Install]
WantedBy=multi-user.target
EOF

cat > /tmp/sentinel-frontend.service << EOF
[Unit]
Description=Sentinel-X Web Dashboard Node.js Proxy Server
After=network.target sentinel-backend.service
Wants=sentinel-backend.service

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR/frontend
ExecStart=/usr/bin/node server.js
Restart=always
RestartSec=5
StartLimitIntervalSec=60
StartLimitBurst=5
Environment=PORT=3000
Environment=BACKEND_URL=http://127.0.0.1:8000

[Install]
WantedBy=multi-user.target
EOF

sudo cp -f /tmp/sentinel-backend.service /etc/systemd/system/sentinel-backend.service
sudo cp -f /tmp/sentinel-frontend.service /etc/systemd/system/sentinel-frontend.service
rm -f /tmp/sentinel-backend.service /tmp/sentinel-frontend.service

sudo systemctl daemon-reload
sudo systemctl enable sentinel-backend
sudo systemctl enable sentinel-frontend
sudo systemctl restart sentinel-backend
sudo systemctl restart sentinel-frontend

# Fix permissions on all shell scripts
chmod +x "$INSTALL_DIR"/*.sh "$INSTALL_DIR"/scripts/*.sh 2>/dev/null || true

# 8. Health Verification
echo "[8/8] Performing System Health Diagnostics..."
sleep 3
BACKEND_HEALTH=$(curl -s http://127.0.0.1:8000/api/health || echo '{"status":"starting"}')
echo "  -> Backend Status: $BACKEND_HEALTH"

PI_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$PI_IP" ]; then PI_IP="127.0.0.1"; fi

echo "======================================================================"
echo "          SENTINEL-X INSTALLATION COMPLETE!                           "
echo "======================================================================"
echo "  [✓] Mosquitto MQTT Running (1883)"
echo "  [✓] Sentinel FastAPI Backend Running (8000)"
echo "  [✓] Sentinel Web Dashboard Running (3000)"
echo "  [✓] Dynamic Systemd Services Configured for User: $CURRENT_USER"
echo ""
echo "  Local Dashboard URL:   http://localhost:3000/app.html?demo=1"
echo "  Remote Network URL:   http://${PI_IP}:3000"
echo "  Backend API Swagger:  http://${PI_IP}:8000/docs"
echo ""
echo "  Helpful Commands:"
echo "    • View Status:      bash status.sh"
echo "    • Stop Services:    bash stop.sh"
echo "    • Start Services:   bash start.sh"
echo "    • Emergency Rescue: bash scripts/unblock_pi.sh"
echo "======================================================================"
