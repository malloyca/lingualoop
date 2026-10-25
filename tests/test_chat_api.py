import sqlite3

import pytest
from fastapi.testclient import TestClient

from lingualoop import main
from lingualoop.llm import Message


class FakeLLMClient:
    def __init__(self, **_kwargs: object) -> None:
        self.messages: list[Message] | None = None

    async def chat(self, messages: list[Message]) -> str:
        self.messages = messages
        return "你好！"

    async def close(self) -> None:
        pass


def test_chat_endpoint_builds_prompt_and_returns_reply(monkeypatch, tmp_path) -> None:
    # Prevent startup from creating a database in the normal app data directory
    database_file = tmp_path / "chat-test.sqlite3"
    monkeypatch.setenv("LINGUALOOP_DB_PATH", str(database_file))
    monkeypatch.setattr(main, "LLMClient", FakeLLMClient)

    # Entering and exiting TestClient runs FastAPI's startup and shutdown code
    with TestClient(main.app) as client:
        llm = main.app.state.llm
        response = client.post("/api/chat", json={"message": "你好"})
        health_response = client.get("/health")

    assert main.app.state.database_path == database_file
    assert database_file.is_file()

    # Starting again should succeed with the database already migrated
    with TestClient(main.app):
        assert main.app.state.database_path == database_file

    # Alembic records the applied migration in this table
    connection = sqlite3.connect(database_file)
    try:
        revision = connection.execute(
            "SELECT version_num FROM alembic_version"
        ).fetchone()
    finally:
        connection.close()
    # Update this expected revision when a new migration becomes the head
    assert revision == ("052b23595207",)

    assert response.status_code == 200
    assert response.json() == {"response": "你好！"}
    assert llm.messages is not None
    assert [message["role"] for message in llm.messages] == ["system", "user"]
    assert "You are LinguaLoop" in llm.messages[0]["content"]
    assert llm.messages[-1]["content"] == "你好"

    assert health_response.status_code == 200
    assert health_response.json() == {"status": "ok", "database": "ready"}


def test_startup_rejects_relative_database_path(monkeypatch) -> None:
    monkeypatch.setenv("LINGUALOOP_DB_PATH", "data/test.sqlite3")

    with pytest.raises(ValueError, match="absolute path"):
        with TestClient(main.app):
            pass
