# Phase D — Hydrate-Coated Regime: Findings

Per [../STUDY_PLAN.md](../STUDY_PLAN.md) §3.3/§6 Phase D. Harmonization
tool: [../model/hydrate_shell.py](../model/hydrate_shell.py). This phase
doesn't build a new predictive correlation the way Phases B and C did —
there's no bubble-diameter/velocity input to sweep over the way there was
for a free gas bubble, and this project's main model already implements
the practical regime behavior (Method H: a constant, literature-sourced
rate, independent of Reynolds number). What Phase D actually needed, and
didn't have going in, was **all the hydrate-coated literature values on
one comparable basis** — the 2002 thesis's own Table 4-1 tried to do this
("converted... for an 85% pure carbon dioxide bubble at a depth of 1500
m") and its own table came out corrupted (see `../data/SOURCES.md`).

## Harmonized comparison

All values converted to mass flux (kg/m²/s), using pure liquid CO2
density at 1500 m (998.6 kg/m³, computed via this project's own EOS
module — matching the depth basis the 2002 thesis itself intended):

| Source | Flow regime | Harmonized flux (kg/m²/s) |
|---|---|---|
| Aya, Yamane & Yamada (1992) | quiescent | 1.9×10⁻⁶ |
| Tabe/Hirai et al. (1999) | unknown | 1.15×10⁻⁴ |
| Fujioka et al. (1994) | quiescent | 2.5×10⁻⁴ |
| Hirai et al. (1996), low end | forced flow | 3.0×10⁻⁴ |
| Hirai et al. (1996), high end | forced flow | 1.5×10⁻³ |
| *Brewer et al. (2000) — excluded, geometry* | *in-situ field* | *1.5×10⁻⁷* |

(Brewer shown for context only — excluded from the comparison per the
Phase A geometry finding, not a bubble/droplet measurement.)

## What this shows

**Hydrate state does explain a lot of the original scatter, at the top
level.** Every genuine hydrate-coated value here is well below the
non-hydrate gas-bubble range Phases B/C worked with (Saito's reported
2.0×10⁻⁴ m/s, Cho & Choi's 3.6–10×10⁻⁵ m/s) once put on comparable terms
— consistent with hydrate film acting as a real transport barrier, the
qualitative story this whole project (and the original 2002 thesis) has
told from the start.

**But the hydrate-coated bucket does *not* collapse to one number.**
Even excluding Brewer, the remaining four sources span **1.9×10⁻⁶ to
1.5×10⁻³ kg/m²/s — nearly three orders of magnitude on their own.** A
simple constant-rate model (what Method H already implements) cannot
represent this range; it can only pick a representative point within it.
That's not a defect introduced by this study — it's a description of
what the literature actually contains, made visible by putting everything
on one basis for the first time.

**A specific, checkable reason for part of that scatter**: the two
forced-flow Hirai (1996) values sit at or above the two quiescent values
(Fujioka, and — with a caveat below — Tabe/Hirai). That's the direction
you'd expect if imposed flow enhances hydrate-limited transfer at all,
which is not what a strict "hydrate transfer is Reynolds-number-
independent" reading of §3.3's theory would predict. This is not
incidental: **the 2002 thesis's own prose says exactly this about Hirai's
data** — that the hydrate-coated rate varies "depending on temperature,
pressure, and rise velocity." The simple film-diffusion picture (§3.3)
assumes the shell's diffusive resistance doesn't care about outer flow;
what's more likely happening, and what this study can only name rather
than confirm without primary-text access, is that flow affects the
**hydrate shell itself** — its thickness or growth/erosion rate — rather
than violating diffusion-through-a-fixed-shell physics directly. A
Reynolds-independent flux *through a fixed shell* is still consistent
with a Reynolds-*dependent* shell thickness produced by the flow that
formed it.

**Aya (1992) is a clear outlier**, roughly 60–130× lower than every other
quiescent or forced-flow value here. Two explanations are consistent
with what's known: (a) it may reflect a different measured quantity — the
source paper's own title ("stability of clathrate-hydrate... in highly
pressurized water") suggests a focus on long-term equilibrium hydrate
stability rather than an actively dissolving droplet's transient shrink
rate, which could plausibly be measuring something closer to a
near-equilibrium residual rate than the other four sources' active-
dissolution rates; (b) it could simply be a different hydrate film
quality/thickness, unremarked in what's recoverable from this paper at
abstract level. Not resolved further without the primary text.

## Bottom line for Phase E

The regime split (hydrate vs. non-hydrate, rigid vs. mobile) explains the
original scatter well at the level Phases B/C demonstrated for gas
bubbles specifically, and at the coarse "hydrate vs. not" level generally.
It does **not** fully explain the scatter *within* the hydrate-coated
bucket — real residual disagreement remains there, most plausibly tied to
uncontrolled hydrate-film properties and a genuine (if secondary and
indirect) flow dependence the simple constant-rate model doesn't capture.
Phase E's write-up should report this as a partial, not total,
reconciliation — which is itself the honest and more useful answer to
this study's original question than a claim of full resolution would be.
