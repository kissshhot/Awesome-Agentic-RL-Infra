#!/usr/bin/env python3
"""Build the reading list, source audit, and BibTeX from reviewed catalog data."""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

def slug(text):
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')

def cell(text):
    return str(text).replace('|', r'\|').replace('\n', ' ')

def render():
    catalog = json.loads((ROOT / 'data/catalog.json').read_text())
    projects = json.loads((ROOT / 'data/projects.json').read_text())
    papers, date = catalog['papers'], catalog['as_of']
    lines = [
        '# Awesome Agentic RL Infrastructure', '',
        'A curated reading list on **infrastructure for agentic reinforcement learning**: multi-turn agent training, rollout execution, distributed optimization, environment management, and algorithm-system co-design.', '',
        f'**{len(papers)} papers** · **{len(projects)} official project entries** · **Source review: {date}** · **English and Chinese paper summaries**', '',
        '[Contents](#table-of-contents) · [Reading guide](docs/READING_GUIDE.md) · [Source audit](docs/SOURCE_AUDIT.md) · [Search record](docs/SEARCH_LOG.md) · [BibTeX](references.bib) · [Contributing](CONTRIBUTING.md)', '',
        '## Scope and Terminology', '',
        'The core scope is **LLM agents trained through repeated interaction with tools or environments**. Infrastructure includes the agent harness, trajectory collection, inference services, environments, rewards, experience storage, policy optimization, weight synchronization, and resource scheduling.', '',
        'The catalog separates direct agent-training systems from general RLHF/RLVR foundations, environment/data pipelines, optimization methods, and embodied extensions. A code-generation benchmark alone does not establish multi-turn agent support. Likewise, an environment dataset is not a distributed trainer, and asynchronous execution alone does not guarantee learning stability.', '',
        '- **Rollout:** a sampled sequence of model actions and environment observations; its length and runtime can vary across tasks.',
        '- **Agent harness:** the program managing tools, context, and interaction control flow around model calls.',
        '- **Disaggregation:** separate components or resource pools for training, inference, environments, or rewards; the exact separation differs by system.',
        '- **Policy staleness:** the lag between the policy used to generate a sample and the policy being optimized.',
        '- **Partial rollout:** interruption or staged processing of an unfinished trajectory; version and probability handling must follow the specific algorithm.',
        '- **Training-inference mismatch:** different probabilities produced by training and inference implementations, distinct from policy-version lag.', '',
        '## Reading the Entries', '',
        '- **First submitted** comes from the arXiv submission history, not the identifier month, repository announcement, conference date, or latest revision.',
        '- **A** means the primary-source abstract, metadata, and submission history were inspected. **M** additionally requires a cited method-section review. All initial entries are **A**; no experiment reproduction is implied.',
        '- The **Source** cell links to the paper and, when verified, its official project. A missing code link means no official implementation was verified in this review, not that no code exists.',
        '- **Checked** links to the exact reviewed version, full title, authors, and scope notes in the audit. Summaries describe that paper version; current repositories can contain later features.',
        '- English and Chinese summaries carry the same mechanism and scope. Tags are editorial navigation aids. Entries have one primary section and are sorted by first submission within it.',
        '- This is a curated starting collection, not an exhaustive survey or a cross-paper performance leaderboard.', '',
        '## Start Here', '',
        'Suggested sequence: **HybridFlow → AReaL → AgentRL → Agent Lightning / v1.0 → RollArt**. Read the original Lightning paper for the abstraction and its separate v1.0 report for harness integration. Then branch toward scheduling, environment costs, or algorithm-system correctness using the [reading guide](docs/READING_GUIDE.md).', '',
        '## Table of Contents', '',
        '- [Direction Overview](#direction-overview)',
    ]
    lines += [f'- [{s["title"]}](#{slug(s["title"])})' for s in catalog['sections']]
    lines += ['- [Official Projects](#official-projects)', '- [Contributing](#contributing)', '', '## Direction Overview', '',
              '| Direction | Papers | Systems question |', '| --- | --- | --- |']
    for s in catalog['sections']:
        count = sum(p['section'] == s['id'] for p in papers)
        lines.append(f'| [{s["title"]}](#{slug(s["title"])}) | {count} | {s["description"]} |')
    for s in catalog['sections']:
        lines += ['', '## ' + s['title'], '', s['description'], '',
                  '| Paper and direction | First submitted | English | 中文 | Source | Checked |',
                  '| --- | --- | --- | --- | --- | --- |']
        for p in sorted((p for p in papers if p['section'] == s['id']), key=lambda p:(p['first_submitted'],p['id'])):
            source = f'[arXiv {p["id"]}]({p["source_url"]})'
            if p['project']:
                source += f'<br>[Code](https://github.com/{p["project"]})'
            anchor = 'paper-' + p['id'].replace('.', '-')
            values = [f'**{p["name"]}**<br>' + ' · '.join(p['tags']), p['first_submitted'], p['summary_en'], p['summary_zh'], source,
                      f'[{p["review_status"]} · {p["reviewed_version"]}](docs/SOURCE_AUDIT.md#{anchor})']
            lines.append('| ' + ' | '.join(cell(v) for v in values) + ' |')
    lines += ['', '## Official Projects', '',
              f'Repository identities, README paper links, and archive flags were checked on **{date}**. These are navigation entries, not feature-parity or maintenance-quality rankings. Multiple papers may share one codebase. README blob identifiers are recorded in [projects.json](data/projects.json).', '',
              '| Official repository | Related catalog entries | Repository status at review |', '| --- | --- | --- |']
    for project in sorted(projects, key=lambda p:p['repository'].lower()):
        related = [p['name'] for p in papers if p['project'] == project['repository']]
        state = 'Archived' if project['archived'] else 'Not archived'
        lines.append(f'| [{project["repository"]}]({project["url"]}) | {cell("; ".join(related))} | {state} |')
    lines += ['', '## Contributing', '',
              'See [CONTRIBUTING.md](CONTRIBUTING.md) for inclusion criteria, bilingual summaries, evidence requirements, and validation. Edit [catalog.json](data/catalog.json), then regenerate the README, source audit, and bibliography.', '',
              '## Organization Reference', '',
              'This repository follows the English navigation, bilingual paper tables, explicit scope boundaries, submission dates, and source-audit style of [Awesome-OPD](https://github.com/kissshhot/Awesome-OPD). Its taxonomy and summaries are written specifically for agentic RL infrastructure.', '']
    audit = ['# Source Audit', '', f'Review cutoff: **{date}**. **{len(papers)} unique arXiv records**.', '',
             'All entries have status **A**: the abstract, bibliographic metadata, and submission history on the primary arXiv page were read. This does not certify all claims, constitute a full-paper review, or imply reproduction. The reviewed version is the latest version shown by the source at this review and no later than the cutoff.', '',
             'Dates are the calendar dates displayed in the arXiv submission history (UTC). The unversioned source is retained for discovery; the versioned link below identifies the reviewed text. Full author lists are in [catalog.json](../data/catalog.json). Official repository identities and README snapshots are in [projects.json](../data/projects.json).', '']
    for p in sorted(papers, key=lambda p:p['id']):
        anchor = 'paper-' + p['id'].replace('.', '-')
        author = '; '.join(p['authors'][:3]) + ('; et al.' if len(p['authors'])>3 else '')
        audit += [f'<a id="{anchor}"></a>', f'## {p["name"]}', '',
                  f'- **Title:** {p["title"]}', f'- **Authors:** {author}',
                  f'- **First submitted:** {p["first_submitted"]}',
                  f'- **Reviewed:** [{p["reviewed_version"]}]({p["source_url"]}{p["reviewed_version"]}) · version date {p["version_date"]} · checked {p["checked_on"]}',
                  f'- **Evidence:** {p["review_status"]} — {p["evidence"]}.',
                  '- **Scope:** ' + next(s['title'] for s in catalog['sections'] if s['id']==p['section']) + '.',
                  '- **Official project:** ' + (f'[{p["project"]}](https://github.com/{p["project"]}).' if p['project'] else 'Not verified in this review.')]
        if p['audit_note']:
            audit += ['- **Version / identity note:** ' + p['audit_note']]
        audit += ['']
    bib=[]
    for p in sorted(papers,key=lambda p:p['id']):
        title=p['title'].replace('&',r'\&').replace('%',r'\%')
        bib += [f'@misc{{arxiv{p["id"].replace(".","")},',f'  title = {{{{{title}}}}},',
                '  author = {' + ' and '.join(p['authors']) + '},',
                f'  year = {{{p["first_submitted"][:4]}}},', f'  eprint = {{{p["id"]}}},',
                '  archivePrefix = {arXiv},',f'  url = {{{p["source_url"]}}},',
                f'  note = {{Reviewed {p["reviewed_version"]}, {p["version_date"]}}}', '}', '']
    return {'README.md':'\n'.join(lines),'docs/SOURCE_AUDIT.md':'\n'.join(audit),'references.bib':'\n'.join(bib)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated files differ; do not write files')
    args=parser.parse_args()
    stale=[]
    for filename, content in render().items():
        path=ROOT/filename
        if args.check:
            if not path.exists() or path.read_text()!=content: stale.append(filename)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit('Regenerate catalog files: '+', '.join(stale))
    print('Generated files are current.' if args.check else 'Generated README.md, docs/SOURCE_AUDIT.md, and references.bib.')

if __name__=='__main__':
    main()
