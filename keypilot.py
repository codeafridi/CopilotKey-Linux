# from evdev import InputDevice, categorize, ecodes
# import subprocess
# import os

# # === CONFIG ===
# import shutil
# import sys

# def check_dependencies():
#     if not shutil.which("rofi"):
#         print("Error: rofi not installed")
#         print("Install with: sudo apt install rofi")
#         sys.exit(1)

#     if not shutil.which("xdg-open"):
#         print("Error: xdg-open missing")
#         sys.exit(1)

# DEVICE = "/dev/input/event3"
# REAL_USER = os.environ.get("SUDO_USER")

# dev = InputDevice(DEVICE)

# print("Listening...")


# def get_user_env():
#     return {
#         "DISPLAY": ":0",
#         "XAUTHORITY": f"/home/{REAL_USER}/.Xauthority",
#         "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus"
#     }


# def run_as_user(command):
#     subprocess.Popen(
#         ["sudo", "-u", REAL_USER] + command,
#         env=get_user_env()
#     )


# # === UNIVERSAL TERMINAL LAUNCHER ===
# def open_terminal():
#     terminals = [
#         "gnome-terminal",
#         "alacritty",
#         "kitty",
#         "konsole",
#         "xfce4-terminal",
#         "lxterminal",
#         "xterm"
#     ]

#     for term in terminals:
#         if subprocess.call(
#             ["which", term],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL
#         ) == 0:
#             try:
#                 run_as_user([term])
#                 return
#             except Exception:
#                 continue

#     print("No working terminal found.")
#     print("Try installing one: sudo apt install gnome-terminal or xterm")
#     print("If GNOME Terminal fails, run: sudo apt install dbus-x11")


# # === MENU ===
# def open_menu():
#     options = "Terminal\nBrowser\nShutdown"

#     result = subprocess.run(
#         ["sudo", "-u", REAL_USER, "rofi", "-dmenu"],
#         input=options,
#         text=True,
#         capture_output=True,
#         env=get_user_env()
#     )

#     choice = result.stdout.strip()

#     if choice == "Terminal":
#         open_terminal()

#     elif choice == "Browser":
#         run_as_user(["xdg-open", "https://google.com"])

#     elif choice == "Shutdown":
#         subprocess.Popen("shutdown now", shell=True)


# # === LISTENER ===
# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         key = categorize(event)

#         if key.keystate == key.key_down:
#             if key.keycode == 'KEY_F23' or (
#                 isinstance(key.keycode, list) and 'KEY_F23' in key.keycode
#             ):
#                 print("Launching menu...")
#                 open_menu()

from evdev import InputDevice, categorize, ecodes
import subprocess
import shutil
import json

import evdev

def find_keyboard():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for dev in devices:
        if "keyboard" in dev.name.lower():
            return dev.path
    return None

DEVICE = find_keyboard()

if not DEVICE:
    print("No keyboard found")
    exit(1)

dev = InputDevice(DEVICE)

print("Listening...")


def load_config():
    with open("config.json") as f:
        return json.load(f)


config = load_config()


def open_terminal():
    terminals = [
        "gnome-terminal",
        "alacritty",
        "kitty",
        "konsole",
        "xfce4-terminal",
        "lxterminal",
        "xterm"
    ]

    for term in terminals:
        if shutil.which(term):
            subprocess.Popen([term])
            return

    print("No working terminal found.")
    print("Try installing one: sudo apt install gnome-terminal or xterm")
    print("If GNOME Terminal fails, run: sudo apt install dbus-x11")


def run_action(action):
    if action == "terminal":
        open_terminal()
    elif action == "browser":
        subprocess.Popen(["xdg-open", "https://google.com"])
    elif action == "shutdown":
        subprocess.Popen(["shutdown", "now"])


import subprocess

def is_rofi_running():
    return subprocess.call(
        ["pgrep", "-x", "rofi"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0


import subprocess

rofi_process = None

rofi_process = None

def open_menu(options):
    global rofi_process

    # If already open → close
    if rofi_process and rofi_process.poll() is None:
        rofi_process.terminate()
        rofi_process = None
        return

    menu_text = "\n".join([opt["label"] for opt in options])

    rofi_process = subprocess.Popen(
        ["rofi", "-dmenu", "-i", "-p", "KeyPilot"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    rofi_process.stdin.write(menu_text)
    rofi_process.stdin.close()

    


for event in dev.read_loop():

    if event.type == ecodes.EV_KEY:
        key = categorize(event)

        if key.keystate == key.key_down:
            keycode = key.keycode

            if isinstance(keycode, list):
                keycode = keycode[0]

            if keycode in config:
                action = config[keycode]

                if action["type"] == "menu":
                    open_menu(action["options"])


    if rofi_process and rofi_process.poll() is not None:
        output = rofi_process.stdout.read().strip()
        rofi_process = None

        if "KEY_F23" in config:
            options = config["KEY_F23"]["options"]

            for opt in options:
                if opt["label"] == output:
                    run_action(opt["action"])
                    break