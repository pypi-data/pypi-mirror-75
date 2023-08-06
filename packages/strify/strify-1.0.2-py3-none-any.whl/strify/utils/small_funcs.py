from typing import Union
from .types import FunctionType, MethodType

import inspect


def gets_only_one_parameter(obj: Union[FunctionType, MethodType]) -> bool:
    if inspect.isfunction(obj):
        signature = inspect.signature(obj)
    elif inspect.ismethod(obj):
        signature = inspect.signature(obj.__func__)
    else:
        raise TypeError(f'Expected {FunctionType} or {MethodType}, got {type(obj)}')
    parameters = signature.parameters
    return len(parameters) == 1
