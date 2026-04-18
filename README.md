# KeyPilot

Turn your Copilot key into a customizable launcher on Linux.

Press → menu → run anything instantly.
---

## ✨ Features

- Press Copilot key → instantly open a menu  
- Launch apps, browser, or system actions  
- Fully customizable using a simple config file  
- Runs in the background automatically  
- Works across different Linux setups  

---

![demo](demo.gif)

## 🚀 Installation

```bash
git clone https://github.com/yourname/keypilot
cd keypilot
chmod +x install.sh
./install.sh
```

⚠️ After installation, **log out and log back in** (required for permissions).

---

## 🎯 Usage

Just press the **Copilot key**.

A menu will appear where you can:
- Open terminal  
- Open browser  
- Run custom actions  

---

## ⚙️ Customization

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

---

## 📦 Requirements

- Linux (X11 session)  
- Python 3  
- rofi  

---

## ⚠️ Notes

- Uses low-level input (`/dev/input`) → permissions handled in install script  
- Wayland support is limited (common Linux limitation)  

---

## 💡 Why this exists

On Linux, the Copilot key is useless.

KeyPilot turns it into something actually useful.

⚠️ Works best on X11. Wayland support may be limited.