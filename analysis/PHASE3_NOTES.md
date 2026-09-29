> **Update**: the EOS phase-selection bug and the missing hydrate physics
> flagged below as "known rough edge" / "not reproduced" have since been
> addressed — see [method_a_vs_b.md](method_a_vs_b.md) for what changed
> (EOS stable-root fix, Method H hydrate compensation) and the Method A
> vs. B comparison this section originally called out as a next step. The
> qualitative checks below should be read as the *before* picture.
>
> **Second update**: the "≥95% dissolved above 500 m" gap flagged below
> as "not reproduced at that magnitude" is now largely closed, once
> shape-regime-aware rise velocity was integrated (real bubbles at this
> size rise slower than rigid-sphere theory predicted, so they spend more
> time dissolving) — the 300/500 m rows now run 97.1-100.0%, not
> 68-75%. Full account: [shape_regime_integration.md](shape_regime_integration.md).

# Phase 3 checkpoint — first working Python model

Status of the reimplementation in [../model/co2n2_bubble/](../model/co2n2_bubble/),
against [../model/EQUATIONS_SPEC.md](../model/EQUATIONS_SPEC.md). Read this
alongside that spec's §8 ("what this doesn't attempt") — the gaps here are
the ones already flagged there, not new surprises.

## Language decision (Phase 3, per PROJECT_THESIS.md §4.2)

**Python.** Once the equation spec was written out, the deciding factors
were: `gsw` (TEOS-10 seawater properties) and general scientific-Python
tooling are free and readily available, the Peng-Robinson EOS and
mass-transfer correlations are short enough to hand-code without needing
GAUSS's matrix/econometrics strengths, and a Python repo is easier for
anyone else to run without a license. GAUSS remains a fine option if a
future phase needs it for something GAUSS is actually better at — nothing
here forecloses that.

## What runs

`model/run_simulation.py` reproduces the original's input surface (depth,
CO2 fraction, bubble diameter) and its six-panel output plot layout. The
full original scenario matrix — 15/50/85/100% CO2 × 300/500/1000/1500 m,
1 cm initial bubble — runs to completion without errors for all 16
combinations. Demo output: [demo_500m_50pct.csv](demo_500m_50pct.csv) /
[demo_500m_50pct.png](demo_500m_50pct.png) (500 m, 50% CO2).

## Qualitative checks against the 2002 conclusions

The 2002 report's Chapter 6 makes a few qualitative claims independent of
exact numbers. Checked against this reimplementation:

- **"Low-purity bubbles accelerate as they rise (N2 expansion, decreasing
  bubble density)."** — **Reproduced.** E.g. 15% CO2 at 1000 m: rise
  velocity 0.53 → 1.13 m/s, diameter 1.0 → 4.6 cm over the run.
- **"Pure CO2 bubbles decelerate as they shrink."** — **Not reproduced.**
  In this model, pure CO2 at 1000 m also grows (1.0 → 6.25 cm) and
  accelerates, because decompression-driven expansion dominates over
  dissolution-driven shrinkage here. This is the expected consequence of a
  documented, deliberate scope cut (EQUATIONS_SPEC.md §6): hydrate-coating
  effects on pure CO2 bubbles were **not implemented** in this pass, and
  hydrate coating is exactly the mechanism the original relies on to slow
  and shrink pure CO2 bubbles at these depths (hydrate film reduces the
  mass-transfer rate enough that dissolution can outpace decompression).
  Without it, pure CO2 in this model behaves like just another
  low-solubility-limited gas — which is arguably a reasonable model of
  "pure CO2 if hydrate didn't form," but it isn't the original's scenario.
  **This is the clearest concrete next step**, not a bug: implement the
  hydrate-compensated mass-transfer branch (original Eqs. 4-11′–4-13,
  already speced in EQUATIONS_SPEC.md §6 as scoped-out) if the pure-CO2
  comparison case is going to be carried into the revised report.
- **"≥95% of injected CO2 dissolves before reaching the mixed layer for
  bubbles injected above 500 m."** — **Not reproduced at that magnitude.**
  This model shows roughly 68–75% dissolved across most compositions and
  depths, not ≥95%. This traces to the two [MODERNIZED] substitutions in
  EQUATIONS_SPEC.md §4/§6: the fugacity-corrected Weiss (1974) solubility
  model and the Hirai constant-rate (Method B) mass-transfer default are
  both defensible but not calibrated to reproduce the original's specific
  dissolution rate — they were never expected to be a numeric match (the
  spec says as much). Two concrete follow-ups, not mutually exclusive:
  1. Re-run with `--method A` (Sherwood-correlation mass transfer) and
     compare — Method A is the original's own "faster-dissolving" option
     per its Fig. 5-1 comparison, so it may close some of this gap on its
     own.
  2. Implement the full Duan & Sun (2003) CO2-brine solubility model in
     place of the Weiss/fugacity approximation, per the follow-up already
     flagged in EQUATIONS_SPEC.md §4.

## Known rough edge

100% CO2 at 500 m shows a discontinuous-looking jump (diameter to 6.7 cm,
only 36.7% dissolved, fewer timesteps than neighboring scenarios) — right
in the depth/composition region the original's own Chapter 2 flags as
phase-behavior-sensitive (hydrate zone boundary). Consistent with the
hydrate-physics gap above rather than a separate defect, but worth
re-checking once hydrate compensation is added.

## Bottom line

The rise-velocity mechanics, EOS-driven bubble expansion, and the
insoluble-N2 mixture-dilution behavior all work and match the original's
mixture-specific qualitative findings. The parts that don't match yet are
exactly the parts the spec already flagged as modernized substitutions or
deliberately scoped out (hydrate compensation, solubility model choice) —
not new problems. Recommended next Phase 3 work, in priority order: (1)
compare Method A vs. B directly, (2) decide whether hydrate compensation
is in scope for the revised report (it matters for the pure-CO2 comparator,
less for the CO2/N2 mixtures that are this report's actual subject), (3) if
pursued, implement Duan & Sun (2003) properly from the primary source.
