"""Mobile/clean-sphere mass-transfer model. STUDY_PLAN.md section 3.2.

Levich's (1962) penetration-theory result for a bubble with a fully
mobile (stress-free, internally circulating) interface:

    k_L = (2/sqrt(pi)) * sqrt(D_gw * U / Db)
    Sh  = (2/sqrt(pi)) * Pe^(1/2),      Pe = Re * Sc

Verified against a live secondary source while writing STUDY_PLAN.md
(not taken from memory alone) -- see that file's section 3.2 for the
citation trail. Contrast with rigid_sphere.py's Sc^(1/3) form: this is
Sc^(1/2), a genuinely different scaling, not just a different prefactor.

Terminal velocity, updated from the first Phase C pass: this module now
uses a genuine mobile-sphere (clean-bubble) drag law, not a reused
rigid-sphere velocity. Mei, Klausner & Lawrence (1994) give a single
closed-form drag coefficient spanning creeping flow through moderate-to-
high Reynolds number:

    Cd = (16/Re) * (16 + 3.315 sqrt(Re) + 3 Re) / (16 + 3.315 sqrt(Re) + Re)

Checked independently before use (not just trusted from a single search
result), by verifying both of its analytic limits against separately
well-established results: as Re -> 0, Cd -> 16/Re, exactly the classical
Hadamard-Rybczynski creeping-flow drag on a gas bubble (2/3 of the rigid-
sphere Stokes value, 24/Re -- the correct low-Re clean-bubble reduction);
as Re -> infinity, Cd -> 48/Re, exactly Moore's (1965) classical high-Re
clean-bubble asymptote. A single formula correctly reproducing two
independently-known limits is meaningfully more trustworthy than a
formula taken on the strength of one search result alone.

This still doesn't model bubble shape deformation, and that turns out to
matter a great deal for this study's own data, not just as a theoretical
caveat: checking the Eotvos number (eotvos_number() below) for Saito et
al.'s plausible bubble sizes (2-30 mm) shows Eo ranging from ~0.5 to
>100 -- i.e. Saito's *entire* plausible bubble-size range sits in the
shape-deformed (ellipsoidal/wobbling) regime, not the spherical regime
this formula (or rigid_sphere.py's, which shares the same spherical
premise) assumes. Cho & Choi's micron-scale bubbles, by contrast, have
Eo ~ 1e-4 -- deeply spherical, no such concern. Practical consequence,
reported in full in analysis/phase_c_findings.md: this module's numbers
should NOT be read as an improved Saito comparison (the previous,
rigid-drag-based conservative estimate is what's actually reported
there) -- they're kept here as a real, informative negative result about
the limits of a sphere-only theoretical framework, discovered specifically
by attempting this refinement rather than assumed in advance.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble import mass_transfer, eos  # noqa: E402

G = 9.81


def eotvos_number(Db_m: float, rho_sea: float, rho_bub: float,
                   sigma_l: float = 0.074) -> float:
    """Eo = g rho_diff Db^2 / sigma -- governs whether a bubble stays
    spherical (Eo << 1) or deforms to ellipsoidal/spherical-cap (Eo >~ 1).
    Mei et al.'s drag law -- and the whole spherical-bubble premise this
    module and rigid_sphere.py both share -- assumes an undeformed
    sphere; it has no theoretical basis once Eo is not small.
    """
    return G * abs(rho_sea - rho_bub) * Db_m**2 / sigma_l


def _mei_drag_coefficient(Re: float) -> float:
    return (16.0 / Re) * (16 + 3.315 * np.sqrt(Re) + 3 * Re) / (16 + 3.315 * np.sqrt(Re) + Re)


def terminal_velocity_mobile(Db_m: float, rho_bub: float, rho_sea: float,
                              mu_sea_mPas: float, max_iter: int = 200,
                              tol: float = 1e-9) -> float:
    """Steady-state rise velocity for a clean (mobile-interface) bubble,
    via the Mei/Klausner/Lawrence (1994) drag law -- same fixed-point
    structure as rigid_sphere.py's terminal_velocity_rigid, different
    (lower) drag law.
    """
    mu_pa_s = mu_sea_mPas / 1000.0
    delta_ratio = 1.0 - rho_bub / rho_sea
    if delta_ratio <= 0:
        raise ValueError("Bubble is denser than seawater -- would sink, not rise.")

    U = 0.1
    for _ in range(max_iter):
        Re = U * Db_m * rho_sea / mu_pa_s
        Cd = _mei_drag_coefficient(Re)
        U_new = np.sqrt((4.0 / 3.0) * G * Db_m * delta_ratio / Cd)
        if abs(U_new - U) < tol * max(1.0, U):
            return U_new
        U = U_new
    return U


def predict_kL(Db_m: float, U_m_s: float, mu_sea_mPas: float) -> float:
    """Levich mobile-sphere k_L [m/s]. Reuses the existing Hayduk-Laudie
    diffusivity helper in mass_transfer.py rather than duplicating it."""
    D_gw = mass_transfer._diffusivity_co2_water_m2_s(mu_sea_mPas)
    return (2.0 / np.sqrt(np.pi)) * np.sqrt(D_gw * U_m_s / Db_m)


def predict_over_diameter_range(diameters_m, y_gas: tuple, T_K: float,
                                 P_bar: float, rho_sea: float,
                                 mu_sea_mPas: float) -> list:
    """Same diameter-sweep pattern as rigid_sphere.py, for direct
    side-by-side comparison. Velocity is now the self-consistent
    mobile-sphere (Mei et al. 1994) terminal velocity.
    """
    state = eos.mixture_density(y_gas, T_K, P_bar)
    rho_bub = state.density_kg_m3
    mu_pa_s = mu_sea_mPas / 1000.0
    D_gw = mass_transfer._diffusivity_co2_water_m2_s(mu_sea_mPas)
    Sc = mu_pa_s / (rho_sea * D_gw)

    results = []
    for Db in diameters_m:
        U = terminal_velocity_mobile(Db, rho_bub, rho_sea, mu_sea_mPas)
        kL = predict_kL(Db, U, mu_sea_mPas)
        Re = U * Db * rho_sea / mu_pa_s
        Eo = eotvos_number(Db, rho_sea, rho_bub)
        results.append({"Db_m": Db, "U_m_s": U, "Re": Re, "Pe": Re * Sc,
                         "kL_m_s": kL, "Eo": Eo, "sphere_theory_valid": Eo < 0.5})
    return results
