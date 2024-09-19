from bs4 import BeautifulSoup
import re
import json

with open("tools/art_sets.html", "r") as html_file:
    html = html_file.read()

soup = BeautifulSoup(html, "html.parser")

name_divs = soup.find_all("div", class_="name")
set_names: dict[str] = [div.get_text() for div in name_divs]

set_keys = []
for set_name in set_names:
    set_name = set_name.replace("-", " ")
    set_name = re.sub(r"[^a-zA-Z0-9\s]", "", set_name)
    set_key = "".join([_.capitalize() for _ in set_name.split(" ")])
    set_keys.append(set_key)

set_dict = {"set_keys": set_keys}
with open("./art_sets_stats.json", "r") as json_file:
    art_sets_stats = json.load(json_file)
    art_sets_stats["set_keys"] = set_keys
with open("./art_sets_stats.json", "w") as json_file:
    json.dump(art_sets_stats, json_file, indent=4)
