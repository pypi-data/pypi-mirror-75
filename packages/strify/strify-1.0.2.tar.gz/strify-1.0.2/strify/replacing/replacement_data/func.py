from strify.replacing.replacement_data.replacement_data import ReplacementData


class FuncReplacementData(ReplacementData):
    def __init__(self, func, marker_name: str = None):
        self.func = func
        self._marker_name = marker_name or func.__name__

    @property
    def marker_name(self) -> str:
        return self._marker_name

    @property
    def marker_attr(self) -> str:
        return self.func.__name__
