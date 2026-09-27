"""CO2 solubility (saturation mass fraction) in seawater at depth.

EQUATIONS_SPEC.md section 4 -- [MODERNIZED]. Replaces the original's
hand-interpolated figure (Mori & Mochizuki 1998 data, not recoverable)
with the Duan & Sun (2003) CO2-brine solubility model (see duan_sun.py),
used as the default. An earlier, simpler fugacity-corrected Weiss (1974)
Henry's-law approximation is kept as `solubility_mass_fraction_weiss` for
comparison -- it was the first-pass placeholder before Duan & Sun (2003)
was transcribed; see EQUATIONS_SPEC.md section 4 for the full history and
why the Method A vs. B comparison (analysis/method_a_vs_b.md) made
upgrading past it a priority.

Seawater is approximated as an equivalent NaCl solution (Duan & Sun
support NaCl explicitly; other seawater ions are the minority by mass and
this project doesn't track them elsewhere either -- consistent scope, not
a new simplification introduced here).
"""

import numpy as np

from . import eos, duan_sun
from .constants import MOLAR_MASS

_NACL_MOLAR_MASS_G_MOL = 58.44


def seawater_nacl_equivalent_molality(salinity_psu: float = 35.0) -> float:
    """Converts bulk salinity (g salt / kg seawater, ~= practical salinity
    units) to an equivalent NaCl molality (mol NaCl / kg water), for use
    with duan_sun.py. S=35 -> ~0.62 mol/kg.
    """
    salt_kg_per_kg_seawater = salinity_psu / 1000.0
    water_kg_per_kg_seawater = 1.0 - salt_kg_per_kg_seawater
    moles_nacl_per_kg_seawater = (salinity_psu / _NACL_MOLAR_MASS_G_MOL)
    return moles_nacl_per_kg_seawater / water_kg_per_kg_seawater


def solubility_mass_fraction_duan_sun(y: tuple, T_K: float, P_bar: float,
                                       salinity_psu: float = 35.0) -> float:
    """Default solubility model. Computes the bubble's actual CO2
    fugacity from this project's own CO2/N2 mixture EOS (eos.py, which
    correctly accounts for N2 dilution) and feeds it into Duan & Sun's
    (2003) aqueous-equilibrium relation.
    """
    phi_co2 = eos.fugacity_coefficient_co2(y, T_K, P_bar)
    f_co2_bar = phi_co2 * y[0] * P_bar
    nacl_m = seawater_nacl_equivalent_molality(salinity_psu)
    return duan_sun.solubility_mass_fraction_for_bubble(f_co2_bar, T_K, P_bar, nacl_m)


# --- Legacy Weiss (1974) approximation, kept for comparison ---

_WEISS_A1, _WEISS_A2, _WEISS_A3 = -60.2409, 93.4517, 23.3585
_WEISS_B1, _WEISS_B2, _WEISS_B3 = 0.023517, -0.023656, 0.0047036
_BAR_TO_ATM = 0.986923


def _weiss_k0(T_K: float, salinity_psu: float) -> float:
    """K0, mol CO2 / (kg seawater * atm), Weiss (1974)."""
    ln_k0 = (
        _WEISS_A1 + _WEISS_A2 * (100.0 / T_K) + _WEISS_A3 * np.log(T_K / 100.0)
        + salinity_psu * (_WEISS_B1 + _WEISS_B2 * (T_K / 100.0)
                           + _WEISS_B3 * (T_K / 100.0) ** 2)
    )
    return float(np.exp(ln_k0))


def solubility_mass_fraction_weiss(y: tuple, T_K: float, P_bar: float,
                                    salinity_psu: float = 35.0) -> float:
    """First-pass placeholder (superseded by solubility_mass_fraction_duan_sun,
    now the default). Kept only for side-by-side comparison."""
    k0 = _weiss_k0(T_K, salinity_psu)  # mol/(kg*atm)
    phi_co2 = eos.fugacity_coefficient_co2(y, T_K, P_bar)
    f_co2_atm = phi_co2 * y[0] * P_bar * _BAR_TO_ATM

    c_sat_mol_per_kg = k0 * f_co2_atm
    return c_sat_mol_per_kg * MOLAR_MASS[0] / 1000.0


def solubility_mass_fraction(y: tuple, T_K: float, P_bar: float,
                              salinity_psu: float = 35.0) -> float:
    """Saturation mass fraction of CO2 in seawater (kg CO2 / kg seawater),
    i.e. x_gs in Eq. 4-5, at the bubble's current composition/T/P. Uses
    Duan & Sun (2003) by default.
    """
    return solubility_mass_fraction_duan_sun(y, T_K, P_bar, salinity_psu)
