"""CLI entry point for salon-archive.

Usage:
    python -m src ingest --audio /path/to/audio.wav --session-id S001
    python -m src search --topic "recursion" [--participant "Alice"]
    python -m src export --session-id S001 [--format json|markdown]
"""
from __future__ import annotations

import argparse
import json
import sys

from .sessions import SalonSession, SessionArchive
from .transcription import TranscriptionPipeline


def cmd_ingest(args: argparse.Namespace) -> int:
    """Ingest an audio recording and produce a transcription."""
    pipeline = TranscriptionPipeline(language=args.language)
    result = pipeline.process_audio(args.session_id, args.audio)
    print(f"Ingested session {args.session_id}: {len(result.segments)} segment(s)")
    print(f"Status: {result.status.value}")
    print(f"Duration: {result.total_duration}")
    if result.speaker_list:
        print(f"Speakers: {', '.join(result.speaker_list)}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search the session archive by topic or participant."""
    archive = SessionArchive()

    # In a real system this would load from persistent storage;
    # for the prototype we report that the archive is empty.
    results: list[SalonSession] = []
    if args.topic:
        results = archive.search_by_topic(args.topic)
    elif args.participant:
        results = archive.search_by_participant(args.participant)
    else:
        results = archive.get_recent(args.limit)

    if not results:
        print("No matching sessions found.")
        return 0

    for session in results:
        print(f"  [{session.session_id}] {session.title} ({session.date.date()})")
    print(f"\n{len(results)} session(s) found.")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export a session record in the requested format."""
    archive = SessionArchive()

    try:
        session = archive.get_session(args.session_id)
    except KeyError:
        print(f"Session '{args.session_id}' not found in archive.", file=sys.stderr)
        return 1

    record = session.to_archive_record()
    if args.format == "json":
        print(json.dumps(record, indent=2))
    else:
        print(f"# {record['title']}")
        print(f"**Date:** {record['date']}")
        print(f"**Participants:** {record['participant_count']}")
        print(f"**Topics:** {', '.join(record['topics'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to the appropriate subcommand."""
    parser = argparse.ArgumentParser(
        prog="salon-archive",
        description="Salon transcription, search, and export toolkit",
    )
    sub = parser.add_subparsers(dest="command")

    # ingest
    p_ingest = sub.add_parser("ingest", help="Ingest audio recording")
    p_ingest.add_argument("--audio", required=True, help="Path to audio file")
    p_ingest.add_argument("--session-id", required=True, help="Unique session identifier")
    p_ingest.add_argument("--language", default="en", help="Language code (default: en)")

    # search
    p_search = sub.add_parser("search", help="Search sessions")
    p_search.add_argument("--topic", help="Search by topic keyword")
    p_search.add_argument("--participant", help="Search by participant name")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")

    # export
    p_export = sub.add_parser("export", help="Export session record")
    p_export.add_argument("--session-id", required=True, help="Session to export")
    p_export.add_argument("--format", choices=["json", "markdown"], default="json")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2

    dispatch = {
        "ingest": cmd_ingest,
        "search": cmd_search,
        "export": cmd_export,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
