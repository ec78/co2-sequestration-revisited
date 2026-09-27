"""Peng-Robinson EOS for the CO2/N2 bubble mixture.

EQUATIONS_SPEC.md section 3. Single-phase-at-a-time treatment (no
liquid/vapor flash splitting the bubble into two coexisting phases), but
-- as of this revision -- with correct *stable-root selection* when the
cubic has three real roots: the root with the lower residual Gibbs energy
is chosen, not just the largest one. See `_select_stable_root` docstring
for why the earlier "always take the vapor root" version was wrong for
CO2-rich mixtures at depth.
"""

from dataclasses import dataclass

import numpy as np

from .constants import R_BAR, TC_K, PC_BAR, OMEGA, MOLAR_MASS

KAPPA = tuple(0.37464 + 1.54226 * w - 0.26992 * w**2 for w in OMEGA)

# Binary interaction parameter, CO2-N2. [RECONSTRUCTED, documented
# assumption] -- not given in the original; 0.0 is a common simplifying
# default. See EQUATIONS_SPEC.md section 3.
K_IJ = 0.0


@dataclass
class BubbleState:
    Z: float              # compressibility factor of the selected root
    molar_volume: float   # cm^3/mol
    density_kg_m3: float
    phase: str             # "vapor", "liquid", or "single" (only one root)


def _alpha(T_K: float) -> tuple:
    return tuple(
        (1.0 + KAPPA[i] * (1.0 - np.sqrt(T_K / TC_K[i]))) ** 2
        for i in range(2)
    )


def _a_i(T_K: float) -> tuple:
    alpha = _alpha(T_K)
    return tuple(
        0.45724 * R_BAR**2 * TC_K[i]**2 / PC_BAR[i] * alpha[i]
        for i in range(2)
    )


def _b_i() -> tuple:
    return tuple(0.07780 * R_BAR * TC_K[i] / PC_BAR[i] for i in range(2))


def _mixture_ab(y: tuple, T_K: float):
    """Returns (a_mix, b_mix, a_i, b_i, cross) where cross[i] = sum_j y_j
    sqrt(a_i a_j)(1-k_ij), needed by both the EOS and the fugacity calc.
    """
    y_co2, y_n2 = y
    a_i = _a_i(T_K)
    b_i = _b_i()

    cross = [0.0, 0.0]
    a_mix = 0.0
    ys = (y_co2, y_n2)
    for i in range(2):
        for j in range(2):
            term = ys[i] * ys[j] * np.sqrt(a_i[i] * a_i[j]) * (1 - K_IJ if i != j else 1.0)
            a_mix += term
    for i in range(2):
        for j in range(2):
            cross[i] += ys[j] * np.sqrt(a_i[i] * a_i[j]) * (1 - K_IJ if i != j else 1.0)
    b_mix = y_co2 * b_i[0] + y_n2 * b_i[1]

    return a_mix, b_mix, a_i, b_i, cross


def _residual_gibbs_RT(Z: float, A: float, B: float) -> float:
    """Residual (departure) Gibbs energy / RT for a PR EOS root. The
    thermodynamically stable root among several real roots is the one
    that MINIMIZES this quantity (equivalently, minimizes fugacity) --
    standard cubic-EOS phase-stability criterion.
    """
    return (
        (Z - 1.0) - np.log(Z - B)
        - (A / (2 * np.sqrt(2) * B))
        * np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B))
    )


def _real_roots_above_B(A: float, B: float) -> list:
    coeffs = [1.0, -(1.0 - B), A - 3 * B**2 - 2 * B, -(A * B - B**2 - B**3)]
    roots = np.roots(coeffs)
    return [r.real for r in roots if abs(r.imag) < 1e-8 and r.real > B]


def _select_stable_root(A: float, B: float, force_vapor: bool = False) -> tuple:
    """Returns (Z, phase_label).

    [BUG FIX, this revision] The cubic Z^3 - (1-B)Z^2 + (A-3B^2-2B)Z -
    (AB-B^2-B^3) = 0 can have one or three real roots > B. With three
    real roots (common for CO2-rich mixtures below CO2's saturation
    pressure at ocean temperatures -- verified numerically for this
    model's own 300-1500 m scenario matrix), the largest root is the
    metastable/unstable "vapor" branch and the smallest is the stable
    liquid branch, or vice versa depending on conditions; picking the
    largest unconditionally (the previous version of this function) gives
    the wrong phase whenever liquid is actually stable, which is exactly
    the regime the original report's own Chapter 2 identifies as
    important (CO2 approaching its liquefaction boundary). The correct
    selection minimizes residual Gibbs energy across the candidate roots.

    force_vapor: when True, always return the largest real root instead
    of the stable one. Used for the hydrate-coated regime (mass_transfer
    Method H / EQUATIONS_SPEC.md section 6), where a hydrate shell is
    assumed to kinetically trap the bubble core in a vapor-like state
    rather than letting it equilibrate to bulk liquid CO2.
    """
    real_roots = _real_roots_above_B(A, B)
    if not real_roots:
        raise ValueError(f"No valid PR EOS root: A={A}, B={B}")
    if len(real_roots) == 1:
        return real_roots[0], "single"

    if force_vapor:
        return max(real_roots), "vapor_forced"

    g = [_residual_gibbs_RT(z, A, B) for z in real_roots]
    order = sorted(range(len(real_roots)), key=lambda i: g[i])
    z_stable = real_roots[order[0]]
    label = "vapor" if z_stable == max(real_roots) else "liquid"
    return z_stable, label


def mixture_density(y: tuple, T_K: float, P_bar: float,
                     force_vapor: bool = False) -> BubbleState:
    """y = (y_CO2, y_N2) mole fractions. Returns the thermodynamically
    stable-phase bubble state at this T, P (see _select_stable_root),
    unless force_vapor is set (hydrate-coated regime)."""
    y_co2, y_n2 = y
    a_mix, b_mix, _, _, _ = _mixture_ab(y, T_K)

    A = a_mix * P_bar / (R_BAR * T_K) ** 2
    B = b_mix * P_bar / (R_BAR * T_K)

    Z, phase = _select_stable_root(A, B, force_vapor=force_vapor)

    V_molar = Z * R_BAR * T_K / P_bar  # cm^3/mol
    M_mix = y_co2 * MOLAR_MASS[0] + y_n2 * MOLAR_MASS[1]  # g/mol
    density = (M_mix / V_molar) * 1000.0  # g/cm^3 -> kg/m^3

    return BubbleState(Z=Z, molar_volume=V_molar, density_kg_m3=density, phase=phase)


def fugacity_coefficient_co2(y: tuple, T_K: float, P_bar: float) -> float:
    """Fugacity coefficient of CO2 in the (stable-phase) mixture, for the
    solubility module's high-pressure Henry's-law correction.
    """
    y_co2, y_n2 = y
    a_mix, b_mix, a_i, b_i, cross = _mixture_ab(y, T_K)

    state = mixture_density((y_co2, y_n2), T_K, P_bar)
    Z = state.Z
    A = a_mix * P_bar / (R_BAR * T_K) ** 2
    B = b_mix * P_bar / (R_BAR * T_K)

    b0_ratio = b_i[0] / b_mix
    a0_term = (2 * cross[0] / a_mix) - b0_ratio

    ln_phi = (b0_ratio * (Z - 1) - np.log(Z - B)
              - (A / (2 * np.sqrt(2) * B)) * a0_term
              * np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B)))
    return float(np.exp(ln_phi))
