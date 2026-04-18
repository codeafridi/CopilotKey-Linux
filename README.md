# KeyPilot

Turn your unused Copilot key into a powerful launcher on Linux.

Instead of doing nothing, your Copilot key can now open apps, run commands, and act like a smart shortcut.

---

## ✨ Features

- Press Copilot key → instantly open a menu
- Launch apps, browser, or system actions
- Fully customizable using a simple config file
- Runs in the background automatically
- Works across different Linux setups

---

## 🚀 Installation

```bash
git clone https://github.com/yourname/keypilot
cd keypilot
chmod +x install.sh
./install.sh ```

⚠️ After installation, log out and log back in (required for permissions).

## 🎯 Usage

Just press the Copilot key.

A menu will appear where you can:

1. Open terminal
2. Open browser
3. Run custom actions

## ⚙️ Customization

Edit config.json to change what the key does.

Example:
```bash
{
  "KEY_F23": {
    "type": "menu",
    "options": [
      { "label": "Terminal", "action": "terminal" },
      { "label": "Browser", "action": "browser" }
    ]
  }
} ```

You can add your own actions easily.

## 📦 Requirements
Linux (X11 session)
Python 3
rofi

## ⚠️ Notes
Uses low-level input (/dev/input) → permissions handled in install script
Wayland support is limited (common Linux limitation)
💡 Why this exists

On Linux, the Copilot key is useless.

KeyPilot turns it into something actually useful.
