# Search Record

## Review Scope

- **Cutoff and source-check date:** 2026-10-12.
- **Coverage:** a curated starting collection from distributed LLM RL foundations through multi-turn agent training, rollout scheduling, environment costs, and selected 2026 developments.
- **Discovery sources:** arXiv searches, author-maintained project READMEs, and the related-work entries in [Awesome-OPD](https://github.com/kissshhot/Awesome-OPD).
- **Reference layout:** Awesome-OPD main tree `24c82bfc11520411353033bbd9720e8c75d6703d`, README blob `f7ab5b50b0ec14d7baa3d425ff631db4ba3ac753`. Its English headings, bilingual summaries, date discipline, and source-audit pattern informed this repository; its OPD taxonomy was not copied.
- **Verification:** primary arXiv abstracts, metadata, and submission histories were retrieved and read for all 34 entries. Official repository metadata and README paper links were inspected for 17 projects. Bibliographic metadata is preserved in `data/catalog.json`; repository README blob SHAs are in `data/projects.json`.
- **Limit:** this is not an exhaustive systematic review. A-level inspection does not validate every experimental claim. No code was trained or benchmark reproduced.

## Discovery Queries and Follow-up Paths

Representative queries used during the initial search:

- `agentic reinforcement learning infrastructure system paper arxiv asynchronous rollout 2026`
- `agentic reinforcement learning system infrastructure 2026 September October`
- `HybridFlow Reinforcement`; `AReaL Asynchronous`; `RLinf Flexible`
- `AgentRL Scaling Asynchronous`; `AgentFly framework`; `SkyRL-Agent`
- `AsyncFlow reinforcement learning`; `StreamRL reinforcement learning`
- `ReaLHF efficient RLHF parameter reallocation`; `OpenRLHF scalable framework`
- `ROLL Efficient Reinforcement Learning`; `Rollout-Training Co-Design Efficient`
- `Molt Scalable PyTorch`; `Training Software Engineering Agents and Verifiers`
- `AgentGym Evolving`; `SWE-smith`; `SWE-Factory GitHub`

Search results were used for discovery, not as final authority for version-sensitive fields. Official READMEs supplied additional candidates: Agent Lightning v1.0, RollPacker, and RAGEN-2. Those records were then checked on arXiv and added as distinct publications.

## Version and Identity Corrections

- **AgentFly:** reviewed v2, dated 2026-10-08, has a new title and a unified-resource-system emphasis. The similarly named arXiv:2508.16153 is a different project and is not merged into this entry.
- **ReaL:** arXiv:2406.14088 v2 uses ReaL in the title; the code remains named ReaLHF and is archived.
- **RollArt:** the v2 title and wording differ from v1. The initial abstract used RollArc internally; the current entry follows v2.
- **Molt:** the September revision differs from the initial search-index description. This catalog follows v3.
- **Agent Lightning v1.0:** arXiv first submission is 2026-08-18, whereas the repository lists an August 19 announcement.
- **AsyncWebRL:** arXiv first submission is 2026-06-04. Secondary-index publication dates are not substituted for submission history.
- **RLinf-VLA:** the current title spells out reinforcement learning of vision-language-action models.
- **Repository redirects:** `volcengine/verl` → `verl-project/verl`; `inclusionAI/AReaL` → `areal-project/AReaL`; `RAGEN-AI/RAGEN` → `mll-lab-nu/RAGEN`.

## Selection Boundaries and Deferred Candidates

| Candidate or family | Decision |
| --- | --- |
| rLLM: Relational Table Learning with LLMs, arXiv:2407.20157 | Excluded: a name collision with unrelated relational-table learning. No agent-training paper identity was inferred from the acronym. |
| AgentFly: Fine-tuning LLM Agents without Fine-tuning LLMs, arXiv:2508.16153 | Excluded from the AgentFly entry: a separate work, not the training-infrastructure paper arXiv:2507.14897. |
| LightningRL for diffusion LLMs | Excluded from Agent Lightning: unrelated work sharing part of the name. |
| General model technical reports and task-performance papers | Deferred unless a specific infrastructure contribution is inspected; an agent score alone does not meet this catalog's scope. |
| Generic serving systems and historical distributed RL systems | Deferred to keep this initial collection focused; they can be added as explicitly labeled background later. |
| Asynchronous evolution strategies, arXiv:2610.04196 | Deferred: adjacent optimization work, outside the initial gradient-based RL infrastructure focus. |
| R2E-Gym and other additional environment suites | Deferred for a later environment-focused source review; absence is not a judgment on quality or relevance. |
| slime, rLLM agent-training projects, and other code-first libraries | No paper was assigned without an inspected primary paper record and official project mapping. They can be cataloged separately after a dedicated software review. |

The collection includes related environment/data papers and a small algorithm-system section because they explain constraints on the training infrastructure. Their inclusion is explicitly qualified in both languages.
