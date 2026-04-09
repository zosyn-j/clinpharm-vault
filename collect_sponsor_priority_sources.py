#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from lxml import html as lxml_html

BASE = Path('/home/jordon/.openclaw/workspace/research-db/csu-cindu-db-v2')
RAW_DIR = BASE / 'raw' / 'sponsors'
INV_DIR = BASE / 'inventories'
FETCHED_AT = datetime.now(timezone.utc).isoformat()

SOURCES = [
    # BTK - Novartis / remibrutinib
    {'program': 'remibrutinib', 'priority_class': 'BTK', 'sponsor': 'Novartis', 'kind': 'html', 'label': '2023 Phase III primary endpoints press release', 'url': 'https://www.novartis.com/news/media-releases/novartis-remibrutinib-phase-iii-trials-met-their-primary-endpoints-and-showed-rapid-symptom-control-chronic-spontaneous-urticaria'},
    {'program': 'remibrutinib', 'priority_class': 'BTK', 'sponsor': 'Novartis', 'kind': 'html', 'label': '2024 sustained efficacy and safety press release', 'url': 'https://www.novartis.com/news/media-releases/novartis-phase-iii-data-confirm-sustained-efficacy-and-long-term-safety-oral-remibrutinib-chronic-spontaneous-urticaria'},
    {'program': 'remibrutinib', 'priority_class': 'BTK', 'sponsor': 'Novartis', 'kind': 'html', 'label': '2026 CIndU Phase III RemIND press release', 'url': 'https://www.novartis.com/news/media-releases/novartis-remibrutinib-first-therapy-achieve-phase-iii-primary-endpoint-chronic-inducible-urticaria-cindu'},
    {'program': 'remibrutinib', 'priority_class': 'BTK', 'sponsor': 'Novartis', 'kind': 'html', 'label': 'Novartis trial page NCT06865651', 'url': 'https://www.novartis.com/clinicaltrials/study/nct06865651'},
    {'program': 'rilzabrutinib', 'priority_class': 'BTK', 'sponsor': 'Sanofi', 'kind': 'html', 'label': 'Sanofi pipeline page', 'url': 'https://www.sanofi.com/en/our-science/our-pipeline'},

    # KIT
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'html', 'label': 'IR press release positive results', 'url': 'https://ir.celldex.com/news-releases/news-release-details/celldex-therapeutics-presents-positive-results-barzolvolimab'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'html', 'label': 'IR press release additional positive data', 'url': 'https://ir.celldex.com/news-releases/news-release-details/celldex-presents-additional-positive-data-demonstrating'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'pdf', 'label': 'AAAAI 2025 CSU poster', 'url': 'https://celldex.com/wp-content/uploads/2025/06/AAAAI-2025-CSU-posterL11.pdf'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'pdf', 'label': 'Phase 2 CIndU ACAAI poster', 'url': 'https://celldex.com/wp-content/uploads/2025/06/Barzolvolimab_Phase-2-ClndU_ACAAI_FINAL.pdf'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'pdf', 'label': 'EADV 2024 congress presentation', 'url': 'https://celldex.com/wp-content/uploads/2025/06/CLDX_EADV2024_Congress_Presentation.pdf'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'sponsor': 'Celldex', 'kind': 'pdf', 'label': 'IR press release PDF additional data', 'url': 'https://ir.celldex.com/node/16446/pdf'},
    {'program': 'blu-808', 'priority_class': 'KIT', 'sponsor': 'Blueprint Medicines', 'kind': 'html', 'label': 'Core programs page', 'url': 'https://www.blueprintmedicines.com/pipeline/core-programs/'},
    {'program': 'blu-808', 'priority_class': 'KIT', 'sponsor': 'Blueprint Medicines', 'kind': 'html', 'label': 'AAAAI WAO 2025 publications page', 'url': 'https://www.blueprintmedicines.com/publications/2025-american-academy-of-allergy-asthma-immunology-aaaai-world-allergy-organization-wao-joint-congress-10/'},
    {'program': 'blu-808', 'priority_class': 'KIT', 'sponsor': 'Blueprint Medicines', 'kind': 'pdf', 'label': 'AAAAI WAO 2025 BLU-808 WT KIT poster', 'url': 'https://www.blueprintmedicines.com/wp-content/uploads/2025/02/Blueprint-Medicines-AAAAI-WAO-2025-BLU-808-Wild-Type-KIT-Inhibitor-Poster.pdf'},
    {'program': 'blu-808', 'priority_class': 'KIT', 'sponsor': 'Blueprint Medicines', 'kind': 'pdf', 'label': 'AAAAI 2024 BLU-808 WT KIT poster', 'url': 'https://www.blueprintmedicines.com/wp-content/uploads/2024/02/Blueprint-Medicines-AAAAI-2024-BLU-808-Wild-Type-KIT-Mast-Cell-Disorders-Poster.pdf'},
    {'program': 'briquilimab', 'priority_class': 'KIT', 'sponsor': 'Jasper Therapeutics', 'kind': 'html', 'label': 'Briquilimab program page', 'url': 'https://jaspertx.com/briquilimab/'},

    # MRGPRX2
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'html', 'label': 'MRGPRX2 antagonist program page', 'url': 'https://www.evommune.com/mrgprx2-antagonist/'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'html', 'label': 'Clinical trials page', 'url': 'https://www.evommune.com/clinical-trials/'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'pdf', 'label': 'CIndU Phase 2 trial initiation PDF', 'url': 'https://www.evommune.com/wp-content/uploads/2024/09/21_Evommune_EVO756_CindU_Phase_2_Trial.pdf'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'pdf', 'label': 'GA2LEN 2024 trial results presentation PDF', 'url': 'https://www.evommune.com/wp-content/uploads/2024/12/23_Evommune_EVO756_Trial_Results_Preso.pdf'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'pdf', 'label': 'CSU Phase 2b trial initiation PDF', 'url': 'https://www.evommune.com/wp-content/uploads/2025/04/25_Evommune_756_CSU_Phase_2_Trial_Initiation.pdf'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'pdf', 'label': 'CIndU top-line press release PDF', 'url': 'https://www.evommune.com/wp-content/uploads/2025/05/26b_Evommune_CIndU_Press_Release.pdf'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'sponsor': 'Evommune', 'kind': 'pdf', 'label': 'EADV 2025 CIndU presentation PDF', 'url': 'https://www.evommune.com/wp-content/uploads/2025/09/29b_Evommune_EADV_CIndU_091925.pdf'},
    {'program': 'sep-631', 'priority_class': 'MRGPRX2', 'sponsor': 'Septerna', 'kind': 'html', 'label': 'Pipeline page', 'url': 'https://septerna.com/pipeline/'},
    {'program': 'sep-631', 'priority_class': 'MRGPRX2', 'sponsor': 'Septerna', 'kind': 'pdf', 'label': 'AAAAI 2026 poster PDF', 'url': 'https://www.septerna.com/wp-content/uploads/2026.03.01_SEP-631-AAAAI-2026-Poster_FINAL.pdf'},
    {'program': 'ep262', 'priority_class': 'MRGPRX2', 'sponsor': 'Escient Pharmaceuticals', 'kind': 'html', 'label': 'Pipeline page', 'url': 'https://www.escientpharma.com/programs/pipeline/'},
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def ensure_dirs() -> None:
    for src in SOURCES:
        program_dir = RAW_DIR / src['priority_class'].lower() / slugify(src['program'])
        program_dir.mkdir(parents=True, exist_ok=True)
    INV_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    text = text.replace('\r', '')
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip() + '\n'


def save_html_source(src: dict) -> dict:
    program_dir = RAW_DIR / src['priority_class'].lower() / slugify(src['program'])
    stem = slugify(src['label'])
    html_path = program_dir / f'{stem}.html'
    md_path = program_dir / f'{stem}.md'

    r = requests.get(src['url'], timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    html_path.write_text(r.text)

    tree = lxml_html.fromstring(r.content)
    text = tree.text_content()
    text = normalize_text(text)

    md = []
    md.append(f"# {src['label']}")
    md.append('')
    md.append(f"- Program: {src['program']}")
    md.append(f"- Priority class: {src['priority_class']}")
    md.append(f"- Sponsor: {src['sponsor']}")
    md.append(f"- Source URL: {src['url']}")
    md.append(f"- Fetched at: {FETCHED_AT}")
    md.append(f"- Raw HTML: {html_path.name}")
    md.append('')
    md.append('## Extracted page text')
    md.append('')
    md.append('```text')
    md.append(text)
    md.append('```')
    md_path.write_text('\n'.join(md))

    return {
        **src,
        'status': 'ok',
        'saved_files': [str(html_path.relative_to(BASE)), str(md_path.relative_to(BASE))],
    }


def save_pdf_source(src: dict) -> dict:
    program_dir = RAW_DIR / src['priority_class'].lower() / slugify(src['program'])
    stem = slugify(src['label'])
    parsed = urlparse(src['url'])
    ext = Path(parsed.path).suffix or '.pdf'
    pdf_path = program_dir / f'{stem}{ext}'
    txt_path = program_dir / f'{stem}.txt'
    md_path = program_dir / f'{stem}.md'

    r = requests.get(src['url'], timeout=90, headers={'User-Agent': 'Mozilla/5.0'})
    r.raise_for_status()
    pdf_path.write_bytes(r.content)

    subprocess.run(['pdftotext', '-layout', str(pdf_path), str(txt_path)], check=True)
    text = normalize_text(txt_path.read_text(errors='ignore'))

    md = []
    md.append(f"# {src['label']}")
    md.append('')
    md.append(f"- Program: {src['program']}")
    md.append(f"- Priority class: {src['priority_class']}")
    md.append(f"- Sponsor: {src['sponsor']}")
    md.append(f"- Source URL: {src['url']}")
    md.append(f"- Fetched at: {FETCHED_AT}")
    md.append(f"- Raw PDF: {pdf_path.name}")
    md.append(f"- Extracted text: {txt_path.name}")
    md.append('')
    md.append('## Extracted PDF text')
    md.append('')
    md.append('```text')
    md.append(text)
    md.append('```')
    md_path.write_text('\n'.join(md))

    return {
        **src,
        'status': 'ok',
        'saved_files': [str(pdf_path.relative_to(BASE)), str(txt_path.relative_to(BASE)), str(md_path.relative_to(BASE))],
    }


def main() -> None:
    ensure_dirs()
    results = []
    for src in SOURCES:
        try:
            if src['kind'] == 'html':
                results.append(save_html_source(src))
            elif src['kind'] == 'pdf':
                results.append(save_pdf_source(src))
            else:
                results.append({**src, 'status': 'unsupported'})
        except Exception as e:
            results.append({**src, 'status': 'error', 'error': repr(e)})

    (INV_DIR / 'sponsor_priority_sources.json').write_text(json.dumps({
        'fetched_at': FETCHED_AT,
        'results': results,
    }, indent=2))

    lines = []
    lines.append('# Sponsor priority-source inventory')
    lines.append('')
    lines.append(f'- Built: {FETCHED_AT}')
    lines.append('- Goal: raw sponsor-source cache for BTK, KIT, and MRGPRX2 urticaria programs')
    lines.append('- Format: HTML pages saved as raw HTML plus extracted Markdown text; PDFs saved as raw PDF plus pdftotext output plus Markdown wrapper')
    lines.append('')
    lines.append('| Priority class | Program | Sponsor | Label | Kind | Status | Local files |')
    lines.append('|---|---|---|---|---|---|---|')
    for r in results:
        files = '<br>'.join(r.get('saved_files', [])) if r.get('saved_files') else (r.get('error', ''))
        lines.append(f"| {r['priority_class']} | {r['program']} | {r['sponsor']} | {r['label']} | {r['kind']} | {r['status']} | {files} |")
    (INV_DIR / 'sponsor_priority_sources.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
