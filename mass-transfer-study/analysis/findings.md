# Findings: Reconciling CO2-Seawater Mass-Transfer Coefficients

A standalone research effort growing out of the co2-sequestration-revisited
project's own literature review, which found that a specific problem the
original 2002 Stanford M.S. report flagged as unresolved — wildly
disagreeing reported values for how fast CO2 dissolves from a bubble or
droplet into seawater — was, as of 2026, still unresolved in the current
literature. This document is the capstone summary; full phase-by-phase
detail (including the search process, primary-source verification
attempts, and the numbers behind every claim below) is linked throughout
rather than repeated.

## The question

Can the reported 2–6 order-of-magnitude scatter in CO2-seawater
mass-transfer coefficients be explained by known physical regime
differences — bubble surface mobility, hydrate coating, disperse phase,
measurement geometry — rather than remaining an unexplained empirical
disagreement? ([STUDY_PLAN.md](../STUDY_PLAN.md) §2)

## Method, in brief

No new experiments or measurements — this is a literature reconciliation
built entirely from previously published data, consistent with the
constraint that applies across this whole repository (no lab access).
Three established, decades-old analytical theories were implemented and
tested against a compiled literature dataset:

- **Rigid/contaminated bubble surface** (boundary-layer theory, `Sh ~
  Re^0.5 Sc^(1/3)`) — [model/rigid_sphere.py](../model/rigid_sphere.py)
- **Mobile/clean bubble surface** (Levich's penetration theory, `Sh ~
  Re^0.5 Sc^(1/2)`, a genuinely different scaling and a higher
  prediction at the same Re) — [model/mobile_sphere.py](../model/mobile_sphere.py)
- **Hydrate-coated shell** (diffusion-limited, expected roughly
  independent of Reynolds number) —
  [model/hydrate_shell.py](../model/hydrate_shell.py), harmonizing units
  across sources rather than adding a new correlation

None of these three forms were fit to this study's own data — they're
independently established results (Levich 1962; Frössling 1938; Higbie
1935), still cited as standard in current review literature.

## What the dataset actually contains (Phase A)

Verifying the 2002 thesis's own citations against primary sources (as far
as access allowed — no institutional journal subscription, a documented,
accepted limit, not an open gap) surfaced four concrete findings before
any modeling began:

1. An internal numeric inconsistency in the 2002 thesis itself (Hirai
   1996's non-hydrate rate: 1.25×10⁻⁵ in its prose vs. 1.25×10⁻⁴ in the
   equation it actually computes with).
2. A bibliography gap (the thesis cites "Aya et al. 1992" but its own
   reference list only contains an unrelated 1997 Aya paper).
3. A geometry mismatch serious enough to exclude a data point: Brewer et
   al. (2000)'s reported coefficient comes from a bulk hydrate mass or a
   planar interface, not a bubble or droplet — not comparable to a
   spherical-bubble theory at all.
4. A phase mismatch: most of the historical hydrate-era literature
   (Fujioka, Hirai, Aya, Tabe/Hirai) is about **liquid** CO2, not **gas**
   bubbles — a physically distinct system from the CO2/N2 gas bubbles
   this whole project otherwise models. Only two entries in the entire
   dataset are genuine gas bubbles: Saito et al. (2000) and Cho & Choi
   (2019).

Full detail: [data/SOURCES.md](../data/SOURCES.md),
[data/coefficients.csv](../data/coefficients.csv).

## Results

### Before: the raw picture
Lined up naively — the way a literature table typically presents these
values — the dataset spans **3.9×10⁻⁹ to 1.5×10⁻³, nearly six orders of
magnitude.** That's wider than the 2002 thesis's own "2–3 orders of
magnitude" description, and part of the width is itself a finding: some
of it is a **units problem**, not a physics disagreement — diameter-
shrinkage rates, mass fluxes, molar fluxes, and true transfer
coefficients were being compared as if they were the same kind of number.

### After: regime-classified
Once split by disperse phase, geometry, and hydrate state
([analysis/phase_e_reconciliation.md](phase_e_reconciliation.md) for the
full table):

- **Non-hydrate gas bubbles** (the only bucket with unambiguous units and
  physical comparability): **3.6×10⁻⁵ to 2.0×10⁻⁴ m/s — under one order
  of magnitude.** Within this bucket, mobile-sphere theory closes a 3–6×
  gap that rigid-sphere theory left open for the one clean test case
  (Saito et al. 2000), landing within 8–32% using a deliberately
  conservative velocity estimate
  ([phase_b_findings.md](phase_b_findings.md),
  [phase_c_findings.md](phase_c_findings.md)).
- **Hydrate-coated** (mostly liquid CO2): **1.9×10⁻⁶ to 1.5×10⁻³ kg/m²/s
  — a real, unresolved ~2.9-order-of-magnitude residual**, correctly
  separated from the non-hydrate bucket by hydrate state but not
  collapsed within itself. The 2002 thesis's own cited source (Hirai
  1996) reports this rate as flow-velocity-dependent, directly
  contradicting the simple Reynolds-independence assumption — most
  likely because flow affects hydrate shell thickness/growth rather than
  violating diffusion-through-a-fixed-shell physics, though this
  study can't fully confirm that without primary-text access
  ([phase_d_findings.md](phase_d_findings.md)).
- **A regime this study's theories don't cover well**: Cho & Choi's
  micro-bubbles sit at Reynolds numbers (0.0006–0.015) and Péclet numbers
  (0.3–9) below where either analytical theory was ever derived to
  apply. Both give inconsistent, unreliable predictions there — reported
  as a mapped boundary of the framework, not forced into either bucket.

## Answer to the central question

**Partially yes.** Most of the apparent disagreement in the
non-hydrate-gas-bubble literature dissolves once the data is classified
correctly and the right theory (mobile, not rigid, surface behavior) is
applied — a specific, falsifiable prediction that held up for the one
case with a clean test. The hydrate-coated literature retains genuine,
unresolved scatter this study narrows but does not close, most plausibly
tied to uncontrolled hydrate-film properties across different
experiments. And there's a Reynolds/Péclet regime (very small bubbles)
where neither available theory gives dependable answers at all.

That's a materially better answer than "the literature disagrees and
nobody knows why" — which is where both the original 2002 thesis and this
project's own Phase 1 literature check landed, twenty-four years apart.
It is not a complete resolution, and this document doesn't claim to be
one.

## Why this matters beyond a 2002 thesis footnote

The mass-transfer-coefficient uncertainty this study investigated isn't
just a historical loose end. It's a live input to ocean-based carbon
dioxide removal (mCDR) research — several proposed approaches (gas-liquid
contactors, electrochemical ocean carbon capture) depend on exactly this
physics, and mCDR's own research community and the 1990s–2000s ocean-CO2-
disposal literature this study drew from don't appear to cite each other
much. Bridging that gap — even partially, even from a desk with no lab
access — is the more current contribution this whole effort was aimed at
producing (see the parent project's
[PROJECT_THESIS.md](../../PROJECT_THESIS.md) for how this study came to
exist).

## Honest limitations, all stated once rather than scattered

- No new experimental data anywhere in this study, by design and by
  necessity.
- Several literature values could not be verified against primary
  full-text sources (no institutional journal access) — verified at the
  abstract/bibliographic level instead, with that limit stated
  explicitly rather than glossed over.
- The mobile-sphere comparison reused a conservative (rigid-sphere-drag)
  velocity rather than a fully self-consistent mobile-drag model — stated
  in `model/mobile_sphere.py` and not expected to change the qualitative
  conclusion, but a real simplification.
- Sample size is small in every bucket (as few as one or two points) —
  these are illustrative, falsifiable comparisons, not a statistically
  powered study.
