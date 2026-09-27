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
