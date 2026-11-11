"""From spring rate to what the driver feels."""
import math

G = 9.80665


def wheel_rate(spring_rate_n_per_m: float, motion_ratio: float) -> float:
    """Effective rate at the wheel (N/m): k_wheel = k_spring * MR^2.

    MR = spring travel / wheel travel. A spring mounted partway down a control
    arm (MR < 1) feels much softer at the wheel than its own rate.
    """
    if spring_rate_n_per_m <= 0 or motion_ratio <= 0:
        raise ValueError("inputs must be > 0")
    return spring_rate_n_per_m * motion_ratio ** 2


def ride_frequency(wheel_rate_n_per_m: float, sprung_corner_mass_kg: float) -> float:
    """Undamped ride frequency (Hz): f = sqrt(k / m) / (2 pi).

    Typical passenger cars run about 1.0 to 1.5 Hz; sports cars go higher.
    Tire stiffness is ignored (it lowers the real value slightly).
    """
    if wheel_rate_n_per_m <= 0 or sprung_corner_mass_kg <= 0:
        raise ValueError("inputs must be > 0")
    return math.sqrt(wheel_rate_n_per_m / sprung_corner_mass_kg) / (2 * math.pi)


def static_sag(wheel_rate_n_per_m: float, sprung_corner_mass_kg: float) -> float:
    """Static wheel deflection under the corner's weight (m): x = m g / k."""
    if wheel_rate_n_per_m <= 0 or sprung_corner_mass_kg < 0:
        raise ValueError("invalid input")
    return sprung_corner_mass_kg * G / wheel_rate_n_per_m
