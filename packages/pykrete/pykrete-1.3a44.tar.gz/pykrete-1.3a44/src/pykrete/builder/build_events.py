"""
Build events
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""


class BuildEvents:
    """Build events
    """

    def run_pre_build(self):
        """Runs pre-build event
        """
        self._pre_build()

    def run_post_build(self):
        """Runs post-build event
        """
        self._post_build()

    def __init__(self, pre_build=None, post_build=None):
        """Initialize this instance

        :param post_build: post-build action (optional)
        """
        self._pre_build = pre_build if pre_build else self.nothing
        self._post_build = post_build if post_build else self.nothing

    @staticmethod
    def nothing():
        """Empty action
        """
