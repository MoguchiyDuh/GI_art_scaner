import cv2
import pyautogui
from thefuzz import process
import json
import re
from time import localtime, strftime
import pytesseract

with open("content/config.json", "r") as file:
    config = json.load(file)


def image2text() -> str:
    screen_width, screen_height = pyautogui.size()
    if (screen_width, screen_height) == (1920, 1080):
        x = int(screen_width * 0.75)
        dx = int(screen_width * 0.25)
    else:
        x = int(screen_width * 0.78)
        dx = int(screen_width * 0.22)
    y = int(screen_height * 0.1)
    dy = int(screen_height * 0.8)
    region = (x, y, dx, dy)

    formatted_time = strftime("%Y.%m.%d-%H.%M.%S", localtime())
    screenshots_folder = config["screenshots_folder"]
    path = f"{screenshots_folder}/{formatted_time}.png"
    print(path)

    pyautogui.screenshot(region=region).save(path)

    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 150, 240, cv2.THRESH_BINARY)

    try:
        text = pytesseract.image_to_string(img, lang=config["lang"])

    except pytesseract.TesseractError:
        text = pytesseract.image_to_string(img, lang="eng")
        print("special language is not found, using eng.traineddata")

    return text[: re.search(r"\(\d\)", text).start()]


def parse(text: str) -> dict:
    with open("content/arts_info.json", "r") as json_file:
        art_sets_stats = json.load(json_file)

    set_keys: list = art_sets_stats["set_keys"]
    stat_keys: dict = art_sets_stats["stat_keys"]
    slot_keys: list = art_sets_stats["slot_keys"]

    def get_stat(_line: str) -> str:
        _stat = process.extract(_line, stat_keys.keys(), limit=2)
        if _stat[0][1] == _stat[1][1] and "%" in _line:
            _stat = _stat[1][0]
        else:
            _stat = _stat[0][0]
        return stat_keys[_stat]

    # create the template
    json_art = {
        "setKey": "",
        "slotKey": "",
        "level": 20,
        "rarity": 5,
        "mainStatKey": "",
        "location": "",
        "lock": False,
        "substats": [
            {"key": "", "value": 0},
            {"key": "", "value": 0},
            {"key": "", "value": 0},
            {"key": "", "value": 0},
        ],
    }

    text = re.sub(r"[^a-zA-Z0-9%\+\.\s\n]", "", text)
    text = (
        text.replace("/0", "%")
        .replace("\n\n", "\n")
        .replace("I0", "10")
        .replace("l0", "10")
        .replace("3i", "311")
    )
    text = re.sub(r"[ \t]+", " ", text)
    formatted_time = strftime("%Y.%m.%d-%H.%M.%S", localtime())
    with open("log.txt", "a") as file:
        file.write(f"{formatted_time}\n")
        file.write(text)
        file.write("\n" + "=" * 50 + "\n")
    text = text.split("\n")

    # find slot key and delete array items before it
    indexes = []
    for index, line in enumerate(text[1:3]):
        for slot in slot_keys:
            if slot in line.lower():
                slot_choice = slot
                indexes.append(index + 1)
    text = text[indexes[-1] + 1 :]
    json_art["slotKey"] = slot_choice

    # check if the set key is 2 lines long and merge these lines
    if process.extractOne(text[-2], stat_keys.keys())[1] < 90:
        text[-2] = text[-2] + " " + text[-1]
        text.pop()

    # find set
    set_choice = process.extractOne(text[-1], set_keys)[0]
    text = text[:-1]
    json_art["setKey"] = set_choice

    # find the main stat
    if slot_choice == "flower":
        main_stat_choice = "hp"
    elif slot_choice == "plume":
        main_stat_choice = "atk"
    else:
        main_stat_choice = get_stat(text[0])
    json_art["mainStatKey"] = main_stat_choice

    # find the level
    level_choice = -1
    for line in text[:3]:
        if re.match(r"\+([0-9]|1[0-9]|20)$", line):
            level_choice = re.sub(r"[^\d]", "", line)
            text = text[text.index(line) + 1 :]
            break
    json_art["level"] = int(level_choice)

    # find substats
    substats = []
    for line in text:
        substat = {"key": "", "value": 0}
        substat["key"] = get_stat(line)
        substat["value"] = float(re.sub(r"[^\d\.]", "", line).replace("..", "."))
        substats.append(substat)
    json_art["substats"] = substats

    return json_art
