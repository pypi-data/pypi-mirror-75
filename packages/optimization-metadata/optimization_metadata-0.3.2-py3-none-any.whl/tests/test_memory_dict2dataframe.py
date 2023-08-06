# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from optimization_metadata.memory_conv import memory_dict2dataframe


def test_memory_dict2dataframe():
    search_space = {"x": list(np.arange(20)), "y": list(np.arange(20))}

    memory_dict = {
        (0, 0): {"score": 0.1, "eval_time": 0.1},
        (1, 1): {"score": 0.2, "eval_time": 0.2},
        (2, 2): {"score": 0.3, "eval_time": 0.3},
    }

    dataframe = memory_dict2dataframe(memory_dict, search_space)

    array = np.array([[0, 0, 0.1, 0.1], [1, 1, 0.2, 0.2], [2, 2, 0.3, 0.3]])
    df1 = pd.DataFrame(array, columns=["x", "y", "score", "eval_time"])
    df1 = df1[dataframe.columns]

    assert_frame_equal(df1, dataframe, check_dtype=False)
