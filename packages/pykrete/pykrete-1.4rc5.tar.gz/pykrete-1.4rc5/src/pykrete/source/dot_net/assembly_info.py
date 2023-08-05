"""
.Net source project's assembly info
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
from pykrete.io.file import File, ReReplacement


class AssemblyInfo:
    """.Net project's assembly info management"""

    @property
    def include(self):
        """
        :return: included artifacts, or '*' if none are defined
        """
        return self._include

    @property
    def version(self):
        """
        :return: (Version) project version
        """
        return self._version

    @version.setter
    def version(self, value):
        """Set project version

        :param value: (Version) project version
        """
        self._version = value
        self.__apply_version()

    def __init__(self, path):
        """Initialize this instance

        :param path: path to assembly info file
        """
        self._path = path
        self._file = File(path)
        self._include = self.__extract_artifacts()
        self._version = None

    def __extract_artifacts(self):
        # doesn't seem to work for MuDi.Cli!
        include = re.findall(r'\[assembly: Artifact"\(.*\)"\]', self._file.read())
        return include if include else "*"

    def __apply_version(self):
        if not self._file.update(
                lambda x: 'assembly: Assembly' in x,
                ReReplacement(r'Version\(".*?"\)', f'Version("{self._version.number_str}")')):
            raise KeyError('No assembly information found in ' + self._path)
