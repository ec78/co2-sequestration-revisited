# Phase G — Hydrate Film Growth / Flow-Dependence Deep-Dive: Findings

Follow-up to [phase_d_findings.md](phase_d_findings.md), pursuing the
thread [PROJECT_THESIS.md](../../PROJECT_THESIS.md) §6.3 flagged as
"genuinely new research, not integration" and explicitly higher-risk than
the shape-regime work that preceded it. Working hypothesis going in: flow
affects hydrate shell thickness/growth, which is why Hirai et al.
(1996)'s forced-flow hydrate-coated flux values sit above Fujioka et al.
(1994)'s quiescent value, even though a simple fixed-shell diffusion
model predicts no such dependence. This phase tested that hypothesis
against real, newly-retrieved literature rather than leaving it asserted.

## What changed since Phase D

Five new sources, retrieved and read (not recalled from memory — see
[../data/SOURCES.md](../data/SOURCES.md)'s "Phase G addendum" for full
per-source detail and access-limit caveats):

1. **Ogasawara, Yamasaki & Teng (2001)**, *Energy & Fuels* 15:147–150 — a
   water-tunnel study built specifically to measure CO2-drop mass
   transfer with and without a hydrate shell as a function of water
   velocity. Confirms, independently of Hirai's data, that shrinkage rate
   increases with flow velocity, and reports doing so via a **series
   mass-transfer model** for the shelled case — exactly the standard
   two-film mechanism this phase goes on to test quantitatively.
2. **Teng, Yamasaki & Shindo (1996)**, *Chem. Eng. Sci.* 51(22) — a
   different candidate mechanism: CO2 hydrate is nonstoichiometric, and
   the shell's own CO2 content drops as it grows until it hits an
   instability threshold (x_CO2^H ≈ 0.098) and **collapses into
   clusters**. Raises episodic shell collapse/regrowth as a real
   alternative to steady-thickness diffusion — not testable with what
   this project has access to (no flow-vs-collapse-rate data found), but
   worth recording as a named, real candidate rather than leaving the
   mechanism question as a single hypothesis.
3. **Kar et al. (2021)**, *Chem. Eng. Sci.* 234:116456 — fully open access,
   read in full. Directly complicates the working hypothesis: presents
   strong, multi-dataset-validated evidence (R² > 0.98, including CO2
   hydrates specifically) that **heat transfer is not the rate-limiting
   mechanism for the fast, initial hydrate film-formation phase**
   (seconds), contrary to the Mori (2001)-style heat-transfer models the
   original working hypothesis leaned toward. Important nuance in this
   project's favor, though: the paper's own conclusion explicitly
   reserves heat transfer a role in "later stages of hydrate growth,"
   which is the ~1000+ second regime Method H actually models (an
   already-coated, slowly-dissolving bubble) — so this finding narrows,
   rather than eliminates, the relevance of flow/convection to this
   project's specific problem.
4-5. **Peng et al. (2007)** and **Sun et al. (2007)** — the two studies
   with the closest geometric match to this project's own problem (a
   single gas bubble suspended in water, not a droplet or planar
   interface) — both deliberately held flow at **zero**. A genuine,
   confirmed gap: the literature's best-matched geometry and its
   flow-varying study never overlap.

## What this phase actually tested: the series-resistance hypothesis

Ogasawara et al.'s own "series-mass-transfer model" framing is the most
standard, most directly implementable candidate mechanism available —
and, unlike a hydrate-film-growth-kinetics model, it requires **no new
unverified physics**: it's a combination of two things this project has
already built and validated.

`model/series_resistance.py` implements it:

- **Shell resistance**: backed out from Method H's existing Fujioka-based
  constant rate (`model/co2n2_bubble/mass_transfer.method_h_rate`),
  re-expressed as an equivalent `kL_shell` on the same driving-force basis
  (`ρ_sea · x_gs`) Method A already uses — the standard convention needed
  to combine two coefficients as series resistances. This is a modeling
  bookkeeping choice for this comparison, not a claim that Method H's
  rate secretly depends on `x_gs` — flagged explicitly in the module.
- **External resistance**: the existing rigid-sphere Sherwood correlation
  (`mass_transfer.method_a_kL`, `regime="spherical"`) — the same regime
  choice this project's main model already uses for hydrate-active
  bubbles (`EQUATIONS_SPEC.md` §5b: a hydrate shell is a rigid interface,
  with no basis for the shape-deformed treatment used elsewhere).
- Combined via the textbook two-film relation:
  `1/k_overall = 1/k_shell + 1/k_external`.

### Result: a real, quantitative negative finding

At representative bubble sizes (0.5–2 cm) and depths (500–1500 m):

| Db | depth | k_overall / k_shell at U=0.05 m/s | at U=3.0 m/s | max enhancement |
|---|---|---|---|---|
| 0.5 cm | 1000 m | 0.82 | 0.97 | 1.22× |
| 1.0 cm | 1000 m | 0.76 | 0.96 | 1.31× |
| 2.0 cm | 1000 m | 0.70 | 0.95 | 1.42× |

(Full sweep across 500/1000/1500 m and 0.5/1.0/2.0 cm gives the same
picture — see `series_resistance.enhancement_over_velocity_range`.)

**The shell resistance dominates so heavily that this mechanism predicts
at most ~1.2–1.4× enhancement** going from near-quiescent (0.05 m/s) to
fast forced flow (3 m/s) — because `k_shell` (~3.6×10⁻⁶ m/s, backed out
from Fujioka's rate) is roughly an order of magnitude smaller than
`k_external` even at low velocity (`k_external` ≈ 1.2×10⁻⁵ m/s at
0.05 m/s, rising to ≈ 7.9×10⁻⁵ m/s at 2 m/s — see the worked example in
`series_resistance.py`'s docstring), so external convection is never
close to being the limiting resistance, and `k_overall` is bounded above
by `k_shell` regardless of how fast the flow gets.

**That is not enough to explain what's actually observed.** The
harmonized hydrate-coated dataset ([phase_d_findings.md](phase_d_findings.md))
shows Hirai's forced-flow flux (3.0×10⁻⁴–1.5×10⁻³ kg/m²/s) running
roughly **1.2× to 6× above** Fujioka's quiescent value (2.5×10⁻⁴), and
the full bucket spans nearly three orders of magnitude. The
series-resistance mechanism's *own* upper bound (1.2–1.4×) sits at or
below the *low* end of that observed range, and nowhere close to the
high end.

## What this means

**A real mechanism was tested quantitatively, using this project's own
already-validated machinery, and found insufficient — a genuine, useful
negative result**, not a failure to find an answer. It rules out "the
shell stays physically the same, only the outside boundary layer
changes" as a *complete* explanation, and does so with a number, not just
a plausibility argument.

**This strengthens, rather than resolves, Phase D's original reading**:
whatever flow is doing, it most likely has to be changing the shell
itself — its thickness, its defect structure, or (per the newly-found
Teng, Yamasaki & Shindo 1996 mechanism) its stability/collapse dynamics —
not just how fast water moves past an unchanged shell. That is a sharper,
better-evidenced version of Phase D's "working hypothesis, not yet
tested" framing, even though it still isn't a quantitative answer.

**No accessible source provides a usable, quantitative shell-growth-vs-
flow correlation.** This isn't from a lack of searching: the two studies
using this project's own bubble geometry (Peng 2007, Sun 2007) held flow
at zero; the one study that varied flow (Ogasawara 2001) is paywalled
past its abstract, and even its secondary-source-reported numbers
couldn't be confidently attributed to the shelled vs. bare case. Genuinely
confirmed as harder than the shape-regime work
([../../analysis/shape_regime_integration.md](../../analysis/shape_regime_integration.md)),
exactly as flagged when this thread was queued.

## Consequence for the main thesis model: no change

**Method H's implementation in `model/co2n2_bubble/mass_transfer.py`
is deliberately left unchanged.** Adding a ~1.2–1.4× "flow correction"
based on the series-resistance mechanism tested here would suggest more
precision than this phase actually delivered — it would apply a real but
small, quantitatively-justified factor while silently ignoring that it
accounts for at most a fraction of the literature's own observed spread.
The honest choice is to leave Method H's flat, literature-sourced
constant rate as the best currently defensible model, and record what
this phase found and didn't find here instead of encoding a
false-precision patch into the simulation.

## Bottom line

Tested, not just asserted: whether flow could explain hydrate-coated
CO2's observed dissolution-rate spread via the standard, most obvious
mechanism (external boundary-layer resistance in series with an
unchanged shell). It cannot, on its own — quantitatively confirmed using
this project's own validated Sherwood-correlation machinery, not a new
unverified model. Two credible alternative mechanisms are now named and
sourced (shell-thickness/defect response to flow; nonstoichiometric
shell instability and collapse, Teng/Yamasaki/Shindo 1996), but neither
has an accessible, quantitative correlation this project can implement
without new experimental data it doesn't have access to. The
~2.9-order-of-magnitude hydrate-coated residual
([phase_e_reconciliation.md](phase_e_reconciliation.md)) remains
genuinely open — narrowed in explanation, not narrowed in magnitude.
