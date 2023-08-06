from abc import ABC, abstractmethod
from strify.utils.small_funcs import gets_only_one_parameter
from typing import Any

import inspect


class ReplacementData(ABC):

    @property
    @abstractmethod
    def marker_name(self) -> str:
        pass

    @property
    @abstractmethod
    def marker_attr(self) -> str:
        pass

    def get(self, instance) -> Any:
        attr = getattr(instance, self.marker_attr)

        if inspect.ismethod(attr):
            if gets_only_one_parameter(attr):
                result = attr()
            else:
                raise Exception("Can't stringify a function that takes anything but self")
        else:
            result = attr

        return result
