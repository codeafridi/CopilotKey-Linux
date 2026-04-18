#!/bin/bash

echo "Installing KeyPilot..."

# Install dependencies
sudo apt update
sudo apt install -y python3-pip rofi

pip install -r requirements.txt

# Permissions
sudo usermod -aG input $USER

# Udev rule
echo 'KERNEL=="event*", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-keypilot.rules

sudo udevadm control --reload-rules
sudo udevadm trigger

# Setup systemd
mkdir -p ~/.config/systemd/user
cp keypilot.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable keypilot

echo "Done."
echo "⚠️ Log out and log back in"
