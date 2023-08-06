# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json


def save_json(path, name, dictionary_):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + name + ".json", "w") as f:
        json.dump(dictionary_, f, indent=4)


def load_json(path, name):
    with open(path + name + ".json", "r") as f:
        dictionary_ = json.load(f)

    return dictionary_
