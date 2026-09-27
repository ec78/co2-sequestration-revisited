"""Duan & Sun (2003) CO2 solubility model.

EQUATIONS_SPEC.md section 4. Replaces the fugacity-corrected Weiss (1974)
placeholder as the default solubility model. Implements:

  Duan, Z., Sun, R. (2003). "An improved model calculating CO2 solubility
  in pure water and aqueous NaCl solutions from 273 to 533 K and from 0
  to 2000 bar." Chemical Geology, 193(3), 257-271.

using Duan et al.'s (1992) own CO2 equation of state for the vapor-phase
fugacity coefficient (rather than reusing this project's generic
Peng-Robinson EOS from eos.py, which was fit for a different purpose) --
this is the EOS the solubility model was actually calibrated against.

Provenance / transcription note (see EQUATIONS_SPEC.md section 4 for the
full account): the coefficients below were not read directly from the
original 2003 paper (no clean full-text copy could be retrieved -- every
PDF found had a font-encoding fault that corrupted negative-number
characters). They come from an independent open-source implementation
(CO2REAKT, github.com/mcrossover97/CO2REAKT, solvers/DuanSun2003.py, LGPL
v2.1), cross-validated line-by-line against numeric fragments recovered
from a peer-reviewed paper that reproduces the same tables (Gilbert et
al., 2016/2014-era, "CO2 solubility in aqueous solutions containing Na+,
Ca2+..."; Table 6/7/8 of a related Petroleum Science paper) -- every
digit that survived that second source's own extraction matched this
implementation exactly, including cases where the second source alone
would have been ambiguous about which coefficient belonged to which
parameter. Treated as trustworthy on that basis, not as a verbatim
primary-source transcription.
"""

import numpy as np
from scipy.optimize import brentq

from .constants import MOLAR_MASS

# Water critical properties
_TC_H2O = 647.29  # K
_PC_H2O = 220.85  # bar

# CO2 critical properties (Duan et al. 1992's own values -- close to but
# not necessarily bit-identical to eos.py's constants.TC_K/PC_BAR, which
# come from a different source; kept separate deliberately so this module
# reproduces Duan & Sun's own EOS exactly rather than mixing constant
# sources).
_TC_CO2 = 304.15  # K
_PC_CO2 = 73.8     # bar


def _p_h2o_bar(T_K: float) -> float:
    """Water vapor pressure, bar (Duan & Sun's own correlation, not a
    general steam-table lookup -- consistent with how they assumed
    yH2O*P = P_H2O for the CO2-H2O-NaCl system).
    """
    c1, c2, c3, c4, c5 = -38.640844, 5.8948420, 59.876516, 26.654627, 10.637097
    t = (T_K - _TC_H2O) / _TC_H2O
    return (_PC_H2O * T_K / _TC_H2O) * (
        1 + c1 * (-t) ** 1.9 + c2 * t + c3 * t**2 + c4 * t**3 + c5 * t**4
    )


def _eos_residual(Vr: float, Pr: float, Tr: float) -> float:
    a1, a2, a3 = 8.99288497e-2, -4.94783127e-1, 4.77922245e-2
    a4, a5, a6 = 1.03808883e-2, -2.82516861e-2, 9.49887563e-2
    a7, a8, a9 = 5.20600880e-4, -2.93540971e-4, -1.77265112e-3
    a10, a11, a12 = -2.51101973e-5, 8.93353441e-5, 7.88998563e-5
    a13, a14, a15 = -1.66727022e-2, 1.39800000, 2.96000000e-2

    term1 = (a1 + a2 / Tr**2 + a3 / Tr**3) / Vr
    term2 = (a4 + a5 / Tr**2 + a6 / Tr**3) / Vr**2
    term3 = (a7 + a8 / Tr**2 + a9 / Tr**3) / Vr**4
    term4 = (a10 + a11 / Tr**2 + a12 / Tr**3) / Vr**5
    term5 = a13 / (Tr**3 * Vr**2) * (a14 + a15 / Vr**2) * np.exp(-a15 / Vr**2)
    return Pr * Vr / Tr - (1 + term1 + term2 + term3 + term4 + term5)


def _fugacity_coefficient_co2(T_K: float, P_bar: float) -> float:
    """CO2 fugacity coefficient from Duan et al. (1992)'s own EOS."""
    Pr = P_bar / _PC_CO2
    Tr = T_K / _TC_CO2

    Vr = brentq(_eos_residual, 1e-3, 1e3, args=(Pr, Tr), maxiter=200)
    Z = Pr * Vr / Tr

    a1, a2, a3 = 8.99288497e-2, -4.94783127e-1, 4.77922245e-2
    a4, a5, a6 = 1.03808883e-2, -2.82516861e-2, 9.49887563e-2
    a7, a8, a9 = 5.20600880e-4, -2.93540971e-4, -1.77265112e-3
    a10, a11, a12 = -2.51101973e-5, 8.93353441e-5, 7.88998563e-5
    a13, a14, a15 = -1.66727022e-2, 1.39800000, 2.96000000e-2

    term1 = (a1 + a2 / Tr**2 + a3 / Tr**3) / Vr
    term2 = (a4 + a5 / Tr**2 + a6 / Tr**3) / (2 * Vr**2)
    term3 = (a7 + a8 / Tr**2 + a9 / Tr**3) / (4 * Vr**4)
    term4 = (a10 + a11 / Tr**2 + a12 / Tr**3) / (5 * Vr**5)
    term5 = (a13 / (2 * Tr**3 * a15)
             * (a14 + 1 - (a14 + 1 + a15 / Vr**2) * np.exp(-a15 / Vr**2)))
    ln_phi = Z - 1 - np.log(Z) + term1 + term2 + term3 + term4 + term5
    return np.exp(ln_phi)


def _mu0_co2_RT(P_bar: float, T_K: float) -> float:
    c1, c2, c3 = 28.9447706, -0.0354581768, -4770.67077
    c4, c5, c6 = 1.02782768e-5, 33.8126098, 9.04037140e-3
    c7, c8, c9 = -1.14934031e-3, -0.307405726, -0.0907301486
    c10 = 9.32713393e-4
    return (c1 + c2 * T_K + c3 / T_K + c4 * T_K**2 + c5 / (630 - T_K)
            + c6 * P_bar + c7 * P_bar * np.log(T_K) + c8 * P_bar / T_K
            + c9 * P_bar / (630 - T_K) + c10 * P_bar**2 / (630 - T_K) ** 2)


def _lambda_co2_na(P_bar: float, T_K: float) -> float:
    c1, c2, c3 = -0.411370585, 6.07632013e-4, 97.5347708
    c8, c9, c11 = -0.0237622469, 0.0170656236, 1.41335834e-5
    return (c1 + c2 * T_K + c3 / T_K + c8 * P_bar / T_K
            + c9 * P_bar / (630 - T_K) + c11 * T_K * np.log(P_bar))


def _xi_co2_na_cl(P_bar: float, T_K: float) -> float:
    c1, c2 = 3.36389723e-4, -1.98298980e-5
    c8, c9 = 2.12220830e-3, -5.24873303e-3
    return c1 + c2 * T_K + c8 * P_bar / T_K + c9 * P_bar / (630 - T_K)


def _co2_molality_from_fugacity(f_co2_bar: float, T_K: float, P_bar: float,
                                 nacl_molality: float) -> float:
    """The actual Duan & Sun aqueous-equilibrium relation (Eq. 11), taking
    CO2 fugacity directly rather than computing it internally. The
    mu0/lambda/xi terms describe the *aqueous* side of the CO2(g) <->
    CO2(aq) equilibrium and don't care how f_CO2 was obtained -- fugacity
    is fugacity regardless of which EOS/route computed it, so this is the
    natural seam for supplying a vapor-phase fugacity from a different
    model than Duan & Sun's own (see co2_molality_pure_system's docstring
    for why that matters here).
    """
    mu0_RT = _mu0_co2_RT(P_bar, T_K)
    lam = _lambda_co2_na(P_bar, T_K)
    xi = _xi_co2_na_cl(P_bar, T_K)

    m_na = nacl_molality
    m_cl = nacl_molality

    ln_m_co2 = (
        np.log(f_co2_bar)
        - mu0_RT
        - 2 * lam * m_na
        - xi * m_cl * m_na
    )
    return float(np.exp(ln_m_co2))


def co2_molality_pure_system(T_K: float, P_bar: float,
                              nacl_molality: float = 0.0) -> float:
    """CO2 solubility, mol CO2 / kg H2O, for a PURE CO2 + H2O vapor phase
    (Duan & Sun's own calibration system) in equilibrium with a NaCl
    solution of the given molality. Uses Duan & Sun's own y_CO2 =
    (P-P_H2O)/P and their own EOS's fugacity coefficient -- valid only
    when the vapor phase really is just CO2 + water vapor.

    This is NOT what this project's bubble model should call directly
    (the bubble is a CO2/N2 mixture; treating "everything that isn't
    water vapor" as CO2 would wrongly count N2 as CO2 and overstate CO2's
    fugacity). Kept as the standalone, literature-comparable entry point
    -- used for the pure-water/pure-CO2 validation checks in
    analysis/PHASE3_NOTES.md. The bubble model uses
    solubility_mass_fraction_for_bubble instead.
    """
    p_h2o = _p_h2o_bar(T_K)
    y_co2 = (P_bar - p_h2o) / P_bar
    if y_co2 <= 0:
        return 0.0
    phi_co2 = _fugacity_coefficient_co2(T_K, P_bar)
    f_co2 = y_co2 * phi_co2 * P_bar
    return _co2_molality_from_fugacity(f_co2, T_K, P_bar, nacl_molality)


def solubility_mass_fraction_for_bubble(f_co2_bar: float, T_K: float,
                                         P_bar: float,
                                         nacl_molality: float = 0.0) -> float:
    """Saturation mass fraction of CO2 in seawater (kg CO2 / kg solution)
    given the CO2 fugacity actually present in a CO2/N2 bubble (computed
    by eos.py's mixture fugacity coefficient, which correctly accounts
    for N2 dilution) -- this is what bubble_model.py should call. Drop-in
    replacement for solubility.py's x_gs.
    """
    m_co2 = _co2_molality_from_fugacity(f_co2_bar, T_K, P_bar, nacl_molality)
    mass_co2_per_kg_water = m_co2 * MOLAR_MASS[0] / 1000.0  # kg CO2 / kg H2O
    return mass_co2_per_kg_water / (1.0 + mass_co2_per_kg_water)
