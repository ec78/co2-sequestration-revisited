# Mass-Transfer Coefficient Reconciliation Study

A standalone research effort inside this repo (decision log:
[../PROJECT_THESIS.md](../PROJECT_THESIS.md) — the "Tier 2" option from the
discussion of where the thesis-revisit project could go next). Living plan
document; update in place as phases complete.

## 1. Motivation

The 2002 thesis's own conclusion flagged a problem it couldn't solve: reported
CO2-into-seawater mass-transfer coefficients disagree by 2–3 orders of
magnitude depending on source (see the original's Table 4-1). This project's
Phase 1 literature search (2026) confirmed that problem is *still open* —
current reviews treat it as an active, unresolved area, not a historical
footnote (see [../LITERATURE_UPDATE.md](../LITERATURE_UPDATE.md) §7). That
combination — a real, still-open physical question, with direct relevance to
a live research field (ocean-based carbon dioxide removal, mCDR) that this
project's own literature search surfaced — is what makes it worth a
dedicated effort, rather than another paragraph in the thesis revisit's own
conclusion.

## 2. Research question

**Can the reported scatter in gas-into-seawater mass-transfer coefficients be
explained by known physical regime differences — bubble surface mobility
(clean/circulating vs. contaminated/rigid), hydrate coating, and Reynolds
number — rather than remaining an unexplained empirical disagreement?**

If regime-matched theory reconciles most of the scatter (i.e., residual
disagreement *within* a regime is much smaller than the raw range *across*
regimes), that's a genuine, useful result: it turns "the literature
disagrees and nobody knows why" into "the literature agrees, once you
account for which physical regime each measurement was actually made
under" — directly useful to anyone (including mCDR researchers) who needs to
pick a coefficient for a new calculation and currently has no principled way
to choose among the published values.

## 3. Theoretical framework

Three mechanistically distinct regimes, each with an established analytical
prediction — not curve-fit to this project's own data, but derived
independently in the literature decades ago:

### 3.1 Rigid / contaminated interface (no-slip boundary)
A bubble with a surface immobilized by adsorbed surfactant or natural
organic contamination behaves, for mass-transfer purposes, like a rigid
solid sphere: no internal circulation renews the interface, so transfer is
governed by a diffusive boundary layer. Classic boundary-layer theory
(Levich, 1962) gives creeping-flow scaling `Sh ~ Pe^(1/3)`; the widely used
engineering correlations (Frössling, 1938; the similar rigid-sphere forms
used by Mori & Mochizuki, 1998 and reproduced in this project's own
`mass_transfer.py` as "Method A") extend this to moderate Reynolds number as
`Sh = 1 + a·Re^b·Sc^(1/3)`. **Signature: `Sc^(1/3)` scaling, and lower
absolute transfer than the mobile case at the same Re.**

### 3.2 Mobile / clean interface (circulating bubble)
A truly clean bubble surface (no surfactant, no contamination) permits
internal (Hadamard–Rybczynski) circulation, which continuously renews the
interface and enhances transfer. Levich's (1962) penetration-theory result
for this case:
```
k_L = (2/√π) · √(D·U/d)          Sh = (2/√π) · Pe^(1/2),   Pe = Re·Sc
```
(cross-checked directly against a secondary derivation citing Levich
verbatim — see study sources below). **Signature: `Sc^(1/2)` scaling (not
`1/3`), and — critically — a *higher* predicted coefficient than the rigid
case at identical Re, often by 100% or more at high Peclet number.** Real
seawater is rarely perfectly clean; this regime is the theoretical ceiling,
most relevant to laboratory measurements in deliberately purified water.

### 3.3 Hydrate-coated interface (solid-shell diffusion)
Once a solid clathrate hydrate shell forms, the rate-limiting step shifts
from liquid-phase convection to diffusion through the (effectively solid,
stagnant) shell. This project's own `mass_transfer.py` ("Method H") already
implements the practical consequence: hydrate-coated dissolution is modeled
via a *constant* empirically reported rate (Fujioka et al., 1994), not a
Reynolds-number-dependent correlation. **Signature: little to no dependence
on rise velocity/Reynolds number** — the opposite behavior from regimes 3.1
and 3.2, both of which scale with Re. This is the study's most direct
testable prediction: hydrate-coated literature values should show much
weaker correlation with reported bubble Reynolds number than non-hydrate
values do.

### Why this framework is worth trusting
None of these three forms were derived for this study — they're
30–90-year-old, independently established results (Levich 1962; Frössling
1938; Higbie 1935), still cited as the standard framework in a 2024 review
surveyed for this project (Frontiers in Physics, "Bubble mass transfer in
fluids under gravity," 2024), which explicitly confirms that surface
contamination reduces transfer relative to the clean case — the correct
qualitative direction for 3.1 vs. 3.2. Takemura & Yabe (1999) — already a
reference in the *original 2002 thesis's own bibliography* — is still cited
in that 2024 review as a standard rigid/contaminated-regime correlation,
which is a useful bridge: the original report was already drawing on
literature that current reviews still treat as current.

## 4. Approach

1. **Compile** a normalized dataset of reported coefficients spanning both
   the historical ocean-disposal literature (1990s–2000s, cm-scale bubbles,
   the original thesis's own sources) and modern literature (2010s–2020s,
   often much smaller bubbles, industrial/engineering context) — see
   `data/` and §5 below.
2. **Classify** each data point by which regime it was actually measured
   under, from the source paper's own stated conditions (hydrate
   present/absent; water source — natural seawater vs. purified lab water,
   as a proxy for likely contamination state; reported or inferable
   Reynolds number).
3. **Predict**: for each data point's regime and reported bubble
   size/velocity/temperature, compute what that regime's theoretical
   correlation (§3) predicts, using this project's existing
   `../model/co2n2_bubble/seawater.py` for water properties and the
   existing diffusivity correlation in `../model/co2n2_bubble/mass_transfer.py`
   for `D_gw`.
4. **Compare**: does the regime-matched prediction fall close to the
   reported value? Is the *residual* scatter (predicted vs. reported,
   within a regime) much smaller than the raw scatter across all reported
   values regardless of regime? Does the hydrate-regime subset show the
   predicted Re-independence?
5. **Write up** the result plainly — including if the answer turns out to
   be "no, regime alone doesn't explain it," which would itself be a real,
   useful finding (it would mean the field's disagreement has a different,
   still-unidentified cause).

This is entirely a desk/computational exercise — no new bubbles, no new
measurements. It is bounded by what's already been published, which is the
right boundary for what a literature reconciliation study can honestly
claim to do (see PROJECT_THESIS.md's own no-new-data constraint, which
applies here too).

## 5. Data sources

**Superseded by [data/coefficients.csv](data/coefficients.csv) and
[data/SOURCES.md](data/SOURCES.md)** (Phase A complete — see §6/§7
below). The table originally drafted here was the unverified starting
point; kept below only as a historical record of what was assumed before
verification.

<details>
<summary>Original unverified draft table (superseded)</summary>

| Source | Year | Value | Units | Regime (as reported) | Bubble scale |
|---|---|---|---|---|---|
| Brewer et al. | 2000 | 3.4×10⁻⁶ | mol m⁻² s⁻¹ | hydrate-coated | cm (field, deep-sea) |
| Aya et al. | 1992 | 3.9×10⁻⁹ | m/s (diameter reduction) | hydrate-coated | cm |
| Fujioka et al. | 1994 | 5.0×10⁻⁷ | m/s (diameter reduction) | hydrate-coated | cm |
| Tabe et al. | 1999 | 1.15×10⁻⁴ | kg m⁻² s⁻¹ | hydrate-coated | cm |
| Hirai et al. | 1996 | 3×10⁻⁴–1.5×10⁻³ | kg m⁻² s⁻¹ | hydrate-coated | cm |
| Hirai et al. | 1996 | 1.25×10⁻⁴ | kg m⁻² s⁻¹ | non-hydrate | cm |
| Hirai et al. | 1996 | 2.8×10⁻⁴ | m/s | non-hydrate | cm |
| Saito et al. | 2000 | 2.0×10⁻⁴ | m/s | non-hydrate | cm |
| Cho & Choi | 2019 | 3.6×10⁻⁵–1.0×10⁻⁴ | m/s | not hydrate-relevant (micro-bubble, industrial) | 10–30 μm |

**Provenance note**: the 1990s entries above are sourced from the *original
2002 thesis's own summary table* (its Table 4-1 and supporting prose), which
is itself a secondary citation of the primary papers — the thesis's own
table had OCR/transcription issues when extracted for this project (see
[../model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md) §6 for the same
issue affecting this project's earlier work), and where prose and table
disagreed, the prose was used as more reliable. **Phase A below is where
these get checked against primary sources directly**, not left as
secondary citations, before any conclusion leans on their exact values.
The Cho & Choi (2019) row was pulled directly from the primary paper.

</details>

## 6. Phased plan

### Phase A — Literature data compilation and verification ✅ (within access limits)
- [x] Attempted to read each primary source directly rather than trusting
      the 2002 thesis's citation of it. **Hard limit hit and accepted**:
      none of the 1990s sources are open-access and this project has no
      journal subscription (the same documented constraint as everywhere
      else in this repo) — abstract-level and bibliographic verification
      was achieved, exact full-text numeric re-derivation was not, and
      isn't expected to become possible later without a different access
      arrangement. Not treated as an open TODO.
- [x] Extended the search past Phase 1: added Cho & Choi (2019), a
      genuinely different bubble-size regime (10–30 μm industrial
      micro-bubbles vs. the historical literature's cm-scale bubbles).
- [x] Recorded what's available per entry (hydrate state, geometry, flow
      regime, confidence) in `data/coefficients.csv`; exact bubble
      diameter/Reynolds number for the 1990s sources noted as unavailable
      rather than guessed.
- [x] Produced `data/coefficients.csv` and `data/SOURCES.md`.

**Three real findings came out of this**, documented in full in
[data/SOURCES.md](data/SOURCES.md):
1. **A genuine internal inconsistency in the 2002 thesis itself**: its own
   prose states Hirai et al. (1996)'s non-hydrate rate as 1.25×10⁻⁵ kg
   m⁻² s⁻¹, but the equation it actually uses (Eq. 4-11, which this
   project's own model implements) uses 1.25×10⁻⁴ — a 10× difference for
   the same citation in the same document.
2. **A genuine bibliography gap in the 2002 thesis**: its Table 4-1 cites
   "Aya et al. (1992)" but its own reference list only contains an
   unrelated 1997 Aya/Yamane/Nariai paper. A separate, plausible 1992
   Aya/Yamane/Yamada conference paper was found and is likely the true
   source — but it was never in the original's own bibliography.
3. **A geometry mismatch serious enough to change the study's plan**:
   Brewer et al. (2000)'s reported coefficient comes from a bulk
   flocculant hydrate mass or a near-planar CO2/hydrate-film interface —
   not a spherical bubble or droplet at all. It cannot be fairly compared
   against a spherical-bubble Sherwood-number prediction. **Decision**:
   excluded from Phase E's primary comparison, reported separately
   instead — see `data/coefficients.csv`'s `geometry` column, which now
   also flags Hirai (1996) as forced-flow rather than free-rise, a
   milder version of the same issue.

### Phase B — Rigid/contaminated regime model ✅
- [x] Implemented in `model/rigid_sphere.py`, reusing the existing
      `model/co2n2_bubble` package (Method A's Sherwood correlation,
      seawater properties) rather than re-deriving the physics, plus a
      new genuine steady-state terminal-velocity solver (needed because
      the main model's rise-velocity solver is deliberately transient/
      history-tracking, not a terminal-velocity finder).
- [x] Validated against the dataset's only two genuine gas-bubble entries
      (Saito 2000, Cho & Choi 2019 — everything else turned out to be
      liquid CO2 or geometrically excluded, per the finding logged in
      `data/SOURCES.md`). **Neither matches cleanly, in two different,
      identifiable directions** — full results and interpretation in
      [analysis/phase_b_findings.md](analysis/phase_b_findings.md):
      - Saito (Re 300–21000): reported transfer is 3–6× **faster** than
        rigid-sphere theory predicts across the whole plausible bubble
        size range — a real gap, not noise, and the natural target for
        Phase C to try to close.
      - Cho & Choi (Re 0.0006–0.015): reported transfer is ~2× **slower**
        than predicted — most likely because Method A's correlation is a
        moderate-Re engineering fit being extrapolated 3-4 orders of
        magnitude below its normal range, not a physics disagreement.
        Flagged as a stress-test case rather than forced into either
        theory's comparison.

### Phase C — Mobile/clean regime model ✅
- [x] Implemented in `model/mobile_sphere.py` (Levich's formula, §3.2),
      deliberately reusing the rigid-sphere terminal velocity from Phase B
      as a conservative (understating, not inflating) stand-in for a full
      mobile-drag treatment — see module docstring.
- [x] **Answered the specific question Phase B raised**: yes. Mobile
      theory brackets Saito's reported 2.0×10⁻⁴ m/s across the whole
      plausible bubble-size range and lands within 8–32% of it at the
      physically reasonable larger-diameter end (15–30 mm), using a
      *conservative* velocity — where rigid theory (Phase B) missed by
      3–6×. Full numbers and honest framing in
      [analysis/phase_c_findings.md](analysis/phase_c_findings.md).
- [x] Checked Cho & Choi again for completeness: mobile theory lands
      within 8% for one of their two conditions but overshoots by >5× for
      the other — an inconsistent result that reinforces, rather than
      contradicts, Phase B's read that this Reynolds/Péclet regime
      (Pe ≈ 0.3–9) is below where either analytical theory reliably
      applies. Not treated as a second validation, and not treated as a
      refutation either — it's outside both theories' honest scope.
- No deliberately-purified/clean-water CO2-seawater data point turned up
  in the literature search to date — noted as a real gap in available
  data, not pursued further (would need new literature search effort
  disproportionate to this phase's scope).

### Phase D — Hydrate-coated regime model ✅
- [x] Built `model/hydrate_shell.py` — not a new predictive correlation
      (there's no diameter/velocity sweep to run the way Phases B/C had),
      but the unit-harmonization tool needed to put every hydrate-coated
      literature value (reported as a diameter-reduction rate, a mass
      flux, or a molar flux, across four different sources) onto one
      comparable basis — matching the 1500 m / pure-CO2 basis the 2002
      thesis's own Table 4-1 tried and failed to use consistently.
- [x] Tested the Re-independence prediction directly.
      **Partially contradicted, and the 2002 thesis's own prose already
      said so**: it explicitly states Hirai (1996)'s hydrate rate varies
      "depending on temperature, pressure, and rise velocity." Confirmed
      in the harmonized data too — Hirai's forced-flow values sit at or
      above the quiescent ones. Likely explanation: flow affects hydrate
      *shell thickness/growth*, not diffusion-through-a-fixed-shell
      directly, so this isn't a wholesale rejection of the film-diffusion
      picture, but it is a real limit on the simple constant-rate model.
- [x] **Found real residual scatter the regime split doesn't explain**:
      even excluding Brewer (geometry), the four remaining hydrate-coated
      sources span ~1.9×10⁻⁶ to 1.5×10⁻³ kg/m²/s — nearly three orders of
      magnitude among themselves. Hydrate-vs-not explains the broad
      picture; it doesn't collapse the hydrate bucket to one number. Full
      writeup: [analysis/phase_d_findings.md](analysis/phase_d_findings.md).

### Phase E — Reconciliation analysis ✅
- [x] Regime-classified the full dataset and compared raw (unclassified)
      scatter against within-bucket scatter directly:
      [analysis/phase_e_reconciliation.md](analysis/phase_e_reconciliation.md).
- [x] **Central test result**: raw scatter across the whole dataset is
      actually ~6 orders of magnitude (wider than the 2002 thesis's own
      "2–3 orders" characterization) — and part of that width is a units
      artifact (diameter-rate, mass flux, molar flux, and true k_L
      treated as the same kind of number). Once split into physically
      comparable buckets: non-hydrate gas bubbles collapse to **under one
      order of magnitude**, with a specific validated explanation
      (Phase C) for most of what's left; hydrate-coated retains a real
      **~2.9-order-of-magnitude residual** the regime split narrows but
      doesn't close; one bucket (non-hydrate liquid CO2) has too little
      usable data to assess.
- [x] Handled honestly: this is reported as a **partial** reconciliation,
      not a solved problem — see the write-up's closing section.

### Phase F — Write-up ✅
- [x] [analysis/findings.md](analysis/findings.md): standalone capstone
      summary — the question, method, dataset findings, before/after
      reconciliation numbers, direct answer to the central question, why
      it matters beyond this repo, and limitations, all in one place,
      citing the phase-by-phase detail rather than repeating it. Written
      plainly, repo-as-artifact style, per the scope decision logged in
      the parent project's PROJECT_THESIS.md — not aiming for publication
      polish at this stage.

## 7. Status

**All six phases (A–F) are done.** Capstone summary:
[analysis/findings.md](analysis/findings.md) — start there. Phase-by-phase
detail: `data/SOURCES.md` and `data/coefficients.csv` (Phase A),
`analysis/phase_b_findings.md` (rigid-sphere), `analysis/phase_c_findings.md`
(mobile-sphere — closes the Saito gap), `analysis/phase_d_findings.md`
(hydrate-coated harmonization), `analysis/phase_e_reconciliation.md` (the
full before/after picture).

**Headline result**: raw literature scatter is actually ~6 orders of
magnitude (wider than the 2002 thesis's own "2–3 orders" description,
partly because different physical quantities were being compared as the
same kind of number). Once correctly classified by disperse phase,
geometry, and hydrate state: non-hydrate gas bubbles collapse to under
one order of magnitude, with mobile-sphere theory closing most of a 3–6×
gap that rigid-sphere theory left open, for the one clean test case
available (Saito et al. 2000). Hydrate-coated measurements retain a real,
unresolved ~2.9-order-of-magnitude residual. One regime (very small,
low-Reynolds-number bubbles) sits outside where either analytical theory
was ever meant to apply. Reported throughout as a **partial**
reconciliation — a materially better answer than "the literature
disagrees and nobody knows why," not a claim of full resolution.

**Fully self-consistent mobile-sphere drag law: attempted, and it
revealed something more useful than a numeric refinement.**
`model/mobile_sphere.py` now implements Mei, Klausner & Lawrence's (1994)
clean-bubble drag law (verified via two independently-known analytic
limits before use), replacing the earlier conservative rigid-drag
stand-in. Applying it to Saito's conditions gives unphysical velocities
(up to 180 m/s) — not a bug, but the correct consequence of a formula
that assumes an undeformed sphere, checked directly via the Eötvös
number: **Saito's entire plausible bubble-size range (2–30 mm) sits in
the shape-deformed regime (Eo 0.5 to >100)**, not the spherical regime
either this study's rigid or mobile theory assumes. Cho & Choi's
micron-scale bubbles (Eo ~10⁻⁴) remain genuinely spherical; re-run with
proper mobile drag, their match shifts modestly (0.16×/0.75× vs. the
earlier 0.19×/0.92×), not resolving anything new there either. **The
earlier conservative comparison remains the one reported** — not because
it's rigorously correct, but because it avoids a worse, clearer error.
Full account: `analysis/phase_c_findings.md`'s addendum. A proper
treatment of Saito's regime would need ellipsoidal/spherical-cap drag and
mass-transfer theory (Clift, Grace & Weber 1978) — a real further
increment, now precisely scoped rather than vaguely deferred.

**That precisely-scoped increment was then pursued, and it produced the
strongest result in the whole study.** `model/deformed_bubble.py`
implements the two regimes Saito's bubbles actually occupy — ellipsoidal
(Mendelson, 1967) and spherical-cap (Davies & Taylor, 1950), both
verified against sources before use — dispatched by Eötvös number rather
than assuming a spherical bubble throughout. Result: **at 10 mm — a
thoroughly plausible size for the small-scale visualization experiment
Saito's coefficient came from — the predicted k_L matches the reported
2.0×10⁻⁴ m/s to within 1%**, and across the full 2–30 mm plausible range
the predictions bracket the reported value tightly (0.58×–2.36×),
against 3–6× low (rigid) or unphysical (idealized spherical-mobile)
in the earlier attempts. The terminal velocities themselves (0.21–0.29
m/s, roughly constant across the size range) also now match the
well-known experimental fact that mm-to-cm bubbles in water rise at a
roughly size-independent speed — something neither earlier model got
right either. Reading this honestly: it doesn't prove Saito's bubbles
were exactly 10 mm, and it reveals that "mobile vs. rigid interface" was
the wrong axis for this regime all along — shape, not surface
contamination state, is what governs bubble dynamics once bubbles
deform, since both ellipsoidal and cap bubbles circulate strongly
regardless of surface state. Cho & Choi's regime is unaffected (still
deeply spherical, Eo ~10⁻⁴, correctly falls back to the same spherical
treatment) and remains the framework's one clear unresolved stress case.
Full account: `analysis/phase_f_deformed_bubble.md`.

**Not pursued further, and not silently dropped**: primary full-text
verification of several 1990s sources (no journal access — a hard,
accepted limit, not a to-do); the non-hydrate liquid-CO2 bucket (Hirai
1996's own non-hydrate values), which never had enough consistent data to
assess; a fully rigorous Clift-Grace-Weber treatment (this phase used the
simpler, well-verified Mendelson/Davies-Taylor forms rather than the full
shape-regime machinery); Cho & Choi's low-Re/Pe regime, still unresolved
by any theory in this study. Any of these would be a reasonable next
increment if this study is picked up again.
