# Governing Equations — CO2/N2 Single Bubble Release Model

Re-derived from Chapter 4 and Appendix A of the original 2002 report
([../original/thesis_full_text.txt](../original/thesis_full_text.txt),
[../original/appendix_a_original.m](../original/appendix_a_original.m)),
independent of MATLAB syntax, per Phase 3 of
[../PROJECT_THESIS.md](../PROJECT_THESIS.md). This is the spec the Python
reimplementation in this directory follows.

Every equation below is tagged:
- **[ORIGINAL]** — equation/correlation as given in the 2002 text, used
  as-is.
- **[RECONSTRUCTED]** — the 2002 text described it but the PDF's equation
  OCR was unreliable (Greek letters, subscripts, and symbols routinely
  dropped) or the referenced helper function's source wasn't included in
  the appendix; reconstructed here from the surrounding prose, the main
  driver script's usage of the value, and the standard form of the cited
  method (Wilke-Chang, Frössling/rigid-sphere Sherwood correlations,
  etc.). Flagged explicitly wherever this involved a judgment call.
- **[MODERNIZED]** — deliberately swapped for a current standard, per the
  Phase 1 literature findings and the "no new experimental data" constraint
  (see PROJECT_THESIS.md §3) — usually because the 2002 source was a
  toolbox/dataset that's since been superseded and re-digitizing the 2002
  original isn't possible without the original data.

## 1. State and scope

Single bubble, released at depth `D0` with initial diameter `Db0` and CO2
mole fraction `CO2Z0` (balance N2). Tracked over time until it either
reaches the surface (`depth <= 0`) or fully dissolves (`Db <= 0`):
depth, diameter, rise velocity, CO2 mole fraction, bubble density, seawater
density, mass of CO2 dissolved.

Scope limitation carried over from the original: **spherical bubble,
negligible deformation** (justified in the text via Weber-number argument,
Yabe et al. 1999), and **N2 assumed insoluble** (its seawater solubility is
orders of magnitude below CO2's) — all dissolution is CO2 leaving the
bubble.

## 2. Seawater properties

### 2.1 Temperature vs. depth — **[ORIGINAL]**

```
T(z) = 3946 / (z + 112) + 273.6        [K, z in meters]
```
(Eq. 4-6, attributed to Ohmura and Mori 1998.)

### 2.2 Pressure and density — **[MODERNIZED]**

Original used Morgan's `SEAWATER` MATLAB toolbox (1994, UNESCO EOS-80
formulation) at latitude 36.75°N (Monterey Bay). Per Phase 1,
`SEAWATER` is superseded by the **GSW/TEOS-10** toolbox (the current
international standard, 2010). This implementation uses the `gsw` Python
package (TEOS-10 reference implementation) for:
- `gsw.p_from_z(z, lat)` → sea pressure [dbar] from depth
- `gsw.rho(SA, CT, p)` → in-situ seawater density [kg/m³]

Practical note: EOS-80 vs. TEOS-10 density differ at the ~0.01–0.1 kg/m³
level for typical ocean water — immaterial at this model's precision, so
this substitution is not expected to change results in any way that
matters, and it removes a dependency on an unmaintained toolbox.

Reference salinity `SA = 35.0 g/kg` (open-ocean typical value; the 2002
report doesn't state its assumed salinity — this is a documented
assumption, not a recovered original value) and conservative temperature
`CT` derived from §2.1's `T(z)` are used as `gsw.rho` inputs.

## 3. Bubble (gas mixture) density — Peng-Robinson EOS — **[ORIGINAL
   method, RECONSTRUCTED mixing rule]**

Original calls a `flashb` routine (not included in the appendix — no
source recovered) with critical properties:

```
Tc = [304.2, 126.2] K       (CO2, N2)
Pc = [72.8,  33.5]  bar     (CO2, N2)
R  = 83.1451                (cm^3 bar / mol K)
```

These are standard literature critical constants for CO2 and N2 and are
used unchanged. The mixture is treated as a single phase (no coexisting
vapor+liquid split within one bubble) rather than a full VLE flash:

```
P = RT/(V-b) - aα(T) / [V(V+b) + b(V-b)]
```
with van der Waals one-fluid mixing rules and **[RECONSTRUCTED, documented
assumption]** binary interaction parameter `k_ij = 0` (not stated in the
2002 text; literature values for the CO2–N2 pair are typically small,
roughly -0.02 to 0 — this is a clearly-labeled, tunable parameter in the
code, not a recovered original value).

**Phase-root selection — fixed after the first Phase 3 pass.** The first
implementation always took the largest real root of the cubic (the
"vapor" branch). Checking the root structure numerically across this
model's own 300–1500 m scenario matrix showed that's wrong for CO2-rich
mixtures: at 300 m the cubic has three real roots (vapor/unstable/liquid)
and the correct *thermodynamically stable* one has to be picked by
minimizing residual Gibbs energy, not by taking the largest Z; at 500 m
and below, pure CO2 has only **one** real root at all, and it's the dense,
liquid-like one (ρ ≈ 860–999 kg/m³, consistent with the original's own
Chapter 2 claim that liquid CO2 density approaches seawater density near
1800 m). `eos.py`'s `mixture_density` now selects the stable root
correctly (`_select_stable_root`); `BubbleState.phase` reports which
branch was used.

**This is correct for equilibrium thermodynamics, and it's the right
choice for the CO2/N2 mixture cases that are this report's actual
subject** — N2 content suppresses hydrate formation (the report's own
central finding), and without a hydrate shell there's no known mechanism
to keep the mixture from equilibrating to its true stable phase.

**It is very likely *not* what the original model assumed for the
pure-CO2 comparator**, though. The original's own Chapter 2 discussion
implies pure CO2 below ~400–500 m forms a *hydrate skin* while still
gaseous in the interior — a kinetically metastable state, not the
equilibrium liquid phase, because the hydrate crust is a diffusion barrier
that can keep the core from ever reaching bulk liquid equilibrium on the
timescale of a bubble's rise. Mori & Mochizuki (1998) and the other
pure-CO2 models this report builds on treat the bubble as staying
gas/rigid-sphere-like throughout, consistent with that metastable picture,
not with letting it flash to equilibrium liquid. **Practical
consequence**: the equilibrium-phase EOS fix above is correct for the
mixture cases (used unconditionally), but reproducing the original's
pure-CO2 "decelerates and shrinks" behavior needs the hydrate-affected
pathway (§6, hydrate compensation) to be modeled as a **forced-vapor,
kinetically-trapped state** rather than letting it flash to the
equilibrium liquid root. This is now the concrete link between this
section's fix and the still-open hydrate-compensation item — see §6.

## 4. CO2 solubility in seawater, `x_gs` — **[MODERNIZED]**

Original: interpolated by hand from a digitized experimental dataset (Mori
and Mochizuki, 1998) shown as Figure 4-3 in the report — no closed-form
equation, and the underlying digitized data points aren't recoverable from
the PDF (a figure, not a table).

Since re-digitizing that specific figure isn't possible without the
original data (PROJECT_THESIS.md §3 constraint) and Phase 1 didn't surface
a public re-hosted version of it, this implementation uses the
**Duan & Sun (2003)** CO2-brine solubility model as the default
(`duan_sun.py`), with an earlier fugacity-corrected Weiss (1974)
Henry's-law approximation kept in `solubility.py` as
`solubility_mass_fraction_weiss` for comparison only.

**Provenance of the Duan & Sun coefficients**: no clean full-text copy of
the primary 2003 paper could be retrieved — every PDF found had a
font-encoding fault that specifically corrupted negative-number
characters (several coefficients came through as bare `(` where a
minus sign should have been). The ~25 coefficients used here come from an
independent open-source implementation (CO2REAKT,
github.com/mcrossover97/CO2REAKT, `solvers/DuanSun2003.py`, LGPL v2.1),
cross-validated against the numeric fragments that *did* survive
extraction from a second, independent peer-reviewed source (a Petroleum
Science paper reproducing the same coefficient tables) — every digit that
survived that second extraction matched the GitHub source exactly,
including several cases where the PDF's own table layout was too garbled
to tell which coefficient belonged to which parameter without the
independent confirmation. Implementation additionally validated against
a textbook reference point (CO2 solubility in pure water at 25°C/1 atm:
this implementation gives 0.0329 mol/kg against a commonly cited
~0.033–0.034 mol/kg) and checked for the correct qualitative salting-out
direction (solubility decreases monotonically with increasing NaCl
molality, confirmed numerically). Treated as trustworthy on that basis,
not as a verbatim primary-source transcription — flagged accordingly
rather than presented as equivalent to reading the paper directly.

**A real bug caught during wiring this in, worth recording**: Duan &
Sun's own formula for CO2's vapor-phase mole fraction (`y_CO2 =
(P-P_H2O)/P`) assumes the vapor phase is *only* CO2 + water vapor — it
would wrongly treat this project's N2 as if it were more CO2. Fixed by
splitting `duan_sun.py` so the aqueous-equilibrium relation (the
mu0/lambda/xi terms, which only care about CO2's fugacity, not what else
is in the vapor phase) takes fugacity as an input, and feeding it this
project's own CO2/N2 mixture fugacity from `eos.py` (which correctly
accounts for N2 dilution) instead of Duan & Sun's pure-system shortcut.
The pure-CO2-system version is kept as `co2_molality_pure_system` for
the validation checks above, where it's the physically correct thing to
use.

Seawater is approximated as an equivalent NaCl molality derived from bulk
salinity (`solubility.py`'s `seawater_nacl_equivalent_molality`, S=35 →
≈0.62 mol/kg) — Duan & Sun support NaCl explicitly, and this project
doesn't track other seawater ions anywhere else either, so this isn't a
new simplification relative to the rest of the model.

**What actually changed as a result** (see
[analysis/method_a_vs_b.md](../analysis/method_a_vs_b.md) for the full
before/after): Duan & Sun gives modestly **lower** solubility than the
Weiss approximation across this model's scenario matrix (roughly 5–25%
lower, growing with depth/pressure) — the expected direction, since Weiss
was a linear extrapolation and real solubility saturates. But that
reduction turned out **not** to be enough to change Method A's
100%-dissolved-in-every-scenario result from the previous checkpoint.
That's a genuine, useful negative result: Method A's speed relative to
Method B is a robust property of the Sherwood-correlation mass-transfer
approach itself at these bubble sizes, not an artifact of the (now
properly validated) solubility model.

## 5. Bubble rise velocity — **[ORIGINAL]**

Force balance on a rigid sphere (Eq. 4-1/4-2), discretized in time
(Eq. 4-4) and solved implicitly each step via a guessed-velocity /
Reynolds-number / drag-coefficient iteration, exactly as in the original
driver script:

```
ψ = ρ_sea / (ρ_bub + 0.5 ρ_sea)
γ = ρ_bub / ρ_sea

Re = U * Db * ρ_sea / μ_sea
Cd(Re) = (24/Re)(1 + 0.173 Re^0.657) + 0.413 / (1 + 16300 Re^-1.09)   [Eq. 4-3]

(3/4) ψ (Cd/Db) Δt · U_{n+1}^2 + U_{n+1} - [U_n + Δt ψ(1-γ)(9.81)] = 0   [Eq. 4-4]
```

solved as a quadratic in `U_{n+1}` each step (positive root), iterated
against `Re` until `|Re_guess - Re_calc| < 1` — reproduced verbatim from
the MATLAB loop structure.

`μ_sea` (seawater viscosity) — **[RECONSTRUCTED]**: the original calls
`Find_Vissea(T)`, source not included in the appendix. Implemented here via
a standard seawater dynamic-viscosity correlation (temperature- and
salinity-dependent); flagged as an assumption, not a recovered original
formula.

## 5b. Shape-regime-aware rise velocity and mass transfer — **[MODERNIZED]**

Integrates [../mass-transfer-study/](../mass-transfer-study/)'s strongest
result (its own `model/deformed_bubble.py`, verified against a real
literature coefficient to within 1% —
[../mass-transfer-study/analysis/phase_f_deformed_bubble.md](../mass-transfer-study/analysis/phase_f_deformed_bubble.md))
back into this model. §5's rigid-sphere force balance assumes an
undeformed sphere throughout (justified in the original text by a
Weber-number argument, §1 above); the mass-transfer study found that this
model's own ~1 cm bubble sizes actually sit in the shape-*deformed*
regime (Eötvös number 0.5 to >100 across that study's own Saito et al.
2000 comparison), not the spherical regime §5 assumes. This section
brings that regime awareness into the transient simulation
(`bubble_model.solve_rise_velocity_shape_aware`, `mass_transfer.py`'s
`method_a_kL`), rather than leaving it as a separate, disconnected
finding.

**Eötvös number and regime thresholds**: `Eo = g|ρ_sea - ρ_bub|Db²/σ`,
dispatched at `Eo < 0.5` (spherical), `0.5 ≤ Eo < 40` (ellipsoidal),
`Eo ≥ 40` (spherical cap) — the same Clift-Grace-Weber (1978) thresholds
`mass-transfer-study/model/deformed_bubble.py` uses, not independently
re-derived (`model/co2n2_bubble/shape_regime.py`).

**Ellipsoidal regime**: Mendelson's (1967) wave-analogy terminal velocity,
`U = sqrt(2σ/(ρ_sea·Db) + g·Db/2)`. **Spherical-cap regime**: Davies &
Taylor's (1950) result, `U = (2/3)sqrt(g·Db/2)`. Both formulas are used
as-is from the mass-transfer study, which independently verified each
against a source reproducing it directly before use — not re-verified
again here, since nothing about porting them into this model's own loop
changes the formulas themselves.

**Design decision — quasi-steady dispatch, numerically verified.**
Mendelson's and Davies & Taylor's formulas are algebraic terminal-velocity
results; there is no transient force-balance ODE version of them the way
§5's `U_{n+1}` quadratic is for the rigid sphere. This implementation
therefore treats rise velocity as quasi-steady at each timestep: at every
step, the regime is re-evaluated from the *current* diameter/density, and
if ellipsoidal or cap, `U_{n+1}` is simply the regime's terminal-velocity
formula rather than an integrated quantity carried from `U_n`. This is
only valid if velocity actually equilibrates much faster than the
timestep — checked directly, not assumed: sub-stepping the existing
rigid-sphere ODE from rest (`U=0`) at representative mid-scenario-matrix
conditions (1 cm bubble, 1000 m, 50% CO2) reaches within 1% of its own
terminal velocity in **~0.13 s** — over 15× faster than this model's own
`Δt = 2 s` timestep, and 3-4 orders of magnitude faster than a typical
full simulated rise (hundreds to ~1800 s in this model's own demo runs,
`analysis/demo_*.csv`). The rigid-sphere case is, if anything, the
*slower*-relaxing of the regimes checked here (a bare force balance, no
analog of the deformed regimes' near-instantaneous wave/potential-flow
response), so this is a conservative check, not a best-case one.

**Design decision — hydrate-coated bubbles are excluded from this
dispatch, regardless of Eötvös number.** A hydrate shell (§6's Method H)
is a rigid, solid interface — the physical opposite of the deformable,
responsive fluid interface both Mendelson's and Davies & Taylor's
derivations require. So whenever `mass_transfer.in_hydrate_window` is
active, the bubble keeps §5's original rigid-sphere ODE unconditionally,
even if its Eötvös number (computed from whatever forced-vapor density
Method H uses) would otherwise indicate a deformed regime. Rigid-sphere
theory is, if anything, *more* physically appropriate for a hydrate-coated
bubble than anywhere else in this model, not less — this is a
strengthening of the rigid-sphere assumption's scope, not a compromise.

**Surface tension, σ — new to this revision.** §§1-6 never needed a
surface-tension parameter before (rigid-sphere theory throughout); this
integration's Eötvös number does. `mass-transfer-study/model/mobile_sphere.py`
used a flat placeholder (`σ = 0.074 N/m`, pure-water-like) for the same
purpose. This implementation instead sources a pressure-dependent
treatment (`seawater.interfacial_tension_N_m`), since pressure is exactly
what varies across this model's own 300–1500 m scenario matrix and the
literature is unambiguous that CO2-water interfacial tension is strongly
pressure-dependent. Two retrieved sources: Hebach et al. (2002, *J. Chem.
Eng. Data*), measuring CO2-water IFT dropping from ~72 mN/m near
atmospheric pressure to ~30 mN/m by 12-20 MPa; Chalbaud et al. (2009,
*Energy Procedia*/*Adv. Water Resour.*), reporting the same high-pressure
plateau (~30 mN/m at 308 K) and finding brine salinity's effect on it
negligible (supporting reuse of a seawater-salinity-independent CO2-water
value here rather than a separate brine correlation). The implementation
is a smooth two-parameter exponential interpolation between a
near-atmospheric endpoint (0.074 N/m) and the high-pressure plateau
(0.030 N/m, decay scale 40 bar, chosen to match the qualitative shape both
sources report) — **not** a digitized reproduction of either source's
primary data (inaccessible, same constraint as everywhere else in this
project) and **not** fit at this model's own ocean temperatures. Both
cited studies validate their correlations over 293–398 K; this model's own
Eq. 4-6 gives 276–283 K across the scenario matrix, colder than either
study's range — flagged honestly as an extrapolation, most likely biasing
this model's Eötvös numbers slightly high (surface tension tends to rise
as temperature falls, and a lower assumed σ inflates Eo), not corrected
further without new low-temperature CO2-water IFT data this project
doesn't have access to. Full reasoning: `seawater.py`'s
`interfacial_tension_N_m` docstring.

**Effect on mass transfer (Method A only)**: `mass_transfer.method_a_kL`
now takes a `regime` argument. In the spherical regime (including
hydrate-active steps), it is unchanged — §6's rigid-sphere Sherwood
correlation. In the ellipsoidal/cap regimes, it uses the same Levich
penetration-theory `k_L` the mass-transfer study validated
(`shape_regime.deformed_kL`, reusing this model's own diffusivity
correlation), with the already-regime-correct velocity substituted in.
**Deliberately does not** fall back to a mobile-but-still-spherical
treatment for the spherical case the way
`mass-transfer-study/model/deformed_bubble.py`'s own spherical branch
does (that module reuses `mobile_sphere.py`'s clean-bubble drag even for
Eo < 0.5, for consistency with its own architecture) — this model's
default is deliberately the rigid/contaminated regime, since real
seawater is rarely perfectly clean
([../mass-transfer-study/STUDY_PLAN.md](../mass-transfer-study/STUDY_PLAN.md)
§3.2), so mobile-type theory is reserved here for cases with an
independent, shape-driven reason to circulate strongly, not used as a
general substitute for rigid-sphere theory. Methods B and H are unaffected
in their own rate formulas (neither depends on velocity or shape), but
their simulated *trajectories* still shift under this section, because
rise velocity changes how long the bubble spends at each depth — see
`analysis/shape_regime_integration.md` for the resulting numbers.

## 6. Mass transfer — two methods, both from the original — **[ORIGINAL,
   with RECONSTRUCTED sub-pieces noted]**

Governing mass balance (Eq. 4-5):
```
-d/dt [ (π/6) Db^3 ρ_g ] = π Db^2 · D · ρ_w · x_gs
```

**Method A** (Mori & Mochizuki-style correlation) — Sherwood-number-based:
```
Sh = D·Db / D_gw
Sh = 1 + 0.425 Re^0.55 Sc^(1/3)        (Re ≤ 2×10^3)     [Eq. 4-7]
Sh = 1 + 0.724 Re^0.48 Sc^(1/3)        (100 ≤ Re, Re > 2×10^3)  [Eq. 4-8]
Sc = μ_w / (ρ_w D_gw)                                      [Eq. 4-9]
```
with `D_gw` (CO2-in-water molecular diffusivity) from a Hayduk-Laudie-type
correlation (Eq. 4-10). **[RECONSTRUCTED]**: the OCR'd form of Eq. 4-10 is
not fully trustworthy (garbled exponents/subscripts); implemented here
using the standard published Hayduk & Laudie (1974) diffusivity
correlation rather than the possibly-corrupted transcription. Documented
in code with a citation so it can be checked against the original text
directly if a cleaner scan ever becomes available.

**As of this revision, the Sherwood correlation above is used only in the
spherical regime.** §5b (below the rise-velocity section) adds
shape-regime awareness: in the ellipsoidal/spherical-cap regimes this
model's own bubble sizes mostly occupy, `method_a_kL` uses a different,
independently-validated `k_L` formula instead — see §5b for the full
account. Not just a numerical refinement: at representative mid-column
conditions (1000 m, 50% CO2, ellipsoidal regime), Method A's flux
advantage over Method B grew from the ~20× `method_a_vs_b.md` originally
reported to **~141×**, per `analysis/shape_regime_integration.md`.

**Method B** (Hirai et al. 1996 constant rate, non-hydrate case):
```
dn_CO2/dt = 1.25e-4 [kg/m²/s] × (π Db²) × (1000/44.01) × X_CO2   [Eq. 4-11]
```
i.e. Hirai's reported constant mass flux, times bubble surface area,
converted from kg/s to mol/s, scaled by current CO2 mole fraction (the
2002 model's own stated assumption that the mass-transfer coefficient
scales linearly with CO2 content for mixed bubbles — not Hirai's own
assumption). **[RECONSTRUCTED]**: the `π` in the surface-area term was
dropped by OCR but is recovered here from the sphere-surface-area identity
`4πr² = π Db²`, consistent with all other surface-area uses in the report.

Both methods are implemented, matching the original's own comparison
(§4.3.3.2 / Fig. 5-1) of Method A vs. Method B dissolution predictions.
**Method B is used as the default** for the scenario runs — it's fully
specified without reconstruction uncertainty; Method A carries more
reconstruction risk in `D_gw` and is offered as a secondary/comparison
option, clearly labeled.

*Hydrate compensation* (Eqs. 4-11′–4-13, for pure CO2 below ~500–1000 m in
the original) — **implemented in this revision as "Method H."** The whole
premise of this project (Phase 1/2) is that N2 content suppresses hydrate
formation across the CO2/N2 mixture compositions that are this report's
actual subject, so hydrate correction only matters for the pure/near-pure
CO2 comparator. But §3's EOS phase-selection fix made clear *why* it
matters there: without it, pure CO2 either equilibrates to bulk liquid
(if the stable-root EOS is used) or free-dissolves as an uncoated gas
bubble (if forced to stay vapor) — neither reproduces the original's
"hydrate-coated gas core, slow diffusion-limited dissolution" picture.

Method H models exactly that: for CO2 fractions/depths in the hydrate
window (per Ch. 2's phase diagram — roughly CO2 content high enough and
depth ≳ 400–500 m at typical ocean temperatures), the bubble is (a) kept
on the **forced-vapor** EOS root rather than letting it equilibrate to
the liquid root — physically justified by the hydrate shell acting as a
kinetic barrier to bulk liquefaction on the timescale of a bubble's rise
— and (b) given the constant diameter-shrinkage rate reported by Fujioka
et al. (1994) for hydrate-coated bubbles (5.0×10⁻⁷ m/s), converted to a
mass/molar loss rate.

**[RECONSTRUCTED, deliberately re-derived rather than transcribed]**: the
OCR'd algebra in Eqs. 4-12/4-13 (rearranging Eq. 4-5 for `D` given an
imposed `dDb/dt`) isn't trustworthy enough to use verbatim — dropped
symbols leave real ambiguity in the constants. Rather than guess at the
OCR'd form, this implementation re-derives the equivalent mass rate
directly from Eq. 4-5 itself (which *is* unambiguous) by differentiating
its left-hand side at fixed `ρ_g`:
```
mass_rate = -(π/2) ρ_g Db² (dDb/dt)          [kg/s, dDb/dt < 0]
```
using Fujioka's reported `dDb/dt = -5.0×10⁻⁷ m/s`, then converting to
mol CO2/s the same way Methods A/B do. This is mathematically consistent
with Eq. 4-5 as stated in this document (§6 above) even though it isn't
guaranteed to match whatever constant actually survived the original's
own (possibly-different) algebra in 4-12/4-13 — flagged explicitly rather
than presented as a recovered original formula. Outside the hydrate
window (low CO2 fraction, or above the hydrate-formation depth), the
bubble uses the ordinary stable-root EOS and Methods A/B exactly as
before — Method H only overrides behavior *inside* the window it's meant
for.

**The hydrate-window boundary — updated, no longer the original box
placeholder.** The original's Fig. 2-5 (CSMHYD-predicted hydrate
formation pressure vs. CO2/N2 composition and temperature) still isn't
numerically recoverable from the PDF (a figure, not a table), so a full
digitized reproduction of it remains out of reach. But the first-pass
placeholder (a fixed depth ≥ 400 m *and* CO2 mole fraction ≥ 0.5 box, no
temperature or pressure sensitivity at all) has been replaced by a
composition-continuous, physically-motivated criterion: hydrate forms
when the mixture's CO2 fugacity (computed via this project's own EOS,
eos.py — the same one already used everywhere else in this file) meets
or exceeds pure CO2's fugacity at its own equilibrium hydrate-formation
pressure at the same temperature. Diluting with N2 lowers CO2's fugacity
at fixed total pressure, so a mixture needs a higher pressure or colder
temperature than pure CO2 to cross that threshold — the same qualitative
behavior Fig. 2-5 describes, reached by a different, independently
sourced route (the pure-CO2 boundary curve is a two-point fit through the
CO2 hydrate system's two quadruple points, both independently retrieved
and cross-checked during this revision). Full derivation, sourcing, and
an honestly-reported calibration discrepancy against the original's own
qualitative statement about pure CO2 at 500 m: `hydrate_boundary.py`'s
module docstring. The old box remains available as
`hydrate_boundary.legacy_box_hydrate_window` for comparison, not deleted.

## 7. Per-step update procedure — **[ORIGINAL, algorithmic]**

Each timestep (`Δt = 2 s`, matching the original):
1. Compute seawater T, P, ρ at current depth (§2).
2. Flash/EOS the current bubble composition to get `ρ_bub` (§3).
3. Get `x_gs` at current P (§4).
4. Solve for `U_{n+1}` (§5).
5. Update depth: `depth_{n+1} = depth_n - U_{n+1}·Δt`.
6. Compute CO2 mass transferred out this step (§6); update moles of CO2 in
   bubble (N2 moles unchanged — insoluble); recompute mole fractions.
7. Re-flash the new composition at the new depth's T, P to get new bubble
   volume → new diameter (`Find_NewBubDiameter`).
8. Track cumulative CO2 mass lost and percent of original CO2 mass lost,
   for the dissolution-vs-depth plots the original produces.

Loop terminates when `depth <= 0` (bubble reached surface) or `Db <= 0`
(bubble fully dissolved).

## 8. What this spec deliberately does not attempt

- Reproducing exact 2002 numeric output. The lost helper-function source
  (§§3–5's `Find_Vissea`, `flashb` internals) and the lost solubility
  figure data (§4) mean an exact regression against 2002 numbers isn't
  achievable — only a **behavioral** check (does it reproduce the
  qualitative conclusions: impure bubbles accelerate while rising, pure
  bubbles decelerate, near-total dissolution above 500 m, etc.) is
  possible with what survives in the PDF.
- The P-GLAD/J-tube model (Chapter 3) — reimplemented separately in
  `pglad/` (its own spec: `pglad/PGLAD_SPEC.md`), since it's a genuinely
  different physical system (two-phase pipe flow, not a single rising
  bubble) from everything else in this file. Honest result: it does not
  reproduce the original's own worked-example water flow rate (362.3
  kg/s), with a specific, independently-corroborated reason why (the
  original's own Table 5-1 shows liquid flow increasing ~20% along the
  upriser in a way its stated equations don't explain — see
  `pglad/PGLAD_SPEC.md` §5 for the full account).
- Hydrate-coated bubble behavior — **implemented**, not scoped out (see
  §6 above, "Method H"). This note is left here only to flag that an
  earlier draft of this document said otherwise; §6 is the current,
  correct account.
