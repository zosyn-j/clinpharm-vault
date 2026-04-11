# Barzolvolimab longitudinal UAS7 extraction notes

Created: 2026-04-10

## Timepoints now captured (explicit numeric)

### Baseline UAS7
- Core randomized arms only: **75 mg Q4W, 150 mg Q4W, 300 mg Q8W, placebo**
- Source: AAAAI 2025 CSU poster
- Current baseline values captured: **30.3, 30.8, 31.3, 30.1**

### UAS7 change from baseline (LS mean)
- **Week 12** for the four core randomized arms
- Source: AAAAI 2025 CSU poster
- Values captured:
  - 75 mg Q4W: **-17.06**
  - 150 mg Q4W: **-23.02**
  - 300 mg Q8W: **-23.87**
  - placebo: **-10.47**

### UAS7 <= 6 response landmarks
- **Weeks 12 and 52**
- Source: EADV 2024 congress presentation
- Groups captured:
  - **75 mg Q4W -> 150 mg Q4W / 300 mg Q8W**
  - **150 mg Q4W**
  - **300 mg Q8W**
  - **placebo -> 150 mg Q4W / 300 mg Q8W**
- Current explicit values:
  - 75 -> 150/300: **41.7% -> 59.6%**
  - 150 mg Q4W: **67.4% -> 73.7%**
  - 300 mg Q8W: **62.5% -> 68.2%**
  - placebo -> 150/300: **12.8% -> 63.0%**

### UAS7 = 0 complete-response landmarks
- **Weeks 12 and 52**
- Week 12 values cross-supported by the phase 2 manuscript abstract and the EADV 2024 presentation
- Current explicit values:
  - 75 -> 150/300: **22.9% -> 53.5%**
  - 150 mg Q4W: **51.1% -> 71.1%**
  - 300 mg Q8W: **37.5% -> 52.3%**
  - placebo -> 150/300: **6.4% -> 58.7%**

### Late post-treatment landmark
- **Week 76** sponsor-summary follow-up
- Source: IR press release additional positive data
- Current explicit value: **up to 41%** complete response after treatment completion
- Important caveat: the cached text does **not** cleanly resolve the exact regimen-specific denominator for this week-76 value, so it is stored as a high-level follow-up landmark, not a regimen-resolved series point.

## What is NOT yet captured

1. **Week-by-week mean UAS7 curve**
   - The EADV 2024 and AAAAI 2025 sources clearly show over-time curves, including improvement as early as week 1 and maintenance through week 52.
   - In the current pdftotext-derived wrappers, those curves remain graphical rather than cleanly tabulated.
   - No week-1, week-4, week-8, week-16, week-24, or week-36 mean UAS7 values are being invented.

2. **Exact week 52 mean UAS7 or mean UAS7 CFB by regimen**
   - The current local extraction gives strong week-52 responder and complete-response landmarks, but not a clean regimen-resolved numeric mean UAS7 series.

3. **Exact week 52 / week 76 denominators for observed-data responder analyses**
   - The sponsor materials provide percentages, but the currently cached text does not reliably expose a clean arm-by-arm observed denominator table for later timepoints.

4. **Omalizumab-subgroup week 52 UAS7 CFB table**
   - The EADV 2024 presentation appears to contain this, but the current text extraction is too layout-scrambled to map every numeric value safely back to each subgroup row and treatment group.
   - That layer should wait for a cleaner extraction rather than forcing a guess.

## Important interpretation caveat

- This first-pass dataset mixes:
  - **core randomized arm labels** at baseline and week 12, and
  - **post-week-16 transition groups** at week 52.
- That means the week-52 values should be read as **landmark durability / deepening-of-response outputs**, not as a pure unchanged-randomization trajectory from baseline.

## Best next extraction pass

1. Try a cleaner visual or OCR-assisted extraction of the **mean UAS7 over time** figure from the EADV 2024 presentation.
2. Recover the **week 52 omalizumab-subgroup UAS7 CFB** values only if each number can be mapped safely to the right row/column.
3. Check whether later Celldex posters or any manuscript supplement expose a cleaner **week-52 observed denominator table**.
