# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import json
import glob

import numpy as np
import pandas as pd

from functools import partial

from .memory_io import MemoryIO
from .utils import model_id, model_path


class MemoryLoad(MemoryIO):
    def __init__(self, X, y, model, search_space):
        super().__init__(X, y, model, search_space)

        self.pos_best = None
        self.score_best = -np.inf

        self.meta_data_found = False

        self.con_ids = []

        if not os.path.exists(self.meta_path + "model_connections.json"):
            with open(self.meta_path + "model_connections.json", "w") as f:
                json.dump({}, f, indent=4)

        with open(self.meta_path + "model_connections.json") as f:
            self.model_con = json.load(f)

        model_id_ = model_id(self.model)
        if model_id_ in self.model_con:
            self._get_id_list(self.model_con[model_id_])
        else:
            self.con_ids = [model_id_]

        self.con_ids = set(self.con_ids)

    def _get_id_list(self, id_list):
        self.con_ids = self.con_ids + id_list

        for id in id_list:
            id_list_new = self.model_con[id]

            if set(id_list_new).issubset(self.con_ids):
                continue

            self._get_id_list(id_list_new)

    def hyperactive_memory_load(self):
        para, score = self._read_func_metadata(self.model)
        if para is None or score is None:
            print("No meta data found")
            return {}

        # print(len(para), "samples found")

        # _verb_.load_samples(para)

        memory_dict = self._load_data_into_memory(para, score)
        self.n_dims = len(para.columns)

        return memory_dict

    def _read_func_metadata(self, model_func):
        paths = self._get_func_data_names()

        meta_data_list = []
        for path in paths:
            meta_data = pd.read_csv(path)
            meta_data_list.append(meta_data)
            self.meta_data_found = True

        if len(meta_data_list) > 0:
            meta_data = pd.concat(meta_data_list, ignore_index=True)

            para = meta_data[self.para_names]
            score = meta_data[self.score_col_name]

            # _verb_.load_meta_data()
            return para, score

        else:
            # _verb_.no_meta_data(model_func)
            return None, None

    def _get_func_data_names(self):
        paths = []
        for id in self.con_ids:
            paths = paths + glob.glob(
                self.meta_path + model_path(id) + self.meta_data_name
            )

        return paths

    def idx_closest_values(self, X, Y):
        dist = np.absolute(X - Y[:, np.newaxis])
        return dist.argmin(axis=1)

    def apply_index(self, pos_key, df):
        return (
            self.search_space[pos_key].index(df)
            if df in self.search_space[pos_key]
            else None
        )

    def para2pos(self, paras):
        paras = paras[self.para_names]
        pos = paras.copy()

        for pos_key in self.search_space:
            is_float = isinstance(self.search_space[pos_key][0], float)
            if is_float:
                pos[pos_key] = self.idx_closest_values(
                    self.search_space[pos_key], paras[pos_key]
                )
            else:
                apply_index = partial(self.apply_index, pos_key)
                pos[pos_key] = paras[pos_key].apply(apply_index)

        # print("\n pos \n", pos, type(pos))

        pos.dropna(how="any", inplace=True)
        pos = pos.astype("int64")

        return pos

    def _load_data_into_memory(self, paras, scores):
        # print("\n paras \n", paras, type(paras))

        paras = paras.replace(self.hash2obj)
        pos = self.para2pos(paras)

        scores_np = np.array(scores)[:, 0]
        paras_np = np.array(paras)

        print("scores_np", scores_np)

        idx = np.argmax(scores_np)
        self.score_best = scores_np[idx]
        self.pos_best = paras_np[idx]

        print("self.score_best", self.score_best)

        scores = scores.to_dict("records")
        tuple_list = list(map(tuple, pos.values))
        memory_dict = dict(zip(tuple_list, scores))

        print("Meta data successfully loaded")

        return memory_dict
