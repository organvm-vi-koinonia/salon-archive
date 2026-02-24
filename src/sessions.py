"""Sessions module for managing salon session metadata and archives.

DEPRECATED: This in-memory implementation is retained as an offline fallback.
For database-backed operations, use repository.py with koinonia-db models.

Tracks salon sessions with participants, topics, recordings,
and cross-references to transcription outputs.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "salon_archive.sessions is deprecated — use repository.SalonRepository instead",
    DeprecationWarning,
    stacklevel=2,
)

from dataclasses import dataclass, field  # noqa: E402
from datetime import datetime  # noqa: E402
from typing import Any  # noqa: E402


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

    def search_by_date_range(self, start: datetime, end: datetime) -> list[SalonSession]:
        """Return sessions within a date range (inclusive)."""
        return [s for s in self._sessions.values() if start <= s.date <= end]

    def update_session(self, session_id: str, **kwargs) -> SalonSession:
        """Update fields on an existing session."""
        session = self._sessions[session_id]
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        return session

    @property
    def total_sessions(self) -> int:
        return len(self._sessions)
