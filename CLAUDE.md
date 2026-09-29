# CLAUDE.md

Guidance for Claude Code (or any assistant) working in this repository.

## What this repo is

A revisit of Eric Clower's August 2002 M.S. report, *"Ocean Sequestration of
CO2/N2 Mixtures"*, submitted to the Department of Petroleum Engineering at
Stanford University (advisor: Dr. Franklin Orr). The original document is
[02-thesis.pdf](02-thesis.pdf) — the only file in the repo at the outset of
this project.

The goal is to bring the 2002 work up to date: refresh the literature,
re-evaluate the science and economics against ~20+ years of subsequent
research and policy change, and (likely) rebuild the numeric model that
originally shipped as MATLAB code in Appendix A of the report.

The full roadmap, phased plan, and open decisions live in
[PROJECT_THESIS.md](PROJECT_THESIS.md). **Read that file before picking up
work here** — it is the living plan and should be kept current as phases
complete or the approach changes.

## Hard constraint: no new experimental data

The author is no longer affiliated with a research institution and has no
access to the lab, field equipment, or data-collection capability that
produced the original 2002 results (in-situ ocean bubble releases,
MBARI-style field experiments, etc.). This means:

- Do not propose work plans that assume new experiments or proprietary data
  access.
- Any model revalidation must use **published data** (papers, public DOE/NOAA
  reports, digitized figures from open-access literature) or purely
  computational updates (better EOS, updated correlations, translated/
  modernized code).
- Flag clearly, anywhere in the roadmap or writing, when a claim would
  ideally be checked against experimental data that isn't accessible.

## Working with the source PDF

`pdftotext` (poppler, via the mingw64/git-bash toolchain) is available in
this environment and works well on this file:

```
pdftotext -layout 02-thesis.pdf <output>.txt
```

Use `-layout` to preserve table/equation spacing reasonably well. Equations
rendered as images or with special symbols will extract poorly — treat
extracted equation text as a rough guide and verify against a rendered page
view when precision matters. `pdftoppm` (page-to-image rendering) is **not**
installed in this environment, so page-image review isn't currently
available via the Read tool's PDF path — extracted text is the primary way
to work with the document for now.

## Literature and citations

- This is an academic document. Do not fabricate citations, page numbers, or
  quoted findings. Any new source must be one actually retrieved (via
  WebSearch/WebFetch or provided by the user), not recalled from memory
  alone — model knowledge is a starting point for search terms, not a
  citable source.
- Prefer open-access sources (journal open-access articles, preprints,
  IPCC/National Academies/DOE/NOAA reports, government and IGO publications)
  given the author has no institutional journal access.
- Note the field-defining regulatory fact up front: the 2006/2007 amendments
  to the London Protocol effectively prohibit direct disposal of CO2 into the
  ocean water column (as opposed to sub-seabed geological storage). This is
  central to how the original thesis topic should be reframed — see
  PROJECT_THESIS.md.

## Conventions for this repo

- Keep the original PDF untouched; do all derivative work (extracted text,
  notes, new drafts, code) as new files alongside it.
- Prefer plain Markdown for planning/roadmap docs. Don't create additional
  top-level planning documents beyond `PROJECT_THESIS.md` and
  `LITERATURE_UPDATE.md` — update those in place rather than scattering
  status across new files.

## Repo layout

- `original/` — the source PDF, a full text extraction of it, and the
  original MATLAB driver script from Appendix A, transcribed verbatim.
  Nothing here is executed; it's provenance/reference only (no MATLAB
  access).
- `model/` — the Python reimplementation. Two independent subpackages,
  each modeling a genuinely different physical system from the original
  report: `co2n2_bubble/` (the single-bubble dissolution model, Chapter 4;
  spec: `EQUATIONS_SPEC.md`) and `pglad/` (the gas-lift J-tube, Chapter 3;
  spec: `pglad/PGLAD_SPEC.md` — note this one honestly does *not*
  reproduce the original's own worked-example numbers, with a specific
  reason why documented in that spec's §5). Read the relevant spec before
  touching either package's code — both tag every equation as original,
  reconstructed (from incomplete OCR/missing source), or deliberately
  modernized, and that framing should stay in sync with the code.
  `co2n2_bubble/shape_regime.py` is where `mass-transfer-study/`'s
  shape-deformed-bubble result was fed back into this model (see below
  and `EQUATIONS_SPEC.md` §5b) — the two directories aren't fully
  independent of each other despite the standalone framing.
- `analysis/` — run outputs and write-ups checking model behavior against
  the 2002 report's claims (`PHASE3_NOTES.md`, `method_a_vs_b.md`) and the
  economic re-analysis (`economic_reanalysis.md`).
- `report/` — `revised_report.md`, the synthesized deliverable (Phase 5).
  It cites the other three directories rather than duplicating their
  content — when updating any finding, fix it at the source (literature
  note, equations spec, or analysis file) and then update the report's
  reference to it, not the other way around.
- `mass-transfer-study/` — a separate, standalone research effort (not a
  further revision of the 2002 report): a literature reconciliation of
  the mass-transfer-coefficient discrepancy this project's own literature
  search found still-unresolved. Complete through its shape-regime
  follow-up (`model/deformed_bubble.py` — ellipsoidal/spherical-cap
  bubble theory, its strongest result), which has since been fed back
  into the main thesis model itself (`model/co2n2_bubble/shape_regime.py`,
  `analysis/shape_regime_integration.md`) — no longer just a standalone
  finding. Own living plan and status:
  `mass-transfer-study/STUDY_PLAN.md`; capstone result:
  `mass-transfer-study/analysis/findings.md`. Also complete through a
  follow-up hydrate-film-growth deep-dive (`model/series_resistance.py`,
  `analysis/phase_g_series_resistance.md`) — a partial, honestly-reported
  negative result (rules out one candidate flow-dependence mechanism
  quantitatively, doesn't close the ~2.9-order-of-magnitude hydrate-coated
  residual). Nothing further is currently queued — see `PROJECT_THESIS.md`
  §6.3/§6.4. Same no-new-data constraint applies here as everywhere else
  in this repo.
