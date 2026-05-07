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
sudo apt install -y python3-pip rofi

# Install python dependency
python3 -m pip install --user -r requirements.txt || python3 -m pip install --break-system-packages -r requirements.txt

# Add user to input group
sudo usermod -aG input "$USER"

# Create udev rule
echo 'KERNEL=="event*", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-keypilot.rules

sudo udevadm control --reload-rules
sudo udevadm trigger

# Setup systemd user service
mkdir -p ~/.config/systemd/user
sed "s|%h/keypilot|$PWD|g" keypilot.service > ~/.config/systemd/user/keypilot.service

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
