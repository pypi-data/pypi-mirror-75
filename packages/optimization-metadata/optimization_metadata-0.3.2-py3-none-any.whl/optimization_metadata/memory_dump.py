# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json
import dill
import inspect
import random

import numpy as np
import pandas as pd

from operator import itemgetter
from .memory_io import MemoryIO
from .dataset_features import get_dataset_features
from .utils import object_hash


class MemoryDump(MemoryIO):
    def __init__(self, X, y, model, search_space):
        super().__init__(X, y, model, search_space)

    def dump_object(self, _object, path, name):
        with open(path + name, "wb") as dill_file:
            dill.dump(_object, dill_file)

    def dump_dict(self, _dict, path):
        with open(path, "w") as json_file:
            json.dump(_dict, json_file, indent=4)

    def dump_dataframe(self, _dataframe, path, name):
        if os.path.exists(path + name):
            _dataframe_old = pd.read_csv(path + name)

            assert len(_dataframe_old.columns) == len(
                _dataframe.columns
            ), "Warning meta data dimensionality does not match"

            _dataframe_final = _dataframe_old.append(_dataframe)

            columns = list(_dataframe_final.columns)
            noScore = ["_score_", "cv_default_score", "eval_time", "run"]
            columns_noScore = [c for c in columns if c not in noScore]

            _dataframe_final = _dataframe_final.drop_duplicates(subset=columns_noScore)
        else:
            _dataframe_final = _dataframe

        _dataframe_final.to_csv(path + name, index=False)

    def memory_dict2dataframe(self, memory_dict, object2hash=True):
        tuple_list = list(memory_dict.keys())
        result_list = list(memory_dict.values())

        results_df = pd.DataFrame(result_list)
        np_pos = np.array(tuple_list)

        para_dict = {}
        for i, key in zip(range(np_pos.shape[1]), self.search_space):
            np_pos_ = list(np_pos[:, i])
            search_space_list = list(self.search_space[key])

            if self.search_space_types[key] == "object" and object2hash:
                search_space_list = self.object_hash_dict[key]

            search_space_list = np.array(search_space_list)
            para_list = search_space_list[np_pos_]

            # para_list = list(itemgetter(*np_pos_)(search_space_list))
            para_dict[key] = para_list

        para_df = pd.DataFrame(para_dict)
        return pd.concat([para_df, results_df], axis=1)

    def save_dataset_info(self, path, name):
        data_features = get_dataset_features(self.X, self.y)

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        with open(path + name, "w") as f:
            json.dump(data_features, f, indent=4)

    def save_search_data(self, memory_dict, path, name):
        self._search_space_types()
        self._create_hash_list(path)
        meta_data_df = self.memory_dict2dataframe(memory_dict)

        # meta_data_df["run"] = self.datetime

        self.dump_dataframe(meta_data_df, path, name)

        print("\nMeta data saved in:\n", self.path)

    def _get_file_path(self, model_func):
        if not os.path.exists(self.date_path):
            os.makedirs(self.date_path)

        return self.model_path + self.meta_data_name

    def _search_space_types(self):
        self.search_space_types = {}
        for key in self.search_space.keys():
            search_space_list = list(self.search_space[key])

            # sampled_list = random.sample(aList, 3)

            value = search_space_list[0]

            if isinstance(value, int):
                self.search_space_types[key] = "int"
            elif isinstance(value, float):
                self.search_space_types[key] = "float"
            elif isinstance(value, str):
                self.search_space_types[key] = "str"
            else:
                self.search_space_types[key] = "object"

    def _create_hash_list(self, path):
        self.object_hash_dict = {}

        for key in self.search_space.keys():
            if self.search_space_types[key] == "object":
                search_space_list = list(self.search_space[key])

                object_hash_list = []

                for value in search_space_list:
                    para_dill = dill.dumps(value)
                    para_hash = object_hash(para_dill)

                    self.dump_object(para_dill, path, str(para_hash) + ".pkl")
                    object_hash_list.append(para_hash)

                self.object_hash_dict[key] = object_hash_list
