# KeyPilot

Turn your Copilot key into a customizable launcher on Linux.

Press → menu → run anything instantly.
---

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

 After installation, **log out and log back in** (required for permissions).

---

## Usage

Just press the **Copilot key**.

A menu will appear where you can:
- Open terminal  
- Open browser  
- Run custom actions  

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
At last run the file again ```./install.sh ```

---

## Requirements

- Linux (X11 session)  
- Python 3  
- rofi  

---

## Notes

- Uses low-level input (`/dev/input`) → permissions handled in install script  
- Wayland support is limited (common Linux limitation)  

---

## Why this exists

On Linux, the Copilot key is useless.

KeyPilot turns it into something actually useful.

Works best on X11. Wayland support may be limited.