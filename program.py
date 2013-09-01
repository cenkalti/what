"""
Sample program that is used in tests.

"""
from sys import stdout, argv, exit
from time import sleep


if __name__ == '__main__':
    stdout.write(argv[1])
    stdout.flush()
    
    sleep(int(argv[2]))
    
    stdout.write(argv[3])
    stdout.flush()
    
    exit(int(argv[4]))
