# KeyPilot

Turn your Copilot key into a customizable launcher on Linux.

Press the Copilot/F23 key, pick an action, and launch apps, websites, files, or system commands instantly.

![KeyPilot screenshot](https://github.com/user-attachments/assets/2eac6d8d-46c6-4262-9c26-d98f351b4c49)

## Features

- Opens a launcher menu from the Copilot/F23 key
- Runs apps, websites, files, folders, and system commands
- Configurable with simple JSON
- Runs as a background user service
- Supports `rofi-wayland`, `wofi`, `fuzzel`, and `rofi`

## Install From Source

```bash
git clone https://github.com/codeafridi/CopilotKey-Linux.git
cd CopilotKey-Linux
chmod +x install.sh
./install.sh
```

Run the script as your normal user, not with `sudo`. It asks for `sudo` only when it needs to install system packages or update input-device permissions.

After installation, log out and log back in. This is required so Linux applies the new `input` group permission to your desktop session.

Then start KeyPilot:

```bash
systemctl --user restart keypilot
```

## Install From A Debian Package

Build a local `.deb` package:

```bash
chmod +x packaging/deb/build-deb.sh
packaging/deb/build-deb.sh 0.1.0
```

Install it on Ubuntu/Debian:

```bash
sudo apt install ./dist/keypilot_0.1.0_all.deb
```

Then enable permissions and the user service:

```bash
sudo usermod -aG input "$USER"
```

Log out and log back in, then run:

```bash
mkdir -p ~/.config/keypilot
cp /etc/keypilot/config.json ~/.config/keypilot/config.json
systemctl --user daemon-reload
systemctl --user enable --now keypilot
```

## Usage

Press the Copilot key. A menu appears with your configured actions.

Check whether the service is running:

```bash
systemctl --user status keypilot
```

Watch logs while pressing the key:

```bash
journalctl --user -u keypilot -f
```

## Configuration

Edit:

```bash
~/.config/keypilot/config.json
```

Example:

```json
{
  "KEY_F23": {
    "type": "menu",
    "options": [
      {
        "label": "Terminal",
        "action": "terminal"
      },
      {
        "label": "GitHub",
        "command": ["xdg-open", "https://github.com"]
      },
      {
        "label": "VS Code",
        "command": ["code"]
      }
    ]
  }
}
```

Each menu option supports either:

- `action`: a built-in KeyPilot action
- `command`: a command array, for example `["xdg-open", "https://example.com"]`

Built-in actions:

- `terminal`
- `browser`
- `shutdown`

Use `command` for everything else. KeyPilot does not run commands through a shell, so write each command and argument as a separate JSON string.

## Requirements

- Linux
- Python 3
- `evdev`
- `xdg-open`
- One menu launcher:
  - `rofi-wayland` recommended for GNOME/Wayland
  - `wofi`
  - `fuzzel`
  - `rofi`

## Permissions

KeyPilot reads low-level keyboard events from `/dev/input`. On Ubuntu, the installer adds your user to the `input` group so the user service can read the Copilot/F23 key.

This is powerful access. Only install KeyPilot from source you trust.

## Packaging Roadmap

- `.deb` package for Ubuntu/Debian
- AUR package for Arch Linux
- Snap package for Ubuntu App Center
- Optional GNOME extension later, if deeper GNOME integration becomes useful

## License

MIT
