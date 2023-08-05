"""
Traced CLI call
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .call_base import CallBase
from .threaded_tracer import ThreadedStreamTracer


class TracedCall(CallBase):
    """Used to execute shell commands and hold the execution results while tracing to log
    """

    def _run_and_get_streams(self):
        """Traces prints from the process' stdout and stderr using threaded tracers, returning the
         aggregated results

        :return (string, string): (stdout, stderr) strings
        """
        tracers = [ThreadedStreamTracer(self._process.stdout, self._logger.info, self.__done_test),
                   ThreadedStreamTracer(self._process.stderr, self._logger.error, self.__done_test)]
        for tracer in tracers:
            tracer.start()
        for tracer in tracers:
            tracer.join()
        return tuple(['\n'.join(tracer.trace) for tracer in tracers])

    def __done_test(self):
        """Tests if the process has ended

        :return: True if process ended, false otherwise
        """
        return self._process.poll() is not None
