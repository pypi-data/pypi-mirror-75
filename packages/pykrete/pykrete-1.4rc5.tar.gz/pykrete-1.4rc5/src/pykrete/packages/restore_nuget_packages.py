"""
Python package installation
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.tools import Externals


def restore_nuget_packages(sln_path, nuget_config=None, is_update=False):
    """Restores NuGet package
    """
    nuget = Externals().nuget(nuget_config)
    commands = ['restore'] + (['update'] if is_update else [])
    for command in commands:
        nuget.run([command, sln_path], 'failed to run nuget ' + command)
