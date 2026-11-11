# Suspension Spring Calculator

A tested Python library that connects a coil spring's dimensions to what the car does: spring rate, stress in the wire, rate at the wheel, ride frequency, and how far the car settles at ride height.

Built by an ASE-certified automotive technician to back up shop decisions (spring swaps, lowering springs, sagging cars) with the engineering behind them.

## The math

**1. Spring rate** (helical compression spring)

$$k = \frac{G\,d^4}{8\,D^3\,N_a}$$

d = wire diameter, D = mean coil diameter, Nₐ = active coils, G = shear modulus (79.3 GPa for spring steel).

**2. Spring index and Wahl factor**

$$C = \frac{D}{d}, \qquad K_w = \frac{4C-1}{4C-4} + \frac{0.615}{C}$$

**3. Corrected shear stress in the wire**

$$\tau = K_w \frac{8 F D}{\pi d^3}$$

**4. Wheel rate** (MR = spring travel / wheel travel)

$$k_{wheel} = k_{spring} \cdot MR^2$$

**5. Ride frequency**

$$f = \frac{1}{2\pi}\sqrt{\frac{k_{wheel}}{m_{corner}}}$$

**6. Static sag**

$$x = \frac{m g}{k_{wheel}}$$

All functions use SI units (N, m, kg, Pa).

## Example

```bash
python examples/front_corner.py
```

```
Spring rate:         28.0 N/mm
Wheel rate:          25.2 N/mm
Ride frequency:      1.23 Hz
Static sag:           163 mm at the wheel
Spring index C:       8.8  (Wahl factor 1.166)
Shear stress:         725 MPa at ride height
```

This is a midsize sedan front strut. 1.23 Hz is in the normal comfort range for a passenger car, about 1.0 to 1.5 Hz.

## Shop takeaways

- **Wire diameter matters most:** rate goes up with d⁴, so 10% thicker wire gives about 46% more rate.
- **Cutting coils makes a spring stiffer,** not softer, because fewer active coils means a higher rate. It also raises stress, which is one reason cut springs sag or break.
- **Motion ratio is squared:** a spring halfway down a control arm (MR 0.5) gives only a quarter of its rate at the wheel.
- **Ride frequency and sag are linked** (f ≈ 0.5 / √x, with x in meters). A "too soft" complaint and a "sits too low" complaint are often the same problem.

## Install and test

```bash
pip install pytest
pytest -q
```

## Project layout

```
suspension/
  spring.py   spring rate, index, Wahl factor, shear stress
  ride.py     wheel rate, ride frequency, static sag
tests/        12 pytest tests
examples/     worked front corner example
```

## How this was built

1. **Started from shop problems.** I chose questions I run into on the job, like why a cut spring rides harsh, why a car sits low, and why the same spring feels different on a strut than on a control arm.
2. **Used standard machine design formulas.** These are the textbook helical spring equations with the Wahl correction, plus basic vibration math for ride frequency.
3. **Checked by hand first.** I worked out the test values by hand, for example the 12 mm wire, 100 mm coil, 8 coil spring at about 25.7 N/mm. The tests also check the scaling rules: d⁴, 1/Nₐ and MR².
4. **Wrote 12 pytest tests,** including invalid inputs, and ran a worked example. The output in this README comes from actually running it.

**Limits:** this models static, linear springs. It doesn't include tire stiffness, progressive springs, or dampers. For a real build, use the OEM or spring maker's data.

## License

MIT
