# Remibrutinib longitudinal UAS7 extraction notes

Created: 2026-04-10

## Timepoints now captured (explicit numeric)

### UAS7 change from baseline (LS mean, MMRM)
- **Weeks 1, 2, 4, 12, 24** — REMIX-1 and REMIX-2 individually
- Source: ACAAI 2024 early symptom improvement poster (Figure 2 axis labels)
- Both remibrutinib 25 mg BID and placebo arms, with SE and P-values

### UAS7 responder rates (UAS7<=6)
- **Weeks 1, 2, 12, 24** — REMIX-1 and REMIX-2 individually
- Source: EADV 2024 52-week oral presentation (bar chart explicit values)
- **Week 12 pooled** — EADV 2025 subgroup poster (forest plot overall line)

### UAS7 MID achievement (>=10.5 CFB)
- **Weeks 1, 2** — pooled REMIX-1+2
- Source: ACAAI 2024 poster (Figure 3a)

### UAS7 severity band proportions (pooled)
- **Weeks 0, 1, 2, 12, 24, 52** for severe and moderate bands
- **Weeks 1, 2, 24** for well-controlled+complete and UAS7=0 separately
- Source: GUF 2024 52-week band shift poster

### ISS7 and HSS7 change from baseline
- **Weeks 1, 2, 4, 12, 24** — REMIX-1 and REMIX-2 individually
- Source: ACAAI 2024 poster (Figures 2b, 2c)

## What is NOT yet captured

1. **Week 52 mean UAS7 CFB numeric value** — The EADV 2024 oral has a longitudinal curve
   to week 52 but the exact values at weeks 28-52 are in a graph without axis labels
   readable from pdftotext. The curve visually shows maintenance of ~-20 to -25 CFB through
   week 52, but no explicit number extracted. The GUF 2024 band shift poster confirms
   sustained effect at week 52 via band proportions.

2. **Week 52 UAS7<=6 and UAS7=0 responder rates per-trial** — Only the pooled band shift
   data captures week 52 (complete response 35.1%). Per-trial week 52 responder curves are
   in the EADV 2024 oral but values are graphical.

3. **Placebo-to-remibrutinib switch arm** — Curves exist in EADV 2024 and GUF 2024 sources
   showing the transition at week 24, but no explicit numeric timepoints were extracted
   (graph-only).

4. **Absolute mean UAS7 over time** (not CFB) — Not directly reported in any source. Can be
   derived: baseline ~30.4 + CFB at each week.

## Best source for next extraction pass

**EADV 2024 oral (eadv-2024-early-and-long-term-efficacy-oral.pdf)** is the highest-value
source for the next extraction. It contains:
- Full week-by-week UAS7 CFB curve to week 52 (Figure, both trials)
- Week 52 UAS7<=6 and UAS7=0 responder rates (likely in later slides)
- Switch-arm trajectories

The PDF is image-heavy (Illustrator figures). To get the week 52 numeric values, the best
path is likely:
1. Check the Metz et al. NEJM 2025;392(10):984-994 manuscript supplement for tabulated
   per-week data
2. Or use a visual extraction tool / manual read of the PDF figures

**Secondary candidate**: The EAACI 2024 oral has swimmer plots but is mostly qualitative.
The GUF 2024 poster already gave us the best pooled week 52 data (band proportions).
