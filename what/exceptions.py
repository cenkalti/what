class WhatError(Exception):
    """Base class for What exceptions."""

    def __init__(self, what_object, expected, timeout=False):
        super(WhatError, self).__init__(what_object, expected)
        self.what = what_object
        self.expectation = expected
        self.timeout = timeout
        # save output at the time of exception
        self.output = what_object.get_output()

    def __str__(self):
        return "Expectation is not met\n" \
               "Expected: %r\n" \
               "Return code: %r\n" \
               "Timed out: %r\n" \
               "%s" % (
               self.expectation,
               self.what.returncode,
               self.timeout,
               self.format_output())

    def format_output(self):
        return "Last %i lines:\n%s\n%s" % (
            self.what.BUFFER_SIZE, '='*70, self.output)


class Timeout(WhatError):
    def __init__(self, what_object, expected):
        super(Timeout, self).__init__(what_object, expected, timeout=True)


class EOF(WhatError):
    pass


class UnexpectedExit(WhatError):
    pass
