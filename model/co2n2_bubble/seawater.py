"""Seawater temperature, pressure, density, and viscosity vs. depth.

EQUATIONS_SPEC.md section 2. Temperature-depth correlation is the
original's Eq. 4-6; pressure/density use the GSW/TEOS-10 toolbox in place
of the original's SEAWATER (Morgan, 1994) -- see spec for why.
"""

import gsw

from .constants import REFERENCE_SALINITY_PSU, LATITUDE_DEG


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
