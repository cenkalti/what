from __future__ import absolute_import

from time import time
from threading import Thread
from subprocess import Popen, PIPE, STDOUT

from .six import PY3
from .six.moves import queue
from .ringbuffer import RingBuffer
from .exceptions import Timeout, EOF, UnexpectedExit

__version__ = '0.5.0'


class What(Popen):
    """
    Wrapper around subprocess.Popen that has additional methods for checking
    process output and return code.

    Inspired by the solution from J.F. Sebastian.
    Source: http://stackoverflow.com/a/4896288/242451

    """
    BUFFER_SIZE = 100

    def __init__(self, *args, **kwargs):
        """
        Both args and kwargs will be passed to Popen constructor.

        """
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = STDOUT
        kwargs['bufsize'] = 0
        kwargs['close_fds'] = True
        super(What, self).__init__(args, **kwargs)
        self.timeout = 10
        self.queue = queue.Queue(self.BUFFER_SIZE)
        self.lines = RingBuffer(self.BUFFER_SIZE)
        self.reader = Thread(target=self._enqueue_output)
        self.reader.daemon = True
        self.reader.start()

    def expect(self, string, timeout=None):
        """
        Expect a string in output. If timeout is given and expected string
        is not found before timeout Timeout will be raised. If end of the file
        is reached while waiting for string EOF will be raised.

        If timeout is None, self.timeout is going to be used as a value.

        """
        if timeout is None:
            timeout = self.timeout

        start = time()
        try:
            while 1:
                passed = time() - start
                get_timeout = timeout - passed
                if get_timeout < 0:
                    raise Timeout(self, string)

                line = self.queue.get(timeout=get_timeout)
                if line is EOF:
                    self.wait()
                    raise EOF(self, string)

                if string in line:
                    return line
        except queue.Empty:
            raise Timeout(self, string)

    def expect_exit(self, exit_code=None, timeout=None):
        """
        Expect process to exit with specified exit code.

        If timeout is None, self.timeout is going to be used as a value.

        """
        if timeout is None:
            timeout = self.timeout

        start = time()
        while 1:
            returncode = self.poll()
            if returncode is not None:
                break
            passed = time() - start
            if passed > timeout:
                raise Timeout(self, exit_code)

        if exit_code is not None and returncode != exit_code:
            raise UnexpectedExit(self, exit_code)

        self.wait()

    def get_output(self):
        """Return lines read in the read buffer."""
        return '\n'.join(self.lines)

    def _enqueue_output(self):
        """Thread target of self.reader."""
        for line in iter(self.stdout.readline, b''):
            if PY3:
                line = line.decode('utf-8')
            line = line.rstrip('\n')
            self.queue.put(line)
            self.lines.append(line)
        self.queue.put(EOF)
        self.stdout.close()
