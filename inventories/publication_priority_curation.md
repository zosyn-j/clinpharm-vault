# Curated publication priority-source inventory

- Built from: `inventories/publication_priority_sources.json`
- Purpose: separate true primary trial manuscripts from reviews, background papers, and search-collision hits.
- Curation rule: only promote a paper as a primary manuscript when the title/abstract clearly indicates original clinical data for the program.

## Status summary

- Primary manuscripts found: 4
- Supporting only: 1
- No PubMed hits: 3
- Search collisions only: 1

## remibrutinib (BTK)

- Search term: `(remibrutinib OR LOU064) AND urticaria`
- PubMed hits: 20
- Status: Primary manuscripts found
- Summary: Strong manuscript coverage. Original CSU clinical data are available for phase 2b, phase 2b extension, phase 3 REMIX week-12/24 results, and 52-week REMIX follow-up.

### Primary trial manuscripts

- PMID 36096203 (2022, The Journal of allergy and clinical immunology): **Remibrutinib, a novel BTK inhibitor, demonstrates promising efficacy and safety in chronic spontaneous urticaria.**
  - Role: phase_2b_core
  - Linked trial IDs: NCT03926611
  - Evidence note: Abstract explicitly cites NCT03926611.
  - Cache: `raw/publications/pubmed/markdown/PMID36096203.md`
- PMID 37866460 (2024, The Journal of allergy and clinical immunology): **Remibrutinib demonstrates favorable safety profile and sustained efficacy in chronic spontaneous urticaria over 52 weeks.**
  - Role: phase_2b_extension
  - Linked trial IDs: NCT03926611
  - Evidence note: Abstract describes a phase 2b extension study following the remibrutinib core CSU trial; registration not explicitly repeated in the abstract text saved here.
  - Cache: `raw/publications/pubmed/markdown/PMID37866460.md`
- PMID 40043237 (2025, The New England journal of medicine): **Remibrutinib in Chronic Spontaneous Urticaria.**
  - Role: phase_3_core
  - Linked trial IDs: NCT05030311, NCT05032157
  - Evidence note: Abstract explicitly cites REMIX-1 NCT05030311 and REMIX-2 NCT05032157.
  - Cache: `raw/publications/pubmed/markdown/PMID40043237.md`
- PMID 41115533 (2026, The Journal of allergy and clinical immunology): **Remibrutinib in chronic spontaneous urticaria: 52-week results from two phase 3 studies.**
  - Role: phase_3_long_term
  - Linked trial IDs: NCT05030311, NCT05032157
  - Evidence note: Abstract explicitly cites REMIX-1 NCT05030311 and REMIX-2 NCT05032157.
  - Cache: `raw/publications/pubmed/markdown/PMID41115533.md`

### Supporting/background publications

- PMID 33834628 (2021, Clinical and translational science): **Remibrutinib (LOU064): A selective potent oral BTK inhibitor with promising clinical safety and pharmacodynamics in a randomized phase I trial.**
  - Role: phase_1_background
  - Note: Healthy-volunteer phase 1 safety/pharmacodynamics paper, useful background but not a urticaria efficacy manuscript.
  - Cache: `raw/publications/pubmed/markdown/PMID33834628.md`
- PMID 40455080 (2025, Immunotherapy): **Evaluating remibrutinib in the treatment of chronic spontaneous urticaria.**
  - Role: review
  - Note: Narrative review summarizing remibrutinib CSU data.
  - Cache: `raw/publications/pubmed/markdown/PMID40455080.md`

### Explicit non-primary / excluded hits

- PMID 40435483: Remibrutinib in Chronic Spontaneous Urticaria.
  - Reason: Letter/comment on the NEJM phase 3 paper, not an original trial report.

### Remaining query hits not manually curated yet

- 35667749, 32083858, 41186128, 38141832, 35175630, 40074986, 40663028, 39598410, 40911497, 40747638, 31446134, 41105846, 40682317

## fenebrutinib (BTK)

- Search term: `(fenebrutinib OR GDC-0853) AND urticaria`
- PubMed hits: 15
- Status: Primary manuscripts found
- Summary: One clear primary CSU efficacy manuscript was identified. Remaining hits are mostly reviews, mechanistic/background papers, or search collisions.

### Primary trial manuscripts

- PMID 34750553 (2021, Nature medicine); PMCID PMC8604722: **Fenebrutinib in H1 antihistamine-refractory chronic spontaneous urticaria: a randomized phase 2 trial.**
  - Role: phase_2_core
  - Linked trial IDs: EudraCT 2016-004624-35
  - Evidence note: Abstract explicitly cites EudraCT 2016-004624-35.
  - Cache: `raw/publications/pubmed/markdown/PMID34750553.md`
  - Full text cache: `raw/publications/pmc/markdown/PMC8604722.md`

### Supporting/background publications

- PMID 29457982 (2018, Journal of medicinal chemistry): **Discovery of GDC-0853: A Potent, Selective, and Noncovalent Bruton's Tyrosine Kinase Inhibitor in Early Clinical Development.**
  - Role: discovery_background
  - Note: Medicinal chemistry discovery paper for GDC-0853/fenebrutinib.
  - Cache: `raw/publications/pubmed/markdown/PMID29457982.md`
- PMID 36420759 (2023, Allergy): **Fenebrutinib and BTK inhibition: Unveiling a new target for the treatment of chronic spontaneous urticaria.**
  - Role: review
  - Note: Fenebrutinib-focused review article in CSU.
  - Cache: `raw/publications/pubmed/markdown/PMID36420759.md`
- PMID 40326848 (2025, Clinical and translational allergy): **Biological and target synthetic treatments for chronic spontaneous urticaria: A systematic review and network meta-analysis.**
  - Role: meta_analysis
  - Note: Network meta-analysis including fenebrutinib among CSU therapies.
  - Cache: `raw/publications/pubmed/markdown/PMID40326848.md`

### Explicit non-primary / excluded hits

- PMID 34650565: What Basophil Testing Tells Us About CSU Patients - Results of the CORSA Study.
  - Reason: CORSA basophil-testing study, not a fenebrutinib trial manuscript.

### Remaining query hits not manually curated yet

- 35667749, 38141832, 35175630, 31446134, 35166638, 35569949, 30015639, 31494233, 41270830, 41654334

## rilzabrutinib (BTK)

- Search term: `(rilzabrutinib OR PRN1008) AND urticaria`
- PubMed hits: 10
- Status: Primary manuscripts found
- Summary: One clear primary CSU efficacy manuscript was identified, plus later non-primary drug-review coverage.

### Primary trial manuscripts

- PMID 40266575 (2025, JAMA dermatology); PMCID PMC12019677: **Rilzabrutinib in Antihistamine-Refractory Chronic Spontaneous Urticaria: The RILECSU Phase 2 Randomized Clinical Trial.**
  - Role: phase_2_core
  - Linked trial IDs: NCT05107115
  - Evidence note: Abstract explicitly cites NCT05107115.
  - Cache: `raw/publications/pubmed/markdown/PMID40266575.md`
  - Full text cache: `raw/publications/pmc/markdown/PMC12019677.md`

### Supporting/background publications

- PMID 41359083 (2026, Drugs): **Rilzabrutinib: First Approval.**
  - Role: approval_review
  - Note: First-approval review article, useful for context but not a primary urticaria trial manuscript.
  - Cache: `raw/publications/pubmed/markdown/PMID41359083.md`

### Remaining query hits not manually curated yet

- 38141832, 35175630, 40074986, 39598410, 40326848, 35166638, 41587611, 41937093

## barzolvolimab (KIT)

- Search term: `(barzolvolimab OR CDX-0159) AND urticaria`
- PubMed hits: 16
- Status: Primary manuscripts found
- Summary: Strong manuscript coverage across early CIndU proof-of-concept, CSU phase 1b MAD, and CSU phase 2 dose-finding.

### Primary trial manuscripts

- PMID 36385701 (2023, Allergy): **Anti-KIT antibody, barzolvolimab, reduces skin mast cells and disease activity in chronic inducible urticaria.**
  - Role: cindu_open_label_proof_of_concept
  - Linked trial IDs: NR
  - Evidence note: Abstract describes the open-label single-dose CIndU study but does not state a registration identifier in the saved abstract text.
  - Cache: `raw/publications/pubmed/markdown/PMID36385701.md`
- PMID 40415544 (2025, Allergy); PMCID PMC12368744: **Anti-KIT Barzolvolimab for Chronic Spontaneous Urticaria.**
  - Role: csu_phase_1b_mad
  - Linked trial IDs: NCT04538794
  - Evidence note: Abstract explicitly cites NCT04538794.
  - Cache: `raw/publications/pubmed/markdown/PMID40415544.md`
  - Full text cache: `raw/publications/pmc/markdown/PMC12368744.md`
- PMID 41747871 (2026, The Journal of allergy and clinical immunology): **Randomized dose-finding study of anti-KIT barzolvolimab in patients with chronic spontaneous urticaria.**
  - Role: csu_phase_2_core
  - Linked trial IDs: NCT05368285
  - Evidence note: Abstract explicitly cites NCT05368285.
  - Cache: `raw/publications/pubmed/markdown/PMID41747871.md`

### Supporting/background publications

- PMID 37897679 (2023, Expert opinion on investigational drugs): **Inhibition of KIT for chronic urticaria: a status update on drugs in early clinical development.**
  - Role: review
  - Note: KIT-inhibition status update covering barzolvolimab and related programs.
  - Cache: `raw/publications/pubmed/markdown/PMID37897679.md`
- PMID 38937013 (2024, Immunology and allergy clinics of North America): **Emerging Therapeutics in Chronic Urticaria.**
  - Role: review
  - Note: Broad chronic urticaria emerging-therapeutics review.
  - Cache: `raw/publications/pubmed/markdown/PMID38937013.md`

### Explicit non-primary / excluded hits

- PMID 41535531: Improvement of Chronic Spontaneous Urticaria After Glucagon-Like Peptide 1 Receptor Agonist Therapy: Report of Two Cases.
  - Reason: Case report on GLP-1 receptor agonist therapy, not a barzolvolimab trial manuscript.
- PMID 41877821: Challenges in Differentiating Chronic Inducible Urticaria from Chronic Spontaneous Urticaria.
  - Reason: Differential-diagnosis review, not a barzolvolimab trial manuscript.

### Remaining query hits not manually curated yet

- 40074986, 39598410, 40747638, 35166638, 36719690, 40702781, 41654334, 41270830, 33685605

## briquilimab (KIT)

- Search term: `(briquilimab OR JSP191) AND urticaria`
- PubMed hits: 1
- Status: Supporting only
- Summary: No briquilimab-specific urticaria trial manuscript was identified in this PubMed pass. One broad KIT review hit was captured.

### Supporting/background publications

- PMID 37897679 (2023, Expert opinion on investigational drugs): **Inhibition of KIT for chronic urticaria: a status update on drugs in early clinical development.**
  - Role: review
  - Note: Broad KIT-inhibition review that may mention briquilimab/JSP191, but not a primary urticaria manuscript.
  - Cache: `raw/publications/pubmed/markdown/PMID37897679.md`

## blu-808 (KIT)

- Search term: `BLU-808 AND urticaria`
- PubMed hits: 0
- Status: No PubMed hits
- Summary: No PubMed hits were returned for BLU-808 AND urticaria in this pass.

## evo756 (MRGPRX2)

- Search term: `EVO756 AND urticaria`
- PubMed hits: 0
- Status: No PubMed hits
- Summary: No PubMed hits were returned for EVO756 AND urticaria in this pass.

## ep262 (MRGPRX2)

- Search term: `EP262 AND urticaria`
- PubMed hits: 3
- Status: Search collisions only
- Summary: The PubMed search returned 3 hits, but title-level review suggests they are broad chronic urticaria reviews rather than direct EP262 manuscripts.

### Explicit non-primary / excluded hits

- PMID 40747638: Biologic and small molecule therapies in chronic spontaneous urticaria: an update.
  - Reason: Broad biologic/small-molecule CSU update, not an EP262 primary manuscript.
- PMID 41270830: Emerging IgE and non-IgE targeted therapies for chronic urticaria.
  - Reason: Emerging chronic urticaria therapy review, not an EP262 primary manuscript.
- PMID 41654334: Systemic Treatments for Chronic Spontaneous Urticaria: Anti-IgE and Beyond.
  - Reason: Systemic CSU treatment review, not an EP262 primary manuscript.

## sep-631 (MRGPRX2)

- Search term: `SEP-631 AND urticaria`
- PubMed hits: 0
- Status: No PubMed hits
- Summary: No PubMed hits were returned for SEP-631 AND urticaria in this pass.
