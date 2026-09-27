# Phase B — Rigid/Contaminated-Sphere Model: Findings

Per [../STUDY_PLAN.md](../STUDY_PLAN.md) §3.1/§6 Phase B. Model:
[../model/rigid_sphere.py](../model/rigid_sphere.py), reusing this
project's existing `model/co2n2_bubble` package rather than re-deriving
the same physics.

## Which data points this actually tests

Per the gas-vs-liquid finding added to
[../data/SOURCES.md](../data/SOURCES.md) while starting this phase, only
**two** entries in the compiled dataset are genuine gas bubbles suitable
for testing gas-bubble rigid-sphere theory: **Saito et al. (2000)**
(cm-scale, P-GLAD gas-lift context, ~300 m) and **Cho & Choi (2019)**
(10–30 μm industrial micro-bubbles). Everything else in the dataset is
either liquid CO2 (not a gas bubble at all) or excluded on geometry
grounds (Brewer 2000).

Neither source reports the exact bubble diameter used to derive its
mass-transfer coefficient, so the honest comparison is a **predicted
range** across plausible diameters (via `predict_over_diameter_range`,
which solves a genuine terminal-velocity fixed point at each candidate
size — see `rigid_sphere.py`), not a single fabricated-precision number.

## Saito et al. (2000)

Conditions: 300 m depth (T≈283.2 K, P≈31.3 bar, seawater from this
project's existing `seawater.py`), ~95% CO2 / 5% N2 (P-GLAD injection
purity). Swept diameters 2–30 mm — a reasonable span for the small-scale
bubble-visualization experiments the coefficient was derived from.

| Db | U (terminal) | Re | Predicted k_L |
|---|---|---|---|
| 2 mm | 0.19 m/s | 297 | 6.1×10⁻⁵ m/s |
| 5 mm | 0.38 m/s | 1504 | 5.9×10⁻⁵ m/s |
| 10 mm | 0.56 m/s | 4395 | 5.0×10⁻⁵ m/s |
| 15 mm | 0.67 m/s | 7879 | 4.4×10⁻⁵ m/s |
| 20 mm | 0.75 m/s | 11862 | 4.1×10⁻⁵ m/s |
| 30 mm | 0.90 m/s | 21209 | 3.6×10⁻⁵ m/s |

**Reported value: 2.0×10⁻⁴ m/s.** The rigid-sphere prediction across this
entire plausible size range (3.6–6.1×10⁻⁵ m/s) is **3–6× lower** than
what Saito et al. actually report. Rigid-sphere theory does not explain
this data point — the reported transfer is consistently faster than a
contaminated sphere should allow.

## Cho & Choi (2019)

Conditions: pure CO2 micro-bubbles in seawater (paper states "sea
water" explicitly), T assumed 293.15 K (20°C) — **a flagged assumption**:
this is a lab/industrial contactor study, not an open-ocean measurement,
so this project's ocean depth-temperature correlation (calibrated to a
Monterey Bay profile) doesn't apply; 20°C is a reasonable but unconfirmed
stand-in for typical lab conditions.

| Case | Db | P | Re | Predicted k_L | Reported | Ratio (reported/predicted) |
|---|---|---|---|---|---|---|
| No mixer | 30 μm | 4 bar | 0.015 | 7.5×10⁻⁵ m/s | 3.6×10⁻⁵ m/s | 0.48× |
| With mixer | 10 μm | 3 bar | 0.0006 | 1.75×10⁻⁴ m/s | 9.97×10⁻⁵ m/s | 0.57× |

Here the rigid-sphere prediction is **roughly 2× too high**, the
**opposite** direction from the Saito comparison.

## Reading these honestly — not forcing a match

Both comparisons disagree with rigid-sphere theory, in opposite
directions, and for what look like different reasons — worth stating
plainly rather than either claiming false agreement or treating both as
equally "the theory is wrong":

- **Saito (moderate-to-high Re, 300–21000)**: transfer is *faster* than
  rigid-sphere theory allows. The natural next check (Phase C) is whether
  the mobile/clean-interface theory — which predicts *higher* transfer
  than the rigid case at the same Re, by construction — closes this gap.
  If it does, that's a real, interpretable finding: Saito's small-scale
  visualization bubbles may not have been as contaminated as assumed, or
  the P-GLAD gas-lift flow field itself may add turbulent enhancement a
  free-rise model doesn't capture.
- **Cho & Choi (Re ≈ 0.0006–0.015, deep creeping flow)**: transfer is
  *slower* than rigid-sphere theory predicts. This is more likely a
  **correlation-validity problem than a physics disagreement**: the
  specific Sherwood correlation this project's Method A implements
  (`Sh = 1 + 0.425 Re^0.55 Sc^(1/3)`) is a moderate-Reynolds-number
  engineering fit; extrapolating it down to Re ≈ 0.001–0.02 — three to
  four orders of magnitude below where it's normally applied — is not a
  safe use of that correlation, and the mismatch may say more about the
  correlation's range of validity than about whether rigid-sphere
  *physics* holds at micro-bubble scale. Worth flagging for Phase C too:
  Levich's mobile-sphere result technically wants high Péclet number
  (Pe = Re·Sc) for its boundary-layer approximation to hold, and at
  Sc ≈ 900–1000 for CO2 in water, Pe here works out to only ≈0.6–15 —
  marginal, not comfortably in Levich's own valid range either.

## What this means for Phase C and beyond

- Phase C (mobile/clean-sphere, Levich/Higbie) should check directly
  whether it closes the Saito gap — that's now a specific, falsifiable
  sub-question, not a vague "let's see."
- Cho & Choi sits in a Reynolds/Péclet regime this study's two
  candidate theories weren't built for. Rather than force a comparison
  that neither theory is calibrated to make, Phase E's write-up should
  present it as a **stress test that both theories fail at low Re/Pe**,
  which is itself useful — it marks where the reconciliation framework's
  boundaries are, rather than papering over a bad fit.
- The rigid-sphere model implementation itself (`rigid_sphere.py`) is
  validated as *internally consistent* with this project's main bubble
  model (the terminal-velocity sanity check landed within 4% of a
  comparable run in the main model — see commit history) — the
  discrepancies above are about the correlation's applicability, not a
  bug in this reimplementation.
