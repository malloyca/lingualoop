import pytest

from lingualoop import config
from lingualoop.config import database_path


def test_database_path_uses_absolute_override(monkeypatch, tmp_path):
    expected = tmp_path / "test.sqlite3"
    monkeypatch.setenv("LINGUALOOP_DB_PATH", str(expected))

    assert database_path() == expected

def test_database_path_uses_default_when_unset(monkeypatch, tmp_path):
    monkeypatch.delenv("LINGUALOOP_DB_PATH", raising=False)
    monkeypatch.setattr(
        config,
        "user_data_path",
        lambda *args, **kwargs: tmp_path,
    )

    assert config.database_path() == tmp_path / "lingualoop.sqlite3"

def test_database_path_rejects_empty_override(monkeypatch):
    monkeypatch.setenv("LINGUALOOP_DB_PATH", "")

    with pytest.raises(ValueError, match="cannot be empty"):
        database_path()

def test_database_path_rejects_relative_override(monkeypatch):
    monkeypatch.setenv("LINGUALOOP_DB_PATH", "data/test.sqlite3")

    with pytest.raises(ValueError, match="absolute path"):
        database_path()