# P-GLAD J-Tube Hydraulic Model — Governing Equations and Validation

Re-derivation of the original 2002 report's Chapter 3 P-GLAD model,
independent of MATLAB syntax — there is no MATLAB source to work from
here at all (unlike the single-bubble model): the thesis's own single
appendix contains only the single-bubble driver
(`../../original/appendix_a_original.m`); no P-GLAD code was ever
published alongside the report. This is a from-scratch reimplementation
of the equations Chapter 3 states in prose/equation form only.

## 1. What the original system is

A gas-lift J-tube (Saito et al., 2000): low-purity CO2 is injected at the
bottom of a shallow **upriser**, rises via gas-lift transport while
dissolving into the surrounding seawater, and vents any undissolved gas
at the top; the resulting CO2-rich seawater then flows down a separate
**downriser** to deep disposal, driven by the combined gas-lift and
density-differential effect. No pump — the water flow rate is not a
controlled input, it's whatever the gas-lift effect can sustain, found
by matching ambient hydrostatic pressure at both open ends of the system
(the injection point and the discharge point) simultaneously.

## 2. Governing equations — **[ORIGINAL]**

Two-phase (upriser) and single-phase (downriser) pressure-gradient
equations, mass and momentum conservation for the mixture, and the
drift-flux relations for in-situ vs. superficial velocity — all as given
in the original text (Eqs. 3-1 through 3-23; Saito et al., 2000; Chen,
2001; Govier & Aziz, 1972). The downriser is modeled as single-phase flow
of CO2-saturated seawater (the original's own stated assumption: "all
gases either dissolve into the seawater or are emitted through the top
of the J-tube"), with the kinetic-energy term dropped as negligible (also
the original's own stated simplification) and fluid properties evaluated
locally rather than held rigorously constant (a minor, flagged deviation
from the original's stated "constant throughout the downriser" — using
local values is strictly more accurate and was simple to do given this
project already has a full seawater-property module).

## 3. Two-phase friction correlation — **[MODERNIZED]**

The original used the Govier & Aziz (1972) two-phase friction factor
correlation, presented in that source as a **graphical** correlation
(friction factor vs. a reduced liquid Reynolds number, read off a chart)
— not usable without the original 1972 book, which isn't accessible to
this project (no institutional library access, the same constraint
documented throughout this repo).

**Beggs & Brill (1973)** is substituted: a fully closed-form two-phase
pipe-flow correlation from the same petroleum-engineering tradition (this
is a Petroleum Engineering department report), well suited to the
upriser's near-vertical gas-lift flow, and still a standard reference
correlation today. Implementation: `beggs_brill.py`. Provenance and the
same "not independently verified against the 1973 primary paper, cross-
validated against a second source instead" honesty standard as this
project's Duan & Sun (2003) solubility substitution: full account in that
file's own docstring.

## 4. Solution method — **[ORIGINAL]**

A shooting method: guess the water mass flow rate, march the upriser
pressure from the known injection-depth ambient pressure up to the top,
then march the downriser pressure from that computed top value down to
the discharge depth, and adjust the guessed water flow rate until the
computed discharge-depth pressure matches the true ambient value there —
exactly the original's own stated "guess and check procedure... setting
the pressures at the bottom of the upriser and the bottom of the
downriser to correct hydrostatic pressures." Implementation:
`jtube_model.py`, using `scipy.optimize.brentq` for the root search
(the original doesn't specify its own root-finding method beyond "guess
and check").

## 5. Validation against the original's own worked example — **honest result: does not reproduce**

The original gives a fully specified worked example (thesis text,
§5.2.1, Table 5-1): 0.5 m diameter pipe, 200 m upriser (injection at
300 m, top at 100 m), 900 m downriser (top at 100 m, discharge at
1000 m), 5 kg/s gas injection (95% CO2/5% N2), reporting a solved water
flow rate of **362.3 kg/s**.

**This reimplementation does not reproduce that number.** Scanning the
pressure-mismatch residual across water flow rates from 1 to 2000 kg/s
shows no root near 362.3 kg/s at all — the two genuine sign changes found
are both near 25–53 kg/s (almost certainly numerical artifacts of
Beggs & Brill's flow-regime-boundary kinks, not a physically meaningful
second operating point), and across the entire 100–2000 kg/s range the
pressure mismatch stays roughly **flat at 3.5–4.6 bar (≈3.5–4.5% of the
~102 bar target)** — including at 362.3 kg/s itself (≈4.6 bar off). A
flat, only mildly flow-rate-sensitive mismatch of this kind points to a
**systematic missing term or a different empirical correlation**, not a
water-rate-sensitive error a shooting method could converge past by
trying harder.

**A specific, independently-derived reason to expect this**: Table 5-1
itself, read carefully, shows the liquid volumetric flow rate increasing
by roughly 20% between injection (0.294 m³/s) and the top of the upriser
(0.353 m³/s) — far more than seawater density variation over 200 m could
explain (well under 1%). That implies Saito et al.'s underlying model
couples water flow to gas dissolution or entrainment along the upriser in
a way the 2002 thesis's own stated equations (3-1 to 3-23) don't specify
— this reimplementation, built strictly from those equations plus a
modernized friction correlation, has no such coupling, and holds both gas
and liquid mass flow constant along the pipe instead (a documented
simplification, not an oversight). That's a very plausible, though not
confirmed, explanation for the discrepancy: **the 2002 thesis's own
presentation of Chapter 3 appears to be an incomplete summary of Saito et
al.'s actual model**, not a self-contained specification of it — the same
kind of gap this project has already found and documented elsewhere
(the missing single-bubble helper subroutines; the corrupted Table 4-1).
Confirming this would require Saito et al.'s own paper directly, which
isn't accessible to this project.

## 6. What this reimplementation is good for, honestly

- It correctly reproduces the *qualitative* gas-lift mechanism: for a
  fixed water rate and a fixed (ambient) bottom pressure, increasing the
  gas injection rate **increases** the computed pressure at the top of
  the upriser — i.e. more gas lightens the column and leaves more of the
  original ambient pressure "unspent" by the climb, rather than lost to
  hydrostatic head. Checked directly: 0.5 → 20 kg/s gas at fixed 200 kg/s
  water monotonically raises the computed top pressure from 12.2 to
  21.5 bar. That's exactly the mechanism that makes the downstream
  pumping effect possible — more residual pressure at the junction means
  more driving force available to push water down the downriser.
- It is a real, working, documented two-phase-flow J-tube solver, useful
  for exploring how the system's behavior changes with pipe diameter,
  depth, or gas rate — just not calibrated to reproduce this one
  historical number without the missing entrainment/dissolution physics.
- It should **not** be read as validating or invalidating Saito et al.'s
  own reported P-GLAD economics (already covered via the literature-
  sourced comparison in `../../analysis/economic_reanalysis.md`) — this
  model doesn't reach the fidelity needed to second-guess that number
  either way.
