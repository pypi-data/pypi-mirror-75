from typing import Union, Callable
from strify.replacing.replacement_data import FuncReplacementData, AttrNameReplacementData


class Replacement:
    def __init__(
            self,
            replacement_info: Union[FuncReplacementData, AttrNameReplacementData],
            preprocessing_func: Callable
    ):
        self.info = replacement_info
        self.preprocessing_func = preprocessing_func

    @property
    def marker(self) -> str:
        return f'[{self.info.marker_name}]'

    def get(self, instance) -> str:
        res = self.info.get(instance)
        if self.preprocessing_func:
            res = self.preprocessing_func(res)
        return str(res)
