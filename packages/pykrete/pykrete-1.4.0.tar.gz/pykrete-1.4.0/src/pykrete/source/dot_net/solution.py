"""
.Net source solution
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
import re
from pykrete.args import exiting_file
from pykrete.io.file import File
from .project import Project


class Solution:
    """Handle a source-code solution

        Properties:
        path (string): the solution file's path
        projects ([SourceProject]): a vector of projects in the solution
    """

    @property
    def path(self):
        """
        :return: (string) the solution file's path
        """
        return self._path

    @property
    def projects(self):
        """
        :return: [Project] a list of projects in the solution
        """
        return self._projects

    def __init__(self, path):
        """Initializes this instance

        :param path: solution's path
        """
        self._path = exiting_file(path)
        self._projects = self.__locate_projects()

    def __locate_projects(self):
        """Extracts project paths from the relevant line in the solution file"""
        return [Project(os.path.join(os.path.dirname(self.path), path)) for
                path in re.findall(r'Project.*?FAE04EC0.*?, "([^"]+?)"', File(self.path).read())]
