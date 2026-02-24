"""Tests for salon_archive data_export — session index and sample generation."""
import json
from pathlib import Path

from src.data_export import (
    load_seed_sessions,
    build_sessions_index,
    render_sample_session,
    export_all,
)


SEED_DIR = Path(__file__).parent.parent.parent / "koinonia-db" / "seed"


def test_load_seed_sessions():
    """Loads sessions from the real seed file."""
    sessions = load_seed_sessions(SEED_DIR)
    assert len(sessions) >= 2
    assert sessions[0]["title"]


def test_load_seed_sessions_missing_dir(tmp_path):
    """Returns empty list when seed dir doesn't have the file."""
    sessions = load_seed_sessions(tmp_path)
    assert sessions == []


def test_build_sessions_index():
    """Index has expected structure and counts."""
    sessions = load_seed_sessions(SEED_DIR)
    index = build_sessions_index(sessions)
    assert index["session_count"] >= 2
    assert len(index["formats"]) > 0
    assert len(index["organ_tags"]) > 0
    assert index["date_range"]["earliest"] is not None
    assert index["date_range"]["latest"] is not None
    for s in index["sessions"]:
        assert "title" in s
        assert "participant_count" in s
        assert "segment_count" in s


def test_render_sample_session():
    """Renders a session to markdown with expected headings."""
    sessions = load_seed_sessions(SEED_DIR)
    md = render_sample_session(sessions[0])
    assert md.startswith("# ")
    assert "**Date:**" in md
    assert "**Format:**" in md
    assert "## Transcript" in md


def test_export_all_writes_files(tmp_path):
    """export_all writes both artifacts to the output directory."""
    paths = export_all(seed_dir=SEED_DIR, output_dir=tmp_path)
    assert len(paths) == 2

    index_path = tmp_path / "sessions-index.json"
    assert index_path.exists()
    data = json.loads(index_path.read_text())
    assert data["session_count"] >= 2

    md_path = tmp_path / "sample-session.md"
    assert md_path.exists()
    assert md_path.read_text().startswith("# ")
