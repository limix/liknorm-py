from numpy import asarray, empty
from numpy.random import RandomState
from numpy.testing import assert_allclose

from liknorm import LikNormMachine


def test_liknormmachine():
    machine = LikNormMachine('binomial', 500)
    random = RandomState(0)

    ntrials = random.randint(1, 100, 5)
    nsuccesses = [random.randint(0, i + 1) for i in ntrials]

    ntrials = asarray(ntrials)
    nsuccesses = asarray(nsuccesses)

    y = (ntrials, nsuccesses)
    ceta = random.rand(5)
    ctau = random.randn(5) * ceta

    lmom0 = empty(5)
    hmu = empty(5)
    hvar = empty(5)

    machine.moments(y, ceta, ctau,
                    {'log_zeroth': lmom0,
                     'mean': hmu,
                     'variance': hvar})

    assert_allclose(lmom0, [
        -2.55989674e-12, -2.56128452e-12, -2.55787058e-12, 2.79396772e-09,
        -2.55950816e-12
    ])
    assert_allclose(hmu, [
        2.25294624e+00, 2.99693419e+00, 6.69308618e-01, 1.90604126e+07,
        3.19419728e+00
    ])
    assert_allclose(hvar, [
        5.87559282e+00, 3.78532198e+00, 1.26548506e+00, 3.35662124e+07,
        3.45096033e+00
    ])
