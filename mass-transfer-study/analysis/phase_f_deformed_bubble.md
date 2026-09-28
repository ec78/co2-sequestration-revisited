# Phase F (follow-up) — Ellipsoidal / Spherical-Cap Regime: Findings

Direct continuation of the gap [phase_c_findings.md](phase_c_findings.md)'s
addendum identified: Saito et al.'s (2000) plausible bubble sizes (2–30 mm)
sit entirely in the shape-*deformed* regime (Eötvös number 0.5 to >100),
where neither this study's rigid-sphere nor idealized clean-spherical-
bubble theory has a real physical basis. Model:
[../model/deformed_bubble.py](../model/deformed_bubble.py), implementing
the two regimes real bubbles that size actually occupy — ellipsoidal
(Mendelson, 1967) and spherical-cap (Davies & Taylor, 1950) — rather than
the fuller Clift-Grace-Weber (1978) machinery. Both formulas verified
against sources reproducing them directly before use, per this study's
standing practice.

## Result: a close, physically grounded match

Sweeping the same plausible bubble-diameter range as Phases B–C (2–30 mm)
at Saito's stated conditions (300 m, 95% CO2/5% N2):

| Db | Regime | Eo | U (terminal) | Re | Predicted k_L | Ratio to reported |
|---|---|---|---|---|---|---|
| 2 mm | ellipsoidal | 0.51 | 0.29 m/s | 450 | 4.72×10⁻⁴ | 2.36× |
| 5 mm | ellipsoidal | 3.2 | 0.23 m/s | 909 | 2.68×10⁻⁴ | 1.34× |
| 10 mm | ellipsoidal | 12.7 | 0.25 m/s | 1983 | **1.98×10⁻⁴** | **0.99×** |
| 15 mm | ellipsoidal | 28.5 | 0.29 m/s | 3405 | 1.73×10⁻⁴ | 0.87× |
| 20 mm | cap | 50.7 | 0.21 m/s | 3287 | 1.28×10⁻⁴ | 0.64× |
| 30 mm | cap | 114.0 | 0.26 m/s | 6039 | 1.15×10⁻⁴ | 0.58× |

**Reported value: 2.0×10⁻⁴ m/s.** At 10 mm — one centimeter, a thoroughly
plausible size for the small-scale bubble-visualization experiments
Saito et al.'s own coefficient came from — the predicted value is
1.98×10⁻⁴ m/s: a match to within 1%. Across the full plausible size
range, the predictions bracket the reported value tightly (0.58×–2.36×),
a substantially closer and more consistent match than either earlier
attempt:

- Rigid-sphere theory (Phase B): 3.6–6.1×10⁻⁵ m/s — always 3–6× too low.
- Idealized clean-spherical-bubble theory (Phase C addendum): unphysical
  (up to 180 m/s) — the theory's own premise (an undeformed sphere)
  doesn't hold at this size at all.
- **Ellipsoidal/cap theory (this phase): 0.58×–2.36×, essentially exact
  at a physically plausible size.**

The terminal velocities themselves (0.21–0.29 m/s across the whole size
range) are now physically realistic in a second, independent sense: they
match the well-known experimental fact that millimeter-to-centimeter gas
bubbles in water rise at a roughly *constant* speed around 20–30 cm/s
across a wide size range, rather than increasing with size the way small
rigid or idealized-spherical bubbles do. Both the rigid-sphere (Phase B)
and idealized-mobile-sphere (Phase C) models get this qualitatively
wrong — their velocities increase monotonically with diameter. This
model gets it right, because it's now using the theory real bubbles at
this size actually follow.

## Reading this honestly

This is the single strongest quantitative result in the whole study —
worth being precise about what it does and doesn't establish:

- It does **not** prove Saito et al.'s bubbles were exactly 10 mm, or
  that this study has independently determined their bubble size. It
  shows that *a* plausible size, well within the range such visualization
  experiments actually use, reproduces the reported coefficient almost
  exactly under standard, independently-verified deformed-bubble theory.
  That's a strong consistency check, not a size measurement.
- It **does** mean the earlier Phase B/C conclusion — "mobile-sphere
  theory closes most of the gap, using a conservative estimate" — was
  the right direction but the wrong mechanism. The gap wasn't
  (primarily) about interface mobility (rigid vs. clean surface); it was
  about bubble *shape*. Once shape is modeled correctly, "mobile vs.
  rigid" mostly stops mattering at this scale, because both ellipsoidal
  and spherical-cap bubbles have strong internal circulation/wake
  shedding regardless of surface contamination state — surface
  mobility's effect is second-order compared to the shape-driven
  velocity change.
- The mass-transfer side still borrows Levich's penetration-theory
  formula (Sc^(1/2) scaling) with the regime-correct velocity substituted
  in, rather than a mass-transfer correlation independently derived for
  deformed bubbles. That's standard practice, not a new unverified leap,
  but it's worth naming as still a piece reused across regimes rather
  than re-derived for each one.
- R in the Davies-Taylor formula is approximated as the equivalent-sphere
  radius, not the bubble's actual cap radius of curvature — a standard
  simplification, not a rigorous geometric treatment.

## Consequence for the study's overall answer

This meaningfully strengthens [phase_e_reconciliation.md](phase_e_reconciliation.md)'s
"Bucket 1" (non-hydrate gas bubbles) finding. What was reported there as
"mobile theory closes most of the gap for one clean test case, using a
conservative velocity estimate" is now: **a physically correct
shape-and-mobility-aware theory matches Saito's reported coefficient to
within 1% at a plausible bubble size, using no fitting to this study's
own data.** The Cho & Choi comparison is unaffected (their bubbles are
still deeply spherical, Eo ~10⁻⁴, and the shape-regime dispatch correctly
falls back to the same spherical treatment Phase C already used) — that
regime remains a genuine, unresolved stress case for this whole
theoretical framework, not addressed by this phase.
