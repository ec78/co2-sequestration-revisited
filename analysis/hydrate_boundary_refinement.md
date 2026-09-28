# Hydrate-Window Refinement

Open item #2 from the post-Phase-5 discussion (`PROJECT_THESIS.md`).
Replaces the Phase 3 placeholder — a fixed depth ≥ 400 m *and* CO2 mole
fraction ≥ 0.5 box, with no temperature/pressure sensitivity — with a
composition-continuous, physically-motivated boundary. Full derivation:
[model/co2n2_bubble/hydrate_boundary.py](../model/co2n2_bubble/hydrate_boundary.py).

## The approach

Hydrate is predicted to form when the CO2/N2 mixture's CO2 fugacity
(computed via this project's own Peng-Robinson EOS) meets or exceeds
pure CO2's fugacity at *its own* equilibrium hydrate-formation pressure,
at the same temperature. N2 dilution lowers CO2's fugacity at a given
total pressure, so a mixture needs a colder temperature or higher
pressure than pure CO2 to cross the same threshold — the same
qualitative behavior the original report's Chapter 2 describes
("for a CO2 content below about 50% mixture hydrate formation pressure
drastically increases"), reached by an independent route rather than a
digitized reproduction of the original's own figure (which isn't
numerically recoverable from the PDF).

The pure-CO2 boundary curve itself is a simple two-point
Clausius-Clapeyron-style fit (`ln P = a + b/T`) through the CO2 hydrate
system's two quadruple points — both independently retrieved and
cross-checked across multiple sources during this work:
- Lower quadruple point (ice + water + hydrate + vapor): 271.6 K, 1.044 MPa
- Upper quadruple point (water + hydrate + vapor + liquid CO2): 283.0 K, 4.5 MPa

This range (271.6–283 K) comfortably covers this project's own scenario
matrix (~276–283 K at 300–1500 m depth).

## What changed in practice

Comparing the new model against the old box across the original scenario
matrix (16 depth × composition combinations): identical everywhere
except one marginal case, **500 m / 50% CO2**, which the old box called
"hydrate" (exactly on both thresholds) and the new model correctly calls
"not yet hydrate-forming" — consistent with the physical picture that
dilution genuinely shrinks the hydrate-forming region, not just at an
arbitrary composition cutoff.

Re-running the two existing demo scenarios: the 500 m/50% case is
numerically unchanged (72.2% dissolved either way — the bubble transits
that marginal depth too quickly for the reclassification to matter for
the overall trajectory). The 1000 m/100% CO2 hydrate-compensated case
shifts modestly (62.4% → 61.5% dissolved), reflecting a slightly
different depth at which the rising bubble exits the hydrate window under
the new, continuous boundary versus the old flat threshold. Full
regression (all 32 depth × composition × method combinations) still runs
without errors.

## Honest limitation carried forward, not resolved

The fugacity-threshold *mixture* criterion is physically motivated but
not independently validated against real CO2/N2 hydrate equilibrium
data — this project could not access primary measurements or a full
van der Waals-Platteeuw model (CSMGem or newer CPA-EoS approaches are the
field's actual current standard here, per `LITERATURE_UPDATE.md` §6) to
calibrate it against. Checked honestly against the original report's own
qualitative statement that pure CO2 forms hydrate around 279 K at typical
500 m ocean pressure (~50 atm): this curve instead predicts pure CO2
hydrate forming at only ~27 bar at 279 K — a real, unresolved
discrepancy, most likely because the thesis's own statement describes
where the real ocean profile happens to overlap the hydrate-forming
region at that depth, rather than a precise equilibrium-curve reading.
Reported rather than smoothed over, consistent with how every other
approximation in this project has been handled.

**Bottom line**: this is a genuine improvement in functional form — a
smooth, physically-grounded, composition-sensitive boundary in place of
an arbitrary box — even though its exact numerical calibration remains
open. `legacy_box_hydrate_window` is kept in the code for direct
comparison, not deleted.
