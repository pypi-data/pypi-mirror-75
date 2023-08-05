"""
Pykrete NuGet tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import unittest
import os
from pykrete.packages.nuget_package import NugetPackage
from pykrete.io.file import File


class TestNuget(unittest.TestCase):
    """Unit tests for handling NuGet packages
    """
    _base_path = os.path.join('src', 'pykrete', 'tests', 'src')

    def test_update_release_notes(self):
        """Verifies that updating release notes succeeds
        """
        nuspec_path = os.path.join(self._base_path, 'some.nuspec')
        rtf_path = os.path.join(self._base_path, 'Notes.rtf')
        package = NugetPackage(nuspec_path, None)
        package.update_release_notes(rtf_path)
        self.assertTrue('A newt?' in File(nuspec_path).read(),
                        'Release notes not pasted into nuspec')


if __name__ == '__main__':
    unittest.main()
