"""Main time-stepping simulation loop.

EQUATIONS_SPEC.md section 7. Mirrors the structure of the original MATLAB
driver (../../original/appendix_a_original.m) step for step, with the
convergence-check fix noted in solve_rise_velocity's docstring.
"""

from dataclasses import dataclass, field

import numpy as np

from . import eos, seawater, solubility, mass_transfer
from .constants import G, MOLAR_MASS


def solve_rise_velocity(U_prev: float, Db_m: float, psi: float, gamma: float,
                         rho_sea: float, mu_sea_mPas: float, dt: float,
                         U_guess: float, max_iter: int = 100) -> float:
    """Eq. 4-4, solved iteratively against the Reynolds number, as in the
    original. [MINOR FIX] the original's convergence check is a bare
    `ReGuess - ReCalc > 1`, which can under-converge if ReCalc exceeds
    ReGuess (asymmetric). This implementation checks abs(ReGuess - ReCalc)
    against a small tolerance instead, which preserves the original's
    intent (iterate to a fixed point) more robustly. Flagged here rather
    than silently changed.
    """
    mu_pa_s = mu_sea_mPas / 1000.0
    U_new = U_guess

    for _ in range(max_iter):
        Re_guess = U_new * Db_m * rho_sea / mu_pa_s
        Cd = (24.0 / Re_guess) * (1 + 0.173 * Re_guess**0.657) + \
            0.413 / (1 + 16300 * Re_guess**-1.09)

        a = dt * (0.75 * psi * (Cd / Db_m))
        b = 1.0
        c = -U_prev - dt * (psi * (1 - gamma) * G)

        roots = np.roots([a, b, c])
        positive = [r.real for r in roots if abs(r.imag) < 1e-9 and r.real > 0]
        if not positive:
            raise ValueError("No positive rise-velocity root found")
        U_candidate = max(positive)

        Re_calc = U_candidate * Db_m * rho_sea / mu_pa_s
        if abs(Re_guess - Re_calc) < 1e-6 * max(1.0, Re_guess):
            return U_candidate
        U_new = U_candidate

    return U_new  # best effort if it doesn't tighten further


@dataclass
class SimulationResult:
    time_s: list = field(default_factory=list)
    depth_m: list = field(default_factory=list)
    diameter_m: list = field(default_factory=list)
    velocity_m_s: list = field(default_factory=list)
    co2_mole_frac: list = field(default_factory=list)
    rho_bubble: list = field(default_factory=list)
    rho_seawater: list = field(default_factory=list)
    mass_co2_lost_kg: list = field(default_factory=list)
    percent_co2_lost: list = field(default_factory=list)


def simulate(depth0_m: float, co2_frac0: float, diameter0_m: float,
             dt_s: float = 2.0, mass_transfer_method: str = "B",
             hydrate_model: bool = True,
             max_steps: int = 20000) -> SimulationResult:
    """Run the single-bubble release simulation.

    depth0_m: initial injection depth, m
    co2_frac0: initial CO2 mole fraction (0-1); balance is N2
    diameter0_m: initial bubble diameter, m
    mass_transfer_method: "A" or "B" -- used whenever the bubble is
        outside the hydrate window (or hydrate_model=False).
    hydrate_model: if True (default), CO2-rich bubbles at depth (see
        mass_transfer.in_hydrate_window) are kept on the forced-vapor EOS
        root and dissolve via Method H instead, per EQUATIONS_SPEC.md
        section 6. Set False to get the simpler, hydrate-agnostic model
        used in the first Phase 3 pass.
    """
    result = SimulationResult()

    depth = depth0_m
    Db = diameter0_m
    y = (co2_frac0, 1.0 - co2_frac0)
    U_prev = 0.0
    U_guess = 0.05

    # Initial moles in the bubble, from PR EOS molar volume.
    T = seawater.temperature_K(depth)
    P = seawater.pressure_bar(depth)
    force_vapor0 = hydrate_model and mass_transfer.in_hydrate_window(depth, y[0])
    state = eos.mixture_density(y, T, P, force_vapor=force_vapor0)
    volume_m3 = (np.pi / 6.0) * Db**3
    n_total = volume_m3 * 1e6 / state.molar_volume  # mol
    n_co2 = y[0] * n_total
    n_n2 = y[1] * n_total
    co2_mass_orig_kg = n_co2 * MOLAR_MASS[0] / 1000.0
    cumulative_mass_lost_kg = 0.0

    t = 0.0
    for step in range(max_steps):
        if depth <= 0 or Db <= 0 or n_co2 <= 0:
            break

        T = seawater.temperature_K(depth)
        P = seawater.pressure_bar(depth)
        rho_sea = seawater.density_kg_m3(depth)
        mu_sea = seawater.viscosity_mPa_s(depth)
        hydrate_active = hydrate_model and mass_transfer.in_hydrate_window(depth, y[0])
        state = eos.mixture_density(y, T, P, force_vapor=hydrate_active)
        rho_bub = state.density_kg_m3
        x_gs = solubility.solubility_mass_fraction(y, T, P)

        psi = rho_sea / (rho_bub + 0.5 * rho_sea)
        gamma = rho_bub / rho_sea

        U_new = solve_rise_velocity(U_prev, Db, psi, gamma, rho_sea, mu_sea,
                                     dt_s, U_guess)

        active_method = "H" if hydrate_active else mass_transfer_method
        rate_mol_s = mass_transfer.dissolution_rate(
            active_method, Db_m=Db, x_co2=y[0], U_m_s=U_new,
            rho_sea=rho_sea, mu_sea_mPas=mu_sea, T_K=T, x_gs=x_gs,
            rho_bub=rho_bub,
        )
        moles_lost = min(rate_mol_s * dt_s, n_co2)

        new_depth = depth - U_new * dt_s
        n_co2_new = n_co2 - moles_lost
        n_total_new = n_co2_new + n_n2
        y_new = (n_co2_new / n_total_new, n_n2 / n_total_new) if n_total_new > 0 else (0.0, 1.0)

        mass_lost_step_kg = moles_lost * MOLAR_MASS[0] / 1000.0
        cumulative_mass_lost_kg += mass_lost_step_kg
        percent_lost = (cumulative_mass_lost_kg / co2_mass_orig_kg) * 100.0 if co2_mass_orig_kg > 0 else 0.0

        # New bubble diameter: re-flash new composition at new depth's T,P.
        if new_depth > 0 and n_total_new > 0:
            T_new = seawater.temperature_K(new_depth)
            P_new = seawater.pressure_bar(new_depth)
            force_vapor_new = hydrate_model and mass_transfer.in_hydrate_window(new_depth, y_new[0])
            state_new = eos.mixture_density(y_new, T_new, P_new, force_vapor=force_vapor_new)
            volume_new_m3 = n_total_new * state_new.molar_volume / 1e6
            Db_new = (6.0 * volume_new_m3 / np.pi) ** (1.0 / 3.0)
        else:
            Db_new = 0.0

        result.time_s.append(t)
        result.depth_m.append(depth)
        result.diameter_m.append(Db)
        result.velocity_m_s.append(U_new)
        result.co2_mole_frac.append(y[0])
        result.rho_bubble.append(rho_bub)
        result.rho_seawater.append(rho_sea)
        result.mass_co2_lost_kg.append(cumulative_mass_lost_kg)
        result.percent_co2_lost.append(percent_lost)

        depth = new_depth
        Db = Db_new
        y = y_new
        n_co2 = n_co2_new
        n_total = n_total_new
        U_prev = U_new
        U_guess = U_new
        t += dt_s

    return result
