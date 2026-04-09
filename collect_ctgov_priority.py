#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

BASE = Path('/home/jordon/.openclaw/workspace/research-db/csu-cindu-db-v2')
RAW_JSON_DIR = BASE / 'raw' / 'clinicaltrials' / 'json'
RAW_MD_DIR = BASE / 'raw' / 'clinicaltrials' / 'markdown'
SEARCH_DIR = BASE / 'raw' / 'clinicaltrials' / 'searches'
INV_DIR = BASE / 'inventories'

API_BASE = 'https://clinicaltrials.gov/api/v2/studies'
FETCHED_AT = datetime.now(timezone.utc).isoformat()

SEEDS = [
    {
        'priority_class': 'BTK',
        'program': 'Remibrutinib',
        'terms': ['remibrutinib', 'LOU064'],
    },
    {
        'priority_class': 'BTK',
        'program': 'Fenebrutinib',
        'terms': ['fenebrutinib', 'GDC-0853'],
    },
    {
        'priority_class': 'BTK',
        'program': 'Rilzabrutinib',
        'terms': ['rilzabrutinib', 'PRN1008'],
    },
    {
        'priority_class': 'KIT',
        'program': 'Barzolvolimab',
        'terms': ['barzolvolimab', 'CDX-0159'],
    },
    {
        'priority_class': 'KIT',
        'program': 'Briquilimab',
        'terms': ['briquilimab', 'JSP191'],
    },
    {
        'priority_class': 'KIT',
        'program': 'BLU-808',
        'terms': ['BLU-808'],
    },
    {
        'priority_class': 'MRGPRX2',
        'program': 'EVO756',
        'terms': ['EVO756'],
    },
    {
        'priority_class': 'MRGPRX2',
        'program': 'EP262',
        'terms': ['EP262'],
    },
    {
        'priority_class': 'MRGPRX2',
        'program': 'SEP-631',
        'terms': ['SEP-631'],
    },
]


def ensure_dirs() -> None:
    for path in [RAW_JSON_DIR, RAW_MD_DIR, SEARCH_DIR, INV_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def get(url: str, **params: Any) -> requests.Response:
    r = requests.get(url, params=params or None, timeout=60)
    r.raise_for_status()
    return r


def search_term(term: str) -> dict[str, Any]:
    params = {'query.cond': 'urticaria', 'query.term': term, 'pageSize': 100}
    r = get(API_BASE, **params)
    data = r.json()
    out = {
        'term': term,
        'url': r.url,
        'fetched_at': FETCHED_AT,
        'study_count': len(data.get('studies', [])),
        'studies': [],
    }
    for study in data.get('studies', []):
        ident = study.get('protocolSection', {}).get('identificationModule', {})
        conds = study.get('protocolSection', {}).get('conditionsModule', {}).get('conditions', [])
        out['studies'].append({
            'nct_id': ident.get('nctId'),
            'brief_title': ident.get('briefTitle'),
            'official_title': ident.get('officialTitle'),
            'conditions': conds,
        })
    return out


def fetch_study(nct_id: str) -> dict[str, Any]:
    r = get(f'{API_BASE}/{nct_id}')
    data = r.json()
    data['_meta'] = {'source_url': r.url, 'fetched_at': FETCHED_AT}
    return data


def pick_program(text_blob: str, hits: list[dict[str, str]]) -> tuple[str | None, str | None]:
    lowered = text_blob.lower()
    for hit in hits:
        if hit['term'].lower() in lowered:
            return hit['program'], hit['priority_class']
    if hits:
        return hits[0]['program'], hits[0]['priority_class']
    return None, None


def simplify_study(study: dict[str, Any], seed_hits: list[dict[str, str]]) -> dict[str, Any]:
    ps = study.get('protocolSection', {})
    ident = ps.get('identificationModule', {})
    status = ps.get('statusModule', {})
    sponsor = ps.get('sponsorCollaboratorsModule', {})
    design = ps.get('designModule', {})
    arms = ps.get('armsInterventionsModule', {})
    conds = ps.get('conditionsModule', {})
    elig = ps.get('eligibilityModule', {})
    desc = ps.get('descriptionModule', {})
    contacts = ps.get('contactsLocationsModule', {})
    outcomes = ps.get('outcomesModule', {})

    intervention_names = []
    for intr in arms.get('interventions', []) or []:
        if intr.get('name'):
            intervention_names.append(intr['name'])

    title_blob = ' '.join(
        filter(
            None,
            [
                ident.get('briefTitle', ''),
                ident.get('officialTitle', ''),
                ' '.join(conds.get('conditions', []) or []),
                ' '.join(intervention_names),
            ],
        )
    )
    program, priority_class = pick_program(title_blob, seed_hits)

    arm_groups = []
    for arm in arms.get('armGroups', []) or []:
        arm_groups.append({
            'label': arm.get('label'),
            'type': arm.get('type'),
            'description': arm.get('description'),
            'intervention_names': arm.get('interventionNames', []),
        })

    primary_outcomes = []
    for out in outcomes.get('primaryOutcomes', []) or []:
        primary_outcomes.append({
            'measure': out.get('measure'),
            'time_frame': out.get('timeFrame'),
            'description': out.get('description'),
        })

    return {
        'nct_id': ident.get('nctId'),
        'brief_title': ident.get('briefTitle'),
        'official_title': ident.get('officialTitle'),
        'priority_class': priority_class,
        'program': program,
        'seed_hits': seed_hits,
        'overall_status': status.get('overallStatus'),
        'study_type': design.get('studyType'),
        'phases': design.get('phases', []),
        'conditions': conds.get('conditions', []),
        'keywords': conds.get('keywords', []),
        'brief_summary': desc.get('briefSummary'),
        'detailed_description': desc.get('detailedDescription'),
        'lead_sponsor': (sponsor.get('leadSponsor') or {}).get('name'),
        'start_date': status.get('startDateStruct', {}).get('date'),
        'primary_completion_date': status.get('primaryCompletionDateStruct', {}).get('date'),
        'completion_date': status.get('completionDateStruct', {}).get('date'),
        'enrollment': (design.get('enrollmentInfo') or {}).get('count'),
        'enrollment_type': (design.get('enrollmentInfo') or {}).get('type'),
        'allocation': design.get('designInfo', {}).get('allocation'),
        'intervention_model': design.get('designInfo', {}).get('interventionModel'),
        'primary_purpose': design.get('designInfo', {}).get('primaryPurpose'),
        'masking': (design.get('designInfo', {}).get('maskingInfo') or {}).get('masking'),
        'healthy_volunteers': elig.get('healthyVolunteers'),
        'sex': elig.get('sex'),
        'minimum_age': elig.get('minimumAge'),
        'maximum_age': elig.get('maximumAge'),
        'eligibility_criteria': elig.get('eligibilityCriteria'),
        'arm_groups': arm_groups,
        'interventions': arms.get('interventions', []),
        'primary_outcomes': primary_outcomes,
        'ctgov_url': f"https://clinicaltrials.gov/study/{ident.get('nctId')}",
        'locations_count': len(contacts.get('locations', []) or []),
    }


def md_list(items: list[str]) -> str:
    if not items:
        return '- none listed'
    return '\n'.join(f'- {item}' for item in items)


def write_markdown(summary: dict[str, Any]) -> None:
    lines = []
    lines.append(f"# {summary['nct_id']} - {summary.get('brief_title') or 'Untitled study'}")
    lines.append('')
    lines.append('## Trial identity')
    lines.append(f"- NCT ID: {summary['nct_id']}")
    lines.append(f"- Program: {summary.get('program') or 'Unmapped'}")
    lines.append(f"- Priority class: {summary.get('priority_class') or 'Unmapped'}")
    lines.append(f"- Official title: {summary.get('official_title') or 'NR'}")
    lines.append(f"- ClinicalTrials.gov URL: {summary.get('ctgov_url')}")
    lines.append('')
    lines.append('## Status and design')
    lines.append(f"- Overall status: {summary.get('overall_status') or 'NR'}")
    lines.append(f"- Study type: {summary.get('study_type') or 'NR'}")
    lines.append(f"- Phase(s): {', '.join(summary.get('phases') or []) or 'NR'}")
    lines.append(f"- Allocation: {summary.get('allocation') or 'NR'}")
    lines.append(f"- Intervention model: {summary.get('intervention_model') or 'NR'}")
    lines.append(f"- Primary purpose: {summary.get('primary_purpose') or 'NR'}")
    lines.append(f"- Masking: {summary.get('masking') or 'NR'}")
    lines.append('')
    lines.append('## Dates and enrollment')
    lines.append(f"- Start date: {summary.get('start_date') or 'NR'}")
    lines.append(f"- Primary completion date: {summary.get('primary_completion_date') or 'NR'}")
    lines.append(f"- Completion date: {summary.get('completion_date') or 'NR'}")
    lines.append(f"- Enrollment: {summary.get('enrollment') or 'NR'} ({summary.get('enrollment_type') or 'NR'})")
    lines.append('')
    lines.append('## Conditions')
    lines.append(md_list(summary.get('conditions') or []))
    lines.append('')
    lines.append('## Keywords')
    lines.append(md_list(summary.get('keywords') or []))
    lines.append('')
    lines.append('## Interventions')
    intr_lines = []
    for intr in summary.get('interventions') or []:
        intr_lines.append(f"- {intr.get('type') or 'NR'}: {intr.get('name') or 'NR'}")
    lines.append('\n'.join(intr_lines) if intr_lines else '- none listed')
    lines.append('')
    lines.append('## Arm groups')
    if summary.get('arm_groups'):
        for arm in summary['arm_groups']:
            lines.append(f"### {arm.get('label') or 'Unnamed arm'}")
            lines.append(f"- Type: {arm.get('type') or 'NR'}")
            lines.append(f"- Interventions: {', '.join(arm.get('intervention_names') or []) or 'NR'}")
            if arm.get('description'):
                lines.append(f"- Description: {arm['description']}")
            lines.append('')
    else:
        lines.append('- none listed')
        lines.append('')
    lines.append('## Primary outcomes')
    if summary.get('primary_outcomes'):
        for out in summary['primary_outcomes']:
            lines.append(f"- Measure: {out.get('measure') or 'NR'}")
            lines.append(f"  - Time frame: {out.get('time_frame') or 'NR'}")
            if out.get('description'):
                lines.append(f"  - Description: {out['description']}")
    else:
        lines.append('- none listed')
    lines.append('')
    lines.append('## Eligibility snapshot')
    lines.append(f"- Sex: {summary.get('sex') or 'NR'}")
    lines.append(f"- Minimum age: {summary.get('minimum_age') or 'NR'}")
    lines.append(f"- Maximum age: {summary.get('maximum_age') or 'NR'}")
    lines.append(f"- Healthy volunteers: {summary.get('healthy_volunteers') if summary.get('healthy_volunteers') is not None else 'NR'}")
    if summary.get('eligibility_criteria'):
        lines.append('')
        lines.append('```text')
        lines.append(summary['eligibility_criteria'].strip())
        lines.append('```')
    lines.append('')
    lines.append('## Summary text')
    if summary.get('brief_summary'):
        lines.append(summary['brief_summary'])
        lines.append('')
    if summary.get('detailed_description'):
        lines.append(summary['detailed_description'])
        lines.append('')
    lines.append('## Provenance')
    lines.append('- Source: ClinicalTrials.gov API v2')
    lines.append(f"- Fetched at: {FETCHED_AT}")
    lines.append(f"- Raw JSON: ../json/{summary['nct_id']}.json")

    (RAW_MD_DIR / f"{summary['nct_id']}.md").write_text('\n'.join(lines))


def main() -> None:
    ensure_dirs()
    search_manifest = []
    study_hits: dict[str, list[dict[str, str]]] = defaultdict(list)

    for seed in SEEDS:
        for term in seed['terms']:
            result = search_term(term)
            search_manifest.append({
                'priority_class': seed['priority_class'],
                'program': seed['program'],
                **result,
            })
            (SEARCH_DIR / f"{slugify(seed['priority_class'])}__{slugify(seed['program'])}__{slugify(term)}.json").write_text(
                json.dumps({
                    'priority_class': seed['priority_class'],
                    'program': seed['program'],
                    **result,
                }, indent=2)
            )
            for study in result['studies']:
                if study['nct_id']:
                    study_hits[study['nct_id']].append({
                        'priority_class': seed['priority_class'],
                        'program': seed['program'],
                        'term': term,
                    })

    (SEARCH_DIR / 'search_manifest.json').write_text(json.dumps(search_manifest, indent=2))

    inventory = []
    for nct_id, hits in sorted(study_hits.items()):
        raw = fetch_study(nct_id)
        (RAW_JSON_DIR / f'{nct_id}.json').write_text(json.dumps(raw, indent=2))
        summary = simplify_study(raw, hits)
        write_markdown(summary)
        inventory.append(summary)

    inventory.sort(key=lambda x: ((x.get('priority_class') or ''), (x.get('program') or ''), x['nct_id']))
    (INV_DIR / 'ctgov_priority_trials.json').write_text(json.dumps(inventory, indent=2))

    lines = []
    lines.append('# ClinicalTrials.gov priority-trial inventory')
    lines.append('')
    lines.append(f'- Built: {FETCHED_AT}')
    lines.append('- Scope: urticaria studies located from ClinicalTrials.gov API v2 using priority seeds for BTK, KIT, and MRGPRX2 programs')
    lines.append('- Important: priority class assignment is currently seed-based. It should be treated as a working bucket for raw collection, not final target verification, until each program target is rechecked from direct sponsor or publication sources.')
    lines.append('')
    lines.append('| Priority class | Program | NCT ID | Phase(s) | Status | Conditions | File |')
    lines.append('|---|---|---|---|---|---|---|')
    for item in inventory:
        lines.append(
            f"| {item.get('priority_class') or 'Unmapped'} | {item.get('program') or 'Unmapped'} | {item['nct_id']} | {'; '.join(item.get('phases') or []) or 'NR'} | {item.get('overall_status') or 'NR'} | {'; '.join(item.get('conditions') or []) or 'NR'} | [md](../raw/clinicaltrials/markdown/{item['nct_id']}.md) |"
        )
    lines.append('')
    lines.append('## Seeds with zero ClinicalTrials.gov hits in current search')
    for seed in SEEDS:
        found = any(r['program'] == seed['program'] and r['study_count'] > 0 for r in search_manifest)
        if not found:
            lines.append(f"- {seed['priority_class']} / {seed['program']} via {', '.join(seed['terms'])}")
    (INV_DIR / 'ctgov_priority_trials.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
