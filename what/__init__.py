from time import time
from threading import Thread
from Queue import Queue, Empty
from subprocess import Popen, PIPE, STDOUT

from ringbuffer import RingBuffer

__version__ = '0.2.2'


class What(Popen):
    """Adapted from: http://stackoverflow.com/a/4896288/242451"""

    def __init__(self, *args, **kwargs):
        kwargs['stdout'] = PIPE
        kwargs['stderr'] = STDOUT
        kwargs['bufsize'] = 0
        kwargs['close_fds'] = True
        super(What, self).__init__(args, **kwargs)
        self.timeout = 10
        self.queue = Queue()
        self.lines = RingBuffer(100)
        self.reader = Thread(target=self.enqueue_output)
        self.reader.daemon = True
        self.reader.start()

    def enqueue_output(self):
        for line in iter(self.stdout.readline, b''):
            line = line.rstrip('\n')
            self.queue.put(line)
            self.lines.append(line)
        self.stdout.close()

    def expect(self, string, timeout=None):
        if timeout is None:
            timeout = self.timeout

        start = time()
        try:
            while 1:
                passed = time() - start
                line = self.queue.get(timeout=timeout - passed)
                if string in line:
                    return line
        except Empty:
            raise WhatError(self, string)

    def expect_exit(self, exit_code, timeout=None):
        if timeout is None:
            timeout = self.timeout

        start = time()
        while 1:
            returncode = self.poll()
            if returncode is not None:
                break
            passed = time() - start
            if passed > timeout:
                raise WhatError(self, exit_code)

        if returncode != exit_code:
            raise WhatError(self, exit_code)


class WhatError(Exception):

    def __init__(self, what_object, expectation):
        super(WhatError, self).__init__(what_object, expectation)
        self.what = what_object
        self.expectation = expectation
        self.lines = list(what_object.lines)

    def __str__(self):
        return "\nExpected: %r\n" \
               "Found: %r\n" \
               "Last 100 lines:\n" \
               "%s\n" \
               "%s" % (
               self.expectation,
               self.what.returncode,
               "=" * 70,
               '\n'.join(self.lines))
