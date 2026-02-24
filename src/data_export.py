"""Generate static data artifacts from seed session data.

Produces:
  data/sessions-index.json — index of all seed sessions
  data/sample-session.md   — first session rendered as markdown

Reads seed JSON directly (no database required).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .export import export_session_markdown

SEED_DIR = Path(__file__).parent.parent.parent / "koinonia-db" / "seed"


def load_seed_sessions(seed_dir: Path | None = None) -> list[dict[str, Any]]:
    """Load session data from koinonia-db seed file."""
    seed_dir = seed_dir or SEED_DIR
    path = seed_dir / "sample_sessions.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text())
    return data.get("sessions", [])


def build_sessions_index(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a summary index from session data."""
    formats = sorted({s.get("format", "unknown") for s in sessions})
    all_tags: set[str] = set()
    dates: list[str] = []
    for s in sessions:
        all_tags.update(s.get("organ_tags", []))
        if s.get("date"):
            dates.append(s["date"])

    return {
        "session_count": len(sessions),
        "formats": formats,
        "organ_tags": sorted(all_tags),
        "date_range": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None,
        },
        "sessions": [
            {
                "title": s["title"],
                "date": s.get("date"),
                "format": s.get("format"),
                "facilitator": s.get("facilitator"),
                "organ_tags": s.get("organ_tags", []),
                "participant_count": len(s.get("participants", [])),
                "segment_count": len(s.get("segments", [])),
            }
            for s in sessions
        ],
    }


def render_sample_session(session: dict[str, Any]) -> str:
    """Render a session dict as markdown using the existing export function."""
    return export_session_markdown(session)


def export_all(
    seed_dir: Path | None = None,
    output_dir: Path | None = None,
) -> list[Path]:
    """Generate all data artifacts and return output paths."""
    sessions = load_seed_sessions(seed_dir)
    output_dir = output_dir or Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    # sessions-index.json
    index = build_sessions_index(sessions)
    index_path = output_dir / "sessions-index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    outputs.append(index_path)

    # sample-session.md
    if sessions:
        md = render_sample_session(sessions[0])
        md_path = output_dir / "sample-session.md"
        md_path.write_text(md)
        outputs.append(md_path)

    return outputs


def main() -> None:
    """CLI entry point for data export."""
    paths = export_all()
    for p in paths:
        print(f"Written: {p}")


if __name__ == "__main__":
    main()
