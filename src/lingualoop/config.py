import os
from pathlib import Path

from platformdirs import user_data_path


def database_path() -> Path:
    override = os.environ.get("LINGUALOOP_DB_PATH")

    if override is None:
        return user_data_path("LinguaLoop", appauthor=False) / "lingualoop.sqlite3"

    if not override.strip():
        raise ValueError("LINGUALOOP_DB_PATH cannot be empty")

    path = Path(override).expanduser()
    if not path.is_absolute():
        raise ValueError("LINGUALOOP_DB_PATH must be an absolute path")

    return path