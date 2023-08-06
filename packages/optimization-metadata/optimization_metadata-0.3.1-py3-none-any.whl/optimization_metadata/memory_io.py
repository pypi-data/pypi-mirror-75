# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os

from .utils import get_datetime, model_id, _hash2obj
from .utils import (
    model_path,
    date_path,
    meta_data_name,
)

from .paths import _paths_


class MemoryIO:
    def __init__(self, *args, **kwargs):
        self.X = X
        self.y = y
        self.model = model
        self.search_space = search_space

        self.para_names = list(self.search_space.keys())

        self.meta_data_name = meta_data_name(X, y)
        self.score_col_name = ["score", "eval_time"]

        model_id_ = model_id(model)
        self.datetime = get_datetime()

        self.meta_path = _paths_["default"]
        self.model_path = self.meta_path + model_path(model_id_)
        self.date_path = self.model_path + date_path(self.datetime)

        self.dataset_info_path = self.model_path + "dataset_info/"

        if not os.path.exists(self.date_path):
            os.makedirs(self.date_path, exist_ok=True)

        self.hash2obj = _hash2obj(search_space, self.model_path)
