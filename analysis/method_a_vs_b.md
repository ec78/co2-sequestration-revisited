> **Update**: Duan & Sun (2003) has since been implemented properly (was
> the "open Phase 3 item" when this was first written — see
> [../model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md) §4). The
> "best current explanation" section below turned out to be only half
> right: Duan & Sun *does* give lower solubility than Weiss, as
> hypothesized, but not by nearly enough to change Method A's
> 100%-every-time result. See the new section at the end for the
> corrected conclusion.

# Method A vs. Method B — mass-transfer comparison

Second Phase 3 checkpoint, following up
[PHASE3_NOTES.md](PHASE3_NOTES.md). Covers two of the three items flagged
there as remaining work: this comparison, and the hydrate-compensation
("Method H") implementation it's run alongside. See
[../model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md) §3 and §6 for the
underlying equations and what changed.

## What changed since the last checkpoint

1. **EOS phase-selection bug fix.** The first pass always took the PR
   EOS's largest real root ("vapor"). Checking the root structure
   numerically showed that's wrong for CO2-rich mixtures in this model's
   own scenario matrix: pure CO2 at 500–1500 m has a single real root and
   it's the dense, liquid-like one (ρ ≈ 860–999 kg/m³), not a low-density
   gas. Fixed by picking the root that minimizes residual Gibbs energy
   when more than one real root exists (standard cubic-EOS stability
   criterion). Full writeup in EQUATIONS_SPEC.md §3.
2. **Hydrate compensation ("Method H") implemented**, gated to a
   documented placeholder "hydrate window" (depth ≥ 400 m and CO2 mole
   fraction ≥ 0.5 — a stand-in for the original's Fig. 2-5 phase diagram,
   which isn't numerically recoverable from the PDF). Inside the window,
   the bubble is forced onto the vapor EOS root (modeling a hydrate shell
   as a kinetic barrier to bulk liquefaction) and dissolves via a rate
   derived from Fujioka et al.'s (1994) reported hydrate-coated
   diameter-shrinkage rate, instead of Method A/B. Outside the window,
   nothing changes from the previous checkpoint. Full writeup in
   EQUATIONS_SPEC.md §6.
3. This closed a real gap from the last checkpoint: pure CO2 at 1000 m now
   **shrinks (1.00 → 0.89 cm) and rises slowly while hydrate-coated**
   between 1000 m and ~500 m, then undergoes a sharp transition once it
   exits the hydrate window near 400 m and behaves like an ordinary gas
   bubble the rest of the way up. That's a qualitatively different, more
   original-consistent trajectory than the previous checkpoint's
   "grows and accelerates the whole way" result for pure CO2.

## Method A vs. B, full matrix (hydrate model on)

`percent dissolved` at the top / surface for each scenario:

| depth (m) | CO2 % | pct dissolved (B) | pct dissolved (A) |
|-----------|-------|--------------------|--------------------|
| 300  | 15% | 70.3  | 100.0 |
| 300  | 50% | 72.4  | 100.0 |
| 300  | 85% | 74.4  | 100.0 |
| 300  | 100%| 75.6  | 100.0 |
| 500  | 15% | 71.4  | 100.0 |
| 500  | 50% | 72.2  | 100.0 |
| 500  | 85% | 66.9  | 100.0 |
| 500  | 100%| 35.0  | 100.0 |
| 1000 | 15% | 72.1  | 100.0 |
| 1000 | 50% | 69.8  | 100.0 |
| 1000 | 85% | 47.7  | 100.0 |
| 1000 | 100%| 62.4  | 100.0 |
| 1500 | 15% | 72.7  | 100.0 |
| 1500 | 50% | 68.4  | 100.0 |
| 1500 | 85% | 60.8  | 100.0 |
| 1500 | 100%| 91.4  | 100.0 |

**Method A dissolves 100% of the injected CO2 in every single scenario**,
well before the bubble reaches the surface.

## Is that a bug? No — it's the original's own finding, just more extreme

The 2002 report says this outright (Chapter 5, §5.1.1, discussing its own
Fig. 5-1): *"The mass transfer rate as computed following the method
suggested by Mori et al. predicts much faster dissolution rates than the
rate reported by Hirai et al."* — i.e. **Method A > Method B in speed is
the original's own documented result**, not an artifact introduced here.
This reimplementation reproduces that ordering correctly in every
scenario tested.

What's *not* obviously right is the magnitude — saturating at 100% in
every case makes Method A useless as a discriminating comparison (there's
no variation left to look at). Tracing a representative case (1000 m,
50% CO2) to the underlying numbers:

- Method A's rate formula is `area × k_L × ρ_sea × x_gs` (Eq. 4-5)
- At representative mid-column conditions, `x_gs` (this model's
  [MODERNIZED] fugacity-corrected Weiss 1974 solubility, EQUATIONS_SPEC.md
  §4) comes out to **≈5.8% CO2 by mass** — near the upper end of what's
  physically plausible for CO2-in-water solubility (published ceilings are
  roughly in the 5–7 wt% range at optimal low-temperature, moderate-to-high
  pressure conditions), so not obviously wrong in isolation.
- But Method B's rate **never references `x_gs` at all** — it uses
  Hirai's constant reported flux directly. Method A's effective flux at
  these conditions comes out to roughly **20× Hirai's reported flux**,
  which is what drives the 100%-every-time result.

**Best current explanation**: this model's solubility substitution (Weiss
1974, calibrated near atmospheric pressure, extended to depth via a
fugacity correction) is a linear Henry's-law extrapolation, and real
CO2-water solubility is known to be sub-linear (saturating) at the
50–150 bar pressures this scenario matrix covers — a limitation already
flagged in EQUATIONS_SPEC.md §4 before this comparison was run. Method A
is directly exposed to that extrapolation error (it multiplies by `x_gs`);
Method B is structurally insulated from it (constant empirical flux, no
solubility term). That's a genuine, useful distinction to know about the
two methods, independent of whether the exact 100% figures are right.

## Update: what happened after implementing Duan & Sun (2003)

The solubility upgrade was implemented properly (primary-source
coefficients cross-validated against an independent implementation,
textbook reference check, salting-out direction check — full account in
EQUATIONS_SPEC.md §4). Comparing the two solubility models directly
across this scenario matrix:

| depth (m) | CO2 % | x_gs (Weiss) | x_gs (Duan & Sun) |
|-----------|-------|--------------|---------------------|
| 500  | 50% | 0.03917 | 0.03564 |
| 1000 | 50% | 0.05940 | 0.04944 |
| 1000 | 85% | 0.06816 | 0.05632 |
| 1500 | 85% | 0.07585 | 0.05853 |

Duan & Sun gives **5–25% lower** solubility than Weiss, growing with
depth/pressure — exactly the direction hypothesized below (Weiss
over-extrapolates a linear model into a regime where real solubility
saturates).

**But re-running the full Method A vs. B matrix with Duan & Sun wired in
gives the identical result: Method A still dissolves 100% of injected
CO2 in every single scenario**, with step counts essentially unchanged
from the Weiss-based run. A 5–25% reduction in driving force doesn't
come close to closing what turns out to be a much larger gap (recall the
traced example: Method A's effective flux was ~20× Hirai's reported
constant flux at representative conditions).

**Corrected conclusion**: the "best current explanation" section below,
written before this upgrade, was only half right. It correctly identified
that Weiss over-predicts relative to a more rigorous model — but that
over-prediction isn't what's driving Method A's saturating behavior. The
real driver is the Sherwood-correlation mass-transfer coefficient itself:
for a small (1 cm), fast-rising bubble, the resulting flux is large
enough to fully dissolve the CO2 well before the bubble reaches the
surface, more or less regardless of which reasonable solubility value
feeds into it. That makes the original's own finding — Method A dissolves
much faster than Method B — a **robust** result under this
reimplementation, not a fragile one contingent on solubility-model choice.
It also means the magnitude (100% every time) is not something a better
solubility model alone is going to fix; discriminating between
compositions/depths with Method A would need either smaller bubble sizes,
a shorter rise distance, or revisiting the Sherwood correlation's
Reynolds-number regime — out of scope for this pass.

## Bottom line

- Both methods correctly reproduce the original's own *qualitative*
  ordering (A faster than B) — a real, not-previously-checked confirmation,
  and one that held up under a substantially better solubility model, not
  just the first-pass approximation.
- Method A's *magnitude* (100% dissolved in every scenario) is a genuine
  property of the Sherwood-correlation approach at this bubble size, not
  a solubility-model artifact — confirmed, not just hypothesized, after
  the Duan & Sun upgrade.
- **Recommendation unchanged**: Method B remains the default for any
  results feeding into the revised report's Chapter 5 reproduction, since
  it's the one that produces depth/composition-discriminating results.
  Method A is useful for confirming direction (it's faster) but not for
  quantitative comparison across scenarios, for reasons now understood
  rather than merely suspected.
