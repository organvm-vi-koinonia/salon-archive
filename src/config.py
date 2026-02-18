"""Settings from environment variables."""

import os


class Settings:
    """Application settings sourced from environment variables."""

    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    WHISPER_BACKEND: str = os.environ.get("WHISPER_BACKEND", "mock")  # mock, whisper_api

    @classmethod
    def require_db(cls) -> str:
        """Return DATABASE_URL or raise if unset."""
        if not cls.DATABASE_URL:
            raise RuntimeError("DATABASE_URL is not set")
        return cls.DATABASE_URL
