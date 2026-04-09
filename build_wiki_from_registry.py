from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIKI = ROOT / 'wiki'
PROGRAMS_DIR = WIKI / 'programs'
TRIALS_DIR = WIKI / 'trials'
QUERIES_DIR = WIKI / 'queries'
REGISTRY_PATH = ROOT / 'inventories' / 'source_registry.json'
CTGOV_PATH = ROOT / 'inventories' / 'ctgov_priority_trials.json'

NCT_RE = re.compile(r'NCT\d{8}', re.IGNORECASE)

CLASS_TO_MECHANISM = {
    'BTK': "Bruton's tyrosine kinase pathway program",
    'KIT': 'KIT-targeted mast-cell pathway program',
    'MRGPRX2': 'MRGPRX2-pathway program',
}
STATUS_COMPLETED = {'COMPLETED', 'TERMINATED'}
STATUS_ACTIVE = {'RECRUITING', 'ACTIVE_NOT_RECRUITING', 'ENROLLING_BY_INVITATION', 'NOT_YET_RECRUITING'}

REMI_TRIAL_OVERRIDES = {
    'NCT03926611': {
        'display_title': 'Remibrutinib Phase 2b dose-finding CSU study (NCT03926611)',
        'study_family': 'Foundational CSU efficacy program',
        'program_blurb': 'Phase 2b dose-finding core study that established rapid CSU activity reduction across multiple oral remibrutinib dose regimens.',
        'key_points': [
            'PMID 36096203 identifies this as the randomized phase 2b CSU dose-finding trial and reports 311 randomized patients across 6 remibrutinib regimens plus placebo.',
            'The manuscript reports week-4 UAS7 change from baseline ranging from -14.7 to -20.0 across active doses versus -5.4 for placebo.',
            'The saved abstract describes rapid onset of action with symptom reduction from week 1 through week 12.',
        ],
    },
    'NCT04109313': {
        'display_title': 'Remibrutinib CSU phase 2 open-label extension (NCT04109313)',
        'study_family': 'Foundational CSU extension program',
        'program_blurb': 'Open-label extension for participants rolling over from the phase 2b core study.',
        'key_points': [
            'CT.gov describes this as an open-label multicenter extension for eligible participants from CLOU064A2201.',
            'Participants with UAS7 <16 at Week 16 of the prior study could enter an observational period before treatment restart if they relapsed.',
            'Participants with persistent activity or relapse could receive open-label remibrutinib 100 mg twice daily for up to 52 weeks.',
        ],
    },
    'NCT05030311': {
        'display_title': 'REMIX-1 remibrutinib pivotal Phase 3 CSU study (NCT05030311)',
        'study_family': 'Pivotal CSU program',
        'program_blurb': 'One of the two identical REMIX pivotal Phase 3 placebo-controlled CSU studies.',
        'key_points': [
            'PMID 40043237 explicitly identifies this as REMIX-1 and reports 470 randomized patients, with 313 assigned to remibrutinib and 157 to placebo.',
            'The week-12 UAS7 least-squares mean change was -20.0 with remibrutinib versus -13.8 with placebo.',
            'PMID 41115533 reports sustained week-52 UAS7 improvement for patients originally randomized to remibrutinib and rapid improvement after placebo-to-remibrutinib transition at week 24.',
        ],
    },
    'NCT05032157': {
        'display_title': 'REMIX-2 remibrutinib pivotal Phase 3 CSU study (NCT05032157)',
        'study_family': 'Pivotal CSU program',
        'program_blurb': 'Second identical REMIX pivotal Phase 3 placebo-controlled CSU study.',
        'key_points': [
            'PMID 40043237 explicitly identifies this as REMIX-2 and reports 455 randomized patients, with 300 assigned to remibrutinib and 155 to placebo.',
            'The week-12 UAS7 least-squares mean change was -19.4 with remibrutinib versus -11.7 with placebo.',
            'PMID 41115533 reports sustained week-52 benefit and consistent long-term safety across the REMIX phase 3 program.',
        ],
    },
    'NCT05048342': {
        'display_title': 'Remibrutinib Japanese open-label Phase 3 CSU study (NCT05048342)',
        'study_family': 'Regional CSU expansion',
        'program_blurb': 'Open-label Japanese Phase 3 safety, tolerability, and efficacy study.',
        'key_points': [
            'CT.gov lists 71 actual participants in this adult Japanese CSU study.',
            'The trial is open-label and evaluates remibrutinib 25 mg twice daily over 52 weeks.',
        ],
    },
    'NCT05170724': {
        'display_title': 'Remibrutinib managed access program for CSU (NCT05170724)',
        'study_family': 'Access / post-development pathway',
        'program_blurb': 'Managed access cohort rather than a conventional randomized efficacy study.',
        'key_points': [
            'CT.gov identifies this as a managed access program cohort treatment plan for adult CSU patients.',
            'This record should be interpreted separately from the registrational efficacy studies.',
        ],
    },
    'NCT05513001': {
        'display_title': 'Remibrutinib long-term extension and randomized-withdrawal CSU study (NCT05513001)',
        'study_family': 'Lifecycle CSU extension program',
        'program_blurb': 'Phase 3 extension that includes randomized withdrawal plus long-term open-label cycles after the core pivotal studies.',
        'key_points': [
            'CT.gov lists 696 actual participants and describes a randomized-withdrawal epoch followed by repeated open-label treatment cycles.',
            'The primary endpoint is time to first composite relapse/discontinuation/confounding-medication event over 24 weeks.',
        ],
    },
    'NCT05677451': {
        'display_title': 'Remibrutinib adolescent Phase 3 CSU study (NCT05677451)',
        'study_family': 'Pediatric / adolescent expansion',
        'program_blurb': 'Adolescent placebo-controlled Phase 3 study with PK and long-term extension components.',
        'key_points': [
            'CT.gov describes 24-week double-blind placebo-controlled treatment followed by optional open-label extension and long-term treatment-free follow-up.',
            'This record explicitly includes pharmacokinetics as part of the study objectives.',
        ],
    },
    'NCT05795153': {
        'display_title': 'Remibrutinib ambulatory blood pressure monitoring Phase 3 study (NCT05795153)',
        'study_family': 'Focused safety characterization',
        'program_blurb': 'Dedicated open-label ABPM study in adult CSU participants treated with remibrutinib.',
        'key_points': [
            'CT.gov lists 144 actual participants in this 12-week ABPM study.',
            'The primary endpoint is estimated mean change in 24-hour systolic blood pressure at week 4 by ambulatory blood pressure monitoring.',
        ],
    },
    'NCT05976243': {
        'display_title': 'Remibrutinib Phase 3 CIndU basket study (NCT05976243)',
        'study_family': 'CIndU expansion program',
        'program_blurb': 'Basket study spanning symptomatic dermographism, cold urticaria, and cholinergic urticaria.',
        'key_points': [
            'CT.gov lists 362 actual participants in a 52-week randomized double-blind placebo-controlled basket study with open-label extension.',
            'Primary endpoints are subtype-specific complete-response measures at week 12 for symptomatic dermographism, cold urticaria, and cholinergic urticaria.',
            'This is the main late-stage CIndU branch currently visible in the remibrutinib raw-source layer.',
        ],
    },
    'NCT06042478': {
        'display_title': 'Remibrutinib Phase 3b omalizumab-controlled CSU study (NCT06042478)',
        'study_family': 'Comparator / positioning program',
        'program_blurb': 'Phase 3b active-control study versus omalizumab with placebo and switch arms.',
        'key_points': [
            'CT.gov lists a four-arm double-dummy design including remibrutinib, omalizumab, and two placebo-to-active transition arms.',
            'The primary endpoint is absolute change from baseline in UAS7 at week 12.',
        ],
    },
    'NCT06865651': {
        'display_title': 'Remibrutinib exploratory mixed chronic urticaria study (NCT06865651)',
        'study_family': 'Mechanistic / exploratory CU program',
        'program_blurb': 'Exploratory mixed-CU study spanning CSU and multiple CIndU phenotypes with an explicit mechanism-of-action objective.',
        'key_points': [
            'CT.gov lists this as a 12-week randomized participant- and investigator-blinded placebo-controlled exploratory study in chronic urticaria.',
            'A linked Novartis trial page is cached locally and explicitly tied to this NCT identifier.',
            'Primary outcomes include weekly most-bothersome-symptom NRS and UCT7 weekly scores at week 6.',
        ],
    },
    'NCT06868212': {
        'display_title': 'Remibrutinib versus dupilumab Phase 3b CSU study (NCT06868212)',
        'study_family': 'Comparator / positioning program',
        'program_blurb': 'US Phase 3b head-to-head early-timepoint comparison against dupilumab.',
        'key_points': [
            'CT.gov describes a double-blind double-dummy study comparing remibrutinib against dupilumab in inadequately controlled adult CSU.',
            'The primary endpoint is absolute change from baseline in UAS7 at week 4, emphasizing early efficacy differentiation.',
        ],
    },
    'NCT07358364': {
        'display_title': 'Remibrutinib real-world multi-country effectiveness study (NCT07358364)',
        'study_family': 'Real-world evidence program',
        'program_blurb': 'Prospective non-interventional post-approval effectiveness and safety study.',
        'key_points': [
            'CT.gov lists an estimated enrollment of 3280 and three real-world cohorts defined by prior treatment pathway before remibrutinib use.',
            'Primary outcomes include UCT7 and UAS7 at 12 weeks after initiating remibrutinib.',
        ],
    },
    'NCT07358780': {
        'display_title': 'Remibrutinib US real-world sub-study (NCT07358780)',
        'study_family': 'Real-world evidence program',
        'program_blurb': 'US sub-study of the broader prospective real-world remibrutinib effectiveness program.',
        'key_points': [
            'CT.gov lists an estimated enrollment of 505 and mirrors the cohort structure of the broader real-world study.',
            'Primary outcome is UAS7 at 12 weeks after treatment initiation.',
        ],
    },
    'NCT07408219': {
        'display_title': 'RELIEF remibrutinib early real-world effectiveness survey (NCT07408219)',
        'study_family': 'Real-world evidence program',
        'program_blurb': 'Early real-world comparative satisfaction/effectiveness survey against dupilumab.',
        'key_points': [
            'CT.gov identifies this as RELIEF, a real-world study in patients initiating remibrutinib or dupilumab.',
            'The primary outcome is change from baseline in UCT-7 at week 4.',
        ],
    },
}

REMI_PROGRAM_GROUPS = [
    ('Early CSU efficacy foundation', ['NCT03926611', 'NCT04109313']),
    ('Pivotal CSU program and lifecycle extension', ['NCT05030311', 'NCT05032157', 'NCT05513001', 'NCT05048342', 'NCT05795153']),
    ('Comparator, adolescent, and exploratory expansion studies', ['NCT05677451', 'NCT06042478', 'NCT06865651', 'NCT06868212']),
    ('CIndU and broader urticaria expansion', ['NCT05976243']),
    ('Access and real-world evidence layer', ['NCT05170724', 'NCT07358364', 'NCT07358780', 'NCT07408219']),
]


def load_json(path: Path):
    return json.loads(path.read_text())


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or 'item'


def pretty_phase(phases: list[str] | None) -> str:
    if not phases:
        return 'NR'
    return ', '.join(p.replace('PHASE', 'Phase ') for p in phases)


def title_from_trial(rec: dict) -> str:
    return rec.get('brief_title') or rec.get('official_title') or rec['nct_id']


def trial_display_title(program_key: str, rec: dict) -> str:
    if program_key == 'remibrutinib' and rec.get('nct_id') in REMI_TRIAL_OVERRIDES:
        return REMI_TRIAL_OVERRIDES[rec['nct_id']]['display_title']
    return title_from_trial(rec)


def remi_override(trial_id: str) -> dict:
    return REMI_TRIAL_OVERRIDES.get(trial_id, {})


def infer_sponsor(program_entry: dict) -> str:
    sponsors = []
    sponsors.extend([t.get('lead_sponsor') for t in program_entry.get('ctgov_trials', []) if t.get('lead_sponsor')])
    sponsors.extend([s.get('sponsor') for s in program_entry.get('sponsor_artifacts', []) if s.get('sponsor')])
    if not sponsors:
        return 'NR'
    return Counter(sponsors).most_common(1)[0][0]


def infer_indications(program_entry: dict) -> list[str]:
    seen = []
    seen_set = set()
    for trial in program_entry.get('ctgov_trials', []):
        for cond in trial.get('conditions', []):
            if cond not in seen_set:
                seen.append(cond)
                seen_set.add(cond)
    return seen


def infer_program_focus(program_entry: dict) -> str:
    statuses = {t.get('status') for t in program_entry.get('ctgov_trials', [])}
    if any(s in STATUS_ACTIVE for s in statuses):
        return 'Active clinical development represented in current raw-source layer'
    if any(s in STATUS_COMPLETED for s in statuses):
        return 'Completed or historical urticaria development represented in current raw-source layer'
    return 'Program tracked in current raw-source layer'


def existing_trial_slug_map() -> dict[str, str]:
    mapping = {}
    for path in TRIALS_DIR.glob('*.md'):
        text = path.read_text(errors='ignore')
        match = NCT_RE.search(text)
        if match:
            mapping[match.group(0).upper()] = path.name
    return mapping


def existing_program_slug_map() -> dict[str, str]:
    return {path.stem.lower(): path.name for path in PROGRAMS_DIR.glob('*.md')}


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n')


def program_frontmatter(program_entry: dict, sponsor: str, indications: list[str]) -> str:
    tags = [f"class/{c.lower()}" for c in program_entry.get('priority_classes', [])]
    tags.append('type/program')
    lines = [
        '---',
        f"title: {program_entry['display_name']}",
        f"program_key: {program_entry['program_key']}",
        f"sponsor: {json.dumps(sponsor)}",
        'tags:',
    ]
    for tag in tags:
        lines.append(f'  - {tag}')
    if indications:
        lines.append('indications:')
        for item in indications:
            lines.append(f'  - {json.dumps(item)}')
    lines.append('---')
    return '\n'.join(lines)


def trial_frontmatter(ct: dict, program_key: str) -> str:
    tags = ['type/trial', f'program/{program_key}']
    for phase in ct.get('phases') or []:
        tags.append(f"phase/{phase.lower()}")
    override = remi_override(ct['nct_id']) if program_key == 'remibrutinib' else {}
    lines = [
        '---',
        f"title: {json.dumps(trial_display_title(program_key, ct))}",
        f"trial_id: {ct['nct_id']}",
        f"program_key: {program_key}",
        f"status: {ct.get('overall_status', 'NR')}",
    ]
    if override.get('study_family'):
        lines.append(f"study_family: {json.dumps(override['study_family'])}")
    lines.extend([
        'tags:',
    ])
    for tag in tags:
        lines.append(f'  - {tag}')
    lines.append('---')
    return '\n'.join(lines)


def trial_link_name(program_key: str, trial_id: str, trial_slug_map: dict[str, str]) -> str:
    if trial_id in trial_slug_map:
        return trial_slug_map[trial_id]
    return f"{slugify(program_key)}-{trial_id.lower()}.md"


def build_remibrutinib_program_page(program_entry: dict, trial_slug_map: dict[str, str]) -> str:
    sponsor = infer_sponsor(program_entry)
    indications = infer_indications(program_entry)
    trial_by_id = {t['trial_id']: t for t in program_entry.get('ctgov_trials', [])}
    lines = [
        program_frontmatter(program_entry, sponsor, indications),
        '# Remibrutinib',
        '',
        '## Overview',
        '- Priority class: BTK',
        "- Mechanistic bucket: Bruton's tyrosine kinase pathway program",
        f'- Sponsor: {sponsor}',
        '- Alias(es): LOU064',
        '- Development shape in the current raw-source layer: foundational phase 2b CSU dose-finding, pivotal REMIX phase 3 CSU program, extension/lifecycle studies, late-stage CIndU expansion, comparator studies, and real-world follow-up.',
        '',
        '## Program map',
        '',
    ]
    for group_title, ids in REMI_PROGRAM_GROUPS:
        lines.append(f'### {group_title}')
        for trial_id in ids:
            trial = trial_by_id.get(trial_id)
            if not trial:
                continue
            link_name = trial_link_name(program_entry['program_key'], trial_id, trial_slug_map)
            override = remi_override(trial_id)
            status = trial.get('status', 'NR')
            phase = pretty_phase(trial.get('phase'))
            conds = ', '.join(trial.get('conditions', [])) or 'NR'
            lines.append(f"- [{trial_id}](../trials/{link_name}) - {phase}; {status}; {conds}")
            if override.get('program_blurb'):
                lines.append(f"  - {override['program_blurb']}")
        lines.append('')

    lines.extend([
        '## Evidence summary',
        '- Primary manuscript layer is strongest for the CSU efficacy chain: phase 2b core (PMID 36096203), phase 2b extension follow-up (PMID 37866460), REMIX phase 3 core results (PMID 40043237), and 52-week REMIX follow-up (PMID 41115533).',
        '- The REMIX papers directly support the pivotal phase 3 pair `NCT05030311` and `NCT05032157`, including trial names REMIX-1 and REMIX-2, randomized sample sizes, and week-12 plus week-52 efficacy framing.',
        '- The raw-source layer also shows remibrutinib extending beyond classical adult CSU registrational studies into adolescent, CIndU, active-comparator, managed-access, and real-world evidence records.',
        '',
        '## Inventory counts',
        f"- CT.gov trials in registry: {len(program_entry.get('ctgov_trials', []))}",
        f"- Sponsor artifacts in registry: {len(program_entry.get('sponsor_artifacts', []))}",
        f"- Primary publications in registry: {len(program_entry.get('primary_publications', []))}",
        f"- Supporting publications in registry: {len(program_entry.get('supporting_publications', []))}",
        '',
        '## Primary publications',
        '',
    ])
    for pub in program_entry.get('primary_publications', []):
        links = ', '.join(pub.get('linked_trial_ids') or []) or 'NR'
        lines.append(f"- PMID {pub['pmid']} ({pub.get('pub_year', 'NR')}, {pub.get('journal', 'NR')}): **{pub['title']}**")
        lines.append(f"  - Role: {pub.get('role', 'NR')}")
        lines.append(f"  - Linked trial IDs: {links}")
        lines.append(f"  - Local cache: `{pub.get('pubmed_markdown')}`")

    lines.extend(['', '## Sponsor-source layer', ''])
    for item in program_entry.get('sponsor_artifacts', []):
        lines.append(f"- {item['label']} ({item.get('sponsor', 'NR')})")
        for saved in item.get('saved_files', []):
            lines.append(f"  - `{saved}`")

    lines.extend([
        '',
        '## Interpretation',
        '- Verified facts: remibrutinib is no longer represented here as a single flagship page. The current derived layer now exposes the broader study stack spanning early CSU, pivotal CSU, CIndU, comparator, and real-world records.',
        '- Interpretation: remibrutinib is currently the deepest BTK urticaria program in the local evidence stack because it combines dense CT.gov coverage with explicit manuscript linkage for the core CSU efficacy package.',
        '- Open questions:',
        '  - Some remibrutinib records are lifecycle, managed-access, or real-world studies rather than classic interventional efficacy trials, so program-level summaries should keep those categories separate.',
        '  - Several sponsor press releases remain program-level artifacts because the cached metadata did not capture explicit trial IDs, even when the topic clearly belongs to the remibrutinib program.',
        '  - Additional manual enrichment is still needed if we want every remibrutinib study page to carry outcome-level or arm-level detail beyond the conservative CT.gov/manuscript layer.',
        '',
        '## Provenance',
        '- Primary source(s):',
        '  - `../inventories/source_registry.json`',
        '  - `../inventories/source_registry.md`',
        '- Supporting source(s):',
        '  - `../inventories/ctgov_priority_trials.json`',
        '  - `../inventories/publication_priority_curation.json`',
        '  - `../inventories/sponsor_priority_sources.json`',
        '- Last verified: 2026-04-08',
        '- Verification status: Partial',
        '',
        '## Change Log',
        '- 2026-04-08: Rebuilt the remibrutinib program page with study-family grouping and explicit linkage across the broader remibrutinib trial stack.',
    ])
    return '\n'.join(lines)


def build_program_page(program_entry: dict, trial_slug_map: dict[str, str]) -> str:
    if program_entry['program_key'] == 'remibrutinib':
        return build_remibrutinib_program_page(program_entry, trial_slug_map)
    sponsor = infer_sponsor(program_entry)
    indications = infer_indications(program_entry)
    mechanism = ', '.join(CLASS_TO_MECHANISM.get(c, c) for c in program_entry.get('priority_classes', [])) or 'NR'
    completed = []
    active = []
    other = []
    for trial in program_entry.get('ctgov_trials', []):
        item = (trial, trial_link_name(program_entry['program_key'], trial['trial_id'], trial_slug_map))
        status = trial.get('status')
        if status in STATUS_COMPLETED:
            completed.append(item)
        elif status in STATUS_ACTIVE:
            active.append(item)
        else:
            other.append(item)

    lines = [
        program_frontmatter(program_entry, sponsor, indications),
        f"# {program_entry['display_name']}",
        '',
        '## Overview',
        f"- Priority class: {', '.join(program_entry.get('priority_classes', [])) or 'NR'}",
        f"- Mechanistic bucket: {mechanism}",
        f"- Sponsor: {sponsor}",
        f"- Development focus: {infer_program_focus(program_entry)}",
        f"- Indications represented in current raw sources: {', '.join(indications) if indications else 'NR'}",
        '',
        '## Study Inventory',
        '',
    ]

    def add_group(title: str, items: list[tuple[dict, str]]):
        lines.append(f"### {title}")
        if not items:
            lines.append('- None in current registry')
            lines.append('')
            return
        for trial, link_name in items:
            conds = ', '.join(trial.get('conditions', [])) or 'NR'
            lines.append(
                f"- [{trial['trial_id']}](../trials/{link_name}) - {pretty_phase(trial.get('phase'))}; {trial.get('status', 'NR')}; {conds}"
            )
        lines.append('')

    add_group('Completed / historical studies', completed)
    add_group('Active / recruiting studies', active)
    add_group('Other registry entries', other)

    lines.extend([
        '## Evidence Coverage',
        f"- CT.gov trials in registry: {len(program_entry.get('ctgov_trials', []))}",
        f"- Sponsor artifacts in registry: {len(program_entry.get('sponsor_artifacts', []))}",
        f"- Primary publications in registry: {len(program_entry.get('primary_publications', []))}",
        f"- Supporting publications in registry: {len(program_entry.get('supporting_publications', []))}",
    ])
    if program_entry.get('publication_status'):
        lines.append(f"- Publication status: {program_entry['publication_status']}")
    if program_entry.get('publication_summary'):
        lines.append(f"- Publication summary: {program_entry['publication_summary']}")

    lines.extend(['', '## Primary publications', ''])
    if program_entry.get('primary_publications'):
        for pub in program_entry['primary_publications']:
            links = ', '.join(pub.get('linked_trial_ids') or []) or 'NR'
            lines.append(f"- PMID {pub['pmid']} ({pub.get('pub_year', 'NR')}, {pub.get('journal', 'NR')}): **{pub['title']}**")
            lines.append(f"  - Role: {pub.get('role', 'NR')}")
            lines.append(f"  - Linked trial IDs: {links}")
            lines.append(f"  - Local cache: `{pub.get('pubmed_markdown')}`")
    else:
        lines.append('- No primary publications currently linked in the registry')

    lines.extend(['', '## Supporting evidence', ''])
    if program_entry.get('supporting_publications'):
        for pub in program_entry['supporting_publications']:
            lines.append(f"- PMID {pub['pmid']}: {pub['title']} (`{pub.get('pubmed_markdown')}`)")
    else:
        lines.append('- No supporting publications currently listed')
    if program_entry.get('sponsor_artifacts'):
        for item in program_entry['sponsor_artifacts']:
            lines.append(f"- Sponsor artifact: {item['label']} ({item.get('sponsor', 'NR')})")
            for saved in item.get('saved_files', []):
                lines.append(f"  - `{saved}`")

    lines.extend(['', '## Interpretation', ''])
    lines.append(f"- Verified facts: the current v2 registry tracks {len(program_entry.get('ctgov_trials', []))} CT.gov entries for this program and links them conservatively to sponsor and publication evidence where explicit identifiers are available.")
    if program_entry.get('primary_publications'):
        lines.append('- Interpretation: this program already has enough linked manuscript or registry support for a source-first derived program page, but individual study pages should still be reviewed and enriched over time.')
    else:
        lines.append('- Interpretation: this program is currently supported mainly by CT.gov and/or sponsor-source evidence, with weaker direct manuscript coverage in the local cache.')
    open_questions = []
    if program_entry.get('unclassified_query_pmids'):
        open_questions.append(f"Unclassified publication PMIDs remain in the search set: {', '.join(program_entry['unclassified_query_pmids'])}")
    if any(not item.get('explicit_trial_ids') for item in program_entry.get('sponsor_artifacts', [])):
        open_questions.append('Several sponsor artifacts remain program-level because no explicit study identifier was captured in cached metadata.')
    if not open_questions:
        open_questions.append('Further enrichment should focus on study-level endpoint, arm-size, and manuscript-to-trial linkage refinement.')
    lines.append('- Open questions:')
    for item in open_questions:
        lines.append(f'  - {item}')

    lines.extend([
        '',
        '## Provenance',
        '- Primary source(s):',
        '  - `../inventories/source_registry.json`',
        '  - `../inventories/source_registry.md`',
        '- Supporting source(s):',
        '  - `../inventories/ctgov_priority_trials.json`',
        '  - `../inventories/publication_priority_curation.json`',
        '  - `../inventories/sponsor_priority_sources.json`',
        '- Last verified: 2026-04-08',
        '- Verification status: Partial',
        '',
        '## Change Log',
        '- 2026-04-08: Generated or refreshed this program page from the v2 source registry and local source caches.',
    ])
    return '\n'.join(lines)


def summarize_cp_findings(ct: dict, trial_registry_entry: dict) -> list[str]:
    findings = []
    summary_blob = ' '.join(filter(None, [ct.get('brief_summary'), ct.get('detailed_description')])).lower()
    if 'pharmacokinetic' in summary_blob or 'pharmacokinetics' in summary_blob:
        findings.append('- PK: ClinicalTrials.gov summary text indicates pharmacokinetics were part of the study objectives or assessments.')
    else:
        findings.append('- PK: Not clearly summarized in the currently linked local source snippets.')
    if 'pharmacodynamic' in summary_blob or 'pharmacodynamics' in summary_blob:
        findings.append('- PD: ClinicalTrials.gov summary text indicates pharmacodynamics were part of the study objectives or assessments.')
    else:
        findings.append('- PD: Not clearly summarized in the currently linked local source snippets.')
    if trial_registry_entry.get('primary_publications'):
        pubs = '; '.join(f"PMID {p['pmid']}" for p in trial_registry_entry['primary_publications'])
        findings.append(f'- Linked manuscripts: Primary publication support is available in the registry ({pubs}).')
    else:
        findings.append('- Linked manuscripts: No trial-level primary publication is explicitly linked in the current registry.')
    return findings


def build_trial_page(program_entry: dict, ct: dict, trial_registry_entry: dict) -> str:
    title = trial_display_title(program_entry['program_key'], ct)
    override = remi_override(ct['nct_id']) if program_entry['program_key'] == 'remibrutinib' else {}
    lines = [
        trial_frontmatter(ct, program_entry['program_key']),
        f"# {title}",
        '',
        '## Study Snapshot',
        f"- Program: {program_entry['display_name']}",
        f"- Study ID(s): {ct['nct_id']}",
        f"- Phase: {pretty_phase(ct.get('phases'))}",
        f"- Indication: {', '.join(ct.get('conditions', [])) if ct.get('conditions') else 'NR'}",
        f"- Status: {ct.get('overall_status', 'NR').replace('_', ' ').title()}",
        f"- Sponsor: {ct.get('lead_sponsor', 'NR')}",
    ]
    if override.get('study_family'):
        lines.append(f"- Study family: {override['study_family']}")
    lines.extend([
        '',
        '## Design',
        f"- Study type: {ct.get('study_type', 'NR')}",
        f"- Randomization / allocation: {ct.get('allocation', 'NR')}",
        f"- Intervention model: {ct.get('intervention_model', 'NR')}",
        f"- Masking: {ct.get('masking', 'NR')}",
        f"- Primary purpose: {ct.get('primary_purpose', 'NR')}",
        f"- Enrollment: {ct.get('enrollment', 'NR')} ({ct.get('enrollment_type', 'NR')})",
        '',
        '## Population',
        f"- Conditions: {', '.join(ct.get('conditions', [])) if ct.get('conditions') else 'NR'}",
        f"- Sex: {ct.get('sex', 'NR')}",
        f"- Age range: {ct.get('minimum_age', 'NR')} to {ct.get('maximum_age', 'NR')}",
        f"- Healthy volunteers: {ct.get('healthy_volunteers', 'NR')}",
    ])
    if ct.get('brief_summary'):
        lines.append(f"- Summary: {ct['brief_summary']}")

    lines.extend(['', '## Arms', '| Arm | Type | Description | N | Evidence status |', '|---|---|---|---:|---|'])
    if ct.get('arm_groups'):
        for arm in ct['arm_groups']:
            desc = (arm.get('description') or 'NR').replace('\n', ' ')
            label = arm.get('label', 'NR').replace('|', '\\|')
            atype = (arm.get('type') or 'NR').replace('|', '\\|')
            desc = desc.replace('|', '\\|')
            lines.append(f"| {label} | {atype} | {desc} | NR | Per-arm realized N not directly captured in current CT.gov inventory export |")
    else:
        lines.append('| NR | NR | No arm-group details parsed into current inventory | NR | NR |')

    if override.get('key_points'):
        lines.extend(['', '## Key source-backed points'])
        for item in override['key_points']:
            lines.append(f'- {item}')

    lines.extend(['', '## Endpoints'])
    if ct.get('primary_outcomes'):
        lines.append('- Primary outcomes:')
        for outcome in ct['primary_outcomes'][:8]:
            measure = outcome.get('measure', 'NR')
            timeframe = outcome.get('time_frame') or outcome.get('timeframe') or 'NR'
            lines.append(f"  - {measure} (time frame: {timeframe})")
    else:
        lines.append('- Primary outcomes: NR')

    lines.extend(['', '## Clinical Pharmacology Findings'])
    lines.extend(summarize_cp_findings(ct, trial_registry_entry))

    lines.extend(['', '## Safety Findings'])
    if trial_registry_entry.get('primary_publications'):
        lines.append('- Safety details should be reviewed in the linked primary publication(s) for fuller interpretation beyond the CT.gov inventory layer.')
    else:
        lines.append('- Safety detail is not strongly enriched beyond the current CT.gov/source-registry layer.')

    lines.extend(['', '## Linked Evidence'])
    lines.append(f"- CT.gov page: {ct.get('ctgov_url', 'NR')}")
    lines.append(f"- Local CT.gov cache: `{trial_registry_entry['ctgov_record']['local_markdown'] if trial_registry_entry.get('ctgov_record') else 'NR'}`")
    if trial_registry_entry.get('primary_publications'):
        lines.append('- Primary publications:')
        for pub in trial_registry_entry['primary_publications']:
            lines.append(f"  - PMID {pub['pmid']}: {pub['title']} (`../{pub['pubmed_markdown']}`)")
    if trial_registry_entry.get('supporting_publications'):
        lines.append('- Supporting publications:')
        for pub in trial_registry_entry['supporting_publications']:
            lines.append(f"  - PMID {pub['pmid']}: {pub['title']} (`../{pub['pubmed_markdown']}`)")
    if trial_registry_entry.get('sponsor_artifacts'):
        lines.append('- Sponsor artifacts linked by explicit identifier:')
        for item in trial_registry_entry['sponsor_artifacts']:
            lines.append(f"  - {item['label']} ({item.get('sponsor', 'NR')})")
            for saved in item.get('saved_files', []):
                lines.append(f"    - `{saved}`")

    lines.extend(['', '## Interpretation'])
    lines.append('- Verified facts: this page reflects the current local registry and CT.gov inventory export without inferring unsupported arm sizes or endpoint results.')
    if trial_registry_entry.get('primary_publications'):
        lines.append('- Interpretation: this trial already has direct manuscript support in the local source layer and should be a higher-priority candidate for manual enrichment.')
    else:
        lines.append('- Interpretation: this trial is currently represented mainly by CT.gov and any linked sponsor-source artifacts; manual enrichment is still needed for a richer narrative page.')
    lines.append('- Open questions:')
    lines.append('  - Per-arm realized N values are not promoted unless directly stated in the current local source layer.')
    if not trial_registry_entry.get('primary_publications'):
        lines.append('  - No explicit trial-level primary manuscript is currently linked in the registry.')
    if not trial_registry_entry.get('sponsor_artifacts'):
        lines.append('  - No sponsor artifact is explicitly linked to this trial by identifier in the current registry.')

    lines.extend([
        '',
        '## Provenance',
        '- Source type: ClinicalTrials.gov inventory with linked sponsor/publication registry where available',
        '- Primary source(s):',
        f"  - {ct['nct_id']}",
        f"  - `../{trial_registry_entry['ctgov_record']['local_markdown'] if trial_registry_entry.get('ctgov_record') else ''}`",
        '  - `../inventories/source_registry.json`',
        '- Supporting source(s):',
        '  - `../inventories/ctgov_priority_trials.json`',
        '- Last verified: 2026-04-08',
        '- Verification status: Partial',
        '',
        '## Change Log',
        '- 2026-04-08: Generated or refreshed this study page from the v2 source registry and CT.gov inventory.',
    ])
    return '\n'.join(lines)


def build_query_pages(registry: dict, trial_slug_map: dict[str, str]):
    programs = registry['programs']
    lines = [
        '---',
        'title: Program and trial catalog',
        'tags:',
        '  - type/query',
        '---',
        '# Program and trial catalog',
        '',
        f"- Programs in current derived layer: {len(programs)}",
        f"- CT.gov trials in current registry: {sum(len(p.get('ctgov_trials', [])) for p in programs)}",
        '',
        '| Program | Class | Trials | Primary pubs | Program page |',
        '|---|---|---:|---:|---|',
    ]
    for program in programs:
        lines.append(
            f"| {program['display_name']} | {', '.join(program.get('priority_classes', [])) or 'NR'} | {len(program.get('ctgov_trials', []))} | {len(program.get('primary_publications', []))} | [page](../programs/{program['program_key']}.md) |"
        )
    lines.extend(['', '## Trial links', ''])
    for program in programs:
        lines.append(f"### {program['display_name']}")
        if not program.get('ctgov_trials'):
            lines.append('- No CT.gov-linked trials in current registry')
            lines.append('')
            continue
        for trial in program['ctgov_trials']:
            link_name = trial_link_name(program['program_key'], trial['trial_id'], trial_slug_map)
            title = trial_display_title(
                program['program_key'],
                {
                    'nct_id': trial['trial_id'],
                    'brief_title': trial.get('brief_title'),
                    'official_title': trial.get('official_title'),
                },
            )
            lines.append(f"- [{trial['trial_id']}](../trials/{link_name}) - {title}")
        lines.append('')
    write_text(QUERIES_DIR / 'catalog.md', '\n'.join(lines))


def main():
    registry = load_json(REGISTRY_PATH)
    ctgov_records = load_json(CTGOV_PATH)
    ct_by_nct = {rec['nct_id']: rec for rec in ctgov_records}
    trial_slug_map = existing_trial_slug_map()
    program_slug_map = existing_program_slug_map()

    generated_program_files = set()
    generated_trial_files = set()

    for program in registry['programs']:
        program_filename = program_slug_map.get(program['program_key'], f"{program['program_key']}.md")
        generated_program_files.add(program_filename)
        write_text(PROGRAMS_DIR / program_filename, build_program_page(program, trial_slug_map))

        trial_registry_by_id = {item['trial_id']: item for item in program.get('trial_registry', [])}
        for trial in program.get('ctgov_trials', []):
            ct = ct_by_nct[trial['trial_id']]
            trial_filename = trial_link_name(program['program_key'], trial['trial_id'], trial_slug_map)
            generated_trial_files.add(trial_filename)
            write_text(TRIALS_DIR / trial_filename, build_trial_page(program, ct, trial_registry_by_id[trial['trial_id']]))

    for path in PROGRAMS_DIR.glob('*.md'):
        if path.name not in generated_program_files and path.name != '.gitkeep':
            path.unlink()
    for path in TRIALS_DIR.glob('*.md'):
        if path.name not in generated_trial_files and path.name != '.gitkeep':
            path.unlink()

    build_query_pages(registry, trial_slug_map)
    print(f"Generated {len(generated_program_files)} program pages and {len(generated_trial_files)} trial pages")


if __name__ == '__main__':
    main()
