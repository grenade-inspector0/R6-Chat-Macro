import os
import sys
import json
import time
import ctypes
import random
import string
import keyboard
from pynput.keyboard import Key, Controller

pynput_Keyboard = Controller()

def get_config():
    if not os.path.exists("./config.json"):
        if getattr(sys, 'frozen', False):
            file_path = os.path.join(sys._MEIPASS, 'assets', 'config.json')
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'assets', 'config.json')
        default_config = json.load(open(file_path, "r"))

        with open("./config.json", "w") as f:
            json.dump(default_config, f, indent=5)
    return json.load(open("./config.json", "r"))

def press_key(key):
    pynput_Keyboard.press(key)
    time.sleep(0.05)
    pynput_Keyboard.release(key)

def get_positive_messages(num=3, allow_duplicates=False):
    # You can add more messages to ./assets/messages if you want. 
    if getattr(sys, 'frozen', False):
        file_path = os.path.join(sys._MEIPASS, 'assets', 'messages.txt')
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'messages.txt')
    with open(file_path, 'r') as file:
        messages = [line.strip() for line in file.readlines()]
    positive_messages = []
    while len(positive_messages) < num:
        new_message = random.choice(messages)
        if allow_duplicates:
            positive_messages.append(new_message)
        elif new_message not in positive_messages:
            positive_messages.append(new_message)
    return positive_messages

def type_message(text):
    if text is not None:
        press_key("t")
        press_key(Key.backspace)

        # Type the message
        for char in text:
            if char in string.ascii_uppercase:
                with pynput_Keyboard.pressed(Key.shift):
                    press_key(char)
            elif char == "@":
                with pynput_Keyboard.pressed(Key.shift):
                    press_key("2")
            else:
                press_key(char)
        
        press_key(Key.enter)
        press_key(Key.enter)

def send_messages():
    messages = get_positive_messages()
    for message in messages:
        type_message(message)
        time.sleep(random.uniform(0.1, 0.5))

print("v1.0")
keyboard.add_hotkey(hotkey=get_config()["Hotkey"], callback=send_messages, suppress=True)
ctypes.windll.kernel32.SetConsoleTitleW("R6 Reputation Farmer | Status : READY")
print("Ready")

keyboard.wait()