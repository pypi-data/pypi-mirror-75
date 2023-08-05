"""
Pykrete file tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import unittest
import logging
import os
from pykrete.io.file import File, ReReplacement, TextReplacement


class TestFile(unittest.TestCase):
    """Unit tests for the File and ReReplacement classes
    """
    _logger = logging.getLogger(__name__)
    _base_path = os.path.join('src', 'pykrete', 'tests', 'src')
    _temp_path = os.path.join(_base_path, 'temp.txt')

    def test_text_replacement(self):
        """Verify text replacement
        """
        contents = 'ROMANES EUNT DOMUS'
        expected = 'ROMANI ITE DOMUM'
        rep1 = TextReplacement('ROMANES', 'ROMANI')
        rep2 = TextReplacement('EUNT', 'ITE')
        rep3 = TextReplacement('DOMUS', 'DOMUM')
        self._logger.debug(contents)
        File(self._temp_path).write(contents)
        File(self._temp_path).update(lambda x: True, rep1, rep2, rep3)
        self._logger.debug(File(self._temp_path).read())
        self.assertEqual(expected, File(self._temp_path).read(), "text replacement failed")

    def test_regex_replacement(self):
        """Verify regex replacement
        """
        contents = 'I didn\'t expect the Spanish Inquisition!'
        expected = 'No one expects the Spanish Inquisition!'
        rep1 = ReReplacement(r'I .*?t', 'No one')
        rep2 = ReReplacement(r'e\S*t', 'expects')
        File(self._temp_path).write(contents)
        File(self._temp_path).update(lambda x: True, rep1, rep2)
        self.assertEqual(expected, File(self._temp_path).read(), "text replacement failed")

    def test_recurring_unchanged_replacement(self):
        """Verify that pairs of mirror changes leave the file as was
        """
        contents = File(os.path.join(self._base_path, 'AssemblyInfo.cs')).read()
        self._logger.debug(contents)
        rep_to = ReReplacement(r'"99.99.99.99"', '"1.2.3.4"')
        rep_from = ReReplacement(r'"1.2.3.4"', '"99.99.99.99"')
        File(self._temp_path).write(contents)
        for i in range(1, 10):
            self._logger.debug(i)
            File(self._temp_path).update(lambda x: True, rep_to, rep_from)
        self.assertEqual(contents, File(self._temp_path).read(), "contents differ")


if __name__ == '__main__':
    unittest.main()
