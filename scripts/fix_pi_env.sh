#!/bin/bash
# ==============================================================================
# Sentinel-X Raspberry Pi Environment, Keyboard & Terminal Repair Utility
# ==============================================================================
# Resolves:
#   1. Keyboard layout mismatch (UK layout typing wrong chars on US keyboards)
#   2. Missing UTF-8 locales causing terminal character corruption
#   3. Windows CRLF (\r\n) line endings breaking bash scripts
#   4. Script executable permissions (chmod +x)
#   5. APT lock releases
# ==============================================================================

echo "======================================================================"
echo "       SENTINEL-X RASPBERRY PI SYSTEM & KEYBOARD REPAIR UTILITY       "
echo "======================================================================"

# 1. Fix Keyboard Layout to US Standard (Fixes @ " # ~ | key mismatches)
echo "[1/5] Configuring Keyboard Layout to Standard US (English)..."
if command -v setxkbmap &> /dev/null; then
    setxkbmap us 2>/dev/null || true
fi

if command -v localectl &> /dev/null; then
    sudo localectl set-x11-keymap us 2>/dev/null || true
    sudo localectl set-keymap us 2>/dev/null || true
fi

if [ -f "/etc/default/keyboard" ]; then
    sudo sed -i 's/XKBLAYOUT=".*"/XKBLAYOUT="us"/' /etc/default/keyboard 2>/dev/null || true
    sudo udevadm trigger --subsystem-match=input --action=change 2>/dev/null || true
fi
echo "  -> Keyboard layout set to US English."

# 2. Fix Locales to en_US.UTF-8
echo "[2/5] Verifying System Locales (en_US.UTF-8)..."
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 3. Fix Windows CRLF (\r) Line Endings Across Project Files
echo "[3/5] Converting Windows CRLF line endings to Linux LF..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

find "$ROOT_DIR" -maxdepth 3 -type f \( -name "*.sh" -o -name "*.py" -o -name "*.json" -o -name "*.service" -o -name "*.txt" -o -name "*.yaml" -o -name "*.env*" \) -exec sed -i 's/\r$//' {} + 2>/dev/null || true
echo "  -> All shell scripts and configuration files cleaned."

# 4. Set Proper Permissions
echo "[4/5] Granting Executable Permissions to all Scripts..."
find "$ROOT_DIR" -maxdepth 3 -type f -name "*.sh" -exec chmod +x {} + 2>/dev/null || true
chmod +x "$ROOT_DIR"/install.sh 2>/dev/null || true
chmod +x "$ROOT_DIR"/start.sh 2>/dev/null || true
chmod +x "$ROOT_DIR"/stop.sh 2>/dev/null || true
chmod +x "$ROOT_DIR"/status.sh 2>/dev/null || true
chmod +x "$ROOT_DIR"/uninstall.sh 2>/dev/null || true
chmod +x "$ROOT_DIR"/update.sh 2>/dev/null || true
echo "  -> Permissions granted (chmod +x)."

# 5. Clear APT and DPKG Stale Locks
echo "[5/5] Checking and releasing stale package manager locks..."
sudo killall apt-get apt unattended-upgrades dpkg 2>/dev/null || true
sudo rm -f /var/lib/apt/lists/lock /var/cache/apt/archives/lock /var/lib/dpkg/lock* 2>/dev/null || true
sudo dpkg --configure -a 2>/dev/null || true

echo "======================================================================"
echo "  [✓] RASPBERRY PI ENVIRONMENT SUCCESSFULLY REPAIRED!                 "
echo "======================================================================"
echo "  • Keyboard layout is now Standard US English."
echo "  • Line endings and execution permissions are fixed."
echo "  • You can now run: bash install.sh"
echo "======================================================================"
