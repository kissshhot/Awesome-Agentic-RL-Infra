# Contributing

Prefer a well-supported addition or correction over increasing the paper count.

## Scope

Include work with a concrete contribution to agentic RL infrastructure: execution, scheduling, environments, trajectory handling, distributed training, policy synchronization, or algorithm-system constraints. Clearly label general RL systems, data pipelines, optimization methods, position papers, and embodied extensions. An agent benchmark result alone is insufficient for a systems entry.

Each arXiv identifier has one catalog entry. A later revision updates that entry. A separately published follow-up report can have a separate entry with its relationship explained. Keep current section identifiers stable unless a taxonomy change is explicitly part of the contribution.

## Source Review

1. Open the primary paper record and read its abstract. Check the full title, author list, first submission date, version number, and revision date.
2. Use the latest revision available by the declared cutoff. Do not infer dates from identifiers or repository announcements.
3. Assign **A** for abstract and metadata review. Assign **M** only after reading specific method sections and recording those sections in the evidence field. Never infer verification from HTTP success alone.
4. Write concise, matching English and Chinese summaries. Explain the mechanism and scope; distinguish algorithm proposals from deployed or measured systems.
5. Add version and identity qualifications in `audit_note`. Explicitly separate a paper's contribution from later repository features.
6. Link code only after confirming the official repository through the paper or an author-maintained source. Record the canonical identity, README blob SHA, checked date, and archive flag in `data/projects.json`. A missing link means not verified, not unavailable.
7. Avoid unqualified best/first/SOTA claims. Performance numbers require a specific experiment, hardware, model, metric, comparator, and source location; they should not create a cross-paper leaderboard.

## Editing and Validation

The catalog source is `data/catalog.json`. The project index is `data/projects.json`. The generator produces `README.md`, `docs/SOURCE_AUDIT.md`, and `references.bib`; edit the source data rather than generated files. The reading guide and search record are maintained separately.

Required paper fields include `id`, `title`, `authors`, `name`, `section`, `tags`, `first_submitted`, `reviewed_version`, `version_date`, `checked_on`, `review_status`, `evidence`, `summary_en`, `summary_zh`, `source_url`, `project` (or null), and `audit_note`.

Run from any working directory using the corresponding script paths; only Python 3's standard library is needed:

```sh
python3 scripts/build_catalog.py
python3 scripts/validate_catalog.py
python3 scripts/build_catalog.py --check
git diff --check
```

The validator checks identifiers, duplicates, section membership, bilingual fields, numeric parity, dates, project references, generated-file consistency, Markdown table shapes, and relative file/anchor links. It does not verify scientific truth, translation meaning, external availability, or experiment reproducibility. Review both summaries and changed external sources manually.

Record new searches, the cutoff, and important exclusions in `docs/SEARCH_LOG.md`. Describe corrections to titles or source versions in the contribution. Preview rendered Markdown before publishing changes.
