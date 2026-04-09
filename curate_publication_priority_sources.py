from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INVENTORY_JSON = BASE_DIR / "inventories" / "publication_priority_sources.json"
OUT_JSON = BASE_DIR / "inventories" / "publication_priority_curation.json"
OUT_MD = BASE_DIR / "inventories" / "publication_priority_curation.md"

MANUAL_CURATION = {
    "remibrutinib": {
        "status": "primary_manuscripts_found",
        "summary": "Strong manuscript coverage. Original CSU clinical data are available for phase 2b, phase 2b extension, phase 3 REMIX week-12/24 results, and 52-week REMIX follow-up.",
        "primary_pmids": {
            "36096203": {
                "role": "phase_2b_core",
                "linked_trial_ids": ["NCT03926611"],
                "evidence_note": "Abstract explicitly cites NCT03926611.",
            },
            "37866460": {
                "role": "phase_2b_extension",
                "linked_trial_ids": ["NCT03926611"],
                "evidence_note": "Abstract describes a phase 2b extension study following the remibrutinib core CSU trial; registration not explicitly repeated in the abstract text saved here.",
            },
            "40043237": {
                "role": "phase_3_core",
                "linked_trial_ids": ["NCT05030311", "NCT05032157"],
                "evidence_note": "Abstract explicitly cites REMIX-1 NCT05030311 and REMIX-2 NCT05032157.",
            },
            "41115533": {
                "role": "phase_3_long_term",
                "linked_trial_ids": ["NCT05030311", "NCT05032157"],
                "evidence_note": "Abstract explicitly cites REMIX-1 NCT05030311 and REMIX-2 NCT05032157.",
            },
        },
        "supporting_pmids": {
            "33834628": {
                "role": "phase_1_background",
                "note": "Healthy-volunteer phase 1 safety/pharmacodynamics paper, useful background but not a urticaria efficacy manuscript.",
            },
            "40455080": {
                "role": "review",
                "note": "Narrative review summarizing remibrutinib CSU data.",
            },
        },
        "exclude_pmids": {
            "40435483": "Letter/comment on the NEJM phase 3 paper, not an original trial report.",
        },
    },
    "fenebrutinib": {
        "status": "primary_manuscripts_found",
        "summary": "One clear primary CSU efficacy manuscript was identified. Remaining hits are mostly reviews, mechanistic/background papers, or search collisions.",
        "primary_pmids": {
            "34750553": {
                "role": "phase_2_core",
                "linked_trial_ids": ["EudraCT 2016-004624-35"],
                "evidence_note": "Abstract explicitly cites EudraCT 2016-004624-35.",
            },
        },
        "supporting_pmids": {
            "29457982": {
                "role": "discovery_background",
                "note": "Medicinal chemistry discovery paper for GDC-0853/fenebrutinib.",
            },
            "36420759": {
                "role": "review",
                "note": "Fenebrutinib-focused review article in CSU.",
            },
            "40326848": {
                "role": "meta_analysis",
                "note": "Network meta-analysis including fenebrutinib among CSU therapies.",
            },
        },
        "exclude_pmids": {
            "34650565": "CORSA basophil-testing study, not a fenebrutinib trial manuscript.",
        },
    },
    "rilzabrutinib": {
        "status": "primary_manuscripts_found",
        "summary": "One clear primary CSU efficacy manuscript was identified, plus later non-primary drug-review coverage.",
        "primary_pmids": {
            "40266575": {
                "role": "phase_2_core",
                "linked_trial_ids": ["NCT05107115"],
                "evidence_note": "Abstract explicitly cites NCT05107115.",
            },
        },
        "supporting_pmids": {
            "41359083": {
                "role": "approval_review",
                "note": "First-approval review article, useful for context but not a primary urticaria trial manuscript.",
            },
        },
        "exclude_pmids": {},
    },
    "barzolvolimab": {
        "status": "primary_manuscripts_found",
        "summary": "Strong manuscript coverage across early CIndU proof-of-concept, CSU phase 1b MAD, and CSU phase 2 dose-finding.",
        "primary_pmids": {
            "36385701": {
                "role": "cindu_open_label_proof_of_concept",
                "linked_trial_ids": [],
                "evidence_note": "Abstract describes the open-label single-dose CIndU study but does not state a registration identifier in the saved abstract text.",
            },
            "40415544": {
                "role": "csu_phase_1b_mad",
                "linked_trial_ids": ["NCT04538794"],
                "evidence_note": "Abstract explicitly cites NCT04538794.",
            },
            "41747871": {
                "role": "csu_phase_2_core",
                "linked_trial_ids": ["NCT05368285"],
                "evidence_note": "Abstract explicitly cites NCT05368285.",
            },
        },
        "supporting_pmids": {
            "37897679": {
                "role": "review",
                "note": "KIT-inhibition status update covering barzolvolimab and related programs.",
            },
            "38937013": {
                "role": "review",
                "note": "Broad chronic urticaria emerging-therapeutics review.",
            },
        },
        "exclude_pmids": {
            "41535531": "Case report on GLP-1 receptor agonist therapy, not a barzolvolimab trial manuscript.",
            "41877821": "Differential-diagnosis review, not a barzolvolimab trial manuscript.",
        },
    },
    "briquilimab": {
        "status": "supporting_only",
        "summary": "No briquilimab-specific urticaria trial manuscript was identified in this PubMed pass. One broad KIT review hit was captured.",
        "primary_pmids": {},
        "supporting_pmids": {
            "37897679": {
                "role": "review",
                "note": "Broad KIT-inhibition review that may mention briquilimab/JSP191, but not a primary urticaria manuscript.",
            },
        },
        "exclude_pmids": {},
    },
    "blu-808": {
        "status": "no_pubmed_hits",
        "summary": "No PubMed hits were returned for BLU-808 AND urticaria in this pass.",
        "primary_pmids": {},
        "supporting_pmids": {},
        "exclude_pmids": {},
    },
    "evo756": {
        "status": "no_pubmed_hits",
        "summary": "No PubMed hits were returned for EVO756 AND urticaria in this pass.",
        "primary_pmids": {},
        "supporting_pmids": {},
        "exclude_pmids": {},
    },
    "ep262": {
        "status": "search_collisions_only",
        "summary": "The PubMed search returned 3 hits, but title-level review suggests they are broad chronic urticaria reviews rather than direct EP262 manuscripts.",
        "primary_pmids": {},
        "supporting_pmids": {},
        "exclude_pmids": {
            "40747638": "Broad biologic/small-molecule CSU update, not an EP262 primary manuscript.",
            "41270830": "Emerging chronic urticaria therapy review, not an EP262 primary manuscript.",
            "41654334": "Systemic CSU treatment review, not an EP262 primary manuscript.",
        },
    },
    "sep-631": {
        "status": "no_pubmed_hits",
        "summary": "No PubMed hits were returned for SEP-631 AND urticaria in this pass.",
        "primary_pmids": {},
        "supporting_pmids": {},
        "exclude_pmids": {},
    },
}

STATUS_LABELS = {
    "primary_manuscripts_found": "Primary manuscripts found",
    "supporting_only": "Supporting only",
    "no_pubmed_hits": "No PubMed hits",
    "search_collisions_only": "Search collisions only",
}


def load_inventory() -> dict:
    return json.loads(INVENTORY_JSON.read_text())


def build_record_maps(inventory: dict):
    record_by_pmid = {rec["pmid"]: rec for rec in inventory["records"]}
    query_by_program = {query["program"]: query for query in inventory["queries"]}
    return record_by_pmid, query_by_program


def record_payload(record: dict, manual: dict) -> dict:
    payload = {
        "pmid": record["pmid"],
        "title": record["title"],
        "journal": record.get("journal"),
        "pub_year": record.get("pub_year"),
        "doi": record.get("doi"),
        "pmcid": record.get("pmcid"),
        "publication_types": record.get("publication_types") or [],
        "pubmed_markdown": record.get("pubmed_markdown"),
        "pubmed_xml": record.get("pubmed_xml"),
        "pmc_markdown": record.get("pmc_markdown"),
        "pmc_xml": record.get("pmc_xml"),
    }
    payload.update(manual)
    return payload


def build_program_entry(program: str, curation: dict, query: dict, record_by_pmid: dict) -> dict:
    primary = []
    supporting = []
    excluded = []

    for pmid, manual in curation["primary_pmids"].items():
        record = record_by_pmid[pmid]
        primary.append(record_payload(record, manual))

    for pmid, manual in curation["supporting_pmids"].items():
        record = record_by_pmid[pmid]
        supporting.append(record_payload(record, manual))

    for pmid, reason in curation["exclude_pmids"].items():
        record = record_by_pmid.get(pmid)
        if record:
            excluded.append(
                {
                    "pmid": pmid,
                    "title": record["title"],
                    "journal": record.get("journal"),
                    "pub_year": record.get("pub_year"),
                    "reason": reason,
                    "pubmed_markdown": record.get("pubmed_markdown"),
                }
            )
        else:
            excluded.append({"pmid": pmid, "reason": reason})

    curated_pmids = set(curation["primary_pmids"]) | set(curation["supporting_pmids"]) | set(curation["exclude_pmids"])
    unclassified_query_pmids = [pmid for pmid in query["ids"] if pmid not in curated_pmids]

    return {
        "program": program,
        "priority_class": query["priority_class"],
        "search_term": query["term"],
        "pubmed_hit_count": query["count"],
        "status": curation["status"],
        "summary": curation["summary"],
        "search_manifest": f"raw/publications/searches/{query['priority_class'].lower()}__{program}.json",
        "primary_trial_publications": primary,
        "supporting_publications": supporting,
        "excluded_or_nonprimary_hits": excluded,
        "unclassified_query_pmids": unclassified_query_pmids,
    }


def write_outputs(payload: dict):
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n")

    lines = [
        "# Curated publication priority-source inventory",
        "",
        f"- Built from: `inventories/publication_priority_sources.json`",
        "- Purpose: separate true primary trial manuscripts from reviews, background papers, and search-collision hits.",
        "- Curation rule: only promote a paper as a primary manuscript when the title/abstract clearly indicates original clinical data for the program.",
        "",
        "## Status summary",
        "",
    ]

    for status, count in payload["status_summary"].items():
        lines.append(f"- {STATUS_LABELS.get(status, status)}: {count}")

    for program in payload["programs"]:
        lines.extend(
            [
                "",
                f"## {program['program']} ({program['priority_class']})",
                "",
                f"- Search term: `{program['search_term']}`",
                f"- PubMed hits: {program['pubmed_hit_count']}",
                f"- Status: {STATUS_LABELS.get(program['status'], program['status'])}",
                f"- Summary: {program['summary']}",
            ]
        )

        if program["primary_trial_publications"]:
            lines.extend(["", "### Primary trial manuscripts", ""])
            for rec in program["primary_trial_publications"]:
                trial_ids = ", ".join(rec.get("linked_trial_ids") or []) or "NR"
                pmc = f"; PMCID {rec['pmcid']}" if rec.get("pmcid") else ""
                lines.append(
                    f"- PMID {rec['pmid']} ({rec['pub_year']}, {rec['journal']}){pmc}: **{rec['title']}**"
                )
                lines.append(f"  - Role: {rec['role']}")
                lines.append(f"  - Linked trial IDs: {trial_ids}")
                lines.append(f"  - Evidence note: {rec['evidence_note']}")
                lines.append(f"  - Cache: `{rec['pubmed_markdown']}`")
                if rec.get("pmc_markdown"):
                    lines.append(f"  - Full text cache: `{rec['pmc_markdown']}`")

        if program["supporting_publications"]:
            lines.extend(["", "### Supporting/background publications", ""])
            for rec in program["supporting_publications"]:
                lines.append(
                    f"- PMID {rec['pmid']} ({rec['pub_year']}, {rec['journal']}): **{rec['title']}**"
                )
                lines.append(f"  - Role: {rec['role']}")
                lines.append(f"  - Note: {rec['note']}")
                lines.append(f"  - Cache: `{rec['pubmed_markdown']}`")

        if program["excluded_or_nonprimary_hits"]:
            lines.extend(["", "### Explicit non-primary / excluded hits", ""])
            for rec in program["excluded_or_nonprimary_hits"]:
                title = rec.get("title", "Title not cached in program record")
                lines.append(f"- PMID {rec['pmid']}: {title}")
                lines.append(f"  - Reason: {rec['reason']}")

        if program["unclassified_query_pmids"]:
            lines.extend(["", "### Remaining query hits not manually curated yet", ""])
            lines.append("- " + ", ".join(program["unclassified_query_pmids"]))

    OUT_MD.write_text("\n".join(lines) + "\n")


def main():
    inventory = load_inventory()
    record_by_pmid, query_by_program = build_record_maps(inventory)

    programs = []
    for program, curation in MANUAL_CURATION.items():
        query = query_by_program[program]
        programs.append(build_program_entry(program, curation, query, record_by_pmid))

    payload = {
        "source_inventory": "inventories/publication_priority_sources.json",
        "programs": programs,
        "status_summary": dict(Counter(p["status"] for p in programs)),
    }
    write_outputs(payload)


if __name__ == "__main__":
    main()
