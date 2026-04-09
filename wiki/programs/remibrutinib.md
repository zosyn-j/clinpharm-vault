# Remibrutinib

## Overview
- Mechanism: Bruton's tyrosine kinase inhibitor
- Alias(es): LOU064
- Sponsor: Novartis
- Development focus: Chronic spontaneous urticaria, with additional chronic inducible urticaria development captured in the raw source layer
- Indications currently represented in v2 raw sources: CSU, CIndU

## Study Inventory

### Completed or published CSU studies
- `NCT03926611` - Phase 2b dose-finding CSU study (`../trials/remibrutinib-nct03926611-phase-2b.md`)
- `NCT04109313` - completed CSU Phase 2 study (CT.gov cache only in v2 so far)
- `NCT05030311` - Phase 3 CSU study linked to PMID 40043237 and PMID 41115533
- `NCT05032157` - Phase 3 CSU study linked to PMID 40043237 and PMID 41115533
- `NCT05048342` - completed CSU Phase 3 study
- `NCT05795153` - completed CSU Phase 3 study

### Active or recruiting studies in current raw cache
- `NCT05513001`
- `NCT05677451`
- `NCT06042478`
- `NCT06868212`
- `NCT07358364`
- `NCT07358780`
- `NCT07408219`

### CIndU / mixed-CU studies in current raw cache
- `NCT05976243` - active not recruiting Phase 3 CIndU study
- `NCT06865651` - recruiting Phase 2 mixed chronic urticaria study with sponsor trial-page cache

## Evidence Summary

### Verified facts
- `NCT03926611` is a randomized, placebo-controlled Phase 2b dose-finding study in adults with CSU inadequately controlled by H1-antihistamines (`../raw/clinicaltrials/markdown/NCT03926611.md`).
- PMID 36096203 reports that `NCT03926611` randomized 311 patients across 6 remibrutinib dose groups plus placebo, with week-4 UAS7 improvements observed across all remibrutinib doses (`../raw/publications/pubmed/markdown/PMID36096203.md`).
- PMID 37866460 reports a Phase 2b extension study with 194 treated patients and 52-week follow-up efficacy/safety data (`../raw/publications/pubmed/markdown/PMID37866460.md`).
- PMID 40043237 and PMID 41115533 are curated as primary Phase 3 manuscripts linked to `NCT05030311` and `NCT05032157` in the registry (`../inventories/source_registry.md`).

### Interpretation
- Remibrutinib is currently the strongest BTK program in the v2 evidence stack because it has broad CT.gov coverage, multiple sponsor artifacts, and multiple curated primary manuscripts with explicit NCT linkage.
- The CSU evidence chain is already strong enough to support study-by-study rebuilding from v2 without relying on the older wiki as the primary source.

### Open questions
- Several CT.gov records in the remibrutinib cluster are not yet paired to sponsor artifacts or manuscripts in the v2 registry.
- CIndU and mixed-CU branches should be normalized into dedicated study pages next.
- Sponsor press releases for the remibrutinib program remain program-level artifacts unless an explicit study linkage is stated in the cached metadata.

## Provenance
- Primary source(s):
  - `../inventories/source_registry.json`
  - `../raw/clinicaltrials/markdown/NCT03926611.md`
  - `../raw/publications/pubmed/markdown/PMID36096203.md`
  - `../raw/publications/pubmed/markdown/PMID37866460.md`
  - `../raw/publications/pubmed/markdown/PMID40043237.md`
  - `../raw/publications/pubmed/markdown/PMID41115533.md`
- Supporting source(s):
  - `../raw/sponsors/btk/remibrutinib/2023-phase-iii-primary-endpoints-press-release.md`
  - `../raw/sponsors/btk/remibrutinib/2024-sustained-efficacy-and-safety-press-release.md`
  - `../raw/sponsors/btk/remibrutinib/2026-cindu-phase-iii-remind-press-release.md`
- Last verified: 2026-04-08
- Verification status: Partial

## Change Log
- 2026-04-08: Created initial v2 remibrutinib program page from the new source registry and raw-source caches.
