from numpy import all, ascontiguousarray, isfinite, ndarray

from ._ffi import ffi, lib


def ptr(a):
    return ffi.cast("double *", a.ctypes.data)


class LikNormMachine(object):
    def __init__(self, npoints=500):
        self._machine = lib.create_machine(npoints)

    def finish(self):
        lib.destroy_machine(self._machine)

    def moments(self, likname, y, eta, tau, log_zeroth, mean, variance):
        lik = getattr(lib, likname.upper())

        tau = ascontiguousarray(tau, float)
        eta = ascontiguousarray(eta, float)
        log_zeroth = ascontiguousarray(log_zeroth, float)
        mean = ascontiguousarray(mean, float)
        variance = ascontiguousarray(variance, float)

        size = len(log_zeroth)

        args = y + (tau, eta, log_zeroth, mean, variance)

        if likname.lower() == 'binomial':
            lib.apply2d(self._machine, lik, size, *(ptr(arg) for arg in args))
        else:
            lib.apply1d(self._machine, lik, size, *(ptr(arg) for arg in args))

        if not all(isfinite(log_zeroth)):
            raise ValueError("Non-finite value found in _log_zeroth_.")

        if not all(isfinite(mean)):
            raise ValueError("Non-finite value found in _mean_.")

        if not all(isfinite(variance)):
            raise ValueError("Non-finite value found in _variance_.")
