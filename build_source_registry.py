from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INVENTORY_DIR = BASE_DIR / "inventories"
CTGOV_JSON = INVENTORY_DIR / "ctgov_priority_trials.json"
SPONSOR_JSON = INVENTORY_DIR / "sponsor_priority_sources.json"
PUB_CURATION_JSON = INVENTORY_DIR / "publication_priority_curation.json"
OUT_JSON = INVENTORY_DIR / "source_registry.json"
OUT_MD = INVENTORY_DIR / "source_registry.md"

NCT_RE = re.compile(r"NCT\d{8}", re.IGNORECASE)
DISPLAY_NAME_OVERRIDES = {
    "blu-808": "BLU-808",
    "ep262": "EP262",
    "evo756": "EVO756",
    "sep-631": "SEP-631",
}


def load_json(path: Path):
    return json.loads(path.read_text())


def normalize_program(name: str) -> str:
    return name.strip().lower()


def display_name(key: str, *candidates: str) -> str:
    if key in DISPLAY_NAME_OVERRIDES:
        return DISPLAY_NAME_OVERRIDES[key]
    for candidate in candidates:
        if candidate:
            return candidate
    return key.replace("-", " ").title()


def extract_nct_ids(*texts: str) -> list[str]:
    found = []
    seen = set()
    for text in texts:
        if not text:
            continue
        for match in NCT_RE.findall(text):
            token = match.upper()
            if token not in seen:
                seen.add(token)
                found.append(token)
    return found


def make_ct_trial_record(rec: dict) -> dict:
    nct_id = rec["nct_id"]
    return {
        "trial_id": nct_id,
        "brief_title": rec.get("brief_title"),
        "official_title": rec.get("official_title"),
        "phase": rec.get("phases"),
        "status": rec.get("overall_status"),
        "conditions": rec.get("conditions") or [],
        "lead_sponsor": rec.get("lead_sponsor"),
        "ctgov_url": rec.get("ctgov_url"),
        "local_json": f"raw/clinicaltrials/json/{nct_id}.json",
        "local_markdown": f"raw/clinicaltrials/markdown/{nct_id}.md",
    }


def make_sponsor_record(rec: dict) -> dict:
    explicit_trial_ids = extract_nct_ids(
        rec.get("label", ""),
        rec.get("url", ""),
        " ".join(rec.get("saved_files") or []),
    )
    return {
        "label": rec.get("label"),
        "sponsor": rec.get("sponsor"),
        "kind": rec.get("kind"),
        "status": rec.get("status"),
        "url": rec.get("url"),
        "saved_files": rec.get("saved_files") or [],
        "explicit_trial_ids": explicit_trial_ids,
    }


def make_publication_record(rec: dict, primary: bool) -> dict:
    payload = {
        "pmid": rec.get("pmid"),
        "title": rec.get("title"),
        "journal": rec.get("journal"),
        "pub_year": rec.get("pub_year"),
        "doi": rec.get("doi"),
        "pmcid": rec.get("pmcid"),
        "pubmed_markdown": rec.get("pubmed_markdown"),
        "pubmed_xml": rec.get("pubmed_xml"),
        "pmc_markdown": rec.get("pmc_markdown"),
        "pmc_xml": rec.get("pmc_xml"),
        "linked_trial_ids": rec.get("linked_trial_ids") or [],
        "role": rec.get("role"),
    }
    note_field = "evidence_note" if primary else "note"
    if rec.get(note_field):
        payload[note_field] = rec[note_field]
    return payload


def main():
    ctgov_records = load_json(CTGOV_JSON)
    sponsor_records = load_json(SPONSOR_JSON)["results"]
    publication_curation = load_json(PUB_CURATION_JSON)["programs"]

    ct_by_program: dict[str, list[dict]] = defaultdict(list)
    sponsor_by_program: dict[str, list[dict]] = defaultdict(list)
    pub_by_program: dict[str, dict] = {}
    display_candidates: dict[str, list[str]] = defaultdict(list)
    priority_classes: dict[str, set[str]] = defaultdict(set)

    for rec in ctgov_records:
        key = normalize_program(rec["program"])
        ct_by_program[key].append(rec)
        display_candidates[key].append(rec["program"])
        if rec.get("priority_class"):
            priority_classes[key].add(rec["priority_class"])

    for rec in sponsor_records:
        key = normalize_program(rec["program"])
        sponsor_by_program[key].append(rec)
        display_candidates[key].append(rec["program"])
        if rec.get("priority_class"):
            priority_classes[key].add(rec["priority_class"])

    for rec in publication_curation:
        key = normalize_program(rec["program"])
        pub_by_program[key] = rec
        display_candidates[key].append(rec["program"])
        if rec.get("priority_class"):
            priority_classes[key].add(rec["priority_class"])

    all_programs = sorted(set(ct_by_program) | set(sponsor_by_program) | set(pub_by_program))
    programs_payload = []

    for key in all_programs:
        ct_items = [make_ct_trial_record(rec) for rec in ct_by_program.get(key, [])]
        sponsor_items = [make_sponsor_record(rec) for rec in sponsor_by_program.get(key, [])]
        pub_entry = pub_by_program.get(key)
        primary_pubs = []
        supporting_pubs = []
        excluded_pubs = []
        pub_status = None
        pub_summary = None
        unclassified_pmids = []
        search_manifest = None
        search_term = None

        if pub_entry:
            pub_status = pub_entry.get("status")
            pub_summary = pub_entry.get("summary")
            search_manifest = pub_entry.get("search_manifest")
            search_term = pub_entry.get("search_term")
            primary_pubs = [make_publication_record(rec, primary=True) for rec in pub_entry.get("primary_trial_publications", [])]
            supporting_pubs = [make_publication_record(rec, primary=False) for rec in pub_entry.get("supporting_publications", [])]
            excluded_pubs = pub_entry.get("excluded_or_nonprimary_hits", [])
            unclassified_pmids = pub_entry.get("unclassified_query_pmids", [])

        trial_ids = {item["trial_id"] for item in ct_items}
        for sponsor_item in sponsor_items:
            trial_ids.update(sponsor_item["explicit_trial_ids"])
        for pub_item in primary_pubs + supporting_pubs:
            trial_ids.update([trial_id for trial_id in pub_item.get("linked_trial_ids", []) if trial_id.upper().startswith("NCT")])

        trial_registry = []
        for trial_id in sorted(trial_ids):
            ct_match = next((item for item in ct_items if item["trial_id"] == trial_id), None)
            sponsor_matches = [item for item in sponsor_items if trial_id in item["explicit_trial_ids"]]
            primary_matches = [item for item in primary_pubs if trial_id in item.get("linked_trial_ids", [])]
            supporting_matches = [item for item in supporting_pubs if trial_id in item.get("linked_trial_ids", [])]
            trial_registry.append(
                {
                    "trial_id": trial_id,
                    "ctgov_record": ct_match,
                    "sponsor_artifacts": sponsor_matches,
                    "primary_publications": primary_matches,
                    "supporting_publications": supporting_matches,
                    "evidence_layers": {
                        "ctgov": bool(ct_match),
                        "sponsor": bool(sponsor_matches),
                        "publication_primary": bool(primary_matches),
                        "publication_supporting": bool(supporting_matches),
                    },
                }
            )

        programs_payload.append(
            {
                "program_key": key,
                "display_name": display_name(key, *(display_candidates.get(key) or [])),
                "priority_classes": sorted(priority_classes.get(key) or []),
                "ctgov_trials": ct_items,
                "sponsor_artifacts": sponsor_items,
                "publication_status": pub_status,
                "publication_summary": pub_summary,
                "publication_search_term": search_term,
                "publication_search_manifest": search_manifest,
                "primary_publications": primary_pubs,
                "supporting_publications": supporting_pubs,
                "excluded_or_nonprimary_publications": excluded_pubs,
                "unclassified_query_pmids": unclassified_pmids,
                "trial_registry": trial_registry,
                "source_layer_counts": {
                    "ctgov_trials": len(ct_items),
                    "sponsor_artifacts": len(sponsor_items),
                    "primary_publications": len(primary_pubs),
                    "supporting_publications": len(supporting_pubs),
                },
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "built_from": {
            "ctgov": str(CTGOV_JSON.relative_to(BASE_DIR)),
            "sponsor": str(SPONSOR_JSON.relative_to(BASE_DIR)),
            "publication_curation": str(PUB_CURATION_JSON.relative_to(BASE_DIR)),
        },
        "programs": programs_payload,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    md_lines = [
        "# Program and trial source registry",
        "",
        f"- Generated: {payload['generated_at']}",
        f"- Built from: `{payload['built_from']['ctgov']}`, `{payload['built_from']['sponsor']}`, `{payload['built_from']['publication_curation']}`",
        "- Purpose: join raw ClinicalTrials.gov caches, sponsor artifacts, and curated publication records into a single auditable registry by program and trial ID.",
        "- Linking rule: only attach sponsor artifacts or publications to a specific NCT when an explicit identifier is present in the cached metadata or curated manuscript record.",
        "",
        "## Program summary",
        "",
        "| Program | Class | CT.gov trials | Sponsor artifacts | Primary pubs | Supporting pubs | Publication status |",
        "|---|---|---:|---:|---:|---:|---|",
    ]

    for program in programs_payload:
        classes = ", ".join(program["priority_classes"]) or "NR"
        counts = program["source_layer_counts"]
        md_lines.append(
            f"| {program['display_name']} | {classes} | {counts['ctgov_trials']} | {counts['sponsor_artifacts']} | {counts['primary_publications']} | {counts['supporting_publications']} | {program['publication_status'] or 'NR'} |"
        )

    for program in programs_payload:
        md_lines.extend(
            [
                "",
                f"## {program['display_name']}",
                "",
                f"- Priority class(es): {', '.join(program['priority_classes']) or 'NR'}",
                f"- CT.gov trials: {program['source_layer_counts']['ctgov_trials']}",
                f"- Sponsor artifacts: {program['source_layer_counts']['sponsor_artifacts']}",
                f"- Primary publications: {program['source_layer_counts']['primary_publications']}",
                f"- Supporting publications: {program['source_layer_counts']['supporting_publications']}",
            ]
        )
        if program.get("publication_status"):
            md_lines.append(f"- Publication status: {program['publication_status']}")
        if program.get("publication_summary"):
            md_lines.append(f"- Publication summary: {program['publication_summary']}")

        if program["trial_registry"]:
            md_lines.extend(["", "### Trial registry", ""])
            for trial in program["trial_registry"]:
                phase = trial["ctgov_record"]["phase"] if trial["ctgov_record"] else "NR"
                status = trial["ctgov_record"]["status"] if trial["ctgov_record"] else "NR"
                md_lines.append(f"- **{trial['trial_id']}** | phase: {phase} | status: {status}")
                if trial["ctgov_record"]:
                    md_lines.append(f"  - CT.gov cache: `{trial['ctgov_record']['local_markdown']}`")
                if trial["sponsor_artifacts"]:
                    md_lines.append(f"  - Sponsor artifacts linked: {len(trial['sponsor_artifacts'])}")
                    for item in trial["sponsor_artifacts"]:
                        md_lines.append(f"    - {item['label']} ({item['sponsor']})")
                if trial["primary_publications"]:
                    md_lines.append(f"  - Primary publications linked: {len(trial['primary_publications'])}")
                    for item in trial["primary_publications"]:
                        md_lines.append(f"    - PMID {item['pmid']}: {item['title']}")
                if trial["supporting_publications"]:
                    md_lines.append(f"  - Supporting publications linked: {len(trial['supporting_publications'])}")
                    for item in trial["supporting_publications"]:
                        md_lines.append(f"    - PMID {item['pmid']}: {item['title']}")

        unlinked_primary = [pub for pub in program["primary_publications"] if not any(tid.upper().startswith("NCT") for tid in pub.get("linked_trial_ids", []))]
        if unlinked_primary:
            md_lines.extend(["", "### Primary publications without explicit NCT linkage", ""])
            for pub in unlinked_primary:
                trial_ids = ", ".join(pub.get("linked_trial_ids") or []) or "NR"
                md_lines.append(f"- PMID {pub['pmid']}: {pub['title']} (linked IDs: {trial_ids})")

        unlinked_sponsor = [item for item in program["sponsor_artifacts"] if not item["explicit_trial_ids"]]
        if unlinked_sponsor:
            md_lines.extend(["", "### Program-level sponsor artifacts without explicit NCT linkage", ""])
            for item in unlinked_sponsor:
                md_lines.append(f"- {item['label']} ({item['sponsor']})")

        if program["unclassified_query_pmids"]:
            md_lines.extend(["", "### Remaining publication PMIDs not manually curated yet", ""])
            md_lines.append("- " + ", ".join(program["unclassified_query_pmids"]))

    OUT_MD.write_text("\n".join(md_lines) + "\n")


if __name__ == "__main__":
    main()
