# CSU/CIndU DB v2

Fresh-start rebuild focused on raw-source collection first.

## Current scope
Source-first CSU/CIndU evidence collection for prioritized mechanism/program buckets:
- BTK
- KIT
- MRGPRX2

## What is here

### Raw source collection
- `collect_ctgov_priority.py` - pulls urticaria studies from ClinicalTrials.gov API v2 using priority program seeds
- `collect_sponsor_priority_sources.py` - caches sponsor HTML/PDF materials as local raw artifacts plus extracted text
- `collect_pubmed_priority_sources.py` - caches PubMed records and PMC full text when available
- `curate_publication_priority_sources.py` - separates primary trial manuscripts from reviews and search-collision hits
- `build_source_registry.py` - joins CT.gov, sponsor, and publication inventories into a program/trial registry
- `scan_disputes.py` - scans knowledge-content Markdown for `[DISPUTE]`, `[NEEDS REVIEW]`, and `[SOURCE NEEDED]` tags

### Raw evidence folders
- `raw/clinicaltrials/json/` - full raw API JSON per NCT
- `raw/clinicaltrials/markdown/` - local Markdown cache per NCT with key extracted fields
- `raw/clinicaltrials/searches/` - raw search result manifests by seed term
- `raw/sponsors/` - sponsor HTML, PDF, extracted text, and markdown wrappers
- `raw/publications/pubmed/` - PubMed XML plus local manuscript summaries
- `raw/publications/pmc/` - PMC XML plus local full-text markdown when available
- `raw/publications/searches/` - PubMed search manifests by seeded program term

### Registries and inventories
- `inventories/ctgov_priority_trials.md` / `.json`
- `inventories/sponsor_priority_sources.md` / `.json`
- `inventories/publication_priority_sources.md` / `.json`
- `inventories/publication_priority_curation.md` / `.json`
- `inventories/source_registry.md` / `.json`
- `inventories/dispute_index.md` / `.json`

### Wiki-system scaffolding
- `docs/CLINPHARM_WIKI_SYSTEM_PROMPT.md`
- `docs/FILE_CONVENTIONS.md`
- `templates/study_page_template.md`
- `templates/program_page_template.md`
- `templates/provenance_block_template.md`
- `wiki/README.md` plus starter `wiki/programs/`, `wiki/trials/`, and `wiki/queries/` folders

## Operating model
Treat the knowledge system as three layers:
1. raw sources
2. normalized registries and inventories
3. derived wiki pages and summaries

Do not collapse these layers together.

## Important note
The `priority_class` field is currently seed-based for collection workflow. Treat it as a working bucket for raw gathering, not final target verification, until each program target is re-checked from direct sponsor or publication sources.

## Current implementation checkpoint
The v2 project now has:
- a raw ClinicalTrials.gov backbone
- sponsor-source caches for prioritized programs
- a cached publication layer with curated primary-trial vs supporting-paper status
- a first program/trial source registry linking these layers conservatively by explicit identifiers
- wiki-system prompt, conventions, and reusable page templates for source-first clinpharm documentation

## Immediate next step
Use `inventories/source_registry.json` as the provenance spine for rebuilding study pages and program pages. Add stronger manual linkage where explicit identifiers are missing, but do not infer study-level links without direct source support.
