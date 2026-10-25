import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from lingualoop import main


def test_startup_fails_when_database_path_is_a_directory(monkeypatch, tmp_path) -> None:
    database_dir = tmp_path
    monkeypatch.setenv("LINGUALOOP_DB_PATH", str(database_dir))

    with pytest.raises(OperationalError):
        with TestClient(main.app):
            pass