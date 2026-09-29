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

### Phase 6 — Repo polish (optional, low priority) ✅
- [x] Code/figures/data were already organized into a conventional
      structure as Phases 3/4 built it out (the repo-as-artifact layout
      settled in Phase 2, §5b above) — no further reorganization needed.
- [x] Added [README.md](README.md): points a newcomer at
      `report/revised_report.md` as the finished deliverable vs. this
      file as the working roadmap, gives a directory map, and states the
      no-new-data/no-fabricated-citations constraints up front.
- [x] Added an interactive companion dashboard, **Bubble Ascent Lab**
      (https://claude.ai/artifact/NgkgWj6FXAknZCoZAJDtna): an adjustable
      bubble-release simulator across the original scenario matrix, plus
      the shape-regime, mass-transfer-reconciliation, and economics
      findings as charts. Data generated by
      `model/generate_dashboard_data.py` from this repo's own validated
      model — not hand-entered.

## 6. Status

*(Reorganized as a current-state summary for session handoff, not a
chronological log — that's what git history is for. If you're picking
this project up fresh, read this section, then the specific spec/analysis
file for whatever you're about to touch, per the pointers below.)*

### 6.1 Thesis revisit — complete

All six phases done. Primary deliverable:
[report/revised_report.md](report/revised_report.md), which synthesizes
everything below rather than duplicating it.

- **Phase 1 (literature)**: London Protocol has banned water-column CO2
  disposal since Feb 2007; field trials (Hawaii/Norway) and P-GLAD-
  specific research both wound down by ~2005; geological CCS is now
  cheaper in real terms than any 2002 comparator. Detail:
  [LITERATURE_UPDATE.md](LITERATURE_UPDATE.md).
- **Phase 2 (framing)**: settled as a moderate reframe (§4.1, §5a above)
  — keep the physics, rewrite why the application doesn't hold up.
- **Phase 3 (single-bubble model)**: Python reimplementation in
  `model/co2n2_bubble/` (spec: `model/EQUATIONS_SPEC.md`). Fixed a real
  EOS phase-selection bug; implemented hydrate-coated bubble physics
  ("Method H"); implemented Duan & Sun (2003) solubility, replacing an
  approximate placeholder; confirmed the original's own Method A > Method
  B dissolution-speed finding. Detail: `analysis/PHASE3_NOTES.md`,
  `analysis/method_a_vs_b.md`.
- **Phase 4 (economics)**: inflation-adjusted 2002 figures vs. current,
  segment-sourced CCS costs. Key finding: modern full-chain CCS
  (~$70–160/ton) is substantially cheaper than the 2002 liquid-CO2 route
  in real terms (~$232/ton), mainly because capture costs fell, not
  because ocean-disposal engineering caught up. Detail:
  `analysis/economic_reanalysis.md`.
- **Phase 5 (writing)**: `report/revised_report.md` written, all claims
  traced to source files rather than asserted fresh.
- **Post-Phase-5 open items — all resolved**:
  - *P-GLAD reimplementation* (`model/pglad/`, spec: `PGLAD_SPEC.md`):
    Beggs & Brill (1973) substituted for the original's inaccessible
    chart-based friction correlation. **Honest result: does not
    reproduce the original's own worked example** (362.3 kg/s) — a
    corroborated finding (the original's own Table 5-1 implies missing
    water-entrainment physics its stated equations don't specify), not a
    bug to chase further.
  - *Hydrate-window refinement* (`model/co2n2_bubble/hydrate_boundary.py`):
    replaced a flat depth/composition box with a fugacity-threshold
    criterion calibrated against two sourced CO2 hydrate quadruple
    points. One open calibration question against real CO2/N2 mixture
    data, reported not hidden. Detail:
    `analysis/hydrate_boundary_refinement.md`.
  - *Report sync*: `revised_report.md` updated to match both of the above
    plus the mass-transfer study (§6.2) — it had drifted out of date
    before this sync.
  - *Shape-regime integration* (`model/co2n2_bubble/shape_regime.py`):
    the mass-transfer study's (§6.2) strongest result — this model's own
    ~1 cm bubbles sit in the shape-deformed regime, not the spherical
    regime rigid-sphere theory assumes — fed back into the main model's
    rise velocity and Method A mass transfer. Not a minor correction:
    Method B's dissolved fraction across the full scenario matrix rose
    from a 35–92% spread to a tight **87–100%** band, now closely
    matching (rather than falling well short of) the original's own
    "≥95% dissolved above 500 m" claim. Required sourcing a new,
    literature-grounded but temperature-extrapolated surface-tension
    parameter the original model never needed (honestly flagged, not the
    integration's strongest piece). Full account:
    `analysis/shape_regime_integration.md`; design decisions:
    `EQUATIONS_SPEC.md` §5b.
- **Phase 6 (repo polish)**: done — [README.md](README.md) added.

### 6.2 Mass-transfer-coefficient study — complete through its hydrate-film-growth follow-up

Standalone effort, not a further revision of the 2002 report — lives in
[mass-transfer-study/](mass-transfer-study/) with its own living plan,
[mass-transfer-study/STUDY_PLAN.md](mass-transfer-study/STUDY_PLAN.md).
Capstone summary: `mass-transfer-study/analysis/findings.md`.

Core finding: raw literature scatter for CO2-seawater mass transfer is
actually ~6 orders of magnitude (wider than the 2002 thesis's own "2–3
orders" description), but classifying correctly by physical regime
resolves most of it for gas bubbles specifically. The strongest result:
once bubble *shape* (ellipsoidal/spherical-cap, not just surface
mobility) is modeled correctly — `mass-transfer-study/model/deformed_bubble.py`,
Mendelson 1967 / Davies & Taylor 1950, both independently verified before
use — a real reported coefficient (Saito et al. 2000) matches to within
1% at a physically plausible bubble size, with no fitting. Hydrate-coated
measurements retain a real, unresolved ~2.9-order-of-magnitude residual;
Cho & Choi's micro-bubble regime remains outside where any theory in this
study gives dependable answers. Reported throughout as a **partial**
reconciliation, not a solved problem.

This ellipsoidal/spherical-cap result has since been fed back into the
main thesis model itself (§6.1's "Shape-regime integration" bullet,
`model/co2n2_bubble/shape_regime.py`) — no longer just a standalone
finding sitting alongside the thesis revisit, but wired into it.

**The hydrate-coated residual's flow-dependence — pursued as a deep-dive
(Phase G), done as a partial, honestly-reported result.** Five new
sources retrieved (a water-tunnel study directly measuring hydrate-coated
CO2-drop mass transfer vs. flow velocity; a hydrate-shell compositional-
instability/collapse mechanism; a 2021 paper complicating the original
heat-transfer-based working hypothesis for the fast initial film-
formation phase specifically, while leaving heat transfer's role in the
*later-stage* growth this project's Method H actually models an open
question; two bubble-geometry film-growth studies, both run at zero
flow). The most standard, directly-implementable candidate mechanism —
external boundary-layer resistance in series with Method H's existing
shell resistance, reusing this project's own validated Sherwood-
correlation machinery rather than any new unverified physics — was
implemented and quantitatively tested (`mass-transfer-study/model/series_resistance.py`)
and found insufficient: it predicts at most ~1.2–1.4× enhancement from
flow, well short of the literature's observed ~1.2–6× (or up to
~3-orders-of-magnitude across the full hydrate-coated bucket). A real,
useful negative result, not a non-result — it rules out one plausible
mechanism with a number rather than a guess, and narrows (without
resolving) what's actually going on. `mass_transfer.py`'s Method H is
**deliberately left unchanged** in the main model — a partial mechanism
isn't a sound basis for a quantitative correction. Full account:
`mass-transfer-study/analysis/phase_g_series_resistance.md`.

### 6.3 Next planned work

Both threads originally queued from the mass-transfer study are now
done — shape-regime integration (§6.1) and the hydrate-coated residual
deep-dive (§6.2, above), the latter a partial/negative result honestly
reported rather than a closed gap. Nothing is currently queued; see §6.4
for lower-priority options discussed but not agreed to pursue next.

### 6.4 Other options discussed but not queued

Lower priority or explicitly deferred: deeper treatment of geological
CCS or mCDR in the report's Section 7; a PDF/LaTeX version of the report
(the original was submitted as one); the non-hydrate liquid-CO2 bucket
(Hirai 1996's own values — too little consistent data to assess); a full
Clift-Grace-Weber shape-regime treatment (the simpler, verified Mendelson/
Davies-Taylor forms were used instead); primary full-text verification of
several 1990s sources (no journal access — a hard, accepted limit, not a
to-do).
