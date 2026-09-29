# Phase A: Source Verification

Checking the 2002 thesis's own Table 4-1 (and supporting prose) against
primary sources, per
[../STUDY_PLAN.md](../STUDY_PLAN.md) Phase A. Searched via WebSearch/
WebFetch against publisher pages (Wiley, ScienceDirect), OSTI/ETDEWEB
(which often carries fuller abstracts for older energy-research papers
than a bare search snippet), and conference-proceedings indexes.

**Headline limitation, stated up front**: none of these 1990s papers are
open-access, and this project has no institutional journal subscription
(a documented constraint — see [../../CLAUDE.md](../../CLAUDE.md)). What
follows verifies that each citation is real, correctly identified, and
methodologically consistent with how the 2002 thesis describes it, and
recovers abstract-level detail — it does **not** re-derive the exact
reported numeric coefficients from the primary full text, because that
text isn't accessible. Three things were found, though, that are worth
having even without exact-number verification: two citation
inconsistencies inside the 2002 thesis itself, and — more importantly for
this study — real experimental-geometry differences between sources that
matter for whether they're comparable to a spherical free-rising-bubble
model at all.

## Per-source findings

### Hirai et al. (1996) — Energy Conversion and Management 37(6-8):1073-1078
**Real, correctly cited.** Confirmed title, journal, volume/pages via
multiple independent listings.

**Internal inconsistency found in the 2002 thesis itself**: its own §4.3.3.1
prose states Hirai's non-hydrate rate as **1.25×10⁻⁵ kg m⁻² s⁻¹**
(`original/thesis_full_text.txt` line 918), but the equation the thesis
actually uses for its "Method B" model (Eq. 4-11, same document, line
1021) uses **1.25×10⁻⁴** — a factor of 10 different, for a value
attributed to the same paper in the same document. This project's own
`model/co2n2_bubble/mass_transfer.py` implements Eq. 4-11's value
(1.25×10⁻⁴), which is the value actually load-bearing in the original's
own model — a defensible choice (it's what the original *computed with*,
not just mentioned in a literature survey) but flagged here as resting on
an internally inconsistent source.

**Methodological caveat**: the paper's own title/abstract describes
"liquid CO2 in pressurized water **flow**" — a forced-convection flow-cell
experiment, not a freely rising or falling droplet. Its characteristic
velocity is an imposed flow rate, not a buoyancy-driven terminal rise
velocity. This matters for §3 of the study plan: the rigid/mobile-sphere
theory being tested assumes free rise under gravity. A forced-flow
measurement isn't necessarily wrong to compare against, but it's a
different hydrodynamic regime and should be tagged as such, not silently
pooled with free-rise data.

### Fujioka et al. (1994) — International Journal of Energy Research 18:765-769
**Real, correctly cited.** Abstract confirmed directly: "the shrinkage
rate of liquid CO2 droplets in water at 3°C was measured... using a
high-pressure vessel... It is predicted... that a thin film of hydrate
will form at the interface... and will greatly control the dissolution."
Consistent with the 2002 thesis's description (diameter-reduction rate,
hydrate-coated). No pressure value recovered from the abstract (the 2002
thesis attributes the 5.0×10⁻⁷ m/s figure to specific reported
conditions not visible in the abstract alone) — exact numeric value not
independently re-confirmed, but the paper, methodology, and quantity type
(a genuine discrete-droplet diameter-reduction measurement, not a flow-cell
or bulk-mass measurement) all check out. **This is the source whose
geometry most closely matches the study's spherical free-rising-droplet
assumption.**

### Brewer et al. (2000) — Marine Chemistry 72:83-93
**Real, correctly cited** — full author list confirmed (Brewer, Peltzer,
Friederich, Aya, Yamane). **Depth discrepancy noted**: the 2002 thesis
doesn't state the depth for this citation; independent listings give
**619 m** (Monterey Bay in-situ field experiment via ROV), not the 684 m
figure one secondary listing suggested — 619 m is used going forward,
sourced from the OSTI abstract directly.

**Important methodological finding**: the abstract describes **two**
experimental configurations, and *neither is a discrete rising bubble or
droplet*: (1) rapid injection producing "a flocculant mass of hydrate,"
and (2) slower injection producing "a simple two-layer system with a
near-planar interface" between liquid CO2 and the hydrate film. The
mass-transfer figure the 2002 thesis attributes to this paper
(3.4×10⁻⁶ mol m⁻² s⁻¹) almost certainly describes dissolution from one of
these two bulk/planar geometries, not a spherical bubble.

**Consequence for this study**: comparing Brewer's reported coefficient
against a spherical-bubble Sherwood-number prediction (§3 of the study
plan) is not a like-for-like comparison — a planar interface and an
irregular flocculant mass have different characteristic length scales and
different boundary-layer development than a sphere. **Recommendation**:
carry this data point in the compiled dataset with an explicit
`geometry = planar/mass` tag, and exclude it from the primary
spherical-bubble regime-reconciliation comparison in Phase E, reporting it
separately instead. This is a genuine scoping correction relative to the
2002 thesis's own Table 4-1, which listed it alongside bubble/droplet
measurements without noting the geometry difference.

### Aya et al. — two different papers, one missing from the original bibliography
The 2002 thesis's Table 4-1 cites "**Aya et al. (1992)**" for a
diameter-reduction rate of 3.9×10⁻⁹ m/s (hydrate-coated). Its own
reference list, however, only contains **Aya, Yamane & Nariai (1997)**,
"Solubility of CO2 and Density of CO2 Hydrate at 30 MPa," *Energy*
22:263-271 — confirmed real and correctly listed, but a different paper
on a different topic (solubility/density, not diameter-reduction
kinetics) published five years later.

Search confirms a genuinely separate **Aya, Yamane & Yamada (1992)**
paper exists: "Stability of clathrate-hydrate of carbon dioxide in highly
pressurized water," presented at the ASME *Fundamentals of Phase Change:
Freezing, Melting, and Sublimation* conference (HTD vol. 215, 1992) — a
plausible source for the diameter-reduction figure, given its subject
(hydrate stability under pressure) and date match the in-text citation
exactly. **This paper is not in the 2002 thesis's own reference list** —
a genuine bibliographic gap in the original, not an error introduced by
this revision. Exact numeric value not independently recovered (conference
proceedings from 1992 aren't indexed with abstracts in the sources
checked).

### "Tabe et al. (1999)" — resolved, not a gap
The 2002 thesis's Table 4-1 cites "Tabe et al. (1999)" for a constant
hydrate mass-transfer rate of 1.15×10⁻⁴ kg m⁻² s⁻¹. This is **not** a
separate missing reference — it's an informal in-text shorthand for
**Hirai, Tabe, Tanaka & Okazaki (1999)**, "Advanced CO2 Sequestration
Technologies in Intermediate Depth of Ocean," 5th ASME/JSME Thermal
Engineering Joint Conference (confirmed present in the thesis's own
bibliography under Hirai's name, first author). Benign naming
inconsistency, not a bibliography error.

### Saito et al. (2000) — Environ. Sci. Technol. 34:4140-4145
Already substantially checked in this project's Phase 1
([../../LITERATURE_UPDATE.md](../../LITERATURE_UPDATE.md) §3); the
2.0×10⁻⁴ m/s non-hydrate coefficient is described consistently in both
the 2002 thesis's own two mentions of it (§3.2 and Table 4-1) — no
internal inconsistency found here, unlike Hirai's entry above.

## A fourth finding, added while starting Phase B: gas vs. liquid CO2

Building the rigid-sphere model surfaced something the geometry/flow-regime
tagging above didn't yet separate out: **most of the 1990s hydrate-era
literature is about *liquid* CO2 droplets, not *gas* bubbles.** Fujioka
(1994) is titled "Shrinkage of liquid CO2 droplets in water"; Hirai (1996)
is "Transport phenomena of **liquid** CO2 in pressurized water flow"; Aya
and Brewer's work is from the same research context (liquid CO2 disposal
at depths near or below its liquefaction boundary, ~1800 m per this
project's own `report/revised_report.md` §2). That's a real, physically
distinct disperse phase from the CO2/N2 *gas* bubbles this entire project
otherwise models — different density, different viscosity ratio against
the surrounding water (which is exactly the parameter, per STUDY_PLAN.md
§3, that determines whether the Hadamard–Rybczynski mobile-interface limit
even applies), and for a droplet, "rigid vs. mobile" isn't only about
surface contamination, it's also about the two fluids' viscosity ratio.

`data/coefficients.csv` now has a `disperse_phase` column recording this.
**Consequence**: only two entries in the entire dataset are genuine gas
bubbles — Saito et al. (2000) and Cho & Choi (2019) — making them the only
direct tests available for the gas-bubble rigid/mobile theory in
STUDY_PLAN.md §3.1/3.2. The liquid-CO2 entries (Fujioka, Hirai, Aya,
Tabe/Hirai) remain useful for the hydrate-film-diffusion question (§3.3,
Phase D) — hydrate shell diffusion resistance doesn't depend on what's
inside the shell — but are not valid tests of the gas-bubble boundary-layer
theory Phase B is about to implement. This is the second scope correction
this dataset has produced (after Brewer's geometry issue) and is applied
the same way: noted, not silently absorbed.

## Phase G addendum: new sources for the hydrate-film-growth deep-dive

Five additional sources, retrieved and read (abstracts/full text as
access allowed) while investigating Phase D's flow-dependence working
hypothesis further — see
[../analysis/phase_g_series_resistance.md](../analysis/phase_g_series_resistance.md)
for how these are used. Same access-limit caveat as the rest of this
file: full text wasn't retrievable for most of these (paywalled), so
findings below are abstract-level / secondary-source-corroborated, not
independent primary-text verification, exactly as flagged elsewhere in
this document.

### Ogasawara, Yamasaki & Teng (2001) — *Energy & Fuels* 15:147–150
**Real, correctly cited** (DOI 10.1021/ef000151n, confirmed via ACS and
multiple independent listings). A water-tunnel study built specifically
to measure what Phase D could only infer indirectly: mass transfer from
CO2 drops **with and without a hydrate shell**, as a direct function of
water velocity. Per secondary-source summaries (full text paywalled, not
independently re-derived): drop-shrinkage rate increases with water
velocity for both cases; the hydrate-shelled case's transfer coefficient
was evaluated via "a series-mass-transfer model" (external convective
resistance in series with the shell's own diffusive resistance) — the
mechanism `../model/series_resistance.py` tests quantitatively. Reported
aggregate numbers (solvent-side coefficients ks ≈ 1.5×10⁻⁴–7.5×10⁻⁴ m/s,
Sherwood numbers ≈ 7–37) came through a secondary synthesis without a
clear statement of which case (shelled vs. bare) or velocity they
correspond to — **ambiguous, not resolved, and deliberately not added to
`coefficients.csv`** as a result; forcing an unverifiable label onto a
number would be worse than leaving the gap explicit, per this project's
standing practice (e.g. the Hirai 1.25×10⁻⁴ vs. 1.25×10⁻⁵ discrepancy
above, carried as two candidates rather than silently resolved).

### Teng, Yamasaki & Shindo (1996) — *Chemical Engineering Science* 51(22)
**Real, correctly cited** (DOI 10.1016/0009-2509(96)00358-2). A different
mechanism from flow-enhanced transfer, found while researching the same
question: CO2 hydrate is a nonstoichiometric compound whose CO2 mole
fraction *within the shell* (x_CO2^H) decreases as the shell grows; per
the secondary-source summary, once x_CO2^H falls to ≈0.098 (from an
initial ≈0.115), "the hydrate layer becomes unstable and collapses into
hydrate clusters." This raises a genuinely different candidate
explanation for flow-sensitivity, not tested quantitatively in this
phase: episodic shell collapse-and-regrowth (rather than a
steady-thickness diffusion barrier) would expose fresh, uncoated liquid
CO2 to water periodically, and forced flow could plausibly accelerate the
approach to this instability threshold (by speeding whatever process
depletes CO2 from the shell) — a mechanism this phase's series-resistance
test does not capture at all, since that test assumes a fixed, intact
shell throughout. Flagged as a real alternative, not pursued further here
for lack of a quantitative growth-vs-flow relationship to test it with.

### Kar, Bhati, Acharya, Mhadeshwar, Venkataraman, Barckholtz & Bahadur (2021) — *Chemical Engineering Science* 234:116456
**Real, fully open-access, read directly in full** (not just an
abstract — a genuine exception to this file's usual access-limit caveat).
Central finding, directly relevant to Phase D's working hypothesis:
contrary to the widely-cited heat-transfer-controlled film-growth models
this project's initial hypothesis leaned toward (Mori, 2001; Uchida
et al., 1999), this paper presents scaling arguments — validated against
multiple experimental datasets including CO2 hydrates specifically, all
R² > 0.98 — showing heat transfer is **not** the rate-limiting mechanism
for the initial (seconds-timescale) hydrate film-formation phase; water's
high thermal effusivity keeps local temperature rise negligible relative
to subcooling. The paper's own diffusion(mass-transfer)-limited
alternative model explicitly states its fitting "growth rate constant" K
depends on "hydrodynamic perturbations near the film front," citing a
geometry-driven difference between a gas-bubble study and a bulk/planar
study as illustration — but adds "the detailed dependence of K on...the
hydrodynamic perturbations...is not currently explored." Important
scope caveat for this project's own purposes: the paper's own conclusion
distinguishes this fast initial *film-formation* phase (which it argues
is diffusion-limited) from *later-stage* hydrate growth, stating plainly
that "heat transfer will play a significant role in later stages of
hydrate growth along with gas diffusion considerations through the
hydrate layer" — i.e. the ~1000+ second timescale this project's Method H
actually models (an already-coated bubble/droplet dissolving as it rises)
is explicitly *not* the regime this paper's critique most directly
targets, so it narrows rather than eliminates Mori-type heat-transfer
mechanisms as relevant to this project's own problem.

### Peng, Dandekar, Sun, Luo, Ma, Pang & Chen (2007) — *J. Phys. Chem. B* 111(43):12485–12493
**Real, correctly cited.** Directly relevant geometry — hydrate film
growth measured on a **single gas bubble suspended in water** (not a
planar interface or a droplet), matching this project's own bubble
geometry more closely than most of the Phase A dataset's liquid-droplet
sources. Per the abstract: lateral film growth rates measured for
CH4, C2H4, CO2, and gas mixtures at four fixed temperatures; film
thickness inversely proportional to driving force (subcooling). **The
bubble in this experiment was suspended (quiescent), not exposed to
varying flow** — so this paper cannot itself supply a flow-velocity
dependence, despite being the closest geometric match to this project's
own hydrate-coated bubble problem found in this search.

### Sun, Chen, Ma, Huang, Luo & Li (2007) — *J. Crystal Growth* 306:491–499
**Real, correctly cited.** Same quiescent-gas-bubble geometry as Peng
et al. above, extended to aqueous surfactant solutions (SDS). Per the
abstract: SDS promotes hydrate film growth below ≈1000 mg/L (most
efficient near 500 mg/L) and inhibits it above that. Also a quiescent
experiment — no flow-velocity variable tested.

**Net effect of these last two sources on this phase's scope**: the two
studies that used the geometrically closest setup to this project's own
problem (a suspended gas bubble) both deliberately held flow at zero,
while the study that did vary flow (Ogasawara et al.) doesn't specify a
disentangled shelled-vs-bare, velocity-resolved correlation recoverable
without primary-text access. This is a genuine, confirmed gap in the
accessible literature — not a search failure — consistent with Phase D's
own original framing of this thread as the harder, less-standardized one.

## What this means for Phase B onward

- Use the values as reported in the 2002 thesis, since exact primary-text
  verification isn't achievable without journal access — but every value
  now carries an explicit confidence/geometry annotation in
  `coefficients.csv`, rather than being treated as uniformly reliable
  the way the original Table 4-1 presented them.
- **Brewer et al. (2000) is flagged for exclusion from the primary
  spherical-bubble comparison** in Phase E, on genuine geometric grounds,
  and reported separately instead.
- **Hirai et al. (1996) is flagged as forced-convection, not free-rise** —
  usable, but its Reynolds number should be computed from the paper's
  flow velocity, not a rise-velocity model, if the exact experimental
  flow rate can ever be recovered; until then, treat comparisons against
  it as approximate.
- The Hirai non-hydrate 1.25×10⁻⁴ vs. 1.25×10⁻⁵ discrepancy is carried
  forward as *two* candidate values, not resolved to one, since the
  primary source that would settle it isn't accessible.
