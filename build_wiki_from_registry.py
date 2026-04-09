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
CTGOV_BY_NCT: dict[str, dict] = {}

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

TRIAL_OPERATIONAL_OVERRIDES = {
    'NCT03926611': {
        'active_dose_levels_count': 6,
        'design_summary': '7-arm dose-finding study with 6 active oral remibrutinib regimens plus placebo.',
        'per_arm_summary': 'ClinicalTrials.gov results-section denominators support randomized group sizes of 44 (Arm 1), 44 (Arm 2), 47 (Arm 3), 44 (Arm 4), 44 (Arm 5), 45 (Arm 6), and 43 (placebo), totaling 311 participants.',
        'arm_sizes': {
            'LOU064 Arm 1': '44',
            'LOU064 Arm 2': '44',
            'LOU064 Arm 3': '47',
            'LOU064 Arm 4': '44',
            'LOU064 Arm 5': '44',
            'LOU064 Arm 6': '45',
            'Placebo Arm': '43',
        },
        'source_note': 'ClinicalTrials.gov API v2 resultsSection participant flow and baseline-characteristics denominators, plus PMID 36096203 abstract.',
    },
    'NCT05030311': {
        'active_dose_levels_count': 1,
        'design_summary': '2-arm placebo-controlled pivotal REMIX-1 study with remibrutinib 25 mg twice daily versus placebo.',
        'per_arm_summary': '313 remibrutinib, 157 placebo.',
        'arm_sizes': {
            'LOU064 25mg b.i.d.': '313',
            'Placebo': '157',
        },
        'source_note': 'PMID 40043237 abstract.',
    },
    'NCT05032157': {
        'active_dose_levels_count': 1,
        'design_summary': '2-arm placebo-controlled pivotal REMIX-2 study with remibrutinib 25 mg twice daily versus placebo.',
        'per_arm_summary': '300 remibrutinib, 155 placebo.',
        'arm_sizes': {
            'LOU064 25mg b.i.d.': '300',
            'Placebo': '155',
        },
        'source_note': 'PMID 40043237 abstract.',
    },
    'NCT05170724': {
        'design_summary': 'Managed access cohort rather than a conventional randomized efficacy trial.',
        'per_arm_summary': 'The current CT.gov export does not provide a structured arm table or enrollment target for this managed-access record.',
        'source_note': 'ClinicalTrials.gov record metadata.',
    },
    'NCT04538794': {
        'active_dose_levels_count': 4,
        'design_summary': 'Sequential 4-cohort phase 1b IV multiple-ascending-dose study with pooled placebo control.',
        'per_arm_summary': '45 randomized total, with 35 barzolvolimab-treated and 10 placebo-treated overall; publication abstract also lists four dose cohorts (0.5 mg/kg Q4W, 1.5 mg/kg Q4W, 3 mg/kg Q8W, 4.5 mg/kg Q8W).',
        'arm_sizes': {
            'CDX-0159': '35',
            'Normal Saline': '10',
        },
        'source_note': 'PMID 40415544 abstract plus PMCID PMC12368744 full text.',
    },
    'NCT04548869': {
        'active_dose_levels_count': 1,
        'design_summary': 'Single-dose open-label CIndU study using one active barzolvolimab regimen.',
        'per_arm_summary': 'ClinicalTrials.gov arm description states planned enrollment of 20 Cold Contact Urticaria, 10 Symptomatic Dermographism, and 10 Cholinergic Urticaria patients; CT.gov lists 41 actual participants overall.',
        'source_note': 'ClinicalTrials.gov markdown arm description.',
    },
    'NCT05368285': {
        'active_dose_levels_count': 3,
        'design_summary': 'Placebo-controlled 16-week core with three active barzolvolimab dose regimens, followed by re-randomized active extension reflected in the 6 CT.gov arm groups.',
        'per_arm_summary': 'Publication abstract supports placebo-controlled core randomization of 75 mg Q4W (n=53), 150 mg Q4W (n=52), 300 mg Q8W (n=51), and placebo (n=51). The currently generated 52-week CT.gov labels only map cleanly to the sustained 150 mg and 300 mg arms; the re-randomized 75 mg and placebo extension arms remain unresolved at exact row level in the current local evidence layer.',
        'arm_sizes': {
            'barzolvolimab 150 mg': '52',
            'barzolvolimab 300 mg': '51',
        },
        'source_note': 'PMID 41747871 abstract.',
    },
    'NCT05405660': {
        'active_dose_levels_count': 2,
        'design_summary': 'Phase 2 randomized dose-finding CIndU study run as two parallel 3-arm strata, one in ColdU and one in symptomatic dermographism.',
        'per_arm_summary': 'ACAAI poster text supports ColdU n=96 split as 150 mg Q4W n=32, 300 mg Q8W n=32, placebo n=32, and symptomatic dermographism n=97 split as 150 mg Q4W n=33, 300 mg Q8W n=33, placebo n=31.',
        'arm_sizes': {
            'barzolvolimab 150 mg in patients with Symptomatic Dermographism': '33',
            'barzolvolimab 300 mg in patients with Symptomatic Dermographism': '33',
            'Placebo Comparator in patients with Symptomatic Dermographism': '31',
            'barzolvolimab 150 mg in patients with Chronic Inducible Cold Urticaria': '32',
            'barzolvolimab 300 mg in patients with Chronic Inducible Cold Urticaria': '32',
            'Placebo Comparator in patients with Chronic Inducible Cold Urticaria': '32',
        },
        'source_note': 'Celldex Phase 2 CIndU ACAAI poster text cached locally.',
    },
    'NCT03137069': {
        'active_dose_levels_count': 3,
        'design_summary': 'Pilot plus dose-ranging fenebrutinib phase 2 study with separate cohort 1 and cohort 2 structures.',
        'per_arm_summary': 'ClinicalTrials.gov results-section denominators support cohort 1 placebo n=13 and fenebrutinib 200 mg BID n=28, plus cohort 2 placebo n=23, fenebrutinib 50 mg daily n=23, 150 mg daily n=24, and 200 mg twice daily n=23, totaling 134 participants.',
        'arm_sizes': {
            'Cohort 1: Placebo': '13',
            'Cohort 1: GDC-0853 200mg BID': '28',
            'Cohort 2: Placebo': '23',
            'Cohort 2: GDC-0853 50mg QD': '23',
            'Cohort 2: GDC-0853 150mg QD': '24',
            'Cohort 2: GDC-0853 200mg BID': '23',
        },
        'source_note': 'ClinicalTrials.gov API v2 resultsSection participant flow and baseline-characteristics denominators; PMCID PMC8604722 full text remains the linked manuscript source.',
    },
    'NCT03693625': {
        'active_dose_levels_count': 1,
        'design_summary': 'Open-label fenebrutinib extension study that re-treated participants according to parent-study assignment in cohort 2 of GS39684.',
        'per_arm_summary': 'ClinicalTrials.gov results-section denominators support parent-study GDC-0853 n=23 and parent-study placebo n=8, totaling 31 participants.',
        'arm_sizes': {
            'Parent Study: GDC-0853': '23',
            'Parent Study: Placebo': '8',
        },
        'source_note': 'ClinicalTrials.gov API v2 resultsSection participant flow and baseline-characteristics denominators.',
    },
    'NCT05107115': {
        'active_dose_levels_count': 3,
        'design_summary': '4-arm phase 2 dose-ranging study with three oral rilzabrutinib regimens plus placebo.',
        'per_arm_summary': 'PMCID full text directly supports randomized sizes of 400 mg/d n=38, 800 mg/d n=41, 1200 mg/d n=41, and placebo n=40 overall; it also reports primary-analysis sample sizes of placebo n=36, 400 mg/d n=37, 800 mg/d n=35, and 1200 mg/d n=35.',
        'arm_sizes': {
            'Rilzabrutinib dose A': '38',
            'Rilzabrutinib dose B': '41',
            'Rilzabrutinib dose C': '41',
            'Placebo': '40',
        },
        'arm_regimens': {
            'Rilzabrutinib dose A': {'dose': '400 mg', 'frequency': 'QPM', 'route': 'Oral'},
            'Rilzabrutinib dose B': {'dose': '400 mg', 'frequency': 'BID', 'route': 'Oral'},
            'Rilzabrutinib dose C': {'dose': '400 mg', 'frequency': 'TID', 'route': 'Oral'},
            'Placebo': {'dose': 'NR', 'frequency': 'Matched oral placebo', 'route': 'Oral'},
        },
        'source_note': 'PMID 40266575 abstract plus PMCID PMC12019677 full text; CT.gov dose A/B/C rows are mapped to the publication regimen order (400 mg QPM, 400 mg BID, 400 mg TID).',
    },
    'NCT06077773': {
        'active_dose_levels_count': 3,
        'design_summary': 'Terminated phase 2 CSU study with placebo, EP262 50 mg, and EP262 150 mg enrolled in Part 1; CT.gov still lists a planned EP262 25 mg arm not carried into the posted results groups.',
        'per_arm_summary': 'ClinicalTrials.gov results-section denominators support placebo n=38, EP262 50 mg n=37, and EP262 150 mg n=38, totaling 113 participants. The posted results note that Part 2 was not enrolled, so the listed EP262 25 mg row remains unresolved in the current local layer.',
        'arm_sizes': {
            'Placebo': '38',
            'EP262 50 mg': '37',
            'EP262 150 mg': '38',
        },
        'source_note': 'ClinicalTrials.gov API v2 resultsSection participant flow and baseline-characteristics denominators.',
    },
    'NCT06865651': {
        'active_dose_levels_count': 2,
        'design_summary': 'Exploratory parallel-group mixed-CU study with separate remibrutinib/placebo comparisons in CIndU and CSU strata.',
        'per_arm_summary': 'Novartis trial-page text plus CT.gov support approximately 44 total participants across 4 listed arms and notes the study will attempt to enroll approximately 4 to 5 participants for each included chronic urticaria subtype; exact arm-specific counts are not explicitly stated in the current saved source text.',
        'source_note': 'CT.gov plus cached Novartis trial page NCT06865651.',
    },
    'NCT06873516': {
        'active_dose_levels_count': 3,
        'design_summary': 'Global randomized, double-blind, placebo-controlled phase 2b CSU dose-ranging study of oral EVO756.',
        'per_arm_summary': 'Evommune trial-initiation source states approximately 160 patients will be enrolled and randomized to one of three active dose regimens or placebo; exact arm-specific counts are not explicitly stated in the current local source text.',
        'source_note': 'Evommune CSU phase 2b trial-initiation PDF cached locally.',
    },
}

PROGRAM_STRATEGY_OVERRIDES = {
    'barzolvolimab': {
        'headline': 'Parallel KIT franchise build across CSU and CIndU, now extending into multiple phase 3 tracks.',
        'readout': 'The current local source layer suggests Celldex is not treating barzolvolimab as a single-study CSU asset. Instead, it is using early KIT proof across both spontaneous and inducible urticaria to support a broader late-stage urticaria franchise.',
        'bullets': [
            'Completed early studies cover both CSU and CIndU, so proof-of-concept was established across more than one urticaria phenotype before the current phase 3 wave.',
            'Two active phase 3 CSU studies plus a separate recruiting phase 3 CIndU study suggest deliberate parallel expansion rather than sequential single-indication development.',
            'The LTE study indicates lifecycle and durability planning, not just a one-shot registrational attempt.',
        ],
        'watch_items': [
            'How the sponsor differentiates the CSU pair versus the CIndU phase 3 branch in eventual positioning and labeling logic.',
            'Whether later derived pages can tie sponsor posters and press releases more tightly to explicit trial IDs.',
        ],
        'confidence': 'High',
    },
    'blu-808': {
        'headline': 'Broad early basket-style KIT exploration across CSU and CIndU before visible program narrowing.',
        'readout': 'The current registry footprint is still thin, but the visible study design suggests Blueprint is testing whether a wild-type KIT program can generate signal across both spontaneous and inducible urticaria before committing to a narrower late-stage path.',
        'bullets': [
            'Only one CT.gov-linked study is visible in the current local layer, but it explicitly spans both CIndU and CSU.',
            'At this stage the apparent strategy is breadth-first signal seeking, not yet a deep registrational stack.',
        ],
        'watch_items': [
            'Whether later sponsor or abstract evidence shows which urticaria subtype becomes the lead indication.',
        ],
        'confidence': 'Low',
    },
    'briquilimab': {
        'headline': 'Earlier-stage KIT exploration across CSU and CIndU, with extension follow-up but no visible late-stage build yet.',
        'readout': 'The current local stack suggests Jasper is using briquilimab to test KIT-driven benefit across both spontaneous and inducible disease, but the program remains meaningfully earlier than barzolvolimab in visible development maturity.',
        'bullets': [
            'Separate dose-escalation studies exist for CSU and CIndU, which suggests intentional dual-indication exploration rather than a single narrow pilot.',
            'The extension study indicates enough early interest to follow patients longer, but there is no phase 3 or manuscript-rich layer yet in the current cache.',
        ],
        'watch_items': [
            'Whether one phenotype becomes the clear lead path for registrational development.',
        ],
        'confidence': 'Medium',
    },
    'ep262': {
        'headline': 'Split proof-of-concept strategy across CIndU and CSU, but still early and sponsor-heavy in the current evidence layer.',
        'readout': 'The current local evidence suggests Escient is probing both inducible and spontaneous urticaria rather than staying confined to one subtype, but the support is still relatively thin and manuscript depth is weak.',
        'bullets': [
            'One early CIndU study and one randomized CSU study are visible, which looks like paired proof-of-concept branching across the broader urticaria space.',
            'Because publication support is weak in the local cache, this remains a cautious strategic read rather than a fully triangulated one.',
        ],
        'watch_items': [
            'Whether future sponsor or conference materials clarify which phenotype has the stronger efficacy story.',
        ],
        'confidence': 'Low',
    },
    'evo756': {
        'headline': 'Parallel MRGPRX2 development in CSU and CIndU from the phase 2 stage.',
        'readout': 'The current raw-source layer suggests Evommune is not waiting to prove one urticaria subtype first. Instead, EVO756 is being positioned as a broader urticaria mechanism program with concurrent phase 2 activity in CSU and CIndU.',
        'bullets': [
            'Visible trials cover both CIndU and CSU rather than a single lead indication.',
            'The phase 2b CSU study plus separate CIndU study suggest deliberate dual-path development early in the program.',
        ],
        'watch_items': [
            'Which subtype becomes the commercial or registrational lead as more efficacy detail becomes source-backed.',
        ],
        'confidence': 'Medium',
    },
    'fenebrutinib': {
        'headline': 'Historical BTK CSU proof-of-concept program, not a visibly expanding current franchise in the local layer.',
        'readout': 'The local evidence stack shows meaningful phase 2 CSU evidence for fenebrutinib, but the currently visible urticaria program looks more like an important earlier BTK proof point than an actively widening late-stage strategy.',
        'bullets': [
            'The program has a clear primary manuscript and completed CT.gov history, but no active recruiting urticaria studies are currently visible in the local registry.',
            'This makes fenebrutinib strategically important as precedent and mechanism validation, even if it is not the broadest active BTK urticaria stack here.',
        ],
        'watch_items': [
            'Whether additional source work shows newer urticaria development activity not yet captured in the current local layer.',
        ],
        'confidence': 'Medium',
    },
    'remibrutinib': {
        'headline': 'Broad BTK franchise strategy: establish CSU depth first, then layer on lifecycle, comparator, pediatric, CIndU, and real-world expansion.',
        'readout': 'The current local source layer suggests Novartis is treating remibrutinib as a platform urticaria program rather than a single pivotal asset. CSU is the deepest evidence base, but the surrounding studies show deliberate expansion into lifecycle management, differentiation versus standards, CIndU growth, and post-approval evidence generation.',
        'bullets': [
            'The CSU package is unusually dense: phase 2b core and extension, paired REMIX phase 3 studies, long-term follow-up, regional expansion, and dedicated safety work.',
            'Comparator, adolescent, and mixed-CU studies suggest the sponsor is broadening both label reach and positioning, not only finishing the core adult CSU story.',
            'The CIndU basket study and later real-world studies indicate the program is being extended beyond classic pivotal CSU into franchise-level expansion.',
        ],
        'watch_items': [
            'How strongly the CIndU branch matures relative to the already dense CSU package.',
            'Whether comparator studies become mainly differentiation tools or major label-shaping assets.',
        ],
        'confidence': 'High',
    },
    'rilzabrutinib': {
        'headline': 'More focused BTK challenger strategy in CSU, with a thinner visible development stack than remibrutinib.',
        'readout': 'In the current local evidence layer, rilzabrutinib looks like a narrower CSU-centered BTK program rather than a broad urticaria franchise. The strategic posture appears more concentrated and later-entry than remibrutinib’s multi-branch stack.',
        'bullets': [
            'The current local layer shows one clear CSU trial and one primary manuscript, without the same visible extension, CIndU, pediatric, or real-world lattice seen for remibrutinib.',
            'That makes the program easier to describe, but also indicates less disclosed breadth in the current source cache.',
        ],
        'watch_items': [
            'Whether additional sponsor materials reveal broader lifecycle or subtype expansion plans beyond the currently visible CSU focus.',
        ],
        'confidence': 'Medium',
    },
    'sep-631': {
        'headline': 'Pipeline-visible MRGPRX2 program without a disclosed CT.gov study stack in the current local cache.',
        'readout': 'The current local layer shows SEP-631 as strategically interesting, but still early from an evidence-architecture perspective. Right now it reads more like a program signal from sponsor materials than a transparently disclosed clinical development strategy.',
        'bullets': [
            'No CT.gov-linked urticaria records are currently captured in the local registry.',
            'The visible strategy therefore comes mostly from sponsor and poster materials rather than a fully surfaced trial stack.',
        ],
        'watch_items': [
            'Whether a study record or more explicit protocol-level disclosure appears and allows stronger normalization.',
        ],
        'confidence': 'Low',
    },
}


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


def highest_phase_label(program_entry: dict) -> str:
    order = {'PHASE1': 1, 'PHASE2': 2, 'PHASE3': 3, 'PHASE4': 4}
    best = 0
    best_label = 'NR'
    for trial in program_entry.get('ctgov_trials', []):
        for phase in trial.get('phase', []) or []:
            if order.get(phase, 0) > best:
                best = order[phase]
                best_label = phase.replace('PHASE', 'Phase ')
    return best_label


def get_program_strategy(program_entry: dict) -> dict:
    strategy = PROGRAM_STRATEGY_OVERRIDES.get(program_entry['program_key'])
    if strategy:
        return strategy
    return {
        'headline': 'Program strategy not yet manually summarized.',
        'readout': 'The current local source layer is still too thin for a higher-confidence strategic interpretation beyond the visible study inventory.',
        'bullets': [],
        'watch_items': ['Manual enrichment is still needed before making a stronger strategy claim.'],
        'confidence': 'Low',
    }


def get_trial_operational_override(trial_id: str) -> dict:
    return TRIAL_OPERATIONAL_OVERRIDES.get(trial_id, {})


DOSE_RE = re.compile(r'\b\d+(?:\.\d+)?\s*(?:mg/kg|mg|mcg|μg|ug|g)\b', re.IGNORECASE)
RATIO_RE = re.compile(r'(\d+\s*:\s*\d+(?::\s*\d+)*)\s*ratio', re.IGNORECASE)


def arm_text_blob(arm: dict) -> str:
    intervention_names = arm.get('intervention_names') or []
    return ' '.join(filter(None, [arm.get('label'), arm.get('description'), ' '.join(intervention_names)]))


def infer_arm_route(arm: dict) -> str:
    text = arm_text_blob(arm).lower()
    routes = []
    route_checks = [
        ('Subcutaneous', ['subcutaneous', 's.c.', 'sq injection']),
        ('Intravenous', ['intravenous']),
        ('Oral', ['oral', 'orally', 'capsule', 'tablet', 'p.o.']),
        ('Injection', ['injection']),
    ]
    for label, needles in route_checks:
        if any(needle in text for needle in needles):
            if label == 'Injection' and any(r in routes for r in ['Subcutaneous', 'Intravenous']):
                continue
            if label not in routes:
                routes.append(label)
    if re.search(r'\biv\b', text) and 'Intravenous' not in routes:
        routes.append('Intravenous')
    return ' + '.join(routes) if routes else 'NR'


def infer_arm_frequency(arm: dict) -> str:
    text = arm_text_blob(arm).lower()
    found = []
    patterns = [
        ('single dose', 'Single dose'),
        ('once as a', 'Single loading dose'),
        ('twice daily', 'BID'),
        ('b.i.d.', 'BID'),
        (' bid', 'BID'),
        ('once daily', 'QD'),
        (' qd', 'QD'),
        ('qd ', 'QD'),
        ('every 4 weeks', 'Q4W'),
        ('q4w', 'Q4W'),
        ('every 8 weeks', 'Q8W'),
        ('q8w', 'Q8W'),
        ('every other week', 'Q2W'),
    ]
    for needle, label in patterns:
        if needle in text and label not in found:
            found.append(label)
    return ' + '.join(found) if found else 'NR'


def infer_arm_dose(arm: dict) -> str:
    text = arm_text_blob(arm)
    doses = []
    for match in DOSE_RE.findall(text):
        dose = ' '.join(match.split())
        if dose not in doses:
            doses.append(dose)
    if doses:
        return ' -> '.join(doses)
    label = (arm.get('label') or '').strip()
    if re.search(r'\bdose [A-Z0-9]+\b', label, re.IGNORECASE):
        return label
    if label.lower().startswith('dose '):
        return label
    return 'NR'


def arm_regimen_details(arm: dict) -> dict:
    return {
        'dose': infer_arm_dose(arm),
        'frequency': infer_arm_frequency(arm),
        'route': infer_arm_route(arm),
    }


def active_dose_levels_from_ct(ct: dict) -> int | None:
    regimens = []
    for arm in (ct.get('arm_groups') or []):
        arm_type = (arm.get('type') or '').upper()
        if arm_type == 'PLACEBO_COMPARATOR':
            continue
        regimen = arm_regimen_details(arm)
        dose = regimen['dose']
        freq = regimen['frequency']
        route = regimen['route']
        if dose == 'NR' and freq == 'NR' and route == 'NR':
            continue
        key = (dose, freq, route)
        if key not in regimens:
            regimens.append(key)
    return len(regimens) or None


def infer_per_arm_summary(ct: dict, arm_sizes: dict[str, str]) -> str | None:
    arm_groups = ct.get('arm_groups') or []
    enrollment = ct.get('enrollment')
    if arm_sizes:
        labeled = []
        for arm in arm_groups:
            label = arm.get('label')
            if label in arm_sizes:
                labeled.append(f"{label} n={arm_sizes[label]}")
        if labeled:
            return '; '.join(labeled)
    if len(arm_groups) == 1 and enrollment not in (None, '', 'NR'):
        label = arm_groups[0].get('label', 'Single arm')
        return f"{label} n={enrollment} in this single-arm study."
    blob = ' '.join(filter(None, [ct.get('brief_summary'), ct.get('detailed_description')] + [arm_text_blob(a) for a in arm_groups]))
    ratio_match = RATIO_RE.search(blob)
    if ratio_match and enrollment not in (None, '', 'NR') and arm_groups:
        return f"{enrollment} total with a {ratio_match.group(1)} allocation schema across {len(arm_groups)} listed arms; exact arm-specific counts are not explicitly stated in the current local source text."
    if enrollment not in (None, '', 'NR') and arm_groups:
        return f"{enrollment} total across {len(arm_groups)} listed arms; exact arm-specific counts are not explicitly stated in the current local source text."
    return None


def infer_source_note(ct: dict, override: dict) -> str | None:
    if override.get('source_note'):
        return override['source_note']
    if ct.get('arm_groups'):
        return 'ClinicalTrials.gov arm descriptions and summary text.'
    return None


def trial_operational_snapshot(ct: dict) -> dict:
    trial_id = ct.get('nct_id') or ct.get('trial_id')
    override = get_trial_operational_override(trial_id)
    arm_groups = ct.get('arm_groups') or []
    arm_count = len(arm_groups) or None
    active_dose_levels = override.get('active_dose_levels_count') or active_dose_levels_from_ct(ct)
    arm_sizes = dict(override.get('arm_sizes', {}))
    enrollment = ct.get('enrollment')
    if not arm_sizes and len(arm_groups) == 1 and enrollment not in (None, '', 'NR'):
        label = arm_groups[0].get('label')
        if label:
            arm_sizes[label] = str(enrollment)
    arm_regimens = {arm.get('label', 'NR'): arm_regimen_details(arm) for arm in arm_groups}
    arm_regimens.update(override.get('arm_regimens', {}))
    return {
        'arm_count': arm_count,
        'active_dose_levels_count': active_dose_levels,
        'design_summary': override.get('design_summary'),
        'per_arm_summary': override.get('per_arm_summary') or infer_per_arm_summary(ct, arm_sizes),
        'source_note': infer_source_note(ct, override),
        'arm_sizes': arm_sizes,
        'arm_regimens': arm_regimens,
    }


def append_strategy_section(lines: list[str], program_entry: dict):
    strategy = get_program_strategy(program_entry)
    lines.extend([
        '## Strategy readout',
        f"- Headline: {strategy['headline']}",
        f"- Current strategic read: {strategy['readout']}",
        f"- Highest visible phase in current registry: {highest_phase_label(program_entry)}",
        f"- Strategy confidence in current local layer: {strategy['confidence']}",
        '',
        '### Why this looks like the strategy',
    ])
    for item in strategy.get('bullets', []):
        lines.append(f'- {item}')
    if not strategy.get('bullets'):
        lines.append('- The current visible study stack is not yet rich enough for a better derived summary.')
    lines.extend(['', '### What to watch next'])
    for item in strategy.get('watch_items', []):
        lines.append(f'- {item}')
    lines.append('')


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
    ]
    append_strategy_section(lines, program_entry)
    lines.extend([
        '## Operational study design view',
        '| Trial | Arms in registry | Active dose regimens | Total enrollment | Per-arm sample size summary |',
        '|---|---:|---:|---:|---|',
    ])
    for trial in program_entry.get('ctgov_trials', []):
        ct_rec = CTGOV_BY_NCT.get(trial['trial_id'], trial)
        snap = trial_operational_snapshot(ct_rec)
        link_name = trial_link_name(program_entry['program_key'], trial['trial_id'], trial_slug_map)
        arm_count = snap['arm_count'] if snap['arm_count'] is not None else 'NR'
        dose_count = snap['active_dose_levels_count'] if snap['active_dose_levels_count'] is not None else 'NR'
        total_enrollment = ct_rec.get('enrollment', trial.get('enrollment', 'NR'))
        per_arm = snap['per_arm_summary'] or 'Direct per-arm N has not yet been promoted from the current local source layer.'
        lines.append(f"| [{trial['trial_id']}](../trials/{link_name}) | {arm_count} | {dose_count} | {total_enrollment} | {per_arm} |")
    lines.extend([
        '',
        '## Program map',
        '',
    ])
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
    ]
    append_strategy_section(lines, program_entry)
    lines.extend([
        '## Operational study design view',
        '| Trial | Arms in registry | Active dose regimens | Total enrollment | Per-arm sample size summary |',
        '|---|---:|---:|---:|---|',
    ])
    for trial in program_entry.get('ctgov_trials', []):
        ct_rec = CTGOV_BY_NCT.get(trial['trial_id'], trial)
        snap = trial_operational_snapshot(ct_rec)
        link_name = trial_link_name(program_entry['program_key'], trial['trial_id'], trial_slug_map)
        arm_count = snap['arm_count'] if snap['arm_count'] is not None else 'NR'
        dose_count = snap['active_dose_levels_count'] if snap['active_dose_levels_count'] is not None else 'NR'
        total_enrollment = ct_rec.get('enrollment', trial.get('enrollment', 'NR'))
        per_arm = snap['per_arm_summary'] or 'Direct per-arm N has not yet been promoted from the current local source layer.'
        lines.append(f"| [{trial['trial_id']}](../trials/{link_name}) | {arm_count} | {dose_count} | {total_enrollment} | {per_arm} |")
    lines.extend([
        '',
        '## Study Inventory',
        '',
    ])

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
    operational = trial_operational_snapshot(ct)
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

    lines.extend(['', '## Operational design summary'])
    lines.append(f"- Arms represented in current CT.gov export: {operational['arm_count'] if operational['arm_count'] is not None else 'NR'}")
    lines.append(f"- Active dose regimens represented in current local source layer: {operational['active_dose_levels_count'] if operational['active_dose_levels_count'] is not None else 'NR'}")
    lines.append(f"- Total study enrollment in CT.gov: {ct.get('enrollment', 'NR')} ({ct.get('enrollment_type', 'NR')})")
    if operational.get('design_summary'):
        lines.append(f"- Design interpretation: {operational['design_summary']}")
    if operational.get('per_arm_summary'):
        lines.append(f"- Per-arm sample size summary: {operational['per_arm_summary']}")
    else:
        lines.append('- Per-arm sample size summary: direct per-arm N has not yet been promoted from the current local source layer.')
    if operational.get('source_note'):
        lines.append(f"- Arm-size evidence source: {operational['source_note']}")

    lines.extend(['', '## Arms', '| Arm | Type | Dose | Frequency | Route | Description | N | Evidence status |', '|---|---|---|---|---|---|---:|---|'])
    if ct.get('arm_groups'):
        for arm in ct['arm_groups']:
            desc = (arm.get('description') or 'NR').replace('\n', ' ')
            raw_label = arm.get('label', 'NR')
            label = raw_label.replace('|', '\\|')
            atype = (arm.get('type') or 'NR').replace('|', '\\|')
            desc = desc.replace('|', '\\|')
            regimen = operational.get('arm_regimens', {}).get(raw_label, {})
            dose = regimen.get('dose', 'NR').replace('|', '\\|')
            frequency = regimen.get('frequency', 'NR').replace('|', '\\|')
            route = regimen.get('route', 'NR').replace('|', '\\|')
            exact_n = operational.get('arm_sizes', {}).get(raw_label)
            if exact_n:
                evidence_status = 'Directly supported by linked local publication/source text or explicit CT.gov arm-level enrollment context'
                n_value = exact_n
            else:
                if operational.get('per_arm_summary'):
                    evidence_status = 'Summary-level arm-size evidence exists, but exact N is not mapped to this CT.gov arm label in the current local layer'
                else:
                    evidence_status = 'Exact arm-specific N not explicitly promoted from the current local evidence layer'
                n_value = 'NR'
            lines.append(f"| {label} | {atype} | {dose} | {frequency} | {route} | {desc} | {n_value} | {evidence_status} |")
    else:
        lines.append('| NR | NR | NR | NR | NR | No arm-group details parsed into current inventory | NR | NR |')

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
    lines.append('  - Some studies still lack exact arm-specific N in the current promoted evidence layer even when allocation schema or total enrollment is visible.')
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
        '- Derived strategy view: [Program strategy briefs](../queries/program-strategy-briefs.md)',
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

    strategy_lines = [
        '---',
        'title: Program strategy briefs',
        'tags:',
        '  - type/query',
        '---',
        '# Program strategy briefs',
        '',
        'This page is a derived interpretation layer. It is meant to answer the question: what does the current local source stack suggest each sponsor is trying to do with its urticaria program?',
        '',
        '| Program | Class | Highest phase | Trials | Primary pubs | Strategy confidence | Strategy headline |',
        '|---|---|---|---:|---:|---|---|',
    ]
    for program in programs:
        strategy = get_program_strategy(program)
        strategy_lines.append(
            f"| [{program['display_name']}](../programs/{program['program_key']}.md) | {', '.join(program.get('priority_classes', [])) or 'NR'} | {highest_phase_label(program)} | {len(program.get('ctgov_trials', []))} | {len(program.get('primary_publications', []))} | {strategy['confidence']} | {strategy['headline']} |"
        )
    strategy_lines.extend(['', '## Program-by-program strategic readouts', ''])
    for program in programs:
        strategy = get_program_strategy(program)
        strategy_lines.append(f"### {program['display_name']}")
        strategy_lines.append(f"- Program page: [open](../programs/{program['program_key']}.md)")
        strategy_lines.append(f"- Strategic read: {strategy['readout']}")
        strategy_lines.append(f"- Why this read is plausible in the current local layer: {strategy['headline']}")
        strategy_lines.append(f"- Evidence depth: {len(program.get('ctgov_trials', []))} CT.gov trials, {len(program.get('primary_publications', []))} primary publication(s), {len(program.get('sponsor_artifacts', []))} sponsor artifact(s)")
        strategy_lines.append('- Key reasons:')
        for item in strategy.get('bullets', []):
            strategy_lines.append(f"  - {item}")
        if not strategy.get('bullets'):
            strategy_lines.append('  - The visible source stack is still too thin for a richer derived summary.')
        strategy_lines.append('- What to watch:')
        for item in strategy.get('watch_items', []):
            strategy_lines.append(f"  - {item}")
        strategy_lines.append('')
    write_text(QUERIES_DIR / 'program-strategy-briefs.md', '\n'.join(strategy_lines))


def main():
    global CTGOV_BY_NCT
    registry = load_json(REGISTRY_PATH)
    ctgov_records = load_json(CTGOV_PATH)
    ct_by_nct = {rec['nct_id']: rec for rec in ctgov_records}
    CTGOV_BY_NCT = ct_by_nct
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
