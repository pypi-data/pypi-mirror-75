# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import os
import glob
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

