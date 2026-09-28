"""P-GLAD J-tube hydraulic model. PGLAD_SPEC.md sections 1-4.

Couples a two-phase (Beggs & Brill) upriser to a single-phase downriser
and solves for the water flow rate the gas-lift effect can sustain, via
a shooting method matching ambient hydrostatic pressure at both open
ends -- reproducing the original 2002 report's own stated method
("guess and check... setting the pressures at the bottom of the upriser
and the bottom of the downriser to correct hydrostatic pressures").

Geometry and inputs match the original's own worked example exactly
(thesis_full_text.txt lines ~1250-1295, Table 5-1): 0.5 m diameter pipe,
200 m upriser (injection at 300 m, top at 100 m), 900 m downriser (top
at 100 m, discharge at 1000 m), 5 kg/s gas injection, 95% CO2 / 5% N2.

Scope, stated explicitly: this is a HYDRAULICS-ONLY reimplementation.
Gas and liquid mass flow rates are each held constant along the upriser
(no dissolution coupling) -- the original's Table 5-1 shows the liquid
volumetric flow rate increasing by about 20% between injection and the
top of the upriser, far more than seawater density variation over that
depth range could explain, implying Saito et al.'s underlying model
includes a water-entrainment or mass-transfer-coupling mechanism beyond
what the 2002 thesis's own equations (3-1 to 3-23) specify. That
mechanism isn't recoverable from the source available to this project
(the thesis's simplified presentation, not Saito et al.'s own full
paper -- see PGLAD_SPEC.md section 5 for the validation comparison this
produces and how it's read honestly).
"""

import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "co2n2_bubble"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from co2n2_bubble import seawater, eos  # noqa: E402
from pglad import beggs_brill as bb  # noqa: E402

G = 9.81
SIGMA_SEAWATER = 0.074  # N/m -- representative seawater surface tension;
# not given in the original source, a documented assumption (consistent
# with this project's practice of flagging unavailable parameters rather
# than silently picking one -- see EQUATIONS_SPEC.md section 3 for the
# precedent, k_ij=0 for the Peng-Robinson mixing rule).


def _ambient(depth_m: float):
    """Ambient seawater T [K], P [Pa], rho [kg/m^3], mu [Pa s] at depth."""
    T = seawater.temperature_K(depth_m)
    P_bar = seawater.pressure_bar(depth_m)
    rho = seawater.density_kg_m3(depth_m)
    mu_mPas = seawater.viscosity_mPa_s(depth_m)
    return T, P_bar * 1e5, rho, mu_mPas * 1e-3


def integrate_upriser(mdot_gas: float, mdot_water: float, y_gas: tuple,
                       D: float, z_bottom: float, z_top: float,
                       n_sections: int = 40) -> float:
    """Marches from the (known) bottom pressure up to z_top, section by
    section (matching the original's own 5 m-scale explicit marching),
    returns the computed pressure at z_top [Pa].
    """
    A = np.pi * (D / 2) ** 2
    T_bottom, P_bottom, rho_l_bottom, mu_l_bottom = _ambient(z_bottom)

    z = z_bottom
    P = P_bottom
    dz = (z_bottom - z_top) / n_sections  # positive, we step upward (z decreases)

    for _ in range(n_sections):
        T, _, rho_l, mu_l = _ambient(z)  # ambient T/rho_l as local pipe proxies
        gas_state = eos.mixture_density(y_gas, T, P / 1e5)
        rho_g = gas_state.density_kg_m3
        mu_g = 1.5e-5  # Pa s, representative gas viscosity (CO2/N2 at these
        # conditions varies little around this value; not separately modeled)

        Q_l = mdot_water / rho_l
        Q_g = mdot_gas / rho_g
        v_sl = Q_l / A
        v_sg = Q_g / A

        dpdz = bb.pressure_gradient(v_sl, v_sg, rho_l, rho_g, SIGMA_SEAWATER,
                                     mu_l, mu_g, D, uphill=True)
        P = P - dpdz * dz  # pressure decreases moving upward
        z = z - dz

    return P


def integrate_downriser(mdot_water: float, P_top: float, D: float,
                         z_top: float, z_bottom: float,
                         n_sections: int = 40) -> float:
    """Single-phase (CO2-saturated seawater) downriser -- per the
    original's own description, all gas has dissolved or vented by the
    top of the upriser. Marches from z_top (known, from the upriser
    solution) down to z_bottom, returns computed pressure there [Pa].
    """
    A = np.pi * (D / 2) ** 2
    z = z_top
    P = P_top
    dz = (z_bottom - z_top) / n_sections  # positive, stepping downward

    for _ in range(n_sections):
        _, _, rho_l, mu_l = _ambient(z)
        v = mdot_water / (rho_l * A)
        Re = rho_l * v * D / mu_l
        f = bb._moody_friction_factor(Re)
        dpdz = rho_l * G + f * rho_l * v**2 / (2 * D)
        P = P + dpdz * dz  # pressure increases moving downward
        z = z + dz

    return P


def solve_water_flow_rate(mdot_gas: float, y_gas: tuple, D: float,
                           z_injection: float, z_upriser_top: float,
                           z_downriser_bottom: float,
                           mdot_water_bracket=(1.0, 2000.0)) -> dict:
    """Shooting method: find the water mass flow rate [kg/s] for which
    the downriser's computed bottom pressure matches the true ambient
    hydrostatic pressure at z_downriser_bottom.
    """
    _, P_target, _, _ = _ambient(z_downriser_bottom)

    def residual(mdot_water):
        P_top = integrate_upriser(mdot_gas, mdot_water, y_gas, D,
                                   z_injection, z_upriser_top)
        P_bottom = integrate_downriser(mdot_water, P_top, D,
                                        z_upriser_top, z_downriser_bottom)
        return P_bottom - P_target

    mdot_water = brentq(residual, *mdot_water_bracket, xtol=1e-3)
    P_top = integrate_upriser(mdot_gas, mdot_water, y_gas, D,
                               z_injection, z_upriser_top)

    return {"mdot_water_kg_s": mdot_water, "P_top_pa": P_top,
            "P_target_bottom_pa": P_target}
