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
    sessions.py
    taxonomy.py
    transcription.py
📁 tests/
    __init__.py
    test_config.py
    test_export.py
    test_repository.py
    test_sessions.py
    test_taxonomy.py
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
**Org:** `organvm-vi-koinonia` | **Repo:** `salon-archive`

### Edges
- **Produces** → `data`: Salon session records, transcripts, and taxonomy
- **Consumes** ← `koinonia-db`: Shared database models and migrations

### Siblings in Community
`community-hub` (flagship), `koinonia-db`, `reading-group-curriculum`, `adaptive-personal-syllabus`, `.github`

### Governance
- Community infrastructure layer. Consumes from ORGAN-I, II, III. No back-edges.

*Last synced: 2026-02-24T12:00:00Z*
<!-- ORGANVM:AUTO:END -->
