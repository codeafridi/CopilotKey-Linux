# KeyPilot

Turn your Copilot key into a customizable launcher on Linux.

Press → menu → run anything instantly.
---

<img width="1488" height="656" alt="image" src="https://github.com/user-attachments/assets/2eac6d8d-46c6-4262-9c26-d98f351b4c49" />

here are the pdfs repo for CP - [My CP Notes Repo](https://github.com/codeafridi/Competitive-programming-notes)

##  Features

- Press Copilot key → instantly open a menu  
- Launch apps, browser, or system actions  
- Fully customizable using a simple config file  
- Runs in the background automatically  
- Works across different Linux setups  

---

##  Installation

```bash
git clone https://github.com/yourname/keypilot
cd keypilot
chmod +x install.sh
./install.sh
```

Run the script as your normal user, not with `sudo`. It will ask for sudo only
when it needs to install packages or update input-device permissions.

The installer:

- installs Python/system dependencies
- creates a local `.venv`
- installs Python packages into that `.venv`
- installs a menu launcher (`rofi-wayland` when available, otherwise `rofi`)
- adds your user to the `input` group
- enables the `keypilot` user service

After installation, **log out and log back in** or reboot. This is required so
Linux applies the new `input` group permission to your desktop session.

Then start/restart KeyPilot:

```bash
systemctl --user restart keypilot
```

---

## Usage

Just press the **Copilot key**.

A menu will appear where you can:
- Open terminal  
- Open browser  
- Run custom actions  

To check whether the background service is running:

```bash
systemctl --user status keypilot
```

To watch logs while pressing the Copilot key:

```bash
journalctl --user -u keypilot -f
```

---

## Customization

Edit `config.json` to change what the key does.

Example:

```json
{
  "KEY_F23": {
    "type": "menu",
    "options": [
      { "label": "Terminal", "action": "terminal" },
      { "label": "Browser", "action": "browser" }
    ]
  }
}
```
## Adding More Menu Options

You can add as many options as you want to the menu.

Just edit `config.json` and add more items inside the `options` list.

### Example
```json
{
  "KEY_F23": {
    "type": "menu",
    "options": [
      { "label": "Terminal", "action": "terminal" },
      { "label": "Browser", "action": "browser" },
      { "label": "Shutdown", "action": "shutdown" },
      { "label": "Files", "action": "files" },
      { "label": "VS Code", "action": "code" }
    ]
  }
}
```
### Important

If you add a new action in `config.json`, you also need to add it in the code.

Open `keypilot.py` and find the `run_action()` function.

### Actions Guide (Apps, Websites, Files, System Commands)

Every action is executed using:

```python
subprocess.Popen(["command", "arg1", "arg2"])
```

---

##  Quick Rules

- **App** → `["app-name"]`
- **Website** → `["xdg-open", "https://..."]`
- **File/Folder** → `["xdg-open", "path"]`
- **System command** → `["command", "argument"]`
- **Search (optional)** → `["xdg-open", "https://google.com/search?q=..."]`

---

## Common Examples

| Category     | What you want to do         | Example code |
|--------------|----------------------------|--------------|
| App          | Open terminal              | `["gnome-terminal"]` |
| App          | Open VS Code               | `["code"]` |
| App          | Open Firefox               | `["firefox"]` |
| App          | Open file manager          | `["nautilus"]` |
| Website      | Open Google                | `["xdg-open", "https://google.com"]` |
| Website      | Open YouTube               | `["xdg-open", "https://youtube.com"]` |
| File/Folder  | Open current folder        | `["xdg-open", "."]` |
| File/Folder  | Open Downloads             | `["xdg-open", "~/Downloads"]` |
| File         | Open a PDF                 | `["xdg-open", "file.pdf"]` |
| System       | Shutdown                   | `["systemctl", "poweroff"]` |
| System       | Restart                    | `["systemctl", "reboot"]` |
| System       | Lock screen                | `["loginctl", "lock-session"]` |
| System       | Logout                     | `["gnome-session-quit", "--logout"]` |
| Search       | Google search              | `["xdg-open", "https://google.com/search?q=linux"]` |
| Custom       | Run script                 | `["bash", "script.sh"]` |
| Custom       | Python script              | `["python3", "file.py"]` |

---

## Example in `run_action()`

```python
def run_action(action):
    if action == "terminal":
        subprocess.Popen(["gnome-terminal"])
    elif action == "browser":
        subprocess.Popen(["xdg-open", "https://google.com"])
    elif action == "shutdown":
        subprocess.Popen(["systemctl", "poweroff"])
    elif action == "code":
        subprocess.Popen(["code"])
```

---

##  Important

- Always use `["command", "arg"]` format  
- Do NOT write commands as a single string  
- Use `xdg-open` for anything that should open with default apps  

---

Thats it. you can launch anything.
After changing the service file or reinstalling dependencies, run:

```bash
./install.sh
systemctl --user restart keypilot
```

---

## Requirements

- Linux
- Python 3
- `python3-venv`
- one supported menu launcher:
  - `rofi-wayland` recommended for Wayland
  - `wofi`
  - `fuzzel`
  - `rofi` for X11

---

## Notes

- Uses low-level input (`/dev/input`) → permissions handled in install script  
- The installer uses a local `.venv`, so it avoids Python's
  `externally-managed-environment` / PEP 668 error.
- KeyPilot tries menu launchers in this order: `rofi-wayland`, `wofi`,
  `fuzzel`, then `rofi`.
- On GNOME Wayland, classic `/usr/bin/rofi` may crash. Install `rofi-wayland`
  or `wofi`, then restart the service.

---

## Troubleshooting

### Service says "No suitable input device found"

Check your active groups:

```bash
id -nG | grep -w input
```

If nothing prints, log out completely and log back in, or reboot. Then run:

```bash
systemctl --user reset-failed keypilot
systemctl --user restart keypilot
journalctl --user -u keypilot -n 30 --no-pager
```

When it works, the logs should contain something like:

```text
[KeyPilot] Using F23 device: /dev/input/event3 (...)
[KeyPilot] Listening...
```

### Ubuntu reports that rofi crashed

If you see an Ubuntu crash dialog for `/usr/bin/rofi`, install a Wayland-friendly
launcher:

```bash
sudo apt install rofi-wayland
```

If that package is not available:

```bash
sudo apt install wofi
```

Then restart KeyPilot:

```bash
systemctl --user restart keypilot
```

---

## Why this exists

On Linux, the Copilot key is useless.

KeyPilot turns it into something actually useful.

Works on X11 and can work on Wayland when a Wayland-friendly menu launcher is
installed.
