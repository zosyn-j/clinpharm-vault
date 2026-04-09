# Dispute Workflow

## Goal

Make it easy for collaborators to challenge a statement in the vault and have that dispute come back through a repeatable fix, commit, and refresh cycle.

## Supported dispute paths

### 1. Inline dispute in an existing page
Use this when one passage is questionable.

Example:

```text
The terminal half-life was 3 hours. [DISPUTE: check against fed-state dataset and source table]
```

You can also use:
- `[NEEDS REVIEW]`
- `[SOURCE NEEDED]`
- `<!-- DISPUTE: ... -->`

### 2. Dedicated dispute note
Use this when the issue is larger than a single sentence or needs supporting evidence.

Create a note under `wiki/disputes/` using the dispute note template.

## Resolution cycle

1. A collaborator flags a dispute in a page or creates a dispute note.
2. `scan_disputes.py` indexes the open disputes into `inventories/dispute_index.md` and `.json`.
3. The assistant reviews the dispute against local raw sources first.
4. If the issue can be resolved confidently:
   - update the affected page
   - add a Change Log entry
   - commit the change in Git
   - rebuild the static site
5. If the issue cannot be resolved confidently:
   - keep `[NEEDS REVIEW]` or `[SOURCE NEEDED]`
   - explain what evidence is missing
   - commit the updated unresolved state if useful

## Refresh command

Run:

```bash
python3 refresh_vault.py
```

This rebuilds the source registry, updates the dispute index, and rebuilds the static site.

## Routing principle

Disputes are meant to route back to the assistant for action. The intended handling pattern is:
- user/team flags dispute
- assistant scans the dispute index
- assistant fixes source-backed issues
- assistant commits the vault
- assistant refreshes the static site output

## Important rule

Do not silently delete a disputed claim. Either:
- correct it with evidence, or
- leave the dispute visible and mark it unresolved.
