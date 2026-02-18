"""Tests for the repository module.

These tests verify the SalonRepository can be instantiated and that its
methods exist. Live database tests are skipped unless DATABASE_URL is set.
"""

import os

import pytest

from src.repository import SalonRepository


# Skip live DB tests unless DATABASE_URL is in the environment
requires_db = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL not set — skipping live DB tests",
)


class TestSalonRepositoryInit:
    def test_creates_with_plain_url(self):
        repo = SalonRepository("postgresql+psycopg://localhost/test")
        assert repo._engine is not None

    def test_upgrades_bare_postgresql_to_psycopg(self):
        repo = SalonRepository("postgresql://localhost/test")
        url_str = str(repo._engine.url)
        assert "psycopg" in url_str

    def test_has_session_methods(self):
        repo = SalonRepository("postgresql+psycopg://localhost/test")
        assert callable(repo.add_session)
        assert callable(repo.get_session)
        assert callable(repo.list_sessions)
        assert callable(repo.search_by_topic)
        assert callable(repo.get_segments)

    def test_has_taxonomy_methods(self):
        repo = SalonRepository("postgresql+psycopg://localhost/test")
        assert callable(repo.add_taxonomy_node)
        assert callable(repo.get_taxonomy_roots)
        assert callable(repo.search_taxonomy)

    def test_has_count_methods(self):
        repo = SalonRepository("postgresql+psycopg://localhost/test")
        assert callable(repo.count_sessions)
        assert callable(repo.count_taxonomy_nodes)


@requires_db
class TestSalonRepositoryLive:
    """Live DB tests: run only when DATABASE_URL is set."""

    @pytest.fixture()
    def repo(self):
        return SalonRepository(os.environ["DATABASE_URL"])

    def test_count_sessions(self, repo):
        count = repo.count_sessions()
        assert isinstance(count, int)
        assert count >= 0

    def test_count_taxonomy_nodes(self, repo):
        count = repo.count_taxonomy_nodes()
        assert isinstance(count, int)
        assert count >= 0

    def test_list_sessions(self, repo):
        sessions = repo.list_sessions(limit=5)
        assert isinstance(sessions, list)

    def test_get_taxonomy_roots(self, repo):
        roots = repo.get_taxonomy_roots()
        assert isinstance(roots, list)
