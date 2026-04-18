#!/usr/bin/env bash

set -e 

echo "Installing KeyPilot..."

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
systemctl --user start keypilot

echo "Installation complete."
echo "⚠️ You MUST log out and log back in for permissions to apply."