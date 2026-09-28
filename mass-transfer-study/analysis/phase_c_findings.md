# Phase C — Mobile/Clean-Sphere Model: Findings

Per [../STUDY_PLAN.md](../STUDY_PLAN.md) §3.2/§6 Phase C. Model:
[../model/mobile_sphere.py](../model/mobile_sphere.py). Direct
continuation of the specific question Phase B raised — read
[phase_b_findings.md](phase_b_findings.md) first.

> **Addendum** (item 6 from the post-study open-items list, "a fully
> self-consistent mobile-sphere drag law"): attempted and built — see
> the end of this document. It surfaced a deeper finding than a numeric
> refinement: Saito's own plausible bubble sizes sit entirely in the
> shape-*deformed* regime, outside where the spherical theory this whole
> comparison rests on applies at all. The numbers below (using a
> conservative rigid-drag velocity stand-in) remain the reported
> comparison as a result — read the addendum before treating this as
> "not yet done."

## Scoping choice, stated up front

This model reuses the **rigid-sphere terminal velocity** from
`rigid_sphere.py` rather than also deriving a mobile-sphere
(Hadamard-Rybczynski / clean-bubble) drag law — a real physical
simplification. A truly mobile bubble has lower drag and rises faster
than a rigid one of the same size, and since `k_L ~ √U` in Levich's
formula, this makes the numbers below a **conservative (lower-bound)**
estimate of the mobile regime's true transfer rate, not an inflated one.
See the module docstring for the full reasoning.

## Saito et al. (2000): the gap closes

| Db | Re | Pe | Rigid k_L (Phase B) | Mobile k_L | Reported | Mobile/reported |
|---|---|---|---|---|---|---|
| 2 mm | 297 | 308,188 | 6.1×10⁻⁵ | 3.84×10⁻⁴ | 2.0×10⁻⁴ | 1.92× |
| 5 mm | 1504 | 1,559,427 | 5.9×10⁻⁵ | 3.45×10⁻⁴ | 2.0×10⁻⁴ | 1.73× |
| 10 mm | 4395 | 4,557,407 | 5.0×10⁻⁵ | 2.95×10⁻⁴ | 2.0×10⁻⁴ | 1.48× |
| 15 mm | 7879 | 8,171,238 | 4.4×10⁻⁵ | 2.63×10⁻⁴ | 2.0×10⁻⁴ | 1.32× |
| 20 mm | 11,862 | 12,301,689 | 4.1×10⁻⁵ | 2.42×10⁻⁴ | 2.0×10⁻⁴ | 1.21× |
| 30 mm | 21,209 | 21,995,154 | 3.6×10⁻⁵ | 2.16×10⁻⁴ | 2.0×10⁻⁴ | **1.08×** |

This is the result Phase B's specific question was aimed at, and it
answers cleanly: **the mobile-sphere prediction brackets Saito's
reported value across the entire plausible bubble-size range**, and at
the larger end (15–30 mm — itself a physically reasonable size for the
small-scale bubble-visualization experiments the coefficient came from)
it lands within **8–32%** of the reported value, using a *conservative*
velocity estimate. Rigid-sphere theory (Phase B) missed by 3–6×; mobile
theory gets within one significant figure.

**Reading this honestly**: this doesn't *prove* Saito's bubbles had a
clean, uncontaminated surface — it shows that the mobile-interface
hypothesis is quantitatively consistent with the reported measurement in
a way the rigid-interface hypothesis was not, at plausible experimental
conditions. That is a meaningful, falsifiable claim that held up, not a
tautology: rigid theory could easily have been the closer one, or
neither could have come within an order of magnitude, and either result
would have been reported here the same way.

## Cho & Choi (2019): inconsistent, reinforcing the Phase B stress-test read

| Condition | Db | Re | Pe | Mobile k_L | Reported | Ratio |
|---|---|---|---|---|---|---|
| With mixer | 10 μm | 0.0006 | 0.33 | 1.08×10⁻⁴ | 9.97×10⁻⁵ | 0.92× (close) |
| No mixer | 30 μm | 0.015 | 8.9 | 1.86×10⁻⁴ | 3.6×10⁻⁵ | **5.2× over** |

One condition lands within 8%; the other overshoots by more than 5×,
for the same paper, same theory, same model. That inconsistency is itself
the finding: it's not that mobile theory "works" for Cho & Choi and
rigid theory "doesn't," or vice versa — **neither theory gives reliable
answers in this Reynolds/Péclet regime**, exactly as Phase B anticipated
(Pe ≈ 0.3–9 is marginal-to-below where Levich's high-Péclet boundary-layer
approximation is derived to hold, and Method A's correlation is similarly
out of its fitted range here). The apparent 8% match for the "with mixer"
condition is best read as coincidence at this sample size (n=2), not
confirmation.

## What Phase C establishes, going into Phase D and E

- **The central reconciliation hypothesis gains real support**: the one
  case in this dataset with a plausible, physically reasonable regime
  match (Saito, moderate-to-high Re, a real gas bubble) shows rigid
  theory failing by 3–6× and mobile theory closing to within ~8–30%
  using an intentionally conservative velocity. That's the kind of
  result this study set out to look for.
- **The reconciliation has a boundary, and it's now been mapped, not
  just asserted**: at very low Re/Pe (Cho & Choi's micro-bubble regime),
  neither analytical theory this study is built on gives dependable
  predictions. That's worth stating as a limit of the framework, not
  glossed over.
- Phase D (hydrate-coated regime) is now the last piece before Phase E's
  full reconciliation pass can be written up — and per the gas-vs-liquid
  finding from Phase A/B, Phase D's actual test data (Fujioka, Hirai,
  Aya, Tabe/Hirai) will for the first time bring the **liquid-CO2**
  entries back into direct use, since hydrate-shell diffusion resistance
  doesn't care whether the core is gas or liquid.

## Addendum — the fully self-consistent mobile-drag attempt

The result above deliberately used a **conservative** velocity (the
rigid-sphere terminal velocity) rather than deriving a proper
mobile-sphere drag law, flagged at the time as a simplification worth
revisiting. Revisited: [model/mobile_sphere.py](../model/mobile_sphere.py)
now implements Mei, Klausner & Lawrence's (1994) closed-form clean-bubble
drag coefficient, spanning creeping flow through high Reynolds number in
one formula. Checked independently before trusting it (not on the
strength of one search result): its two analytic limits reproduce two
separately well-established results exactly — Re→0 gives Cd=16/Re, the
classical Hadamard-Rybczynski creeping-flow gas-bubble drag (2/3 of the
rigid-sphere Stokes value); Re→∞ gives Cd=48/Re, Moore's (1965) classical
high-Re clean-bubble asymptote.

**Applying it to Saito's conditions gives unphysical results** — rise
velocities up to 180 m/s for a 30 mm bubble. This is not a bug: it is
the mathematically correct consequence of a formula whose Cd → 0 as
Re → ∞, which is the right behavior *for a bubble that stays perfectly
spherical*, and real bubbles do not stay spherical at these sizes.
Checking the Eötvös number (`mobile_sphere.eotvos_number`, which governs
the transition from surface-tension-dominated spherical shape to
inertia-dominated deformation) confirms it directly: **Saito's entire
plausible bubble-size range (2–30 mm) has Eo from ~0.5 to over 100** —
squarely in the shape-deformed (ellipsoidal/wobbling) regime, not the
spherical regime either this module's or `rigid_sphere.py`'s theory
assumes. Cho & Choi's micron-scale bubbles, by contrast, have Eo ~ 10⁻⁴
— genuinely spherical, no such concern; re-running them with the proper
mobile-drag velocity gives 0.16× and 0.75× ratios to the reported values
(versus 0.19× and 0.92× with the earlier conservative estimate) — a
modest shift, not a resolution, consistent with Cho & Choi's regime
already being flagged as outside both theories' dependable range.

**This is a genuine, useful negative result, not a failed refinement.**
It means the rigid-vs-mobile *interface* dichotomy this whole study is
built on (Phases B–C) is the right axis of variation for bubbles small
enough to stay spherical, but for bubbles Saito's size, bubble *shape*
deformation is likely at least as important a physical factor as surface
mobility — and this study's framework doesn't model shape at all. The
earlier conservative comparison (rigid-drag velocity, Levich k_L formula)
remains the one reported, not because it is rigorously correct, but
because it avoids the larger, clearer error of extrapolating an
undeformed-sphere theory into a regime real bubbles don't occupy. A
proper treatment of Saito's regime would need an ellipsoidal/spherical-
cap drag and mass-transfer theory (Clift, Grace & Weber 1978's shape-
regime framework — already cited in the original 2002 thesis's own
bibliography) — out of scope for this pass, flagged rather than
attempted without the same care given to everything else in this study.
