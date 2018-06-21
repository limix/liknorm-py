"""
LikNorm
=======

Python wrapper around the C library LikNorm for fast integration involving
a normal distribution and an exponential-family distribution.

It exports the ``LikNormMachine`` class and the function ``test`` for testing
the package.
"""
from __future__ import absolute_import as _

from ._machine import LikNormMachine
from ._testit import test

__version__ = "1.1.5"

__all__ = ["__version__", "test", "LikNormMachine"]
