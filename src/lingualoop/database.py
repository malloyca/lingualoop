from pathlib import Path

from alembic import command
from alembic.config import Config

from lingualoop.config import database_path


def initialize_database() -> Path:
    # Get database path and create parent directory
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load Alembic config and upgrade to head
    project_root = Path(__file__).resolve().parents[2]
    alembic_config = Config(str(project_root / "alembic.ini"))
    command.upgrade(alembic_config, "head")

    return path