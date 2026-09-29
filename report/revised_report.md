# Ocean Sequestration of CO2/N2 Mixtures, Revisited

*A 2026 revisit of Erica Clower's August 2002 Stanford University M.S.
report of the same subtitle, submitted to the Department of Petroleum
Engineering (original advisor: Dr. Franklin Orr).*

## About this revision

The original report proposed and modeled direct ocean release of impure
CO2/N2 gas mixtures as a low-cost CO2 sequestration method, and compared
it economically to a Japanese gas-lift alternative (P-GLAD) and to direct
release of separated, liquefied CO2. This document revisits that work
after 24 years, without access to the original research facility,
laboratory, or any new experimental data. It is built entirely from: a
literature search of what happened to this research area since 2002, a
from-scratch Python reimplementation of the report's numerical model
(the original MATLAB is preserved for reference but not executed), and an
updated economic analysis against current carbon capture and storage
(CCS) cost benchmarks. The full working process — literature notes, model
source and validation, and economic analysis — lives alongside this
document in the same repository and is cited throughout rather than
repeated in full here.

**Headline finding, stated up front rather than saved for the
conclusion**: the central premise of the original report — that direct
release of CO2 into the open ocean water column is a viable low-cost
sequestration pathway — is no longer viable, for two independent reasons.
First, it has been prohibited under international law since 2007
(Section 3). Second, even setting the legal question aside, the economic
case for the approach has independently weakened, because the capture
costs it was designed to avoid have fallen faster than ocean-disposal
engineering could have closed the gap (Section 6). What survives from the
original work is the technical core: a bubble transport and dissolution
model whose central open question — reliable mass-transfer coefficients
for CO2 dissolving into seawater — is, remarkably, still open in the
literature today (Sections 2 and 4). That question turned out to be
worth pursuing on its own terms: a companion study
(`mass-transfer-study/`, not a further revision of the 2002 report but a
standalone effort this revisit's own literature review led to) finds that
most of the apparent disagreement for gas bubbles resolves once bubble
*shape* — not just surface contamination state — is modeled correctly
(a real reported coefficient matched to within 1% at a physically
plausible bubble size, using standard deformed-bubble theory with no
fitting), leaving a real, unresolved residual specifically in the
hydrate-coated case — see its own capstone summary,
[mass-transfer-study/analysis/findings.md](../mass-transfer-study/analysis/findings.md).

## 1. Introduction

Rising atmospheric CO2 concentrations have driven decades of research
into carbon sequestration pathways: geological storage in saline
aquifers, depleted reservoirs, and enhanced oil recovery; and, in the
1990s and early 2000s, direct disposal of CO2 into the deep ocean. Ocean
disposal exploited a simple physical fact — the ocean already holds a
vast natural CO2 reservoir, and adding to it seemed, for a time, to be a
matter of manageable degree rather than fundamental barrier. Within ocean
disposal, one strand of research asked whether the costly step of
separating CO2 from flue gas before disposal could be skipped entirely:
release the impure gas mixture directly, accept a less efficient
dissolution process, and save the separation cost. The 2002 report this
document revisits was a contribution to that strand, building a numeric
model of CO2/N2 bubble transport and dissolution and comparing its
economics to a Japanese gas-lift alternative (Saito et al., 2000, 2001)
and to conventional liquid CO2 release.

This revisit exists for three reasons, not one:

1. **The bubble transport and dissolution physics the original report
   developed is not obsolete**, even though its application is. The mass-
   transfer coefficient uncertainty the original conclusion flagged as an
   open problem — reported values for CO2 dissolution into seawater
   disagree by orders of magnitude depending on measurement method and
   hydrate state — is still, as of the most recent literature checked for
   this revision, an active and unresolved area of study (Section 4).
2. **The report is a useful case study in how a CCS research direction
   can close.** Unusually, this one didn't close because it was shown to
   be technically wrong. It closed for regulatory and public-acceptance
   reasons that arrived at almost exactly the same time the original
   report was being written (Section 3) — a fact the original author
   could not have known while writing it.
3. **The underlying ocean gas-transfer physics has a live modern
   successor field**, running in the opposite direction: ocean-based
   carbon dioxide *removal* (mCDR), which extracts CO2 from seawater
   rather than injecting it (Section 7).

Section 2 summarizes the phase-behavior and hydrate chemistry that
governs all of this and is carried forward from the original largely
unchanged. Section 3 covers what the original report could not have
known: the regulatory and field-research history of ocean CO2 disposal
from 2002 onward. Sections 4–5 cover the technical model — re-derived
independent of the original MATLAB source, reimplemented in Python, and
checked against the original's own qualitative findings. Section 6
rebuilds the economic comparison against current CCS costs. Section 7
places the surviving technical content on the current research map, and
Section 8 concludes.

## 2. Chemistry of Ocean Sequestration

*(Largely carried forward from the original report's Chapter 2; physics
unchanged, citations refreshed where the literature has moved.)*

Ocean CO2 sequestration, in any of its proposed forms, is governed by the
same underlying physics: hydrate formation, the phase behavior of CO2 and
CO2/N2 mixtures at oceanic temperatures and pressures, and the resulting
transport and dissolution behavior of a released bubble or droplet.

**Hydrates.** CO2 hydrates — crystalline, cage-like structures formed
between CO2 and water at high pressure and low temperature — form readily
under the pressure and temperature conditions found below roughly 400–500
m in the ocean. A hydrate shell around a rising bubble measurably retards
CO2 dissolution: Mori and Mochizuki (1998) and Brewer et al. (2000) both
report slower bubble shrinkage for hydrate-coated bubbles than for
uncoated ones, and Brewer et al. (2000) note the practical double edge of
this — hydrate formation can *help* deep-water sequestration by extending
residence time, but can *hurt* shallower injection if it slows dissolution
enough that a droplet survives intact into the ocean's upper mixed layer.

**Pure CO2 phase behavior.** CO2 density increases with depth faster than
seawater density does, and the original report's own Chapter 2 correctly
identifies that liquid CO2 becomes denser than seawater at roughly 1800 m
— above that depth, released CO2 rises; below it, it sinks. This
revision's reimplemented model independently reproduces the underlying
mechanism (Section 5): a Peng-Robinson equation of state applied to pure
CO2 in this project's own bubble model shows CO2 occupying a dense,
liquid-like phase at 500–1500 m depths (density 860–999 kg/m³) rather
than a low-density gas phase — direct numerical confirmation, via a
different route than the original's, of the same physical picture.

**CO2/N2 mixture phase behavior.** Nitrogen suppresses hydrate formation.
As N2 content increases, the pressure required to form hydrate at a given
temperature rises sharply, shrinking the depth range over which hydrate
forms at all. The original report used the CSMHYD thermodynamic program
(Sloan, 1998) to quantify this for CO2/N2 mixtures. CSMHYD has since been
superseded by CSMGem and by newer cubic-plus-association (CPA) equation-
of-state approaches; notably, a 2024 study found that even these newer
models can still be measurably outperformed by further-refined models
specifically for CO2 hydrate phase equilibrium — this remains an actively
worked problem, not a solved one (Frontiers in Energy Research, 2024; see
[LITERATURE_UPDATE.md §6](../LITERATURE_UPDATE.md)).

This is the physical fact the entire 2002 research direction rested on:
because real flue gas is mostly N2 (typically at most ~15% CO2), direct
release of the *unseparated* mixture would, thanks to N2's hydrate-
suppressing effect, dissolve differently — and in some depth ranges,
faster — than pure CO2 would. That physical insight is not wrong. What
changed is everything downstream of it (Sections 3 and 6).

## 3. Why This Research Direction Closed

The original report was written in a research environment where direct
ocean CO2 disposal was an open, actively studied question. It is not one
today, for reasons that were already in motion in 2002 and fully resolved
within the following five years.

**The regulatory question was settled in 2007.** On November 2, 2006, the
Contracting Parties to the London Protocol amended Annex 1 to permit CO2
stream disposal *only* into sub-seabed geological formations, conditioned
on the stream being overwhelmingly pure CO2. Disposal into the water
column — the entire subject of this report, both the CO2/N2 mixture
concept and the P-GLAD comparator — was excluded. The amendment entered
into force on February 10, 2007 (IMO; WRI, 2006; EPA — see
[LITERATURE_UPDATE.md §1](../LITERATURE_UPDATE.md) for full citations).

**The field research was already ending as this report was written.** In
March 2002, an international consortium (PICHTR, backed by a 1997 Kyoto
COP-3 agreement among the US, Japan, Norway, Canada, and Australia)
applied to the US EPA for a permit to conduct a large-scale liquid CO2
ocean release experiment off Kauai, Hawaii. Public comment, extended once
by the EPA due to volume, was unanimously opposed. The consortium
withdrew the application in June 2002 — the same year this report was
written — without publicly stating a reason. An attempted relocation of
the experiment to a site off Bergen, Norway met the same fate when the
Norwegian government revoked the permit for policy reasons (Nature, 2002;
Environment Hawai'i; see LITERATURE_UPDATE.md §2). Smaller field
experiments (Brewer, Peltzer, and collaborators at MBARI, under an
international program with Japan's NMRI and the University of Bergen)
continued for a few more years, producing papers through roughly 2005 on
plume behavior and ecological effects, before that research line also
wound down.

**The P-GLAD program followed the same trajectory.** Saito and
collaborators published follow-up technical work on the GLAD/P-GLAD
gas-lift system through approximately 2004–2005 (bubble structure,
pumping characteristics, design-factor correlations), then no further
publications on continued development were found. P-GLAD was marketed as
avoiding some of direct release's worst objections — shallow injection,
no liquefaction — but it was still water-column disposal, and it appears
to have been swept up in the same regulatory and political closure as
every other approach in this space.

**International climate assessment reflects the same timeline.** The
IPCC's 2005 Special Report on Carbon Dioxide Capture and Storage still
discussed ocean storage as a live category, citing "unknown biological
impacts, high costs, impermanence of ocean storage, and concerns
regarding public acceptance" as open barriers. By the Fifth Assessment
Report (2014) and Sixth Assessment Report (2022), ocean storage had
dropped out of the mitigation literature entirely (Wikipedia, "Direct
deep-sea carbon dioxide injection," citing Adams & Caldeira 2008 and
Benson & Surles 2006; cross-checked against the IPCC reports directly —
see LITERATURE_UPDATE.md).

The practical upshot: this report's entire subject was foreclosed by
regulation and by an evaporating field-research base within roughly five
years of being written, for reasons that were unrelated to whether the
underlying physics was sound.

## 4. Governing Physics: P-GLAD Model and Single-Bubble Release

*(Original Chapters 3 and 4. Both models have now been re-derived and
reimplemented independent of the original MATLAB source — the P-GLAD
gas-lift hydraulics in a later pass than the single-bubble model, with a
materially different outcome. See
[model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md) for the
single-bubble model's complete line-by-line account, and
[model/pglad/PGLAD_SPEC.md](../model/pglad/PGLAD_SPEC.md) for P-GLAD's.)*

### 4.1 P-GLAD model (reimplemented; does not reproduce the original's own numbers)

The P-GLAD system (Saito et al., 2000) is a gas-lift J-tube: low-purity
CO2 is injected at the bottom of a shallow upriser (~300 m), rises via
gas-lift transport while dissolving into the surrounding seawater, vents
any undissolved gas at the top, and the resulting CO2-rich seawater flows
down a separate downriser to deep disposal — combining shallow-water
injection convenience with deep-water disposal security, without a
separation step. There is no pump: the water flow rate is whatever the
gas-lift effect can sustain, found by matching ambient hydrostatic
pressure at both open ends of the system simultaneously (a two-point
boundary-value problem, solved by a shooting method — the original's own
stated approach).

The original report's Chapter 3 gives the governing equations (two-phase
pipe-flow conservation of mass and momentum, drift-flux relations) but,
unlike the single-bubble model, no accompanying code — the thesis's one
surviving appendix contains only the single-bubble driver. Reimplementing
P-GLAD meant working from the equations alone. One piece could not be
reused as originally specified: the two-phase friction correlation
(Govier & Aziz, 1972) was presented in its source as a graphical
correlation, not a closed-form equation, and that source isn't
accessible to this revision. Beggs & Brill (1973) — a fully closed-form,
still-standard two-phase pipe-flow correlation from the same
petroleum-engineering tradition — was substituted, the same kind of
modernization already used for the single-bubble model's solubility
correlation (Section 4.2).

**This reimplementation does not reproduce the original's own worked
example.** The original gives a fully specified case (0.5 m pipe,
200 m upriser injecting at 300 m, 900 m downriser discharging at 1000 m,
5 kg/s gas injection) and reports a solved water flow rate of
362.3 kg/s. This reimplementation, built strictly from the equations the
original actually states, finds no water flow rate near that value — the
pressure mismatch stays at a roughly constant 3.5–4.6 bar (about 4% of
the target) across a wide range of flow rates, including at 362.3 kg/s
itself, which is the signature of a missing term rather than a
convergence problem. A specific, independently corroborated reason is
available: the original's own results table shows the liquid flow rate
increasing by about 20% between injection and the top of the upriser —
far more than seawater's own density variation over 200 m could produce
— implying Saito et al.'s actual model couples water flow to gas
dissolution or entrainment along the upriser in a way the thesis's own
equations don't specify. In other words, the original report's four-page
presentation of P-GLAD appears to be an incomplete summary of Saito et
al.'s actual model, not a self-contained specification of it — confirming
this would need Saito et al.'s own paper directly, which isn't accessible
to this revision. Full account: `model/pglad/PGLAD_SPEC.md` §5.

This negative result doesn't affect Section 6's economic comparison,
which uses P-GLAD's literature-reported cost figure rather than this
reimplementation's own (unvalidated) hydraulics.

### 4.2 Single-bubble release model (re-derived and reimplemented)

The technical core of the original report is a single-bubble transport
and dissolution model, tracking a released bubble's depth, diameter,
rise velocity, and CO2 content over time. Four physical subsystems
determine its behavior:

**Seawater properties.** Temperature follows a fitted depth correlation
(Ohmura & Mori, 1998). Pressure and density originally came from Morgan's
`SEAWATER` MATLAB toolbox (1994); that toolbox is now superseded by the
TEOS-10/GSW standard, which this revision uses instead — a modernization
expected to have negligible numerical effect (differences at the
0.01–0.1 kg/m³ level) while removing a dependency on unmaintained
software.

**Bubble (gas mixture) density.** A Peng-Robinson equation of state
determines the bubble's density from its composition, temperature, and
pressure. Re-deriving this independently surfaced a genuine correctness
issue, not present in the original's own reported results but easy to
introduce in a naive reimplementation: **the equation of state's cubic
form can have three real roots**, and the thermodynamically correct one
has to be selected by minimizing residual Gibbs energy — not, as a first
pass of this reimplementation initially did, by always taking the
largest root. Getting this wrong specifically breaks pure and high-purity
CO2 behavior: at 500–1500 m depth, this project's own numerical check
shows pure CO2's cubic equation has only one real root, and it is the
dense, liquid-like one (860–999 kg/m³), not a low-density gas — direct
confirmation of the phase behavior described in Section 2. Correcting
this is unconditionally right for the CO2/N2 mixtures that are this
report's actual subject, since nothing keeps a hydrate-free mixture from
reaching its true equilibrium phase.

**Hydrate-affected behavior.** For pure or near-pure CO2 in the
hydrate-forming depth/temperature window, the physical picture is
different: a hydrate shell is understood to kinetically trap the bubble
core in a vapor-like state, preventing it from ever reaching bulk-liquid
equilibrium on the timescale of its rise, and to slow dissolution to the
constant rate reported by Fujioka et al. (1994) for hydrate-coated
bubbles. This revision implements that behavior explicitly (internally
called "Method H"): inside a documented hydrate window, the bubble is
held on the vapor branch of the equation of state and dissolved at
Fujioka's reported rate rather than the ordinary mass-transfer
correlations. The hydrate window's boundary is itself an approximation —
a full CO2/N2 hydrate phase diagram could not be recovered numerically
from the original report's own figure — but it is a physically motivated
one, not an arbitrary cutoff: hydrate is predicted to form when the
mixture's CO2 fugacity meets or exceeds pure CO2's fugacity at its own
equilibrium hydrate-formation pressure at the same temperature, using a
pure-CO2 boundary curve fit to two independently sourced and
cross-checked reference points (the CO2 hydrate system's two quadruple
points). This correctly captures the original's own qualitative claim
that N2 dilution shrinks the hydrate-forming region, reached by an
independent route rather than a digitized reproduction of the original's
figure — though its exact calibration for CO2/N2 *mixtures* specifically
remains unverified against real mixture data, an honestly open point
documented in `model/co2n2_bubble/hydrate_boundary.py`.

**Mass transfer.** Two independent mass-transfer approaches, both from
the original report, are implemented: a Sherwood-number correlation
(after Mori & Mochizuki, 1998, "Method A") and a constant empirically
reported flux (after Hirai et al., 1996, "Method B"). **CO2 solubility in
seawater** — the driving force behind both methods — could not be
recovered from the original (it was read off a hand-digitized figure, not
a formula); this revision instead implements the Duan and Sun (2003)
CO2-brine solubility model, the literature's standard reference for this
quantity at oceanic pressures. Because the primary 2003 paper could not
be read cleanly through the tools available for this revision, its
coefficients were sourced from an independent open-source implementation
and cross-validated digit-for-digit against fragments recovered from a
second, independent peer-reviewed source, then checked against a textbook
reference solubility value and confirmed to show the physically correct
salting-out response to salinity — full provenance in
[EQUATIONS_SPEC.md §4](../model/EQUATIONS_SPEC.md).

Rise velocity is governed by a force balance on a rigid sphere (Mori &
Mochizuki, 1998; a Weber-number argument justifies treating the bubble as
non-deforming), discretized and solved implicitly each timestep against
an iteratively updated drag coefficient — reproduced from the original's
own MATLAB structure essentially unchanged, but no longer the whole
story: see the next subsection.

**Bubble shape — added in this revision, not present in the original.**
The companion mass-transfer-coefficient study (Appendix; standalone,
grown out of this project's own literature review) found that this
model's own ~1 cm bubbles actually sit in the shape-*deformed* regime the
original's Weber-number argument was meant to rule out — not a
contradiction of the original so much as a check the original itself
never had the tooling to run. This revision now checks the bubble's
Eötvös number every timestep and, whenever it indicates a deformed shape,
substitutes an independently-verified ellipsoidal (Mendelson, 1967) or
spherical-cap (Davies & Taylor, 1950) terminal velocity for the
rigid-sphere force balance, together with a correspondingly different
mass-transfer coefficient for Method A. Hydrate-coated bubbles are
deliberately excluded from this substitution — a hydrate shell is a rigid
interface, the opposite premise from the deformable-interface theories
this uses. Full account, including the new surface-tension parameter this
required and the numerical check justifying treating rise velocity as
quasi-steady at each timestep: [EQUATIONS_SPEC.md
§5b](../model/EQUATIONS_SPEC.md). This is not a minor refinement — see
Section 5.

## 5. Simulation Results

The reimplemented model was run across the original's own scenario
matrix — 15%, 50%, 85%, and 100% CO2, injected at 300, 500, 1000, and
1500 m — and checked against the original's own stated qualitative
findings, not against its exact numeric output (which is not recoverable:
several of the original's own helper subroutines were not included in
its published appendix, and the solubility figure's underlying data
points are lost along with it — see EQUATIONS_SPEC.md §8 for the full
accounting of what can and cannot be checked).

**What reproduces correctly.** The original's central claim about the
CO2/N2 mixtures — that low-purity bubbles *accelerate* as they rise, as
the insoluble N2 fraction expands under decreasing pressure and lowers
bubble density — reproduces cleanly. A representative run (15% CO2
injected at 1000 m) shows rise velocity increasing from 0.24 to 0.32 m/s
and diameter growing from 1.0 to 4.6 cm over the ascent. (These velocities
are lower, and the range narrower, than an earlier checkpoint of this
model reported — 0.53 to 1.13 m/s — because that checkpoint used
rigid-sphere theory throughout; §4.2's shape-regime addition now applies
across essentially this entire trajectory, and 0.2–0.3 m/s is also the
better-grounded number: it matches the well-documented experimental fact
that mm-to-cm bubbles in water rise at a roughly size-independent speed,
which rigid-sphere theory does not reproduce. See
[analysis/shape_regime_integration.md](../analysis/shape_regime_integration.md).)

**What required the equation-of-state fix to reproduce.** The original's
companion claim — that *pure* CO2 bubbles behave oppositely, decelerating
as they shrink — did not reproduce until the hydrate-affected pathway
(Method H, Section 4.2) was added. With it, a pure-CO2 bubble injected at
1000 m now shrinks slowly (1.00 → 0.89 cm) while hydrate-coated between
1000 m and roughly 500 m, then undergoes a sharp transition once it exits
the hydrate-forming depth window and behaves like an ordinary expanding
gas bubble the rest of the way to the surface. This two-regime behavior —
slow, hydrate-limited shrinkage at depth, followed by a rapid transition
near the hydrate boundary — is a substantively better match to the
original's qualitative description than a model without hydrate physics
can produce, and it is a direct, mechanistic illustration of why hydrate
formation matters as much as Section 2 says it does. (The hydrate-coated
shrinkage itself is deliberately unaffected by the shape-regime addition —
EQUATIONS_SPEC.md §5b keeps hydrate-coated bubbles on the rigid-sphere
treatment throughout, since a hydrate shell has no deformable interface
for shape theory to apply to.)

**Method A vs. Method B: a genuine confirmation, sharpened by the
shape-regime addition, not undermined by it.** The original report's own
Chapter 5 states that its Sherwood-correlation approach (Method A)
"predicts much faster dissolution rates" than its constant-flux approach
(Method B). This reimplementation confirms that ordering independently:
across every scenario tested, Method A dissolves 100% of the injected CO2
well before the bubble reaches the surface. Method B, whose own rate
formula is unaffected by bubble shape, still shows a large *indirect*
effect: because shape-deformed bubbles rise more slowly than rigid-sphere
theory predicted, they spend longer at depth, so Method B's dissolved
fraction rose from an earlier 35–92% range to **87–100%** across the same
scenario matrix — now closely matching, rather than falling well short
of, the original's own claim that ≥95% of injected CO2 dissolves before
reaching the mixed layer for injection above ~500 m. Tracing the
mechanism further than the original's own text does: Method A's effective
dissolution flux, now also shape-regime-aware, comes out roughly **140
times** larger than Method B's directly-reported literature flux at
representative mid-column conditions (up from an earlier ~20×, once
Method A's own mass-transfer coefficient became shape-aware too — the
deformed-bubble correlation it now uses in place of the rigid-sphere one
predicts substantially higher transfer at the same conditions, a known,
independently-documented property of that correlation, not an artifact).
Upgrading the solubility model from an approximate baseline to the
properly validated Duan & Sun (2003) model reduced the solubility
estimate feeding Method A by 5–25% — the theoretically expected direction
— but nowhere near enough to change the 100%-every-time result, and
neither did the subsequent shape-regime addition. That is a genuine,
useful finding in its own right: **Method A's speed relative to Method B
is a robust property of the Sherwood-correlation approach at this bubble
size, not an artifact of an imprecise solubility or velocity input.**
Method B — fully specified in the original with no reconstruction
uncertainty — is used as this model's default for any quantitative
comparison; Method A is retained as a directional check, per the
original's own use of it.

Full run outputs, plots, and the detailed comparison tables behind these
summaries are in
[analysis/PHASE3_NOTES.md](../analysis/PHASE3_NOTES.md),
[analysis/method_a_vs_b.md](../analysis/method_a_vs_b.md), and — for the
shape-regime addition specifically, including the full before/after
scenario matrix and its honest limitations (chiefly a new,
literature-grounded but temperature-extrapolated surface-tension
parameter this addition required) —
[analysis/shape_regime_integration.md](../analysis/shape_regime_integration.md),
including two demonstration runs referenced here directly:

- 500 m, 50% CO2 (Method B): [demo_500m_50pct.png](../analysis/demo_500m_50pct.png)
- 1000 m, 100% CO2 with hydrate compensation active: [demo_1000m_pureCO2_hydrate.png](../analysis/demo_1000m_pureCO2_hydrate.png)

## 6. Economic Comparison

The original report's economic argument compared three disposal routes
head to head: CO2/N2 mixture release ($118/ton CO2, no separation cost),
P-GLAD ($68/ton, also no separation cost, avoided via shallow gas-lift
injection), and direct liquid CO2 release ($126/ton, including
separation and liquefaction — the standard alternative the report argued
against).

That three-way comparison is moot today: none of the three routes is a
legal disposal option under the London Protocol (Section 3), so ranking
them against each other no longer answers a live question. The useful
comparison now is different: **how do these 2002 figures compare, in
real terms, to what CO2 sequestration actually costs today?**

Adjusting for inflation alone (CPI-U 179.9 in 2002 → ≈331.7 today, a
1.84× multiplier) puts the three 2002 figures at approximately $217,
$125, and $232 per ton in current dollars, respectively. Current,
segment-sourced CCS cost benchmarks — capture (~$61–80/ton for a modern
gas-fired plant, per NETL; a wider $40–240/ton range across the broader
historical literature), transport (as little as ~$2/ton for a favorable
large-pipeline case), and geological storage (~$10–80/ton, geology-
dependent, per NETL's 2024 saline-storage cost model) — combine to an
all-in modern range of roughly **$70–160 per ton**, for a project that,
unlike the original's mixture-release and P-GLAD routes, *does* include
full capture.

The fair comparison is therefore the original's liquid-CO2 route (the one
2002 figure that, like today's benchmarks, included capture cost)
against today's full-chain CCS: **≈$232/ton in 2002 dollars-adjusted, versus
≈$70–160/ton today.** That is a substantial real improvement — and it
did not come from ocean-disposal engineering catching up. It came from
capture technology itself getting dramatically cheaper over 24 years of
deployment and RD&D investment, a trend visible across every capture
technology and source type surveyed for this revision.

This matters for how the original report's economic argument should be
read today, independent of the legal question. The 2002 mixture-release
and P-GLAD concepts were, at bottom, a bet that separation would remain
expensive enough that engineering around it — accepting lower purity,
higher compression and transport volume, or added shallow-water
engineering complexity — was worth the tradeoff. Twenty-four years of
falling capture costs have substantially weakened that bet. Even setting
the legal prohibition aside entirely, the economic case for skipping
capture is considerably less compelling now than it was when this report
was written. Full sourcing, category-by-category figures, and the scope
caveats involved in this comparison are in
[analysis/economic_reanalysis.md](../analysis/economic_reanalysis.md).

## 7. Where the Field Went Instead

Two research directions absorbed what direct ocean CO2 disposal was
trying to accomplish, and both remain active today.

**Geological CCS** — the pathway the London Protocol's 2007 amendment
explicitly carved out as legal — is now the dominant CCS paradigm:
storage in saline aquifers and depleted reservoirs, often paired with
CO2-enhanced oil recovery, supported in the US by the 45Q tax credit
(currently $85/ton for point-source capture with dedicated geologic
storage, $180/ton for direct air capture with storage) and by regulatory
frameworks — Class VI injection wells under the Safe Drinking Water Act,
for instance — that did not exist in their current form in 2002.

**Ocean-based carbon dioxide removal (mCDR)** is the more surprising
successor, because it runs in the opposite direction from this report's
subject: rather than injecting industrial CO2 into the ocean, mCDR
extracts CO2 that is already in seawater or the atmosphere, through
approaches including ocean alkalinity enhancement, electrochemical ocean
carbon capture, and managed biomass sinking. The 2022 US National
Academies report *A Research Strategy for Ocean-based Carbon Dioxide
Removal and Sequestration* is the field's landmark assessment, and a
standing committee established in 2025 keeps it under active revision —
this is a live, growing research area, unlike the field this report
originally contributed to. mCDR inherits much of the same underlying
ocean chemistry and gas-transfer physics this report's model addresses
(seawater CO2 solubility, gas-liquid mass transfer, bubble or interface
behavior for some electrochemical approaches), just applied in the
reverse direction.

Neither of these is examined in depth here — that would be a different
report — but placing this report's surviving technical content
(Sections 2, 4, and 5) against this current map makes its continued
relevance concrete rather than abstract: the mass-transfer-coefficient
uncertainty this report's model runs into is not a historical curiosity,
it is a live input to at least one of these two active fields today.

## 8. Conclusion

What held up, after 24 years and without access to any new experimental
data: the core physical mechanisms this report identified are still
correct. Nitrogen genuinely suppresses hydrate formation and genuinely
changes CO2/N2 mixture dissolution behavior relative to pure CO2, in the
direction the original report described. Pure CO2's transition from
gas-like to liquid-like behavior with depth, and the distinct,
hydrate-mediated shrink-then-transition trajectory that follows from it,
reproduces under independent reimplementation. And the mass-transfer
coefficient problem the original conclusion flagged as unresolved — large,
unreconciled disagreement between reported CO2-in-seawater dissolution
rates depending on measurement method and hydrate state — is, checked
against the most recent literature available for this revision, still
genuinely open in the field at large, though this revision's own
companion study found that the non-hydrate, gas-bubble portion of it
resolves to within about 1% once bubble *shape* — ellipsoidal or
spherical-cap, not the idealized rigid sphere the original 2002 model
assumed throughout — is modeled correctly at a physically plausible
bubble size. That finding was then integrated back into this report's own
single-bubble model (Section 4.2), materially changing its own simulated
rise velocities and dissolution fractions (Section 5) in the process, not
left as a separate, disconnected result — leaving the hydrate-coated case
as the harder, still-unresolved residual.

What did not hold up: the premise that any of this adds up to an
implementable, economically favorable disposal method. It does not,
for two independent reasons that arrived on two different tracks. The
regulatory track closed the door outright, within about five years of
this report being written, for reasons — biological risk, permanence,
public acceptance — that had nothing to do with whether the engineering
worked. The economic track closed more slowly and more quietly: capture
technology, the very cost this report's central idea was designed to
avoid, simply got cheaper faster than any ocean-disposal engineering
could have kept pace with.

The broader lesson this report now demonstrates, better than it could
have known it was demonstrating in 2002, is that a technically sound CCS
research direction can be closed off by policy and public acceptance
long before — and largely independent of — any technical verdict on
whether it would have worked. The bubble transport and dissolution
physics in this report were never disproven. They were simply overtaken
by a regulatory decision made an ocean away from the laboratory, in the
same year the report was written, and by a capture-cost curve that kept
falling for two more decades after anyone had a reason to keep checking
whether skipping capture was still worth it.

## References

The original 2002 bibliography is preserved in full in
[original/thesis_full_text.txt](../original/thesis_full_text.txt)
(Sloan 1998; Saito et al. 2000, 2001; Mori & Mochizuki 1998; Brewer et
al. 1999, 2000; Hirai et al. 1996; Fujioka et al. 1994; Morgan 1994;
Govier & Aziz 1972; Chen 2001; and others). Sources consulted for this
revision, with full citation details and direct links, are in
[LITERATURE_UPDATE.md](../LITERATURE_UPDATE.md) (regulatory history, field
research history, hydrate thermodynamics, mass-transfer literature) and
[analysis/economic_reanalysis.md](../analysis/economic_reanalysis.md)
(current CCS cost benchmarks). Model implementation sources — including
the Duan & Sun (2003) solubility model's provenance chain — are cited
directly in [model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md).

## Appendix

Original MATLAB code: [original/appendix_a_original.m](../original/appendix_a_original.m)
(transcribed verbatim, not executed — see file header for what's missing
from the original appendix; no equivalent P-GLAD code was ever published
alongside the original). Reimplemented Python models:
[model/co2n2_bubble/](../model/co2n2_bubble/) (single-bubble, runnable via
[model/run_simulation.py](../model/run_simulation.py); governing equations
and full change history in [model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md))
and [model/pglad/](../model/pglad/) (gas-lift J-tube hydraulics; spec and
honest validation result in [model/pglad/PGLAD_SPEC.md](../model/pglad/PGLAD_SPEC.md)).

Companion research effort, grown out of this revisit's own literature
review but standalone rather than a further revision of the 2002 report:
[mass-transfer-study/](../mass-transfer-study/), reconciling the
CO2-seawater mass-transfer-coefficient discrepancy discussed in Sections
1, 4, and 8 — capstone summary in
[mass-transfer-study/analysis/findings.md](../mass-transfer-study/analysis/findings.md).
