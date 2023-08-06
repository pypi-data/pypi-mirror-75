# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import dill


def save_object(path, name, _object):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + name + ".pkl", "wb") as dill_file:
        dill.dump(_object, dill_file)


def load_object(path, name):
    with open(path + name + ".pkl", "rb") as dill_file:
        _object = dill.load(dill_file)

    return _object
