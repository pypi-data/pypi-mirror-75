from typing import List, Pattern
from strify.replacing.replacement import Replacement

import re

__all__ = ['Replacer']


class Replacer:
    def __init__(self, replacements):
        self.replacements: List[Replacement] = replacements

    def _get_markers_regex(self) -> Pattern:
        """
        Returns the regex that matches all the replacement markers
        :return: regex
        """
        func_markers = [x.marker for x in self.replacements]
        escaped_keys = map(lambda x: re.escape(x), func_markers)
        regex = re.compile('|'.join(escaped_keys))
        return regex

    def _get_replacement_by_match(self, match) -> Replacement:
        def marker_equal_to_match(replacement):
            nonlocal match_text
            return replacement.marker == match_text

        match_text: str = match.group(0)
        filtered = filter(marker_equal_to_match, self.replacements)
        match_replacement = list(filtered)[0]
        return match_replacement

    def process(self, instance, pattern: str) -> str:
        def get_replacement(match):
            replacement = self._get_replacement_by_match(match)
            preprocessed = replacement.get(instance)
            return preprocessed

        regex = self._get_markers_regex()
        processed_pattern = regex.sub(get_replacement, pattern)
        return processed_pattern
