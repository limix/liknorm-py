from ._ffi import ffi, lib

__all__ = ["LikNormMachine"]


class LikNormMachine(object):
    r"""Moments of ExpFam times Normal distribution.

    Example
    -------

    .. doctest::

        >>> from numpy import empty, float64
        >>> from numpy.random import RandomState
        >>> from liknorm import LikNormMachine
        >>>
        >>> machine = LikNormMachine('bernoulli')
        >>> random = RandomState(0)
        >>> outcome = random.randint(0, 2, 5)
        >>> tau = random.rand(5)
        >>> eta = random.randn(5) * tau
        >>>
        >>> log_zeroth = empty(5, dtype=float64)
        >>> mean = empty(5, dtype=float64)
        >>> variance = empty(5, dtype=float64)
        >>>
        >>> moments = {'log_zeroth': log_zeroth, 'mean': mean,
        ...            'variance': variance}
        >>> machine.moments(outcome, eta, tau, moments)
        >>>
        >>> print('%.3f %.3f %.3f' % (log_zeroth[0], mean[0], variance[0]))
        -0.671 -0.515 0.946
    """

    def __init__(self, likname, npoints=500):
        self._likname = likname
        self._machine = lib.create_machine(npoints)
        self._lik = getattr(lib, likname.upper())
        if likname.lower() == "binomial":
            self._apply = lib.apply2d
        elif likname.lower() == "nbinomial":
            self._apply = lib.apply2d
        else:
            self._apply = lib.apply1d

    def finish(self):
        lib.destroy_machine(self._machine)

    def moments(self, y, eta, tau, moments):
        r"""First three moments of ExpFam times Normal distribution.

        Parameters
        ----------
        likname : string
            Likelihood name.
        y : array_like
            Outcome.
        eta : array_like
            Inverse of the variance (1/variance).
        tau : array_like
            Mean times eta.
        moments : dict
            Log_zeroth, mean, and variance result.
        """
        size = len(moments["log_zeroth"])
        if not isinstance(y, (list, tuple)):
            y = (y,)

        y = tuple(asarray(yi) for yi in y)
        tau = asarray(tau)
        eta = asarray(eta)

        args = y + (
            tau,
            eta,
            moments["log_zeroth"],
            moments["mean"],
            moments["variance"],
        )

        self._apply(self._machine, self._lik, size, *(ptr(a) for a in args))

        if not allfinite(moments["log_zeroth"]):
            raise ValueError("Non-finite value found in _log_zeroth_.")

        if not allfinite(moments["mean"]):
            raise ValueError("Non-finite value found in _mean_.")

        if not allfinite(moments["variance"]):
            raise ValueError("Non-finite value found in _variance_.")


def asarray(seq):
    from ctypes import c_double

    tup = tuple(seq)
    return (c_double * len(tup))(*tup)


def allfinite(arr):
    return lib.allfinite(len(arr), ptr(arr)) == 1


def ptr(a):
    import ctypes

    if a.__class__.__name__ == "<cdata>":
        return a
    elif hasattr(a, "ctypes"):
        addr = a.ctypes.data
    else:
        addr = ctypes.addressof(a)

    return ffi.cast("double *", addr)
