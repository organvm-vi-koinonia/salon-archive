"""Transcription module for processing salon audio recordings.

Provides a pipeline for converting audio recordings into structured
text transcripts with speaker diarization and segment metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Any


class TranscriptionStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Segment:
    """A time-aligned segment of transcribed speech."""
    speaker: str
    text: str
    start_time: timedelta
    end_time: timedelta
    confidence: float = 0.0

    @property
    def duration(self) -> timedelta:
        return self.end_time - self.start_time

    def to_dict(self) -> dict[str, Any]:
        return {
            "speaker": self.speaker,
            "text": self.text,
            "start_seconds": self.start_time.total_seconds(),
            "end_seconds": self.end_time.total_seconds(),
            "confidence": self.confidence,
        }


@dataclass
class TranscriptionResult:
    """Complete transcription output for a salon session."""
    session_id: str
    segments: list[Segment] = field(default_factory=list)
    status: TranscriptionStatus = TranscriptionStatus.PENDING
    language: str = "en"

    @property
    def full_text(self) -> str:
        return " ".join(seg.text for seg in self.segments)

    @property
    def speaker_list(self) -> list[str]:
        return list(dict.fromkeys(seg.speaker for seg in self.segments))

    @property
    def total_duration(self) -> timedelta:
        if not self.segments:
            return timedelta(0)
        return max(seg.end_time for seg in self.segments)


class TranscriptionPipeline:
    """Pipeline for processing audio into structured transcripts."""

    def __init__(self, language: str = "en") -> None:
        self.language = language
        self._results: dict[str, TranscriptionResult] = {}

    def process_audio(self, session_id: str, audio_path: str) -> TranscriptionResult:
        """Process an audio file and generate a transcription.

        Args:
            session_id: Unique identifier for the salon session.
            audio_path: Path to the audio file.

        Returns:
            TranscriptionResult with placeholder segments.
        """
        result = TranscriptionResult(
            session_id=session_id,
            status=TranscriptionStatus.PROCESSING,
            language=self.language,
        )
        # Prototype: generate placeholder segments
        result.segments = [
            Segment(
                speaker="Speaker 1",
                text=f"Transcription placeholder for {audio_path}",
                start_time=timedelta(seconds=0),
                end_time=timedelta(seconds=30),
                confidence=0.95,
            ),
        ]
        result.status = TranscriptionStatus.COMPLETED
        self._results[session_id] = result
        return result

    def get_result(self, session_id: str) -> TranscriptionResult | None:
        return self._results.get(session_id)

    def extract_segments(self, result: TranscriptionResult, speaker: str | None = None) -> list[Segment]:
        """Extract segments, optionally filtered by speaker."""
        if speaker:
            return [s for s in result.segments if s.speaker == speaker]
        return list(result.segments)
