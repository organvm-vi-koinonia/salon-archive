"""Settings from environment variables."""

import os

from koinonia_db.config import require_database_url


class Settings:
    """Application settings sourced from environment variables."""

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    WHISPER_BACKEND: str = os.environ.get("WHISPER_BACKEND", "mock")  # mock, whisper_api

    @classmethod
    def require_db(cls) -> str:
        """Return DATABASE_URL or raise if unset. Converts to psycopg driver."""
        return require_database_url()
