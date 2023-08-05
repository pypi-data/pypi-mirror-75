"""
Regex replacement class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
from pykrete.io.file.replacement_base import ReplacementBase


class ReReplacement(ReplacementBase):
    """Holds regular-expression text replacement request
    """

    def _do_replace(self, target):
        return re.sub(self._find, self._replacement, target)
