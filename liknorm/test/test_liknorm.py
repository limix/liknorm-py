from numpy import asarray, empty, float64
from numpy.random import RandomState
from numpy.testing import assert_allclose, assert_equal

from liknorm import LikNormMachine


def test_sizeof_double():
    from liknorm.machine_ffi import ffi

    assert_equal(ffi.sizeof("double"), 8)


def test_alignof_double():
    from liknorm.machine_ffi import ffi

    assert_equal(ffi.alignof("double"), 8)


def test_nbinomial():
    breakpoint()
    machine = LikNormMachine("nbinomial", 500)
    random = RandomState(0)


def test_liknormmachine():
    machine = LikNormMachine("binomial", 500)
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

    machine.moments(y, ceta, ctau, {"log_zeroth": lmom0, "mean": hmu, "variance": hvar})

    assert_allclose(
        lmom0,
        [
            -3.4782483463503002,
            -6.179203e00,
            -4.473831e00,
            -5413594.18975537,
            -7.042068e00,
        ],
        atol=1e-7,
    )
    assert_allclose(
        hmu,
        [
            1.9525410876129807,
            -1.3518369482936494,
            -0.6763550778266894,
            0.1536059386302032,
            -1.4381119148114612,
        ],
        rtol=1e-5,
        atol=1e-5,
    )
    assert_allclose(
        hvar,
        [
            0.20087012833902396,
            0.12571722809509622,
            0.06619332060373984,
            0.06004980146234101,
            0.09355299409238738,
        ],
        atol=1e-7,
    )

    machine.finish()
