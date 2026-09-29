"""Series (shell + external-boundary-layer) resistance test for
hydrate-coated dissolution. STUDY_PLAN.md Phase G.

Phase D's working hypothesis for the hydrate-coated bucket's ~2.9-order-
of-magnitude residual scatter (../analysis/phase_d_findings.md) was that
flow affects the hydrate *shell itself* (thickness/growth), not the
simple diffusion-through-a-fixed-shell picture Method H implements. This
module tests the most standard, most directly implementable candidate
mechanism for how flow could matter even with an unchanged shell: a
classic two-film/series-resistance picture, where the OUTER liquid-side
convective boundary layer around the hydrate-coated bubble is a second
resistance in series with the shell's own diffusive resistance --
exactly the framing Ogasawara, Yamasaki & Teng (2001, Energy & Fuels
15:147-150) report using ("the mass-transfer coefficient was evaluated
on the basis of a series-mass-transfer model") for CO2 drops with a
hydrate shell in a water-tunnel experiment that directly measured
increasing shrinkage rate with increasing water velocity -- the same
directional effect Hirai et al.'s forced-flow vs. Fujioka et al.'s
quiescent data already suggested (phase_d_findings.md), now corroborated
by a second, independently-retrieved primary source built specifically
to test this.

This does NOT require any new correlation-fitting: it reuses two
pieces this project has already built and validated --
- The shell's own diffusive resistance, backed out from Method H's
  existing literature-sourced constant rate
  (../../model/co2n2_bubble/mass_transfer.method_h_rate, Fujioka et al.
  1994), re-expressed as an equivalent mass-transfer coefficient
  kL_shell on the SAME driving-force basis (rho_sea * x_gs) Method A
  already uses -- the standard convention for combining resistances in
  series (both terms must share one concentration-difference basis for
  1/k_overall = 1/k1 + 1/k2 to be meaningful; see module functions below
  for exactly how this is done and flagged as a modeling choice, not a
  recovered original relationship).
- The external convective coefficient, via the *existing* rigid-sphere
  Sherwood correlation (mass_transfer.method_a_kL, regime="spherical")
  -- appropriate here specifically because a hydrate shell is a rigid
  interface, the same reasoning already used to keep hydrate-active
  bubbles on rigid-sphere rise-velocity treatment in this project's main
  model (EQUATIONS_SPEC.md section 5b) rather than the shape-deformed
  treatment used elsewhere.

Result, reported in full in ../analysis/phase_g_series_resistance.md: at
physically representative bubble sizes/depths, the shell resistance
dominates so heavily that this mechanism predicts at most ~1.2-1.4x
enhancement from quiescent to fast forced flow (0.05 to 3 m/s) -- a real,
useful NEGATIVE result. The literature-reported enhancement (Hirai's
forced-flow flux vs. Fujioka's quiescent flux, or the full hydrate-coated
bucket's spread) is substantially larger than that. External boundary-
layer resistance, tested quantitatively rather than just asserted
plausible, is therefore NOT sufficient on its own to explain the observed
flow-sensitivity -- strengthening, not resolving, the case that the
hydrate shell's own properties (thickness, defects, or collapse/regrowth
dynamics -- see Teng, Yamasaki & Shindo, 1996, on hydrate-layer
compositional instability) are what actually respond to flow.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble import eos, mass_transfer, seawater, solubility  # noqa: E402


def shell_kL_equivalent(Db_m: float, depth_m: float, y_gas: tuple = (1.0, 0.0)) -> float:
    """Back out an equivalent shell mass-transfer coefficient [m/s] from
    Method H's existing constant-rate model (Fujioka et al. 1994), on the
    same (rho_sea * x_gs) driving-force basis Method A uses.

    **Modeling choice, not a recovered original relationship**: Method
    H's own rate is a literature-reported constant diameter-shrinkage
    rate, independent of x_gs by construction (EQUATIONS_SPEC.md section
    6). Re-expressing it as flux / (rho_sea * x_gs) is the standard way to
    put two transfer coefficients meant to be summed as series resistances
    onto one common concentration-difference basis -- it does NOT imply
    Method H's underlying rate is secretly x_gs-dependent; it is a
    bookkeeping convention for this comparison only, flagged explicitly
    per this project's practice of distinguishing genuine model equations
    from convenience conventions used in a specific analysis.
    """
    T_K = seawater.temperature_K(depth_m)
    P_bar = seawater.pressure_bar(depth_m)
    rho_sea = seawater.density_kg_m3(depth_m)
    x_gs = solubility.solubility_mass_fraction(y_gas, T_K, P_bar)
    state = eos.mixture_density(y_gas, T_K, P_bar, force_vapor=True)
    rho_bub = state.density_kg_m3

    rate_mol_s = mass_transfer.method_h_rate(Db_m, rho_bub)
    mass_rate_kg_s = rate_mol_s * 44.01 / 1000.0
    flux_kg_m2_s = mass_rate_kg_s / (np.pi * Db_m**2)
    return flux_kg_m2_s / (rho_sea * x_gs)


def external_kL(Db_m: float, U_m_s: float, depth_m: float) -> float:
    """External convective mass-transfer coefficient [m/s] around a
    hydrate-shelled (rigid-interface) bubble, via the existing rigid-
    sphere Sherwood correlation -- the same regime choice this project's
    main model already uses for hydrate-active bubbles
    (EQUATIONS_SPEC.md section 5b: a hydrate shell has no deformable
    interface for shape theory to apply to).
    """
    T_K = seawater.temperature_K(depth_m)
    rho_sea = seawater.density_kg_m3(depth_m)
    mu_sea = seawater.viscosity_mPa_s(depth_m)
    return mass_transfer.method_a_kL(Db_m, U_m_s, rho_sea, mu_sea, T_K, regime="spherical")


def k_overall_series(kL_shell: float, kL_external: float) -> float:
    """Classic two-resistances-in-series combination:
    1/k_overall = 1/k_shell + 1/k_external.
    """
    return 1.0 / (1.0 / kL_shell + 1.0 / kL_external)


def enhancement_over_velocity_range(Db_m: float, depth_m: float,
                                     velocities_m_s, y_gas: tuple = (1.0, 0.0)) -> list:
    """For a fixed bubble size/depth, how much does the series-resistance
    k_overall rise above the shell-alone (Method H) rate as external flow
    velocity increases? Returns a list of dicts (U_m_s, kL_external,
    k_overall, enhancement_over_shell_alone).
    """
    kL_shell = shell_kL_equivalent(Db_m, depth_m, y_gas)
    results = []
    for U in velocities_m_s:
        kL_ext = external_kL(Db_m, U, depth_m)
        k_overall = k_overall_series(kL_shell, kL_ext)
        results.append({
            "U_m_s": U,
            "kL_shell": kL_shell,
            "kL_external": kL_ext,
            "k_overall": k_overall,
            "enhancement_over_shell_alone": k_overall / kL_shell,
        })
    return results
