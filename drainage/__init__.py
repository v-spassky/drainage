"""
This module declares the public API for the drainage library.

The drainage library is an implementation of UNIX-like pipes for Python.
It allows users to create pipeable functions and chain them together using
the pipe (|) operator.

Example:
    >>> from drainage import piped, filtered, collect
    >>> @piped
    ... def add_one(x):
    ...     return x + 1
    ...
    >>> @filtered
    ... def is_even(x):
    ...     return x % 2 == 0
    ...
    >>> result = [1, 2, 3, 4] | add_one | is_even | collect()
    >>> print(result)
    [2, 4]
"""

from .lib import collect, filtered, piped, reduced, take
