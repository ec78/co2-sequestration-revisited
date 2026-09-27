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

The hydrate-window boundary itself is **[RECONSTRUCTED, approximate]**:
the original's Fig. 2-5 (CSMHYD-predicted hydrate formation pressure vs.
CO2/N2 composition and temperature) isn't numerically recoverable from
the PDF (a figure, not a table), so this implementation uses a simple
documented threshold (depth ≥ 400 m *and* CO2 mole fraction ≥ 0.5) as a
placeholder for that phase boundary, not a digitized reproduction of it.
Flagged clearly in code; refining this against a real CO2/N2 hydrate
model (e.g. re-running CSMHYD-equivalent predictions, per the Phase 1
finding that CSMGem and newer CPA-EoS models have superseded CSMHYD) is a
further follow-up, not resolved here.

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
- The P-GLAD/J-tube model (Chapter 3) — out of scope for this pass; the
  single-bubble model is the technical core carried forward per the Phase
  2 outline (§5a item 4 in PROJECT_THESIS.md).
- Hydrate-coated bubble behavior (§6 above) — scoped out for the same
  reason P-GLAD is: not needed for the CO2/N2 mixture cases that are this
  report's actual contribution.
