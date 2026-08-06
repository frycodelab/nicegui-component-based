"""Shared pytest fixtures.

Enables the NiceGUI testing plugin and provides an isolated temporary database
so tests never touch the real ``data/app.db``.
"""

import pytest

# user_plugin provides the user-simulation fixtures without the full Selenium stack.
pytest_plugins = ['nicegui.testing.user_plugin']


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    """Point the database module at a throwaway SQLite file and seed it."""
    from core import database

    db_file = tmp_path / 'test.db'
    monkeypatch.setattr(database, 'DB_PATH', db_file)
    database.init_db()
    yield db_file
