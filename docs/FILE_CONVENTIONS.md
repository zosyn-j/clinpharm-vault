# Clinical Pharmacology Wiki File Conventions

## A. Dispute tags

Use these inline tags when a statement is questionable:

- `[DISPUTE]` = likely wrong or conflicting with another source
- `[NEEDS REVIEW]` = not confidently resolved yet
- `[SOURCE NEEDED]` = claim currently lacks an adequate source
- `[INFERRED]` = reasonable inference, but not directly stated by source

Optional HTML-comment form:

```html
<!-- DISPUTE: sponsor slide reports 24 subjects but manuscript reports 26 -->
<!-- SOURCE NEEDED: exact Tmax for fed cohort -->
<!-- NEEDS REVIEW: page-level citation missing -->
```

## B. How to flag a disputed passage

Format:

```text
Original sentence. [DISPUTE: short reason or requested action]
```

Example:

```text
The terminal half-life was approximately 3 hours. [DISPUTE: seems inconsistent with 2026 fed-state dataset, re-check source tables]
```

## C. Provenance block

For any study or source-backed page, include a provenance section like this:

```markdown
## Provenance
- Source type: ClinicalTrials.gov / manuscript / protocol / sponsor slide / press release
- Primary source(s):
  - PMID 40043237
  - NCT05030311
  - `raw/publications/pubmed/markdown/PMID40043237.md`
- Supporting source(s):
  - `raw/sponsors/...`
- Last verified: YYYY-MM-DD
- Verification status: Verified / Partial / Needs review
```

## D. Verified vs inferred statements

Use explicit labels in the body when needed:

- **Verified:** directly supported by source text
- **Inferred:** derived from source context but not explicitly stated
- **Unresolved:** conflicting or incomplete evidence

Example:

- **Verified:** 470 patients were randomized in REMIX-1.
- **Inferred:** The extension population likely overlaps substantially with the core efficacy set.
- **Unresolved:** Per-arm discontinuation counts were not consistently reported across sources.

## E. Change Log section

Add this at the bottom of files that are substantively edited:

```markdown
## Change Log
- 2026-04-08: Updated week 12 UAS7 result to match PMID 40043237.
- 2026-04-08: Marked per-arm N as unresolved because the source provided total N and ratio, but not realized arm counts.
```

## F. Citation style inside pages

Prefer simple, auditable references:

- `(PMID 40043237)`
- `(NCT05030311)`
- ``(`raw/publications/pubmed/markdown/PMID40043237.md`)``
- `Source PDF page 18`

If exact page numbers are known, include them.
If exact page numbers are not known, do not invent them.

## G. Conflict handling rule

When two sources disagree:

1. keep both visible
2. prefer the more primary source
3. describe the conflict plainly
4. mark unresolved items with `[NEEDS REVIEW]`
5. log the correction or open issue in Change Log
