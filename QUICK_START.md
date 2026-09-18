# SENTINEL-X QUICK START GUIDE

## 1. Quick Raspberry Pi 3 Deployment
```bash
# Extract package
unzip Sentinel-X-Complete.zip
cd Sentinel-X-Complete

# Single-command installation
chmod +x install.sh start.sh stop.sh status.sh
./install.sh
```

## 2. Service Management
```bash
# Check status of Mosquitto, Backend, and Frontend
./status.sh

# Start services
./start.sh

# Stop services
./stop.sh
```

## 3. Web Access URLs
- **Web Dashboard:** `http://<RASPBERRY_PI_IP>:3000` (or `http://localhost:3000`)
- **FastAPI Backend Swagger:** `http://<RASPBERRY_PI_IP>:8000/docs`
- **Authoritative Twin State:** `http://<RASPBERRY_PI_IP>:8000/api/v1/twin/state`
- **Health Check:** `http://<RASPBERRY_PI_IP>:8000/api/health`

## 4. Hardware Connectivity
1. Flash **Node 01** using `firmware/node01/node01_esp32.ino`.
2. Flash **Node 02** using `firmware/node02/node02_esp32.ino`.
3. Set your local Wi-Fi credentials and Raspberry Pi IP in the `.ino` firmware headers.
4. Verify MQTT packets appear automatically on topics:
   - `sentinel/node01/telemetry`
   - `sentinel/node02/telemetry`
