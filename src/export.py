"""Export salon session data in markdown, JSON, and YAML formats."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def export_session_json(session_data: dict[str, Any]) -> str:
    """Serialize a session data dict to formatted JSON."""
    return json.dumps(session_data, indent=2, default=str)


def export_session_markdown(session_data: dict[str, Any]) -> str:
    """Render a session data dict as a human-readable markdown document."""
    md = f"# {session_data['title']}\n\n"
    md += f"**Date:** {session_data['date']}\n"
    md += f"**Format:** {session_data['format']}\n"
    if session_data.get("facilitator"):
        md += f"**Facilitator:** {session_data['facilitator']}\n"
    md += f"**Tags:** {', '.join(session_data.get('organ_tags', []))}\n\n"

    if session_data.get("notes"):
        md += f"## Notes\n\n{session_data['notes']}\n\n"

    if session_data.get("participants"):
        md += "## Participants\n\n"
        for p in session_data["participants"]:
            md += f"- {p['name']} ({p['role']})\n"
        md += "\n"

    if session_data.get("segments"):
        md += "## Transcript\n\n"
        for seg in session_data["segments"]:
            start = format_time(seg["start_seconds"])
            md += f"**[{start}] {seg['speaker']}:** {seg['text']}\n\n"

    return md


def format_time(seconds: float) -> str:
    """Convert seconds to H:MM:SS or M:SS display string."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def session_to_dict(
    session_row: Any,
    participants: list[Any] | None = None,
    segments: list[Any] | None = None,
) -> dict[str, Any]:
    """Convert a SalonSessionRow (ORM object) to a plain dict for export."""
    return {
        "id": session_row.id,
        "title": session_row.title,
        "date": (
            session_row.date.isoformat()
            if isinstance(session_row.date, datetime)
            else str(session_row.date)
        ),
        "format": session_row.format,
        "facilitator": session_row.facilitator,
        "notes": session_row.notes,
        "organ_tags": session_row.organ_tags or [],
        "participants": [
            {"name": p.name, "role": p.role} for p in (participants or [])
        ],
        "segments": [
            {
                "speaker": s.speaker,
                "text": s.text,
                "start_seconds": s.start_seconds,
                "end_seconds": s.end_seconds,
                "confidence": s.confidence,
            }
            for s in (segments or [])
        ],
    }
