"""
Command-line tool
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.patterns.common import existing_file_environment_cache
from pykrete.calls import CheckedCall


class CalledTool:
    """Manages a CLI tool whose path is detectable and cached in an environment variable
    """
    @property
    def path(self):
        """
        :return: Tool path
        """
        return self._path

    def __init__(self, tool_path_env_var, tool_path_detector, *args):
        """Initializes this instance

        :param tool_path_env_var: Environment variable caching this tool's path
        :param tool_path_detector: Method with no parameters which returns the tool's path
        :param args: (optional) parameters to pass in any call to the tool
        """
        self._path = existing_file_environment_cache(tool_path_env_var, tool_path_detector)
        self._base_call = [self._path] + list(args)

    def run(self, params, error):
        """Runs the tool with parameters, checking for success

        :param params: (str/list) call parameters
        :param error: (str) error message in case of failure
        :return: (str) tool's standard output
        """
        if isinstance(params, list):
            call = CheckedCall(self._base_call + params)
        else:
            base = " ".join(f'"{part}"' if ' ' in part else part for part in self._base_call)
            call = CheckedCall(f'{base} {str(params)}')
        call.assert_success(error)
        return call.stdout
