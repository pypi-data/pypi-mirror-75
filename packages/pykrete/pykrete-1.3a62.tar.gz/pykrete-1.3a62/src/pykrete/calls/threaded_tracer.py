"""
Stream tracer running in its own thread
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import threading


class ThreadedStreamTracer(threading.Thread):
    """Allows tracing a stream in a separate thread

    Properties:
    trace (string) - the aggregated trace
    """
    def __init__(self, source, printer, done_test, line_handler=None):
        """Initializes this instance for tracing

        :param source: (stream) the traced stream
        :param printer: (lambda x) the tracing function
        :param done_test: (lambda) the 'end-of-stream' test
        :param line_handler: (LineHandler) special lines handler
        """
        self.__source = source
        self.__printer = printer
        self.__done_test = done_test
        self.__line_handler = line_handler
        threading.Thread.__init__(self)
        self.trace = []

    def run(self):
        """Performs the trace to the end of the stream
        """
        after_blank = False
        while True:
            line = self._decode_next_line()
            if line == '':
                if self.__done_test():
                    break
                if after_blank:
                    continue
                after_blank = True
            else:
                after_blank = False
            self._trace(line, after_blank)
        self.__source.close()

    def _decode_next_line(self):
        try:
            return self.__source.readline().decode('ascii')
        except UnicodeDecodeError:
            return '<<DECODE FAILED>>'

    def _trace(self, line, after_blank):
        stripped = line.strip()
        if after_blank or not self.__line_handler or not self.__line_handler.handle(line):
            self.__printer(stripped)
        self.trace.append(stripped)
