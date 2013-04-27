from time import time
from threading import Thread
from Queue import Queue, Empty
from subprocess import Popen, PIPE, STDOUT

__version__ = '0.1.0'


class What(Popen):
    """Adapted from: http://stackoverflow.com/a/4896288/242451"""

    def __init__(self, *args):
        super(What, self).__init__(args, stdout=PIPE, stderr=STDOUT,
                                   bufsize=1, close_fds=True)
        self.timeout = 10
        self.queue = Queue()
        self.reader = Thread(target=self.enqueue_output)
        self.reader.daemon = True
        self.reader.start()

    def enqueue_output(self):
        for line in iter(self.stdout.readline, b''):
            self.queue.put(line)
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
                    return line.rstrip('\n')
        except Empty:
            raise Exception('Expected %r but not found' % string)

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
                raise Exception("Timeout while waiting for exit(%r)" %
                                exit_code)

        if returncode != exit_code:
            raise Exception('Expected exit(%i) but received exit(%i)' %
                            (exit_code, returncode))
