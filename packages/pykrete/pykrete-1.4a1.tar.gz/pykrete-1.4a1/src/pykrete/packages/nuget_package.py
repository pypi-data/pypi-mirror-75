"""
Python package
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
import os
from xml.dom import minidom
from pykrete.io.file.rtf import Rtf
from pykrete.io.file import File
from pykrete.tools import Externals


class NugetPackage:
    """NuGet package
    """
    __release_notes_element = 'releaseNotes'

    @property
    def package_file(self):
        """
        :return: Path to the package file, if packed by this instance
        """
        return self._package

    def __init__(self, nuspec_path, version, source=None, nuget_config=None):
        """Initialize this intance

        :param nuspec_path: Nuspec file path
        :param version: package version
        :param source: (optional) package source
        :param nuget_config: (optional) NuGet configuration file path
        """
        self._nuspec_path = nuspec_path
        self._version = version
        self._source = source
        self._nuget = Externals().nuget(nuget_config)
        self._package = None

    def update_release_notes(self, release_notes_rtf_path):
        """Update release notes in nuspec from the specified RTF file

        :param release_notes_rtf_path: RTF file path
        """
        nuspec_doc = minidom.parse(self._nuspec_path)
        rtf_text = Rtf(release_notes_rtf_path).text.strip()
        self._replace_release_notes(nuspec_doc, rtf_text)
        File(self._nuspec_path).write_doc(nuspec_doc)

    def pack(self, is_rc):
        """Creates a NuGet package

        :param is_rc: a flag indicating this is a release-candidate package
        """
        version_name = f'{self._version.number_str_without_build}' \
                       f'{"-rc" if is_rc else "."}{self._version.build}'
        output = self._nuget.run(
            ['pack', os.path.dirname(self._nuspec_path), '-Version', version_name,
             '-properties', f'Configuration={"Debug" if is_rc else "Release"}'],
            f'Failed to pack {self._nuspec_path} [{version_name}]')
        self._package = re.findall(r'Successfully created package \'([^\']*)\'', output)[0] \
            .strip()

    def push(self):
        """Pushes the package file packed by this instance
        """
        params = ['push', self._package] + (['-Source', self._source] if self._source else [])
        self._nuget.run(params, 'Failed to push ' + self._package)

    def _replace_release_notes(self, doc, text):
        release_notes = doc.getElementsByTagName(self.__release_notes_element)[0]
        cdata = doc.createCDATASection(text)
        release_notes.replaceChild(cdata, release_notes.firstChild)
