# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import glob
import dill
import json
import pandas as pd


def save_dataframe(path, name, _dataframe):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    _dataframe.to_csv(path + name + ".csv", index=False)


def load_dataframes(path):
    paths = glob.glob(path + "*.csv")

    dataframe_list = []
    for path in paths:
        dataframe_list.append(pd.read_csv(path))

    return dataframe_list


def save_object(path, name, _object):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + name + ".pkl", "wb") as dill_file:
        dill.dump(_object, dill_file)


def load_object(path, name):
    with open(path + name + ".pkl", "rb") as dill_file:
        _object = dill.load(dill_file)

    return _object


def save_json(path, name, dictionary_):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    with open(path + name + ".json", "w") as f:
        json.dump(dictionary_, f, indent=4)


def load_json(path, name):
    with open(path + name + ".json", "r") as f:
        dictionary_ = json.load(f)

    return dictionary_
