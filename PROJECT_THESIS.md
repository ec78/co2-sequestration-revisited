# Project: Revisiting "Ocean Sequestration of CO2/N2 Mixtures" (2002)

Living roadmap for updating Erica Clower's August 2002 Stanford M.S. report
(advisor: Dr. Franklin Orr, Dept. of Petroleum Engineering). Source document:
[02-thesis.pdf](02-thesis.pdf). Update this file as phases complete, decisions
get made, or the plan changes — it is the single source of truth for project
status, not a historical log.

## 1. What the original report did

- **Question**: Can direct ocean release of *impure* CO2/N2 gas mixtures
  (straight from flue gas, ~15% CO2, no separation step) compete
  economically with (a) separating and releasing pure liquid CO2, and (b)
  the Japanese "P-GLAD" gas-lift J-tube system (Saito et al., 2000/2001),
  which also avoids separation?
- **Method**: Built a numeric single-bubble transport/dissolution model
  (MATLAB, Appendix A) on top of prior pure-CO2 bubble models, using the
  `SEAWATER` MATLAB toolbox (Morgan, 1994) for seawater properties and a
  Peng-Robinson EOS for gas properties. Simulated 15/50/85/100% CO2 bubbles
  released at 300/500/1000/1500 m depth.
- **Key findings**:
  - N2 impurity suppresses hydrate formation, changing dissolution behavior;
    below the hydrate zone, impure bubbles dissolve *faster* than pure CO2.
  - Above ~500 m, ≥95% of injected CO2 dissolves before reaching the mixed
    layer regardless of starting purity — but the *absolute mass* of CO2
    delivered per bubble drops with increasing impurity.
  - Impure bubbles accelerate as they rise (insoluble N2 expands, bubble
    density drops); pure CO2 bubbles decelerate as they shrink.
  - Reported mass-transfer coefficients in the literature disagreed
    substantially — flagged as needing better correlations.
  - Estimated direct release of 15% CO2 at 1000 m: **$118/ton CO2**, vs.
    **$68/ton** for P-GLAD and **$126/ton** for direct release of liquefied
    pure CO2. Mixture release beats liquid release (skips liquefaction) but
    loses to P-GLAD (loses on compression/transport volume).

## 2. Why this needs more than a copy-edit

The literature search hasn't been run yet (Phase 1 below), but the framing
problem is already visible without one: **direct release of CO2 into the
ocean water column — the entire premise of this report — is not a live
option today the way it was in 2002.**

- The 2006/2007 amendments to the **London Protocol** (Annex 1) added CO2
  streams to the list of substances that may be considered for sub-seabed
  *geological* storage, but disposal into the water column itself is
  excluded/prohibited for most signatory states. This is a legal, not just
  technical, dead end for the P-GLAD-vs-mixture-release comparison as
  originally posed.
- Public and regulatory backlash killed pilot-scale ocean CO2 release
  experiments in the early-to-mid 2000s (e.g., a planned Hawaii open-ocean
  test was cancelled in 2002 amid protest — the same year this report was
  written). Field research in this specific direction largely stopped.
  **This needs verification** — flagged for the literature search, not
  stated here as confirmed fact.
- CCS research and deployment since then has overwhelmingly gone toward
  **sub-seabed / onshore geological storage** (saline aquifers, depleted
  reservoirs, EOR-linked storage — Sleipner, Snøhvit, Quest, and many more),
  not water-column disposal.
- A genuinely new, active field has emerged that touches the same ocean
  chemistry as this report but points the opposite direction: **ocean-based
  carbon dioxide removal (mCDR)** — ocean alkalinity enhancement,
  electrochemical ocean carbon capture, macroalgae sinking — pulling CO2
  *out* of seawater/atmosphere rather than injecting industrial flue gas
  *into* it. The 2022 U.S. National Academies report on ocean-based CDR is
  a likely landmark reference to check.
- Hydrate thermodynamics tooling has moved on (CSMHYD → CSMGem/newer tools),
  and CO2 solubility/mass-transfer correlations have continued to be
  refined since 1998–2001, which is the vintage of most of this report's
  citations.

None of this means the underlying fluid-mechanics/dissolution modeling is
worthless — it means the report's **framing** ("this is a viable near-term
disposal method, here's its cost") almost certainly needs to change to
something like a **retrospective/critical reassessment**: what this line of
research got right technically, why it was abandoned as policy, and what of
it is still relevant to adjacent fields (sub-seabed leak/blowout modeling,
mCDR bubble/gas transport, CO2 pipeline safety, etc.).

**This is the central open decision — see Section 4.** The roadmap below
is written so Phase 1 (literature search) produces the evidence needed to
make that call with the user, rather than assuming it up front.

## 3. Constraints

- No institutional affiliation → no paywalled journal access. Lean on
  open-access papers, preprints, IPCC/National Academies/DOE/NOAA public
  reports, and author-hosted PDFs.
- No lab, no field access, no proprietary data → **no new experimental
  data**. Model updates must be validated against data already published in
  the literature (digitizing published figures if needed) or left as
  purely computational refinements without new empirical validation.
- The original MATLAB `SEAWATER` toolbox and Peng-Robinson implementation
  are ~1990s/2002-vintage; availability and license status of `SEAWATER`
  specifically should be checked before assuming it can be reused as-is.

## 4. Decisions

1. **Framing of the updated report** — **settled: moderate reframe**
   (decided in Phase 2, after Phase 1 evidence — see Section 5a below for
   what this means concretely). Not a light-touch refresh (the legal/
   economic ground has genuinely shifted, so pretending otherwise would be
   wrong) and not a full pivot away from the original subject (the
   underlying physics — bubble transport, dissolution, hydrate formation —
   is still sound and still relevant work, worth keeping as the spine of
   the document).
2. **Implementation language** — **settled: Python** (decided in Phase 3).
   Original MATLAB (Appendix A) is kept in-repo for reference only, not
   executed. Deciding factor: free, high-quality open packages exist for
   exactly the pieces this model needs (`gsw` for TEOS-10 seawater
   properties in particular, confirming the Phase 1 finding that
   `SEAWATER` (Morgan 1994) is stale), and the EOS/mass-transfer math is
   compact enough that GAUSS's comparative strengths (matrix/econometric
   workloads) weren't decisive either way. GAUSS remains available if a
   later phase hits something it's genuinely better suited for.
3. **Deliverable format** — **repo-as-artifact first** (code + analysis +
   short written summaries, versioned in this repo), **then** a revised
   standalone report once the technical work has something to report on.
   Phase 5 ("Writing") comes after Phase 3/4 substance exists, not before.

## 5. Phased roadmap

### Phase 0 — Repo setup ✅ (this session)
- [x] Extract thesis text for reference/search (`pdftotext -layout`).
- [x] `CLAUDE.md` written.
- [x] `PROJECT_THESIS.md` (this file) written.

### Phase 1 — Literature search & landscape check ✅
Goal: verify/replace the claims in Section 2 with cited sources, and gather
what's needed to make the Section 4 framing decision.

**Done.** Findings, with sources, are in [LITERATURE_UPDATE.md](LITERATURE_UPDATE.md).
Headline results: the London Protocol ban on water-column CO2 disposal is
confirmed (in force since Feb 2007); the Hawaii/Norway field trial
cancellations are confirmed and happened the same year as this report;
field and P-GLAD-specific research both trail off by ~2005; geological CCS
is now cheaper in real terms than any of the three 2002 comparators even
before the legal point; the mass-transfer-coefficient uncertainty the 2002
report flagged is still an open problem today; `SEAWATER` (Morgan 1994) is
superseded by the GSW/TEOS-10 toolbox. Full detail and caveats (this was a
search-engine-based pass, not a systematic review — primary sources still
need direct reading before anything here is cited in a revised report) are
in that file.

Search threads to run:
- London Protocol / London Convention 1996 Protocol, 2006–2007 amendments
  on CO2 streams — current legal status of ocean water-column CO2 disposal.
- Status/history of early-2000s ocean CO2 release field trials (Hawaii
  test cancellation, MBARI/Brewer & Peltzer program, Japanese field work
  under Saito/Ohsumi) — what happened after 2002–2004.
- P-GLAD / gas-lift CO2 disposal system — any post-2001 follow-up work by
  Saito et al. or others.
- Current state of geological CCS deployment (representative large
  projects, current cost benchmarks per ton CO2 for capture/transport/
  storage) for an updated economic comparison.
- Ocean-based CDR (mCDR): National Academies 2022 report, IPCC AR6 WG3
  coverage, and recent (2023–2026) review articles — to decide if/how the
  report should gesture toward this adjacent field.
- CO2/N2 (and CO2 mixture) hydrate thermodynamics tooling and data since
  Sloan (1998)/CSMHYD — current standard tools and any updated phase
  diagrams for CO2/N2 mixtures specifically.
- CO2 bubble dissolution / mass-transfer coefficient literature since
  ~2000 (successors to Takemura & Yabe 1999, Mori & Mochizuki 1998) —
  whether the "large discrepancy between correlations" problem the report
  flagged has been resolved.
- Seawater property toolbox status: is `SEAWATER` (Morgan 1994, CSIRO)
  still maintained/available, or has it been superseded (e.g., GSW/TEOS-10)?

Deliverable: an annotated bibliography / updated literature summary
(new file, e.g. `LITERATURE_UPDATE.md`) plus a revisit of the Section 4
framing decision with the user.

### Phase 2 — Reframing decision ✅
- [x] Walked through Phase 1 findings; framing settled as **moderate
      reframe** (Section 4.1).
- [x] Concrete document outline for the moderate reframe: Section 5a below.
- [x] Repo-as-artifact structure proposed for Phase 3 to build into:
      Section 5b below.

#### 5a. Outline for the reframed document (target for Phase 5, scopes Phase 3/4)

Old chapter numbers in parentheses for reference. **Kept** = physics/methods
mostly still valid, update citations only. **Rewritten** = framing has to
change given Phase 1 findings. **New** = didn't exist in 2002.

1. **Introduction** (Ch. 1) — *Rewritten.* State up front, in the first
   page, that direct ocean water-column CO2 disposal has been prohibited
   under the London Protocol since 2007 and that field research in this
   area wound down around the same time this report was originally
   written. Frame the revisit's purpose explicitly: (a) the bubble
   transport/dissolution/hydrate modeling this report developed addresses
   problems — mass-transfer coefficient uncertainty especially — that are
   *still open* in the literature independent of the disposal application;
   (b) the report is also a useful case study in *why* a CCS research
   pathway got abandoned; (c) the same underlying gas-transfer physics is
   now relevant to a live adjacent field (mCDR).
2. **Chemistry of Ocean Sequestration** (Ch. 2) — *Kept*, citations
   refreshed. Hydrate/phase-behavior physics hasn't changed; update the
   CSMHYD reference and note the field has moved to CSMGem and newer
   CPA-EoS approaches (still imperfect per 2024 literature).
3. **Why This Research Direction Closed** — *New.* The regulatory timeline
   (London Protocol 2006/2007 amendment), the Hawaii/Norway field trial
   cancellations, the P-GLAD/GLAD program's own wind-down by ~2005, and
   the IPCC's own retreat from ocean storage between AR4 (2007) and AR6
   (2022). Largely a written-up version of LITERATURE_UPDATE.md §§1–3,
   with primary sources read directly rather than taken from search
   summaries.
4. **P-GLAD Model** (Ch. 3) and **Single Bubble Release** (Ch. 4) —
   *Kept* as the technical core, governing equations re-derived
   independent of MATLAB syntax (Phase 3), correlations updated where
   Phase 1 found newer literature (mass-transfer coefficient options,
   hydrate boundary predictions).
5. **Simulation Results and Discussion** (Ch. 5) — *Rewritten.*
   Reproduce the original 2002 scenario matrix as a regression check
   against the reimplemented model, then show results from the
   literature-updated correlations side by side so the delta from 2002
   is visible, not just a fresh run.
6. **Economic Comparison** (part of old Ch. 5) — *Rewritten.* Drop the
   framing of comparing three *disposal options against each other*
   (moot — none of them are legal or economically live anymore).
   Instead: inflation-adjust the original three figures as a historical
   reference point, and compare against current geological CCS cost
   benchmarks (Phase 1 §4) to make the "the field moved on, and here's
   the order of magnitude by which the ground shifted" point concretely.
7. **Where the Field Went Instead** — *New, short.* Geological CCS as
   the pathway that absorbed this research direction's goals; mCDR as
   the adjacent field where similar ocean-gas-transfer physics is being
   applied today, pointed the other direction. Not a full review of
   either — just enough to place this report's technical content on the
   current map.
8. **Conclusion** (Ch. 6) — *Rewritten.* What held up (bubble transport
   mechanics, hydrate suppression by N2, the mass-transfer uncertainty
   as a still-real problem), what didn't (the economic case, the premise
   that this is an implementable disposal method), and what the
   20-plus-year gap actually demonstrates about how a CCS research
   subfield can be closed off by policy/regulation rather than by being
   technically disproven.
9. **References** — merged original 2002 bibliography + new sources from
   LITERATURE_UPDATE.md, each checked against the primary source (not
   left as search-result citations).
10. **Appendix** — modernized model code (Phase 3 language decision);
    original MATLAB (Appendix A, 2002) kept verbatim alongside it for
    comparison/provenance, not deleted.

#### 5b. Proposed repo-as-artifact structure (to stand up at the start of Phase 3)

```
/original/         02-thesis.pdf, full.txt extract, original MATLAB code
                    (pulled out of the PDF appendix as its own file)
/literature/        LITERATURE_UPDATE.md and any follow-up notes per source
/model/              new Python and/or GAUSS implementation (Phase 3)
/analysis/           scripts/notebooks reproducing and extending Ch. 5
                      results, figures
/report/             eventual Phase 5 draft (not started until Phase 3/4
                      substance exists, per Section 4.3)
```

`original/`, `model/`, and `analysis/` now exist and are populated (Phase 3,
this session). `report/` is still not created — correctly, per Section 4.3,
it waits for Phase 3/4 substance to exist first.

### Phase 3 — Model modernization (computational, no new data) — 🔶 in progress
- [x] Re-derived the governing equations from Appendix A and Chapters 3–4
      into [model/EQUATIONS_SPEC.md](model/EQUATIONS_SPEC.md), independent
      of MATLAB syntax, with every equation tagged **[ORIGINAL]**,
      **[RECONSTRUCTED]** (OCR/appendix gaps, filled from standard forms of
      the cited methods), or **[MODERNIZED]** (deliberate literature-driven
      swap).
- [x] Language decision: Python (§4.2 above).
- [x] Repo-as-artifact structure stood up: `original/` (extracted thesis
      text + the original MATLAB driver, transcribed verbatim, not
      executed), `model/` (Python package `co2n2_bubble` + spec),
      `analysis/` (run outputs).
- [x] First working implementation: seawater properties (TEOS-10 via
      `gsw`), Peng-Robinson EOS for the bubble mixture, CO2 solubility
      (fugacity-corrected Weiss 1974, labeled as a modernized placeholder
      for Duan & Sun 2003), two mass-transfer methods (Hirai constant-rate
      "B", Sherwood-correlation "A"), and the rise-velocity ODE solver.
      Runs the full original 15/50/85/100% CO2 × 300/500/1000/1500 m
      scenario matrix without errors.
- [x] Behavioral check against the original's qualitative Ch. 6 claims —
      results and gaps in
      [analysis/PHASE3_NOTES.md](analysis/PHASE3_NOTES.md). Headline: the
      CO2/N2 mixture behavior (N2-expansion acceleration, monotonic CO2
      depletion) reproduces correctly; the pure-CO2 "decelerates and
      shrinks" claim does not, because hydrate-coating effects were
      deliberately scoped out (spec §6) and are what drives that specific
      behavior in the original; absolute dissolution percentages run
      lower than the original's ≥95% claim, attributable to the
      solubility/mass-transfer substitutions, not a defect.
- [x] **EOS phase-selection bug fix.** The first pass always picked the
      PR EOS's largest real root ("vapor"). Numerically checking the root
      structure across this model's own scenario matrix showed that's
      wrong for CO2-rich mixtures — pure CO2 at 500–1500 m has a single
      real root and it's the dense, liquid-like one (ρ ≈ 860–999 kg/m³),
      consistent with the original's own Chapter 2 claim about liquid CO2
      approaching seawater density near 1800 m. Fixed via a standard
      residual-Gibbs-energy stability criterion when multiple real roots
      exist. Correct and used unconditionally for the CO2/N2 mixture cases
      (no known mechanism keeps them from equilibrium once N2 suppresses
      hydrate formation, this report's own central finding).
- [x] **Hydrate compensation ("Method H") implemented**, gated to a
      documented placeholder "hydrate window" (depth ≥ 400 m, CO2 mole
      fraction ≥ 0.5 — standing in for the original's Fig. 2-5 phase
      diagram, not numerically recoverable from the PDF). Forces the
      bubble onto the vapor EOS root (hydrate shell as kinetic barrier to
      bulk liquefaction) and applies a Fujioka et al. (1994)
      diameter-shrinkage-rate-derived dissolution rate in place of
      Methods A/B while inside the window. Result: pure CO2 now shrinks
      and rises slowly while hydrate-coated, then transitions sharply once
      it exits the window — materially closer to the original's own
      qualitative description than the previous checkpoint.
- [x] **Method A vs. B compared systematically** across the full scenario
      matrix. Finding: Method A dissolves 100% of injected CO2 in every
      scenario, Method B gives the more graded ~35–92% range from before.
      This *direction* (A faster than B) is the original's own documented
      Fig. 5-1 finding, confirmed here, not a bug — but the 100%-every-time
      magnitude traces to Method A's dependence on the solubility module
      (`x_gs`), which is the modernized/approximate piece, while Method B
      doesn't use `x_gs` at all and is structurally more trustworthy right
      now. Full writeup: [analysis/method_a_vs_b.md](analysis/method_a_vs_b.md).
      **Method B remains the default** for anything feeding into Phase 4/5.
- [x] **Duan & Sun (2003) implemented as the default solubility model**
      (`model/co2n2_bubble/duan_sun.py`), superseding the Weiss (1974)
      approximation (kept only for comparison). The primary paper itself
      couldn't be read cleanly (every PDF found had a font-encoding fault
      corrupting negative-number characters); coefficients instead come
      from an independent open-source implementation, cross-validated
      digit-for-digit against numeric fragments recovered from a second,
      independent peer-reviewed source, plus a textbook reference-value
      check and a physical sanity check (salting-out direction). Caught
      and fixed a real bug in the process: Duan & Sun's own CO2
      mole-fraction shortcut assumes a pure CO2+H2O vapor phase, which
      would have silently mistreated this project's N2 as CO2 — fixed by
      feeding it this project's own CO2/N2 mixture fugacity instead. Full
      account: EQUATIONS_SPEC.md §4.
- [x] **Re-ran the Method A vs. B comparison** with Duan & Sun in place.
      Result: Duan & Sun gives 5–25% lower solubility than Weiss (the
      expected direction), but Method A still dissolves 100% of CO2 in
      every scenario — the earlier hypothesis that Weiss's extrapolation
      was the main driver was only half right. The real driver is the
      Sherwood-correlation coefficient itself at this bubble size,
      confirmed rather than merely suspected now. Updated:
      [analysis/method_a_vs_b.md](analysis/method_a_vs_b.md). Method B
      remains the default for anything downstream.
- [ ] **Still open, lower priority**: refining the hydrate-window boundary
      beyond the depth/composition threshold placeholder; an exact
      numeric regression against 2002 output isn't achievable at all
      regardless (helper-function source and the solubility figure's
      underlying data are both unrecoverable — see EQUATIONS_SPEC.md §8).

### Phase 4 — Economic re-analysis ✅
- [x] Inflation-adjusted the three 2002 figures using a sourced CPI-U
      multiplier (179.9 in 2002 → ≈331.7 now, ≈1.84×): mixture release
      $118→≈$217, P-GLAD $68→≈$125, liquid CO2 release $126→≈$232 (2026
      dollars).
- [x] Rebuilt the comparison against current CCS cost benchmarks,
      sourced by segment: capture (~$61–80/tonne modern NGCC per NETL,
      $40–240/tonne across GCCSI's broader historical dataset, DOE
      targeting <$40/tonne by 2025), transport (~$2/tonne favorable
      pipeline case per NETL, higher for shipping-based logistics),
      geological storage (~$10–80/tonne per NETL's 2024 saline storage
      model, geology-dependent), plus the 45Q credit ($85/tonne
      point-source+storage) as a policy-benchmark cross-check. All-in
      modern range: **≈$70–160/tonne**.
- [x] **Key finding**: the fairest comparison — 2002's liquid-CO2 full
      chain (≈$232/tonne, 2026 dollars, the only 2002 route that included
      capture cost) against today's full-chain CCS (≈$70–160/tonne) —
      shows a real, large improvement, driven mainly by capture costs
      falling over 24 years of deployment and RD&D, not by ocean-disposal
      engineering catching up. This independently weakens the 2002
      report's central economic bet (that avoiding capture cost via
      engineering cleverness was worth the tradeoffs), on top of the
      Phase 1 legal-prohibition finding. Full writeup, sourcing, and
      scope-mismatch caveats:
      [analysis/economic_reanalysis.md](analysis/economic_reanalysis.md).
- Did not pursue the "pivot to adjacent current problem" branch (Phase 2
  settled on the moderate reframe instead), so this phase stayed close to
  its original scope.

### Phase 5 — Writing ✅
- [x] Produced the full revised document per the Phase 2 outline (§5a):
      [report/revised_report.md](report/revised_report.md). All nine
      sections written — Introduction and Conclusion rewritten, a new
      "Why This Research Direction Closed" chapter added, Chemistry
      (Ch. 2) and the governing-physics chapter (Ch. 3–4) carried forward
      with refreshed citations and the Phase 3 findings woven in,
      Simulation Results and Economic Comparison rewritten around what
      Phases 3–4 actually found, and a new short "Where the Field Went
      Instead" chapter (geological CCS, mCDR) added.
- [x] Every claim in the document traces back to a source file already in
      this repo (LITERATURE_UPDATE.md, EQUATIONS_SPEC.md, the analysis/
      files) rather than being asserted fresh — the report is a synthesis
      of prior phases' work, not new research.

### Phase 6 — Repo polish (optional, low priority)
- Organize code/figures/data into a conventional structure once Phase 2
  settles the deliverable format.
- Add a README pointing newcomers at the final document vs. this working
  roadmap.

## 6. Status

**Phases 0 through 5 are all done.** The revised document —
[report/revised_report.md](report/revised_report.md) — is the
project's primary deliverable at this point: it synthesizes the Phase 1
literature findings, the Phase 3 model work, and the Phase 4 economic
analysis into the document outlined in §5a. Supporting detail lives in
[LITERATURE_UPDATE.md](LITERATURE_UPDATE.md),
[model/EQUATIONS_SPEC.md](model/EQUATIONS_SPEC.md), and the `analysis/`
directory, all cited from the report rather than duplicated into it.

One minor Phase 3 placeholder remains (the hydrate window's
depth/composition threshold is a documented approximation, not a
digitized phase diagram), noted in the report itself, not blocking.

**Phase 6 (repo polish)** remains unstarted — optional, low priority per
its own description.

**A new, standalone effort has since started**: a mechanistic
reconciliation study of the mass-transfer-coefficient discrepancy that
this project's own Phase 1 confirmed is still unresolved in the current
literature (the "Tier 2" option from post-Phase-5 discussion of where
this project could make a more current contribution). It lives in
[mass-transfer-study/](mass-transfer-study/), scoped as its own living
plan in
[mass-transfer-study/STUDY_PLAN.md](mass-transfer-study/STUDY_PLAN.md) —
deliberately kept separate from this roadmap since it's a new research
question, not a further revision of the 2002 report.

**Status: complete (all six phases).** Headline result — raw literature
scatter for CO2-seawater mass transfer is actually wider than the 2002
thesis's own "2–3 orders of magnitude" description once properly counted
(~6 orders), but most of that collapses once correctly classified by
physical regime: non-hydrate gas bubbles narrow to under one order of
magnitude, with mobile-sphere (not rigid-sphere) theory closing most of
the remaining gap for the one clean test case available. Hydrate-coated
measurements retain a real, unresolved residual. Reported as a partial,
not complete, reconciliation. Full capstone summary:
[mass-transfer-study/analysis/findings.md](mass-transfer-study/analysis/findings.md).

**P-GLAD reimplementation: done** — `model/pglad/` (own spec:
`model/pglad/PGLAD_SPEC.md`). Beggs & Brill (1973) substituted for the
original's chart-based Govier & Aziz (1972) friction correlation (same
modernization pattern as Duan & Sun replacing Weiss for the single-bubble
model), and a shooting-method solver reimplementing the original's own
stated method. **Honest result: does not reproduce the original's worked
example** (362.3 kg/s water flow rate) — the pressure mismatch is a
roughly flat ~3.5–4.6 bar (~4%) across a wide range of water flow rates,
not something a better root search would close. Independently
corroborated: the original's own Table 5-1 shows liquid flow increasing
~20% along the upriser in a way its stated equations can't explain,
implying Saito et al.'s actual model has water-entrainment/dissolution
coupling the 2002 thesis's simplified presentation doesn't specify. Full
account in `model/pglad/PGLAD_SPEC.md` §5.

**Hydrate-window refinement: done** —
`model/co2n2_bubble/hydrate_boundary.py`. Replaced the flat depth/
composition box with a composition-continuous, fugacity-threshold
criterion (hydrate forms when the mixture's CO2 fugacity meets pure
CO2's fugacity at its own equilibrium boundary, at the same
temperature), calibrated against two independently-sourced and
cross-checked CO2 hydrate quadruple points. Changes behavior at exactly
one point in the original scenario matrix (500 m/50% CO2, now correctly
excluded from the hydrate window) with no practical effect on that run's
outcome; the pure-CO2 hydrate-compensated demo shifts modestly (62.4% →
61.5% dissolved). Honest open item carried forward: the mixture
extension isn't independently validated against real CO2/N2 hydrate
data, and shows a real, reported discrepancy against the original
thesis's own qualitative statement about pure CO2 at 500 m depth. Full
account: `analysis/hydrate_boundary_refinement.md`.

**Report sync: done.** `report/revised_report.md` had drifted out of
date after the above work — it still said P-GLAD "was not rebuilt for
this revision" and made no mention of the mass-transfer study. Updated:
Section 4.1 now describes the P-GLAD reimplementation and its honest
non-match finding; Section 4.2's hydrate-window paragraph now describes
the fugacity-threshold boundary instead of the old flat box; the
mass-transfer study is now cited from the front matter, the Conclusion,
and the Appendix. All new links checked against the actual files.

Other options discussed but not started: deeper treatment of any single
report section (geological CCS or mCDR in real depth), a different
deliverable format for the report (PDF/LaTeX, given the original was
submitted as one).
