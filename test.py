import os
import sys
import unittest

from what import What


class WhatTestCase(unittest.TestCase):

    def test_str(self):
        w = run_program('asdf', 0, '', 0)
        line = w.expect('a', 1)
        self.assertEqual(line, 'asdf')

    def test_str_wrong(self):
        w = run_program('asdf', 0, '', 0)
        self.assertRaises(Exception, w.expect, ('x', 1))

    def test_str_timeout(self):
        w = run_program('', 1, 'zxcv', 0)
        self.assertRaises(Exception, w.expect, ('zxcv', 0))
        w.expect('zxcv', 2)

    def test_exit(self):
        w = run_program('', 0, '', 0)
        w.expect_exit(0, 1)

    def test_exit_wrong(self):
        w = run_program('', 0, '', 2)
        self.assertRaises(Exception, w.expect_exit, (0, 1))

    def test_exit_timeout(self):
        w = run_program('', 1, '', 0)
        self.assertRaises(Exception, w.expect_exit, (0, 0))
        w.expect_exit(0, 2)


def run_program(before, sleep_seconds, after, exit_code):
    return What(
        sys.executable,
        os.path.join(os.path.dirname(__file__), 'program.py'),
        before, str(sleep_seconds), after, str(exit_code))


if __name__ == '__main__':
    unittest.main()
