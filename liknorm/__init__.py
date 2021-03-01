"""
LikNorm
=======

Python wrapper around the C library LikNorm for fast integration involving
a normal distribution and an exponential-family distribution.

It exports the ``LikNormMachine`` class and the function ``test`` for testing
the package.
"""
from ._machine import LikNormMachine
from ._testit import test

try:
    from ._ffi import ffi as _

    del _
except Exception as e:
    _ffi_err = """
It is likely caused by a broken installation of this package.
Please, make sure you have a C compiler and try to uninstall
and reinstall the package again."""

    raise RuntimeError(str(e) + _ffi_err)

__version__ = "1.2.5"

__all__ = ["__version__", "test", "LikNormMachine"]
