"""Hydrate-coated regime. STUDY_PLAN.md section 3.3 / Phase D.

Once a solid hydrate shell coats a droplet/bubble, the rate-limiting step
shifts from liquid-phase convection to diffusion through the (effectively
solid, stagnant) shell -- this project's main model already implements the
practical consequence as "Method H": a constant, literature-reported rate,
independent of Reynolds number (../../model/co2n2_bubble/mass_transfer.py,
method_h_rate). This module doesn't re-derive that -- it does the thing
Phase D actually needed, which the literature review surfaced as missing:
the compiled hydrate-coated dataset reports rates in at least three
different units (a diameter-reduction rate in m/s; a mass flux in
kg/m^2/s; a molar flux in mol/m^2/s), and the 2002 thesis's own Table 4-1
tried and failed (due to OCR/table corruption -- see
../data/SOURCES.md) to put them on one common basis. This harmonizes them.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "model"))

from co2n2_bubble.constants import MOLAR_MASS  # noqa: E402

CO2_MOLAR_MASS_G_MOL = MOLAR_MASS[0]


def diameter_rate_to_mass_flux(dDb_dt_m_s: float, rho_liquid_co2_kg_m3: float) -> float:
    """Converts a reported diameter-reduction rate [m/s] to an equivalent
    mass flux [kg/m^2/s], via the same relation this project's Method H
    uses (EQUATIONS_SPEC.md section 6): mass_rate = (pi/2) rho Db^2
    |dDb/dt|, flux = mass_rate / (pi Db^2) = 0.5 rho |dDb/dt|. Note Db
    cancels -- flux is independent of droplet size under a
    constant-diameter-rate model, which is itself worth noting as an
    assumption (see findings write-up).
    """
    return 0.5 * rho_liquid_co2_kg_m3 * abs(dDb_dt_m_s)


def molar_flux_to_mass_flux(molar_flux_mol_m2_s: float) -> float:
    """mol/m^2/s -> kg/m^2/s."""
    return molar_flux_mol_m2_s * CO2_MOLAR_MASS_G_MOL / 1000.0
