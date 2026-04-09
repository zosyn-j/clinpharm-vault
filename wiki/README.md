# Derived wiki layer

This folder is the synthesis layer for the v2 rebuild.

## Rule of use
- Do not treat this folder as the source of truth.
- Raw evidence lives under `../raw/`.
- Normalized linkage lives under `../inventories/`, especially `source_registry.json`.
- Pages here should cite the registry and underlying source artifacts.

## Suggested layout
- `programs/` - program-level overview pages
- `trials/` - one page per study / NCT when possible
- `queries/` - cross-study comparison pages and audit views

## Editing rule
When writing pages here:
1. start from `../inventories/source_registry.json`
2. cite the underlying raw files directly
3. preserve uncertainty when source linkage is incomplete
4. use the templates under `../templates/`
