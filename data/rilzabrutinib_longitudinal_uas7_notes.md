# Rilzabrutinib longitudinal UAS7 notes

## Scope

This is a **first-pass landmark dataset** for rilzabrutinib in CSU, centered on explicit numeric values only.

Current local evidence is materially thinner than the remibrutinib and barzolvolimab layers for longitudinal plotting. The usable numeric backbone currently comes from:

- `raw/publications/pmc/markdown/PMC12019677.md`
- `raw/publications/pmc/xml/PMC12019677.xml`
- `raw/publications/pubmed/markdown/PMID40266575.md`
- `raw/sponsors/btk/rilzabrutinib/rilecsu-phase-2-hives-poster.pdf`
- `raw/sponsors/btk/rilzabrutinib/rilecsu-phase-2-hives-poster.txt`
- `raw/sponsors/btk/rilzabrutinib/rilecsu-phase-2-hives-poster.md`
- `raw/sponsors/btk/rilzabrutinib/phase-2-csu-results-press-release.md`

## What is strong enough to use now

### 1) Randomized-arm UAS7 change-from-baseline at week 4 and week 12

From **PMCID `PMC12019677` Table 2** (primary analysis population, omalizumab-naive):

- Week 4 LS mean UAS7 CFB
  - placebo: **-7.06**
  - 400 mg/day: **-9.14**
  - 800 mg/day: **-12.89**
  - 1200 mg/day: **-13.66**
- Week 12 LS mean UAS7 CFB
  - placebo: **-10.14**
  - 400 mg/day: **-9.74**
  - 800 mg/day: **-14.24**
  - 1200 mg/day: **-16.89**

These are the cleanest arm-resolved rilzabrutinib UAS7 longitudinal anchors currently available locally.

### 2) Early 1200 mg/day versus placebo onset landmarks

The same manuscript gives explicit **between-arm** UAS7 difference landmarks for the 1200 mg/day arm:

- Week 1: **-7.89** (95% CI **-12.98 to -2.81**)
- Week 4: **-6.60** (95% CI **-11.22 to -1.97**)
- Week 12: **-6.75** (95% CI **-12.23 to -1.26**)

This supports an honest early-onset plot for the high-dose arm without inventing full per-arm week-1 values.

### 3) Week 12 responder landmarks

From **PMCID `PMC12019677` Table 2**:

- `UAS7 <= 6` at week 12
  - placebo: **11.1%**
  - 1200 mg/day: **34.3%**
  - response difference: **20.3%** (95% CI **1.9 to 38.8**)
- `UAS7 = 0` at week 12
  - placebo: **11.1%**
  - 1200 mg/day: **20.0%**
  - response difference: **6.9%** (95% CI **-9.4 to 23.1**)

## Useful but not yet promoted into the main plotted layer

### Baseline UAS7 by randomized arm

From **PMCID `PMC12019677` Table 1**:

- placebo: **30.0**
- 400 mg/day: **31.4**
- 800 mg/day: **30.2**
- 1200 mg/day: **29.9**

These are useful context values, but the baseline table is in the randomized population while the plotted efficacy landmarks use the primary analysis population. That makes them acceptable as metadata but not ideal for building a pseudo-continuous mean-UAS7 trajectory.

## What is *not* strong enough yet

- Clean per-arm **week 1** UAS7 means or UAS7 change-from-baseline values across all four arms
- A safely tabulated **week-by-week** UAS7 curve
- Mature **week 24 / week 52** CSU efficacy numerics for direct longitudinal comparison in the current local cache
- A clean long-term extension efficacy table analogous to what is available for remibrutinib or the sponsor-poster durability layer for barzolvolimab

## Interpretation rule used for this first pass

Rilzabrutinib should be represented as a **landmark-based longitudinal layer**, not a smooth full-curve layer.

That means:

- Use explicit week 4 and week 12 arm-resolved UAS7 CFB values
- Use explicit week 1, week 4, and week 12 **1200 mg/day vs placebo** difference landmarks
- Use explicit week 12 responder landmarks
- Do **not** fabricate missing weekly points or extension trajectories
