"""Rigid/contaminated-sphere mass-transfer model. STUDY_PLAN.md section 3.1.

A gas bubble with a contaminated (no-slip) surface behaves, for mass
transfer, like a rigid solid sphere: no internal circulation renews the
interface, so transfer is governed by a diffusive boundary layer. This is
the regime the engineering correlations (Frossling-type; the form used by
Mori & Mochizuki, 1998) describe, and it's already implemented in this
repo's main model as "Method A" (../../model/co2n2_bubble/mass_transfer.py)
-- reused here directly rather than re-derived, per this repo's own
convention of fixing/extending physics at its single source.

What this module adds beyond the existing Method A: a genuine
steady-state (terminal) rise-velocity solver for the rigid-sphere drag
law, usable independently of the main bubble model's time-stepping loop,
for cases (like most of this study's literature dataset) where the
bubble diameter actually used in a given experiment isn't known and a
plausible-range sweep is the honest thing to compute instead of a single
fabricated-precision point estimate.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble import mass_transfer, eos  # noqa: E402

G = 9.81


def terminal_velocity_rigid(Db_m: float, rho_bub: float, rho_sea: float,
                             mu_sea_mPas: float, max_iter: int = 200,
                             tol: float = 1e-9) -> float:
    """Steady-state rise velocity for a rigid sphere: buoyancy balanced
    against drag, using the same Cd(Re) correlation as this project's main
    bubble model (Mori & Mochizuki rigid-sphere form -- Eq. 4-3 in
    ../../model/EQUATIONS_SPEC.md). Solved as a genuine fixed point in Re,
    not a single transient time-step (the main model's
    bubble_model.solve_rise_velocity is deliberately transient/dt-based
    for its own purpose -- tracking a rising bubble's history -- and isn't
    the right tool for "what is the terminal velocity of a rigid sphere
    of this size," which is what a literature measurement typically
    reports).
    """
    mu_pa_s = mu_sea_mPas / 1000.0
    delta_ratio = 1.0 - rho_bub / rho_sea  # (1 - gamma)
    if delta_ratio <= 0:
        raise ValueError("Bubble is denser than seawater -- would sink, not rise.")

    U = 0.1
    for _ in range(max_iter):
        Re = U * Db_m * rho_sea / mu_pa_s
        Cd = (24.0 / Re) * (1 + 0.173 * Re**0.657) + 0.413 / (1 + 16300 * Re**-1.09)
        U_new = np.sqrt((4.0 / 3.0) * G * Db_m * delta_ratio / Cd)
        if abs(U_new - U) < tol * max(1.0, U):
            return U_new
        U = U_new
    return U


def predict_kL(Db_m: float, U_m_s: float, rho_sea: float,
                mu_sea_mPas: float, T_K: float) -> float:
    """Rigid-sphere k_L [m/s] at a known diameter and velocity -- thin,
    named wrapper on the existing Method A implementation."""
    return mass_transfer.method_a_kL(Db_m, U_m_s, rho_sea, mu_sea_mPas, T_K)


def predict_over_diameter_range(diameters_m, y_gas: tuple, T_K: float,
                                 P_bar: float, rho_sea: float,
                                 mu_sea_mPas: float) -> list:
    """For each candidate diameter, solve the self-consistent rigid-sphere
    terminal velocity, then predict k_L at that velocity. Returns a list
    of dicts (Db_m, U_m_s, Re, kL_m_s) -- the honest way to compare
    against a literature value whose actual bubble size isn't known: a
    predicted range, not a single fabricated-precision number.
    """
    state = eos.mixture_density(y_gas, T_K, P_bar)
    rho_bub = state.density_kg_m3

    results = []
    for Db in diameters_m:
        U = terminal_velocity_rigid(Db, rho_bub, rho_sea, mu_sea_mPas)
        kL = predict_kL(Db, U, rho_sea, mu_sea_mPas, T_K)
        mu_pa_s = mu_sea_mPas / 1000.0
        Re = U * Db * rho_sea / mu_pa_s
        results.append({"Db_m": Db, "U_m_s": U, "Re": Re, "kL_m_s": kL})
    return results
