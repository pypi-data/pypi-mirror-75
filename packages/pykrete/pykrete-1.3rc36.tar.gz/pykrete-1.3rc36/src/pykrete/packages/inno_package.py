"""
INNO setup management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
from pykrete.io.file import File, ReReplacement, TextReplacement
from pykrete.calls.checked_call import CheckedCall


class InnoPackage:
    """Handles Inno setup packages
    """

    _inno_path = 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'

    def __init__(self, mode, version):
        """Initializes this instance to manage the specified solution's installer

        :param mode: Package mode: debug / release
        :param version: Package version
        """
        self._mode = mode
        self._version = version

    def make_installer(self, script_path, temp_path):
        """Makes the installer exe using INNO tool

        :param script_path: INNO script path
        :param temp_path: temp folder path (holds MuDI Folder)
        :return: installer's path
        """
        File(script_path).update(lambda x: True, *self.__inno_script_replacements(temp_path))
        cmd = CheckedCall([self._inno_path, script_path,
                           f'/DConfig={self._mode.name.title()}'])
        cmd.assert_success(f'failed to make installer from {script_path}')
        setups = re.findall(r'Resulting Setup program filename is:[\s\S]*?(.*\.exe)', cmd.stdout)
        return setups[0].strip()

    def __inno_script_replacements(self, temp_path):
        return [
            ReReplacement(r'#define MyAppVersion ".*?"',
                          f'#define MyAppVersion "{self._version.number_str}"'),
            ReReplacement(r'#define MyVersionTitle ".*?"',
                          f'#define MyVersionTitle "{self._version.number_str_without_build}"'),
            TextReplacement('{#MainFolder}MuDiInstaller\\Temp\\', temp_path)
        ]
