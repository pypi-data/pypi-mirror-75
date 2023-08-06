# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np
import pandas as pd


def intersection(lst1, lst2):
    inter = [value for value in lst1 if value in lst2]
    return inter


def convert_dataframe(dataframe1, search_space1, search_space2):
    dataframe2 = dataframe1.copy()

    for para1 in search_space1:
        if para1 not in search_space2:
            dataframe2.drop(para1, axis=1, inplace=True)
            continue

        search_elements1 = search_space1[para1]
        search_elements2 = search_space2[para1]

        inter = intersection(search_elements1, search_elements2)

        indices_A = [search_elements1.index(x) for x in inter]
        indices_B = [search_elements2.index(x) for x in inter]

        conv_dict = dict(zip(indices_A, indices_B))

        col = dataframe2[para1]
        col_conv = col.map(conv_dict)
        col_conv = col_conv.dropna(how="any")
        col_conv = col_conv.astype(int)

        dataframe2[para1] = col_conv

    dataframe2 = dataframe2.dropna(how="any", axis=0)

    return dataframe2


def memory_dict2dataframe(memory_dict, search_space):
    columns = list(search_space.keys())

    if not bool(memory_dict):
        return pd.DataFrame([], columns=columns)

    pos_tuple_list = list(memory_dict.keys())
    result_list = list(memory_dict.values())

    results_df = pd.DataFrame(result_list)
    np_pos = np.array(pos_tuple_list)

    pd_pos = pd.DataFrame(np_pos, columns=columns)
    dataframe = pd.concat([pd_pos, results_df], axis=1)

    return dataframe


def dataframe2memory_dict(dataframe, search_space):
    columns = list(search_space.keys())

    if dataframe.empty:
        return {}

    positions = dataframe[columns]
    scores = dataframe.drop(columns, axis=1)

    scores = scores.to_dict("records")
    positions_list = positions.values.tolist()

    # list of lists into list of tuples
    pos_tuple_list = list(map(tuple, positions_list))
    memory_dict = dict(zip(pos_tuple_list, scores))

    return memory_dict

