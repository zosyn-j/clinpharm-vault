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
        'headline': 'Broad early wild-type KIT exploration across CSU and CIndU, now carried inside Sanofi after the Blueprint acquisition.',
        'readout': 'The current registry footprint is still thin, but the visible study design suggests BLU-808 remains a breadth-first wild-type KIT urticaria program spanning both spontaneous and inducible disease. The corporate context changed materially once Sanofi completed the Blueprint Medicines acquisition in July 2025, so future BLU-808 decisions should be read as Sanofi portfolio prioritization rather than a standalone Blueprint narrowing decision.',
        'bullets': [
            'Only one CT.gov-linked study is visible in the current local layer, but it explicitly spans both CIndU and CSU.',
            'The current study stack still looks like early cross-phenotype signal seeking rather than a mature registrational build.',
            'The cached Sanofi completion press release explicitly brings Blueprint\'s KIT-driven pipeline into Sanofi and assigns BLU-808 milestone value in the deal structure, which supports treating the asset as part of Sanofi\'s immunology portfolio context rather than only a historical Blueprint program.',
        ],
        'watch_items': [
            'Whether later Sanofi pipeline materials show a clearer lead urticaria phenotype or narrower development focus for BLU-808.',
            'Whether sponsor-facing trial materials and future disclosures start reflecting Sanofi ownership directly instead of legacy Blueprint branding.',
        ],
        'confidence': 'Medium',
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

TRIAL_RESULT_OVERRIDES: dict[str, dict] = {
    # -- Remibrutinib CSU Phase 2b core --
    'NCT03926611': {
        'result_status': 'Published',
        'efficacy': [
            'Primary endpoint (UAS7 change from baseline at week 4): LS mean ranged from -14.7 to -20.0 across 6 active dose regimens versus -5.4 for placebo; nominal P < 0.0001 for all doses versus placebo.',
            'Best-performing regimen (25 mg BID): week-4 UAS7 change -20.0 versus -5.4 placebo.',
            'Rapid onset of symptom reduction observed from week 1 through week 12.',
        ],
        'safety': [
            'Most adverse events were mild or moderate with no dose-dependent pattern.',
        ],
        'source_citations': ['PMID 36096203'],
    },
    # -- Remibrutinib Phase 2b OLE --
    'NCT04109313': {
        'result_status': 'Published',
        'efficacy': [
            '194 of 230 (84.3%) patients from the core study entered the open-label treatment period (remibrutinib 100 mg BID).',
            'Mean UAS7 change from baseline: -17.6 at week 4, -21.8 at week 52.',
            'Complete response (UAS7 = 0): 28.2% at week 4, 55.8% at week 52.',
            'Well-controlled disease (UAS7 <= 6): 52.7% at week 4, 68.0% at week 52.',
        ],
        'safety': [
            'Safety comparable to core study; most TEAEs mild-to-moderate.',
            'Three most common TEAE classes: infections (30.9%), skin/subcutaneous (26.8%), GI disorders (16.5%).',
        ],
        'source_citations': ['PMID 37866460'],
    },
    # -- REMIX-1 --
    'NCT05030311': {
        'result_status': 'Published',
        'efficacy': [
            'Primary endpoint met: week-12 UAS7 LS mean change -20.0 (remibrutinib) versus -13.8 (placebo), P < 0.001.',
            'Well-controlled disease (UAS7 <= 6) at week 12: 49.8% versus 24.8% (P < 0.001).',
            'Complete response (UAS7 = 0) at week 12: 31.1% versus 10.5% (P < 0.001).',
            '52-week UAS7 change from baseline (remibrutinib): -23.22 (95% CI -24.78 to -21.66); sustained improvement confirmed.',
            'Placebo-to-remibrutinib crossover at week 24 showed similar response as early as 1 week after switch.',
        ],
        'safety': [
            'AE and SAE rates similar between remibrutinib and placebo through week 24.',
            'Petechiae higher with remibrutinib (3.8% versus 0.3% in combined REMIX data).',
            'Exposure-adjusted AE incidence at 52 weeks remained consistent with the 24-week analysis.',
        ],
        'source_citations': ['PMID 40043237', 'PMID 41115533'],
    },
    # -- REMIX-2 --
    'NCT05032157': {
        'result_status': 'Published',
        'efficacy': [
            'Primary endpoint met: week-12 UAS7 LS mean change -19.4 (remibrutinib) versus -11.7 (placebo), P < 0.001.',
            'Well-controlled disease (UAS7 <= 6) at week 12: 46.8% versus 19.6% (P < 0.001).',
            'Complete response (UAS7 = 0) at week 12: 27.9% versus 6.5% (P < 0.001).',
            '52-week UAS7 change from baseline (remibrutinib): -22.98 (95% CI -24.51 to -21.44); sustained benefit confirmed.',
        ],
        'safety': [
            'Safety profile consistent with REMIX-1; no new signals at 52 weeks.',
            'Most common AEs (>= 5%): respiratory tract infections and headache, comparable with placebo.',
            'Liver transaminase elevations balanced across arms; all asymptomatic, transient, and reversible.',
        ],
        'source_citations': ['PMID 40043237', 'PMID 41115533'],
    },
    # -- RemIND CIndU Phase 3 --
    'NCT05976243': {
        'result_status': 'Topline',
        'efficacy': [
            'Primary endpoint met for all three CIndU subtypes: significantly higher complete response rates versus placebo at week 12 for symptomatic dermographism, cold urticaria, and cholinergic urticaria.',
            'Described as the first therapy to achieve a Phase III primary endpoint in CIndU.',
        ],
        'safety': [
            'Well-tolerated; favorable safety profile; no liver safety concerns reported in topline release.',
        ],
        'source_citations': ['Novartis press release, 2026-02-18 (raw/sponsors/btk/remibrutinib/2026-cindu-phase-iii-remind-press-release.md)'],
    },
    # -- Barzolvolimab Phase 1b CSU --
    'NCT04538794': {
        'result_status': 'Published',
        'efficacy': [
            'At week 12 across all barzolvolimab doses combined: 71% achieved well-controlled disease (UAS7 <= 6), 57% achieved complete response (UAS7 = 0).',
            '77% achieved well-controlled UCT (>= 12); 43% achieved complete UCT response (UCT = 16).',
            'Rapid symptom reduction within 1 week; response paralleled tryptase suppression.',
            'Similar response regardless of prior omalizumab use (44% of patients had prior omalizumab).',
        ],
        'safety': [
            'Well tolerated; hair color change was the most common AE (mechanism-related KIT effect).',
        ],
        'source_citations': ['PMID 40415544'],
    },
    # -- Barzolvolimab Phase 2 CSU --
    'NCT05368285': {
        'result_status': 'Published',
        'efficacy': [
            'Primary endpoint met at week 12 (UAS7 change from baseline, LS mean delta versus placebo): 150 mg Q4W -12.55 (P < 0.0001), 300 mg Q8W -13.41 (P < 0.0001), 75 mg Q4W -6.60 (P = 0.0017).',
            'Complete response (UAS7 = 0) at week 12: 150 mg 51.1%, 300 mg 37.5%, 75 mg 22.9%, placebo 6.4%.',
            'Week 52 sustained results (all patients on 150 mg or 300 mg): up to 71% complete response, up to 74% well-controlled disease, with early gains visible from week 1.',
            'EADV 2025 sponsor poster indicates similarly strong efficacy in low-IgE and normal/high-IgE subgroups at weeks 12 and 52, supporting activity beyond a narrow biomarker-defined subset.',
            'Week 76 off-treatment follow-up: up to 41% maintained complete response (UAS7 = 0); 69% of Week 52 responders still well-controlled; suggestive of disease modification.',
        ],
        'safety': [
            'Hair color changes (26%), neutropenia (17%), skin hypopigmentation (13%); all mechanism-related, mostly Grade 1, reversible upon discontinuation.',
            'AEs were not dose-dependent; no association between infections and neutropenia.',
            'Treatment-related SAEs: 2 (1%) across 156 barzolvolimab-treated patients.',
        ],
        'source_citations': ['PMID 41747871', 'raw/sponsors/kit/barzolvolimab/aaaai-2025-csu-poster.md', 'raw/sponsors/kit/barzolvolimab/eadv-2024-congress-presentation.md', 'raw/sponsors/kit/barzolvolimab/eadv-2025-csu-ige-poster.md'],
    },
    # -- Barzolvolimab Phase 2 CIndU --
    'NCT05405660': {
        'result_status': 'Conference',
        'efficacy': [
            'Primary endpoint (negative provocation test at week 12) -- Cold urticaria: 150 mg Q4W 53.1%, 300 mg Q8W 46.9%, placebo 12.5%.',
            'Symptomatic dermographism: 150 mg Q4W 57.6%, 300 mg Q8W 42.4%, placebo 3.2%.',
            'Critical Temperature Threshold (ColdU) LS mean change at week 12: 150 mg -9.61 C, 300 mg -8.82 C versus placebo -0.82 C (both P < 0.0001).',
            'Critical Friction Threshold (SD) LS mean change at week 12: 150 mg -2.46 pins, 300 mg -2.27 pins versus placebo -0.30 pins (both P < 0.0001 and P = 0.0002).',
            'Week 20: complete response up to 66% ColdU, 49% SD.',
        ],
        'safety': [
            '98% of TEAEs were Grade 1 or 2; hair color changes 13% (versus 0% placebo), neutropenia 10% (versus 0% placebo).',
            'No difference in AE-related discontinuation rates between active (2%) and placebo (3%).',
        ],
        'source_citations': ['raw/sponsors/kit/barzolvolimab/phase-2-cindu-acaai-poster.md', 'raw/sponsors/kit/barzolvolimab/ir-press-release-pdf-additional-data.md'],
    },
    # -- Fenebrutinib Phase 2 CSU --
    'NCT03137069': {
        'result_status': 'Published',
        'efficacy': [
            'Cohort 2 primary endpoint (UAS7 change at week 8, LS mean difference versus placebo): 200 mg BID -9.5 (95% CI -16.7 to -2.4; significant), 150 mg QD -6.4 (95% CI -13.4 to 0.6; trend), 50 mg QD -0.5 (not significant).',
            'Well-controlled disease (UAS7 <= 6) at week 8: 200 mg BID 57%, 150 mg 46%, 50 mg 35%, placebo 22%.',
            'Complete response (UAS7 = 0) at week 8: 200 mg BID 39%, 150 mg 25%, 50 mg 13%, placebo 4%.',
            'Rapid onset: 200 mg BID week-4 UAS7 LS mean difference -10.8 versus placebo (95% CI -18.2 to -3.3).',
            'Exploratory: all doses reduced IgG-anti-FcεRI autoantibodies (median change -43.7% to -53.6% versus +20.4% placebo).',
        ],
        'safety': [
            'No SAEs in Cohort 2; most common AEs: urticaria (15%), nasopharyngitis (11%), headache (6%).',
            'Grade 2/3 liver transaminase elevations in 2 patients each at 150 mg QD and 200 mg BID; all asymptomatic and reversible.',
            'Dose-dependent creatinine increases starting week 1; no serious or opportunistic infections.',
            'Note: further CSU studies of fenebrutinib are not planned; program pivoted to MS.',
        ],
        'source_citations': ['PMID 34750553', 'PMCID PMC8604722'],
    },
    # -- Rilzabrutinib RILECSU Phase 2 --
    'NCT05107115': {
        'result_status': 'Published',
        'efficacy': [
            'Primary endpoint (ISS7 change at week 12, 1200 mg/d versus placebo, omalizumab-naive): LS mean -9.21 versus -5.77; difference -3.44 (95% CI -6.25 to -0.62; P = 0.02).',
            'UAS7 change at week 12 (1200 mg/d versus placebo): LS mean -16.89 versus -10.14; difference -6.75 (95% CI -12.23 to -1.26; P = 0.02).',
            'Well-controlled disease (UAS7 <= 6) at week 12: 34.3% versus 11.1% (difference 20.3%).',
            'Rapid onset: improvements in ISS7, UAS7, HSS7, and AAS7 observed as early as week 1.',
            'Exploratory biomarkers (1200 mg/d): IgG anti-FcεRI -38.7%, IgG anti-TPO -46.7% versus placebo.',
        ],
        'safety': [
            'Favorable risk-benefit; no dose-dependent AEs; most frequent AEs: diarrhea and nausea (mild).',
            'No cytopenia, bleeding, or atrial fibrillation events (distinguishing from older irreversible BTKIs).',
            '3 SAEs total, none related to rilzabrutinib.',
            'ALT > 3x ULN: 4 cases total across arms; all resolved, 3 while continuing drug.',
        ],
        'source_citations': ['PMID 40266575', 'PMCID PMC12019677'],
    },
    # -- EP262 Phase 2 CSU (terminated) --
    'NCT06077773': {
        'result_status': 'Posted (CT.gov)',
        'efficacy': [
            'Primary endpoint not met: UAS7 change from baseline at week 6 showed no significant separation from placebo for either EP262 dose.',
            'EP262 50 mg: LS mean UAS7 change -8.43 versus placebo -10.41; difference +1.99 (95% CI -1.96 to 5.94; P = 0.41).',
            'EP262 150 mg: LS mean UAS7 change -11.95 versus placebo -10.41; difference -1.53 (95% CI -5.49 to 2.42; P = 0.52).',
            'Study was terminated; Part 2 was not enrolled.',
        ],
        'safety': [
            'TEAEs: placebo 12/38 (31.6%), EP262 50 mg 15/37 (40.5%), EP262 150 mg 19/38 (50.0%).',
            'Grade >= 3 TEAEs: placebo 1, EP262 50 mg 0, EP262 150 mg 1.',
        ],
        'source_citations': ['ClinicalTrials.gov posted results (NCT06077773 resultsSection)'],
    },
    # -- EVO756 Phase 2 CIndU (symptomatic dermographism) --
    'NCT06603220': {
        'result_status': 'Conference',
        'efficacy': [
            'Open-label study in symptomatic dermographism (n = 30, 300 mg QD or 50 mg BID, 4 weeks).',
            '93% of patients showed clinical response at 4 weeks in either FricTest score or Pruritus-NRS.',
            '70% improved in FricTest score; 30% achieved complete FricTest response.',
            '82% had reduced Pruritus-NRS; 41% achieved clinically meaningful >= 4-point itch NRS reduction.',
            'Onset of improvement as early as week 1 (including 3 complete responses at week 1).',
            '50% of complete responders were IgE-high (>= 100 IU/mL), showing activity not limited to IgE-low patients.',
        ],
        'safety': [
            'No serious TEAEs; no discontinuations due to AEs; well tolerated and consistent with Phase 1 profile.',
        ],
        'source_citations': ['raw/sponsors/mrgprx2/evo756/eadv-2025-cindu-presentation-pdf.md', 'raw/sponsors/mrgprx2/evo756/cindu-top-line-press-release-pdf.md'],
    },
}


PROGRAM_SPONSOR_RESULTS: dict[str, dict] = {
    'barzolvolimab': {
        'headline': 'CSU sponsor-poster layer is unusually deep, extending the manuscript-backed phase 2 story into durability, quality-of-life, and IgE-subgroup analyses.',
        'entries': [
            {
                'label': 'AAAAI 2025 CSU poster (52-week control and quality-of-life follow-up)',
                'result_status': 'Conference poster',
                'efficacy': [
                    'Improvement in urticaria control was sustained through week 52, with up to 82% of patients reporting well-controlled urticaria by UCT and approximately half reporting complete control at week 52.',
                    'The poster also frames week-52 quality-of-life improvement, with many patients reporting that CSU symptoms no longer had meaningful impact on daily life.',
                    'This poster strengthens the interpretation that the phase 2 CSU dataset is not only statistically positive at week 12, but also durable and patient-meaningful over longer follow-up.',
                ],
                'safety': [
                    'Mechanism-related events highlighted in the sponsor poster remained mainly hair color change, neutropenia, urticaria, and skin pigment change, consistent with the broader barzolvolimab safety narrative.',
                ],
                'source_citations': ['raw/sponsors/kit/barzolvolimab/aaaai-2025-csu-poster.md'],
            },
            {
                'label': 'EADV 2025 CSU IgE subgroup poster',
                'result_status': 'Conference poster',
                'efficacy': [
                    'Weeks 12 and 52 analyses suggest similarly strong efficacy for 150 mg Q4W and 300 mg Q8W in patients with low (< 40 IU/mL) and normal/high (>= 40 IU/mL) baseline IgE levels.',
                    'The cached poster text states that adjusted p-values were non-significant for comparisons between IgE subgroups, while most active-versus-placebo comparisons remained significant, supporting efficacy across biologically distinct CSU subsets.',
                    'This is especially useful strategically because low-IgE CSU is often discussed as a more autoimmune / anti-IgE-refractory phenotype.',
                ],
                'safety': [],
                'source_citations': ['raw/sponsors/kit/barzolvolimab/eadv-2025-csu-ige-poster.md'],
            },
            {
                'label': 'Late follow-up sponsor disclosures (ACAAI/AAAAI-linked releases)',
                'result_status': 'Sponsor press release / IR PDF',
                'efficacy': [
                    'Sponsor disclosures extend the CSU phase 2 story beyond active treatment, including up to 41% complete response at week 76 and persistence of control after treatment discontinuation in a subset of week-52 responders.',
                    'One sponsor summary also highlights a subset analysis in which 88% of patients who completed 52 weeks on 150 mg Q4W or 300 mg Q8W and finished treatment with at least well-controlled disease reported complete response.',
                ],
                'safety': [
                    'Sponsor summaries continue to describe the safety profile as well tolerated, with KIT-related tolerability findings largely reversible after discontinuation.',
                ],
                'source_citations': ['raw/sponsors/kit/barzolvolimab/ir-press-release-additional-positive-data.md', 'raw/sponsors/kit/barzolvolimab/ir-press-release-pdf-additional-data.md'],
            },
        ],
    },
    'sep-631': {
        'headline': 'Phase 1 proof-of-mechanism data available from AAAAI 2026 poster (sponsor-sourced).',
        'entries': [
            {
                'label': 'SEP-631 Phase 1 SAD/MAD in healthy volunteers (NCT07069036)',
                'result_status': 'Conference (sponsor poster)',
                'efficacy': [
                    'Complete inhibition of icatibant 10 µg/mL-induced skin wheals at doses as low as 10 mg QD after 9 days of treatment.',
                    'Complete inhibition of icatibant 100 µg/mL-induced skin wheals at 90 to 200 mg QD.',
                    '120 participants dosed across SAD (n=48), MAD (n=64), and food-effect (n=8) parts.',
                    'PK profile supports once-daily oral dosing; no clinically meaningful food effect observed.',
                ],
                'safety': [
                    'TEAE rate comparable with placebo across all dose cohorts; no severe or serious TEAEs.',
                    'SAD: most common TEAEs were headache (11.1% SEP-631 vs 8.3% placebo) and transaminase increases (5.6% vs 8.3%).',
                    'MAD: most common TEAEs were headache; one mild transaminase elevation with SEP-631 and one with placebo.',
                ],
                'source_citations': ['raw/sponsors/mrgprx2/sep-631/aaaai-2026-poster-pdf.md'],
            },
        ],
    },
    'evo756': {
        'headline': 'Phase 1 proof-of-concept data available from GA2LEN 2024 presentation (sponsor-sourced), in addition to Phase 2 CIndU trial results.',
        'entries': [
            {
                'label': 'EVO756 Phase 1 SAD/MAD proof-of-concept in healthy volunteers',
                'result_status': 'Conference (sponsor presentation)',
                'efficacy': [
                    'Proof-of-concept trial in 132 subjects showed robust target engagement via icatibant skin challenge.',
                    'EVO756 significantly inhibited wheal formation induced by icatibant at multiple dose levels after 14 days of treatment.',
                    'PK profile supports once-daily oral dosing.',
                ],
                'safety': [
                    'Well tolerated; TEAE rate comparable with placebo across all dosing cohorts.',
                    'No severe or serious adverse events; most common TEAEs: headache and IV catheter site pain.',
                ],
                'source_citations': ['raw/sponsors/mrgprx2/evo756/ga2len-2024-trial-results-presentation-pdf.md'],
            },
        ],
    },
    'remibrutinib': {
        'headline': 'Sponsor press releases complement the manuscript-backed REMIX results with topline framing of rapid onset, phase progression, durability, and CIndU expansion.',
        'entries': [
            {
                'label': 'Novartis Phase III topline press release (August 2023)',
                'result_status': 'Sponsor press release',
                'efficacy': [
                    'REMIX-1 and REMIX-2 both met all primary and secondary endpoints, showing clinically meaningful and statistically significant improvements in UAS7 at week 12 (sponsor press release; exact effect sizes reported in PMID 40043237).',
                    'Rapid onset of action illustrated by UAS7 improvement at week 2 in both REMIX studies.',
                    'Sponsor framing positions remibrutinib as the potential first-in-class oral BTK treatment for CSU in a decade.',
                ],
                'safety': [
                    'Well-tolerated with a favorable safety profile; liver function tests balanced between active and placebo arms across both studies (sponsor press release).',
                ],
                'source_citations': ['raw/sponsors/btk/remibrutinib/2023-phase-iii-primary-endpoints-press-release.md'],
            },
            {
                'label': 'Novartis 52-week sustained efficacy and safety press release (May 2024)',
                'result_status': 'Sponsor press release',
                'efficacy': [
                    'UAS7 improvements observed as early as week 1 and sustained to week 52 in both REMIX-1 and REMIX-2.',
                    'At week 24, placebo-to-remibrutinib crossover patients showed response as early as 1 week after switching, sustained to end of study.',
                    'Almost half of patients were completely free of itch and hives (UAS7 = 0) at week 52 (sponsor press release; manuscript-level detail in PMID 41115533).',
                ],
                'safety': [
                    'Favorable and consistent safety profile up to 52 weeks; liver transaminase elevations balanced across arms, all asymptomatic, transient, and reversible.',
                    'AEs, SAEs, and treatment discontinuations due to AEs comparable between remibrutinib and placebo during the 24-week placebo-controlled period; exposure-adjusted rates did not increase with long-term treatment.',
                ],
                'source_citations': ['raw/sponsors/btk/remibrutinib/2024-sustained-efficacy-and-safety-press-release.md'],
            },
            {
                'label': 'Novartis RemIND CIndU Phase III press release (February 2026)',
                'result_status': 'Sponsor press release',
                'efficacy': [
                    'Remibrutinib described as the first therapy to achieve a Phase III primary endpoint in CIndU.',
                    'Statistically significant and clinically meaningful complete response rates versus placebo at week 12 in all three CIndU subtypes: symptomatic dermographism, cold urticaria, and cholinergic urticaria.',
                    'sNDA submitted to FDA for symptomatic dermographism based on RemIND results.',
                ],
                'safety': [
                    'Well-tolerated with no liver safety concerns reported in topline release.',
                ],
                'source_citations': ['raw/sponsors/btk/remibrutinib/2026-cindu-phase-iii-remind-press-release.md'],
            },
        ],
    },
    'rilzabrutinib': {
        'headline': 'Sponsor press release and conference poster provide additional detail beyond the primary manuscript for RILECSU Phase 2.',
        'entries': [
            {
                'label': 'Sanofi RILECSU Phase 2 press release (February 2024)',
                'result_status': 'Sponsor press release',
                'efficacy': [
                    'Rilzabrutinib 400 mg TID (ITT population): significant ISS7 reduction at week 12 (LSM -9.58 vs -6.31 placebo; P = 0.0181).',
                    'Significant UAS7 reduction at week 12 (LSM -17.95 vs -11.20; P = 0.0116).',
                    'Significant HSS7 reduction at week 12 (LSM -8.31 vs -4.89; P < 0.01).',
                    'Significant ISS7 changes observed as early as week 1.',
                ],
                'safety': [
                    'No events of cytopenia, bleeding, or atrial fibrillation (distinguishing from older BTK inhibitors).',
                    'Most common TEAEs (TID): diarrhea 29.3%, nausea 19.5%, headache 9.8%.',
                ],
                'source_citations': ['raw/sponsors/btk/rilzabrutinib/phase-2-csu-results-press-release.md'],
            },
            {
                'label': 'RILECSU Phase 2 hives poster (AAAAI 2024)',
                'result_status': 'Conference poster',
                'efficacy': [
                    'Significant and sustained improvements in UAS7 through week 12 with rilzabrutinib 1200 mg/day.',
                    'Nominally significant improvements in percent change in HSS7 as early as week 1 with all rilzabrutinib doses.',
                ],
                'safety': [],
                'source_citations': ['raw/sponsors/btk/rilzabrutinib/rilecsu-phase-2-hives-poster.md'],
            },
        ],
    },
}

PROGRAM_OPERATIONAL_OVERRIDES = {
    'sep-631': {
        'rows': [
            {
                'trial': 'Planned Phase 2b CSU study (sponsor slide deck)',
                'arms': '5',
                'dose_regimens': '4',
                'enrollment': 'NR',
                'per_arm_summary': '4 active SEP-631 oral QD dose levels plus placebo; enrollment not disclosed in current source.',
            },
        ],
        'notes': [
            'Septerna corporate slide deck page 25 describes a planned global, randomized, double-blind, placebo-controlled Phase 2b CSU study with 4 SEP-631 oral QD dose levels plus placebo, adults 18 to 65 years who remain symptomatic on second-generation H1 antihistamine therapy, and change from baseline in UAS7 at week 12 as the primary endpoint.',
        ],
    },
}

EFFICACY_SUMMARY_OVERRIDES: dict[str, dict] = {
    'barzolvolimab': {
        'tier': 'Rich CSU efficacy layer',
        'headline': 'Deep KIT-sponsored CSU efficacy package with manuscript-backed phase 2 activity and unusually rich sponsor-poster durability follow-up.',
        'strengths': [
            'Phase 2 CSU evidence is no longer just a week-12 story: the local sponsor layer extends into week-52 control, patient-reported disease control, and post-treatment follow-up framing.',
            'The newly cached EADV 2025 poster supports similar activity in low-IgE and normal/high-IgE subgroups, which matters strategically because low-IgE CSU is often discussed as a harder-to-treat biology.',
            'Current local read: one of the strongest public non-BTK CSU efficacy packages in the vault, with clearer durability and subgroup texture than most peers.',
        ],
        'evidence_note': 'Manuscript-backed plus deep sponsor-poster layer',
        'sources': [
            'wiki/programs/barzolvolimab.md',
            'wiki/trials/barzolvolimab-nct05368285.md',
        ],
    },
    'remibrutinib': {
        'tier': 'Rich CSU efficacy layer',
        'headline': 'Richest BTK CSU package in the vault, spanning phase 2b signal, pivotal phase 3 confirmation, and 52-week follow-up.',
        'strengths': [
            'Phase 2b and REMIX phase 3 manuscripts together support rapid symptom reduction, clear week-12 efficacy, and sustained benefit through week 52.',
            'Sponsor press releases add useful topline framing around rapid onset, durability, and the newer CIndU expansion without replacing the manuscript-backed CSU core.',
            'Current local read: the most mature oral BTK urticaria efficacy story in the vault.',
        ],
        'evidence_note': 'Primarily manuscript-backed, with sponsor support for topline framing and CIndU expansion',
        'sources': [
            'wiki/programs/remibrutinib.md',
            'wiki/trials/remibrutinib-nct03926611-phase-2b.md',
        ],
    },
    'rilzabrutinib': {
        'tier': 'Meaningful mid-depth CSU efficacy layer',
        'headline': 'Credible Phase 2 CSU signal with early itch improvement, but still shallower and less mature than remibrutinib or barzolvolimab.',
        'strengths': [
            'The local stack supports week-12 ISS7, UAS7, and HSS7 improvement in RILECSU, with week-1 itch signal visible in sponsor materials.',
            'Evidence remains phase-2-weighted and sponsor/manuscript coverage is narrower than the two flagship programs.',
        ],
        'evidence_note': 'Phase 2 manuscript plus sponsor press release/poster support',
        'sources': [
            'wiki/programs/rilzabrutinib.md',
            'wiki/trials/rilzabrutinib-nct05107115.md',
        ],
    },
    'evo756': {
        'tier': 'Earlier proof-of-concept layer',
        'headline': 'Mechanistic and proof-of-concept signal is visible, but mature CSU efficacy still sits below the flagship programs.',
        'strengths': [
            'Sponsor-backed healthy-volunteer and early urticaria program materials support target engagement and proof-of-concept logic.',
            'Current local read: promising but earlier and less clinically mature than the leading CSU programs.',
        ],
        'evidence_note': 'Mostly sponsor-sourced early program evidence',
        'sources': ['wiki/programs/evo756.md'],
    },
    'sep-631': {
        'tier': 'Earlier proof-of-mechanism layer',
        'headline': 'Strong mechanistic wheal-inhibition signal, but no mature public CSU efficacy package yet in the local layer.',
        'strengths': [
            'The AAAAI 2026 poster supports proof-of-mechanism and once-daily oral development logic.',
            'Current local read: intriguing early mechanism story, not yet a mature clinical-efficacy competitor in public data.',
        ],
        'evidence_note': 'Sponsor-poster proof-of-mechanism data',
        'sources': ['wiki/programs/sep-631.md'],
    },
    'ep262': {
        'tier': 'Weak / negative public efficacy layer',
        'headline': 'Current local public result layer is unfavorable after posted CT.gov phase 2 results failed to separate from placebo.',
        'strengths': [
            'The active-versus-placebo signal does not currently support a strong efficacy narrative in the vault.',
        ],
        'evidence_note': 'CT.gov posted results with negative topline read',
        'sources': ['wiki/trials/ep262-nct06077773.md'],
    },
    'blu-808': {
        'tier': 'Immature public efficacy layer',
        'headline': 'Mechanism and ownership context are clearer now, but mature urticaria efficacy remains thin in the current public source stack.',
        'strengths': [
            'Current local value is mostly program tracking and source capture rather than efficacy interpretation.',
        ],
        'evidence_note': 'Program-tracking layer only',
        'sources': ['wiki/programs/blu-808.md'],
    },
    'fenebrutinib': {
        'tier': 'Moderate historical efficacy layer',
        'headline': 'Historical BTK efficacy signal exists, but the current local layer is still thinner and less operationally useful than remibrutinib.',
        'strengths': [
            'Useful as a competitor/historical comparator, but not the flagship efficacy story in this vault.',
        ],
        'evidence_note': 'Publication-backed historical competitor layer',
        'sources': ['wiki/programs/fenebrutinib.md'],
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
    if program_entry.get('program_key') == 'blu-808':
        return 'Blueprint Medicines (acquired by Sanofi)'
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


def get_trial_result_override(trial_id: str) -> dict:
    return TRIAL_RESULT_OVERRIDES.get(trial_id, {})


def get_program_operational_override(program_key: str) -> dict:
    return PROGRAM_OPERATIONAL_OVERRIDES.get(program_key, {})


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

    result_trials = []
    for trial in program_entry.get('ctgov_trials', []):
        r = get_trial_result_override(trial['trial_id'])
        if r:
            result_trials.append((trial, r))
    if result_trials:
        lines.extend(['## Program Results Summary', ''])
        lines.append(f"Trials with source-backed results in the current local layer: {len(result_trials)} of {len(program_entry.get('ctgov_trials', []))}")
        lines.append('')
        for trial, r in result_trials:
            link_name = trial_link_name(program_entry['program_key'], trial['trial_id'], trial_slug_map)
            lines.append(f"**[{trial['trial_id']}](../trials/{link_name})** ({r.get('result_status', 'NR')})")
            if r.get('efficacy'):
                lines.append(f"- {r['efficacy'][0]}")
            if r.get('safety'):
                lines.append(f"- {r['safety'][0]}")
            if r.get('source_citations'):
                lines.append(f"- Sources: {'; '.join(r['source_citations'])}")
            lines.append('')

    sponsor_results = PROGRAM_SPONSOR_RESULTS.get('remibrutinib')
    if sponsor_results:
        lines.append(f"### Sponsor-sourced result evidence")
        lines.append('')
        lines.append(f"_{sponsor_results['headline']}_")
        lines.append('')
        for entry in sponsor_results['entries']:
            lines.append(f"**{entry['label']}** ({entry['result_status']})")
            if entry.get('efficacy'):
                for item in entry['efficacy']:
                    lines.append(f'- {item}')
            if entry.get('safety'):
                for item in entry['safety']:
                    lines.append(f'- Safety: {item}')
            if entry.get('source_citations'):
                lines.append(f"- Source(s): {'; '.join(entry['source_citations'])}")
            lines.append('')

    lines.extend([
        '## Longitudinal efficacy view',
        '- Plotted page: [Remibrutinib longitudinal UAS7](../queries/remibrutinib-longitudinal-uas7.md)',
        '- Current explicit numeric plotting coverage: derived mean UAS7 through weeks 0, 1, 2, 4, 12, and 24 for REMIX-1 and REMIX-2 separately.',
        '- Current responder plotting coverage: per-trial UAS7 <= 6 through weeks 1, 2, 12, and 24, plus pooled week 52 landmarks where explicit values were available.',
        '- Current main gap: exact week 52 mean UAS7 and per-trial week 52 UAS7 <= 6 values are still graph-only in the current local extraction and remain intentionally unplotted.',
        '- Local data backbone: `data/remibrutinib_longitudinal_uas7.json` and `data/remibrutinib_longitudinal_uas7_notes.md`.',
        '',
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
    program_operational = get_program_operational_override(program_entry['program_key'])
    for row in program_operational.get('rows', []):
        lines.append(
            f"| {row['trial']} | {row['arms']} | {row['dose_regimens']} | {row['enrollment']} | {row['per_arm_summary']} |"
        )
    for note in program_operational.get('notes', []):
        lines.extend(['', f'- {note}'])
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

    result_trials = []
    for trial in program_entry.get('ctgov_trials', []):
        r = get_trial_result_override(trial['trial_id'])
        if r:
            result_trials.append((trial, r))
    if result_trials:
        lines.extend(['', '## Program Results Summary', ''])
        lines.append(f"Trials with source-backed results in the current local layer: {len(result_trials)} of {len(program_entry.get('ctgov_trials', []))}")
        lines.append('')
        for trial, r in result_trials:
            link_name = trial_link_name(program_entry['program_key'], trial['trial_id'], trial_slug_map)
            lines.append(f"**[{trial['trial_id']}](../trials/{link_name})** ({r.get('result_status', 'NR')})")
            if r.get('efficacy'):
                lines.append(f"- {r['efficacy'][0]}")
            if r.get('safety'):
                lines.append(f"- {r['safety'][0]}")
            if r.get('source_citations'):
                lines.append(f"- Sources: {'; '.join(r['source_citations'])}")
            lines.append('')

    sponsor_results = PROGRAM_SPONSOR_RESULTS.get(program_entry['program_key'])
    if sponsor_results:
        if not result_trials:
            lines.extend(['', '## Program Results Summary', ''])
            lines.append('No CT.gov-linked trial in this program has a manuscript-backed result override yet.')
            lines.append('')
        lines.append(f"### Sponsor-sourced result evidence")
        lines.append('')
        lines.append(f"_{sponsor_results['headline']}_")
        lines.append('')
        for entry in sponsor_results['entries']:
            lines.append(f"**{entry['label']}** ({entry['result_status']})")
            if entry.get('efficacy'):
                for item in entry['efficacy']:
                    lines.append(f'- {item}')
            if entry.get('safety'):
                for item in entry['safety']:
                    lines.append(f'- Safety: {item}')
            if entry.get('source_citations'):
                lines.append(f"- Source(s): {'; '.join(entry['source_citations'])}")
            lines.append('')

    if program_entry['program_key'] == 'barzolvolimab':
        lines.extend([
            '## Longitudinal efficacy view',
            '- Plotted page: [Barzolvolimab longitudinal UAS7](../queries/barzolvolimab-longitudinal-uas7.md)',
            '- Current explicit numeric plotting coverage: week 12 UAS7 change-from-baseline by core randomized arm, plus week 12 and week 52 UAS7 <= 6 and UAS7 = 0 landmarks.',
            '- Current main caveat: the week 52 values for the former 75 mg and placebo groups are post-week-16 transition-group landmarks, not unchanged original-arm trajectories.',
            '- Current main gap: the full week-by-week mean UAS7 curve is still graph-only in the current local extraction and remains intentionally unplotted.',
            '- Local data backbone: `data/barzolvolimab_longitudinal_uas7.json` and `data/barzolvolimab_longitudinal_uas7_notes.md`.',
            '',
        ])
    if program_entry['program_key'] == 'rilzabrutinib':
        lines.extend([
            '## Longitudinal efficacy view',
            '- Plotted page: [Rilzabrutinib longitudinal UAS7](../queries/rilzabrutinib-longitudinal-uas7.md)',
            '- Current explicit numeric plotting coverage: randomized-arm UAS7 change-from-baseline landmarks at weeks 4 and 12, plus 1200 mg/day versus placebo UAS7 difference landmarks at weeks 1, 4, and 12.',
            '- Current responder plotting coverage: week 12 UAS7 <= 6 and UAS7 = 0 snapshot for placebo versus rilzabrutinib 1200 mg/day.',
            '- Current main gap: the current local extraction still does not support a safely tabulated four-arm week-by-week UAS7 curve or richer long-term CSU durability numerics.',
            '- Local data backbone: `data/rilzabrutinib_longitudinal_uas7.json` and `data/rilzabrutinib_longitudinal_uas7_notes.md`.',
            '',
        ])

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

    result = get_trial_result_override(ct['nct_id'])
    if result:
        lines.extend(['', '## Key Efficacy and Safety Findings'])
        lines.append(f"- Result status: {result.get('result_status', 'NR')}")
        if result.get('efficacy'):
            lines.extend(['', '### Efficacy'])
            for item in result['efficacy']:
                lines.append(f'- {item}')
        if result.get('safety'):
            lines.extend(['', '### Safety'])
            for item in result['safety']:
                lines.append(f'- {item}')
        if result.get('source_citations'):
            lines.extend(['', '### Result source(s)'])
            for cite in result['source_citations']:
                lines.append(f'- {cite}')

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
        '- Derived efficacy view: [Cross-program efficacy summary](../queries/cross-program-efficacy-summary.md)',
        '- Derived longitudinal view: [Remibrutinib longitudinal UAS7](../queries/remibrutinib-longitudinal-uas7.md)',
        '- Derived longitudinal view: [Barzolvolimab longitudinal UAS7](../queries/barzolvolimab-longitudinal-uas7.md)',
        '- Derived longitudinal view: [Rilzabrutinib longitudinal UAS7](../queries/rilzabrutinib-longitudinal-uas7.md)',
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

    efficacy_lines = [
        '---',
        'title: Cross-program efficacy summary',
        'tags:',
        '  - type/query',
        '---',
        '# Cross-program efficacy summary',
        '',
        'This page is a conservative derived read across the current local source stack. It is meant to answer a practical question: which programs currently have the clearest public efficacy story, and which still look early, thin, or weak?',
        '',
        '- First plotted longitudinal page now live: [Remibrutinib longitudinal UAS7](../queries/remibrutinib-longitudinal-uas7.md)',
        '- New plotted longitudinal landmarks: [Barzolvolimab longitudinal UAS7](../queries/barzolvolimab-longitudinal-uas7.md)',
        '- New plotted longitudinal landmarks: [Rilzabrutinib longitudinal UAS7](../queries/rilzabrutinib-longitudinal-uas7.md)',
        '',
        '| Program | Class | Current read | Evidence type | Program page |',
        '|---|---|---|---|---|',
    ]
    ordered_program_keys = [
        'remibrutinib',
        'barzolvolimab',
        'rilzabrutinib',
        'fenebrutinib',
        'evo756',
        'sep-631',
        'ep262',
        'blu-808',
    ]
    program_by_key = {program['program_key']: program for program in programs}
    for key in ordered_program_keys:
        program = program_by_key.get(key)
        summary = EFFICACY_SUMMARY_OVERRIDES.get(key)
        if not program or not summary:
            continue
        efficacy_lines.append(
            f"| [{program['display_name']}](../programs/{key}.md) | {', '.join(program.get('priority_classes', [])) or 'NR'} | {summary['tier']} | {summary['evidence_note']} | [open](../programs/{key}.md) |"
        )
    efficacy_lines.extend([
        '',
        '## Quick read',
        '- **Current flagship CSU efficacy pages:** remibrutinib and barzolvolimab.',
        '- **Most mature oral BTK CSU story:** remibrutinib.',
        '- **Deepest KIT sponsor-poster durability/subgroup story:** barzolvolimab.',
        '- **Current plotted longitudinal pages:** remibrutinib, barzolvolimab, and rilzabrutinib.',
        '- **Meaningful but shallower Phase 2 CSU story:** rilzabrutinib, now with a landmark-based plotted page but still a thinner numeric time-series layer than the two flagship programs.',
        '- **Earlier proof-of-concept / mechanism layer:** EVO756 and SEP-631.',
        '- **Currently weak or immature public efficacy layer:** EP262, BLU-808, and other thin public programs.',
        '',
        '## Program-by-program notes',
        '',
    ])
    for key in ordered_program_keys:
        program = program_by_key.get(key)
        summary = EFFICACY_SUMMARY_OVERRIDES.get(key)
        if not program or not summary:
            continue
        efficacy_lines.append(f"### {program['display_name']}")
        efficacy_lines.append(f"- Current read: {summary['headline']}")
        efficacy_lines.append(f"- Evidence type: {summary['evidence_note']}")
        efficacy_lines.append('- Why this matters:')
        for item in summary.get('strengths', []):
            efficacy_lines.append(f"  - {item}")
        if summary.get('sources'):
            efficacy_lines.append(f"- Key local pages: {'; '.join(f'`{src}`' for src in summary['sources'])}")
        efficacy_lines.append('')
    write_text(QUERIES_DIR / 'cross-program-efficacy-summary.md', '\n'.join(efficacy_lines))


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
