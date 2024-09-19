import json

default_json_file = {"format": "GOOD", "version": 1, "artifacts": []}

with open("artifacts_GOOD.json", "w") as file:
    json.dump(default_json_file, file)
