#!/bin/bash
# ==============================================================================
# Sentinel-X Autostart & Auto-Browser Setup for Raspberry Pi OS
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LAUNCH_SCRIPT="$SCRIPT_DIR/launch_kiosk.sh"
chmod +x "$LAUNCH_SCRIPT"

# 1. Standard XDG Autostart (.config/autostart)
mkdir -p "$HOME/.config/autostart"
cat > "$HOME/.config/autostart/sentinel-kiosk.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Sentinel-X Industrial Dashboard Kiosk
Comment=Autonomous Sentinel-X Disaster Intelligence Dashboard
Exec=$LAUNCH_SCRIPT
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

# 2. LXDE-pi Autostart (for Bullseye / Legacy Raspberry Pi OS Desktop)
mkdir -p "$HOME/.config/lxsession/LXDE-pi"
if [ ! -f "$HOME/.config/lxsession/LXDE-pi/autostart" ]; then
    if [ -f "/etc/xdg/lxsession/LXDE-pi/autostart" ]; then
        cp /etc/xdg/lxsession/LXDE-pi/autostart "$HOME/.config/lxsession/LXDE-pi/autostart"
    fi
fi

if [ -f "$HOME/.config/lxsession/LXDE-pi/autostart" ]; then
    sed -i '/launch_kiosk.sh/d' "$HOME/.config/lxsession/LXDE-pi/autostart"
    echo "@$LAUNCH_SCRIPT" >> "$HOME/.config/lxsession/LXDE-pi/autostart"
fi

# 3. Wayfire Desktop Configuration (for Bookworm Wayland Desktop)
WAYFIRE_INI="$HOME/.config/wayfire.ini"
if [ -f "$WAYFIRE_INI" ]; then
    if ! grep -q "sentinel_kiosk" "$WAYFIRE_INI"; then
        echo "" >> "$WAYFIRE_INI"
        echo "[autostart]" >> "$WAYFIRE_INI"
        echo "sentinel_kiosk = $LAUNCH_SCRIPT" >> "$WAYFIRE_INI"
    fi
fi

echo "[✓] Automatic Kiosk Browser configured. On boot/reboot, Sentinel-X will open automatically in full-screen!"
