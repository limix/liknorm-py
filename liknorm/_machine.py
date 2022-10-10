from ._ffi import ffi, lib

__all__ = ["LikNormMachine"]


class LikNormMachine(object):
    r"""Moments of ExpFam times Normal distribution.

    Parameters
    ----------
    likname : string
        Likelihood name.

    Example
    -------

    .. doctest::

        >>> import ctypes
        >>> from liknorm import LikNormMachine
        >>>
        >>> def array(x):
        ...     seq = ctypes.c_double * len(x)
        ...     return seq(*x)
        >>>
        >>> machine = LikNormMachine('bernoulli')
        >>> outcome = array([0, 1, 1, 0, 1])
        >>> tau = array([0.85794562, 0.84725174, 0.6235637, 0.38438171, 0.29753461])
        >>> eta = array([-0.04721714, -0.09091897, 0.85145577, -0.03755245, -0.72180545])
        >>>
        >>> log_zeroth = array([0] * 5)
        >>> mean = array([0] * 5)
        >>> variance = array([0] * 5)
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
        y : array_like
            Outcome.
        eta : array_like
            Mean times tau.
        tau : array_like
            Inverse of the variance (1/variance).
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
