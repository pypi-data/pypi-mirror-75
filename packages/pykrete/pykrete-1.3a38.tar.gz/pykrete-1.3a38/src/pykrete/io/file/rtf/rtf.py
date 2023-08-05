"""
Extract text from RTF
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
from pykrete.io.file import File
from .rtf_stripper import RtfStripper


class Rtf:
    """ Read an RTF file's text contenxt
    """
    __control_chars = ''.join(map(chr, list(range(0, 9)) + list(range(14, 18)) +
                                  list(range(127, 160))))
    __control_char_re = re.compile('[%s]' % re.escape(__control_chars))

    @property
    def text(self):
        """
        :return: Text from the RTF file
        """
        return self._text

    def __init__(self, path):
        """Initialize this instance

        :param path: RTF file's path
        """
        rtf = self.__read_rtf_without_control_chars(path)
        self._text = RtfStripper(rtf).text

    def __read_rtf_without_control_chars(self, path):
        rtf = File(path).read()
        clean_rtf = self.__control_char_re.sub('', rtf)
        return clean_rtf
