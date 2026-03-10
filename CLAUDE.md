# CLAUDE.md — salon-archive

**ORGAN VI** (Community) · `organvm-vi-koinonia/salon-archive`
**Status:** ACTIVE · **Branch:** `main`

## What This Repo Is

Archive infrastructure for intellectual salons: transcription pipeline, topic taxonomy, and session metadata aligned with the eight-organ model

## Stack

**Languages:** Python
**Build:** Python (pip/setuptools)
**Testing:** pytest (likely)

## Directory Structure

```
📁 .github/
📁 docs/
    adr
    seed-automation-contract.yaml
    staging-reference.md
📁 src/
    __init__.py
    __main__.py
    config.py
    export.py
    repository.py
    transcription.py
📁 tests/
    __init__.py
    test_config.py
    test_data_export.py
    test_export.py
    test_repository.py
    test_transcription.py
  .gitignore
  CHANGELOG.md
  LICENSE
  README.md
  pyproject.toml
  seed.yaml
```

## Key Files

- `README.md` — Project documentation
- `pyproject.toml` — Python project config
- `seed.yaml` — ORGANVM orchestration metadata
- `src/` — Main source code
- `tests/` — Test suite

## Development

```bash
pip install -e .    # Install in development mode
pytest              # Run tests
```

## ORGANVM Context

This repository is part of the **ORGANVM** eight-organ creative-institutional system.
It belongs to **ORGAN VI (Community)** under the `organvm-vi-koinonia` GitHub organization.

**Registry:** [`registry-v2.json`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/registry-v2.json)
**Corpus:** [`organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm)

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** ORGAN-VI (Community) | **Tier:** standard | **Status:** PUBLIC_PROCESS
**Org:** `organvm-vi-koinonia` | **Repo:** `salon-archive`

### Edges
- **Produces** → `unspecified`: data
- **Consumes** ← `unspecified`: package

### Siblings in Community
`koinonia-db`, `community-hub`, `reading-group-curriculum`, `adaptive-personal-syllabus`, `.github`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-03-08T20:11:35Z*

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |

Linked skills: evaluation-to-growth


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)


## Atomization Pipeline

Run `organvm atoms pipeline --write && organvm atoms fanout --write` to generate task queue.

<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
