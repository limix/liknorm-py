import ctypes

import pytest

from liknorm import LikNormMachine


def array(x):
    seq = ctypes.c_double * len(x)
    return seq(*x)


def test_sizeof_double():
    from liknorm._ffi import ffi

    assert ffi.sizeof("double") == 8


def test_alignof_double():
    from liknorm._ffi import ffi

    assert ffi.alignof("double") == 8


def test_nbinomial():
    machine = LikNormMachine("nbinomial", 500)

    nfails = array([45, 48, 65, 68, 68])
    nsuc = array([10, 84, 22, 37, 88])

    y = (nsuc, nfails)
    ceta = array([0.891773, 0.96366276, 0.38344152, 0.79172504, 0.52889492])
    ctau = array([0.6786729, 0.11725368, 0.17019559, 0.26417832, 0.79021083])

    lmom0 = array([0] * 5)
    hmu = array([0] * 5)
    hvar = array([0] * 5)

    machine.moments(y, ceta, ctau, {"log_zeroth": lmom0, "mean": hmu, "variance": hvar})
    assert lmom0 == pytest.approx(
        [
            -6.688190743822304,
            -11.848482135668725,
            -6.320829229997251,
            -7.7975162914848495,
            -6.961932752665928,
        ]
    )
    assert hmu == pytest.approx(
        [
            -1.6079762669836217,
            -0.45726655885016254,
            -1.382021246058259,
            -1.0425380666681345,
            -0.5764620124469887,
        ]
    )
    assert hvar == pytest.approx(
        [
            0.0661209766656623,
            0.00433977357754467,
            0.0336457123502909,
            0.017150960486480127,
            0.004931267843872045,
        ]
    )


def test_liknormmachine():
    machine = LikNormMachine("binomial", 500)

    ntrials = array([45, 48, 65, 68, 68])
    nsuccesses = array([39, 9, 21, 36, 12])

    y = (nsuccesses, ntrials)
    ceta = array([0.38344152, 0.79172504, 0.52889492, 0.56804456, 0.92559664])
    ctau = array([0.17019559, 0.26417832, 0.79021083, -0.11653904, 0.28977441])

    lmom0 = array([0] * 5)
    hmu = array([0] * 5)
    hvar = array([0] * 5)

    machine.moments(y, ceta, ctau, {"log_zeroth": lmom0, "mean": hmu, "variance": hvar})

    assert lmom0 == pytest.approx(
        [
            -3.4782483463503002,
            -6.179203e00,
            -4.473831e00,
            -5413594.18975537,
            -7.042068e00,
        ],
        abs=1e-7,
        rel=1e-7,
    )
    assert hmu == pytest.approx(
        [
            1.9525410876129807,
            -1.3518369482936494,
            -0.6763550778266894,
            0.1536059386302032,
            -1.4381119148114612,
        ],
        rel=1e-5,
        abs=1e-5,
    )
    assert hvar == pytest.approx(
        [
            0.20087012833902396,
            0.12571722809509622,
            0.06619332060373984,
            0.06004980146234101,
            0.09355299409238738,
        ],
        abs=1e-7,
    )

    machine.finish()
