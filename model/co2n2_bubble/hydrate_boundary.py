"""CO2/N2 mixture hydrate-formation boundary. EQUATIONS_SPEC.md section 6.

Replaces the first-pass placeholder (a fixed depth/composition box) with a
composition-continuous, physically-motivated boundary: hydrate is assumed
to form when the mixture's CO2 fugacity meets or exceeds the fugacity
pure CO2 would have at its own equilibrium hydrate-formation pressure, at
the same temperature. Diluting with N2 lowers CO2's fugacity at a given
total pressure (for the same reason it lowers CO2's partial pressure),
so a mixture needs a higher total pressure (or colder temperature) than
pure CO2 to reach the same fugacity threshold -- which is exactly the
qualitative behavior the original report's own Chapter 2 describes
(Fig. 2-5: "for a CO2 content below about 50% mixture hydrate formation
pressure drastically increases").

Pure-CO2 boundary curve: a simple Clausius-Clapeyron-style fit,
ln(P) = a + b/T, through the two best-corroborated points on the CO2
hydrate V-Lw-H equilibrium line -- its two quadruple points, both
independently retrieved and cross-checked across multiple sources during
this revision:
  - Lower quadruple point (ice + liquid water + hydrate + vapor):
    T = 271.6 K, P = 1.044 MPa
  - Upper quadruple point (liquid water + hydrate + vapor + liquid CO2):
    T = 283.0 K, P = 4.5 MPa
This is a genuine simplification (two points, not a full literature
regression) and is valid only within, or close to, this 271.6-283 K
range -- exactly this project's scenario matrix (~276-283 K at
300-1500 m depth), so this is not a practical limitation here, but it
should not be extrapolated to warmer or much colder conditions without
re-checking.

Provenance / limitation, stated plainly: the mixture extension (the
fugacity-threshold criterion itself) is physically motivated but not
independently validated against real CO2/N2 mixture hydrate data -- this
project could not access primary CO2/N2 hydrate equilibrium measurements
or a full van der Waals-Platteeuw model (the field's actual state of the
art here, e.g. CSMGem or newer CPA-EoS approaches, per
LITERATURE_UPDATE.md section 6) to calibrate it. Checked, honestly, against
the original 2002 report's own qualitative statement that pure CO2 forms
hydrate around 279 K at typical 500 m ocean pressure (~50 atm): this
curve instead predicts pure CO2 hydrate forming around 27 bar at 279 K --
a real discrepancy, most likely because the thesis's own statement
describes where the real ocean's pressure/temperature profile happens to
overlap the hydrate-forming region at 500 m depth, not a precise
equilibrium-curve reading, whereas this curve is fit directly to two
precisely measured quadruple points. Not resolved further; reported
rather than silently smoothed over. This still replaces a cruder
placeholder (a fixed depth/composition box, `legacy_box_hydrate_window`
below) that had no compositional or thermodynamic sensitivity at all --
a strict improvement in functional form, even with this open calibration
question.
"""

import numpy as np

from . import eos

# Clausius-Clapeyron fit through the two CO2 hydrate quadruple points
# (see module docstring for the two source points).
_CC_SLOPE = -9850.7
_CC_INTERCEPT = 38.615


def pure_co2_hydrate_pressure_bar(T_K: float) -> float:
    """Pure CO2 hydrate (V-Lw-H) equilibrium pressure at temperature T_K,
    bar. Valid for T roughly in [271.6, 283] K -- see module docstring.
    """
    return float(np.exp(_CC_INTERCEPT + _CC_SLOPE / T_K))


def hydrate_forms(y_gas: tuple, T_K: float, P_bar: float) -> bool:
    """True if the CO2/N2 mixture at (y_gas, T_K, P_bar) is predicted to
    form hydrate, via the fugacity-threshold criterion (module docstring).
    """
    y_co2 = y_gas[0]
    if y_co2 <= 0:
        return False

    P_eq_pure = pure_co2_hydrate_pressure_bar(T_K)
    phi_pure = eos.fugacity_coefficient_co2((1.0, 0.0), T_K, P_eq_pure)
    f_eq_pure = phi_pure * P_eq_pure

    phi_mix = eos.fugacity_coefficient_co2(y_gas, T_K, P_bar)
    f_actual = phi_mix * y_co2 * P_bar

    return f_actual >= f_eq_pure


# --- Legacy placeholder, kept for comparison ---

LEGACY_MIN_DEPTH_M = 400.0
LEGACY_MIN_CO2_FRAC = 0.5


def legacy_box_hydrate_window(depth_m: float, co2_frac: float) -> bool:
    """The original first-pass placeholder: a fixed depth/composition box
    with no temperature or pressure sensitivity at all. Superseded by
    hydrate_forms() above; kept only so the two can be compared directly.
    """
    return depth_m >= LEGACY_MIN_DEPTH_M and co2_frac >= LEGACY_MIN_CO2_FRAC
