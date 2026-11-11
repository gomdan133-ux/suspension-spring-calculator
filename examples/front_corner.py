"""Worked example: front corner of a midsize sedan (MacPherson strut).

Run from the repo root:  python examples/front_corner.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from suspension import (ride_frequency, spring_index, spring_rate,  # noqa: E402
                        spring_shear_stress, static_sag, wahl_factor, wheel_rate)

wire_d = 0.0125        # m
coil_d = 0.110         # m mean diameter
active = 6.5
motion_ratio = 0.95    # strut: spring nearly in line with the wheel
corner_mass = 420      # kg sprung mass on this corner

k = spring_rate(wire_d, coil_d, active)
kw = wheel_rate(k, motion_ratio)
f = ride_frequency(kw, corner_mass)
sag = static_sag(kw, corner_mass)
c = spring_index(wire_d, coil_d)
spring_force = kw * sag / motion_ratio  # force in the spring at ride height
tau = spring_shear_stress(spring_force, wire_d, coil_d)

print(f"Spring rate:       {k / 1000:6.1f} N/mm")
print(f"Wheel rate:        {kw / 1000:6.1f} N/mm")
print(f"Ride frequency:    {f:6.2f} Hz")
print(f"Static sag:        {sag * 1000:6.0f} mm at the wheel")
print(f"Spring index C:    {c:6.1f}  (Wahl factor {wahl_factor(c):.3f})")
print(f"Shear stress:      {tau / 1e6:6.0f} MPa at ride height")
