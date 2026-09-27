# Phase 4 — Economic Re-Analysis

Per [PROJECT_THESIS.md](../PROJECT_THESIS.md) Phase 4: inflation-adjust
the 2002 cost figures as a historical reference point, then compare
against **current** CCS cost benchmarks — since the original's actual
comparators (P-GLAD, direct liquid CO2 release) aren't legal or economic
alternatives today (Phase 1 finding), geological storage is the relevant
comparison now. This is a search-engine-assisted pass against public
DOE/NETL and industry sources, not a commissioned cost study — ranges and
caveats are called out throughout; treat as directionally reliable, verify
specific numbers against primary sources before citing in anything more
formal than this repo.

## 1. The original 2002 figures, inflation-adjusted

From the original report (Table 5-3, §5.3.2 — full breakdown in
[../original/thesis_full_text.txt](../original/thesis_full_text.txt)):

| Route | 2002 $/ton CO2 | What's included |
|---|---|---|
| Direct release, 15% CO2 mixture (1000 m) | $118 | Compression + transport + sequestration. **No capture/separation, no liquefaction** — the whole point of the mixture-release idea was to skip these. |
| P-GLAD (95% CO2, 300 m) | $68 | Compression + transport + sequestration. **No capture/separation, no liquefaction** — skipped via the gas-lift shallow-injection design instead. |
| Direct release, liquid CO2 | $126 | Capture/separation + liquefaction + compression + transport + sequestration — the **full chain**, the standard alternative the report was arguing against. |

**Inflation adjustment**: CPI-U annual average was 179.9 in 2002; the most
recent available figure is ~331.7, giving a multiplier of **≈1.84×**
([in2013dollars.com](https://www.in2013dollars.com/us-cpi), cross-checked
against the BLS-published 2002 annual average of 179.9). Applied to the
three figures:

| Route | 2002 $/ton | ≈2026 $/ton (real) |
|---|---|---|
| Mixture release | $118 | **≈$217** |
| P-GLAD | $68 | **≈$125** |
| Liquid CO2 release (full chain) | $126 | **≈$232** |

These are reference points only — not adjusted for anything except
general price inflation (no adjustment for energy price changes,
technology-specific cost deflation, regulatory changes, etc.).

## 2. Current CCS cost benchmarks, by segment

### Capture
- NETL's most recent cost-and-performance baseline: **≈$61–80/tonne**
  for 90% capture at an F-class natural-gas combined-cycle (NGCC) plant,
  down from ≈$80/tonne in the prior baseline revision — DOE/NETL,
  reported via [Carbon Herald](https://carbonherald.com/netl-updates-key-report-for-carbon-capture-costs-and-performance/)
  and [NETL's own updated baseline reports](https://netl.doe.gov/NETLVol1BaselineTool).
- Global CCS Institute's 2025 capture-cost-trends report shows a much
  wider historical range across coal and gas studies/plants — roughly
  **$40–240/tonne** — reflecting technology vintage, plant type, and
  whether a project is a mature FEED estimate or an early concept study.
  Newer operational natural-gas projects (e.g. Glacier Entropy) cluster
  toward the lower end of that range.
  ([GCCSI, *Advancements in CCS Technologies and Costs*, 2025](https://www.globalccsinstitute.com/wp-content/uploads/2025/08/Advancements-in-CCS-Technologies-and-Costs-Report-2.pdf))
- DOE's stated program target: capture cost **<$40/tonne by 2025, <$30/tonne
  by 2035** ([Belfer Center](https://www.belfercenter.org/publication/carbon-capture-utilization-and-storage-technologies-and-costs-us-context), cited in Phase 1).

### Transport
- Highly distance- and volume-dependent (strong economies of scale).
  NETL's own reference case gives a first-year break-even transport
  (+storage, combined) cost as low as **≈$2/tonne** for a favorable
  large-pipeline scenario — not representative of small or remote
  projects, but illustrative of how cheap transport gets at scale.
- Long-distance/shipping-based transport (relevant for a non-pipeline-
  connected source) runs considerably higher once liquefaction,
  intermediate storage, and shipping are included — GCCSI's 2025 shipping
  cost-component analysis shows these adding up substantially over
  distance, though not reduced to one clean $/tonne headline figure in
  the source.

### Storage (saline geological)
- NETL's 2024 saline-storage cost model briefing shows **levelized
  storage costs of roughly $10–80/tonne (2023$)**, split sharply by
  formation quality: favorable geology (e.g. the Mount Simon formation)
  toward the low end, poor geology (e.g. Rose Run) toward the high end.
  Significant national storage capacity is available below $10/tonne at
  favorable sites.
  ([NETL, *CO2 Saline Storage: Costs and Storage Capacity*, June 2024](https://www.netl.doe.gov/projects/files/CO2SalineStorageCostsandStorageCapacity_051524.pdf))
- Consistent with Phase 1's earlier, less-detailed finding of a
  **$7–50/tonne** range, base case ≈$20–22.5/tonne
  ([Thunder Said Energy](https://thundersaidenergy.com/downloads/co2-disposal-in-geologic-formations-the-economics/), Phase 1).

### Policy benchmark (not a cost, but informative)
- US 45Q tax credit, current through 2026: **$85/tonne** for point-source
  capture + dedicated geologic storage, **$180/tonne** for direct air
  capture + storage — preserved and left at these levels by the 2025
  "One Big Beautiful Bill Act."
  ([Global CCS Institute](https://www.globalccsinstitute.com/u-s-preserves-and-increases-45q-credit-in-one-big-beautiful-bill-act/);
  [Beancount.io summary](https://beancount.io/blog/2026/05/10/section-45q-carbon-capture-credit-industrial-direct-air-capture-85-180-per-ton-obbba-monetize-sequestration-guide))
  The point-source rate is a rough proxy for what the US considers the
  break-even point worth subsidizing for conventional CCS today.

### All-in estimate
Stacking a representative modern case — capture (~$61–80) + transport
(~$2, favorable case, or higher for less favorable logistics) + storage
(~$10–80, geology-dependent) — gives an **all-in range of roughly
$70–160/tonne** for a well-sited, modern point-source CCS project, with
real projects landing anywhere in a considerably wider band depending on
source type, distance, and storage geology.

## 3. The comparison

| | 2002 nominal | 2002 in ≈2026 dollars | Current (2026) |
|---|---|---|---|
| Mixture release (no capture) | $118 | ≈$217 | *(not a legal option — Phase 1)* |
| P-GLAD (no capture) | $68 | ≈$125 | *(not a legal option — Phase 1)* |
| Liquid CO2 release (full chain, incl. capture) | $126 | ≈$232 | **Modern full-chain CCS: ≈$70–160** |

**The direct comparison that matters**: the original's liquid-CO2-release
full chain (capture + liquefaction + transport + disposal) — the standard
alternative the report was arguing *against* — cost an inflation-adjusted
**≈$232/tonne** in 2002. A modern full-chain project (capture + transport
+ geological storage) runs **≈$70–160/tonne** today. That's a real, large
improvement — not because ocean disposal engineering caught up, but
because **capture technology itself got dramatically cheaper** over 24
years of deployment, RD&D investment, and scale-up (NETL's own reported
capture-cost trend line is steadily downward across every source type in
the GCCSI dataset).

That matters for how this report's economic argument should be framed
now. The 2002 mixture-release and P-GLAD ideas were both, at their core, a
bet that **capture would stay expensive enough that clever engineering to
avoid it was worth the tradeoffs** (lower purity, higher compression/
transport volume, in the mixture case; shallow-water engineering
complexity, in P-GLAD's case). Twenty-four years later, capture costs have
fallen enough — separately from, and in addition to, the legal
prohibition on the disposal route itself — that the premise behind
"avoid capture at any cost" has substantially weakened. Even in a
hypothetical world where direct ocean disposal were still legal, the
economic case for skipping capture is considerably less compelling than
it was in 2002.

## 4. Caveats

- **Scope mismatch**: 2002 mixture-release/P-GLAD figures deliberately
  excluded capture cost (that was their whole value proposition); modern
  "full-chain" figures include it. The fairest single comparison is
  therefore 2002 liquid-release (which *did* include capture) against
  today's full-chain CCS, as done above — comparing 2002's capture-free
  routes directly against modern capture-inclusive costs would
  understate how much cheaper the modern route really is.
- **Not a controlled comparison**: different source types (flue gas
  composition, plant type), different locations, different regulatory
  regimes (Class VI wells, 45Q, EU ETS, etc. didn't exist or looked very
  different in 2002), and different technology maturity all confound a
  clean number-to-number comparison. Treat the $70–160/tonne modern
  range and the ≈$232/tonne inflation-adjusted 2002 full-chain figure as
  order-of-magnitude comparable, not precisely equivalent.
- **Search-sourced, not primary-verified**: as with Phase 1, these figures
  came from search-engine-assisted retrieval of public reports, not full
  primary-source review. Good enough for this repo's analysis and for
  informing the revised report's narrative; worth a direct read of the
  underlying NETL/GCCSI reports before citing specific numbers in a more
  formal write-up.
