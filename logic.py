import os
import json
import shutil
import pygame
import keyboard
from tkinter import messagebox
from parser import image2text, parse

with open("content/config.json", "r") as file:
    config = json.load(file)

stock_art_file = {"format": "GOOD", "version": 1, "artifacts": []}
pygame.mixer.init()
pygame.mixer.music.set_volume(0.3)


def on_hotkey_pressed_logic():
    try:
        text = image2text()
        art = parse(text)

        with open(config["good_file_path"], "r") as file:
            arts_good = json.load(file)

        if art not in arts_good["artifacts"]:
            arts_good["artifacts"].append(art)
            play_sound("success")
        else:
            play_sound("repeatition")
            return

        with open(config["good_file_path"], "w") as file:
            json.dump(arts_good, file, indent=4)

    except Exception as e:
        play_sound("error")
        print(e)


class Listener:
    def __init__(self, key_pressed: bool) -> None:
        self.hotkey = ""
        self.key_pressed = key_pressed

    def on_hotkey_pressed(self):
        if not self.key_pressed:
            on_hotkey_pressed_logic()
            self.key_pressed = True

    def on_hotkey_released(self, event):
        self.key_pressed = False

    def create_bind(self, hotkey):
        self.hotkey = hotkey
        keyboard.add_hotkey(self.hotkey, self.on_hotkey_pressed)
        keyboard.on_release_key(hotkey.split("+")[-1], self.on_hotkey_released)

    def remove_bind(self):
        if self.hotkey != "":
            keyboard.remove_hotkey(self.hotkey)

    def update_bind(self, new_hotkey):
        self.remove_bind()
        self.create_bind(new_hotkey)


def play_sound(sound_type: str):
    """success, error, repeatition"""
    if sound_type == "success":
        pygame.mixer.music.load(config["sounds"]["success"])
        pygame.mixer.music.play()
    elif sound_type == "error":
        pygame.mixer.music.load(config["sounds"]["error"])
        pygame.mixer.music.play()
    elif sound_type == "repeatition":
        messagebox.showwarning("Warning", "You've already had this artifact")
    else:
        messagebox.showerror("Error", "Error")


def clear_cache():
    with open(config["good_file_path"], "w") as file:
        json.dump(stock_art_file, file, indent=4)

    for filename in os.listdir(config["screenshots_folder"]):
        file_path = os.path.join(config["screenshots_folder"], filename)
        if os.path.splitext(file_path)[1] == ".png":
            os.remove(file_path)

    with open("log.txt", "w") as file:
        file.write("")

    print("Cache cleared")


def save_file(file_path):
    try:
        shutil.copy(config["good_file_path"], file_path)
        return True
    except Exception:
        return False


def update_bind(new_bind):
    global config
    config["bind"] = new_bind
    with open("content/config.json", "r") as file:
        config = json.load(file)
    config["bind"] = new_bind
    with open("content/config.json", "w") as file:
        json.dump(config, file, indent=4)
    print(f"Bind's been changed: {new_bind}")
