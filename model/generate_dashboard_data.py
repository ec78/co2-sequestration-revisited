#!/usr/bin/env python
"""Generates the JSON data bundle behind the project's interactive
findings dashboard (published as a Claude Artifact; see
PROJECT_THESIS.md for the link once published).

Every number in the dashboard traces back to either a live re-run of
this repo's own validated model (bubble trajectories, mass-transfer
regime sweep) or a value already published in one of this repo's own
analysis files (the pre-shape-regime-integration comparison numbers,
economics figures) -- nothing is fabricated for presentation purposes,
consistent with the rest of this project.

Run from model/:  python generate_dashboard_data.py > dashboard_data.json
"""

import json
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "../mass-transfer-study/model")

from co2n2_bubble.bubble_model import simulate  # noqa: E402

DEPTHS = [300, 500, 1000, 1500]
CO2_FRACS = [0.15, 0.50, 0.85, 1.00]
METHODS = ["A", "B"]

# Downsample factor for trajectory arrays sent to the browser -- full
# runs are 600-2400 rows at dt=2s; ~80 points is smooth enough for an
# animation and keeps the JSON small.
MAX_POINTS = 80


def r3(x):
    """Round to a reasonable display precision -- shrinks the JSON
    payload substantially without discarding anything the dashboard
    displays (nothing here feeds back into the model)."""
    return round(x, 4) if abs(x) < 1 else round(x, 3)


def downsample(seq, max_points=MAX_POINTS):
    n = len(seq)
    if n <= max_points:
        return list(seq)
    stride = max(1, n // max_points)
    out = list(seq[::stride])
    if seq[-1] != out[-1]:
        out.append(seq[-1])
    return out


def trajectory(depth, co2_frac, method):
    r = simulate(depth0_m=depth, co2_frac0=co2_frac, diameter0_m=0.01,
                 mass_transfer_method=method)
    n = len(r.time_s)
    idx = list(range(n))
    idx_ds = downsample(idx)
    return {
        "depth0_m": depth,
        "co2_frac0": co2_frac,
        "method": method,
        "n_steps": n,
        "final_pct_dissolved": r.percent_co2_lost[-1] if n else 0.0,
        "final_depth_m": r.depth_m[-1] if n else depth,
        "final_diameter_cm": r.diameter_m[-1] * 100 if n else 0.0,
        "time_s": [r3(r.time_s[i]) for i in idx_ds],
        "depth_m": [r3(r.depth_m[i]) for i in idx_ds],
        "diameter_cm": [r3(r.diameter_m[i] * 100) for i in idx_ds],
        "velocity_m_s": [r3(r.velocity_m_s[i]) for i in idx_ds],
        "co2_mole_frac": [r3(r.co2_mole_frac[i]) for i in idx_ds],
        "percent_co2_lost": [r3(r.percent_co2_lost[i]) for i in idx_ds],
        "shape_regime": [r.shape_regime[i] for i in idx_ds],
    }


def mass_transfer_regime_sweep():
    """Reproduces phase_f_deformed_bubble.md's headline sweep live from
    the mass-transfer study's own modules, rather than transcribing the
    published table -- same numbers, generated fresh."""
    from co2n2_bubble import seawater
    import rigid_sphere
    import deformed_bubble

    y_gas = (0.95, 0.05)  # Saito et al. (2000) conditions, 300 m
    depth_m = 300.0
    T_K = seawater.temperature_K(depth_m)
    P_bar = seawater.pressure_bar(depth_m)
    rho_sea = seawater.density_kg_m3(depth_m)
    mu_sea = seawater.viscosity_mPa_s(depth_m)
    diameters_mm = [2, 5, 10, 15, 20, 25, 30]
    diameters_m = [d / 1000.0 for d in diameters_mm]

    rigid = rigid_sphere.predict_over_diameter_range(diameters_m, y_gas, T_K, P_bar, rho_sea, mu_sea)
    deformed = deformed_bubble.predict_over_diameter_range(diameters_m, y_gas, T_K, P_bar, rho_sea, mu_sea)

    rows = []
    for i, d in enumerate(diameters_mm):
        rows.append({
            "diameter_mm": d,
            "regime": deformed[i]["regime"],
            "kL_rigid_m_s": rigid[i]["kL_m_s"],
            "kL_deformed_m_s": deformed[i]["kL_m_s"],
            "U_deformed_m_s": deformed[i]["U_m_s"],
            "Eo": deformed[i]["Eo"],
        })
    return {
        "reported_kL_m_s": 2.0e-4,
        "source": "Saito et al. (2000)",
        "rows": rows,
    }


def main():
    trajectories = []
    for depth in DEPTHS:
        for frac in CO2_FRACS:
            for method in METHODS:
                trajectories.append(trajectory(depth, frac, method))

    data = {
        "scenario_matrix": {
            "depths_m": DEPTHS,
            "co2_fracs": CO2_FRACS,
            "methods": METHODS,
            "trajectories": trajectories,
        },
        "mass_transfer_regime_sweep": mass_transfer_regime_sweep(),
    }
    print(json.dumps(data))


if __name__ == "__main__":
    main()
