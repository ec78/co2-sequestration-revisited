# Phase E — Full Reconciliation

Per [../STUDY_PLAN.md](../STUDY_PLAN.md) §6 Phase E, and directly
answering the question posed in §2: *can the reported scatter in
CO2-seawater mass-transfer coefficients be explained by physical regime
differences, rather than remaining an unexplained disagreement?* This
phase pulls Phases B–D into one picture and gives the central,
before/after answer.

## Before: what "the literature disagrees" actually looks like

Lining up every value in [../data/coefficients.csv](../data/coefficients.csv)
the way the 2002 thesis's own Table 4-1 effectively did — as if they were
all the same kind of number, differing only in magnitude:

**3.9×10⁻⁹ to 1.5×10⁻³** — a raw spread of **almost six orders of
magnitude**, actually *wider* than the "2–3 orders of magnitude" the 2002
thesis's own conclusion described. Part of that widening is itself a
finding: **the raw numbers aren't all the same physical quantity.** The
"literature disagreement" this whole study set out to investigate is, in
part, an artifact of comparing a diameter-shrinkage rate (m/s), a mass
flux (kg/m²/s), a molar flux (mol/m²/s), and a true mass-transfer
coefficient (m/s, but only meaningful multiplied by a concentration
driving force) as if a bare number in each of those systems meant the
same thing. This is worth stating plainly: **some of the original
scatter was never a physics disagreement at all — it was a units
problem**, present even in a single source (Hirai et al. 1996 alone
reports its own values in all three of m/s, kg/m²/s, and — implicitly,
via Method B's use of it — a form requiring composition-dependent
scaling).

## After: what's left once you classify correctly

### Bucket 1 — non-hydrate gas bubbles (directly comparable, k_L, m/s)
The only bucket where every entry is unambiguously the same physical
quantity (a true mass-transfer coefficient) for the same physical system
(a gas bubble, not a liquid droplet or a planar mass):

| Source | k_L (m/s) |
|---|---|
| Cho & Choi (2019), 30 μm | 3.6×10⁻⁵ |
| Cho & Choi (2019), 10 μm | 9.97×10⁻⁵ |
| Saito et al. (2000) | 2.0×10⁻⁴ |

**Spread: 3.6×10⁻⁵ to 2.0×10⁻⁴ — under one order of magnitude (5.6×).**
Already, just from correctly isolating "gas bubble, non-hydrate, true
k_L" from the other five-plus orders of magnitude of unrelated
quantities, most of the apparent disagreement is gone.

*Within* this bucket, Phases B–C explain the remaining spread with real
predictive success in one case and an honestly bounded failure in the
other: rigid-sphere theory under-predicts Saito by 3–6×, mobile-sphere
theory closes that to within 8–32% (§ Phase C); both theories give
inconsistent, unreliable answers for Cho & Choi's much lower Re/Pe
regime, which sits outside where either was ever meant to apply.

### Bucket 2 — hydrate-coated (mass flux, kg/m²/s, liquid CO2 for all but the excluded Brewer entry)

| Source | Flux (kg/m²/s) |
|---|---|
| Aya, Yamane & Yamada (1992) | 1.9×10⁻⁶ |
| Tabe/Hirai et al. (1999) | 1.15×10⁻⁴ |
| Fujioka et al. (1994) | 2.5×10⁻⁴ |
| Hirai et al. (1996), forced flow | 3.0×10⁻⁴–1.5×10⁻³ |

**Spread: 1.9×10⁻⁶ to 1.5×10⁻³ — about 2.9 orders of magnitude.** This is
the residual, unresolved scatter Phase D identified: hydrate state
correctly separates this bucket from Bucket 1 by roughly two to three
orders of magnitude (consistent with hydrate film acting as a real
transport barrier), but doesn't collapse the bucket itself to one number.
Best available explanation (Phase D): uncontrolled hydrate-film
properties across studies, plus a real but indirect flow dependence (the
2002 thesis's own citation of Hirai 1996 states the rate depends on rise
velocity) that the simple constant-rate model doesn't capture.

### Bucket 3 — non-hydrate liquid CO2, forced flow (Hirai 1996's own non-hydrate entries)

| Value | Units |
|---|---|
| 1.25×10⁻⁵ | kg/m²/s |
| 1.25×10⁻⁴ | kg/m²/s |
| 2.8×10⁻⁴ | m/s |

Not resolved in this study — too few points, in inconsistent units even
within one paper (see the internal-inconsistency finding in
`../data/SOURCES.md`), and not a valid test case for either the
gas-bubble theory (wrong phase) or the hydrate theory (not hydrate-
coated). Flagged as an open gap, not silently dropped.

### Bucket 4 — excluded entirely
Brewer et al. (2000): not a bubble or droplet measurement (Phase A
finding). Reported for completeness in earlier phases, excluded here.

## Direct answer to the study's central question

**Partially yes.** Once the dataset is split by what should obviously
matter physically — the actual quantity being reported (coefficient vs.
flux vs. shrinkage rate), the disperse phase (gas vs. liquid CO2), the
geometry (sphere vs. planar/bulk mass), and hydrate state — the apparent
five-to-six-order-of-magnitude disagreement resolves into: one bucket
with under one order of magnitude of spread and a specific, validated
explanation for most of it (Bucket 1); one bucket with a real, roughly
three-order-of-magnitude residual that hydrate-vs-not correctly narrows
but doesn't close (Bucket 2); and one bucket with too little usable data
to assess (Bucket 3).

That is a **materially better answer than "the literature just
disagrees,"** which is where this study started (both the 2002 thesis's
own conclusion and this project's own Phase 1 literature check, twenty-
four years apart, landed on that same unresolved statement). It is not a
complete resolution, and presenting it as one would overclaim past what
a literature-only, no-new-data study can honestly support.
