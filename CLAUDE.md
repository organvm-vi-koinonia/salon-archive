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

**Organ:** ORGAN-VI (Community) | **Tier:** standard | **Status:** CANDIDATE
**Org:** `unknown` | **Repo:** `salon-archive`

### Edges
- **Produces** → `unknown`: unknown
- **Consumes** ← `unknown`: unknown

### Siblings in Community
`koinonia-db`, `community-hub`, `reading-group-curriculum`, `adaptive-personal-syllabus`, `.github`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-02-24T12:41:28Z*
<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
