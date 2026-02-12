"""Tests for the sessions module — session management, archive, search."""

from datetime import datetime

import pytest

from src.sessions import SalonSession, SessionArchive


def _make_session(session_id: str = "S001", **kwargs) -> SalonSession:
    defaults = {
        "session_id": session_id,
        "title": "Recursion and Identity",
        "date": datetime(2026, 1, 15, 18, 0),
        "participants": ["Alice", "Bob"],
        "topics": ["recursion", "identity", "philosophy"],
    }
    defaults.update(kwargs)
    return SalonSession(**defaults)


class TestSalonSession:
    def test_create_session(self):
        session = _make_session()
        assert session.session_id == "S001"
        assert session.title == "Recursion and Identity"

    def test_add_participant(self):
        session = _make_session(participants=["Alice"])
        session.add_participant("Bob")
        assert "Bob" in session.participants
        assert len(session.participants) == 2

    def test_add_duplicate_participant(self):
        session = _make_session(participants=["Alice"])
        session.add_participant("Alice")
        assert len(session.participants) == 1

    def test_to_archive_record(self):
        session = _make_session(recording_path="/audio/s1.wav", transcript_available=True)
        record = session.to_archive_record()
        assert record["session_id"] == "S001"
        assert record["participant_count"] == 2
        assert record["has_recording"] is True
        assert record["has_transcript"] is True

    def test_archive_record_no_recording(self):
        session = _make_session(recording_path=None)
        record = session.to_archive_record()
        assert record["has_recording"] is False


class TestSessionArchive:
    def test_add_and_get_session(self):
        archive = SessionArchive()
        session = _make_session()
        archive.add_session(session)
        assert archive.get_session("S001").title == "Recursion and Identity"

    def test_duplicate_session_raises(self):
        archive = SessionArchive()
        archive.add_session(_make_session("S001"))
        with pytest.raises(ValueError, match="already archived"):
            archive.add_session(_make_session("S001"))

    def test_search_by_topic(self):
        archive = SessionArchive()
        archive.add_session(_make_session("S001", topics=["recursion", "art"]))
        archive.add_session(_make_session("S002", topics=["commerce", "SaaS"]))
        results = archive.search_by_topic("recursion")
        assert len(results) == 1
        assert results[0].session_id == "S001"

    def test_search_by_topic_case_insensitive(self):
        archive = SessionArchive()
        archive.add_session(_make_session("S001", topics=["Philosophy"]))
        results = archive.search_by_topic("philosophy")
        assert len(results) == 1

    def test_search_by_participant(self):
        archive = SessionArchive()
        archive.add_session(_make_session("S001", participants=["Alice", "Bob"]))
        archive.add_session(_make_session("S002", participants=["Charlie"]))
        results = archive.search_by_participant("alice")
        assert len(results) == 1

    def test_get_recent(self):
        archive = SessionArchive()
        archive.add_session(_make_session("S001", date=datetime(2026, 1, 1)))
        archive.add_session(_make_session("S002", date=datetime(2026, 2, 1)))
        archive.add_session(_make_session("S003", date=datetime(2026, 1, 15)))
        recent = archive.get_recent(2)
        assert len(recent) == 2
        assert recent[0].session_id == "S002"  # most recent first

    def test_total_sessions(self):
        archive = SessionArchive()
        assert archive.total_sessions == 0
        archive.add_session(_make_session("S001"))
        archive.add_session(_make_session("S002"))
        assert archive.total_sessions == 2

    def test_get_missing_session_raises(self):
        archive = SessionArchive()
        with pytest.raises(KeyError):
            archive.get_session("MISSING")
