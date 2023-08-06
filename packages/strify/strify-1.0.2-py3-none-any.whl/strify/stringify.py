from strify.replacing.replacement_data.func import FuncReplacementData
from strify.replacing.replacement import Replacement
from strify.module_storage import ModuleStorage
from strify.utils.types import FunctionType
import strify.config as config

import inspect

__all__ = ['stringify']


def _save_func_replacement_in_store(replacement: Replacement) -> None:
    # TODO(ekon): when python3.8 becomes usual, replace with an assigment expression
    replacement_info_class = replacement.info.__class__
    if replacement_info_class is not FuncReplacementData:
        raise TypeError(f'Got {replacement_info_class}, expected {FuncReplacementData.__name__}')

    func = replacement.info.func
    module_storage = ModuleStorage.from_func(func, config.STORE_NAME)
    func_name = func.__name__
    module_storage[func_name] = replacement


def _get_non_function_error_message(non_function):
    t = lambda x: '\t' * x
    stringify_decorator = f'@{stringify.__name__}()'
    raise TypeError(f'Expected {FunctionType}, got {type(non_function)}.\n'
                    f'{stringify_decorator} MUST get the original function as a parameter.\n'
                    f'The simplest method to handle the error is to make sure that {stringify_decorator} '
                    f'is the first decorator that\'s applied.\n'
                    f'Example:\n'
                    f'OK:{t(5)}Not OK:\n'
                    f'{t(1)}class A:{t(3)}class A:\n'
                    f'{t(2)}@property{t(3)}{stringify_decorator}\n'
                    f'{t(2)}{stringify_decorator}{t(2)}@property\n'
                    f'{t(2)}def method():{t(3)}def method():\n'
                    f'{t(3)}pass{t(5)}pass\n')


def stringify(preprocessing_func=None, marker_name: str = None):
    if preprocessing_func and not callable(preprocessing_func):
        raise TypeError(f'Preprocessing function must be callable, got type {type(preprocessing_func)}')

    def decorator(func):
        if not inspect.isfunction(func):
            error_str = _get_non_function_error_message(func)
            raise TypeError(error_str)

        replacement_data = FuncReplacementData(func, marker_name)
        replacement = Replacement(replacement_data, preprocessing_func)
        _save_func_replacement_in_store(replacement)
        return func

    return decorator
