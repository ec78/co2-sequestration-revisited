#!/usr/bin/env python
"""CLI entry point -- mirrors the original MATLAB script's `input()`
prompts (depth, CO2 concentration, bubble diameter), but non-interactive
(argparse) since this runs headless. See EQUATIONS_SPEC.md for the model.

Example:
    python run_simulation.py --depth 500 --co2-fraction 0.5 --diameter-cm 1 \
        --method B --plot analysis/demo_500m_50pct.png
"""

import argparse
import sys

from co2n2_bubble.bubble_model import simulate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=float, required=True,
                         help="Initial injection depth, meters")
    parser.add_argument("--co2-fraction", type=float, required=True,
                         help="Initial CO2 mole fraction (0-1); balance N2")
    parser.add_argument("--diameter-cm", type=float, required=True,
                         help="Initial bubble diameter, cm")
    parser.add_argument("--method", choices=["A", "B"], default="B",
                         help="Mass transfer method (default: B, Hirai constant-rate)")
    parser.add_argument("--dt", type=float, default=2.0, help="Timestep, s")
    parser.add_argument("--out", type=str, default=None,
                         help="Path to write CSV output (optional)")
    parser.add_argument("--plot", type=str, default=None,
                         help="Path to write a summary PNG plot (optional)")
    args = parser.parse_args()

    result = simulate(
        depth0_m=args.depth,
        co2_frac0=args.co2_fraction,
        diameter0_m=args.diameter_cm / 100.0,
        dt_s=args.dt,
        mass_transfer_method=args.method,
    )

    n = len(result.time_s)
    if n == 0:
        print("No simulation steps ran -- check inputs.", file=sys.stderr)
        sys.exit(1)

    print(f"Ran {n} steps ({result.time_s[-1]:.0f} s simulated).")
    print(f"Final depth: {result.depth_m[-1]:.1f} m")
    print(f"Final diameter: {result.diameter_m[-1]*100:.3f} cm")
    print(f"Final CO2 mole fraction in bubble: {result.co2_mole_frac[-1]:.3f}")
    print(f"Percent of original CO2 dissolved: {result.percent_co2_lost[-1]:.1f}%")

    if args.out:
        import csv
        with open(args.out, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time_s", "depth_m", "diameter_m", "velocity_m_s",
                              "co2_mole_frac", "rho_bubble", "rho_seawater",
                              "mass_co2_lost_kg", "percent_co2_lost"])
            for i in range(n):
                writer.writerow([
                    result.time_s[i], result.depth_m[i], result.diameter_m[i],
                    result.velocity_m_s[i], result.co2_mole_frac[i],
                    result.rho_bubble[i], result.rho_seawater[i],
                    result.mass_co2_lost_kg[i], result.percent_co2_lost[i],
                ])
        print(f"Wrote {args.out}")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 2, figsize=(10, 10))
        axes[0, 0].plot(result.time_s, result.depth_m)
        axes[0, 0].set(xlabel="Time (s)", ylabel="Depth (m)",
                       title="Depth of Bubble with Time")
        axes[0, 0].invert_yaxis()

        axes[0, 1].plot(result.depth_m, result.co2_mole_frac)
        axes[0, 1].set(xlabel="Depth (m)", ylabel="CO2 mole fraction",
                       title="Bubble CO2 Content")

        axes[1, 0].plot(result.depth_m, [d * 100 for d in result.diameter_m])
        axes[1, 0].set(xlabel="Depth (m)", ylabel="Bubble diameter (cm)",
                       title="Bubble Diameter with Depth")

        axes[1, 1].plot(result.depth_m, result.rho_bubble, label="bubble")
        axes[1, 1].plot(result.depth_m, result.rho_seawater, label="seawater")
        axes[1, 1].set(xlabel="Depth (m)", ylabel="Density (kg/m^3)",
                       title="Densities")
        axes[1, 1].legend()

        axes[2, 0].plot(result.depth_m, result.percent_co2_lost)
        axes[2, 0].set(xlabel="Depth (m)", ylabel="Percent",
                       title="Percent CO2 Dissolved")

        axes[2, 1].plot(result.depth_m, result.mass_co2_lost_kg)
        axes[2, 1].set(xlabel="Depth (m)", ylabel="Mass CO2 dissolved (kg)",
                       title="Mass of CO2 Dissolved")

        fig.tight_layout()
        fig.savefig(args.plot, dpi=150)
        print(f"Wrote {args.plot}")


if __name__ == "__main__":
    main()
