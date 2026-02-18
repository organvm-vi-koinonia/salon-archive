"""Tests for the export module."""

import json
from types import SimpleNamespace

from src.export import (
    export_session_json,
    export_session_markdown,
    format_time,
    session_to_dict,
)


def _sample_data() -> dict:
    return {
        "id": 1,
        "title": "Recursion and Identity",
        "date": "2026-01-15",
        "format": "deep_dive",
        "facilitator": "Alice",
        "notes": "An exploration of self-reference.",
        "organ_tags": ["recursion", "identity"],
        "participants": [
            {"name": "Alice", "role": "facilitator"},
            {"name": "Bob", "role": "participant"},
        ],
        "segments": [
            {
                "speaker": "Alice",
                "text": "Let us begin.",
                "start_seconds": 0.0,
                "end_seconds": 10.0,
                "confidence": 0.95,
            },
            {
                "speaker": "Bob",
                "text": "Agreed.",
                "start_seconds": 10.0,
                "end_seconds": 15.0,
                "confidence": 0.92,
            },
        ],
    }


class TestExportJson:
    def test_valid_json(self):
        data = _sample_data()
        result = export_session_json(data)
        parsed = json.loads(result)
        assert parsed["title"] == "Recursion and Identity"

    def test_json_indented(self):
        data = _sample_data()
        result = export_session_json(data)
        assert "\n" in result  # indented output

    def test_json_contains_all_keys(self):
        data = _sample_data()
        parsed = json.loads(export_session_json(data))
        for key in ("id", "title", "date", "format", "facilitator", "segments"):
            assert key in parsed


class TestExportMarkdown:
    def test_markdown_title(self):
        md = export_session_markdown(_sample_data())
        assert md.startswith("# Recursion and Identity")

    def test_markdown_contains_date(self):
        md = export_session_markdown(_sample_data())
        assert "**Date:** 2026-01-15" in md

    def test_markdown_contains_facilitator(self):
        md = export_session_markdown(_sample_data())
        assert "**Facilitator:** Alice" in md

    def test_markdown_no_facilitator(self):
        data = _sample_data()
        data["facilitator"] = None
        md = export_session_markdown(data)
        assert "Facilitator" not in md

    def test_markdown_contains_participants(self):
        md = export_session_markdown(_sample_data())
        assert "- Alice (facilitator)" in md
        assert "- Bob (participant)" in md

    def test_markdown_contains_transcript(self):
        md = export_session_markdown(_sample_data())
        assert "## Transcript" in md
        assert "Let us begin." in md

    def test_markdown_contains_notes(self):
        md = export_session_markdown(_sample_data())
        assert "## Notes" in md
        assert "An exploration of self-reference." in md

    def test_markdown_contains_tags(self):
        md = export_session_markdown(_sample_data())
        assert "recursion, identity" in md


class TestFormatTime:
    def test_seconds_only(self):
        assert format_time(45.0) == "0:45"

    def test_minutes_and_seconds(self):
        assert format_time(125.0) == "2:05"

    def test_hours(self):
        assert format_time(3661.0) == "1:01:01"

    def test_zero(self):
        assert format_time(0.0) == "0:00"


class TestSessionToDict:
    def test_converts_orm_like_object(self):
        from datetime import datetime

        session = SimpleNamespace(
            id=1,
            title="Test",
            date=datetime(2026, 1, 15),
            format="deep_dive",
            facilitator="Alice",
            notes="Some notes",
            organ_tags=["tag1"],
        )
        participant = SimpleNamespace(name="Alice", role="facilitator")
        segment = SimpleNamespace(
            speaker="Alice",
            text="Hello",
            start_seconds=0.0,
            end_seconds=10.0,
            confidence=0.95,
        )

        result = session_to_dict(session, participants=[participant], segments=[segment])
        assert result["id"] == 1
        assert result["title"] == "Test"
        assert result["date"] == "2026-01-15T00:00:00"
        assert len(result["participants"]) == 1
        assert len(result["segments"]) == 1
        assert result["participants"][0]["name"] == "Alice"
        assert result["segments"][0]["speaker"] == "Alice"

    def test_no_participants_or_segments(self):
        session = SimpleNamespace(
            id=2,
            title="Empty",
            date="2026-02-01",
            format="roundtable",
            facilitator=None,
            notes="",
            organ_tags=None,
        )
        result = session_to_dict(session)
        assert result["participants"] == []
        assert result["segments"] == []
        assert result["organ_tags"] == []
