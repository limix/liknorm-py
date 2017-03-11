from numpy import all as npall
from numpy import ascontiguousarray, isfinite

from ._ffi.lib import create_machine, destroy_machine, apply1d, apply2d


def ptr(a):
    from ._ffi import ffi
    return ffi.cast("double *", a.ctypes.data)

class LikNormMachine(object):
    def __init__(self, likname, npoints=500):
        from ._ffi import lib
        self._likname = likname
        self._machine = create_machine(npoints)
        self._lik = getattr(lib, likname.upper())
        if likname.lower() == 'binomial':
            self._apply = apply2d
        else:
            self._apply = apply1d

    def finish(self):
        destroy_machine(self._machine)

    def moments(self, y, eta, tau, moments):
        r"""First three moments of ExpFam times Normal distribution.

        Args:
            likname (string): likelihood name.
            y (array_like): outcome.
            eta (array_like): inverse of the variance (1/variance).
            tau (array_like): mean times eta.
            moments (dict): log_zeroth, mean, and variance result.
        """

        size = len(moments['log_zeroth'])

        args = y + (tau, eta, moments['log_zeroth'], moments['mean'],
                    moments['variance'])

        self._apply(self._machine, self._lik, size, *(ptr(a) for a in args))

        if not npall(isfinite(moments['log_zeroth'])):
            raise ValueError("Non-finite value found in _log_zeroth_.")

        if not npall(isfinite(moments['mean'])):
            raise ValueError("Non-finite value found in _mean_.")

        if not npall(isfinite(moments['variance'])):
            raise ValueError("Non-finite value found in _variance_.")
