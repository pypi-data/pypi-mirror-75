from typing import Optional, Iterable
from strify.replacing.replacement import Replacement
from strify.replacing.replacer import Replacer
from strify.stringify_info import stringify_infos_into_replacements
from strify.module_storage import ModuleStorage
import strify.config as config

import inspect

__all__ = ['stringifiable']


def _get_replacements_made_by_stringify(cls) -> Iterable[Replacement]:
    storage_wrapper = ModuleStorage.from_cls(cls, config.STORE_NAME)
    replacements = storage_wrapper.storage.values()
    storage_wrapper.delete()
    return replacements


def _get_replacer(cls, stringify_infos: Optional[list]) -> Replacer:
    if not inspect.isclass(cls):
        raise TypeError(f'Class expected, get {type(cls)}')

    if stringify_infos:
        replacements = stringify_infos_into_replacements(stringify_infos)
    else:
        replacements = _get_replacements_made_by_stringify(cls)
    replacer = Replacer(replacements)
    return replacer


def stringifiable(stringify_infos: list = None, method_name: str = 'stringify'):
    def decorator(cls):
        replacer = _get_replacer(cls, stringify_infos)

        def stringify_method(self: type(cls), pattern: str) -> str:
            processed = replacer.process(self, pattern)
            return processed

        setattr(cls, method_name, stringify_method)
        return cls

    return decorator
