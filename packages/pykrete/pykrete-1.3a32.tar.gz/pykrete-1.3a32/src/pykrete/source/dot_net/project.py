"""
.Net source project
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
import re
import logging
from pykrete.args import exiting_file
from pykrete.io.file import File
from pykrete.patterns import first_or_error
from pykrete.packages import NugetPackage
from pykrete.calls import CheckedCall
from .project_type import ProjectType
from .assembly_info import AssemblyInfo


class Project:
    """Handle source-code projects in a solution
    """

    __test_project_type_guid = '3AC096D0-A1C2-E12C-1390-A8335801FDAB'
    _logger = logging.getLogger(__name__)

    @property
    def path(self):
        """
        :return: (string) the project's path
        """
        return self._path

    @property
    def directory(self):
        """
        :return: (string) the project's directory
        """
        return os.path.dirname(self._path)

    @property
    def name(self):
        """
        :return: (string) the project's name
        """
        return self._name

    @property
    def type(self):
        """
        :return: (ProjectType) the project's type
        """
        return self._type

    @property
    def assembly_info(self):
        """
        :return: (AssemblyInfo) the project's assembly info
        """
        return self._assembly_info

    def __init__(self, path):
        """Initializes this instance

        :param path: project's path
        """
        self._path = exiting_file(path)
        self.__file = File(path)
        self.__file.read_contents()
        self._name = self.__locate_name()
        self._type = self.__locate_type()
        self._output = self.__locate_output()
        self._assembly_info = self.__locate_assembly_info()
        self._nuspec = self.__locate_nuspec()
        self.__file.forget_contents()

    def create_nuget_package_manager(self, source=None, nuget_config=None):
        """Creates a nuget package manager for this project, if it has a nuspec in it

        :param source: NuGet source (optional)
        :param nuget_config: NuGet config path (optional)
        :return: (NugetPackage) nuget package manager, or None if no nuspec is present
        """
        return NugetPackage(self._nuspec, self._assembly_info.version, source, nuget_config) \
            if self._nuspec else None

    def __str__(self):
        """Returns a string representation of this object

        :return: a string representation of this object
        """
        return f'{self.name} [{self.directory}]'

    def extract_artifacts(self, destination, mode):
        """Extracts artifacts from the project's output

        :param destination: path into which artifacts are extracted
        :param mode: build mode of the artifacts
        """
        action_str = f'Copying artifacts from {self._name} [{self._assembly_info.include}]'
        self._logger.debug(action_str)
        CheckedCall(
            ['xcopy',
             f'{os.path.join(self._output[mode.name.title()], self._assembly_info.include)}',
             f'{os.path.join(destination, self._type.name, self._name, "")}',
             '/E', '/I', '/Y', '/F']) \
            .assert_success(f'Failed while {action_str}')

    def __locate_name(self):
        return first_or_error(re.findall(r'<AssemblyName>(.*?)</', self.__file.get_contents()),
                              'AssemblyName not found in ' + self.path)

    def __locate_type(self):
        output_type = re.findall(r'<OutputType>(.+?)</OutputType>', self.__file.get_contents())[0]
        if output_type == "Library":
            if self.__test_project_type_guid in self.__file.get_contents():
                return ProjectType.UNIT_TEST
            if self.name.endswith("Tests") or self.name.endswith("Test"):
                return ProjectType.FLOW_TEST
            return ProjectType.LIBRARY
        if output_type.endswith("Exe"):
            return ProjectType.EXECUTABLE
        return ProjectType.UNKNOWN

    def __locate_output(self):
        mode_and_out_path = re.findall(
            r'<PropertyGroup Condition=" \'\$\(C.+?\)\|.+?\)\'.+_?\'(.+?)\|[\s\S]+?'
            r'<OutputPath>(.+?)<', self.__file.get_contents())
        return {mode: os.path.join(self.directory, out_path)
                for (mode, out_path) in mode_and_out_path}

    def __locate_assembly_info(self):
        return AssemblyInfo(
            os.path.join(
                self.directory,
                first_or_error(
                    re.findall(r'<Compile Include="(.*AssemblyInfo\.cs)"',
                               self.__file.get_contents()),
                    'AssemblyInfo not found in ' + self.path)))

    def __locate_nuspec(self):
        nuspecs = [f for f in os.listdir(self.directory) if f.endswith('.nuspec')]
        return os.path.join(self.directory, nuspecs[0]) if nuspecs else None
