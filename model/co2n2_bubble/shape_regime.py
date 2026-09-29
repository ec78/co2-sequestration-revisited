"""Shape-regime-aware bubble terminal velocity and mass transfer.

EQUATIONS_SPEC.md section 5b. Brings the strongest result of
../../mass-transfer-study/ (its own model/deformed_bubble.py) into the main
thesis model: at the ~1 cm bubble sizes this model's own scenario matrix
covers, real bubbles are not spherical (Eotvos number 0.5-100+, per
eotvos_number below applied to this model's own density/surface-tension
values) -- they deform to ellipsoidal or spherical-cap shapes, which rise
faster and transfer mass differently than the rigid-sphere theory
Sections 5/6 assume throughout.

This module does not re-derive anything -- it re-exports the same two
independently-verified closed-form results the mass-transfer study already
validated against a real literature coefficient (Saito et al. 2000, matched
to within 1% at a plausible bubble size -- see
../../mass-transfer-study/analysis/phase_f_deformed_bubble.md):

- **Ellipsoidal / wobbling** (0.5 <= Eo < 40): Mendelson's (1967)
  wave-analogy terminal velocity, U = sqrt(2 sigma/(rho_L Db) + g Db/2).
- **Spherical cap** (Eo >= 40): Davies & Taylor's (1950) result,
  U = (2/3) sqrt(g R), R = Db/2 (equivalent-volume-sphere radius).

Regime thresholds (Eo < 0.5 spherical, 0.5-40 ellipsoidal, >= 40 cap) are
the same commonly-cited Clift-Grace-Weber (1978) thresholds
mass-transfer-study/model/deformed_bubble.py uses -- not re-derived here.

**Design decision (this integration, not present in the study): the
spherical->deformed swap only applies to bubbles with an intact,
mobile fluid interface.** A hydrate-coated bubble (bubble_model.py's
"Method H" regime) is physically the opposite case -- a rigid clathrate
shell is the whole premise of that regime (EQUATIONS_SPEC.md section 6),
and neither Mendelson's nor Davies & Taylor's derivation has any basis for
a solid-shelled particle (both assume a responsive, deformable gas-liquid
interface, either as a capillary-gravity wave analogy or as potential flow
matched to a fluid cap). So hydrate-active steps keep the existing
rigid-sphere rise-velocity ODE (bubble_model.solve_rise_velocity)
regardless of Eotvos number -- the rigid-sphere assumption is *more*
physically appropriate there, not less, than anywhere else in this model.
See bubble_model.py's per-step dispatch and EQUATIONS_SPEC.md section 5b
for the full reasoning.

**Quasi-steady design decision, verified numerically (not just asserted):**
Mendelson's and Davies & Taylor's formulas are algebraic terminal-velocity
results, not a force-balance ODE that could be time-stepped the way the
rigid-sphere Eq. 4-4 iteration is -- so applying them inside this model's
transient loop requires treating rise velocity as quasi-steady at each
timestep (re-equilibrating to the new regime-correct terminal velocity
every step, rather than relaxing toward it). Checked directly: sub-stepping
the *existing* rigid-sphere ODE from rest (U=0) at representative
mid-scenario-matrix conditions (1 cm bubble, 1000 m, 50% CO2) reaches
within 1% of its own terminal velocity in ~0.13 s -- over 15x faster than
this model's own 2 s per-step timestep, and 3-4 orders of magnitude faster
than a typical full simulated rise (hundreds to ~1800 s in this model's
existing demo runs, analysis/demo_*.csv). Since the rigid-sphere case is
if anything the *slower*-relaxing of the regimes here (a bare force
balance with no analog of the ellipsoidal/cap formulas' near-instantaneous
wave/potential-flow response), this is a conservative check -- the
deformed regimes relax at least as fast. Quasi-steady swapping is
therefore a well-justified simplification at this model's timestep, not an
unverified convenience.
"""

import numpy as np

G = 9.81

EO_SPHERICAL_MAX = 0.5
EO_ELLIPSOIDAL_MAX = 40.0


def eotvos_number(Db_m: float, rho_sea: float, rho_bub: float,
                   sigma_l: float) -> float:
    """Eo = g |rho_sea - rho_bub| Db^2 / sigma -- governs whether a bubble
    stays spherical (Eo << 1) or deforms to ellipsoidal/spherical-cap
    (Eo >~ 1). Same definition as
    mass-transfer-study/model/mobile_sphere.eotvos_number.
    """
    return G * abs(rho_sea - rho_bub) * Db_m**2 / sigma_l


def shape_regime(Eo: float) -> str:
    if Eo < EO_SPHERICAL_MAX:
        return "spherical"
    elif Eo < EO_ELLIPSOIDAL_MAX:
        return "ellipsoidal"
    else:
        return "cap"


def terminal_velocity_mendelson(Db_m: float, rho_sea: float, sigma_l: float) -> float:
    """Mendelson (1967) ellipsoidal/wobbling-regime terminal velocity."""
    return np.sqrt(2 * sigma_l / (rho_sea * Db_m) + G * Db_m / 2.0)


def terminal_velocity_davies_taylor(Db_m: float) -> float:
    """Davies & Taylor (1950) spherical-cap terminal velocity."""
    R = Db_m / 2.0
    return (2.0 / 3.0) * np.sqrt(G * R)


def deformed_kL(Db_m: float, U_m_s: float, D_gw_m2_s: float) -> float:
    """Levich penetration-theory k_L [m/s] with a regime-correct velocity
    substituted in, for the ellipsoidal/cap regimes -- same formula and
    same reasoning as mass-transfer-study/model/mobile_sphere.predict_kL
    and deformed_bubble.py (standard practice: penetration theory applies
    broadly across mobile/circulating-interface regimes, and both deformed
    regimes circulate strongly regardless of surface contamination state --
    see this module's docstring and EQUATIONS_SPEC.md section 5b for why
    this differs from the rigid-sphere Sherwood correlation Method A uses
    in the spherical regime). Takes D_gw directly (rather than importing
    mass_transfer's diffusivity helper) to avoid a circular import --
    mass_transfer.py imports this module for regime dispatch.
    """
    return (2.0 / np.sqrt(np.pi)) * np.sqrt(D_gw_m2_s * U_m_s / Db_m)
