"""
Simple CLI call
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .call_base import CallBase


class CheckedCall(CallBase):
    """Used to execute shell commands and hold the execution results"""

    def __init__(self, cmd):
        """Initializes this instance with the specified command

        :param cmd: (string/list) shell command
        """
        super().__init__(cmd)
        self._logger.debug(
            'Command result:\n--- >> start output << ---\n%s\n--- >> end output << ---',
            self.get_output())

    def _run_and_get_streams(self):
        """
        :return (string, string): (stdout, stderr) strings
        """
        return tuple([stream.decode('ascii').strip() for stream in self._process.communicate()])
