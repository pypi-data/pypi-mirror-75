"""
Handler for lines
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""


class LineHandler:
    """Handler for lines"""

    def __init__(self, matcher, handler):
        """Initialize this instance

        :param matcher: Predicate for matching lines to this handler
        :param handler: Function for handling matched lines
        """
        self._matcher = matcher
        self._handler = handler

    def handle(self, line):
        """Handle a line

        :param line: Line to handle
        :return: True if line was handled, false otherwise
        """
        if self._matcher(line):
            self._handler(line)
            return True
        return False
