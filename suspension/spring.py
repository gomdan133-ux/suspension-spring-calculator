"""Helical compression spring: rate and stress."""
import math

STEEL_SHEAR_MODULUS = 79.3e9  # Pa, typical spring steel


def spring_rate(wire_d_m: float, mean_coil_d_m: float, active_coils: float,
                shear_modulus_pa: float = STEEL_SHEAR_MODULUS) -> float:
    """Spring rate (N/m) of a helical compression spring.

    k = G d^4 / (8 D^3 Na)
    d = wire diameter, D = mean coil diameter, Na = active coils.
    """
    if min(wire_d_m, mean_coil_d_m, active_coils, shear_modulus_pa) <= 0:
        raise ValueError("all inputs must be > 0")
    if wire_d_m >= mean_coil_d_m:
        raise ValueError("wire diameter must be smaller than mean coil diameter")
    return shear_modulus_pa * wire_d_m ** 4 / (8 * mean_coil_d_m ** 3 * active_coils)


def spring_index(wire_d_m: float, mean_coil_d_m: float) -> float:
    """C = D / d. Practical springs are usually between 4 and 12."""
    if wire_d_m <= 0 or mean_coil_d_m <= 0:
        raise ValueError("inputs must be > 0")
    return mean_coil_d_m / wire_d_m


def wahl_factor(index: float) -> float:
    """Wahl correction for curvature and direct shear: (4C-1)/(4C-4) + 0.615/C."""
    if index <= 1:
        raise ValueError("spring index must be > 1")
    return (4 * index - 1) / (4 * index - 4) + 0.615 / index


def spring_shear_stress(force_n: float, wire_d_m: float, mean_coil_d_m: float) -> float:
    """Corrected max shear stress (Pa): tau = Kw * 8 F D / (pi d^3)."""
    if force_n < 0:
        raise ValueError("force must be >= 0")
    kw = wahl_factor(spring_index(wire_d_m, mean_coil_d_m))
    return kw * 8 * force_n * mean_coil_d_m / (math.pi * wire_d_m ** 3)
