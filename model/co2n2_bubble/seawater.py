"""Seawater temperature, pressure, density, and viscosity vs. depth.

EQUATIONS_SPEC.md section 2. Temperature-depth correlation is the
original's Eq. 4-6; pressure/density use the GSW/TEOS-10 toolbox in place
of the original's SEAWATER (Morgan, 1994) -- see spec for why.
"""

import gsw
import numpy as np

from .constants import REFERENCE_SALINITY_PSU, LATITUDE_DEG

_SIGMA_ATM_N_M = 0.074      # near-atmospheric CO2/N2-water IFT, N/m
_SIGMA_PLATEAU_N_M = 0.030  # high-pressure plateau, N/m
_SIGMA_P_SCALE_BAR = 40.0   # decay scale, bar


def temperature_K(depth_m: float) -> float:
    """Eq. 4-6: T(z) = 3946/(z+112) + 273.6, z in meters, T in Kelvin."""
    return 3946.0 / (depth_m + 112.0) + 273.6


def pressure_bar(depth_m: float, lat_deg: float = LATITUDE_DEG) -> float:
    """Absolute (not gauge) pressure at depth, in bar.

    gsw.p_from_z returns sea pressure in dbar relative to the surface
    (i.e. 0 at z=0); add standard atmospheric pressure to get absolute
    pressure, which is what the Peng-Robinson EOS needs.
    """
    p_sea_dbar = gsw.p_from_z(-depth_m, lat_deg)
    p_sea_bar = p_sea_dbar / 10.0
    return p_sea_bar + 1.01325


def density_kg_m3(depth_m: float, lat_deg: float = LATITUDE_DEG,
                   salinity_psu: float = REFERENCE_SALINITY_PSU) -> float:
    """In-situ seawater density at depth, kg/m^3, via TEOS-10."""
    p_sea_dbar = gsw.p_from_z(-depth_m, lat_deg)
    t_c = temperature_K(depth_m) - 273.15
    # Practical (~EOS-80-consistent) salinity treated as reference/absolute
    # salinity here; the distinction is well below this model's precision.
    SA = gsw.SR_from_SP(salinity_psu)
    CT = gsw.CT_from_t(SA, t_c, p_sea_dbar)
    return gsw.rho(SA, CT, p_sea_dbar)


def viscosity_mPa_s(depth_m: float,
                     salinity_psu: float = REFERENCE_SALINITY_PSU) -> float:
    """Seawater dynamic viscosity, mPa*s (= cP), vs. temperature/salinity.

    [RECONSTRUCTED] -- the original calls Find_Vissea(T), source not in
    the appendix (EQUATIONS_SPEC.md section 5). This uses the standard
    El-Dessouky & Ettouney (2002) seawater viscosity correlation, a
    widely cited closed form covering typical ocean temperature/salinity
    ranges -- not a recovered original formula.
    """
    t_c = temperature_K(depth_m) - 273.15
    s = salinity_psu / 1000.0  # mass fraction

    mu_w = (t_c + 246.0) / (
        (0.05594 * t_c + 5.2842) * t_c + 137.37
    )  # pure water viscosity, cP

    a = 1.474e-3 + 1.5e-5 * t_c - 3.927e-8 * t_c**2
    b = 1.0734e-5 - 8.5e-8 * t_c + 2.23e-10 * t_c**2
    mu_rel = 1.0 + a * s + b * s**2

    return mu_w * mu_rel


def interfacial_tension_N_m(depth_m: float) -> float:
    """CO2/N2-seawater interfacial tension, N/m. **[MODERNIZED]** --
    EQUATIONS_SPEC.md section 5b.

    The original 2002 model has no surface-tension parameter at all (it
    never needed one -- rigid-sphere theory throughout). This model needs
    one for the Eotvos number driving shape_regime.py's regime dispatch.
    mass-transfer-study/model/mobile_sphere.py used a flat placeholder
    (sigma_l = 0.074 N/m, pure-water-like) for the same purpose; this
    implementation instead sources a pressure-dependent treatment, since
    pressure is exactly the variable that changes across this model's own
    300-1500 m scenario matrix and the literature is unambiguous that CO2-
    water interfacial tension is strongly pressure-dependent, not constant.

    Two independent sources (retrieved and read, not recalled from model
    knowledge): Hebach et al. (2002, J. Chem. Eng. Data) measured CO2-water
    IFT dropping from ~72 mN/m near atmospheric pressure to ~30 mN/m by
    12-20 MPa (120-200 bar); Chalbaud et al. (2009, Energy Procedia / Adv.
    Water Resour.) report the same high-pressure plateau (~30 mN/m at
    308 K, ~23 mN/m at 383 K -- i.e. the plateau itself drops somewhat with
    *increasing* temperature) and found salinity's effect on it negligible
    (supporting reuse of a seawater-salinity-independent CO2-water value
    here, rather than a separate brine correlation).

    This function is a smooth two-parameter interpolation between those
    two endpoints (sigma_atm=0.074 N/m at P->0, sigma_plateau=0.030 N/m
    for P gtrsim 150-200 bar, exponential decay with scale 40 bar chosen so
    the transition matches the qualitative shape both sources report: most
    of the drop by ~100 bar, near-plateau by ~150-200 bar) -- **not** a
    digitized reproduction of either source's primary data (inaccessible;
    same constraint as everywhere else in this project), and **not** fit
    at this project's own ocean temperatures. Both cited studies validate
    their correlations over 293-398 K; this model's own Eq. 4-6 gives
    276-283 K across the 300-1500 m scenario matrix -- colder than either
    study's range. Surface tension generally *increases* as temperature
    falls, so this extrapolation most likely runs slightly low (i.e.
    understates true IFT, which would overstate the Eotvos number and bias
    the shape_regime.py dispatch slightly toward *more* deformation than a
    fully temperature-corrected value would give) -- a documented
    directional bias, not a silent one, and not correctable without new
    low-temperature CO2-water IFT data this project doesn't have access to.
    """
    P_bar = pressure_bar(depth_m)
    return _SIGMA_PLATEAU_N_M + (_SIGMA_ATM_N_M - _SIGMA_PLATEAU_N_M) * \
        np.exp(-P_bar / _SIGMA_P_SCALE_BAR)
