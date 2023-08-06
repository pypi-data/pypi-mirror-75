# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import numpy as np

from optimization_metadata import HyperactiveWrapper
from sklearn.datasets import load_iris


def test_():
    data = load_iris()
    X, y = data.data, data.target

    def himmelblau(para):
        return -(
            (para["x"] ** 2 + para["y"] - 11) ** 2
            + (para["x"] + para["y"] ** 2 - 7) ** 2
        )

    x_range = list(np.arange(0, 10, 0.1))
    search_space = {"x": x_range, "y": x_range}

    memory_dict = {
        (0, 0): {"score": 0.1, "eval_time": 0.1},
        (1, 1): {"score": 0.2, "eval_time": 0.2},
        (2, 2): {"score": 0.3, "eval_time": 0.3},
    }

    mem = HyperactiveWrapper(
        "./", X=X, y=y, model=himmelblau, search_space=search_space
    )
    mem.save(memory_dict)
    memory_dict_new = mem.load()

    assert memory_dict == memory_dict_new

