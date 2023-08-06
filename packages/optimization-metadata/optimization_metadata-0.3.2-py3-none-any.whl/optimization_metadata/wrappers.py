# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import dill
import datetime
import numpy as np
import pandas as pd
import hashlib
import inspect

from .paths import HypermemoryPaths
from .io_helpers import (
    save_object,
    load_object,
    save_json,
    load_json,
    save_dataframe,
    load_dataframes,
)

from .verbosity import VerbosityLVL0, VerbosityLVL1
from .dataset_features import dataset_features
from .memory_conv import memory_dict2dataframe, convert_dataframe, dataframe2memory_dict


def get_datetime():
    return datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S:%f")


class HyperactiveWrapper:
    def __init__(self, main_path, X, y, model, search_space, verbosity=1):
        self.paths = HypermemoryPaths(main_path)
        self.paths.add_directory(name="X", prefix="X_ID:", id_type="array", object_=X)
        self.paths.add_directory(name="y", prefix="y_ID:", id_type="array", object_=y)
        self.paths.add_directory(
            name="model", prefix="model_ID:", id_type="function", object_=model
        )
        self.paths.add_directory(
            name="search_space",
            prefix="search_space_ID:",
            id_type="dictionary",
            object_=search_space,
        )

        self.X = X
        self.y = y
        self.model = model
        self.search_space = search_space

        if verbosity == 0:
            self.verb = VerbosityLVL0()
        else:
            self.verb = VerbosityLVL1()

    def _drop_duplicates(self, dataframe):
        columns_drop = list(self.search_space.keys())
        return dataframe.drop_duplicates(subset=columns_drop, keep="last")

    def _load_dataframes(self):
        subdirs = self.paths.subdirs("model")

        dataframes_all = []
        for subdir in subdirs:
            search_space = load_object(path=subdir, name="search_space")
            dataframes = load_dataframes(subdir)

            for dataframe in dataframes:
                dataframe = convert_dataframe(
                    dataframe, search_space, self.search_space
                )
                dataframes_all.append(dataframe)

        return dataframes_all

    def load(self):
        self.verb.load_search_data(self.model)

        dataframes_all = self._load_dataframes()
        if len(dataframes_all) == 0:
            return {}

        dataframe = pd.concat(dataframes_all, axis=0)
        dataframe = self._drop_duplicates(dataframe)

        memory_dict = dataframe2memory_dict(dataframe, self.search_space)
        self.verb.load_search_data_success(self.model, dataframe)

        return memory_dict

    def save(self, memory_dict):
        dataframe = memory_dict2dataframe(memory_dict, self.search_space)

        if len(dataframe) == 0:
            self.verb.save_search_data_canceled(self.model)

        else:
            self.verb.save_search_data(self.model)

            X_info = dataset_features(self.X)
            y_info = dataset_features(self.y)

            io_X_path = self.paths.path_dict["X"]
            io_y_path = self.paths.path_dict["y"]
            io_model_path = self.paths.path_dict["model"]
            io_search_space_path = self.paths.path_dict["search_space"]

            save_json(io_X_path, "X_meta_data", X_info)
            save_json(io_y_path, "y_meta_data", y_info)
            save_object(io_model_path, "model", self.model)
            save_object(io_search_space_path, "search_space", self.search_space)
            save_dataframe(
                io_search_space_path, "search_data_" + str(get_datetime()), dataframe
            )

            self.verb.save_search_data_success(self.model, dataframe)

