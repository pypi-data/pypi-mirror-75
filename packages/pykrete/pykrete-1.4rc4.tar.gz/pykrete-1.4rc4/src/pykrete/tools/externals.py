"""
Packaged external tools
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
from pykrete.patterns import pykrete_root
from .called_tool import CalledTool


class Externals:
    """Wrappers for packaged external tools"""
    _nuget_environment_variable = "PYKRETE_NUGET"

    def nuget(self, config=None):
        """
        :param config: (optional) NuGet configuration file path
        :return: (CalledTool) NuGet tool wrapper
        """
        if self._nuget is None:
            if config is None:
                self._nuget = CalledTool(self._nuget_environment_variable, self._external_nuget)
            else:
                self._nuget = CalledTool(self._nuget_environment_variable, self._external_nuget,
                                         '-ConfigFile', config)
        return self._nuget

    def __init__(self):
        """Initializes this instance"""
        self._nuget = None

    def __str__(self):
        return f'Path: {self.pykrete_externals("")}'

    @staticmethod
    def pykrete_externals(filename):
        """
        :param filename: file under 'externals' folder
        :return: path to an externals file in this package's intallation folder
        """
        return os.path.join(pykrete_root(), 'externals', filename)

    def _external_nuget(self):
        nuget_exe = 'nuget.exe'
        return self.pykrete_externals(nuget_exe)
