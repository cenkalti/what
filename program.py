"""
Sample program that is used in tests.

"""
import sys
from sys import argv, exit
from time import sleep


class Unbuffered(object):
    """http://stackoverflow.com/a/107717/242451"""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


if __name__ == '__main__':
    # make output unbuffered
    sys.stdout = Unbuffered(sys.stdout)

    print argv[1]
    sleep(int(argv[2]))
    print argv[3]
    exit(int(argv[4]))
