# Program and trial source registry

- Generated: 2026-04-09T16:58:14.998407+00:00
- Built from: `inventories/ctgov_priority_trials.json`, `inventories/sponsor_priority_sources.json`, `inventories/publication_priority_curation.json`
- Purpose: join raw ClinicalTrials.gov caches, sponsor artifacts, and curated publication records into a single auditable registry by program and trial ID.
- Linking rule: only attach sponsor artifacts or publications to a specific NCT when an explicit identifier is present in the cached metadata or curated manuscript record.

## Program summary

| Program | Class | CT.gov trials | Sponsor artifacts | Primary pubs | Supporting pubs | Publication status |
|---|---|---:|---:|---:|---:|---|
| Barzolvolimab | KIT | 8 | 6 | 3 | 2 | primary_manuscripts_found |
| BLU-808 | KIT | 1 | 4 | 0 | 0 | no_pubmed_hits |
| Briquilimab | KIT | 3 | 1 | 0 | 1 | supporting_only |
| EP262 | MRGPRX2 | 2 | 1 | 0 | 0 | search_collisions_only |
| EVO756 | MRGPRX2 | 2 | 7 | 0 | 0 | no_pubmed_hits |
| Fenebrutinib | BTK | 2 | 0 | 1 | 3 | primary_manuscripts_found |
| Remibrutinib | BTK | 16 | 4 | 4 | 2 | primary_manuscripts_found |
| Rilzabrutinib | BTK | 1 | 1 | 1 | 1 | primary_manuscripts_found |
| SEP-631 | MRGPRX2 | 0 | 2 | 0 | 0 | no_pubmed_hits |

## Barzolvolimab

- Priority class(es): KIT
- CT.gov trials: 8
- Sponsor artifacts: 6
- Primary publications: 3
- Supporting publications: 2
- Publication status: primary_manuscripts_found
- Publication summary: Strong manuscript coverage across early CIndU proof-of-concept, CSU phase 1b MAD, and CSU phase 2 dose-finding.

### Trial registry

- **NCT04538794** | phase: ['PHASE1'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT04538794.md`
  - Primary publications linked: 1
    - PMID 40415544: Anti-KIT Barzolvolimab for Chronic Spontaneous Urticaria.
- **NCT04548869** | phase: ['PHASE1'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT04548869.md`
- **NCT05368285** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05368285.md`
  - Primary publications linked: 1
    - PMID 41747871: Randomized dose-finding study of anti-KIT barzolvolimab in patients with chronic spontaneous urticaria.
- **NCT05405660** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05405660.md`
- **NCT06445023** | phase: ['PHASE3'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06445023.md`
- **NCT06455202** | phase: ['PHASE3'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06455202.md`
- **NCT07256392** | phase: ['PHASE3'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT07256392.md`
- **NCT07266402** | phase: ['PHASE3'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT07266402.md`

### Primary publications without explicit NCT linkage

- PMID 36385701: Anti-KIT antibody, barzolvolimab, reduces skin mast cells and disease activity in chronic inducible urticaria. (linked IDs: NR)

### Program-level sponsor artifacts without explicit NCT linkage

- IR press release positive results (Celldex)
- IR press release additional positive data (Celldex)
- AAAAI 2025 CSU poster (Celldex)
- Phase 2 CIndU ACAAI poster (Celldex)
- EADV 2024 congress presentation (Celldex)
- IR press release PDF additional data (Celldex)

### Remaining publication PMIDs not manually curated yet

- 40074986, 39598410, 40747638, 35166638, 36719690, 40702781, 41654334, 41270830, 33685605

## BLU-808

- Priority class(es): KIT
- CT.gov trials: 1
- Sponsor artifacts: 4
- Primary publications: 0
- Supporting publications: 0
- Publication status: no_pubmed_hits
- Publication summary: No PubMed hits were returned for BLU-808 AND urticaria in this pass.

### Trial registry

- **NCT06931405** | phase: ['PHASE2'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06931405.md`

### Program-level sponsor artifacts without explicit NCT linkage

- Core programs page (Blueprint Medicines)
- AAAAI WAO 2025 publications page (Blueprint Medicines)
- AAAAI WAO 2025 BLU-808 WT KIT poster (Blueprint Medicines)
- AAAAI 2024 BLU-808 WT KIT poster (Blueprint Medicines)

## Briquilimab

- Priority class(es): KIT
- CT.gov trials: 3
- Sponsor artifacts: 1
- Primary publications: 0
- Supporting publications: 1
- Publication status: supporting_only
- Publication summary: No briquilimab-specific urticaria trial manuscript was identified in this PubMed pass. One broad KIT review hit was captured.

### Trial registry

- **NCT06162728** | phase: ['PHASE1', 'PHASE2'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06162728.md`
- **NCT06353971** | phase: ['PHASE1', 'PHASE2'] | status: TERMINATED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06353971.md`
- **NCT06736262** | phase: ['PHASE2'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06736262.md`

### Program-level sponsor artifacts without explicit NCT linkage

- Briquilimab program page (Jasper Therapeutics)

## EP262

- Priority class(es): MRGPRX2
- CT.gov trials: 2
- Sponsor artifacts: 1
- Primary publications: 0
- Supporting publications: 0
- Publication status: search_collisions_only
- Publication summary: The PubMed search returned 3 hits, but title-level review suggests they are broad chronic urticaria reviews rather than direct EP262 manuscripts.

### Trial registry

- **NCT06050928** | phase: ['PHASE1'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06050928.md`
- **NCT06077773** | phase: ['PHASE2'] | status: TERMINATED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06077773.md`

### Program-level sponsor artifacts without explicit NCT linkage

- Pipeline page (Escient Pharmaceuticals)

## EVO756

- Priority class(es): MRGPRX2
- CT.gov trials: 2
- Sponsor artifacts: 7
- Primary publications: 0
- Supporting publications: 0
- Publication status: no_pubmed_hits
- Publication summary: No PubMed hits were returned for EVO756 AND urticaria in this pass.

### Trial registry

- **NCT06603220** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06603220.md`
- **NCT06873516** | phase: ['PHASE2'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06873516.md`

### Program-level sponsor artifacts without explicit NCT linkage

- MRGPRX2 antagonist program page (Evommune)
- Clinical trials page (Evommune)
- CIndU Phase 2 trial initiation PDF (Evommune)
- GA2LEN 2024 trial results presentation PDF (Evommune)
- CSU Phase 2b trial initiation PDF (Evommune)
- CIndU top-line press release PDF (Evommune)
- EADV 2025 CIndU presentation PDF (Evommune)

## Fenebrutinib

- Priority class(es): BTK
- CT.gov trials: 2
- Sponsor artifacts: 0
- Primary publications: 1
- Supporting publications: 3
- Publication status: primary_manuscripts_found
- Publication summary: One clear primary CSU efficacy manuscript was identified. Remaining hits are mostly reviews, mechanistic/background papers, or search collisions.

### Trial registry

- **NCT03137069** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT03137069.md`
- **NCT03693625** | phase: ['PHASE2'] | status: TERMINATED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT03693625.md`

### Primary publications without explicit NCT linkage

- PMID 34750553: Fenebrutinib in H1 antihistamine-refractory chronic spontaneous urticaria: a randomized phase 2 trial. (linked IDs: EudraCT 2016-004624-35)

### Remaining publication PMIDs not manually curated yet

- 35667749, 38141832, 35175630, 31446134, 35166638, 35569949, 30015639, 31494233, 41270830, 41654334

## Remibrutinib

- Priority class(es): BTK
- CT.gov trials: 16
- Sponsor artifacts: 4
- Primary publications: 4
- Supporting publications: 2
- Publication status: primary_manuscripts_found
- Publication summary: Strong manuscript coverage. Original CSU clinical data are available for phase 2b, phase 2b extension, phase 3 REMIX week-12/24 results, and 52-week REMIX follow-up.

### Trial registry

- **NCT03926611** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT03926611.md`
  - Primary publications linked: 2
    - PMID 36096203: Remibrutinib, a novel BTK inhibitor, demonstrates promising efficacy and safety in chronic spontaneous urticaria.
    - PMID 37866460: Remibrutinib demonstrates favorable safety profile and sustained efficacy in chronic spontaneous urticaria over 52 weeks.
- **NCT04109313** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT04109313.md`
- **NCT05030311** | phase: ['PHASE3'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05030311.md`
  - Primary publications linked: 2
    - PMID 40043237: Remibrutinib in Chronic Spontaneous Urticaria.
    - PMID 41115533: Remibrutinib in chronic spontaneous urticaria: 52-week results from two phase 3 studies.
- **NCT05032157** | phase: ['PHASE3'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05032157.md`
  - Primary publications linked: 2
    - PMID 40043237: Remibrutinib in Chronic Spontaneous Urticaria.
    - PMID 41115533: Remibrutinib in chronic spontaneous urticaria: 52-week results from two phase 3 studies.
- **NCT05048342** | phase: ['PHASE3'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05048342.md`
- **NCT05170724** | phase: [] | status: AVAILABLE
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05170724.md`
- **NCT05513001** | phase: ['PHASE3'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05513001.md`
- **NCT05677451** | phase: ['PHASE3'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05677451.md`
- **NCT05795153** | phase: ['PHASE3'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05795153.md`
- **NCT05976243** | phase: ['PHASE3'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05976243.md`
- **NCT06042478** | phase: ['PHASE3'] | status: ACTIVE_NOT_RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06042478.md`
- **NCT06865651** | phase: ['PHASE2'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06865651.md`
  - Sponsor artifacts linked: 1
    - Novartis trial page NCT06865651 (Novartis)
- **NCT06868212** | phase: ['PHASE3'] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT06868212.md`
- **NCT07358364** | phase: [] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT07358364.md`
- **NCT07358780** | phase: [] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT07358780.md`
- **NCT07408219** | phase: [] | status: RECRUITING
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT07408219.md`

### Program-level sponsor artifacts without explicit NCT linkage

- 2023 Phase III primary endpoints press release (Novartis)
- 2024 sustained efficacy and safety press release (Novartis)
- 2026 CIndU Phase III RemIND press release (Novartis)

### Remaining publication PMIDs not manually curated yet

- 35667749, 32083858, 41186128, 38141832, 35175630, 40074986, 40663028, 39598410, 40911497, 40747638, 31446134, 41105846, 40682317

## Rilzabrutinib

- Priority class(es): BTK
- CT.gov trials: 1
- Sponsor artifacts: 1
- Primary publications: 1
- Supporting publications: 1
- Publication status: primary_manuscripts_found
- Publication summary: One clear primary CSU efficacy manuscript was identified, plus later non-primary drug-review coverage.

### Trial registry

- **NCT05107115** | phase: ['PHASE2'] | status: COMPLETED
  - CT.gov cache: `raw/clinicaltrials/markdown/NCT05107115.md`
  - Primary publications linked: 1
    - PMID 40266575: Rilzabrutinib in Antihistamine-Refractory Chronic Spontaneous Urticaria: The RILECSU Phase 2 Randomized Clinical Trial.

### Program-level sponsor artifacts without explicit NCT linkage

- Sanofi pipeline page (Sanofi)

### Remaining publication PMIDs not manually curated yet

- 38141832, 35175630, 40074986, 39598410, 40326848, 35166638, 41587611, 41937093

## SEP-631

- Priority class(es): MRGPRX2
- CT.gov trials: 0
- Sponsor artifacts: 2
- Primary publications: 0
- Supporting publications: 0
- Publication status: no_pubmed_hits
- Publication summary: No PubMed hits were returned for SEP-631 AND urticaria in this pass.

### Program-level sponsor artifacts without explicit NCT linkage

- Pipeline page (Septerna)
- AAAAI 2026 poster PDF (Septerna)
