from strify.replacing.replacement_data.attr_name import AttrNameReplacementData
from strify.replacing.replacement import Replacement
from .utils.small_funcs import gets_only_one_parameter
from typing import Callable, List, Any


def expects_str(value: Any):
    if value is not str:
        raise TypeError(f'Expected attr_name to be {str}, but it is of type {type(value)}')


class StringifyInfo:
    __slots__ = 'marker_name', 'marker_attribute', 'preprocessing_func'

    def __init__(self, marker_name: str, marker_attribute: str = None, preprocessing_func: Callable = None):
        """
        :param marker_name: f"[{marker_name}]" is a substring to be replaced in the pattern:
               >> class_instance.stringify(pattern)
        :param marker_attribute: the above string will be replaced with:
               >> res = getattr(class_instance, attr_name)
               But:
               if res is a method, it will be called and the returned value will be used as a replacement
        :param preprocessing_func: callable that takes the value (see attr_name description),
               modifies it somehow and returns the final replacement

        Example:
        Let's define an example class':

        >>@stringifiable([
        ...    StringifyInfo('name', '_name', lambda x: x[0].upper() + x[1:].lower()),
        ...    StringifyInfo('age', '_age'),
        ...    StringifyInfo('hash', '__hash__'),
        ...])
        ...class Person:
        ...    def __init__(self, name, age):
        ...        self._name = name
        ...        self._age = age
        ...    def __hash__(self):
        ...        return hash(str(self._age) + self._name)

        And an instance of the class:
        >> john = Person('john', 27)

        If we want to stringify it, we have to use patterns like this:
        >> pattern_1 = "-- [name], how old are you?\n -- I'm [age]"
        >> pattern_2 = "[name]'s hash is [hash]"

        Let's see what we will get:
        >> john.stringify(pattern1)
        -- John, how old are you?
        -- I'm 27
        >> john.stringify(pattern2)
        John's hash is 7791988088276876325

        P.S. Notice that john.name is in lowercase, but preprocessing_func we gave as a parameter made
        the first letter uppercase
        """
        self.marker_name = marker_name
        self.marker_attribute = marker_attribute if marker_attribute else marker_name
        self.preprocessing_func = preprocessing_func

    def _check_types(self) -> None:
        expects_str(self.marker_name)
        expects_str(self.marker_attribute)
        if self.preprocessing_func:
            if callable(self.preprocessing_func):
                raise TypeError(f'Expected attr_name to be {Callable}, but it is {type(self.preprocessing_func)}')
            if not gets_only_one_parameter(self.preprocessing_func):
                raise Exception('Preprocessing function must get only 1 parameter: str to be modified')


def stringify_infos_into_replacements(stringify_infos: list) -> List[Replacement]:
    replacements = []
    for stringify_info in stringify_infos:
        replacement_data = AttrNameReplacementData(stringify_info.marker_name, stringify_info.marker_attribute)
        replacement = Replacement(replacement_data, stringify_info.preprocessing_func)
        replacements.append(replacement)
    return replacements
