"""Mobile/clean-sphere mass-transfer model. STUDY_PLAN.md section 3.2.

Levich's (1962) penetration-theory result for a bubble with a fully
mobile (stress-free, internally circulating) interface:

    k_L = (2/sqrt(pi)) * sqrt(D_gw * U / Db)
    Sh  = (2/sqrt(pi)) * Pe^(1/2),      Pe = Re * Sc

Verified against a live secondary source while writing STUDY_PLAN.md
(not taken from memory alone) -- see that file's section 3.2 for the
citation trail. Contrast with rigid_sphere.py's Sc^(1/3) form: this is
Sc^(1/2), a genuinely different scaling, not just a different prefactor.

Scoping simplification, stated plainly (see STUDY_PLAN.md Phase C):
this module reuses rigid_sphere.py's rigid-sphere terminal velocity
(Mori & Mochizuki drag law) rather than also deriving a mobile-sphere
(Hadamard-Rybczynski at low Re; a different clean-bubble drag law again
at the moderate-to-high Re most of this study's data sits in) drag
model. A truly mobile bubble has lower drag and rises faster than a
rigid one of the same size, so reusing the rigid velocity here is a
CONSERVATIVE choice -- since k_L ~ sqrt(U), it under-, not over-,
estimates the mobile regime's true k_L. If this conservative estimate
already closes a rigid-sphere gap, that's meaningful; if it doesn't, a
fully self-consistent mobile-drag treatment (a further refinement, not
attempted here) would only close it further, not less.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble import mass_transfer, eos  # noqa: E402
from rigid_sphere import terminal_velocity_rigid  # noqa: E402


def predict_kL(Db_m: float, U_m_s: float, mu_sea_mPas: float) -> float:
    """Levich mobile-sphere k_L [m/s]. Reuses the existing Hayduk-Laudie
    diffusivity helper in mass_transfer.py rather than duplicating it."""
    D_gw = mass_transfer._diffusivity_co2_water_m2_s(mu_sea_mPas)
    return (2.0 / np.sqrt(np.pi)) * np.sqrt(D_gw * U_m_s / Db_m)


def predict_over_diameter_range(diameters_m, y_gas: tuple, T_K: float,
                                 P_bar: float, rho_sea: float,
                                 mu_sea_mPas: float) -> list:
    """Same diameter-sweep pattern as rigid_sphere.py, for direct
    side-by-side comparison. Velocity is the rigid-sphere terminal
    velocity (see module docstring for why that's the conservative,
    not incorrect, choice here).
    """
    state = eos.mixture_density(y_gas, T_K, P_bar)
    rho_bub = state.density_kg_m3
    mu_pa_s = mu_sea_mPas / 1000.0
    D_gw = mass_transfer._diffusivity_co2_water_m2_s(mu_sea_mPas)
    Sc = mu_pa_s / (rho_sea * D_gw)

    results = []
    for Db in diameters_m:
        U = terminal_velocity_rigid(Db, rho_bub, rho_sea, mu_sea_mPas)
        kL = predict_kL(Db, U, mu_sea_mPas)
        Re = U * Db * rho_sea / mu_pa_s
        results.append({"Db_m": Db, "U_m_s": U, "Re": Re, "Pe": Re * Sc, "kL_m_s": kL})
    return results
