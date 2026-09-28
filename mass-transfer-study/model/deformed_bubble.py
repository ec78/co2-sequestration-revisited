"""Ellipsoidal / spherical-cap bubble regime. STUDY_PLAN.md follow-up from
the mobile_sphere.py addendum.

Phase C's mobile-sphere work found that Saito et al.'s (2000) plausible
bubble sizes (2-30 mm) sit entirely in the shape-*deformed* regime
(Eotvos number 0.5 to >100, per mobile_sphere.eotvos_number), where
neither the rigid-sphere nor the idealized clean-spherical-bubble theory
this study built has any real physical basis -- both assume an
undeformed sphere. This module adds the two regimes real bubbles that
size actually occupy, using well-established, independently-verified
closed-form results rather than the full Clift, Grace & Weber (1978)
shape-regime machinery (already cited in the original 2002 thesis's own
bibliography, and the more complete treatment if this is ever revisited
further):

- **Ellipsoidal / wobbling** (moderate Eo): Mendelson's (1967) wave-
  analogy terminal velocity,
      U = sqrt(2 sigma/(rho_L Db) + g Db/2)
  derived from treating a rising bubble's terminal speed as analogous to
  the propagation speed of a surface gravity-capillary wave of
  wavelength ~ Db. Verified against a source reproducing the formula
  directly (not taken from memory alone).

- **Spherical cap** (high Eo): the classical Davies & Taylor (1950)
  result,
      U = (2/3) sqrt(g R),  R = Db/2 (equivalent-sphere radius)
  derived from matching the pressure field over the cap to ideal
  potential flow around a sphere. R here is the equivalent-volume-sphere
  radius, a standard simplifying approximation -- the bubble's actual
  cap radius of curvature differs somewhat and would need its own
  correlation (e.g. Wegener & Parlange) for a fully rigorous treatment,
  not attempted here.

Regime boundaries (Eo < 0.5 spherical, 0.5-40 ellipsoidal, > 40 cap) are
the commonly cited thresholds from the Clift-Grace-Weber picture, not
independently re-derived.

Mass transfer in both deformed regimes uses the same Levich penetration-
theory k_L formula as mobile_sphere.py, with the regime-correct velocity
substituted in -- standard engineering practice (penetration theory is
applied broadly across mobile/circulating-interface regimes, not just
the idealized spherical case), not a new, unverified assumption beyond
what mobile_sphere.py already documents.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble import eos  # noqa: E402
from mobile_sphere import eotvos_number, terminal_velocity_mobile, predict_kL  # noqa: E402

G = 9.81

EO_SPHERICAL_MAX = 0.5
EO_ELLIPSOIDAL_MAX = 40.0


def shape_regime(Eo: float) -> str:
    if Eo < EO_SPHERICAL_MAX:
        return "spherical"
    elif Eo < EO_ELLIPSOIDAL_MAX:
        return "ellipsoidal"
    else:
        return "cap"


def terminal_velocity_mendelson(Db_m: float, rho_sea: float, sigma_l: float) -> float:
    return np.sqrt(2 * sigma_l / (rho_sea * Db_m) + G * Db_m / 2.0)


def terminal_velocity_davies_taylor(Db_m: float) -> float:
    R = Db_m / 2.0
    return (2.0 / 3.0) * np.sqrt(G * R)


def terminal_velocity_deformed(Db_m: float, rho_bub: float, rho_sea: float,
                                mu_sea_mPas: float, sigma_l: float = 0.074) -> tuple:
    """Returns (U, regime). Dispatches to the regime-correct terminal
    velocity based on Eotvos number; falls back to the (already-verified)
    mobile-sphere spherical treatment when Eo is small.
    """
    Eo = eotvos_number(Db_m, rho_sea, rho_bub, sigma_l)
    regime = shape_regime(Eo)

    if regime == "spherical":
        U = terminal_velocity_mobile(Db_m, rho_bub, rho_sea, mu_sea_mPas)
    elif regime == "ellipsoidal":
        U = terminal_velocity_mendelson(Db_m, rho_sea, sigma_l)
    else:
        U = terminal_velocity_davies_taylor(Db_m)

    return U, regime


def predict_over_diameter_range(diameters_m, y_gas: tuple, T_K: float,
                                 P_bar: float, rho_sea: float,
                                 mu_sea_mPas: float,
                                 sigma_l: float = 0.074) -> list:
    """Same diameter-sweep pattern as rigid_sphere.py / mobile_sphere.py,
    now with the physically appropriate regime (and its own terminal
    velocity) selected per diameter rather than assuming a spherical
    bubble throughout.
    """
    state = eos.mixture_density(y_gas, T_K, P_bar)
    rho_bub = state.density_kg_m3
    mu_pa_s = mu_sea_mPas / 1000.0

    results = []
    for Db in diameters_m:
        U, regime = terminal_velocity_deformed(Db, rho_bub, rho_sea, mu_sea_mPas, sigma_l)
        kL = predict_kL(Db, U, mu_sea_mPas)
        Re = U * Db * rho_sea / mu_pa_s
        Eo = eotvos_number(Db, rho_sea, rho_bub, sigma_l)
        results.append({"Db_m": Db, "U_m_s": U, "Re": Re, "Eo": Eo,
                         "regime": regime, "kL_m_s": kL})
    return results
