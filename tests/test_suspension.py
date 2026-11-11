import math

import pytest

from suspension import (ride_frequency, spring_index, spring_rate,
                        spring_shear_stress, static_sag, wahl_factor, wheel_rate)


def test_spring_rate_known_value():
    # d=12 mm, D=100 mm, 8 active coils, G=79.3 GPa -> about 25.7 N/mm
    k = spring_rate(0.012, 0.100, 8)
    assert k == pytest.approx(79.3e9 * 0.012**4 / (8 * 0.1**3 * 8))
    assert k / 1000 == pytest.approx(25.69, rel=1e-3)


def test_rate_scales_with_d4_and_inverse_coils():
    base = spring_rate(0.012, 0.1, 8)
    assert spring_rate(0.024, 0.1, 8) == pytest.approx(16 * base)
    assert spring_rate(0.012, 0.1, 4) == pytest.approx(2 * base)


def test_wahl_factor_c_8():
    assert wahl_factor(8) == pytest.approx(31 / 28 + 0.615 / 8)  # about 1.184


def test_shear_stress():
    c = spring_index(0.012, 0.1)
    expected = wahl_factor(c) * 8 * 4000 * 0.1 / (math.pi * 0.012**3)
    assert spring_shear_stress(4000, 0.012, 0.1) == pytest.approx(expected)


def test_wheel_rate_motion_ratio():
    assert wheel_rate(50_000, 0.7) == pytest.approx(24_500)


def test_ride_frequency_typical_car():
    # 24.5 N/mm at the wheel, 400 kg sprung corner -> about 1.25 Hz
    assert ride_frequency(24_500, 400) == pytest.approx(1.2456, rel=1e-3)


def test_static_sag():
    assert static_sag(24_500, 400) == pytest.approx(0.1601, rel=1e-3)


@pytest.mark.parametrize("fn,args", [
    (spring_rate, (0.1, 0.05, 8)),
    (spring_rate, (0, 0.1, 8)),
    (wahl_factor, (1,)),
    (wheel_rate, (1000, 0)),
    (ride_frequency, (1000, 0)),
])
def test_invalid(fn, args):
    with pytest.raises(ValueError):
        fn(*args)
