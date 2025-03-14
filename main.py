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

if getattr(sys, 'frozen', False):
    file_path = os.path.join(sys._MEIPASS, 'assets', 'config.json')
else:
    file_path = os.path.join(os.path.dirname(__file__), 'assets', 'config.json')
default_config = json.load(open(file_path, "r"))

def clean_exit(exit_reason):
    os.system("cls")
    input(f"{exit_reason}\n\nPress Enter to exit...")
    os.system("cls")
    sys.exit()

def create_config(exit_reason="Config not found. Generating new config file... Config file successfully generated!"):
    with open("./config.json", "w") as f:
        json.dump(default_config, f, indent=5)

    # Tell the user a config was created, and or why it was created
    clean_exit(exit_reason)

def get_config():
    # Create a new config if the user doesn't already have a config, then exit
    if not os.path.exists("./config.json"):
        create_config()
    
    # Check for any missing keys, this mainly for when a version changes and the user has the old config
    missing_keys = [key for key in default_config if key not in json.load(open("./config.json", "r"))]
    if missing_keys: # If there are variables (also called keys) are missing in the user's current config, then it will generate a new config
        create_config(exit_reason="Config found!\nYour config file is missing variables. Generating new config... Config file successfully generated!")

    config_data = json.load(open("./config.json", "r"))
    # If both use_custom_messages and the Youtube Link typer are enabled, then exit
    if config_data["Messages"]["use_custom_messages"] and config_data["Messages"]["Youtube_Link_Typer"]["enabled"]:
        clean_exit("\"Use_Custom_Messages\" and the Youtube Link Typer are both enabled.\nEnable only one of them.")

    return config_data

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

        # Type the text (in this case, the message) that is inputted into the function
        keyboard.write(text, random.uniform(0.035, 0.055))
        
        press_key(Key.enter)
        press_key(Key.enter)

def send_messages():
    if get_config()["Messages"]["use_custom_messages"]:
        messages = get_messages(get_config()["Messages"]["custom_messages"])
    elif get_config()["Messages"]["Youtube_Link_Typer"]["enabled"]:
        # е м о с т у - The russian characters used to bypass Ubisoft's Link Filter
        messages = [f"уоuтubе.сом/@{get_config()["Messages"]["Youtube_Link_Typer"]["yt_channel_name"]}" for _ in range(3)]
    else:
        # You can add more messages to ./assets/messages if you want; Only possible if you compile it yourself.
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

ctypes.windll.kernel32.SetConsoleTitleW(f"R6 Reputation Farmer v{VERSION}")
print(f"v{VERSION}")
print(f"Ready\n\nPress your exit hotkey if you wish to exit.")

response = None
last_hotkeys = [get_config()["Hotkey"], get_config()["Exit_Hotkey"]]
last_hotkey = get_config()["Hotkey"]
responses = [keyboard.add_hotkey(hotkey=last_hotkeys[0], callback=send_messages, suppress=True),
             keyboard.add_hotkey(hotkey=last_hotkeys[1], callback=clean_exit, args=("Thanks for using the R6 Chat Macro.", ), suppress=True)]

while True:
    # Every 3 seconds check if the user has changed the hotkeys they wish to use
    if last_hotkeys[0] != get_config()["Hotkey"]: 
        keyboard.remove_hotkey(responses[0]) # If they have, remove their old hotkey
        responses[0] = keyboard.add_hotkey(hotkey=get_config()["Hotkey"], callback=send_messages, suppress=True) # Change the hotkey to the new one
        last_hotkeys[0] = get_config()["Hotkey"] # Set the new hotkey as the last used hotkey
    if last_hotkeys[1] != get_config()["Exit_Hotkey"]: 
        keyboard.remove_hotkey(responses[1]) # If they have, remove their old hotkey
        responses[1] = keyboard.add_hotkey(hotkey=get_config()["Exit_Hotkey"], callback=clean_exit, args=("Thanks for using the R6 Chat Macro.", ), suppress=True) # Change the exit hotkey to the new one
        last_hotkeys[1] = get_config()["Exit_Hotkey"] # Set the new hotkey as the last used hotkey
    time.sleep(3)
