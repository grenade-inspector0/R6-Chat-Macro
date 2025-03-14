import os
import sys
import json
import time
import ctypes
import random
import string
import keyboard
from pynput.keyboard import Key, Controller

VERSION = 2.0
pynput_Keyboard = Controller()

def clean_exit(exit_reason):
    os.system("cls")
    input(f"{exit_reason}\n\nPress Enter to exit...")
    os.system("cls")
    sys.exit()

def get_config():
    if not os.path.exists("./config.json"):
        if getattr(sys, 'frozen', False):
            file_path = os.path.join(sys._MEIPASS, 'assets', 'config.json')
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'assets', 'config.json')
        default_config = json.load(open(file_path, "r"))

        with open("./config.json", "w") as f:
            json.dump(default_config, f, indent=5)
        
        # Tell the user a config was created
        clean_exit("Config not found. Generating new config file... Config file successfully generated!")
        
    return json.load(open("./config.json", "r"))

def press_key(key):
    pynput_Keyboard.press(key)
    time.sleep(0.05)
    pynput_Keyboard.release(key)

def get_messages(messages=[], num=3, allow_duplicates=False):
    output_messages = []
    while len(output_messages) < num:
        new_message = random.choice(messages)
        if allow_duplicates:
            output_messages.append(new_message)
        elif new_message not in output_messages:
            output_messages.append(new_message)
    return output_messages

def type_message(text):
    if text is not None:
        press_key(get_config()["All_Chat_Key"])
        press_key(Key.backspace)

        keyboard.write(text, random.uniform(0.035, 0.055))
        
        press_key(Key.enter)
        press_key(Key.enter)

def send_messages():
    if get_config()["Messages"]["use_custom_messages"]:
        messages = get_messages(get_config()["Messages"]["custom_messages"])
    else:
        # You can add more messages to ./assets/messages if you want. 
        if getattr(sys, 'frozen', False):
            file_path = os.path.join(sys._MEIPASS, 'assets', 'messages.txt')
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'assets', 'messages.txt')
        with open(file_path, 'r') as file:
            positive_messages = [line.strip() for line in file.readlines()]
        messages = get_messages(positive_messages)

    for message in messages:
        type_message(message)
        time.sleep(random.uniform(0.1, 0.5))

print(f"v{VERSION}")
print(f"Ready")

response = None
last_hotkey = get_config()["Hotkey"]
response = keyboard.add_hotkey(hotkey=get_config()["Hotkey"], callback=send_messages, suppress=True)

while True:
    if last_hotkey != get_config()["Hotkey"]:
        keyboard.remove_hotkey(response)
        last_hotkey = get_config()["Hotkey"]
        response = keyboard.add_hotkey(hotkey=get_config()["Hotkey"], callback=send_messages, suppress=True)
    time.sleep(3)

ctypes.windll.kernel32.SetConsoleTitleW(f"R6 Reputation Farmer v{VERSION}")
keyboard.wait()