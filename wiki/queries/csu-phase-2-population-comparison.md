---
title: CSU Phase 2 population comparison
tags:
  - type/query
---
# CSU Phase 2 population comparison

This page is a conservative, source-backed comparison of the enrolled **CSU Phase 2 populations** across the main public competitor programs currently represented in the vault. It is meant to answer a practical question: **were these studies really enrolling the same kind of patients, or only broadly similar ones?**

## Bottom line

The Phase 2 CSU programs were **directionally similar**, meaning they generally enrolled **adult patients with active CSU that remained inadequately controlled on H1-antihistamines**. But they were **not literally identical populations**.

The biggest practical differences in the current local source layer are:
- **prior omalizumab handling**
- **minimum CSU diagnosis duration**
- **how explicitly activity thresholds were defined**
- **whether background H1 therapy stability was spelled out**
- **age caps**

## Comparison table

| Program                                       | Trial                                                         | CSU diagnosis length | H1 use (Y/N, treatment context)                                                                                                                                                                                                                                                                               | Oma use gated (Y/N)                                                                                                                                                                                                                                                                                                                                                 | Activity threshold (UAS7, ISS7, HSS7)                                                                         | Age bracket |
| --------------------------------------------- | ------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------- |
| [Remibrutinib](../programs/remibrutinib.md)   | [NCT03926611](../trials/remibrutinib-nct03926611-phase-2b.md) | **>= 6 months**      | **Yes**. Inadequately controlled on second-generation H1-antihistamines; itch and hives had to be present for **>= 6 consecutive weeks despite H1 use**. No explicit stable-run-in duration is visible in the current local layer.                                                                            | **No**. Publication states patients could enroll **with or without prior anti-IgE treatment**.                                                                                                                                                                                                                                                                      | **UAS7 >= 16; HSS7 >= 8**                                                                                     | **18-99**   |
| [Rilzabrutinib](../programs/rilzabrutinib.md) | [NCT05107115](../trials/rilzabrutinib-nct05107115.md)         | **>= 3 months**      | **Yes**. Refractory to H1-antihistamines; itch and hives had to be present for **>= 6 consecutive weeks despite H1 use**. Participants were to be on a study-defined H1-antihistamine regimen.                                                                                                                | **Yes, partial gate**. Eligible population was **omalizumab-naive or omalizumab-incomplete responders**; the manuscript's primary analysis population was **omalizumab-naive**.                                                                                                                                                                                     | **UAS7 >= 16; ISS7 >= 8**                                                                                     | **18-80**   |
| [Barzolvolimab](../programs/barzolvolimab.md) | [NCT05368285](../trials/barzolvolimab-nct05368285.md)         | **>= 6 months**      | **Yes**. Had to have CSU despite a **stable second-generation non-sedating H1-antihistamine regimen**; hives present for **>= 6 weeks** despite H1 use; stable regimen required for **>= 4 weeks** before treatment.                                                                                          | **No explicit gate in current local eligibility layer**. Publication says patients **with and without prior omalizumab treatment** responded similarly, which implies prior exposure was present in at least part of the enrolled population.                                                                                                                       | **UAS7 >= 16; ISS7 >= 8**                                                                                     | **18+**     |
| [Fenebrutinib](../programs/fenebrutinib.md)   | [NCT03137069](../trials/fenebrutinib-nct03137069.md)          | **>= 6 months**      | **Yes**. Refractory to H1-antihistamines at randomization; manuscript-level methods say patients were symptomatic despite H1 antihistamines, up to **4x approved dose**, and maintained stable H1 therapy starting at least **3 consecutive days immediately before screening and continuing through Day 1**. | **Yes**. Excluded **omalizumab within 4 months before screening** and excluded **primary nonresponse to omalizumab**.                                                                                                                                                                                                                                               | **UAS7 >= 16** in manuscript methods; no ISS7 or HSS7 threshold surfaced in the current local promoted layer. | **18-75**   |
| [EVO756](../programs/evo756.md)               | [NCT06873516](../trials/evo756-nct06873516.md)                | **>= 3 months**      | **Yes**. Inadequate response to H1-antihistamines; if taking H1-antihistamines, participants had to be on a **stable regimen for 4 weeks before Day 1** and remain on it during study.                                                                                                                        | **No, prior exposure allowed**. A March 2026 Evommune corporate presentation for the phase 2b CSU trial states **prior exposure to omalizumab allowed** (slide 23). Exact gating beyond that allowance is still not fully detailed in the current local public layer.                                              | **UAS7 >= 16**; no visible ISS7 or HSS7 threshold in the current local layer.                                 | **18+**     |

## Practical read

- **Closest pair by general population shape:** remibrutinib and barzolvolimab, with rilzabrutinib also clearly in the same adult active-antihistamine-refractory CSU bucket.
- **Most important non-equivalence issue:** **omalizumab handling**. This is the biggest reason not to pretend these trials enrolled interchangeable populations.
- **Shorter diagnosis-duration threshold:** rilzabrutinib and EVO756 used **>= 3 months**, whereas remibrutinib, barzolvolimab, and fenebrutinib used **>= 6 months**.
- **Most explicit background H1 stability wording:** barzolvolimab and EVO756.
- **Most restrictive visible omalizumab rule:** fenebrutinib.
- **Most publication-thin public population layer:** EVO756, which currently looks broadly comparable but is still less richly characterized than the more mature BTK and KIT programs.

## Suggested extra columns to add later

If we want to make this comparison table sharper, the highest-value additional columns would be:
- **Prior biologic exposure detail** rather than a simple Oma gate Y/N
- **Symptom duration requirement** as its own column, separate from diagnosis duration
- **Background H1 stability / run-in requirement** as its own column
- **CIndU / physical urticaria exclusion wording**
- **Prior BTK / prior KIT / prior investigational therapy exclusion**
- **Baseline angioedema allowance or prevalence**
- **Geography / site count**, if we want a cleaner operational-comparability layer

## Source notes

This comparison is based on the currently cached local source layer, primarily:
- [Remibrutinib NCT03926611](../trials/remibrutinib-nct03926611-phase-2b.md) plus `raw/publications/pubmed/markdown/PMID36096203.md`
- [Rilzabrutinib NCT05107115](../trials/rilzabrutinib-nct05107115.md) plus `raw/publications/pubmed/markdown/PMID40266575.md`
- [Barzolvolimab NCT05368285](../trials/barzolvolimab-nct05368285.md) plus `raw/publications/pubmed/markdown/PMID41747871.md`
- [Fenebrutinib NCT03137069](../trials/fenebrutinib-nct03137069.md) plus `raw/publications/pubmed/markdown/PMID34750553.md` and `raw/publications/pmc/markdown/PMC8604722.md`
- [EVO756 NCT06873516](../trials/evo756-nct06873516.md) plus `raw/sponsors/mrgprx2/evo756/csu-phase-2b-trial-initiation-pdf.md` and `raw/sponsors/mrgprx2/evo756/corporate-presentation-march-2026.md` (slide 23 for prior omalizumab exposure allowed)
