"""
Visual studio tools
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
import os
from pykrete.calls.checked_call import CheckedCall
from pykrete.args import build_version
from .called_tool import CalledTool


class VisualStudio:
    """Microsoft Visual Studio tools wrapper
    """

    _vswhere_exe = '"%ProgramFiles(x86)%\\Microsoft Visual Studio\\Installer\\vswhere.exe"'
    _vswhere_params = ' -latest -requires Microsoft.Component.MSBuild'
    _msbuild_environment_variable = "VSTOOLS_LATEST_MSBUILD"
    _mstest_environment_variable = "VSTOOLS_LATEST_MSTEST"

    @property
    def path(self):
        """
        :return: (str) Visual Studio installation path
        """
        return self._path

    @property
    def version(self):
        """
        :return: (match) Visual Studio version used
        """
        return self._version

    @property
    def build(self):
        """
        :return: (CalledTool) MS Build tool wrapper
        """
        if self._ms_build is None:
            self._ms_build = CalledTool(self._msbuild_environment_variable, self._detect_msbuild)
        return self._ms_build

    @property
    def test(self):
        """
        :return: (CalledTool) MS Test tool wrapper
        """
        if self._ms_test is None:
            self._ms_test = CalledTool(self._mstest_environment_variable, self._detect_mstest)
        return self._ms_test

    def __init__(self):
        """Initializes this instance for the latest VS
        """
        vswhere = CheckedCall(self._vswhere_exe + self._vswhere_params)
        if not vswhere.success:
            raise SystemError('Failed to location VS installation: ' + vswhere.stderr)

        parts = dict(re.findall(r'installation(Path|Version): (.*)', vswhere.stdout))

        self._path = parts["Path"].strip()
        self._version = build_version(parts["Version"].strip()).group(1)
        self._ms_build = None
        self._ms_test = None

    def __str__(self):
        return f'Path: {self.path}; Version: {self.version}'

    def _detect_msbuild(self):
        """Gets the detected msbuild tool path

        :return: path to msbuild tool
        """
        return [path for path in
                [os.path.join(self.path, 'MSBuild', option, 'Bin', 'msbuild.exe') for option in
                 ['current', f'{self.version}.0']]
                if os.path.isfile(path)][0]

    def _detect_mstest(self):
        """Gets the detected mstest tool path, cached by an environment variable

        :return: path to mstest tool
        """
        return f'{self.path}\\Common7\\IDE\\mstest.exe'
