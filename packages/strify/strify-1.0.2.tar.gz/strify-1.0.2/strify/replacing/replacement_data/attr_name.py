from strify.replacing.replacement_data.replacement_data import ReplacementData


class AttrNameReplacementData(ReplacementData):
    def __init__(self, marker_name, marker_attr):
        self._marker_name = marker_name
        self._marker_attr = marker_attr

    @property
    def marker_name(self) -> str:
        return self._marker_name

    @property
    def marker_attr(self) -> str:
        return self._marker_attr
