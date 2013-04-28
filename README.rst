What
====

A helper for testing output of a process in tests.


Installing
----------

.. code-block:: bash

   $ pip install what


Usage
-----

.. code-block:: pycon

    >>> from what import What
    >>> w = What('echo', 'hello world')
    >>> w.expect('hello')
    'hello world'
    >>> w.expect('unicorns', timeout=1)
    >>> # ... tracback here ...
    what.exceptions.EOF: End of file is reached while expecting string
    Expected: unicorns
    Return code: 0
    Timed out: False
    Last 100 lines:
    ======================================================================
    hello world
    >>> w.expect_exit(0)
