"""
Build modes
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from enum import Enum


class BuildMode(Enum):
    """Build modes enumeration
    """
    DEBUG = 1
    RELEASE = 2
