"""
Replacement base class
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from abc import abstractmethod


class ReplacementBase:
    """Replacement base class
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, find, replacement):
        """Initialize this instance with the specified find and replacement

        :param find: (string) search string
        :param replacement: (string) replacement string
        """
        self._find = find
        self._replacement = replacement

    def replace(self, target):
        """Perform this replacement on the specified target

        :param target: (string) replacement target string
        """
        result = self._do_replace(target)
        self._logger.debug('[%s] :: before [%s] :: after [%s]', self, target, result)
        return result

    @abstractmethod
    def _do_replace(self, target):
        pass

    def __str__(self):
        return f'find: {self._find}; replace: {self._replacement}'
