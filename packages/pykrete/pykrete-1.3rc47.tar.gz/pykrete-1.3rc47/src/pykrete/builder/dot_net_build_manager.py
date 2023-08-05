"""
.NET build manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
import shutil
import logging
from pykrete.versioning import Version
from pykrete.source.dot_net import Solution, ProjectType
from pykrete.packages import restore_nuget_packages
from pykrete.args import environ, BuildMode
from pykrete.tools import VisualStudio
from pykrete.calls import CheckedCall
from .build_manager import BuildManager


class DotNetBuildManager(BuildManager):
    """Manages building a python package"""

    BINARIES = os.path.abspath('binaries')
    _logger = logging.getLogger(__name__)

    @property
    def mode(self):
        """
        :return: (BuildMode) the build mode used, or None if not built yet
        """
        return self._mode

    def __init__(self, version: Version, build_events=None, release_notes=None):
        """Initialize this instance

        :param version: Build version
        :param release_notes: (dict) release notes per nuspec (use * for default)
        """
        super().__init__(version, build_events)
        self._solution = Solution(self._project)
        self._release_notes = release_notes if release_notes else {}
        self._nuget_config = environ('NUGET_CONFIG')
        self._nuget_source = environ('NUGET_SOURCE')
        self._mode = None

    def _clean_distribution(self):
        """Removes previous distribution files"""
        self._logger.debug('Deleting previous distribution')
        shutil.rmtree('binaries', ignore_errors=True)

    def _set_package_version(self):
        """Sets the package version in the project's version file"""
        print(f'Updating {self._project} projects\' version to {self._version}:')
        for project in self._solution.projects:
            project.assembly_info.version = self._version
            print(f' - updated {project}')

    def _build(self):
        """Performs the actual build"""
        self._logger.debug('Building %s', self._project)
        restore_nuget_packages(self._project, self._nuget_config)
        self._run_msbuild()
        self._extract_artifacts()

    def _run_msbuild(self):
        self._mode = BuildMode.RELEASE if self._is_release else BuildMode.DEBUG
        is_multi_threaded = environ('MSBUILD_MULTITHREADED') is not None
        VisualStudio().build.run(
            [f'{self._project}', '/t:Clean,ReBuild', f'/p:Configuration={self._mode.name.title()}']
            + (['/m'] if is_multi_threaded else []),
            'failed to build ' + self._project)

    def _extract_artifacts(self):
        mode = BuildMode.RELEASE if self._is_release else BuildMode.DEBUG
        relevant_projects = [project for project in self._solution.projects
                             if project.type != ProjectType.LIBRARY]
        for project in relevant_projects:
            project.extract_artifacts(self.BINARIES, mode)

    def _upload(self):
        """Uploads the package
        """
        self._logger.debug('Uploading %s', self._project)
        for nuget in self._pack_nugets():
            nuget.push()

    def _pack_nugets(self):
        default_notes = self._release_notes.get('*', None)
        nugets = []
        for project in self._solution.projects:
            nuget = project.create_nuget_package_manager(self._nuget_source, self._nuget_config)
            if nuget:
                self._pack_nuget(default_notes, nuget, project)
                nugets.append(nuget)
        return nugets

    def _pack_nuget(self, default_notes, nuget, project):
        project.set_default_mode(BuildMode.RELEASE if self._is_release else BuildMode.DEBUG)
        notes = self._release_notes.get(project.name, default_notes)
        if notes:
            nuget.update_release_notes(notes)
        nuget.pack(not self._is_release)
        CheckedCall(
            ['xcopy', f'{nuget.package_file}', f'{os.path.join(self.BINARIES, "nuget", "")}',
             '/E', '/I', '/Y', '/F']) \
            .assert_success(f'Failed while copying {nuget.package_file}')
