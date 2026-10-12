#!/usr/bin/env python3
"""Validate local catalog structure and generated documentation (no network)."""
import datetime
import json
import pathlib
import re
import sys
from urllib.parse import unquote, urlsplit

from build_catalog import ROOT, render, slug

errors = []
def require(condition, message):
    if not condition:
        errors.append(message)

def date(value, label):
    try:
        return datetime.date.fromisoformat(value)
    except (ValueError, TypeError):
        errors.append(f'{label}: invalid ISO date {value!r}')
        return datetime.date.min

catalog = json.loads((ROOT/'data/catalog.json').read_text())
projects = json.loads((ROOT/'data/projects.json').read_text())
cutoff = date(catalog['as_of'], 'catalog cutoff')
sections = {s['id'] for s in catalog['sections']}
require(len(sections) == len(catalog['sections']), 'duplicate sections')
require(len({p['repository'] for p in projects}) == len(projects), 'duplicate project identities')
project_names = {p['repository'] for p in projects}
seen = set()
for p in catalog['papers']:
    ident = p['id']
    require(bool(re.fullmatch(r'\d{4}\.\d{4,5}', ident)), f'{ident}: invalid arXiv identifier')
    require(ident not in seen, f'{ident}: duplicate paper')
    seen.add(ident)
    require(p['section'] in sections, f'{ident}: unknown section')
    require(p['source_url'] == f'https://arxiv.org/abs/{ident}', f'{ident}: noncanonical source URL')
    require(bool(re.fullmatch(r'v[1-9]\d*', p['reviewed_version'])), f'{ident}: invalid version')
    require(p['review_status'] in ('A', 'M'), f'{ident}: invalid review status')
    require(bool(p['evidence'].strip()), f'{ident}: evidence required')
    if p['review_status'] == 'M':
        require(bool(re.search(r'section|appendix|§', p['evidence'], re.I)), f'{ident}: M requires section evidence')
    first = date(p['first_submitted'], ident)
    revised = date(p['version_date'], ident)
    checked = date(p['checked_on'], ident)
    require(first <= revised <= checked <= cutoff, f'{ident}: inconsistent or post-cutoff dates')
    require(p['authors'] and all(isinstance(a,str) and a.strip() for a in p['authors']), f'{ident}: authors required')
    require(p['title'].strip() and p['name'].strip() and p['tags'], f'{ident}: missing title, name, or tags')
    require(bool(re.search(r'[A-Za-z]', p['summary_en'])), f'{ident}: English summary required')
    require(bool(re.search(r'[\u4e00-\u9fff]', p['summary_zh'])), f'{ident}: Chinese summary required')
    require(re.findall(r'\d+(?:\.\d+)?', p['summary_en']) == re.findall(r'\d+(?:\.\d+)?', p['summary_zh']), f'{ident}: summary numbers differ')
    require(p['project'] is None or p['project'] in project_names, f'{ident}: unverified project reference')
for p in projects:
    require(p['url'] == 'https://github.com/'+p['repository'], f'{p["repository"]}: project URL mismatch')
    require(bool(re.fullmatch(r'[0-9a-f]{40}', p['readme_sha'] or '')), f'{p["repository"]}: missing README blob evidence')
    require(date(p['checked_on'],p['repository']) <= cutoff, f'{p["repository"]}: post-cutoff project check')
    require(any(x['project']==p['repository'] for x in catalog['papers']), f'{p["repository"]}: project has no related paper')
for filename, expected in render().items():
    path = ROOT/filename
    require(path.exists() and path.read_text()==expected, f'{filename}: stale generated output')

# Derive GitHub-style heading slugs plus explicit audit anchors, ignoring fenced code.
md_files = list(ROOT.glob('*.md')) + list((ROOT/'docs').glob('*.md'))
anchors = {}
for path in md_files:
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    known = set(re.findall(r'<a\s+id="([^"]+)"', text))
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        base = slug(title)
        n = counts.get(base, 0)
        known.add(base if n == 0 else f'{base}-{n}')
        counts[base] = n+1
    anchors[path.resolve()] = known
    expected_columns = None
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.startswith('|'):
            columns = len(re.split(r'(?<!\\)\|', line))-2
            if expected_columns is None:
                expected_columns = columns
            require(columns == expected_columns, f'{path.name}:{line_no}: inconsistent table width')
        else:
            expected_columns = None
    for target in re.findall(r'\]\(([^\s)]+)\)', text):
        if urlsplit(target).scheme or target.startswith('//'):
            continue
        filename, _, fragment = unquote(target).partition('#')
        dest = (path.parent/filename).resolve() if filename else path.resolve()
        require(dest.exists(), f'{path.name}: broken relative link {target}')
        # Defer anchor checks until all files have been indexed.
for path in md_files:
    text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    for target in re.findall(r'\]\(([^\s)]+)\)', text):
        if urlsplit(target).scheme or target.startswith('//'):
            continue
        filename, _, fragment = unquote(target).partition('#')
        dest = (path.parent/filename).resolve() if filename else path.resolve()
        if fragment:
            require(fragment in anchors.get(dest,set()), f'{path.name}: missing anchor {target}')

bib = (ROOT/'references.bib').read_text()
require(len(re.findall(r'^@misc\{',bib,re.M)) == len(seen), 'bibliography entry count mismatch')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Validated {len(seen)} papers, {len(projects)} projects, {len(sections)} sections, generated files, tables, and local links.')
