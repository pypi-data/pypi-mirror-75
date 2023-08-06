# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import sys
import json
import dill
import shutil
import pathlib
from fnmatch import fnmatch

import numpy as np
import pandas as pd

from .memory_load import MemoryLoad
from .memory_dump import MemoryDump

from .utils import (
    _connect_key2value,
    _split_key_value,
    _reset_memory,
    _query_yes_no,
    object_hash,
    model_id,
    meta_data_name,
)

from .paths import _paths_


class Hypermemory(MemoryDump):
    def __init__(self, *args, **kwargs):
        self.memory_dict = None
        self.meta_data_found = False
        self.n_dims = None

        self.meta_path = _paths_["default"]

    def load(self):
        self._load_ = MemoryLoad(X, y, model, search_space)

        self.memory_dict = self._load_.hyperactive_memory_load()
        self.meta_data_found = self._load_.meta_data_found

        self.score_best = self._load_.score_best
        self.pos_best = self._load_.pos_best

        return self.memory_dict

    def dump(self, memory):
        self._dump_ = MemoryDump(X, y, model, search_space)
        self._dump_.hyperactive_memory_dump(memory)

    def _get_para(self):
        if self.memory_dict is None:
            print("Error")
            return
        para_pd, metrics_pd = self._dump_._get_opt_meta_data(self.memory_dict)

        return para_pd.values, np.expand_dims(metrics_pd["score"].values, axis=1)

    def get_best_model(self, X, y):
        meta_data_paths = []
        pattern = meta_data_name(X, y)

        for path, subdirs, files in os.walk(self.meta_path):
            for name in files:
                if fnmatch(name, pattern):
                    meta_data_paths.append(pathlib.PurePath(path, name))

        score_best = -np.inf

        for path in meta_data_paths:
            path = str(path)
            meta_data = pd.read_csv(path)
            scores = meta_data["_score_"].values

            # score_mean = scores.mean()
            # score_std = scores.std()
            score_max = scores.max()
            # score_min = scores.min()

            if score_max > score_best:
                score_best = score_max

                model_path = path.rsplit("dataset_id:", 1)[0]

                obj_func_path = model_path + "objective_function.pkl"
                search_space_path = model_path + "search_space.pkl"

                with open(obj_func_path, "rb") as fp:
                    obj_func = dill.load(fp)

                with open(search_space_path, "rb") as fp:
                    search_space = dill.load(fp)

                para_names = list(search_space.keys())

                best_para = meta_data[meta_data["_score_"] == score_max]
                best_para = best_para[para_names].iloc[0]

                best_para = best_para.to_dict()

            return (score_best, {obj_func: search_space}, {obj_func: best_para})

    def reset_memory(self, force_true=False):
        if force_true:
            _reset_memory(self.meta_path)
        elif _query_yes_no():
            _reset_memory(self.meta_path)

    def delete_model(self, model):
        model_hash = model_id(model)
        path = self.meta_path + "model_id:" + str(model_hash)

        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
            print("Model data successfully removed")
        else:
            print("Model data not found in memory")

    def delete_model_dataset(self, model, X, y):
        csv_file = self._get_file_path(model, X, y)

        if os.path.exists(csv_file):
            os.remove(csv_file)
            print("Model data successfully removed")
        else:
            print("Model data not found in memory")

    def connect_model_IDs(self, model1, model2):
        # do checks if search space has same dim

        with open(self.meta_path + "model_connections.json") as f:
            data = json.load(f)

        model1_hash = model_id(model1)
        model2_hash = model_id(model2)

        if model1_hash in data:
            key_model = model1_hash
            value_model = model2_hash
            data = _connect_key2value(data, key_model, value_model)
        else:
            data[model1_hash] = [model2_hash]
            print("IDs successfully connected")

        if model2_hash in data:
            key_model = model2_hash
            value_model = model1_hash
            data = _connect_key2value(data, key_model, value_model)
        else:
            data[model2_hash] = [model1_hash]
            print("IDs successfully connected")

        with open(self.meta_path + "model_connections.json", "w") as f:
            json.dump(data, f, indent=4)

    def split_model_IDs(self, model1, model2):
        # TODO: do checks if search space has same dim

        with open(self.meta_path + "model_connections.json") as f:
            data = json.load(f)

        model1_hash = model_id(model1)
        model2_hash = model_id(model2)

        if model1_hash in data:
            key_model = model1_hash
            value_model = model2_hash
            data = _split_key_value(data, key_model, value_model)
        else:
            print("IDs of models are not connected")

        if model2_hash in data:
            key_model = model2_hash
            value_model = model1_hash
            data = _split_key_value(data, key_model, value_model)
        else:
            print("IDs of models are not connected")

        with open(self.meta_path + "model_connections.json", "w") as f:
            json.dump(data, f, indent=4)

    def _get_file_path(self, model, X, y):
        func_path_ = "model_id:" + model_id(model) + "/"
        func_path = self.meta_path + func_path_

        feature_hash = object_hash(X)
        label_hash = object_hash(y)

        return func_path + (feature_hash + "_" + label_hash + "_.csv")
