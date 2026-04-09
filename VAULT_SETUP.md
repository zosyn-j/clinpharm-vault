# ClinPharm Vault Setup

This vault was initialized from `research-db/csu-cindu-db-v2/` to make the clinpharm source-first system available to Obsidian-compatible tooling.

## Structure
- `raw/` - raw evidence cache
- `inventories/` - normalized registries and audits
- `wiki/` - derived study/program/query pages
- `docs/` - system prompt and file conventions
- `templates/` - reusable page templates

## Notes
- Canonical workflow is source-first: raw -> inventories -> wiki
- This vault is intended for use with `obsidian-mcp`
- Git is initialized in this vault for local history and rollback
