"""Sessions module for managing salon session metadata and archives.

Tracks salon sessions with participants, topics, recordings,
and cross-references to transcription outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SalonSession:
    """A single salon session record."""
    session_id: str
    title: str
    date: datetime
    participants: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    recording_path: str | None = None
    transcript_available: bool = False
    notes: str = ""

    def add_participant(self, name: str) -> None:
        if name not in self.participants:
            self.participants.append(name)

    def to_archive_record(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "title": self.title,
            "date": self.date.isoformat(),
            "participant_count": len(self.participants),
            "topics": self.topics,
            "has_recording": self.recording_path is not None,
            "has_transcript": self.transcript_available,
        }


class SessionArchive:
    """Archive of all salon sessions with search and filter capabilities."""

    def __init__(self) -> None:
        self._sessions: dict[str, SalonSession] = {}

    def add_session(self, session: SalonSession) -> None:
        if session.session_id in self._sessions:
            raise ValueError(f"Session '{session.session_id}' already archived")
        self._sessions[session.session_id] = session

    def get_session(self, session_id: str) -> SalonSession:
        return self._sessions[session_id]

    def search_by_topic(self, topic: str) -> list[SalonSession]:
        t = topic.lower()
        return [s for s in self._sessions.values() if any(t in tp.lower() for tp in s.topics)]

    def search_by_participant(self, name: str) -> list[SalonSession]:
        n = name.lower()
        return [s for s in self._sessions.values() if any(n in p.lower() for p in s.participants)]

    def get_recent(self, count: int = 10) -> list[SalonSession]:
        sorted_sessions = sorted(self._sessions.values(), key=lambda s: s.date, reverse=True)
        return sorted_sessions[:count]

    @property
    def total_sessions(self) -> int:
        return len(self._sessions)
