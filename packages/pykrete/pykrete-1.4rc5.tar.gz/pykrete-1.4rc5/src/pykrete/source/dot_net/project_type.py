"""
.Net source project types
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from enum import Enum


class ProjectType(Enum):
    """Project type enumeration
    """

    UNKNOWN = 0
    LIBRARY = 1
    EXECUTABLE = 2
    UNIT_TEST = 3
    FLOW_TEST = 4
