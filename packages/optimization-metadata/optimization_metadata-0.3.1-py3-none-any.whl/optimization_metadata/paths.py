# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os
import glob
import dill
import hashlib
import inspect


class HypermemoryPaths:
    def __init__(self, main_path):
        self.path_dict = {"main_path": main_path}
        self.get_id = {
            "array": self._array_id,
            "function": self._function_id,
            "dictionary": self._dictionary_id,
        }

    def _object_hash(self, object):
        return hashlib.sha1(object).hexdigest()

    def _function_string(self, function):
        return inspect.getsource(function)

    def _array_id(self, array_):
        return str(self._object_hash(array_))

    def _function_id(self, function_):
        return str(self._object_hash(self._function_string(function_).encode("utf-8")))

    def _dictionary_id(self, dictionary_):
        return str(self._object_hash(dill.dumps(dictionary_)))

    def subdirs(self, name):
        return glob.glob(self.path_dict[name] + "*/")

    def add_directory(self, name, id_type, object_, prefix="", sufix=""):
        path_new = str(prefix) + self.get_id[id_type](object_) + str(sufix) + "/"

        last_path = list(self.path_dict.values())[-1]
        self.path_dict[name] = last_path + path_new

