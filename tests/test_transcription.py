"""Tests for the transcription module."""
from datetime import timedelta
from src.transcription import TranscriptionPipeline, TranscriptionStatus, Segment


def test_pipeline_processes_audio():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/session1.wav")
    assert result.status == TranscriptionStatus.COMPLETED
    assert len(result.segments) > 0

def test_pipeline_stores_result():
    pipeline = TranscriptionPipeline()
    pipeline.process_audio("S001", "/audio/session1.wav")
    assert pipeline.get_result("S001") is not None
    assert pipeline.get_result("MISSING") is None

def test_segment_duration():
    seg = Segment(speaker="A", text="Hello", start_time=timedelta(seconds=10), end_time=timedelta(seconds=25))
    assert seg.duration == timedelta(seconds=15)

def test_result_full_text():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/test.wav")
    assert len(result.full_text) > 0

def test_extract_segments_by_speaker():
    pipeline = TranscriptionPipeline()
    result = pipeline.process_audio("S001", "/audio/test.wav")
    segs = pipeline.extract_segments(result, "Speaker 1")
    assert len(segs) == 1
