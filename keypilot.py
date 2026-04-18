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
import argparse
import logging
import sys


# ---------- LOGGING ----------
logging.basicConfig(
    level=logging.INFO,
    format="[KeyPilot] %(message)s"
)


# ---------- CLI ----------
parser = argparse.ArgumentParser()
parser.add_argument("--device", help="Manually specify input device")
args = parser.parse_args()


# ---------- DEVICE DETECTION ----------
def find_input_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    # Try finding KEY_F23 device
    for dev in devices:
        capabilities = dev.capabilities()

        if ecodes.EV_KEY in capabilities:
            if ecodes.KEY_F23 in capabilities[ecodes.EV_KEY]:
                logging.info(f"Using F23 device: {dev.path} ({dev.name})")
                return dev.path

    # Fallback: first keyboard-like device
    for dev in devices:
        if "keyboard" in dev.name.lower():
            logging.warning(f"F23 not found, falling back to: {dev.path} ({dev.name})")
            return dev.path

    return None


DEVICE = args.device if args.device else find_input_device()

if not DEVICE:
    logging.error("No suitable input device found")
    sys.exit(1)

dev = InputDevice(DEVICE)
logging.info("Listening...")


# ---------- CONFIG ----------
def load_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        sys.exit(1)


config = load_config()


# ---------- DEPENDENCIES ----------
if not shutil.which("rofi"):
    logging.error("rofi not installed")
    sys.exit(1)


# ---------- ACTIONS ----------
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

    logging.error("No terminal found. Install one (gnome-terminal, xterm, etc.)")


def run_action(action):
    if action == "terminal":
        open_terminal()
    elif action == "browser":
        subprocess.Popen(["xdg-open", "https://google.com"])
    elif action == "shutdown":
        subprocess.Popen(["systemctl", "poweroff"])


# ---------- MENU ----------
rofi_process = None
current_options = None


def open_menu(options):
    global rofi_process, current_options

    # Toggle behavior
    if rofi_process and rofi_process.poll() is None:
        rofi_process.terminate()
        rofi_process = None
        return

    menu_text = "\n".join([opt["label"] for opt in options])
    current_options = options

    rofi_process = subprocess.Popen(
        ["rofi", "-dmenu", "-i", "-p", "KeyPilot"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    rofi_process.stdin.write(menu_text)
    rofi_process.stdin.close()


# ---------- MAIN LOOP ----------
for event in dev.read_loop():

    try:
        if event.type == ecodes.EV_KEY:
            key = categorize(event)

            if key.keystate == key.key_down:
                keycode = key.keycode

                if isinstance(keycode, list):
                    keycode = keycode[0]

                if keycode in config:
                    action = config[keycode]

                    if action.get("type") == "menu":
                        open_menu(action.get("options", []))

        # Handle rofi output
        if rofi_process and rofi_process.poll() is not None:
            output = rofi_process.stdout.read().strip() if rofi_process.stdout else ""
            rofi_process = None

            if output and current_options:
                for opt in current_options:
                    if opt["label"] == output:
                        run_action(opt["action"])
                        break

    except Exception as e:
        logging.error(f"Runtime error: {e}")