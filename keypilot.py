#!/usr/bin/env python3
from evdev import InputDevice, categorize, ecodes
import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import threading

import evdev


APP_NAME = "KeyPilot"
CONFIG_ENV = "KEYPILOT_CONFIG"
CONFIG_PATHS = [
    os.path.expanduser("~/.config/keypilot/config.json"),
    "/etc/keypilot/config.json",
    os.path.join(os.getcwd(), "config.json"),
]


logging.basicConfig(level=logging.INFO, format="[KeyPilot] %(message)s")


parser = argparse.ArgumentParser(description="Turn the Copilot/F23 key into a launcher.")
parser.add_argument("--device", help="Manually specify input device, for example /dev/input/event3")
parser.add_argument("--config", help="Path to a KeyPilot config file")
args = parser.parse_args()


def find_input_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for dev in devices:
        capabilities = dev.capabilities()
        if ecodes.EV_KEY in capabilities and ecodes.KEY_F23 in capabilities[ecodes.EV_KEY]:
            logging.info(f"Using F23 device: {dev.path} ({dev.name})")
            return dev.path

    for dev in devices:
        if "keyboard" in dev.name.lower():
            logging.warning(f"F23 not found, falling back to: {dev.path} ({dev.name})")
            return dev.path

    return None


def config_candidates():
    if args.config:
        return [args.config]

    env_config = os.environ.get(CONFIG_ENV)
    if env_config:
        return [env_config]

    return CONFIG_PATHS


def load_config():
    for path in config_candidates():
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            try:
                with open(expanded, encoding="utf-8") as config_file:
                    logging.info(f"Using config: {expanded}")
                    return json.load(config_file)
            except Exception as exc:
                logging.error(f"Failed to load config {expanded}: {exc}")
                sys.exit(1)

    logging.error("No config found. Create ~/.config/keypilot/config.json or install /etc/keypilot/config.json")
    sys.exit(1)


def find_menu_launcher():
    launchers = [
        ("rofi-wayland", ["rofi-wayland", "-dmenu", "-i", "-p", APP_NAME]),
        ("wofi", ["wofi", "--dmenu", "--prompt", APP_NAME]),
        ("fuzzel", ["fuzzel", "--dmenu", "--prompt", f"{APP_NAME}> "]),
        ("rofi", ["rofi", "-dmenu", "-i", "-p", APP_NAME]),
    ]

    for binary, command in launchers:
        if shutil.which(binary):
            return binary, command

    return None, None


DEVICE = args.device if args.device else find_input_device()

if not DEVICE:
    logging.error("No suitable input device found")
    sys.exit(1)

dev = InputDevice(DEVICE)
config = load_config()
MENU_LAUNCHER, MENU_COMMAND = find_menu_launcher()

if not MENU_COMMAND:
    logging.error("No menu launcher found. Install rofi-wayland, wofi, fuzzel, or rofi")
    sys.exit(1)

logging.info(f"Using menu launcher: {MENU_LAUNCHER}")
logging.info("Listening...")


def open_terminal():
    terminals = [
        "gnome-terminal",
        "alacritty",
        "kitty",
        "konsole",
        "xfce4-terminal",
        "lxterminal",
        "xterm",
    ]

    for term in terminals:
        if shutil.which(term):
            subprocess.Popen([term])
            return

    logging.error("No terminal found. Install one such as gnome-terminal, alacritty, or xterm")


def run_command(command):
    if not isinstance(command, list) or not command or not all(isinstance(part, str) for part in command):
        logging.error("Invalid command. Use a JSON array like [\"xdg-open\", \"https://example.com\"]")
        return

    try:
        subprocess.Popen(command)
    except FileNotFoundError:
        logging.error(f"Command not found: {command[0]}")
    except Exception as exc:
        logging.error(f"Failed to run command {command}: {exc}")


def run_action(option):
    if isinstance(option, str):
        action = option
        command = None
    else:
        action = option.get("action")
        command = option.get("command")

    if command:
        run_command(command)
    elif action == "terminal":
        open_terminal()
    elif action == "browser":
        run_command(["xdg-open", "https://google.com"])
    elif action == "shutdown":
        run_command(["systemctl", "poweroff"])
    else:
        logging.error(f"Unknown action: {action}")


menu_process = None
menu_lock = threading.Lock()


def launcher_env():
    uid = os.getuid()
    env = os.environ.copy()
    env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", f"unix:path=/run/user/{uid}/bus")
    env.setdefault("WAYLAND_DISPLAY", "wayland-0")
    env.setdefault("DISPLAY", ":0")
    return env


def handle_menu_output(process, options):
    global menu_process

    stdout, stderr = process.communicate()

    with menu_lock:
        if menu_process is process:
            menu_process = None

    if process.returncode not in (0, 1):
        error = stderr.strip() if stderr else f"exit code {process.returncode}"
        logging.error(f"{MENU_LAUNCHER} failed: {error}")
        return

    choice = stdout.strip() if stdout else ""
    if not choice:
        return

    for option in options:
        if option.get("label") == choice:
            run_action(option)
            return


def open_menu(options):
    global menu_process

    with menu_lock:
        if menu_process and menu_process.poll() is None:
            menu_process.terminate()
            menu_process = None
            return

        menu_text = "\n".join([option.get("label", "") for option in options])
        menu_process = subprocess.Popen(
            MENU_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=launcher_env(),
        )

        menu_process.stdin.write(menu_text)
        menu_process.stdin.close()
        threading.Thread(target=handle_menu_output, args=(menu_process, options), daemon=True).start()


for event in dev.read_loop():
    try:
        if event.type != ecodes.EV_KEY:
            continue

        key = categorize(event)
        if key.keystate != key.key_down:
            continue

        keycode = key.keycode[0] if isinstance(key.keycode, list) else key.keycode
        key_config = config.get(keycode)

        if key_config and key_config.get("type") == "menu":
            open_menu(key_config.get("options", []))
    except Exception as exc:
        logging.error(f"Runtime error: {exc}")
