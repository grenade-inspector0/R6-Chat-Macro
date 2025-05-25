import os
import sys
import json
import time
import ctypes
import random
import string
import keyboard
from pynput.keyboard import Key, Controller

VERSION = 3.1
pynput_Keyboard = Controller()

# Currently, the only messages that I know of that actually work. (As of Y10 S1)
messages = [
    "gr",
    "gg",
    "ggs",
    "glhf",
    "nt"
]

def clean_exit(exit_reason):
    os.system("cls")
    input(f"{exit_reason}\n\nPress Enter to exit...")
    os.system("cls")
    os._exit(0)

def get_config():
    # Create a new config if the user doesn't already have a config, then exit
    if not os.path.exists("./config.json"):
        file_path = os.path.join(sys._MEIPASS, 'assets', 'config.json') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'assets', 'config.json')
        default_config = json.load(open(file_path, "r"))
        with open("./config.json", "w") as f:
            json.dump(default_config, f, indent=5)
        clean_exit("Config not found. Generating new config file... Config file successfully generated!")
    
    return json.load(open("./config.json", "r"))

def press_key(key):
    pynput_Keyboard.press(key)
    time.sleep(0.05)
    pynput_Keyboard.release(key)

def send_messages():
    for message in messages:
        press_key(config_data["All_Chat_Key"])
        press_key(Key.backspace)

        keyboard.write(message, random.uniform(0.035, 0.055))
        
        press_key(Key.enter)
        press_key(Key.enter)
        time.sleep(random.uniform(0.1, 0.5))

os.system("cls")
ctypes.windll.kernel32.SetConsoleTitleW(f"R6 Chat Macro v{VERSION}")
config_data = get_config()

keyboard.add_hotkey(hotkey=config_data["Hotkey"], callback=send_messages, suppress=True)
print(f"v{VERSION}")
print(f"Ready\n\nIf you wish to exit, simply close the window.")

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        clean_exit("Exiting...")