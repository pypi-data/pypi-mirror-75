"""
Text replacement class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.io.file.replacement_base import ReplacementBase


class TextReplacement(ReplacementBase):
    """Holds regular-expression text replacement request
    """

    def _do_replace(self, target):
        """Perform this replacement on the specified target

        :param target: (string) replacement target string
        """
        return target.replace(self._find, self._replacement)
