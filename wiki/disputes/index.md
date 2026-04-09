# Disputes

Use this section to flag content that needs verification or correction.

## How to dispute a page

### Option 1: Inline flag in the page
Add one of these directly next to the questionable passage:
- `[DISPUTE: ...]`
- `[NEEDS REVIEW]`
- `[SOURCE NEEDED]`

Example:

```text
The predicted half-life was 3 hours. [DISPUTE: re-check against latest dataset and manuscript table]
```

### Option 2: Create a dispute note
Create a new note in `wiki/disputes/` using `../templates/dispute_note_template.md` as the starting format.

## What happens next
- The dispute is indexed by `scan_disputes.py`
- The assistant reviews the dispute against local raw sources first
- If the issue is fixable, the relevant page is updated, committed, and the static site is rebuilt
- If not fixable yet, the dispute stays visible with `[NEEDS REVIEW]` or `[SOURCE NEEDED]`

## Current status
The canonical generated queue is in:
- `../inventories/dispute_index.md`
- `../inventories/dispute_index.json`
