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


def test_chat_endpoint_builds_prompt_and_returns_reply(monkeypatch) -> None:
    monkeypatch.setattr(main, "LLMClient", FakeLLMClient)

    with TestClient(main.app) as client:
        llm = main.app.state.llm
        response = client.post("/api/chat", json={"message": "你好"})

    assert response.status_code == 200
    assert response.json() == {"response": "你好！"}
    assert llm.messages is not None
    assert [message["role"] for message in llm.messages] == ["system", "user"]
    assert "You are LinguaLoop" in llm.messages[0]["content"]
    assert llm.messages[-1]["content"] == "你好"
