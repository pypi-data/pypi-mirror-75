"""
Pykrete tools tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import unittest
from pykrete.tools import VisualStudio, Externals


class PykreteToolsTestCase(unittest.TestCase):
    """Unit tests pykrete's tools
    """

    _logger = logging.getLogger(__name__)

    def test_visual_studio(self):
        """Verify creation and basic usage of the VisualStudio tool set
        """
        visual_studio = VisualStudio()
        self._logger.info(visual_studio)
        self._logger.info(visual_studio.build.path)
        self._logger.info(visual_studio.build.run('-version', 'failed to get msbuild version'))
        self._logger.info(visual_studio.test.path)
        self._logger.info(visual_studio.test.run('/help', 'failed to get mstest help'))

    def test_externals(self):
        """Verify creation and basic usage of the VisualStudio tool set
        """
        externals = Externals()
        self._logger.info(externals)
        nuget = externals.nuget()
        self._logger.info(nuget.path)
        self._logger.info(nuget.run('help', 'failed to get nuget help'))
