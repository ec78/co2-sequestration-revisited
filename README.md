# Ocean Sequestration of CO2/N2 Mixtures, Revisited

A 2026 revisit of Erica Clower's August 2002 M.S. report to Stanford's
Department of Petroleum Engineering (advisor: Dr. Franklin Orr),
[02-thesis.pdf](02-thesis.pdf) — the only file that existed here at the
start of this project.

**Start here**: [report/revised_report.md](report/revised_report.md) is
the finished deliverable — a synthesized, updated document that keeps the
original's bubble-transport/dissolution physics as its technical core
while rewriting why the original disposal application no longer holds up
(the 2006/2007 London Protocol amendments effectively banned it) and
bringing the literature, model, and economics up to date.

Everything else in this repo is the working history and evidence behind
that document — model code, run outputs, literature notes — kept because
the report cites it rather than duplicating it. If you want to see *how*
a specific claim in the report was reached, or pick up further work,
[PROJECT_THESIS.md](PROJECT_THESIS.md) is the living roadmap: what was
done, in what order, and why, organized as a current-state summary
(§6) rather than a chronological log.

## Repo layout

```
02-thesis.pdf          the original 2002 report (untouched; all derivative
                        work lives alongside it, never edits it)
LITERATURE_UPDATE.md    2020s literature findings that motivated the revisit
PROJECT_THESIS.md       living roadmap / current-state summary (read this
                        before picking up further work)

original/               the source PDF's text extraction and the original
                        MATLAB driver (Appendix A), transcribed verbatim,
                        reference-only -- nothing here is executed
model/                  Python reimplementation: co2n2_bubble/ (Chapter 4
                        single-bubble dissolution model) and pglad/
                        (Chapter 3 gas-lift J-tube); EQUATIONS_SPEC.md
                        documents every equation as original/reconstructed/
                        modernized relative to the 2002 source
analysis/               run outputs and write-ups checking the model
                        against the 2002 report's own claims, plus the
                        economic re-analysis
report/                 revised_report.md -- the deliverable described above

mass-transfer-study/    a standalone follow-on effort: reconciling why
                        reported CO2-seawater mass-transfer coefficients
                        disagree by orders of magnitude in the literature.
                        Own living plan: mass-transfer-study/STUDY_PLAN.md.
                        Its strongest result (bubble shape, not just
                        surface contamination, governs transfer at this
                        project's bubble sizes) was fed back into
                        model/co2n2_bubble/ -- the two directories aren't
                        fully independent despite the standalone framing.
```

## Running the model

```
pip install -r model/requirements.txt
python model/run_simulation.py --depth 1000 --co2-fraction 0.5 \
    --diameter-cm 1 --method B --plot out.png
```

`model/co2n2_bubble/` has no test suite; correctness is checked by
comparing simulation output against the 2002 report's own qualitative
claims (`analysis/PHASE3_NOTES.md` and friends) rather than by unit tests,
since there's no ground-truth numeric output to test against (see
`model/EQUATIONS_SPEC.md` §8 for exactly what is and isn't recoverable
from the original).

## Working constraints, for anyone picking this up

- **No new experimental data anywhere in this repo.** The author has no
  lab, field, or institutional access; every model update or claim is
  checked against already-published sources or left as a purely
  computational refinement. Flagged explicitly wherever a claim would
  ideally need data that isn't accessible.
- **No fabricated citations.** Every source cited was actually retrieved
  (search/fetch or user-provided), not recalled from model knowledge
  alone.
- Full detail on both, plus conventions for working in this repo, is in
  [CLAUDE.md](CLAUDE.md) (written for an AI assistant, but the substance
  applies to anyone continuing this work).
