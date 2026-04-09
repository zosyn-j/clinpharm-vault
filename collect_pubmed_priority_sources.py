#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import requests

BASE = Path('/home/jordon/.openclaw/workspace/research-db/csu-cindu-db-v2')
RAW_DIR = BASE / 'raw' / 'publications'
SEARCH_DIR = RAW_DIR / 'searches'
PUBMED_XML_DIR = RAW_DIR / 'pubmed' / 'xml'
PUBMED_MD_DIR = RAW_DIR / 'pubmed' / 'markdown'
PMC_XML_DIR = RAW_DIR / 'pmc' / 'xml'
PMC_MD_DIR = RAW_DIR / 'pmc' / 'markdown'
INV_DIR = BASE / 'inventories'
FETCHED_AT = datetime.now(timezone.utc).isoformat()
NCBI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
HEADERS = {'User-Agent': 'OpenClaw/1.0 (local research cache)'}

QUERIES = [
    {'program': 'remibrutinib', 'priority_class': 'BTK', 'term': '(remibrutinib OR LOU064) AND urticaria'},
    {'program': 'fenebrutinib', 'priority_class': 'BTK', 'term': '(fenebrutinib OR GDC-0853) AND urticaria'},
    {'program': 'rilzabrutinib', 'priority_class': 'BTK', 'term': '(rilzabrutinib OR PRN1008) AND urticaria'},
    {'program': 'barzolvolimab', 'priority_class': 'KIT', 'term': '(barzolvolimab OR CDX-0159) AND urticaria'},
    {'program': 'briquilimab', 'priority_class': 'KIT', 'term': '(briquilimab OR JSP191) AND urticaria'},
    {'program': 'blu-808', 'priority_class': 'KIT', 'term': 'BLU-808 AND urticaria'},
    {'program': 'evo756', 'priority_class': 'MRGPRX2', 'term': 'EVO756 AND urticaria'},
    {'program': 'ep262', 'priority_class': 'MRGPRX2', 'term': 'EP262 AND urticaria'},
    {'program': 'sep-631', 'priority_class': 'MRGPRX2', 'term': 'SEP-631 AND urticaria'},
]


def ensure_dirs() -> None:
    for d in [SEARCH_DIR, PUBMED_XML_DIR, PUBMED_MD_DIR, PMC_XML_DIR, PMC_MD_DIR, INV_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def get(url: str, **params: Any) -> requests.Response:
    r = requests.get(url, params=params or None, headers=HEADERS, timeout=60)
    r.raise_for_status()
    time.sleep(0.34)
    return r


def text_or_none(elem: ET.Element | None) -> str | None:
    if elem is None:
        return None
    txt = ''.join(elem.itertext()).strip()
    return txt or None


def search_pubmed(term: str, retmax: int = 20) -> dict[str, Any]:
    r = get(f'{NCBI}/esearch.fcgi', db='pubmed', term=term, retmode='json', retmax=str(retmax), sort='relevance')
    return r.json()


def fetch_pubmed_xml(pmids: list[str]) -> str:
    r = get(f'{NCBI}/efetch.fcgi', db='pubmed', id=','.join(pmids), retmode='xml')
    return r.text


def fetch_pmc_xml(pmcid: str) -> str | None:
    try:
        r = get(f'{NCBI}/efetch.fcgi', db='pmc', id=pmcid, retmode='xml')
        if '<error>' in r.text.lower() or not r.text.strip():
            return None
        return r.text
    except Exception:
        return None


def parse_pubmed_article(article: ET.Element) -> dict[str, Any]:
    medline = article.find('MedlineCitation')
    article_meta = medline.find('Article') if medline is not None else None
    pmid = text_or_none(medline.find('PMID')) if medline is not None else None
    title = text_or_none(article_meta.find('ArticleTitle')) if article_meta is not None else None
    abstract_parts = []
    if article_meta is not None:
        for abst in article_meta.findall('.//Abstract/AbstractText'):
            label = abst.attrib.get('Label')
            txt = ''.join(abst.itertext()).strip()
            if txt:
                abstract_parts.append(f'{label}: {txt}' if label else txt)
    journal = text_or_none(article_meta.find('./Journal/Title')) if article_meta is not None else None
    pub_year = None
    if article_meta is not None:
        pub_year = text_or_none(article_meta.find('./Journal/JournalIssue/PubDate/Year'))
        if not pub_year:
            medline_date = text_or_none(article_meta.find('./Journal/JournalIssue/PubDate/MedlineDate'))
            pub_year = medline_date
    authors = []
    if article_meta is not None:
        for author in article_meta.findall('./AuthorList/Author'):
            ln = text_or_none(author.find('LastName'))
            ini = text_or_none(author.find('Initials'))
            coll = text_or_none(author.find('CollectiveName'))
            if coll:
                authors.append(coll)
            elif ln:
                authors.append(f'{ln} {ini or ""}'.strip())
    article_ids = {}
    for aid in article.findall('.//PubmedData/ArticleIdList/ArticleId'):
        idtype = aid.attrib.get('IdType')
        if idtype:
            article_ids[idtype] = ''.join(aid.itertext()).strip()
    publication_types = []
    if medline is not None:
        for pt in medline.findall('.//PublicationTypeList/PublicationType'):
            t = ''.join(pt.itertext()).strip()
            if t:
                publication_types.append(t)

    return {
        'pmid': pmid,
        'title': title,
        'journal': journal,
        'pub_year': pub_year,
        'authors': authors,
        'abstract': '\n\n'.join(abstract_parts).strip() or None,
        'article_ids': article_ids,
        'publication_types': publication_types,
    }


def write_pubmed_markdown(meta: dict[str, Any], xml_file: Path, query_info: dict[str, Any]) -> Path:
    pmid = meta['pmid']
    md_path = PUBMED_MD_DIR / f'PMID{pmid}.md'
    lines = []
    lines.append(f"# PMID {pmid} - {meta.get('title') or 'Untitled'}")
    lines.append('')
    lines.append(f"- Program seed: {query_info['program']}")
    lines.append(f"- Priority class: {query_info['priority_class']}")
    lines.append(f"- Search term: {query_info['term']}")
    lines.append(f"- Journal: {meta.get('journal') or 'NR'}")
    lines.append(f"- Year: {meta.get('pub_year') or 'NR'}")
    lines.append(f"- Authors: {', '.join(meta.get('authors') or []) or 'NR'}")
    lines.append(f"- PMID: {pmid}")
    if meta['article_ids'].get('doi'):
        lines.append(f"- DOI: {meta['article_ids']['doi']}")
    if meta['article_ids'].get('pmc'):
        lines.append(f"- PMCID: {meta['article_ids']['pmc']}")
    lines.append(f"- PubMed URL: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
    lines.append(f"- Raw XML: {xml_file.name}")
    lines.append(f"- Fetched at: {FETCHED_AT}")
    lines.append('')
    lines.append('## Publication types')
    if meta.get('publication_types'):
        lines.extend(f'- {x}' for x in meta['publication_types'])
    else:
        lines.append('- none listed')
    lines.append('')
    lines.append('## Abstract text')
    lines.append('')
    lines.append('```text')
    lines.append(meta.get('abstract') or 'No abstract text available in fetched PubMed record.')
    lines.append('```')
    md_path.write_text('\n'.join(lines))
    return md_path


def write_pmc_markdown(pmcid: str, xml_text: str, program: str, priority_class: str) -> Path:
    md_path = PMC_MD_DIR / f'{pmcid}.md'
    try:
        root = ET.fromstring(xml_text)
        title = text_or_none(root.find('.//article-title')) or pmcid
        body_parts = []
        for p in root.findall('.//body//p'):
            p_text = ''.join(p.itertext()).strip()
            if p_text:
                body_parts.append(p_text)
        body_text = '\n\n'.join(body_parts)
    except Exception:
        title = pmcid
        body_text = xml_text
    lines = []
    lines.append(f'# {pmcid} - {title}')
    lines.append('')
    lines.append(f'- Program seed: {program}')
    lines.append(f'- Priority class: {priority_class}')
    lines.append(f'- PMCID: {pmcid}')
    lines.append(f'- PMC URL: https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/')
    lines.append(f'- Fetched at: {FETCHED_AT}')
    lines.append('')
    lines.append('## Full text (PMC XML-derived body text)')
    lines.append('')
    lines.append('```text')
    lines.append(body_text or 'No body text parsed from PMC XML.')
    lines.append('```')
    md_path.write_text('\n'.join(lines))
    return md_path


def main() -> None:
    ensure_dirs()
    search_manifest = []
    seen_pmids: dict[str, dict[str, Any]] = {}
    inventory = []

    for query in QUERIES:
        search = search_pubmed(query['term'])
        ids = search.get('esearchresult', {}).get('idlist', [])
        search_record = {
            **query,
            'fetched_at': FETCHED_AT,
            'count': len(ids),
            'ids': ids,
            'search_url': f"https://pubmed.ncbi.nlm.nih.gov/?term={quote_plus(query['term'])}",
            'raw': search,
        }
        SEARCH_DIR.joinpath(f"{query['priority_class'].lower()}__{slugify(query['program'])}.json").write_text(json.dumps(search_record, indent=2))
        search_manifest.append(search_record)

        if not ids:
            continue

        xml_text = fetch_pubmed_xml(ids)
        root = ET.fromstring(xml_text)
        for article in root.findall('./PubmedArticle'):
            meta = parse_pubmed_article(article)
            pmid = meta.get('pmid')
            if not pmid:
                continue
            if pmid in seen_pmids:
                seen_pmids[pmid]['search_terms'].append(query['term'])
                continue
            xml_file = PUBMED_XML_DIR / f'PMID{pmid}.xml'
            xml_file.write_text(ET.tostring(article, encoding='unicode'))
            md_file = write_pubmed_markdown(meta, xml_file, query)
            pmc_md = None
            pmcid = meta.get('article_ids', {}).get('pmc')
            pmc_xml_file = None
            if pmcid:
                pmc_xml = fetch_pmc_xml(pmcid)
                if pmc_xml:
                    pmc_xml_file = PMC_XML_DIR / f'{pmcid}.xml'
                    pmc_xml_file.write_text(pmc_xml)
                    pmc_md = write_pmc_markdown(pmcid, pmc_xml, query['program'], query['priority_class'])
            rec = {
                'priority_class': query['priority_class'],
                'program_seed': query['program'],
                'search_terms': [query['term']],
                'pmid': pmid,
                'title': meta.get('title'),
                'journal': meta.get('journal'),
                'pub_year': meta.get('pub_year'),
                'doi': meta.get('article_ids', {}).get('doi'),
                'pmcid': pmcid,
                'publication_types': meta.get('publication_types', []),
                'pubmed_markdown': str(md_file.relative_to(BASE)),
                'pubmed_xml': str(xml_file.relative_to(BASE)),
                'pmc_markdown': str(pmc_md.relative_to(BASE)) if pmc_md else None,
                'pmc_xml': str(pmc_xml_file.relative_to(BASE)) if pmc_xml_file else None,
                'pubmed_url': f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
                'pmc_url': f'https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/' if pmcid else None,
            }
            inventory.append(rec)
            seen_pmids[pmid] = rec

    inventory.sort(key=lambda x: (x['priority_class'], x['program_seed'], int(x['pub_year'][:4]) if x.get('pub_year') and x['pub_year'][:4].isdigit() else 0, x['pmid']))
    INV_DIR.joinpath('publication_priority_sources.json').write_text(json.dumps({
        'fetched_at': FETCHED_AT,
        'queries': [{k: v for k, v in q.items() if k != 'raw'} for q in search_manifest],
        'records': inventory,
    }, indent=2))

    lines = []
    lines.append('# Publication priority-source inventory')
    lines.append('')
    lines.append(f'- Built: {FETCHED_AT}')
    lines.append('- Source system: PubMed via NCBI E-utilities, with PMC XML full text when available')
    lines.append('- Goal: preserve original publication/abstract text locally for precise future citations')
    lines.append('')
    lines.append('| Priority class | Program seed | PMID | Year | Journal | PMCID | PubMed cache | PMC cache |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for rec in inventory:
        lines.append(
            f"| {rec['priority_class']} | {rec['program_seed']} | {rec['pmid']} | {rec.get('pub_year') or 'NR'} | {rec.get('journal') or 'NR'} | {rec.get('pmcid') or 'NR'} | [md](../{rec['pubmed_markdown']}) | {('[md](../' + rec['pmc_markdown'] + ')') if rec.get('pmc_markdown') else 'NR'} |"
        )
    lines.append('')
    lines.append('## Query terms used')
    for q in search_manifest:
        lines.append(f"- {q['priority_class']} / {q['program']}: `{q['term']}` ({q['count']} PubMed hits)")
    INV_DIR.joinpath('publication_priority_sources.md').write_text('\n'.join(lines))


if __name__ == '__main__':
    main()
