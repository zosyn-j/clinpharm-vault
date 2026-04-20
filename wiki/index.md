# ClinPharm Vault

<div class="hero">
  <h2>Source-first clinical pharmacology knowledge base</h2>
  <p>This site is built from local raw evidence, normalized registries, and derived wiki pages. If a claim matters, you should be able to trace it back to the underlying source files.</p>
</div>

## What is here

This vault is organized into three layers:
1. **Raw evidence** in `../raw/`
2. **Registries and inventories** in `../inventories/`
3. **Derived wiki pages** in this `wiki/` folder

Current first-pass derived coverage now includes:
- **9 program pages**
- **35 CT.gov-linked trial pages**
- registry, dispute, and data-access pages

<div class="card-grid">
  <div class="card">
    <h3>Programs</h3>
    <p>Program-level evidence maps, sponsor context, and study inventory across the current urticaria set.</p>
    <a href="queries/catalog.html">Open program catalog</a>
  </div>
  <div class="card">
    <h3>Trials</h3>
    <p>Study-level pages with design, endpoints, provenance, and open questions.</p>
    <a href="queries/catalog.html">Browse trial catalog</a>
  </div>
  <div class="card">
    <h3>Registry</h3>
    <p>The main provenance spine linking CT.gov, sponsor artifacts, and publications.</p>
    <a href="inventories/source_registry.html">Open source registry</a>
  </div>
  <div class="card">
    <h3>Disputes</h3>
    <p>Flag questionable statements, track unresolved items, and route them back for correction.</p>
    <a href="disputes/index.html">Open dispute workflow</a>
  </div>
  <div class="card">
    <h3>Data</h3>
    <p>Open the source registry and jump out to the full raw data cache in GitHub.</p>
    <a href="data.html">Open data access page</a>
  </div>
  <div class="card">
    <h3>Phase 2 populations</h3>
    <p>Compare enrolled CSU Phase 2 populations across remibrutinib, rilzabrutinib, barzolvolimab, fenebrutinib, and EVO756.</p>
    <a href="queries/csu-phase-2-population-comparison.html">Open Phase 2 population table</a>
  </div>
</div>

## Current emphasis
- Urticaria development landscape
- Program-level evidence mapping
- Study-level provenance
- Source-backed study design and manuscript linkage

## Key entry points
- [Program and trial catalog](queries/catalog.md)
- [CSU Phase 2 population comparison](queries/csu-phase-2-population-comparison.md)
- [Remibrutinib program](programs/remibrutinib.md)
- [Barzolvolimab program](programs/barzolvolimab.md)
- [Fenebrutinib program](programs/fenebrutinib.md)
- [Rilzabrutinib program](programs/rilzabrutinib.md)
- [Source registry](../inventories/source_registry.md)
- [Dispute index](../inventories/dispute_index.md)
- [Data access](data.md)

<div class="note">
  <strong>Editing model:</strong> edit in Obsidian, track changes with Git, and publish through the generated static site. Derived pages are not the source of truth, the underlying raw evidence and registries are.
</div>
