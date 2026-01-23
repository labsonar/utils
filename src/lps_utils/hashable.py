"""HASHABLE

This module provides the class to serialize and create hashables childs.
"""
import json
import hashlib

class Hashable:
    """ Class for serializing and creating hashables childs. """

    def __hash__(self):
        cfg = self.__get_hash_base__()
        cfg_str = json.dumps(cfg, sort_keys=True, default=str)
        return int(hashlib.sha256(cfg_str.encode()).hexdigest(), 16)

    def __get_hash_base__(self):
        return {
            "class": self.__class__.__name__,
            "module": self.__class__.__module__,
            "params": self._get_params()
        }

    def _get_params(self):
        return self._serialize(self.__dict__)

    def _serialize(self, obj):
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self._serialize(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, Hashable):
            return obj.__get_hash_base__()
        else:
            return str(obj)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)
