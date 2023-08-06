# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


def dataset_features(array):
    return {
        "array_size": array.size,
        "array_byte_size": array.itemsize,
        "array_ndim": array.ndim,
    }

