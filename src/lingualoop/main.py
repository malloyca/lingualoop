from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from lingualoop.llm import LLMClient
from lingualoop.schemas import ChatRequest, ChatResponse



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = LLMClient(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3.8-27b",
    )

    yield

    await app.state.llm.close()



app = FastAPI(lifespan=lifespan)

@app.post("/api/chat")
async def chat(
        request: ChatRequest,
        http_request: Request,
) -> ChatResponse:
    llm = http_request.app.state.llm

    messages = [
        {
            "role": "user",
            "content": request.message,
        }
    ]

    response = await llm.chat(messages)

    return ChatResponse(response=response)