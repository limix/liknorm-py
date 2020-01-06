try:
    from ._ffi import ffi, lib
    from ._ffi.lib import apply1d, apply2d, create_machine, destroy_machine
except ImportError as e:
    msg = "\nIt is likely caused by a broken installation of this package."
    msg += "\nPlease, make sure you have a C compiler and try to uninstall"
    msg += "\nand reinstall the package again."
    raise ImportError(str(e) + msg)


def ptr(a):
    return ffi.cast("double *", a.ctypes.data)


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
        self._machine = create_machine(npoints)
        self._lik = getattr(lib, likname.upper())
        if likname.lower() == "binomial":
            self._apply = apply2d
        elif likname.lower() == "nbinomial":
            self._apply = apply2d
        else:
            self._apply = apply1d

    def finish(self):
        destroy_machine(self._machine)

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
        from numpy import all as npall
        from numpy import asarray, float64, isfinite

        size = len(moments["log_zeroth"])
        if not isinstance(y, (list, tuple)):
            y = (y,)

        y = tuple(asarray(yi, float64) for yi in y)
        tau = asarray(tau, float64)
        eta = asarray(eta, float64)

        args = y + (
            tau,
            eta,
            moments["log_zeroth"],
            moments["mean"],
            moments["variance"],
        )

        self._apply(self._machine, self._lik, size, *(ptr(a) for a in args))

        if not npall(isfinite(moments["log_zeroth"])):
            raise ValueError("Non-finite value found in _log_zeroth_.")

        if not npall(isfinite(moments["mean"])):
            raise ValueError("Non-finite value found in _mean_.")

        if not npall(isfinite(moments["variance"])):
            raise ValueError("Non-finite value found in _variance_.")
