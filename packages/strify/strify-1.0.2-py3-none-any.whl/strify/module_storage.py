from types import ModuleType
from strify.replacing.replacement import Replacement

import sys


class ModuleStorage:
    def __init__(self, module: ModuleType, storage_name: str):
        self._module = module
        self._storage_name = storage_name

    @staticmethod
    def _get_module(module_name):
        return sys.modules[module_name]

    @classmethod
    def from_func(cls, func, storage_name):
        module = cls._get_module(func.__module__)
        return cls(module, storage_name)

    @classmethod
    def from_cls(cls, input_class, storage_name):
        module = cls._get_module(input_class.__module__)
        return cls(module, storage_name)

    @property
    def module(self):
        return self._module

    @property
    def storage(self):
        if not hasattr(self._module, self._storage_name):
            setattr(self._module, self._storage_name, {})
        storage = getattr(self._module, self._storage_name)
        return storage

    def __setitem__(self, key, value: Replacement):
        self.storage[key] = value

    def delete(self):
        delattr(self._module, self._storage_name)
