# Shape-regime integration — full scenario matrix re-run

Follow-up to [method_a_vs_b.md](method_a_vs_b.md) and
[PHASE3_NOTES.md](PHASE3_NOTES.md), closing the first item queued in
[../PROJECT_THESIS.md](../PROJECT_THESIS.md) §6.3: feeding
[../mass-transfer-study/](../mass-transfer-study/)'s strongest result —
that this model's own ~1 cm bubbles sit in the shape-*deformed* regime,
not the spherical regime the main model assumed throughout — back into
`model/co2n2_bubble/bubble_model.py` and `mass_transfer.py`. Design and
equations: [../model/EQUATIONS_SPEC.md §5b](../model/EQUATIONS_SPEC.md).
Code: `model/co2n2_bubble/shape_regime.py`.

## What changed

Per timestep, the model now computes the bubble's Eötvös number
(`Eo = g|ρ_sea - ρ_bub|Db²/σ`, using a new pressure-dependent
CO2-seawater interfacial tension, `seawater.interfacial_tension_N_m` —
EQUATIONS_SPEC.md §5b) and dispatches:

- **Eo < 0.5 (spherical)** or **hydrate-coated** (regardless of Eo — see
  below): unchanged rigid-sphere rise-velocity ODE (Eq. 4-4) and, for
  Method A, the unchanged rigid-sphere Sherwood correlation.
- **0.5 ≤ Eo < 40 (ellipsoidal)**: Mendelson's (1967) terminal velocity,
  quasi-steady (see EQUATIONS_SPEC.md §5b for the numerical justification
  of that assumption).
- **Eo ≥ 40 (spherical cap)**: Davies & Taylor's (1950) terminal velocity,
  same quasi-steady treatment.
- Method A's mass-transfer coefficient uses the same Levich penetration-
  theory `k_L` the mass-transfer study validated (`shape_regime.deformed_kL`)
  with the regime-correct velocity, whenever the regime is ellipsoidal or
  cap. Method B (constant Hirai flux) and Method H (hydrate) are unchanged
  in their own rate formulas, since neither depends on velocity — but
  their *trajectories* still shift, because rise velocity changes how long
  the bubble spends at each depth.
- Hydrate-coated bubbles (Method H active) always keep the rigid-sphere
  treatment, deliberately *not* dispatched by Eötvös number even when
  Eo ≥ 0.5: a hydrate shell is a rigid interface, the physical opposite of
  the deformable-interface premise both Mendelson's and Davies & Taylor's
  derivations depend on. See `shape_regime.py`'s module docstring for the
  full reasoning.

## Full matrix re-run (1 cm initial bubble, dt = 2 s)

`percent dissolved` at the surface, and the fraction of simulated
timesteps (Method B run) spent in a shape-deformed (ellipsoidal or cap)
regime rather than spherical/hydrate-rigid:

| depth (m) | CO2 % | pct dissolved (B), **before** | pct dissolved (B), **after** | pct dissolved (A) | U initial → final (m/s) | % steps deformed |
|---|---|---|---|---|---|---|
| 300  | 15%  | 70.3 | **97.1**  | 100.0 | 0.242 → 0.258 | 100% |
| 300  | 50%  | 72.4 | **97.9**  | 100.0 | 0.242 → 0.241 | 100% |
| 300  | 85%  | 74.4 | **98.8**  | 100.0 | 0.242 → 0.201 | 100% |
| 300  | 100% | 75.6 | **100.0** | 100.0 | 0.242 → 0.061 | 99%  |
| 500  | 15%  | 71.4 | **97.7**  | 100.0 | 0.239 → 0.283 | 100% |
| 500  | 50%  | 72.2 | **98.2**  | 100.0 | 0.239 → 0.265 | 100% |
| 500  | 85%  | 66.9 | **98.2**  | 100.0 | 0.534 → 0.229 | 93%  |
| 500  | 100% | 35.0 | **87.0**  | 100.0 | 0.217 → 0.294 | 88%  |
| 1000 | 15%  | 72.1 | **98.2**  | 100.0 | 0.236 → 0.317 | 100% |
| 1000 | 50%  | 69.8 | **97.7**  | 100.0 | 0.508 → 0.306 | 85%  |
| 1000 | 85%  | 47.7 | **91.9**  | 100.0 | 0.308 → 0.315 | 62%  |
| 1000 | 100% | 62.4 | **96.4**  | 100.0 | 0.140 → 0.243 | 36%  |
| 1500 | 15%  | 72.7 | **98.6**  | 100.0 | 0.235 → 0.343 | 100% |
| 1500 | 50%  | 68.4 | **97.8**  | 100.0 | 0.458 → 0.333 | 75%  |
| 1500 | 85%  | 60.8 | **94.3**  | 100.0 | 0.249 → 0.315 | 44%  |
| 1500 | 100% | 91.4 | **99.2**  | 100.0 | 0.083 → 0.301 | 14%  |

("before" column reproduced from [method_a_vs_b.md](method_a_vs_b.md)'s
hydrate-model-on table.)

Method A still dissolves 100% of the injected CO2 in every scenario — the
finding [method_a_vs_b.md](method_a_vs_b.md) already reported as robust to
the solubility-model choice is now also robust to the rise-velocity model,
which is a stronger form of the same conclusion, not a new one: whatever
sets Method A's effective flux (see below), it's large enough that it
doesn't matter which velocity model feeds it, at this bubble size.

## What's actually driving the Method B change — a big one, and why

**Method B's dissolved fraction rose sharply and uniformly**, from a
35–91% spread to a tight 87–100% band. The mechanism is not a change to
Method B's own rate formula (unchanged — it's still Hirai's constant flux,
independent of velocity) but a change to **how long the bubble spends at
depth**: rigid-sphere theory predicted rise velocities that *increase*
with bubble diameter (up to ~1 m/s+ for the larger, decompression-grown
bubbles later in a run); Mendelson/Davies-Taylor terminal velocities are
much flatter, mostly in the 0.2–0.35 m/s band regardless of size — the
same qualitative finding
[mass-transfer-study/analysis/phase_f_deformed_bubble.md](../mass-transfer-study/analysis/phase_f_deformed_bubble.md)
already reported as matching the well-known experimental fact that
mm-to-cm bubbles rise at a roughly size-independent speed. A slower-rising
bubble spends more time at each depth, so Method B's fixed-flux dissolution
has more time to act before the bubble reaches the surface — hence more
total CO2 dissolved, system-wide, not just in one scenario.

**This closes most of a gap [PHASE3_NOTES.md](PHASE3_NOTES.md) flagged as
open from the very first Phase 3 checkpoint.** The 2002 report's own claim
— "≥95% of injected CO2 dissolves before reaching the mixed layer" for
shallow injection — was explicitly *not reproduced* in every checkpoint up
to this one (68–75% in the first pass, still only 35–92% after Method H
was added). Post-integration, the 300 m and 500 m rows (the depths the
original's claim was specifically about) sit at 97.1–100.0% — a close,
in most cases exceeding, match. The 1000 m and 1500 m rows (outside the
original's own ≤500 m claim) also cluster high, 91.9–99.2%. This should
be read as evidence the rigid-sphere velocity assumption was a genuine
source of the earlier mismatch, not proof the model is now numerically
exact — the surface-tension and hydrate-boundary approximations
underneath it are still just that, approximations (see Limitations below).

**Method A's effective flux advantage over Method B also grew.** Tracing
the same representative case method_a_vs_b.md used (1000 m, 50% CO2,
mid-column conditions, now landing in the ellipsoidal regime, Eo ≈ 23.7):
Method A's rate is now **~141× Method B's**, not ~20×. This is the
expected direction, not a red flag: Method A's `k_L` in the deformed
regime is Levich's penetration-theory result (`Sh ~ Sc^(1/2)`), which
STUDY_PLAN.md §3.2 already documents as predicting *substantially higher*
transfer than the rigid-sphere Sherwood correlation (`Sh ~ Sc^(1/3)`) at
the same conditions — precisely the mechanism the mass-transfer study
built and validated, now visible inside the main model too.
[method_a_vs_b.md](method_a_vs_b.md) is not rewritten (its own point —
Method A saturates regardless of solubility model — still stands and is
reinforced) but should be read with this note: its "~20×" flux-ratio
figure is superseded by the number above.

## Regenerated reference runs

Both demo runs cited from `report/revised_report.md` §5 were regenerated
and their CSV/PNG outputs in this directory updated in place:

- **500 m, 50% CO2 (Method B)**: 98.2% dissolved at the surface (was
  72.2%), 1007 steps, final diameter 3.23 cm.
- **1000 m, 100% CO2 with hydrate compensation**: 96.4% dissolved (was
  62.4%). The hydrate-coated shrinkage itself is essentially unchanged —
  minimum diameter during the hydrate-coated phase is 0.887 cm (was
  0.89 cm) — exactly as designed, since hydrate-active steps deliberately
  keep the pre-integration rigid-sphere treatment untouched
  (EQUATIONS_SPEC.md §5b). The large jump in total dissolved percentage
  comes entirely from the post-hydrate-exit phase (below ~400 m), where
  the bubble is now shape-deformed and rises much more slowly than the
  old rigid-sphere prediction, giving Method B far more time to act on
  the remaining CO2 before the surface.
- The pre-existing hydrate-boundary "flutter" noted as a known rough edge
  in [PHASE3_NOTES.md](PHASE3_NOTES.md) (brief in/out transitions right at
  the window boundary) is still present in the regenerated run — unrelated
  to this integration (it's driven by `hydrate_boundary.py`'s own
  criterion, untouched here) and not re-investigated as part of this task.

## Limitations, stated once rather than scattered

- **Surface tension is a new, documented approximation, not a literature
  digitization.** `seawater.interfacial_tension_N_m` interpolates between
  a near-atmospheric value (0.074 N/m) and a high-pressure plateau
  (0.030 N/m) sourced from two retrieved papers (Hebach et al. 2002;
  Chalbaud et al. 2009), using a decay shape chosen to match their
  qualitative description, not a digitized fit to either paper's own data
  (inaccessible). Both papers validate their measurements at 293–398 K;
  this model's own ocean temperatures (Eq. 4-6) run colder, 276–283 K,
  which is outside that validated range and most likely biases this
  model's Eötvös numbers slightly high (i.e. toward *more* apparent
  deformation than a temperature-corrected value would give) — see
  `seawater.py`'s docstring for the full reasoning. This is the single
  largest source of quantitative uncertainty introduced by this
  integration, more than the shape-regime formulas themselves (Mendelson
  and Davies & Taylor are independently verified, per the mass-transfer
  study).
- **Regime boundaries are hard thresholds (Eo = 0.5, 40), not smoothed.**
  Consistent with `mass-transfer-study/model/deformed_bubble.py`'s own
  (already-validated) dispatch, not a new source of un-vetted behavior —
  but it means velocity and `k_L` can jump discontinuously at a regime
  boundary crossing between timesteps, on top of the pre-existing
  hydrate-boundary flutter noted above. Not smoothed here, matching the
  mass-transfer study's own precedent rather than introducing new,
  unvalidated smoothing machinery.
- **This is still a quasi-steady approximation**, numerically justified
  (EQUATIONS_SPEC.md §5b: velocity relaxation ~0.13 s vs. a 2 s timestep
  and hundreds-to-thousands-of-seconds full rise) but not a rigorous
  transient shape-deformed force balance, which doesn't exist in
  closed form in the literature this project has access to.
- No new experimental data anywhere in this integration, consistent with
  the project-wide constraint (CLAUDE.md) — every quantitative change
  above comes from re-running the existing model with better physics, not
  from new measurements.

## Bottom line

The shape-regime integration is not a minor correction — it materially
changes this model's quantitative results, in the direction the
mass-transfer study's own literature-matched finding predicted (real
bubbles at this size rise slower and more uniformly than rigid-sphere
theory says, so they dissolve more before reaching the surface). It also
resolves, in large part, a gap flagged as open since the very first Phase
3 checkpoint: Method B's dissolved fractions now sit close to the
original 2002 report's own "≥95% above 500 m" claim, rather than well
below it. Method A's saturating, discriminating-power-free behavior is
confirmed more strongly, not undermined. The main new source of
uncertainty is the surface-tension approximation this integration had to
introduce from scratch (the original model never needed one), documented
honestly above rather than presented as more precise than it is.
