# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import pytest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from optimization_metadata.memory_conv import convert_dataframe


def test_convert_dataframe1():
    array = np.reshape(np.arange(20), (10, 2))
    df1 = pd.DataFrame(array, columns=["x1", "x2"])

    search_space1 = {
        "x1": list(np.arange(20)),
        "x2": list(np.arange(20)),
    }
    search_space2 = {
        "x1": list(np.arange(20)),
        "x2": list(np.arange(20)),
    }
    df2 = convert_dataframe(df1, search_space1, search_space2)

    assert_frame_equal(df1, df2, check_dtype=False)


def test_convert_dataframe2():
    array = np.reshape(np.arange(20), (10, 2))
    df1 = pd.DataFrame(array, columns=["x1", "x2"])

    search_space1 = {
        "x1": list(np.arange(20)),
        "x2": list(np.arange(20)),
    }
    search_space2 = {
        "x1": list(np.arange(5)),
        "x2": list(np.arange(20)),
    }
    df2 = convert_dataframe(df1, search_space1, search_space2)

    with pytest.raises(Exception):
        assert_frame_equal(df1, df2, check_dtype=False)


def test_convert_dataframe3():
    array = np.reshape(np.arange(20), (10, 2))
    df1 = pd.DataFrame(array, columns=["x1", "x2"])

    search_space1 = {
        "x1": list(np.arange(20)),
        "x2": list(np.arange(20)),
    }
    search_space2 = {
        "x1": list(np.arange(20)),
        # "x2": list(np.arange(20)),
    }
    df2 = convert_dataframe(df1, search_space1, search_space2)

    df1.drop("x2", axis=1, inplace=True)

    assert_frame_equal(df1, df2, check_dtype=False)

