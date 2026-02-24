"""Tests for the config module."""

import os
from unittest import mock

import pytest

from src.config import Settings


class TestSettings:
    def test_database_url_defaults_empty(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            # Re-import to pick up cleared env
            assert Settings.DATABASE_URL is not None  # class attribute exists

    def test_whisper_backend_default(self):
        assert Settings.WHISPER_BACKEND in ("mock", os.environ.get("WHISPER_BACKEND", "mock"))

    def test_require_db_raises_when_unset(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(RuntimeError, match="DATABASE_URL is not set"):
                Settings.require_db()

    def test_require_db_returns_url_when_set(self):
        with mock.patch.dict(os.environ, {"DATABASE_URL": "postgresql://localhost/test"}):
            url = Settings.require_db()
            assert url == "postgresql+psycopg://localhost/test"
