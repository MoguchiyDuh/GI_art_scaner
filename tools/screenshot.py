from time import localtime, strftime
from pynput import keyboard
import pyautogui


def take_screenshot():
    formatted_time = strftime("%Y.%m.%d-%H.%M.%S", localtime())
    path = f"screenshots/{formatted_time}.png"
    print(path)
    screen_width, screen_height = pyautogui.size()
    x = int(screen_width * 0.78)
    y = int(screen_height * 0.1)
    dx = int(screen_width * 0.22)
    dy = int(screen_height * 0.8)
    region = (x, y, dx, dy)
    pyautogui.screenshot(region=region).save(path)


def on_release(key):
    try:
        if key.char == "p":
            take_screenshot()
        elif key.char == "o":
            print("exit")
            exit()
    except AttributeError:
        pass


if __name__ == "__main__":
    with keyboard.Listener(on_release=on_release) as listener:
        print("started")
        listener.join()
