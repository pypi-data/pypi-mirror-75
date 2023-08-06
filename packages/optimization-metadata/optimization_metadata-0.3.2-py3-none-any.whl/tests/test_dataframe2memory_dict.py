# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from optimization_metadata.memory_conv import dataframe2memory_dict


def test_dataframe2memory_dict():
    search_space = {"x": list(np.arange(20)), "y": list(np.arange(20))}

    array = np.array([[0, 0, 0.1, 0.1], [1, 1, 0.2, 0.2], [2, 2, 0.3, 0.3]])
    df1 = pd.DataFrame(array, columns=["x", "y", "eval_time", "score"])

    memory_dict_new = dataframe2memory_dict(df1, search_space)

    memory_dict = {
        (0, 0): {"score": 0.1, "eval_time": 0.1},
        (1, 1): {"score": 0.2, "eval_time": 0.2},
        (2, 2): {"score": 0.3, "eval_time": 0.3},
    }

    assert memory_dict_new == memory_dict
