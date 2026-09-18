# RASPBERRY PI 3/4/5 DEPLOYMENT GUIDE

## 1. Target Hardware Specifications
- **Central Edge Node:** Raspberry Pi 3 (or 4/5) running Raspberry Pi OS (Debian 64-bit / 32-bit).
- **Network Interface:** Static/DHCP Ethernet or Wi-Fi (e.g., `10.242.228.126`).
- **Required Ports:**
  - `1883`: Mosquitto MQTT Broker (Sensor nodes to edge)
  - `8000`: FastAPI REST + WebSocket Engine
  - `3000`: Sentinel-X Web Dashboard

---

## 2. Automated One-Command Installation
```bash
# On your Raspberry Pi terminal:
cd ~
unzip Sentinel-X-Complete.zip
cd Sentinel-X-Complete

# Make scripts executable
chmod +x install.sh start.sh stop.sh status.sh update.sh uninstall.sh

# Run full setup
./install.sh
```

### What `install.sh` Performs:
1. Validates Python 3, pip, and venv; installs necessary build dependencies.
2. Installs and configures Mosquitto MQTT broker (`/etc/mosquitto/conf.d/sentinel.conf`).
3. Installs backend Python packages (`fastapi`, `uvicorn`, `paho-mqtt`, `pydantic`).
4. Installs frontend web server runtime.
5. Installs and enables systemd service units for automatic boot startup:
   - `sentinel-backend.service`
   - `sentinel-frontend.service`
   - `sentinel-mqtt-check.service`
6. Runs startup health checks and outputs active LAN dashboard links.

---

## 3. Automatic Kiosk Mode on 5-Inch HDMI Display
If connected to a 5-inch HDMI LCD on the Raspberry Pi:
Add to `~/.config/lxsession/LXDE-pi/autostart` or `/etc/xdg/lxsession/LXDE-pi/autostart`:
```bash
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --noerrdialogs --disable-infobars --kiosk http://localhost:3000
```
This boots directly into the Sentinel-X high-contrast industrial dashboard upon power-on.
