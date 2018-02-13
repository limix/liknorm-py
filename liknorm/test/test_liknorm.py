from liknorm import LikNormMachine
from numpy import asarray, empty, float64
from numpy.random import RandomState
from numpy.testing import assert_allclose, assert_equal


def test_sizeof_double():
    from liknorm.machine_ffi import ffi
    assert_equal(ffi.sizeof("double"), 8)


def test_alignof_double():
    from liknorm.machine_ffi import ffi
    assert_equal(ffi.alignof("double"), 8)


def test_liknormmachine():
    machine = LikNormMachine('binomial', 500)
    random = RandomState(0)

    ntrials = random.randint(1, 100, 5)
    nsuccesses = [random.randint(0, i + 1) for i in ntrials]

    ntrials = asarray(ntrials)
    nsuccesses = asarray(nsuccesses)

    y = (nsuccesses, ntrials)
    ceta = random.rand(5)
    ctau = random.randn(5) * ceta

    lmom0 = empty(5, dtype=float64)
    hmu = empty(5, dtype=float64)
    hvar = empty(5, dtype=float64)

    machine.moments(y, ceta, ctau, {
        'log_zeroth': lmom0,
        'mean': hmu,
        'variance': hvar
    })

    assert_allclose(
        lmom0, [
            -3.478250e+00, -6.179203e+00, -4.473831e+00, -6.086356e+08,
            -7.042068e+00
        ],
        atol=1e-7)
    assert_allclose(
        hmu, [
            1.952541e+00, -1.351837e+00, -6.763551e-01, 1.901923e+07,
            -1.438112e+00
        ],
        rtol=1e-5,
        atol=1e-5)
    assert_allclose(
        hvar,
        [2.008703e-01, 1.257172e-01, 6.619332e-02, 9.629856e+11, 9.355299e-02],
        atol=1e-7)

    machine.finish()
