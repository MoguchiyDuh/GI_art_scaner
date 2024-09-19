import pyautogui
from pynput import keyboard
from time import localtime, strftime
import pytesseract
import cv2
from parser import parse
import os
import json


screen_width, screen_height = pyautogui.size()
x = int(screen_width * 0.78)
y = int(screen_height * 0.1)
dx = int(screen_width * 0.22)
dy = int(screen_height * 0.8)
region = (x, y, dx, dy)
folder = "./screenshots"


def image2text() -> str:
    formatted_time = strftime("%Y.%m.%d-%H.%M.%S", localtime())
    path = f"{folder}/{formatted_time}.png"
    print(path)

    pyautogui.screenshot(region=region).save(path)

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 150, 250, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(img, lang="eng")

    os.remove(path)
    return text[: text.find("(0)")]


def on_release(key):
    try:
        if key.char == "p":
            text = image2text()
            art = parse(text)

            with open("artifacts_GOOD.json", "r") as file:
                arts_good = json.load(file)
            arts_good["artifacts"].append(art)
            with open("artifacts_GOOD.json", "w") as file:
                json.dump(arts_good, file, indent=4)
        elif key.char == "o":
            print("exit")
            exit()
    except AttributeError:
        pass


if __name__ == "__main__":
    with keyboard.Listener(on_release=on_release) as listener:
        print("started")
        listener.join()
