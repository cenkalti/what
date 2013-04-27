What
====

A helper for testing output of a process in tests.


Installing
----------

.. code-block:: bash

   $ pip install what


Usage
-----

.. code-block:: python

    >>> from what import What
    >>> w = What('echo', 'hello world')
    >>> w.expect('hello')
    'hello world'
    >>> w.expect('unicorns', timeout=1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/cenk/projects/what/what/__init__.py", line 46, in expect
        raise WhatError(self, string)
    what.WhatError:
    Expected: 'unicorns'
    Found: None
    Last 100 lines:
    ======================================================================
    hello world
    >>> w.expect_exit(0)
