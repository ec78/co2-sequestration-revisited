"""CO2 mass transfer rate out of the bubble -- Methods A and B.

EQUATIONS_SPEC.md section 6. Both methods return a molar dissolution rate
[mol CO2 / s]; the driver (bubble_model.py) multiplies by dt and updates
composition.
"""

import numpy as np

from .constants import MOLAR_MASS

_HIRAI_FLUX_KG_M2_S = 1.25e-4  # Hirai et al. (1996), non-hydrate case
_FUJIOKA_DDB_DT_M_S = 5.0e-7   # Fujioka et al. (1994), hydrate-coated bubble

# Hydrate-window threshold. [RECONSTRUCTED, approximate placeholder] --
# the original's Fig. 2-5 (CSMHYD-predicted CO2/N2 hydrate formation
# pressure vs. composition/temperature) isn't numerically recoverable
# from the PDF. See EQUATIONS_SPEC.md section 6.
HYDRATE_MIN_DEPTH_M = 400.0
HYDRATE_MIN_CO2_FRAC = 0.5


def in_hydrate_window(depth_m: float, co2_frac: float) -> bool:
    return depth_m >= HYDRATE_MIN_DEPTH_M and co2_frac >= HYDRATE_MIN_CO2_FRAC


def method_b_rate(Db_m: float, x_co2: float) -> float:
    """Eq. 4-11: constant flux (Hirai et al. 1996) x surface area x current
    CO2 mole fraction. Fully specified in the original text -- default
    method for this implementation (see EQUATIONS_SPEC.md section 6).
    """
    area_m2 = np.pi * Db_m**2
    kg_per_s = _HIRAI_FLUX_KG_M2_S * area_m2
    mol_per_s = kg_per_s * 1000.0 / MOLAR_MASS[0]
    return mol_per_s * x_co2


def _diffusivity_co2_water_m2_s(mu_water_cP: float) -> float:
    """Hayduk & Laudie (1974): D_AB = 13.26e-5 / (mu_B^1.14 * V_A^0.589)
    [cm^2/s], mu in cP, V_A = molar volume of solute (CO2) at its normal
    boiling point, ~34.0 cm^3/mol (standard literature value).
    [RECONSTRUCTED] -- see EQUATIONS_SPEC.md section 6 re: Eq. 4-10 OCR
    reliability.
    """
    V_A = 34.0
    D_cm2_s = 13.26e-5 / (mu_water_cP**1.14 * V_A**0.589)
    return D_cm2_s * 1e-4


def method_a_kL(Db_m: float, U_m_s: float, rho_sea: float,
                 mu_sea_mPas: float, T_K: float) -> float:
    """Mass transfer coefficient k_L [m/s] via Sherwood-number correlation
    for a rigid sphere (Eqs. 4-7/4-8/4-9), Mori & Mochizuki (1998) style.
    """
    D_gw = _diffusivity_co2_water_m2_s(mu_sea_mPas)
    mu_pa_s = mu_sea_mPas / 1000.0
    Re = U_m_s * Db_m * rho_sea / mu_pa_s
    Sc = mu_pa_s / (rho_sea * D_gw)

    if Re <= 2000:
        Sh = 1.0 + 0.425 * Re**0.55 * Sc ** (1.0 / 3.0)
    else:
        Sh = 1.0 + 0.724 * Re**0.48 * Sc ** (1.0 / 3.0)

    return Sh * D_gw / Db_m


def method_a_rate(Db_m: float, U_m_s: float, rho_sea: float,
                   mu_sea_mPas: float, T_K: float, x_gs: float) -> float:
    """Eq. 4-5 with k_L from method_a_kL: dmass/dt = -pi Db^2 kL rho_w x_gs."""
    kL = method_a_kL(Db_m, U_m_s, rho_sea, mu_sea_mPas, T_K)
    area_m2 = np.pi * Db_m**2
    kg_per_s = area_m2 * kL * rho_sea * x_gs
    return kg_per_s * 1000.0 / MOLAR_MASS[0]


def method_h_rate(Db_m: float, rho_bub: float) -> float:
    """Hydrate-coated pure/high-CO2 bubble: constant diameter-shrinkage
    rate (Fujioka et al. 1994), converted to a molar rate by
    differentiating Eq. 4-5's left-hand side at fixed rho_bub --
    mass_rate = (pi/2) rho_bub Db^2 |dDb/dt|. See EQUATIONS_SPEC.md
    section 6 for why this is re-derived rather than transcribed from the
    OCR'd Eqs. 4-12/4-13.
    """
    mass_rate_kg_s = (np.pi / 2.0) * rho_bub * Db_m**2 * _FUJIOKA_DDB_DT_M_S
    return mass_rate_kg_s * 1000.0 / MOLAR_MASS[0]


def dissolution_rate(method: str, *, Db_m: float, x_co2: float,
                      U_m_s: float, rho_sea: float, mu_sea_mPas: float,
                      T_K: float, x_gs: float, rho_bub: float = None) -> float:
    """Dispatch to the requested method. method in {"A", "B", "H"}."""
    if method == "B":
        return method_b_rate(Db_m, x_co2)
    if method == "A":
        return method_a_rate(Db_m, U_m_s, rho_sea, mu_sea_mPas, T_K, x_gs)
    if method == "H":
        return method_h_rate(Db_m, rho_bub)
    raise ValueError(f"Unknown mass transfer method: {method!r}")
