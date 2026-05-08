#!/usr/bin/env bash

set -e 

echo "Installing KeyPilot..."

if [ "$(id -u)" -eq 0 ]; then
    echo "Please run this script as your normal user, not with sudo."
    echo "The script will ask for sudo only when system changes are needed."
    exit 1
fi

# Install system dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv
sudo apt install -y rofi-wayland || sudo apt install -y rofi

# Install python dependency
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# Install user config without overwriting local changes
mkdir -p ~/.config/keypilot
if [ ! -f ~/.config/keypilot/config.json ]; then
    cp config.example.json ~/.config/keypilot/config.json
fi

# Add user to input group
sudo usermod -aG input "$USER"

# Create udev rule
echo 'KERNEL=="event*", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-keypilot.rules

sudo udevadm control --reload-rules
sudo udevadm trigger

# Setup systemd user service
mkdir -p ~/.config/systemd/user
sed "s|%h/keypilot|$PWD|g" keypilot.service > ~/.config/systemd/user/keypilot.service

systemctl --user import-environment DISPLAY WAYLAND_DISPLAY XAUTHORITY DBUS_SESSION_BUS_ADDRESS XDG_CURRENT_DESKTOP XDG_SESSION_TYPE PATH || true
systemctl --user daemon-reload
systemctl --user enable keypilot

if id -nG | grep -qw input; then
    systemctl --user reset-failed keypilot || true
    systemctl --user restart keypilot
else
    echo "KeyPilot service enabled, but not started yet."
    echo "Your current login session is not using the new input-group permission."
fi

echo "Installation complete."
echo "You MUST log out and log back in for permissions to apply."
echo "After logging back in, run: systemctl --user restart keypilot"
