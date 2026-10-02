"""Beggs & Brill (1973) two-phase pipe-flow pressure-gradient correlation.

EQUATIONS_SPEC.md section 9 (P-GLAD) -- [MODERNIZED]. The original 2002
report's upriser model used the Govier & Aziz (1972) two-phase friction
factor correlation, presented in that source as a graphical
correlation (friction factor vs. a reduced liquid Reynolds number,
read off a chart) rather than a closed-form equation -- not usable
without the original 1972 book, which isn't accessible for this project
(no institutional library access, same constraint as everywhere else in
this repo).

Beggs & Brill (1973) is substituted instead: a fully closed-form, still
-standard two-phase pipe-flow correlation from the same petroleum-
engineering tradition (this is, after all, a Petroleum Engineering
department report) and well suited to the P-GLAD upriser's near-vertical
gas-lift flow. Includes the Payne et al. (1979) holdup correction, a
widely-used refinement of the original 1973 correlation's known
holdup-overprediction tendency.

Provenance: the primary 1973 paper (Journal of Petroleum Technology,
May 1973) isn't accessible either. Coefficients here come from an
independent open-source implementation (PressureDrop.jl,
github.com/jnoynaert/PressureDrop.jl, src/pressurecorrelations.jl),
cross-validated against a second independent source (a technical wiki
reproducing the same holdup correlation coefficients and flow-regime
boundary constants) for every coefficient that source covered -- all
matched exactly. The inclination-correction (e, f, g, h) coefficients
and the Payne correction factors were not independently re-confirmed
against a second source; flagged as resting on the one verified
implementation, same honesty standard as duan_sun.py's provenance note
in ../co2n2_bubble/duan_sun.py.

**License correction (pre-publication provenance audit)**: this
docstring previously, incorrectly, described PressureDrop.jl as
MIT-licensed. Checked directly against the live repository's LICENSE
file: it is **Apache License 2.0**, copyright Jared M. Noynaert (2019).
The MIT claim here was never accurate -- flagged and fixed rather than
quietly corrected, since the earlier session that wrote this docstring
apparently never verified the license it cited. Apache-2.0 carries
different obligations than MIT (notably: state changes made to any
modified file, and preserve the copyright/license notices), which this
repo does not yet satisfy -- see the top-level LICENSE/NOTICE situation,
still unresolved as of this correction.

All formulas here are in SI units (the source implementation uses US
field units bundled with unit-conversion constants; this module uses the
underlying dimensionless-group definitions directly, which are
unit-system-independent).
"""

import numpy as np

G = 9.81  # m/s^2

_BB_COEFFICIENTS = {
    "segregated": dict(a=0.980, b=0.4846, c=0.0868, e=0.011, f=-3.768, g=3.539, h=-1.614),
    "intermittent": dict(a=0.845, b=0.5351, c=0.0173, e=2.960, f=0.305, g=-0.4473, h=0.0978),
    "distributed": dict(a=1.065, b=0.5824, c=0.0609),
    "downhill": dict(e=4.700, f=-0.3692, g=0.1244, h=-0.5056),
}

_PAYNE_UPHILL = 0.924
_PAYNE_DOWNHILL = 0.685


def flow_pattern(lambda_l: float, N_Fr: float) -> str:
    """Beggs & Brill flow-regime map from no-slip liquid holdup and
    mixture Froude number."""
    L1 = 316.0 * lambda_l**0.302
    L2 = 9.25e-4 * lambda_l**-2.468
    L3 = 0.1 * lambda_l**-1.4516
    L4 = 0.5 * lambda_l**-6.738

    if N_Fr < L1 and N_Fr < L2:
        return "segregated"
    elif L2 <= N_Fr < L3:
        return "transition"
    elif N_Fr >= L1 or N_Fr >= L4:
        return "distributed"
    else:
        return "intermittent"


def _horizontal_holdup(pattern: str, lambda_l: float, N_Fr: float) -> float:
    c = _BB_COEFFICIENTS[pattern]
    return c["a"] * lambda_l**c["b"] / N_Fr**c["c"]


def _inclination_factor(pattern: str, lambda_l: float, N_Fr: float,
                         N_lv: float, uphill: bool) -> float:
    """Vertical-pipe (alpha = 90 deg) inclination correction psi.
    P-GLAD's upriser/downriser are vertical, so this module only
    implements the vertical case (alpha ~ 0 rad from vertical -> the
    "vertical flow" branch of the general inclined-pipe formula)."""
    if uphill and pattern == "distributed":
        return 1.0

    coeffs = _BB_COEFFICIENTS["downhill"] if not uphill else _BB_COEFFICIENTS[pattern]
    C = max((1 - lambda_l) * np.log(coeffs["e"] * lambda_l**coeffs["f"]
                                     * N_lv**coeffs["g"] * N_Fr**coeffs["h"]), 0.0)
    return 1.0 + 0.3 * C  # vertical-pipe form


def liquid_holdup(lambda_l: float, N_Fr: float, N_lv: float, uphill: bool,
                   payne_correction: bool = True) -> float:
    """Adjusted (inclination-corrected) in-situ liquid holdup."""
    pattern = flow_pattern(lambda_l, N_Fr)

    if pattern == "transition":
        L2 = 9.25e-4 * lambda_l**-2.468
        L3 = 0.1 * lambda_l**-1.4516
        B = (L3 - N_Fr) / (L3 - L2)
        eps_seg = _horizontal_holdup("segregated", lambda_l, N_Fr) * \
            _inclination_factor("segregated", lambda_l, N_Fr, N_lv, uphill)
        eps_int = _horizontal_holdup("intermittent", lambda_l, N_Fr) * \
            _inclination_factor("intermittent", lambda_l, N_Fr, N_lv, uphill)
        eps = B * eps_seg + (1 - B) * eps_int
    else:
        eps_h = _horizontal_holdup(pattern, lambda_l, N_Fr)
        psi = _inclination_factor(pattern, lambda_l, N_Fr, N_lv, uphill)
        eps = eps_h * psi

    if payne_correction:
        eps *= _PAYNE_UPHILL if uphill else _PAYNE_DOWNHILL

    if uphill:
        eps = max(eps, lambda_l)  # true holdup >= no-slip holdup for uphill flow

    return eps


def _friction_factor_ratio(lambda_l: float, eps_l: float) -> float:
    """f_tp / f_n via the Beggs & Brill S-function."""
    y = lambda_l / eps_l**2
    if 1.0 < y < 1.2:
        s = np.log(2.2 * y - 1.2)
    else:
        ln_y = np.log(y)
        s = ln_y / (-0.0523 + 3.182 * ln_y - 0.872 * ln_y**2 + 0.01853 * ln_y**4)
    return np.exp(s)


def _moody_friction_factor(Re: float, relative_roughness: float = 1e-5) -> float:
    """Darcy friction factor: laminar below Re=2000, Colebrook-White
    (Serghide's explicit approximation) above -- standard, not specific
    to Beggs & Brill."""
    if Re < 2000:
        return 64.0 / Re
    k = relative_roughness
    A = -2 * np.log10(k / 3.7 + 12 / Re)
    B = -2 * np.log10(k / 3.7 + 2.51 * A / Re)
    C = -2 * np.log10(k / 3.7 + 2.51 * B / Re)
    return (A - (B - A) ** 2 / (C - 2 * B + A)) ** -2


def pressure_gradient(v_sl: float, v_sg: float, rho_l: float, rho_g: float,
                       sigma_l: float, mu_l: float, mu_g: float, D: float,
                       uphill: bool = True, payne_correction: bool = True,
                       relative_roughness: float = 1e-5) -> float:
    """Total pressure gradient dP/dz [Pa/m] (elevation + friction; the
    kinetic/acceleration term is omitted -- the original 2002 report's
    own treatment of this equation explicitly drops it as negligible for
    the J-tube, EQUATIONS_SPEC.md section 9). Positive = pressure
    increases in the direction of flow (i.e. going deeper).

    v_sl, v_sg: superficial liquid/gas velocities [m/s]
    rho_l, rho_g: phase densities [kg/m^3]
    sigma_l: gas-liquid interfacial tension [N/m]
    mu_l, mu_g: phase viscosities [Pa s]
    D: pipe internal diameter [m]
    """
    v_m = v_sl + v_sg
    lambda_l = v_sl / v_m
    N_Fr = v_m**2 / (G * D)
    N_lv = v_sl * (rho_l / (G * sigma_l)) ** 0.25

    eps_l = liquid_holdup(lambda_l, N_Fr, N_lv, uphill, payne_correction)

    rho_ns = rho_l * lambda_l + rho_g * (1 - lambda_l)
    mu_ns = mu_l * lambda_l + mu_g * (1 - lambda_l)
    Re_ns = rho_ns * v_m * D / mu_ns

    f_n = _moody_friction_factor(Re_ns, relative_roughness)
    f_tp = f_n * _friction_factor_ratio(lambda_l, eps_l)

    rho_m = rho_l * eps_l + rho_g * (1 - eps_l)

    dpdz_elevation = rho_m * G
    dpdz_friction = f_tp * rho_ns * v_m**2 / (2 * D)

    return dpdz_elevation + dpdz_friction
