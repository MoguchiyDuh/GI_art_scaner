from thefuzz import fuzz, process
import json
import re


with open("art_sets_stats.json", "r") as json_file:
    art_sets_stats = json.load(json_file)

set_keys: list = art_sets_stats["set_keys"]
stat_keys: dict = art_sets_stats["stat_keys"]
slot_keys: dict = art_sets_stats["slot_keys"]


def get_stat(_line):
    _stat = process.extract(_line, stat_keys.keys(), limit=2)
    if _stat[0][1] == _stat[1][1] and "%" in _line:
        _stat = _stat[1][0]
    else:
        _stat = _stat[0][0]
    return stat_keys[_stat]


def parse(text):
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
    text = text.replace("/0", "%").replace("\n\n", "\n")
    text = re.sub(r"[ \t]+", " ", text).split("\n")

    # find slot key and delete array items before it
    for line in text[1:3]:
        slot_choice = process.extractOne(line, slot_keys.keys())
        if slot_choice[1] > 85:
            text = text[text.index(line) + 1 :]
            slot_choice = slot_keys[slot_choice[0]]
            break
    print(slot_choice)
    json_art["slotKey"] = slot_choice

    # check if the set key is 2 lines long and merge these lines
    if process.extractOne(text[-2], stat_keys)[1] < 90:
        text[-2] = text[-2] + " " + text[-1]
        text.pop()

    set_choice = process.extractOne(text[-1], set_keys)[0]
    text = text[:-1]
    print(set_choice)
    json_art["setKey"] = set_choice

    # find the main stat
    if slot_choice == "flower":
        main_stat_choice = "hp"
    elif slot_choice == "plume":
        main_stat_choice = "atk"
    else:
        main_stat_choice = get_stat(text[0])
    print(main_stat_choice)
    json_art["mainStatKey"] = main_stat_choice

    # find the level
    for line in text[:3]:
        if re.match(r"^([0-9]|1[0-9]|20)$", line):
            level_choice = re.sub(r"[^\d]", "", line)
            text = text[text.index(line) + 1 :]
            break
    print(level_choice)
    json_art["level"] = level_choice

    # there should be only substats
    substats = []
    for line in text:
        substat = {"key": "", "value": 0}
        substat["key"] = get_stat(line)
        substat["value"] = float(re.sub(r"[^\d\.]", "", line))
        substats.append(substat)
    print(substats)
    json_art["substats"] = substats

    print(json_art)
    return json_art
