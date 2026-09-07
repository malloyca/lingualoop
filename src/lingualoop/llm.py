# LLMClient v0.1
# 
# Purpose:
#     Provide a small interface for sending chat conversations
#     to an OpenAI-compatible LLM server and receiving generated text.
# 
# Responsibilities:
#     - Manage the server's base URL.
#     - Specify the model.
#     - Send chat completion requests.
#     - Parse the response.
#     - Return generated text.
#     - Translate low-level communication failures into
#       application-level errors.
# 
# Does NOT:
#     - Know which LLM runner is being used.
#     - Manage conversations.
#     - Store messages.
#     - Construct language-learning prompts.
#     - Know about FastAPI.
#     - Know about the frontend.
#     - Know about users/learners.
#     - Handle STT/TTS.
# 
# Initial interface:
# 
#     LLMClient(
#         base_url,
#         model,
#         ...
#     )
# 
#     chat(messages) -> str


import httpx
from typing import Literal, TypedDict



class Message(TypedDict):
    role: Literal["system", "developer", "user", "assistant"]
    content: str



class LLMClient:

    def __init__(
            self,
            base_url: str,
            model: str,
            temperature: float = 0.7,
    ):
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

        self.client = httpx.AsyncClient(
            # For now default to 2 min timeout to give the model time to respond
            timeout=httpx.Timeout(120.0),
        )

    async def chat(
            self,
            messages: list[Message],
    ) -> str:
        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
            },
        )

        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def close(self) -> None:
        await self.client.aclose()
